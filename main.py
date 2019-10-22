from lexer import Lexer
from my_parser import Parser
from codegen import CodeGen

fname = "input.lang"
with open(fname) as f:
  text_input = f.read()

# text_input = """
# !(4 + 2 - 3 * 5 / 2)
# """

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

codegen = CodeGen()

module = codegen.module
builder = codegen.builder
printf = codegen.printf

pg = Parser()
pg.parse()
parser = pg.get_parser()
parser.parse(tokens).eval()

