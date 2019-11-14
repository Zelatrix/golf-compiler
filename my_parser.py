from rply import ParserGenerator
from ast import Number, Sum, Sub, Print, Mult, Div, Modulus


class Parser:
  # Initialise the parser with the list of tokens
  def __init__(self, printf):
    tokenList = ["NUM", "PLUS", "MINUS", "STAR", "SLASH", "MOD", "LEFT_PAR", "RIGHT_PAR", "BANG"]
                # ["BANG", "DBL_QUOTE", "SINGLE_QUOTE", "FOR", "WHILE", "IF", "DICT", "ARRAY"]
                # ["OPEN_COMM","CLOSE_COMM", "SEMICOLON", "COLON", "VAR"]

    self.pg = ParserGenerator(tokenList)
    self.printf = printf
    # self.var = var
    # self.for = for
    # self.if = if
    # self.dict = dict
    # self.array = array
    # self.while = while

  # Pass the structure of the program to the parser
  def parse(self):
    @self.pg.production('program : BANG LEFT_PAR expr RIGHT_PAR')
    def program(p):
      return Print(self.printf, p[2])

    # @self.pg.production('variable : expr')
    # def variable():
    #   pass
    #
    # @self.pg.production('for : LEFT_PAR expr RIGHT_PAR')
    # def for_loop():
    #   pass
    #
    # @self.pg.production('if : LEFT_PAR expr RIGHT_PAR')
    # def if_stmt():
    #   pass
    #
    # @self.pg.production('dict : LEFT_PAR expr RIGHT_PAR')
    # def dictionary():
    #   pass
    #
    # @self.pg.production('array : LEFT_PAR expr RIGHT_PAR')
    # def array():
    #   pass
    #
    # @self.pg.production('while : LEFT_PAR expr RIGHT_PAR')
    # def while_stmt():
    #   pass

    # Create production rules for arithmetic operators
    @self.pg.production('expr : expr PLUS expr')
    @self.pg.production('expr : expr MINUS expr')
    @self.pg.production('expr : expr STAR expr')
    @self.pg.production('expr : expr SLASH expr')
    @self.pg.production('expr : expr MOD expr')
    def expression(p):
      left = p[0]
      right = p[2]
      operator = p[1]

    # Check the type of the encountered token
    # Run the necessary method depending on the type of the token
      if operator.gettokentype() == "PLUS":
        return Sum(left, right)
      elif operator.gettokentype() == 'MINUS':
        return Sub(left, right)
      elif operator.gettokentype() == 'STAR':
        return Mult(left, right)
      elif operator.gettokentype() == 'SLASH':
        # print(type(left), type(right))
        return Div(left, right)
      elif operator.gettokentype() == "MOD":
        return Modulus(left, right)

    @self.pg.production('expr : LEFT_PAR expr RIGHT_PAR ')
    def paren_expr(p):
      return p[1]

    # Create a production rule for numbers
    @self.pg.production('expr : NUM')
    def number(p):
        return Number(p[0].value)

    # Error handling
    @self.pg.error
    def error_handle(token):
        raise ValueError(token)

    # Build the finished parser
  def get_parser(self):
    return self.pg.build()
