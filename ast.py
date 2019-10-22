from llvmlite import ir

class Number():
  def __init__(self, value):
    self.builder = builder
    self.module = module
    self.value = value
  
  def eval(self):
    i = ir.Constant(ir.IntType(8), int(self.value))
    return i
    #return int(self.value)

class BinaryOp():
  def __init__(self, builder, module, left, right):
    self.builder = builder
    self.module = module
    self.left = left
    self.right = right
  
class Sum(BinaryOp):
  def eval(self):
    i = self.builder.add(self.left.eval(), self.right.eval())
    return i
    #return self.left.eval() + self.right.eval()

class Sub(BinaryOp):
  def eval(self):
    i = self.builder.sub(self.left.eval(), self.right.eval())
    return i
    #return self.left.eval() - self.right.eval()

# class Mult(BinaryOp):
#   def eval(self):
#     return self.left.eval() * self.right.eval()

# class Div(BinaryOp):
#   def eval(self):
#     return self.left.eval() / self.right.eval()

class Print():
  def __init__(self, value):
    self.builder = builder
    self.module = module
    self.printf = printf
    self.value = value
  
  def eval(self):
    value = self.value.eval()
    voidptr_ty = ir.IntType(8).as_pointer()
    fmt = "%i \n\0"
    c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt.encode("utf8")))
    global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name="fstr")
    global_fmt.linkage = 'internal'
    #print(self.value.eval())