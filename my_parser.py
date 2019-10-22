from rply import ParserGenerator
from ast import Number, Sum, Sub, Mult, Div, Print

class Parser():
  def __init__(self):
    self.pg = ParserGenerator(["BANG","LEFT_PAR","RIGHT_PAR","NUM","PLUS", "MINUS", "STAR", "SLASH"])
    self.module = module
    self.builder = builder
    self.printf = printf

  def parse(self):
    @self.pg.production('program : BANG LEFT_PAR expr RIGHT_PAR')
    def program(p):
      return Print(self.builder, self.module, self.printf, p[2])

    @self.pg.production('expr : expr PLUS expr')
    @self.pg.production('expr : expr MINUS expr')
    @self.pg.production('expr : expr STAR expr')
    @self.pg.production('expr : expr SLASH expr')
    def expression(p):
      left = p[0]
      right = p[2]
      operator = p[1]
      if operator.gettokentype() == "PLUS":
        return Sum(left, right)
      elif operator.gettokentype() == 'MINUS':
        return Sub(left, right)
      elif operator.gettokentype() == 'STAR':
        return Mult(left, right)
      elif operator.gettokentype() == 'SLASH':
        return Div(left, right)

    @self.pg.production('expr : NUM')
    def number(p):
      return Number(p[0].value)
    
    @self.pg.error
    def error_handle(token):
      raise ValueError(token)
    
  def get_parser(self):
    return self.pg.build()