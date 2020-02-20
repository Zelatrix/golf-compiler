from llvmlite import ir
# from codegen import llvm_printf

class Visitor:
    def visit(self, visitor):
        return visitor.accept(self)

# The general binary operator type
class BinaryOp:
    def __init__(self, builder, module, left, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right

class Number():
    def __init__(self, builder, module, value):
        self.value = value
        self.builder = builder
        self.module = module

# Integers
class Integer(Number):
    def __eq__(self, other):
        if not isinstance(other, Integer):
            return NotImplemented
        else:
            return self.value == other.value

    def accept(self, visitor):
        return visitor.visit_int

    # def compile(self):
        # i = ir.Constant(ir.IntType(64), int(self.value))
        # return i
        # var_addr = _create_entry_block_alloca(self.builder)
        # self.builder.store(i, var_addr)
        # return self.builder.load(var_addr)

# Floating point numbers
class Float(Number):
    def __eq__(self, other):
        if not isinstance(other, Float):
            return NotImplemented
        else:
            return self.value == other.value

    def accept(self, visitor):
        return visitor.visit_float

    # def compile(self):
        # i = ir.Constant(ir.FloatType(), float(self.value))
        # return i

# Defining the addition operation
class Sum(BinaryOp):
    def accept(self, visitor):
        return visitor.visit_sum(self)

    # def compile(self):
        # if isinstance(self.left, Integer) and isinstance(self.right, Integer):
        #     i = self.builder.add(self.left.compile(), self.right.compile())
        # # elif isinstance(self.left, Float) and isinstance(self.right, Float):
        # #     i = self.builder.fadd(self.left.compile(), self.right.compile())
        #     return i


# Defining the subtraction operation
class Sub(BinaryOp):
    def accept(self, visitor):
        return visitor.visit_sub(self)

    # def compile(self):
        # if isinstance(self.left, Integer) and isinstance(self.right, Integer):
        #     i = self.builder.sub(self.left.compile(), self.right.compile())
        # # elif isinstance(self.left, Float) and isinstance(self.right, Float):
        # #     i = self.builder.fsub(self.left.compile(), self.right.compile())
        #     return i


# Defining the multiplication operation
class Mult(BinaryOp):
    def accept(self, visitor):
        return visitor.visit_mult(self)
    
    # def compile(self):
        # if isinstance(self.left, Integer) and isinstance(self.right, Integer):
        #     i = self.builder.mul(self.left.compile(), self.right.compile())
        # # elif isinstance(self.left, Float) and isinstance(self.right, Float):
        # #     i = self.builder.fmul(self.left.compile(), self.right.compile())
        #     return i

# Defining the division operation
class Div(BinaryOp):
    def accept(self, visitor):
        return visitor.visit_div(self)
    
    # def compile(self):
        # # if self.right is Integer(str(0)) or self.right is Float(str(0.0)):
        # #     raise ZeroDivisionError("You cannot divide by zero!")
        # # else:
        #     i = self.builder.sdiv(self.left.compile(), self.right.compile())
        #     return i

# Defining the modulo operation
class Modulus(BinaryOp):
    def accept(self, visitor):
        return visitor.visit_mod(self)

    # def compile(self):
# #         if self.right == Integer(str(0)) or self.right == Float(str(0.0)):
# #             raise ZeroDivisionError("You cannot take the remainder of a division by zero!")
# #         else:
#             i = self.builder.srem(self.left.compile(), self.right.compile())
#             return i

# For handling Boolean types
class Boolean:
    def __init__(self, value):
        self.value = bool(value)

    def accept(self, visitor):
        pass

    # def compile(self):
    #     return self

# Equality
class Equal(BinaryOp):
    def accept(self, visitor):
        return visitor.visit_equal(self)

    # def compile(self):
    #     if self.left == self.right:
    #         return True
    #     else:
    #         return False

# Less than
class Less(BinaryOp):
    def accept(self, visitor):
        return visitor.visit_lt(self)

    # def compile(self):
    #     if self.left < self.right:
    #         return True
    #     else:
    #         return False

# Less than or equal to
class LessEqual(BinaryOp):
    def accept(self, visitor):
        return visitor.visit_lte(self)

    # def compile(self):
    #     if self.left <= self.right:
    #         return True
    #     else:
    #         return False

# Greater than
class Greater(BinaryOp):
    def accept(self, visitor):
        return visitor.visit_gt(self)

    # def compile(self):
    #     if self.left > self.right:
    #         return True
    #     else:
    #         return False

# Greater than or equal to
class GreaterEqual(BinaryOp):
    def accept(self, visitor):
        return visitor.visit_gte(self)

    # def compile(self):
    #     if self.left >= self.right:
    #         return True
    #     else:
    #         return False

# Strings
class String:
    def __init__(self, value):
        self.value = value

    def compile(self, module, builder):
        return self.value

class Char:
    def __init__(self, value):
        self.value = value

    def compile(self):
        return self.value

class Variable:
    def __init__(self, var_type, identifier, value):
        self.identifier = identifier
        self.value = value
        self.var_type = var_type

    def accept(self, visitor):
        return visitor.visit_var(self)


# Defining the print function
class Print:    
    def __init__(self, builder, module, printf, value):
        self.printf = printf
        self.builder = builder
        self.module = module
        self.value = value
        # self.initialised = False

    def accept(self, visitor):
        return visitor.visit_print(self)
    
    # Evaluating the print function in LLVM
    # def compile(self):
    #     value = self.value.compile()
        # printf = llvm_printf()
        # llvm_printf()
        # self.builder.call(self.printf, [fmt_arg, value])