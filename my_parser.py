from rply import ParserGenerator

# Types
from my_ast import Integer, Float, Char # , String, Char
# Arithmetic 
from my_ast import Sum, Sub, Mult, Div, Modulus
from my_ast import UNeg
from my_ast import Increment, Decrement, TimesEq, DivEq
# Comparison
from my_ast import Equal, NotEqual, Less, LessEqual, Greater, GreaterEqual
# Booleans
from my_ast import And, Or, Not
# Conditionals
from my_ast import IfThen, IfElse, ElseBlock, While
# Arrays
from my_ast import Array, ArrayAssign, ArrayAccess
# Variables
from my_ast import VarDeclaration, VarUsage, VarReassign
# Functions
from my_ast import Function, FunctionCall, FuncArgs, FArgsCall  # , FunParam
# Misc
from my_ast import Print, Return, Arg #, PrintStr

# from my_ast import Specification, ConjSpec, SingleSpec, Is

# Custom parsing errors
from error import ParserError

class Parser:
    def __init__(self, module, builder, printf): #, printstr):
        # The tokens accepted by the lexer
        type_decs = ["TY_INT", "TY_FLOAT", "TY_CHAR", "TY_BOOL", "TY_STRING", "TY_VOID", "RET_TY"]
        types = ["INT", "FLOAT", "STRING", "BOOL", "CHAR"]
        booleans = ["AND", "OR", "NOT", "TRUE", "FALSE"]
        arithmetic = ["PLUS", "MINUS", "STAR", "SLASH", "MOD", "INC", "DEC", "TIMESEQ", "DIVEQ"]
        brackets = ["LEFT_BRACE", "RIGHT_BRACE", "LEFT_PAR", "RIGHT_PAR", "LEFT_CURLY", "RIGHT_CURLY"]
        comparison = ["NOT_EQUAL", "LESS_EQUAL", "GREAT_EQUAL", "EQUAL", "LESS_THAN", "GREATER_THAN"]
        keywords = ["PRINT", "VAR", "IF", "THEN", "ELSE", "WHILE", "FUNCTION", "RETURN"]
        other = ["SEMICOLON", "COMMA", "ASSIGN", "ID"]
        arrays = ["ARRAY"]
        # verification = ["IS"]
        # unused = ["PRINTSTR", "DBL_QUOTE", "SINGLE_QUOTE"]

        # Joining all the tokens together into a single list
        empty = [type_decs, types, booleans, arithmetic, comparison, brackets, keywords, arrays, other] # verification]
        token_list = empty

        # Flatten the nested list of tokens
        flat_tokens = [val for sublist in token_list for val in sublist]

        # Rules of precedence for the operators

        # Precedence for some of the operators was causing a large number
        # of shift/reduce conflicts in the grammar, wherein the computer
        # was not able to figure out whether to advance the pointer to the
        # next token or reduce the input using the rules of the grammar

        # Adding these precedences to the operators has eliminated the shift
        # reduce conflicts
        
        # List of operators in ascending precedence (lowest to highest)
        # Highest precedence operators get evaluated first
        precedence = [
	     ('left',  ['OR']),
             ('left',  ['AND']),
             ('left',  ['EQUAL', 'NOT_EQUAL']),	    
	     ('left',  ['LESS_THAN', 'GREATER_THAN', 'LESS_EQUAL', 'GREAT_EQUAL']),
             ('left',  ['PLUS', 'MINUS']),
             ('left',  ['STAR', 'SLASH', 'MOD']),	    
	     ('right', ['NOT']),
             ('left',  ['LEFT_PAR', 'RIGHT_PAR'])
             ]
        
        self.pg = ParserGenerator(flat_tokens, precedence)
        self.module = module
        self.builder = builder
        self.printf = printf
        # self.printstr = printstr

    def parse(self):
        # The main program
        @self.pg.production('program : statement_list')
        def program(p):
            return p[0]

        @self.pg.production('statement_list : statement SEMICOLON statement_list')
        # @self.pg.production('statement_list : single_spec statement SEMICOLON statement_list')
        def stmt_list(p):
            # if p[1].value == ";":
            return [p[0]] + p[2]
            # else:
            #     return [(p[0], p[1])] + [p[3]]

        # The empty rule
        @self.pg.production('statement_list : ')
        def empty_stmt(p):
            return []
        
        # The print() statement
        @self.pg.production('statement : PRINT LEFT_PAR expr RIGHT_PAR')
        def print_statement(p):
            return Print(self.builder, self.module, self.printf, p[2])
        
        # @self.pg.production('statement : PRINTSTR LEFT_PAR expr RIGHT_PAR')
        # def print_string(p):
        #     return PrintStr(self.builder, self.module, self.printstr, p[2])

        # Types
        @self.pg.production('type : TY_INT')
        @self.pg.production('type : TY_BOOL')
        @self.pg.production('type : TY_STRING')
        @self.pg.production('type : TY_CHAR')
        @self.pg.production('type : TY_FLOAT')
        @self.pg.production('type : TY_VOID')
        def typedef(p):
            return p[0].getstr()

        """
        #@self.pg.production('args : arg_list')
        #def args(p):
        #    return p[0]
        
        # p[0] is the type of the argument
        # p[1] is the argument itself
        # @self.pg.production('arg : type expr')
        # def typed_arg(p):
            # return Arg(self.builder, self.module, p[0], p[1])
        #    return [p[0], p[1]]

        # @self.pg.production('expr : arg')
        # def show_arg(p):
        #     return p[0]

        # Argument list for functions:

        # function f(int x) {
        #   print(x);
        # }

        #@self.pg.production('arg_list : arg COMMA arg_list')
        #def arg_list(p):
        #    # if p[1].value == ",":
        #    return [p[0]] + p[2]
        #    # else:
        #        # return [p[0]] # , p[1])] + [p[3]]
        #    # return p[0] + [p[2]]
        """
        
        # @self.pg.production('arg_list : type ID COMMA arg_list')
        # @self.pg.production('arg_list : type ID')
        # def arg_list(p):
        #     arg = [p[0], p[1]]
        #     if len(p) == 2: 
        #         return [arg]
        #     else: 
        #         return [arg] + p[3]

        @self.pg.production('argument : type ID')
        def fun_argument(p):
            return Arg(self.builder, self.module, p[0], p[1])

        @self.pg.production('arg_list : argument COMMA arg_list')
        # @self.pg.production('arg_list : type ID')
        @self.pg.production('arg_list : argument')
        def arg_list(p):
            try:
                # if p[1] == "COMMA":
                    return [p[0]] + p[2]
            except IndexError:
            # else:
                return [p[0]]

            # if p[1].gettokentype() == "ID":
            #     return [p[0], p[1]]
            # else:
            #     return [p[0], p[1]] + p[2]

        self.pg.production('arg_list : ')
        def empty_args(p):
           return []

        # Parsing variables and variable assignment
        @self.pg.production('statement : VAR ID ASSIGN expr')
        def var_decl(p):
            return VarDeclaration(self.builder, self.module, p[1].getstr(), p[3])

        @self.pg.production('statement : ID ASSIGN expr')
        def var_reassign(p):
            return VarReassign(self.builder, self.module, p[0].getstr(), p[2])

        # Increment a variable by a number
        @self.pg.production('statement : ID INC ID')
        @self.pg.production('statement : ID INC INT')
        @self.pg.production('statement : ID INC FLOAT')
        @self.pg.production('statement : ID ASSIGN ID PLUS INT')
        @self.pg.production('statement : ID ASSIGN ID PLUS FLOAT')
        def increment(p):
            return Increment(self.builder, self.module, p[0].getstr(), p[2].getstr())

        @self.pg.production('statement : ID DEC ID')
        @self.pg.production('statement : ID DEC INT')
        @self.pg.production('statement : ID DEC FLOAT')
        @self.pg.production('statement : ID ASSIGN ID MINUS INT')
        @self.pg.production('statement : ID ASSIGN ID MINUS FLOAT')
        def decrement(p):
            return Decrement(self.builder, self.module, p[0].getstr(), p[2].getstr())

        @self.pg.production('statement : ID TIMESEQ ID')
        @self.pg.production('statement : ID TIMESEQ INT')
        @self.pg.production('statement : ID TIMESEQ FLOAT')
        @self.pg.production('statement : ID ASSIGN ID STAR INT')
        @self.pg.production('statement : ID ASSIGN ID STAR FLOAT')
        def times_eq(p):
            # if p[2].gettokentype() == "ID":
            #     return TimesEq(self.builder, self.module, p[0].getstr(), p[2].value)
            return TimesEq(self.builder, self.module, p[0].getstr(), p[2].getstr())

        @self.pg.production('statement : ID DIVEQ ID')
        @self.pg.production('statement : ID DIVEQ INT')
        @self.pg.production('statement : ID DIVEQ FLOAT')
        @self.pg.production('statement : ID ASSIGN ID SLASH INT')
        @self.pg.production('statement : ID ASSIGN ID SLASH FLOAT')
        def div_eq(p):
            return DivEq(self.builder, self.module, p[0].getstr(), p[2].getstr())

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

        # Strings
        #@self.pg.production('expr : STRING')
        #def string_expr(p):
        #    return String(self.builder, self.module, p[0].value)

        # Bools
        # def bool_expr(p):
        #     pass

        # Chars
        @self.pg.production('expr : CHAR')
        def char_expr(p):
            return Char(self.builder, self.module, p[0].value)

        # If-then statements
        @self.pg.production('statement : IF expr THEN LEFT_CURLY statement_list RIGHT_CURLY')
        def if_then(p):
            return IfThen(self.builder, self.module, p[1], p[4])

        # If-then-else sdatements
        @self.pg.production('statement : IF expr THEN LEFT_CURLY statement_list RIGHT_CURLY '
                            'ELSE LEFT_CURLY statement_list RIGHT_CURLY')
        def if_else(p):
            return IfElse(self.builder, self.module, p[1], p[4], p[8])

        @self.pg.production('statement : ELSE LEFT_CURLY statement_list RIGHT_CURLY statement_list')
        def else_statement(p):
            return ElseBlock(self.builder, self.module, p[2])

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
        @self.pg.production('expr : MINUS LEFT_PAR expr RIGHT_PAR')
        def uneg_expr(p):
            if p[1].value == "(":
                return UNeg(self.builder, self.module, p[2])
            else:
                return UNeg(self.builder, self.module, p[1])

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
                # return String(self.builder, self.module, "true")
            else:
                return Integer(self.builder, self.module, 0)
                # return String(self.builder, self.module, "false")

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

        # Arrays
        @self.pg.production('statement : VAR ID ASSIGN ARRAY LEFT_BRACE expr RIGHT_BRACE')
        @self.pg.production('statement : ARRAY LEFT_BRACE expr RIGHT_BRACE')
        @self.pg.production('statement : ARRAY LEFT_BRACE expr RIGHT_BRACE ASSIGN expr')
        def array(p):
            # Declaring an array
            if p[0].gettokentype() == "VAR":
                return Array(self.builder, self.module, p[5])
            # Accessing a value in an array 
            elif p[0].gettokentype() == "ARRAY":
                try: # if p[4] is not None:
                    # Accessing the value stored in an array
                    return ArrayAccess(self.builder, self.module, p[2])
                except IndexError: # else:
                    # Assigning a value to an index
                    return ArrayAssign(self.builder, self.module, p[2], p[5])

        # Functions with arguments
        # @self.pg.production('statement : FUNCTION ID LEFT_PAR argument RIGHT_PAR LEFT_CURLY statement_list RIGHT_CURLY')
        @self.pg.production('statement : FUNCTION ID LEFT_PAR arg_list RIGHT_PAR RET_TY type LEFT_CURLY statement_list RIGHT_CURLY')
        def udf_args(p):
            # print("Parsed!")
            return FuncArgs(self.builder, self.module, p[1].value, p[3], p[8], p[6])

        # Functions
        @self.pg.production('statement : FUNCTION ID LEFT_PAR RIGHT_PAR RET_TY type LEFT_CURLY statement_list RIGHT_CURLY')
        def udf(p):
            return Function(self.builder, self.module, p[1].value, p[7], p[5])

        # Function call
        @self.pg.production('statement : ID LEFT_PAR RIGHT_PAR')
        def call_fn(p):
            return FunctionCall(self.builder, self.module, p[0].value)
        
        # Parsing the arguments to a function call, such as `f(1, 2, 3)`
        @self.pg.production('call_list : expr COMMA call_list')
        @self.pg.production('call_list : expr')
        def call_list(p):
            try:
                return [p[0]] + p[2]
            except IndexError:
                return [p[0]]

        # Calling a function with arguments
        @self.pg.production('statement : ID LEFT_PAR call_list RIGHT_PAR')
        # @self.pg.production('statement : ID LEFT_PAR expr RIGHT_PAR')
        def call_args(p):
            return FArgsCall(self.builder, self.module, p[0].value, p[2])

        # While loops
        @self.pg.production('statement : WHILE LEFT_PAR expr RIGHT_PAR LEFT_CURLY statement_list RIGHT_CURLY')
        def while_loop(p):
            return While(self.builder, self.module, p[2], p[5])

        # Returns p[1] from the function
        @self.pg.production('statement : RETURN expr')
        def return_kw(p):
            return Return(self.builder, self.module, p[1])

        # Error handling
        @self.pg.error
        def error_handle(token):
            lineno = token.getsourcepos().lineno
            colno = token.getsourcepos().colno
            raise ParserError(f"Invalid token '{token.getstr()}' at line {lineno}, column {colno}")

    def get_parser(self):
        return self.pg.build()
