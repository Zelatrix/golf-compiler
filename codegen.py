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
        
        # A symbol table for global variables
        # self.global_vars = {}
        
        # The stack for storing the local variables for a function
        self.stack = {}

        # For storing the function headers
        self.fun_headers = {}
        
        # Initialising global format string
        global voidptr_ty
        voidptr_ty = ir.IntType(64).as_pointer()   # Change to i8 because characters are 8-bits
        # voidptr_ty = ir.IntType(8).as_pointer()
        fmt = "%lf \n\0"
        #fmt = "%ld \n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt.encode("utf8")))
        
        global global_fmt
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name="fstr")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        global_fmt.align = 1

        # builder = ir.IRBuilder()
        # builder.position_at_start(self.builder.function.entry_basic_block)
        # self.fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty, name="mybitcast")
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

    # Creates a basic block inside the entry block of the function. 
    # This is the smallest element of a segment of code, which has 
    # no branches leaving it.
    def _create_entry_block_alloca(self, topBuilder):
        saved_block = topBuilder.block
        builder = ir.IRBuilder(topBuilder.function.entry_basic_block)
        var_address = builder.alloca(ir.DoubleType(), size=None)
        # var_address = builder.alloca(ir.IntType(64), size=None)
        # var_address = builder.alloca(ir.IntType(8), size=None)
        topBuilder.position_at_end(saved_block)
        return var_address

    """
    Currently, there is only one scope; the main function
    If more functions are added, this code will always think that
    there is only the main() scope and will always be trying to
    read variables from main() when they're not defined there

    To fix that, something like this:

    def add_variable(self, var_address, var_name, fun):
     current_blk = builder.block     
     if current_blk.name == "main":  
         self.symbol_table[var_name] = var_address
     else:
         self.builder.position_at_start(fun)
         self.symbol_table[var_name] = var_address

    """
    def add_variable(self, var_address, var_name):
        current_blk = self.builder.block
        # print(current_blk)
        self.symbol_table[var_name] = var_address
        # print(self.symbol_table)
    
    # Add a local variable to the stack
    # def _add_local(self, var_address, var_name):
    #     self.stack[var_name] = var_address

    def add_global(self, var_address, var_name):
        dbl_typ = ir.DoubleType()
        gbl = ir.GlobalVariable(self.module, dbl_typ, var_name)
        gbl.linkage = "internal"
        self.global_vars[var_name] = gbl

    # Visitor for integers
    def visit_int(self, value):
        return ir.Constant(ir.DoubleType(), float(value))
        # return ir.Constant(ir.IntType(64), value)
        
        """ -- OOPS --"""
        # dbl_typ = ir.DoubleType()
        # gbl = ir.GlobalVariable(self.module, dbl_typ)
        # global_vars[var_name] = gbl

    # Visitor for integers
    # def visit_int(self, value):
        # return ir.Constant(ir.DoubleType(), float(value))
        # return ir.Constant(ir.IntType(64), value)
        # return ir.Constant(ir.IntType(8), value)


    def visit_float(self, value):
        # return ir.Constant(ir.IntType(8), value)
        return ir.Constant(ir.DoubleType(), float(value))

    # Visitor for Sum
    def visit_sum(self, left, right):
        fadd = self.builder.fadd(left, right)
        return fadd

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
    #def visit_string(self, value):
    #    return value
                
        # """
        # Some useful constants
        # """
        # str_len = len(value)
        # i32 = ir.IntType(32)
        # i8 = ir.IntType(8)
        # # str_const = bytearray(value.encode("utf-8"))
        # # var_ty = ir.Constant(ir.ArrayType(ir.IntType(8), str_len), str_const)

        # current_fn = self.builder.function   # The current function being operated on
        # var_ty = ir.ArrayType(i8, str_len)
        # var_alloc = self.builder.alloca(var_ty)
        # self.builder.gep(var_alloc, [i32(0)])
        # self.builder.ret(i32(0))
        # self.builder.ret_void
        # call = self.builder.call()  # tmp2 = self.builder.call(pf, [self.builder.bitcast(gbl_var, ir.IntType(8).as_pointer())], name="tmp2")
        # gep.attributes.add("nounwind")
        # self.builder.ret(ir.Constant(ir.IntType(32), 0))
        # self.builder.ret_void()   # This is added unconditionally at the end so is not needed

        # entry = self._create_entry_block_alloca(self.builder)
        # print(str(self.module))
        
        # ptr_val = ir.ArrayType(ir.IntType(8), 15)
        # return self.builder.gep(ptr_val, ir.IntType(32)(0))  # The getelementptr instruction
        #                                                      # Computes the index using a pointer
        #                                                      # to an aggregate value


        # The horrible errors go away once you return something from
        # the function

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
        
        # Check if the variable is global or local to a function
        # and put it in the corresponding symbol table 
        # current_blk = self.builder.block
        # if current_blk.name != 'entry':
        self.add_variable(var_address, ident)
        # else:
        #     self.add_global(var_address, ident)

        value = self.visit(value)
        self.builder.store(value, var_address)
        # print([x.value for x in list(self.global_vars.values())])

    # Visitor for using variables
    def visit_var_usage(self, name):
        # var_address = self.symbol_table[name]
        
        # Check if the variable is local or global so 
        # you look in the correct symbol table
        # current_blk = self.builder.block
        # if current_blk.name != 'entry':
        var_address = self.symbol_table[name]
            # var_address = self.stack[name]
        # else:
        #     var_address = self.global_vars[name]

        load_address = self.builder.load(var_address)
        return load_address

    # Visitor for variable reassignment
    def visit_reassign(self, ident, value):
        # Check if the variable is local or global so 
        # you look in the correct symbol table
        # curr_blk = self.builder.block
        # if curr_blk == "function":
        load_address = self.symbol_table[ident]
        # else:
            # load_address = self.global_vars[ident]
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
        # print(self.global_vars)

        if re.match(var_id, value):
            rhs_var = self.symbol_table[value]
            # rhs_var = self.global_vars[value]
            rhs_load = self.builder.load(rhs_var)
        else:
            dbl_val = ir.Constant(ir.DoubleType(), value)          # Convert the number to be added into an LLVM object
            # int_val = ir.Constant(ir.IntType(8), value)

        # var_address = self.global_vars[variable]
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
        fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)
        self.builder.call(self.printf, [fmt_arg, value])

    #def visit_print_str(self, value):
    #    fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)
    #    self.builder.call(self.printstr, [fmt_arg, value])

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
        
        """
        THIS CODE IS UNNECESSARY BECAUSE IT CREATES A SECOND MAIN() FUNCTION
        THIS MEANS THAT WE GET A `DUPLICATENAMEERROR` ON THE FUNCTION MAIN()

        THIS WORKS FINE FOR A SINGLE LOOP, BUT NESTED LOOPS WILL PRODUCE THE
        ABOVE ERROR
        """
        # main_ty = ir.FunctionType(i32, (i8, i64.as_pointer()))
        # main_ty = ir.FunctionType(i32, (ir.DoubleType(), i64.as_pointer()))
        # main_fn = ir.Function(self.module, main_ty, name="main_fn")
        
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
    def visit_fun(self, fn_name, fn_body, ret_ty):
        """ Helpful types """
        i32 = ir.IntType(32)
        i64 = ir.IntType(64)
        i8 = ir.IntType(8)
        dtype = ir.DoubleType()
        void_ty = ir.VoidType()

        # Determine the function's return type and convert to LLVM
        if ret_ty == "void":
            fun_ret = void_ty
        elif ret_ty == "int":
            fun_ret = i64
        elif ret_ty == "float":
            fun_ret = dtype

        """ Function declaration """
        fnty = ir.FunctionType(fun_ret, ())
        fun = ir.Function(self.module, fnty, name=f"{fn_name}")
        self.symbol_table[fn_name] = fun  # Append the function definition to the symbol table
        main_bb = self.builder.block  # Save the `main` basic block to return to it later
        fun_bb = fun.append_basic_block(f"{fn_name}") # Create a basic block for the function body 
        self.builder.position_at_start(fun_bb) # Position the pointer at the start of the basic block

        """
        The body of the function
        """

        # Visit each statement in the function body
        for stmt in fn_body:
            self.visit(stmt)

        # Return a 0 of the correct type if the return type
        # is not void. Else, return void
        if ret_ty == "void":
            self.builder.ret_void()  
        else:
            self.builder.ret(fun_ret(0))

        # Switch back to the main() function
        self.builder.position_at_end(main_bb)

        # print(str(self.module))
        # print(self.symbol_table)
        # print(ret_ty)
    
    # def visit_arguments(self, arg):
    #     self.stack[arg] = "test" 
    #     print("Visited!")
    #     print(self.stack)
    
    # def _create_function_param_alloca(self):
    #     saved_block = topBuilder.block
    #     builder = ir.IRBuilder(self.builder.block)
    #     var_address = builder.alloca(ir.DoubleType(), size=None)
        # var_address = builder.alloca(ir.IntType(64), size=None)
        # var_address = builder.alloca(ir.IntType(8), size=None)
        # topBuilder.position_at_end(saved_block)
        # return var_address

    # Code for declaring functions with >= 1 arguments
    def visit_fargs(self, function, arguments, body, ret_ty):

        """ Helpful types """
        i32 = ir.IntType(32)
        i64 = ir.IntType(64)
        i8 = ir.IntType(8)
        dtype = ir.DoubleType()
        void_ty = ir.VoidType()

        # Determine the function's return type and convert to LLVM
        if ret_ty == "void":
            fun_ret = void_ty
        elif ret_ty == "int":
            fun_ret = i64
        elif ret_ty == "float":
            fun_ret = dtype

        """ Creating the function """

        types = [a.a_type for a in [a for a in arguments if type(a).__name__ == "Arg"]]

        # Making a list of LLVM objects for arguments
        llvm_args = []
        for i in range(len(types)):
            if types[i] == "int":
                llvm_args.append(i32)
            elif types[i] == "float":
                llvm_args.append(dtype)

        # print(func_args)
        # print([type(a) for a in func_args])
        # ptrs = [type(ir.PointerType(a)) for a in llvm_args]
        # print(ptrs)

        # Assigning the LLVM objects as function arguments
        func_args = llvm_args 
        # func_args = ptrs

        fnty = ir.FunctionType(fun_ret, func_args)
        main_bb = self.builder.block 
        fun = ir.Function(self.module, fnty, name=f"{function}")
        self.fun_headers[function] = fun
        
        # Create function basic block
        fun_bb = fun.append_basic_block(f"{function}") # Create a basic block for the function body 
        self.builder.position_at_start(fun_bb) # Position the pointer at the start of the basic block

        lst = list(zip(arguments, fun.args))
        # print(lst)

        # SOLVED ISSUE: `w` is being parsed as an Arg correctly, but not added onto 
        # the stack 

        # Allocate the function arguments onto the stack
        # along with the name of the variable
        for a, x in list(zip(arguments, fun.args)):
            if (type(a).__name__) == "Arg":
                # self.stack[str(a.arg.value)] = x                # key = variable name
                aa = self.builder.alloca(x.type)
                self.symbol_table[str(a.a_name.value)] = aa       # value = IR instruction 
                self.builder.store(x, aa)                         # store the value in the `alloca`

        stack_args = list(zip(self.symbol_table.keys(), llvm_args))
        arg_names = list(a[0] for a in stack_args)

        # Make the arguments to the function have the same name as
        # in the source code instead of using numbers
        for i in range(len(arg_names)):
            fun.args[i].name = arg_names[i]
        
        # In order to be able to use arguments in the body of the function, you need to  
        # pass by reference, which means that we need the argument to be a Pointer()
        # object. To accomplish this, use an alloca() to convert the Argument() object
        # into a Pointer() object

        # allocas = []
        # for v in self.symbol_table.values():
        #     # print(v)
        #     a = self.builder.alloca(v.type)
        #     allocas.append(a)
        #     # print(v.type)
        #     # print(alloc)
        #     print(a.type)
        # print(allocas)

        # print(stack_args)

        # for j in range(len(arg_vals)):
        #     print(fun.args[j][1]) # = arg_vals[j]

        # Comment to test
        # for a, v in stack_args:
        #      global stack_arg
        #      stack_arg = self.builder.alloca(v) # , name=f"{a}") # Allocate one stack slot for each function argument 
             # print(a, stack_arg)
             # argm = self.visit(a)
             # global store_instr
             # print(f"Val: {a}")
             # print(f"Ptr: {type(v)}")
            #  global store_instr
            #  store_instr = self.builder.store(ir.IntType(32)(2), stack_arg) # Store a value in the allocated stack slot 
            #  global load_addr
            #  load_addr = self.builder.load(stack_arg)  # Load the value from `store_instr`


        """ The function body """
        for stmt in body:
            self.visit(stmt)

        # Return a 0 of the correct type if the return type
        # is not void. Else, return void
        if ret_ty == "void":
            self.builder.ret_void()  
        else:
            self.builder.ret(fun_ret(0))
        self.builder.position_at_end(main_bb)

    # Function calls with no arguments
    def visit_fcall(self, function):
        fun = self.symbol_table[function]
        self.builder.call(fun, ())

    """
    THIS FUNCTION TAKES A VALUE, AND WRAPS IT IN AN LLVM OBJECT OF THE
    TYPE DETECTED IN THE FUNCTION SIGNATURE  
    """

    # Visitor for functions with >= 1 argument
    def visit_call_args(self, fn_name, fn_args):
        
        """
        This function wraps a given value in an LLVM type

        Declaring the function inside another function means that
        this function is accessible withi the scope of the outer
        function 
        """
        def type_arg(value: int, typ):
            return typ(value)
        
        fun = self.fun_headers[fn_name]  # Retrieving the function header
        arg_list = [i.value for i in fn_args] # Retrieving the function arguments
        types = [type(i) for i in fn_args]
        typed = [type_arg(n, ir.DoubleType()) for n in arg_list]
    
        self.builder.call(fun, (typed))
        # print(self.fun_headers)

    # Return a value from the function
    # No need to account for `void` since that means no return type
    def visit_return(self, ret_val):
       self.builder.ret(ret_val)

    # Declare the function that is used for printing text to the console.
    def _declare_print_function(self):
        voidptr_ty = ir.IntType(64).as_pointer()
        # voidptr_ty = ir.DoubleType().as_pointer()
        printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
        # printf_ty = ir.FunctionType(ir.IntType(32), [ir.IntType(8).as_pointer()], var_arg=True)
        printf = ir.Function(self.module, printf_ty, name="printf")
        # printf.linkage = "dso_local"  # Define the linkage as dso_local
        self.printf = printf

    # Print for strings
    # def _declare_str_print_function(self):
    #      voidptr_ty = ir.IntType(8).as_pointer()
    #      str_ty = ir.FunctionType(ir.IntType(32), [ir.IntType(8).as_pointer()], var_arg=True)
    #      # str_ty = ir.FunctionType(ir.ArrayType(ir.IntType(8), 15), [voidptr_ty], var_arg=True)
    #      printstr = ir.Function(self.module, str_ty, name="printstr")
    #      self.printstr = printstr

    # print(self.symbol_table)

    def _compile_ir(self):
        self.builder.ret_void()

    def create_ir(self):
        self._compile_ir()

    def save_ir(self, filename):
        # print(str(self.module))
        # print(self.symbol_table)
        # print(self.global_vars)

        # Open a file and write the IR into it
        with open(filename, "w") as output_file:
            output_file.write(str(self.module))
