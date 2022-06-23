# Parsing for optional specifications
@self.pg.production('spec : ID IS expr')  # Assignment
@self.pg.production('spec : ID LESS_THAN expr')  # Less-than
@self.pg.production('spec : ID LESS_EQUAL expr')  # Less-than-equal
@self.pg.production('spec : ID GREATER_THAN expr')  # Greater-than
@self.pg.production('spec : ID GREAT_EQUAL expr')  # Greater-than-equal
        
def parse_specification(p):
    pass
    return Specification(self.builder, self.module, p[2])

@self.pg.production('conj_spec : spec AND conj_spec')
def conj_spec(p):
    return ConjSpec(self.builder, self.module, p[0], p[2])

@self.pg.production('conj_spec : spec')
    def end_spec(p):
        return Specification(self.builder, self.module, p[0])

@self.pg.production('single_spec : LEFT_CURLY conj_spec RIGHT_CURLY')
    def single_spec(p):
        return SingleSpec(self.builder, self.module, p[1])

@self.pg.production('statement_list : single_spec')
    def end_single(p):
        return [p[0]]

@self.pg.production('statement : PRINT_STR LEFT_PAR STRING RIGHT_PAR')
    def print_str(p):
        return PrintStr(self.builder, self.module, self.print_str, p[2])

# User defined functions
@self.pg.production('statement : FUNCTION expr LEFT_PAR expr RIGHT_PAR LEFT_CURLY expr RIGHT_CURLY')
    def udf(p):
        pass
        return UserDefinedFunction(self.builder, self.module, p[1].getstr(), p[3], p[6])

@self.pg.production('expr : FN_NAME LEFT_PAR expr RIGHT_PAR')
    def udf_call(p):
        pass