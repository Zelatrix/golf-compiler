from rply import ParserGenerator
from ast import Integer, Float, Char, String, Boolean
from ast import Sum, Sub, Mult, Div, Modulus
from ast import Equal, Less, LessEqual, Greater, GreaterEqual
from ast import Print, Sequence

import re

class Parser():
    def __init__(self, module, builder, printf):
        # The tokens accepted by the lexer
        types = ["INT", "FLOAT", "CHAR", "STRING", "BOOL"]
        bools = ["AND", "OR", "NOT"]
        arithmetic = ["PLUS", "MINUS", "STAR", "SLASH", "MOD", "LEFT_PAR", "RIGHT_PAR"]
        keywords = ["PRINT", "VAR", "FOR", "UNTIL", "WHILE", "IF", "THEN", "ARRAY", "FUNCTION"]
        comparison = ["LESS_EQUAL", "GREAT_EQUAL", "EQUAL", "LESS_THAN", "GREATER_THAN"]
        other = ["ASSIGN", "SEMICOLON", "IDENTIFIER", "COLON", "DBL_QUOTE", "SINGLE_QUOTE"]

        # Joining all the tokens together into a single list
        empty = []
        empty.append(types)
        empty.append(bools)
        empty.append(arithmetic)
        empty.append(keywords)
        empty.append(comparison)
        empty.append(other)
        tokenList = empty

        # Flatten the nested list of tokens
        flatTokens = [val for sublist in tokenList for val in sublist]

        #Rules of precedence for the operators
        precedence = [('left', ['PLUS', 'MINUS']), ('left', ['STAR', 'SLASH'])
                      # ('left', [])('left', [])
                      # ('left', [])('left', [])
                     ]

        self.pg = ParserGenerator(flatTokens, precedence)
        self.module = module
        self.builder = builder
        self.printf = printf

    def parse(self):
        # The main program
        @self.pg.production('program : statementList')
        def program(p):
            return p[0]

        # How to parse multiple statements
        # @self.pg.production('program : statement_list')
        # @self.pg.production('statement_list : statement (statement_list SEMICOLON| SEMICOLON)')
        @self.pg.production('statement : PRINT LEFT_PAR expr RIGHT_PAR')
        def statement(p):
            print("got print")
            return Print(self.builder, self.module, self.printf, p[2])

        @self.pg.production('statementList : statement SEMICOLON statementList')
        def stmt(p):
            return Sequence(self.builder, self.module, self.printf, p[0], p[2])
             #while True:
             #    if token == 'SEMICOLON':
             #        break
             #    else:
             #        continue

        @self.pg.production('statementList : ')
        def stmtEnd(p):
            return []

        # Numbers
        @self.pg.production('expr : INT')
        @self.pg.production('expr : FLOAT')
        def number(p):
            num = p[0]
            if num.gettokentype() == "INT":
                return Integer(self.builder, self.module, p[0].value)
            elif num.gettokentype() == "FLOAT":
                return Float(self.builder, self.module, p[0].value)

        # Strings/Chars
        @self.pg.production('expr : STRING')
        @self.pg.production('expr : CHAR')
        def string_char(p):
            value = p[0]
            if value.gettokentype() == "STRING":
            # if re.match('\".*\"'):
                return String(self.builder, self.module, value)
            elif value.gettokentype() == "CHAR":
            # if re.match('\"[A-Za-z]\"'):
                return Char(self.builder, self.module, value)

        # Arithmetic
        @self.pg.production('expr : expr PLUS expr')
        @self.pg.production('expr : expr MINUS expr')
        @self.pg.production('expr : expr STAR expr')
        @self.pg.production('expr : expr SLASH expr')
        @self.pg.production('expr : expr MOD expr')
        def expression(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == 'PLUS':
                return Sum(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'MINUS':
                return Sub(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'STAR':
                return Mult(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'SLASH':
                return Div(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'MOD':
                return Modulus(self.builder, self.module, left, right)

        # Parenthesised expression
        @self.pg.production('expr : LEFT_PAR expr RIGHT_PAR')
        def paren_expr(p):
            return p[1]

        # Comparison
        @self.pg.production('expr : expr LESS_THAN expr')
        @self.pg.production('expr : expr GREATER_THAN expr')
        @self.pg.production('expr : expr LESS_EQUAL expr')
        @self.pg.production('expr : expr GREAT_EQUAL expr')
        @self.pg.production('expr : expr EQUAL expr')
        def comparison(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == 'LESS_THAN':
                return Less(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'GREATER_THAN':
                return Greater(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'LESS_EQUAL':
                return LessEqual(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'GREAT_EQUAL':
                return GreaterEqual(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'EQUAL':
                return Equal(self.builder, self.module, left, right)

        # Double quotes
        @self.pg.production('expr : DBL_QUOTE')
        def dbl_quote(p):
            pass

        # Single quotes
        @self.pg.production('expr : SINGLE_QUOTE')
        def single_quote(p):
            pass

        # Arrays
        @self.pg.production('expr : ARRAY LEFT_PAR expr RIGHT_PAR')
        def array(p):
            pass

        # Parsing variables and variable assignment
        @self.pg.production('expr : VAR IDENTIFIER SEMICOLON')
        @self.pg.production('expr : VAR IDENTIFIER ASSIGN expr SEMICOLON')
        def var_expr(p):
            pass

        # Parsing an if statement
        @self.pg.production('expr : IF expr THEN COLON')
        def if_stmt(p):
            pass

        # Loops
        @self.pg.production('expr : WHILE expr COLON')
        @self.pg.production('expr : FOR expr UNTIL expr COLON')
        def loop(p):
            pass

        # Functions
        @self.pg.production('expr : FUNCTION LEFT_PAR expr RIGHT_PAR COLON')
        def function(p):
            pass

        # Error handling
        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
