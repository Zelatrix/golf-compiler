class Visitor:
    def visit(self, visitor):
        return visitor.accept(self)


# The general number type
class Number:
    def __init__(self, builder, module, value): #, v_type):
        self.builder = builder
        self.module = module
        self.value = value
        # self.v_type = v_type


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

    # def __init__(self):
    #     self.v_type = "int"

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
        # # if right is Integer(self.builder, self.module, str(0)) or right is Float(self.builder, self.module, str(0.0)):
        #     return ZeroDivisionError("Stop trying to break mathematics!")
        # else:
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
class Boolean:
    def __init__(self, value):
        self.value = bool(value)

    def accept(self, visitor):
        return visitor.visit(self.value)


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


# Variable reassignment
class VarReassign:
    def __init__(self, builder, module, name, value):
        self.builder = builder
        self.module = module
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_reassign(self.name, self.value)


class VarUsage:
    def __init__(self, builder, module, name):
        self.builder = builder
        self.module = module
        self.name = name

    def accept(self, visitor):
        return visitor.visit_var_usage(self.name)

# class FunParam:
#     def __init__(self, builder, module, param):
#         self.builder = builder
#         self.module = module
#         self.param = param

#     def accept(self, visitor):
#         return visitor.visit_arguments(self.param)

# Strings
class String:
   def __init__(self, builder, module, value):
       self.builder = builder
       self.module = module
       self.value = value

   def accept(self, visitor):
       return visitor.visit_string(self.value)

# Characters
class Char:
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value

    def accept(self, value):
        return vsitor.visit_char(self.value)

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


class ElseBlock:
    def __init__(self, builder, module, else_body):
        self.builder = builder
        self.module = module
        self.else_body = else_body

    def accept(self, visitor):
        return visitor.visit_else(self.else_body)


# User defined functions with no arguments
class Function:
   def __init__(self, builder, module, fn_name, fn_body, ret_ty):
       self.builder = builder
       self.module = module
       self.fn_name = fn_name
       self.fn_body = fn_body
       self.ret_ty = ret_ty

   def accept(self, visitor):
       visitor.visit_fun(self.fn_name, self.fn_body, self.ret_ty) # self.fn_params

# Functions with arguments
class FuncArgs:
   def __init__(self, builder, module, fn_name, fn_args, fn_body, ret_ty):
       self.builder = builder
       self.module = module
       self.fn_name = fn_name
       self.fn_body = fn_body
       self.fn_args = fn_args
       self.ret_ty = ret_ty

   def accept(self, visitor):
       visitor.visit_fargs(self.fn_name, self.fn_args, self.fn_body, self.ret_ty)

# Calling a function
class FunctionCall:
   def __init__(self, builder, module, fn_name):
       self.builder = builder
       self.module = module
       self.fn_name = fn_name

   def accept(self, visitor):
       visitor.visit_fcall(self.fn_name)

# Calling a function with arguments
class FArgsCall:
    def __init__(self, builder, module, fn_name, fn_args):
        self.builder = builder
        self.module = module
        self.fn_name = fn_name
        self.fn_args = fn_args

    def accept(self, visitor):
        visitor.visit_call_args(self.fn_name, self.fn_args)

# Arrays
class Array:
    def __init__(self, builder, module, index):
        self.builder = builder
        self.module = module
        self.index = index

    def accept(self, visitor):
        visitor.visit_array(self.index)

# Class for array assignment
class ArrayAssign:
    def __init__(self, builder, module, index, value):
        self.builder = builder
        self.module = module
        self.index = index
        self.value = value
    
    def accept(self, visitor):
        visitor.visit_array_assign(self.index, self.value)

# Accessing the value in an array
class ArrayAccess:
    def __init__(self, builder, module, index):
        self.builder = builder 
        self.module = module
        self.index = index

    def accept(self, visitor):
        visitor.visit(self.index)

# While loops
class While:
    def __init__(self, builder, module, predicate, body):
        self.builder = builder
        self.module = module
        # self.var_list = var_list  # Add back the parameter to test
        self.predicate = predicate
        self.body = body

    def accept(self, visitor):
        visitor.visit_while(self.predicate, self.body)


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
class Decrement:
    def __init__(self, builder, module, var, value):
        self.builder = builder
        self.module = module
        self.var = var
        self.value = value

    def accept(self, visitor):
        visitor.visit_decrement(self.var, self.value)


class TimesEq:
    def __init__(self, builder, module, var, value):
        self.builder = builder
        self.module = module
        self.var = var
        self.value = value

    def accept(self, visitor):
        visitor.visit_timeseq(self.var, self.value)


class DivEq:
    def __init__(self, builder, module, var, value):
        self.builder = builder
        self.module = module
        self.var = var
        self.value = value

    def accept(self, visitor):
        visitor.visit_diveq(self.var, self.value)


class Return:
    def __init__(self, builder, module, ret_val):
        self.builder = builder
        self.module = module
        self.ret_val = ret_val

    def accept(self, visitor):
        visitor.visit_return(self.ret_val)


class Is:
    def __init__(self, builder, module, expr):
        self.builder = builder
        self.module = module
        self.expr = expr

    def accept(self, visitor):
        # pass
        visitor.visit_is(self.expr)

# Defining the print function
class Print:
    def __init__(self, builder, module, printf, value): # gbl_fmt, value):
        self.printf = printf
        self.builder = builder
        self.module = module
        # self.gbl_fmt = gbl_fmt
        self.value = value

    def accept(self, visitor):
        value = self.value.accept(visitor)
        return visitor.visit_print(value) #, gbl_fmt)

class Arg:
    def __init__(self, builder, module, a_type, a_name):
        self.builder = builder
        self.module = module
        self.a_type = a_type
        self.a_name = a_name

    def accept(self, visitor):
        return visitor.visit_arg(a_type, a_name)

# class PrintStr:
#      def __init__(self, builder, module, printf_str, value):
#          self.printf_str = printf_str
#          self.builder = builder
#          self.module = module
#          self.value = value

#      def accept(self, visitor):
#          value = self.value.accept(visitor)
#          return visitor.visit_print_str(value)
