class Visitor:
    def visit(self, visitor):
        return visitor.accept(self)


# The general number type
class Number:
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value


# The general binary operator type
class BinaryOp:
    def __init__(self, builder, module, left, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right


class UnaryOp:
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value


# Integers
class Integer(Number):
    def __eq__(self, other):
        if not isinstance(other, Integer):
            return NotImplemented
        else:
            return self.value == other.value

    def accept(self, visitor):
        return visitor.visit_int(self.value)


# Floating point numbers
class Float(Number):
    def __eq__(self, other):
        if not isinstance(other, Float):
            return NotImplemented
        else:
            return self.value == other.value

    def accept(self, visitor):
        return visitor.visit_float(self.value)


# Defining the addition operation
class Sum(BinaryOp):
    def accept(self, visitor):
        left = self.left.accept(visitor)
        right = self.right.accept(visitor)
        return visitor.visit_sum(left, right)


# Defining the subtraction operation
class Sub(BinaryOp):
    def accept(self, visitor):
        left = self.left.accept(visitor)
        right = self.right.accept(visitor)
        return visitor.visit_sub(left, right)


# Defining the multiplication operation
class Mult(BinaryOp):
    def accept(self, visitor):
        left = self.left.accept(visitor)
        right = self.right.accept(visitor)
        return visitor.visit_mult(left, right)


# Defining the division operation
class Div(BinaryOp):
    def accept(self, visitor):
        left = self.left.accept(visitor)
        right = self.right.accept(visitor)
        if right is Integer(self.builder, self.module, str(0)) or right is Float(self.builder, self.module, str(0.0)):
            return ZeroDivisionError("Stop trying to break mathematics!")
        else:
            return visitor.visit_div(left, right)


# Defining the modulo operation
class Modulus(BinaryOp):
    def accept(self, visitor):
        left = self.left.accept(visitor)
        right = self.right.accept(visitor)
        return visitor.visit_mod(left, right)


# Unary negation
class UNeg(UnaryOp):
    def accept(self, visitor):
        value = self.value.accept(visitor)
        return visitor.visit_uneg(value)

# For handling Boolean types
# class Boolean:
#     def __init__(self, value):
#         self.value = bool(value)
#
#     def accept(self, visitor):
#         return self


# Equality
class Equal(BinaryOp):
    def accept(self, visitor):
        left = self.left.accept(visitor)
        right = self.right.accept(visitor)
        return visitor.visit_eq(left, right)


class NotEqual(BinaryOp):
    def accept(self, visitor):
        left = self.left.accept(visitor)
        right = self.right.accept(visitor)
        return visitor.visit_neq(left, right)


# Less than
class Less(BinaryOp):
    def accept(self, visitor):
        left = self.left.accept(visitor)
        right = self.right.accept(visitor)
        return visitor.visit_lt(left, right)


# Less than or equal to
class LessEqual(BinaryOp):
    def accept(self, visitor):
        left = self.left.accept(visitor)
        right = self.right.accept(visitor)
        return visitor.visit_lte(left, right)


# Greater than
class Greater(BinaryOp):
    def accept(self, visitor):
        left = self.left.accept(visitor)
        right = self.right.accept(visitor)
        return visitor.visit_gt(left, right)


# Greater than or equal to
class GreaterEqual(BinaryOp):
    def accept(self, visitor):
        left = self.left.accept(visitor)
        right = self.right.accept(visitor)
        return visitor.visit_gte(left, right)


# Boolean AND
class And(BinaryOp):
    def accept(self, visitor):
        left = self.left.accept(visitor)
        right = self.right.accept(visitor)
        return visitor.visit_and(left, right)


# Boolean OR
class Or(BinaryOp):
    def accept(self, visitor):
        left = self.left.accept(visitor)
        right = self.right.accept(visitor)
        return visitor.visit_or(left, right)


# Boolean NOT
class Not(UnaryOp):
    def accept(self, visitor):
        value = self.value.accept(visitor)
        return visitor.visit_not(value)


# Variables
class VarDeclaration:
    # def __init__(self, builder, module, name, value):
    def __init__(self, builder, module, name, value):
        self.builder = builder
        self.module = module
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_var_dec(self.name, self.value)


class VarUsage:
    def __init__(self, builder, module, name):
        self.builder = builder
        self.module = module
        self.name = name

    def accept(self, visitor):
        # ident = self.ident.accept(visitor)
        return visitor.visit_var_usage(self.name)


# Strings
class String:
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value
        self.length = len(value)

    def accept(self, visitor):
        return visitor.visit_string(self.value, self.length)


# Characters
# class Char:
#     def __init__(self, builder, module, value):
#         self.builder = builder
#         self.module = module
#         self.value = value
#
#     def accept(self, visitor):
#         return visitor.visit_char(self.value)


# If-then statements
class IfThen:
    def __init__(self, builder, module, predicate, body):
        self.builder = builder
        self.module = module
        self.predicate = predicate
        self.body = body

    def accept(self, visitor):
        return visitor.visit_if(self.predicate, self.body)


class IfElse:
    def __init__(self, builder, module, predicate, if_body, else_body):
        self.builder = builder
        self.module = module
        self.predicate = predicate
        self.if_body = if_body
        self.else_body = else_body

    def accept(self, visitor):
        return visitor.visit_if_else(self.predicate, self.if_body, self.else_body)

# User defined functions
# class UserDefinedFunction:
#     def __init__(self, builder, module):
#         self.builder = builder
#         self.module = module
#
#     def accept(self, visitor):
#         visitor.visit_udf()


# While loops
# class While:
#     def __init__(self, builder, module, predicate):
#         self.predicate = predicate
#
#     def accept(self, visitor):
#         visitor.visit_while(self.predicate)

# Increment a variable
class Increment:
    def __init__(self, builder, module, variable, value):
        self.builder = builder
        self.module = module
        self.variable = variable
        self.value = value

    def accept(self, visitor):
        visitor.visit_increment(self.variable, self.value)


# Decrement a variable
# class Decrement:
#     def __init__(self, var, value):
#         self.var = var
#         self.value = value
#
#     def accept(self, visitor):
#         visitor.visit_decrement(self.var, self.value)


# Defining the print function
class Print:
    def __init__(self, builder, module, printf, value):
        self.printf = printf
        self.builder = builder
        self.module = module
        self.value = value

    def accept(self, visitor):
        value = self.value.accept(visitor)
        return visitor.visit_print(value)
