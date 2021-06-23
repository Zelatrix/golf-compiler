from rply import ParserGenerator

from my_ast import Integer, Float  # , String, Char, Boolean
from my_ast import Sum, Sub, Mult, Div, Modulus
from my_ast import Equal, NotEqual, Less, LessEqual, Greater, GreaterEqual
from my_ast import Print, VarDeclaration, VarUsage, And, Or, Not
from my_ast import IfThen, IfElse
from my_ast import UNeg
# from my_ast import While UserDefinedFunction


class Parser:
    def __init__(self, module, builder, printf):
        # The tokens accepted by the lexer
        types = ["INT", "FLOAT"]  # , "STRING", "CHAR"]
        booleans = ["AND", "OR", "NOT", "TRUE", "FALSE"]
        arithmetic = ["PLUS", "MINUS", "STAR", "SLASH", "MOD"]
        brackets = ["LEFT_PAR", "RIGHT_PAR", "LEFT_CURLY", "RIGHT_CURLY"]
        comparison = ["NOT_EQUAL", "LESS_EQUAL", "GREAT_EQUAL", "EQUAL", "LESS_THAN", "GREATER_THAN"]
        keywords = ["PRINT", "VAR", "IF", "THEN", "ELSE"]
        other = ["SEMICOLON", "ASSIGN", "ID"]  # , "INC", "DEC"]
        # unused = ["FUNCTION", "DBL_QUOTE", "SINGLE_QUOTE", "BOOL", "LEFT_BRACE", "RIGHT_BRACE", "WHILE", "ARRAY"]

        # Joining all the tokens together into a single list
        empty = [types, booleans, arithmetic, comparison, brackets, keywords, other]
        token_list = empty

        # Flatten the nested list of tokens
        flat_tokens = [val for sublist in token_list for val in sublist]

        # Rules of precedence for the operators
        precedence = [('left', ['PLUS', 'MINUS']), ('left', ['STAR', 'SLASH'])]

        self.pg = ParserGenerator(flat_tokens, precedence)
        self.module = module
        self.builder = builder
        self.printf = printf

    def parse(self):
        # The main program
        @self.pg.production('program : statement_list')
        def program(p):
            return p[0]

        @self.pg.production('statement_list : statement SEMICOLON statement_list')
        def stmt_list(p):
            return [p[0]] + p[2]

        @self.pg.production('statement_list : ')
        def empty_stmt(p):
            return []

        @self.pg.production('statement : PRINT LEFT_PAR expr RIGHT_PAR')
        def print_statement(p):
            return Print(self.builder, self.module, self.printf, p[2])

        # Parsing variables and variable assignment
        @self.pg.production('statement : VAR ID ASSIGN expr')
        def var_decl(p):
            return VarDeclaration(self.builder, self.module, p[1].getstr(), p[3])

        @self.pg.production('expr : ID')
        def var_use(p):
            return VarUsage(self.builder, self.module, p[0].getstr())

        # Numbers
        @self.pg.production('expr : INT')
        @self.pg.production('expr : FLOAT')
        def number(p):
            if p[0].gettokentype() == "INT":
                return Integer(self.builder, self.module, p[0].value)
            elif p[0].gettokentype() == "FLOAT":
                return Float(self.builder, self.module, p[0].value)

        # Strings/Chars
        # @self.pg.production('expr : STRING')
        # @self.pg.production('expr : CHAR')
        # def string_char_expr(p):
        #     if len(p[0]) == 1:
        #         return Char(self.builder, self.module, p[0].value)
        #     else:
        #         return String(self.builder, self.module, p[0].value)

        # If-then statements
        @self.pg.production('statement : IF expr THEN LEFT_CURLY statement_list RIGHT_CURLY')
        def if_then(p):
            return IfThen(self.builder, self.module, p[1], p[4])

        # If-then-else statements
        @self.pg.production('statement : IF expr THEN LEFT_CURLY statement_list RIGHT_CURLY '
                            'ELSE LEFT_CURLY statement_list RIGHT_CURLY')
        def if_else(p):
            return IfElse(self.builder, self.module, p[1], p[4], p[8])

        # Arithmetic
        @self.pg.production('expr : expr PLUS expr')
        @self.pg.production('expr : expr MINUS expr')
        @self.pg.production('expr : expr STAR expr')
        @self.pg.production('expr : expr SLASH expr')
        @self.pg.production('expr : expr MOD expr')
        def expression(p):
            if p[1].gettokentype() == 'PLUS':
                return Sum(self.builder, self.module, p[0], p[2])
            elif p[1].gettokentype() == 'MINUS':
                return Sub(self.builder, self.module, p[0], p[2])
            elif p[1].gettokentype() == 'STAR':
                return Mult(self.builder, self.module, p[0], p[2])
            elif p[1].gettokentype() == 'SLASH':
                return Div(self.builder, self.module, p[0], p[2])
            elif p[1].gettokentype() == 'MOD':
                return Modulus(self.builder, self.module, p[0], p[2])
        
        # Unary negation
        @self.pg.production('expr : MINUS expr')
        def uneg_single(p):
            return UNeg(self.builder, self.module, p[1])
        
        @self.pg.production('expr : MINUS LEFT_PAR expr RIGHT_PAR')
        def uneg_expr(p):
            return UNeg(self.builder, self.module, p[2])

        # Boolean And and Or
        @self.pg.production('expr : expr AND expr')
        @self.pg.production('expr : expr OR expr')
        def binary_bool_op(p):
            if p[1].gettokentype() == 'AND':
                return And(self.builder, self.module, p[0], p[2])
            elif p[1].gettokentype() == 'OR':
                return Or(self.builder, self.module, p[0], p[2])

        # Boolean NOT
        @self.pg.production('expr : NOT expr')
        def unary_bool_op(p):
            return Not(self.builder, self.module, p[1])

        # Parsing True and False
        @self.pg.production('expr : TRUE')
        @self.pg.production('expr : FALSE')
        def bool_expr(p):
            if p[0].gettokentype() == "TRUE":
                return Integer(self.builder, self.module, 1)
            else:
                return Integer(self.builder, self.module, 0)

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
        @self.pg.production('expr : expr NOT_EQUAL expr')
        def comparison(p):
            if p[1].gettokentype() == 'LESS_THAN':
                return Less(self.builder, self.module, p[0], p[2])
            elif p[1].gettokentype() == 'GREATER_THAN':
                return Greater(self.builder, self.module, p[0], p[2])
            elif p[1].gettokentype() == 'LESS_EQUAL':
                return LessEqual(self.builder, self.module, p[0], p[2])
            elif p[1].gettokentype() == 'GREAT_EQUAL':
                return GreaterEqual(self.builder, self.module, p[0], p[2])
            elif p[1].gettokentype() == 'EQUAL':
                return Equal(self.builder, self.module, p[0], p[2])
            elif p[1].gettokentype() == 'NOT_EQUAL':
                return NotEqual(self.builder, self.module, p[0], p[2])

        # While loops
        # @self.pg.production('expr : WHILE LEFT_PAR expr RIGHT_PAR LEFT_CURLY expr RIGHT_CURLY')
        # def while_loop(p):
        #     return While(self.builder, self.module, p[2])

        # Arrays
        # @self.pg.production('expr : ARRAY LEFT_BRACE expr RIGHT_BRACE')
        # def array(p):
        #     pass

        # Increment a variable by a number
        # @self.pg.production('expr : ID INC INT')
        # @self.pg.production('expr : ID INC FLOAT')
        # def increment(variable, value):
        #     return Increment(self.builder, self.module)

        # Decrement a variable by a number
        # @self.pg.production('expr : ID DEC INT')
        # @self.pg.production('expr : ID DEC FLOAT')
        # def decrement(variable, value):
        #     return Decrement(self.builder, self.module)

        # Error handling
        @self.pg.error
        def error_handle(token):
            raise ValueError(token)
        
        # User defined functions
        # @self.pg.production('expr : FUNCTION expr LEFT_PAR expr RIGHT_PAR LEFT_CURLY expr RIGHT_CURLY')
        # def udf(p):
        #     return UserDefinedFunction(self.builder, self.module)

    def get_parser(self):
        return self.pg.build()
