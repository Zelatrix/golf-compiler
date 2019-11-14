import os

from lexer import Lexer
from my_parser import Parser
from codegen import CodeGen

# Test source files
# fname = os.path.join(os.getcwd(), 'golf_files\\demo2.golf')
# fname = os.path.join(os.getcwd(), 'golf_files\\arithmetic.golf')
# fname = os.path.join(os.getcwd(), 'golf_files\\hello.golf')
# fname = os.path.join(os.getcwd(), 'golf_files\\hello2.golf')
# fname = os.path.join(os.getcwd(), 'golf_files\\arithmetic2.golf')
# fname = os.path.join(os.getcwd(), 'golf_files\\zero_divide.golf')
# fname = os.path.join(os.getcwd(), 'golf_files\\normal_divide.golf')
# fname = os.path.join(os.getcwd(), 'golf_files\\print.golf')
fname = os.path.join(os.getcwd(), 'golf_files\\modulus.golf')

# Reading the source file
with open(fname) as f:
    text_input = f.read()

# Creating a lexer and passing the source code into it
lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

# Create a code generator object
codegen = CodeGen()

# Assign the variables to the code generator
module = codegen.module
builder = codegen.builder
printf = codegen.printf

# Create a parser object and parse the list of tokens
# created by the lexer.
pg = Parser(printf)
pg.parse()
parser = pg.get_parser()
parser.parse(tokens).eval(module, builder)

# Save the IR representation into an LL file
codegen.create_ir()
codegen.save_ir("output.ll")
