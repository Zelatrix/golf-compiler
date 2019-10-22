from rply import LexerGenerator

class Lexer():
  def __init__(self):
    self.lexer = LexerGenerator()
  
  def add_tokens(self):
    #Exclamation
    self.lexer.add("BANG", r"\!")
    #Left parenthesis
    self.lexer.add("LEFT_PAR", r"\(")
    #Right parenthesis
    self.lexer.add("RIGHT_PAR", r"\)")
    #Digit
    self.lexer.add("NUM", r"\d+")
    #Addition
    self.lexer.add("PLUS", r"\+")
    #Subtraction
    self.lexer.add("MINUS", r"\-")
    #Multiplication
    self.lexer.add("STAR", r"\*")
    #Division
    self.lexer.add("SLASH", r"\/")
    #Ignore spaces
    self.lexer.ignore("\s+")

  def get_lexer(self):
    self.add_tokens()
    return self.lexer.build()