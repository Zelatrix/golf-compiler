from llvmlite import ir


# The general numerical type
class Number:
      def __init__(self, value):
        self.value = value

      def __eq__(self, other):
        if not isinstance(other, Number):
            return NotImplemented
        else:
            return self.value == other.value

      # def __hash__(self):
      #     pass

      def eval(self, module, builder):
        i = ir.Constant(ir.IntType(8), int(self.value))
        return i


# The general binary operator type
class BinaryOp:
    def __init__(self, left, right):
        self.left = left
        self.right = right


# Defining the addition operation
class Sum(BinaryOp):
    def eval(self, module, builder):
        i = builder.add(self.left.eval(module, builder), self.right.eval(module, builder))
        return i


# Defining the subtraction operation
class Sub(BinaryOp):
    def eval(self, module, builder):
        i = builder.sub(self.left.eval(module, builder), self.right.eval(module, builder))
        return i


# Defining the multiplication operation
class Mult(BinaryOp):
    def eval(self, module, builder):
        i = builder.mul(self.left.eval(module, builder), self.right.eval(module, builder))
        return i


# Defining the division operation
class Div(BinaryOp):
    def eval(self, module, builder):
        if self.right == Number(str(0)):
            raise ZeroDivisionError("You cannot divide by zero!")
        else:
            # print(f"The type of 0 is: {type(0)}")
            # print(f"The type of 0 is: {type(Number(0))}")
            # print(f"The type of self.right is: {type(self.right)}")
            i = builder.sdiv(self.left.eval(module, builder), self.right.eval(module, builder))
            return i


# Defining the modulo operation
class Modulus(BinaryOp):
    def eval(self, module, builder):
        if self.right == Number(str(0)):
            raise ZeroDivisionError("You cannot take the remainder of a division by zero!")
        else:
            i = builder.srem(self.left.eval(module, builder), self.right.eval(module, builder))
            return i


# Defining the print function
class Print:
    def __init__(self, printf, value):
        self.printf = printf
        self.value = value

# Evaluating the print function in LLVM
    def eval(self, module, builder):
        value = self.value.eval(module, builder)

        voidptr_ty = ir.IntType(8).as_pointer()
        fmt = "%i \n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt.encode("utf8")))
        global_fmt = ir.GlobalVariable(module, c_fmt.type, name="fstr")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        fmt_arg = builder.bitcast(global_fmt, voidptr_ty)

        builder.call(self.printf, [fmt_arg, value])


# class For:
#     def __init__(self, printf, value):
#         self.printf = printf
#         self.value = value


# class While:
#     def __init__(self, printf, value):
#         self.printf = printf
#         self.value = value


# class If:
#     def __init__(self, printf, value):
#         self.printf = printf
#         self.value = value


# class Dict:
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


# class Variable:
#     def __init__(self, printf, value):
#         self.printf = printf
#         self.value = value
