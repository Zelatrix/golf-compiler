from llvmlite import ir, binding
from ast import Visitor

class CodeGen(Visitor):
# Initialise all the necessary variables that are used by LLVM
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
         var_addr = builder.alloca(ir.DoubleType(), size=None)
         topBuilder.position_at_end(saved_block)
         return var_addr

    def add_variable(self, var_addr, var_name):
        self.symbol_table[var_name] = var_addr
        # print(self.symbol_table)

    # Visitor for integers
    def visit_int(self, value):
        i = ir.Constant(ir.DoubleType(), float(value))
        return i

    def visit_float(self, value):
        i = ir.Constant(ir.DoubleType(), float(value))
        return i

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
    def visit_string(self, value):
        printf = ir.Function(self.module, )

        string_addr = self._create_entry_block_alloca(self.builder)
        indices = ir.Constant(ir.ArrayType(ir.IntType(8), 8), 8) # unsure about this line
        value = self.builder.gep(string_addr, indices)
        self.builder.call(printf, value) # unsure about this line
        self.builder.ret(ir.Constant(ir.IntType(32), 0))
        return value


    # Visitor for UDFs
    def visit_udf(self, name, args):
        pass

    # Visitor for variables
    def visit_var_dec(self, ident, value):
        var_addr = self._create_entry_block_alloca(self.builder)
        self.add_variable(var_addr, ident)
        value = self.visit(value)
        self.builder.store(value, var_addr)

    # Visitor for using variables
    def visit_var_usage(self, name):
        var_addr = self.symbol_table[name]
        return self.builder.load(var_addr)

    # Visitor for Print
    def visit_print(self, value):
        # if not(self.print_initialised):
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
