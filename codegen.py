from llvmlite import ir, binding
from my_ast import Visitor
from WhileContextManager import while_loop

# Initialise all the necessary variables that are used by LLVM
class CodeGen(Visitor):
    def __init__(self):
        self.binding = binding
        self.binding.initialize()
        self.binding.initialize_native_target()
        self.binding.initialize_native_asmprinter()
        self._config_llvm()
        self._create_execution_engine()
        self._declare_print_function()
        self.print_initialised = False
        self.symbol_table = {}

        voidptr_ty = ir.IntType(64).as_pointer()
        fmt = "%lf \n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt.encode("utf8")))
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name="fstr")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        # builder = ir.IRBuilder()
        # builder.position_at_start(self.builder.function.entry_basic_block)
        self.fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)
        self.print_initialised = True

    # Configure LLVM with the required parameters.
    def _config_llvm(self):
        self.module = ir.Module(name=__file__)
        self.module.triple = self.binding.get_default_triple()
        func_type = ir.FunctionType(ir.VoidType(), [])
        base_func = ir.Function(self.module, func_type, name="main")
        block = base_func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

    def _create_execution_engine(self):
        target = self.binding.Target.from_default_triple()
        target_machine = target.create_target_machine()
        backing_mod = binding.parse_assembly("")
        engine = binding.create_mcjit_compiler(backing_mod, target_machine)
        self.engine = engine

    # Creates a basic block. This is the smallest element of a segment
    # of code, which has no branches leaving it.
    def _create_entry_block_alloca(self, topBuilder):
        saved_block = topBuilder.block
        builder = ir.IRBuilder(topBuilder.function.entry_basic_block)
        var_address = builder.alloca(ir.DoubleType(), size=None)
        topBuilder.position_at_end(saved_block)
        return var_address

    def add_variable(self, var_address, var_name):
        self.symbol_table[var_name] = var_address
        # print(self.symbol_table)

    # Visitor for integers
    def visit_int(self, value):
        return ir.Constant(ir.DoubleType(), float(value))

    def visit_float(self, value):
        return ir.Constant(ir.DoubleType(), float(value))

    # Visitor for Sum
    def visit_sum(self, left, right):
        return self.builder.fadd(left, right)

    # Visitor for Sum
    def visit_sub(self, left, right):
        return self.builder.fsub(left, right)

    # Visitor for Mult
    def visit_mult(self, left, right):
        return self.builder.fmul(left, right)

    # Visitor for Div
    def visit_div(self, left, right):
        return self.builder.fdiv(left, right)

    # Visitor for Modulus
    def visit_mod(self, left, right):
        return self.builder.frem(left, right)

    # Visitor for unary negation
    def visit_uneg(self, value):
        return self.builder.fsub(ir.Constant(ir.DoubleType(), float(0)), value)

    # Visitor for Equal
    def visit_eq(self, left, right):
        l = self.builder.sitofp(left, ir.DoubleType())
        r = self.builder.sitofp(right, ir.DoubleType())
        res = self.builder.fcmp_ordered("==", l, r)
        return self.builder.uitofp(res, ir.DoubleType())

    # Visitor for NotEqual
    def visit_neq(self, left, right):
        l = self.builder.sitofp(left, ir.DoubleType())
        r = self.builder.sitofp(right, ir.DoubleType())
        res = self.builder.fcmp_ordered("!=", l, r)
        return self.builder.uitofp(res, ir.DoubleType())

    # Visitor for LessThan
    def visit_lt(self, left, right):
        l = self.builder.sitofp(left, ir.DoubleType())
        r = self.builder.sitofp(right, ir.DoubleType())
        res = self.builder.fcmp_ordered("<", l, r)
        return self.builder.uitofp(res, ir.DoubleType())

    # Visitor for GreaterThan
    def visit_gt(self, left, right):
        l = self.builder.sitofp(left, ir.DoubleType())
        r = self.builder.sitofp(right, ir.DoubleType())
        res = self.builder.fcmp_ordered(">", l, r)
        return self.builder.uitofp(res, ir.DoubleType())

    # Visitor for LessEqual
    def visit_lte(self, left, right):
        l = self.builder.sitofp(left, ir.DoubleType())
        r = self.builder.sitofp(right, ir.DoubleType())
        res = self.builder.fcmp_ordered("<=", l, r)
        return self.builder.uitofp(res, ir.DoubleType())

    # Visitor for GreaterEqual
    def visit_gte(self, left, right):
        l = self.builder.sitofp(left, ir.DoubleType())
        r = self.builder.sitofp(right, ir.DoubleType())
        res = self.builder.fcmp_ordered(">=", l, r)
        return self.builder.uitofp(res, ir.DoubleType())

    # Visitor for AND
    def visit_and(self, left, right):
        l = self.builder.fptosi(left, ir.IntType(64))
        r = self.builder.fptosi(right, ir.IntType(64))
        res = self.builder.and_(l, r)
        return self.builder.uitofp(res, ir.DoubleType())

    # Visitor for OR
    def visit_or(self, left, right):
        l = self.builder.fptosi(left, ir.IntType(64))
        r = self.builder.fptosi(right, ir.IntType(64))
        res = self.builder.or_(l, r)
        return self.builder.uitofp(res, ir.DoubleType())

    # Visitor for NOT
    def visit_not(self, value):
        v = self.builder.fptosi(value, ir.IntType(1))
        res = self.builder.not_(v)
        return self.builder.uitofp(res, ir.DoubleType())

    # Visitor for strings
    def visit_string(self, value, length):
        pass
        # """
        # Helpful constants
        # """
        # # tmp2_args = None
        # # str_len = ir.ArrayType(ir.IntType(8), length)  # An array of 8-bit integers the length of the string
        # i32 = ir.IntType(32)  # An alias for 32-bit integers
        # # binding.ValueRef.linkage = "internal"  # Setting the linkage type to internal
        #
        # # str_len = int(length)
        # # str_const = ir.Constant(ir.ArrayType(ir.IntType(8), str_len), value)  # Internal string constant
        # # print(str_const)
        #
        # """
        # Defining the printf function
        # """
        #
        # # If var_arg = True, then the function takes a variable number of arguments
        # printf_ty = ir.FunctionType(i32, [ir.IntType(8).as_pointer()], var_arg=True)
        # string_printf = ir.Function(self.module, printf_ty, name="str_printf").is_declaration
        # return string_printf
        #
        # # Setting is_declaration = True tells LLVM that it is a declaration
        # # and not a definition of a complete function; just the header.
        # # string_printf.is_declaration
        #
        # """
        # Defining the main function
        # """
        # fnty = ir.FunctionType(i32, [ir.IntType(8).as_pointer()])  # The type of the function
        # func = ir.Function(self.module, fnty, name="str_main")
        # argc, argv = func.args
        #
        # """
        # The function implementation
        # """
        # block = func.append_basic_block(name="entry")
        # builder = ir.IRBuilder(block)
        # builder.gep(str_len, str_len.as_pointer(), str_const, name="tmp1")
        # builder.call(string_printf, tmp2_args, name="tmp2")
        # builder.ret(ir.Constant(ir.IntType(32), 0))

    # Visitor for characters
    # def visit_char(self, value):
    #     pass

    # Visitor for UDFs
    def visit_udf(self, name, args):
        pass

    # Visitor for variables
    def visit_var_dec(self, ident, value):
        var_address = self._create_entry_block_alloca(self.builder)
        self.add_variable(var_address, ident)
        value = self.visit(value)
        self.builder.store(value, var_address)

    # Visitor for using variables
    def visit_var_usage(self, name):
        var_address = self.symbol_table[name]
        load_address = self.builder.load(var_address)
        return load_address

    # Visitor for variable reassignment
    def visit_reassign(self, ident, value):
        load_address = self.symbol_table[ident]
        value = self.visit(value)
        self.builder.store(value, load_address)

    # ---- BUG SOLVED ----
    # There is a bug here, which causes the value to be loaded into memory twice
    # I suspect it's because var_usage also loads it into memory, and incrementing
    # the variable's value gets parsed as a variable usage.

    # The issue is that it needs to be loaded into memory inside visit_increment
    # so that it can be used inside the `fadd` instruction.

    # Solution: https://llvm.discourse.group/t/implementing-in-llvm-ir/3744

    def visit_increment(self, variable, val):
        dbl_val = ir.Constant(ir.DoubleType(), val)           # Convert the number to be added into an LLVM object
        var_address = self.symbol_table[variable]             # Get the value and load it into memory
        load_instr = self.builder.load(var_address)
        incremented = self.builder.fadd(load_instr, dbl_val)  # Increment the variable's value by the specified amount
        self.builder.store(incremented, var_address)          # Store the result back into memory to replace the old value
        return incremented

    def visit_decrement(self, variable, value):
        dbl_val = ir.Constant(ir.DoubleType(), value)         # Convert the number to be added into an LLVM object
        var_address = self.symbol_table[variable]             # Get the value and load it into memory
        load_instr = self.builder.load(var_address)
        decremented = self.builder.fsub(load_instr, dbl_val)  # Decrement the variable's value by the specified amount
        self.builder.store(decremented, var_address)          # Store the result back into memory to replace the old value
        return decremented

    def visit_timeseq(self, variable, value):
        dbl_val = ir.Constant(ir.DoubleType(), value)         # Convert the number to be added into an LLVM object
        var_address = self.symbol_table[variable]             # Get the value and load it into memory
        load_instr = self.builder.load(var_address)
        timeseq = self.builder.fmul(load_instr, dbl_val)      # Decrement the variable's value by the specified amount
        self.builder.store(timeseq, var_address)              # Store the result back into memory to replace the old value
        return timeseq

    def visit_diveq(self, variable, value):
        dbl_val = ir.Constant(ir.DoubleType(), value)         # Convert the number to be added into an LLVM object
        var_address = self.symbol_table[variable]             # Get the value and load it into memory
        load_instr = self.builder.load(var_address)
        diveq = self.builder.fdiv(load_instr, dbl_val)        # Decrement the variable's value by the specified amount
        self.builder.store(diveq, var_address)                # Store the result back into memory to replace the old value
        return diveq

    # Visitor for Print
    def visit_print(self, value):
        self.builder.call(self.printf, [self.fmt_arg, value])

    # Visitor for if-then statements
    def visit_if(self, pred, body):
        p = self.visit(pred)
        bool_cond = self.builder.fptosi(p, ir.IntType(1))
        with self.builder.if_then(bool_cond):
            for stmt in body:
                self.visit(stmt)

    # Visitor for if-else statements
    def visit_if_else(self, pred, if_body, else_body):
        p = self.visit(pred)
        bool_cond = self.builder.fptosi(p, ir.IntType(1))
        with self.builder.if_else(bool_cond) as (then, otherwise):
            with then:
                for stmt in if_body:
                    self.visit(stmt)
            with otherwise:
                for stmt in else_body:
                    self.visit(stmt)

    # ------ This is the kind of thing needed to implement while loops ------------
    # LLVMBasicBlockRef while_body = LLVMAppendBasicBlock(function, "while_body");
    # LLVMBasicBlockRef while_merge = LLVMAppendBasicBlock(function, "while_merge");
    # LLVMBuildCondBr(builder, lower_bexp(ast->children[2]), while_body, while_merge);
    # LLVMPositionBuilderAtEnd(builder, while_body);

    """
    The while loop works by checking the condition each time through the loop
    and if the condition is true, run the body of the loop. If it is false, 
    then exit the loop. As long as the condition is true, jump back to the 
    beginning of the loop
    """

    # int x = 10;
    # START: if (x > 0) {
    #   printf("%d\n", x);
    #   x -= 1;
    #   goto START;
    # }

    # Visitor for while loops
    def visit_while(self, predicate, body):

        i32 = ir.IntType(32)
        fnty = ir.FunctionType(i32, ())
        main_fn = ir.Function(self.module, fnty, name="main_fn")

        # Creating the basic blocks
        bb = self.builder.basic_block
        # entry_bb = main_fn.append_basic_block("entry")
        bb_cond = main_fn.append_basic_block("entry.cond")
        bb_if = main_fn.append_basic_block("entry.if")
        bb_end = main_fn.append_basic_block("entry.endif")
        self.builder.branch(bb_cond)

        # Prepare the variables to enter the loop
        # with self.builder.goto_block(entry_bb):
        #     # for instr in list(bb):
        #     pass

        with self.builder.goto_block(bb_cond):
            p = self.visit(predicate)
            bool_cond = self.builder.fptosi(p, ir.IntType(1))  # The Boolean condition for continuing the loop
            self.builder.cbranch(bool_cond, bb_if, bb_end)

        with self.builder.goto_block(bb_if):
            for stmt in body:
                self.visit(stmt)
            self.builder.branch(bb_cond)

        # Insert a `ret void` instruction into the basic block `entry.endif`
        # and move the pointer back to its original location
        with self.builder.goto_block(bb_end):
            self.builder.ret_void()

        # print(entry_bb)
        print("This is the entry block:")
        print(bb)

        print()
        print("This is the main function:")
        print(main_fn)
        # print(bb_cond)
        # print(bb_if)
        # print(bb_end)

    # Declare the function that is used for printing text to the console.
    def _declare_print_function(self):
        voidptr_ty = ir.IntType(64).as_pointer()
        printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
        printf = ir.Function(self.module, printf_ty, name="printf")
        self.printf = printf

    def _compile_ir(self):
        self.builder.ret_void()
        llvm_ir = str(self.module)
        mod = self.binding.parse_assembly(llvm_ir)
        mod.verify()
        self.engine.add_module(mod)
        self.engine.finalize_object()
        self.engine.run_static_constructors()
        return mod

    # Create and save the .ll file that contains the intermediate
    # representation for the compiled program
    def create_ir(self):
        self._compile_ir()

    def save_ir(self, filename):
        with open(filename, "w") as output_file:
            output_file.write(str(self.module))
