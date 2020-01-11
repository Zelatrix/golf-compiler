from llvmlite import ir

# Integers
class Integer:
    def __init__(self, builder, module, value):
        self.value = value
        self.builder = builder
        self.module = module

    def __eq__(self, other):
        if not isinstance(other, Integer):
            return NotImplemented
        else:
            return self.value == other.value

    def eval(self):
        i = ir.Constant(ir.IntType(64), int(self.value))
        return i

# Floating point numbers
class Float:
    def __init__(self, builder, module, value):
        self.value = value
        self.builder = builder
        self.module = module

    def __eq__(self, other):
        if not isinstance(other, Float):
            return NotImplemented
        else:
            return self.value == other.value

    def eval(self):
        i = ir.Constant(ir.FloatType(), float(self.value))
        return i


# The general binary operator type
class BinaryOp:
    def __init__(self, builder, module, left, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right


# Defining the addition operation
class Sum(BinaryOp):
    def eval(self):
        if isinstance(self.left, Integer) and isinstance(self.right, Integer):
            i = self.builder.add(self.left.eval(), self.right.eval())
        # elif isinstance(self.left, Float) and isinstance(self.right, Float):
        #     i = self.builder.fadd(self.left.eval(), self.right.eval())
            return i


# Defining the subtraction operation
class Sub(BinaryOp):
    def eval(self):
        if isinstance(self.left, Integer) and isinstance(self.right, Integer):
            i = self.builder.sub(self.left.eval(), self.right.eval())
        # elif isinstance(self.left, Float) and isinstance(self.right, Float):
        #     i = self.builder.fsub(self.left.eval(), self.right.eval())
            return i


# Defining the multiplication operation
class Mult(BinaryOp):
    def eval(self):
        if isinstance(self.left, Integer) and isinstance(self.right, Integer):
            i = self.builder.mul(self.left.eval(), self.right.eval())
        # elif isinstance(self.left, Float) and isinstance(self.right, Float):
        #     i = self.builder.fmul(self.left.eval(), self.right.eval())
            return i

# Defining the division operation
class Div(BinaryOp):
    def eval(self):
        # if self.right is Integer(str(0)) or self.right is Float(str(0.0)):
        #     raise ZeroDivisionError("You cannot divide by zero!")
        # else:
            i = self.builder.sdiv(self.left.eval(), self.right.eval())
            return i

# Defining the modulo operation
class Modulus(BinaryOp):
    def eval(self):
#         if self.right == Integer(str(0)) or self.right == Float(str(0.0)): 
#             raise ZeroDivisionError("You cannot take the remainder of a division by zero!")
#         else:
            i = self.builder.srem(self.left.eval(), self.right.eval())
            return i

class Boolean:
    def __init__(self):
        pass

# Equality
class Equal(BinaryOp):
    def eval(self):
        if self.left == self.right:
            return True
        else:
            return False

# Less than
class Less(BinaryOp):
    def eval(self):
        if self.left < self.right:
            return True
        else:
            return False

# Less than or equal to
class LessEqual(BinaryOp):
    def eval(self):
        if self.left <= self.right:
            return True
        else:
            return False

# Greater than
class Greater(BinaryOp):
    def eval(self):
        if self.left > self.right:
            return True
        else:
            return False

# Greater than or equal to
class GreaterEqual(BinaryOp):
    def eval(self):
        if self.left >= self.right:
            return True
        else:
            return False

# Strings
class String:
    def __init__(self, value):
        self.value = value

    def eval(self, module, builder):
        return self.value

class Char:
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

class Variable:
    def __init__(self, ident):
        self.ident = ident
    
    def eval(self):
        pass
    
# class Loop:
#     def __init__(self):
#         pass

#     def eval(self):
#         pass

# class If:
#     def __init__(self, printf, value):
#         self.printf = printf
#         self.value = value


# class Array:
#     def __init__(self, printf, value):
#         self.printf = printf
#         self.value = value


# class Colon:
#     def __init__(self, printf, value):
#         self.printf = printf
#         self.value = value


# class Semicolon:
#     def __init__(self, printf, value):
#         self.printf = printf
#         self.value = value


# Defining the print function
class Print:
    def __init__(self, builder, module, printf, value):
        self.printf = printf
        self.builder = builder
        self.module = module
        self.value = value

    # Evaluating the print function in LLVM
    def eval(self):
        value = self.value.eval()

        voidptr_ty = ir.IntType(64).as_pointer()
        fmt = "%i \n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt.encode("utf8")))
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name="fstr")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)

        self.builder.call(self.printf, [fmt_arg, value])
