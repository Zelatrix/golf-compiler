from rply import LexerGenerator


class Lexer:
    # Initialise the lexer object
      def __init__(self):
            self.lexer = LexerGenerator()

    # Add the list of tokens to the lexer
      def add_tokens(self):
            # Keywords
            self.lexer.add("FOR", r"for")
            self.lexer.add("WHILE", r"while")
            self.lexer.add("IF", r"if")
            self.lexer.add("DICT", r"dict")
            self.lexer.add("ARRAY", r"array")
            self.lexer.add("BANG", r"\!")
            self.lexer.add("VAR", r"var")

            # Arithmetic
            self.lexer.add("NUM", r"\d+")
            self.lexer.add("PLUS", r"\+")
            self.lexer.add("MINUS", r"\-")
            self.lexer.add("STAR", r"\*")
            self.lexer.add("SLASH", r"\/")
            self.lexer.add("MOD", r"mod")

            # Two-part tokens
            self.lexer.ignore("\/\/.+")
            # self.lexer.ignore("/*([A-Z]|[a-z]|[0-9])+*/")

            # Miscellaneous
            #self.lexer.add("BANG", r"\!")
            self.lexer.add("DBL_QUOTE", r"\"")
            self.lexer.add("SINGLE_QUOTE", r"\'")
            self.lexer.add("LEFT_PAR", r"\(")
            self.lexer.add("RIGHT_PAR", r"\)")
            self.lexer.add("SEMICOLON", r"\;")
            self.lexer.add("COLON", r"\:")
            self.lexer.ignore("\s+")

    # Add the tokens to the lexer
    # Build the lexer
      def get_lexer(self):
          self.add_tokens()
          return self.lexer.build()
