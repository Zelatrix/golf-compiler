from lexer import Lexer
from my_parser import Parser
from codegen import CodeGen
from ast import *

import os
from pathlib import Path
import sys

# Golf mode
# def golf_mode():
#     if len(sys.argv[1].read()) > 5000:
#         print("File too long!")
#         print("In Golf mode, files must not exceed 5000 characters!")
#         exit()

# Finding the source file in the directory tree
def find_file():
    file_arg = sys.argv[1]
    p = Path("golf_files")
    for file in p.glob("*"):
        if file.name == file_arg:
            # Change directory
            os.chdir(str(p))
            # Reading the source file
            with open(file_arg) as f:
                return f.read()


text_input = find_file()
# print(text_input)

# Creating a lexer and passing the source code into it
lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

# for tok in tokens:
#    print(tok)

# Create a code generator object
codegen = CodeGen()

# Assign the variables to the code generator
module = codegen.module
builder = codegen.builder
printf = codegen.printf

# Create a parser object and parse the list of tokens created by the lexer.
pg = Parser(module, builder, printf)
# print(module)
pg.parse()
parser = pg.get_parser()

# Loop through the list of statements, and evaluate
# each one.
# for stmt in parser.parse(tokens):
#    codegen.visit(stmt)

# Save the IR representation into an LL file
# codegen.create_ir()
# os.chdir("..")
# codegen.save_ir("output.ll")

# if sys.argv[2] == "--golf":
#     golf_mode()
