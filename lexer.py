from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def add_tokens(self):
        # Keywords
        self.lexer.add("FUNCTION", r"function")
        self.lexer.add("FOR", r"for")
        self.lexer.add("UNTIL", r"until")
        self.lexer.add("WHILE", r"while")
        self.lexer.add("IF", r"if")
        self.lexer.add("THEN", r"then")
        self.lexer.add("ARRAY", r"array")
        self.lexer.add("PRINT", r"print")
        self.lexer.add("VAR", r"var")

        # Boolean operators
        self.lexer.add("AND", r"(and)")
        self.lexer.add("OR", r"(or)")
        self.lexer.add("NOT", r"(not)")

        # Types
        self.lexer.add("INT", r"(?<!\.)\d+(?!\.)")
        self.lexer.add("FLOAT", r"\d+\.\d+")
        self.lexer.add("BOOL", r"(true|false)")
        self.lexer.add("STRING", r"\".+\"")
        self.lexer.add("CHAR", r"[A-Za-z]")

        # Identifiers
        self.lexer.add("IDENTIFIER", r"[A-Za-z_]([A-Za-z_0-9])*")

        # Comparison
        self.lexer.add("LESS_EQUAL", r"\<\=")
        self.lexer.add("GREAT_EQUAL", r"\>\=")
        self.lexer.add("EQUAL", r"\=\=")
        self.lexer.add("LESS_THAN", r"\<")
        self.lexer.add("GREATER_THAN", r"\>")

        # Arithmetic
        self.lexer.add("PLUS", r"\+")
        self.lexer.add("MINUS", r"\-")
        self.lexer.add("STAR", r"\*")
        self.lexer.add("SLASH", r"\/")
        self.lexer.add("MOD", r"mod")

        # Tokens to ignore
        self.lexer.ignore("//.+")
        self.lexer.ignore("\s+")

        # Miscellaneous
        self.lexer.add("ASSIGN", r"\:\=")
        self.lexer.add("DBL_QUOTE", r"\"")
        self.lexer.add("SINGLE_QUOTE", r"\'")
        self.lexer.add("LEFT_PAR", r"\(")
        self.lexer.add("RIGHT_PAR", r"\)")
        self.lexer.add("SEMICOLON", r"\;")
        self.lexer.add("COLON", r"\:")

    # Add the tokens to the lexer
    # Build the lexer
    def get_lexer(self):
        self.add_tokens()
        return self.lexer.build()
