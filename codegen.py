from llvmlite import ir, binding
from my_ast import Visitor
import re

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
        # self._declare_str_print_function()
        self.print_initialised = False
        self.symbol_table = {}
        # print(self.symbol_table)

        voidptr_ty = ir.IntType(64).as_pointer()   # Change to i8 because characters are 8-bits
        # voidptr_ty = ir.IntType(8).as_pointer()
        fmt = "%lf \n\0"
        # fmt = "%ld \n\0"
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
        #print(base_func)
        #print(block)

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
        # var_address = builder.alloca(ir.IntType(8), size=None)
        topBuilder.position_at_end(saved_block)
        return var_address

    def add_variable(self, var_address, var_name):
        self.symbol_table[var_name] = var_address
        # print(self.symbol_table)

    # Visitor for integers
    def visit_int(self, value):
        return ir.Constant(ir.DoubleType(), float(value))
        # return ir.Constant(ir.IntType(8), value)


    def visit_float(self, value):
        # return ir.Constant(ir.IntType(8), value)
        return ir.Constant(ir.DoubleType(), float(value))

    # Visitor for Sum
    def visit_sum(self, left, right):
        fadd = self.builder.fadd(left, right)
        # add = self.builder.add(left, right)
        # print(str(self.module))
        # self.builder.ret_void()
        return fadd
        # return add

    # Visitor for Sub
    def visit_sub(self, left, right):
        return self.builder.fsub(left, right)

    # Visitor for Mult
    def visit_mult(self, left, right):
        return self.builder.fmul(left, right)

    # Visitor for Div
    def visit_div(self, left, right):
        # r = self.visit(right)
        # r = self.builder.sitofp(right, ir.DoubleType())
        # zero = self.builder.sitofp(float(0.0), ir.DoubleType())
        # if self.builder.fcmp_ordered("==", r, zero):
        # if right is Integer(self.builder, self.module, str(0)) or right is Float(self.builder, self.module, str(0.0)):
            # print(r)
            # return ZeroDivisionError("Stop trying to break mathematics!")
        # else:
            # print(r)
            # return visitor.visit_div(left, right)
        return self.builder.fdiv(left, right)

        # Craft a regular expresison to determine what 
        # # the RHS is
        # var_id = re.compile(r"[A-Za-z_]([A-Za-z_0-9])*")
        
        # if re.match(var_id, value):
        #     rhs_var = self.symbol_table[value]
        #     rhs_load = self.builder.load(rhs_var)
        # else:
        #     dbl_val = ir.Constant(ir.DoubleType(), value)      # Convert the number to be added into an LLVM object

        # var_address = self.symbol_table[variable]              # Get the value and load it into memory
        # load_instr = self.builder.load(var_address)
        
        # if re.match(var_id, value):
        #     incremented = self.builder.fadd(load_instr, rhs_load)  # Decrement the variable's value by the specified amount
        # else:
        #     incremented = self.builder.fadd(load_instr, dbl_val)   # Decrement the variable's value by the specified amount
        # self.builder.store(incremented, var_address)               # Store the result back into memory to replace the old value
        # return incremented


    # Visitor for Modulus
    def visit_mod(self, left, right):
        return self.builder.frem(left, right)
        
        # # if not(re.match(var_side, left)) or not(re.match(var_side, right)):
        # #     return self.builder.frem(left, right)
        # if re.match(var_side, str(left)):
        #     add = self.symbol_table[left]
        #     v = self.builder.load(add)
        #     return self.builder.frem(v, right)
        # # else if:
        # #     add = self.symbol_table[right]
        # #     v = self.builder.load(add)
        # #     return self.builder.frem(left, v)


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
    def visit_string(self, value):

        """
        Some useful constants
        """
        str_len = len(value)
        i32 = ir.IntType(32)
        i8 = ir.IntType(8)
        # str_const = bytearray(value.encode("utf-8"))
        # var_ty = ir.Constant(ir.ArrayType(ir.IntType(8), str_len), str_const)

        current_fn = self.builder.function   # The current function being operated on
        var_ty = ir.ArrayType(i8, str_len)
        var_alloc = self.builder.alloca(var_ty)
        self.builder.gep(var_alloc, [i32(0)])
        # call = self.builder.call()  # tmp2 = self.builder.call(pf, [self.builder.bitcast(gbl_var, ir.IntType(8).as_pointer())], name="tmp2")
        # gep.attributes.add("nounwind")
        # self.builder.ret(ir.Constant(ir.IntType(32), 0))
        # self.builder.ret_void()   # This is added unconditionally at the end so is not needed

        # entry = self._create_entry_block_alloca(self.builder)
        print(str(self.module))
        
        # ptr_val = ir.ArrayType(ir.IntType(8), 15)
        # return self.builder.gep(ptr_val, ir.IntType(32)(0))  # The getelementptr instruction
        #                                                      # Computes the index using a pointer
        #                                                      # to an aggregate value


        # The horrible errors go away once you return something from
        # the function

        """
        Some useful constants
        """
        # str_len = len(value)
        # i32 = ir.IntType(32)
        # i8 = ir.IntType(8)
        # str_const = bytearray(value.encode("utf-8"))
        # var_ty = ir.Constant(ir.ArrayType(ir.IntType(8), str_len), str_const)

        # current_fn = self.builder.function   # The current function being operated on
        # self.builder.call()
        # fnty = ir.FunctionType(i32, str_const)
        # ir.Constant(ir.ArrayType(ir.IntType(8), str_len), str_const)
        # self.builder.ret(i32(0)) # Return the value of 0
        # self.builder.ret_void()
        # return 0
        # print(str(self.module))
        # entry = self._create_entry_block_alloca(self.builder)
        # print(entry)


        # # print(var_ty)
        # # print(var_ty.type)

        # gbl_var = ir.GlobalVariable(self.module, var_ty.type, name="gbl_var")

        # # Setting up the string
        # # gep_arg1: used as basis for calculations
        # # gep_arg2: pointer or vector of pointers - base starting addr

        # # gep_arg1 = ir.ArrayType(i8, str_len)
        # # print(gep_arg1)
        # # gep_arg2 = gep_arg1.as_pointer()
        # # print(gep_arg2)

        # # gep_const1 = ir.PointerType(ir.ArrayType(i8, str_len))
        # # gep_const2 = [ir.Constant(ir.PointerType(ir.ArrayType(i8, str_len)), gep_arg2)]

        # """
        # Defining the print function
        # """
        # pf_ty = ir.FunctionType(i32, [i8.as_pointer()], var_arg=True)
        # pf = ir.Function(self.module, pf_ty, name="printf_str")
        # print(pf)

        # """
        # Defining the main function
        # """
        # main_ty = ir.FunctionType(i32, (i32, i8), var_arg=False)
        # main_fun = ir.Function(self.module, main_ty, name="main_fn")
        # main_fun.attributes.add("nounwind")
        # entry_bb = main_fun.append_basic_block(name="entry")

        # with self.builder.goto_block(entry_bb):
        #     # print(type(var_ty))
        #     # vtp = var_ty
        #     # print(vtp)
        #     # tmp1 = self.builder.gep(var_ty, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])  # I don't understand how to use this instruction
        #     # tmp2 = self.builder.call(pf, tmp1, name="tmp2")
        #     # print(tmp1)
        #     tmp2 = self.builder.call(pf, [self.builder.bitcast(gbl_var, ir.IntType(8).as_pointer())], name="tmp2")
        #     tmp2.attributes.add("nounwind")
        #     self.builder.ret(ir.Constant(ir.IntType(32), 0))

        # print(main_fun)
        # return main_fun

    # Visitor for UDFs
    # def visit_udf(self, name, args):
    #     pass

    # Visitor for arrays (contiguous blocks of memory)
    def visit_array(self, count):
        # print("Done!")  # debug info
        arr_ty = ir.ArrayType(ir.IntType(32), count)
        # print(arr_ty)
        return self.builder.alloca(arr_ty)

    # Retrieve the value from that index in the specified array
    def visit_array_access(self):
        pass
    
    # Assign a value to a space in an array
    def visit_array_assign(self):
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

    def visit_increment(self, variable, value):
        # Craft a regular expresison to determine what 
        # the RHS is
        var_id = re.compile(r"[A-Za-z_]([A-Za-z_0-9])*")
        
        if re.match(var_id, value):
            rhs_var = self.symbol_table[value]
            rhs_load = self.builder.load(rhs_var)
        else:
            dbl_val = ir.Constant(ir.DoubleType(), value)          # Convert the number to be added into an LLVM object
            # int_val = ir.Constant(ir.IntType(8), value)

        var_address = self.symbol_table[variable]                  # Get the value and load it into memory
        load_instr = self.builder.load(var_address)
        
        if re.match(var_id, value):
            incremented = self.builder.fadd(load_instr, rhs_load)  # Decrement the variable's value by the specified amount
        else:
            incremented = self.builder.fadd(load_instr, dbl_val)    # Decrement the variable's value by the specified amount
            # incremented = self.builder.add(load_instr, int_val)
        self.builder.store(incremented, var_address)               # Store the result back into memory to replace the old value
        return incremented
        
        # dbl_val = ir.Constant(ir.DoubleType(), val)           # Convert the number to be added into an LLVM object
        # var_address = self.symbol_table[variable]             # Get the value and load it into memory
        # load_instr = self.builder.load(var_address)
        # incremented = self.builder.fadd(load_instr, dbl_val)  # Increment the variable's value by the specified amount
        # self.builder.store(incremented, var_address)          # Store the result back into memory to replace the old value
        # return incremented

    def visit_decrement(self, variable, value):
        # Craft a regular expresison to determine what 
        # the RHS is
        var_id = re.compile(r"[A-Za-z_]([A-Za-z_0-9])*")
        
        if re.match(var_id, value):
            rhs_var = self.symbol_table[value]
            rhs_load = self.builder.load(rhs_var)
        else:
            dbl_val = ir.Constant(ir.DoubleType(), value)      # Convert the number to be added into an LLVM object

        var_address = self.symbol_table[variable]              # Get the value and load it into memory
        load_instr = self.builder.load(var_address)
        
        if re.match(var_id, value):
            decremented = self.builder.fsub(load_instr, rhs_load)  # Decrement the variable's value by the specified amount
        else:
            decremented = self.builder.fsub(load_instr, dbl_val)   # Decrement the variable's value by the specified amount
        self.builder.store(decremented, var_address)               # Store the result back into memory to replace the old value
        return decremented
        
        
        # dbl_val = ir.Constant(ir.DoubleType(), value)         # Convert the number to be added into an LLVM object
        # var_address = self.symbol_table[variable]             # Get the value and load it into memory
        # load_instr = self.builder.load(var_address)
        # decremented = self.builder.fsub(load_instr, dbl_val)  # Decrement the variable's value by the specified amount
        # self.builder.store(decremented, var_address)          # Store the result back into memory to replace the old value
        # return decremented

    def visit_timeseq(self, variable, value):
        # Craft a regular expresison to determine what 
        # the RHS is
        var_id = re.compile(r"[A-Za-z_]([A-Za-z_0-9])*")
        
        if re.match(var_id, value):
            rhs_var = self.symbol_table[value]
            rhs_load = self.builder.load(rhs_var)
        else:
            dbl_val = ir.Constant(ir.DoubleType(), value)      # Convert the number to be added into an LLVM object

        var_address = self.symbol_table[variable]              # Get the value and load it into memory
        load_instr = self.builder.load(var_address)
        
        if re.match(var_id, value):
            timeseq = self.builder.fmul(load_instr, rhs_load)  # Decrement the variable's value by the specified amount
        else:
            timeseq = self.builder.fmul(load_instr, dbl_val)   # Decrement the variable's value by the specified amount
        self.builder.store(timeseq, var_address)               # Store the result back into memory to replace the old value
        return timeseq

    def visit_diveq(self, variable, value):
        # Craft a regular expresison to determine what 
        # the RHS is
        var_id = re.compile(r"[A-Za-z_]([A-Za-z_0-9])*")
        
        if re.match(var_id, value):
            rhs_var = self.symbol_table[value]
            rhs_load = self.builder.load(rhs_var)
        else:
            dbl_val = ir.Constant(ir.DoubleType(), value)      # Convert the number to be added into an LLVM object

        var_address = self.symbol_table[variable]              # Get the value and load it into memory
        load_instr = self.builder.load(var_address)
        
        if re.match(var_id, value):
            diveq = self.builder.fdiv(load_instr, rhs_load)  # Decrement the variable's value by the specified amount
        else:
            diveq = self.builder.fdiv(load_instr, dbl_val)   # Decrement the variable's value by the specified amount
        self.builder.store(diveq, var_address)               # Store the result back into memory to replace the old value
        return diveq
        
        #############################################

        # dbl_val = ir.Constant(ir.DoubleType(), value)         # Convert the number to be added into an LLVM object
        # var_address = self.symbol_table[variable]             # Get the value and load it into memory
        # load_instr = self.builder.load(var_address)
        # diveq = self.builder.fdiv(load_instr, dbl_val)        # Decrement the variable's value by the specified amount
        # self.builder.store(diveq, var_address)                # Store the result back into memory to replace the old value
        # return diveq

    # Visitor for Print
    def visit_print(self, value):
        # if value.type == 
        self.builder.call(self.printf, [self.fmt_arg, value])

    # def visit_print_str(self, value):
    #     self.builder.call(self.printf_str, [self.fmt_arg, value])

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

    def visit_else(self, else_body):
        for stmt in else_body:
            self.visit(stmt)

#loop_entry = func.append_basic_block('loop_start')
#builder.branch(loop_entry)
#builder.goto_block(loop_entry)
#with builder.if_then(cond) as then:
#    # Gen loop body
#    builder.branch(loop_entry)

    """
        The while loop works by checking the condition each time through the loop
        and if the condition is true, run the body of the loop. If it is false, 
        then exit the loop. As long as the condition is true, jump back to the 
        beginning of the loop
    """

    def visit_while(self, predicate, body):
        """
        Some useful constants
        """

        i64 = ir.IntType(64)
        i32 = ir.IntType(32)
        i8 = ir.IntType(8)

        """
        Defining and building the main() function
        """
        
        current_fn = self.builder.function  # The current function being operated on in the basic block
        # main_ty = ir.FunctionType(i32, (i8, i64.as_pointer()))
        main_ty = ir.FunctionType(i32, (ir.DoubleType(), i64.as_pointer()))
        main_fn = ir.Function(self.module, main_ty, name="main_fn")
        
        loop_entry = current_fn.append_basic_block('loop_start')
        self.builder.branch(loop_entry)
        self.builder.position_at_end(loop_entry)  # self.builder.goto_block(loop_entry)

        p = self.visit(predicate)
        bool_cond = self.builder.fptosi(p, ir.IntType(1))

        # print(str(self.module))
        with self.builder.if_then(bool_cond) as then:
            p = self.visit(predicate)
            new_cond = self.builder.fptosi(p, ir.IntType(1))
             
            for stmt in body:
                self.visit(stmt) # Gen loop body
            self.builder.branch(loop_entry)   
            
    # Visitor for functions with no arguments
    def visit_fun(self, fn_name, fn_body):
        """ Helpful types """
        i32 = ir.IntType(32)
        i64 = ir.IntType(64)
        i8 = ir.IntType(8)
        dtype = ir.DoubleType()

        """ Function declaration """
        fnty = ir.FunctionType(i64, ())
        fun = ir.Function(self.module, fnty, name=f"{fn_name}")
        main_bb = self.builder.block  # Save the `main` basic block to return to it later
        fun_bb = fun.append_basic_block("function") # Create a basic block for the function body 
        self.builder.position_at_start(fun_bb) # Position the pointer at the start of the basic block

        """
        The body of the function
        """
        # x = ir.Constant(i8, 2)
        # # x2 = self.builder.alloca(x)
        # y = ir.Constant(i8, 3)
        # res = self.builder.add(x, y)
        # self.builder.call(self.printf, [self.fmt_arg, res])  # print(res)
        # # self.builder.ret(ir.Constant(dtype, float(0)))
        # self.builder.ret(ir.Constant(i64, 0))

        # Visit each statement in the function body
        for stmt in fn_body:
            self.visit(stmt)
        self.builder.ret(ir.IntType(64)(0))  # Return 0 from the function to terminate the block

        # Switch back to the main() function
        self.builder.position_at_end(main_bb)

        print(str(self.module))
        # print(self.symbol_table)

        # self.builder.ret(i32(0))
        # for stmt in fun_bb:
        #     self.visit(stmt)
        
        # self.symbol_table[fn_name] = fun
        # return fun
        # print(self.symbol_table)

        # for stmt in fn_body:
        #     self.visit(stmt)
        # self.builder.ret(i32(0))
        # self.builder.position_at_end(fun_bb)

        # print(str(self.module))

        # void_ty = ir.IntType(64).as_pointer()
        # typ = ir.FunctionType(ir.IntType(32), [ir.DoubleType()])
        # fun = ir.Function(self.module, typ, name=fn_name)
        # print(str(self.module))
        # print("Seen!")

    # Code for functions with < 1 arguments
    def visit_fargs(self, function, arguments):
        pass

    def visit_fcall(self, function):
        pass
        # fnty = ir.FunctionType(ir.DoubleType(), ())
        # function = ir.Function(self.module, fnty, name=f"{function}")
        # fun = self.symbol_table[function]
        # self.builder.call(fun, ())
        # print(self.symbol_table)

    # Visitor for functions with > 1 argument
    # def visit_fun_args(self, fn_name):
    #     pass

    # Return a value from the function
    def visit_return(self, ret_val):
       self.builder.ret(ret_val)

    #def visit_conj_spec(self):
    #    print("Visited!")

    #def visit_specification(self):
    #    print("Visited!")

    # Declare the function that is used for printing text to the console.
    def _declare_print_function(self):
        voidptr_ty = ir.IntType(64).as_pointer()
        # voidptr_ty = ir.DoubleType().as_pointer()
        printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
        # printf_ty = ir.FunctionType(ir.IntType(32), [ir.IntType(8).as_pointer()], var_arg=True)
        printf = ir.Function(self.module, printf_ty, name="printf")
        self.printf = printf

    # Print for strings
    # def _declare_str_print_function(self):
    #     voidptr_ty = ir.IntType(64).as_pointer()
    #     str_ty = ir.FunctionType(ir.ArrayType(ir.IntType(8), 15), [voidptr_ty], var_arg=True)
    #     printf_str = ir.Function(self.module, str_ty, name="printf_str")
    #     self.printf_str = printf_str

    def _compile_ir(self):
        self.builder.ret_void()
        llvm_ir = str(self.module)
        # print(llvm_ir)
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
