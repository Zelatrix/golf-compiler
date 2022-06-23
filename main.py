import platform

from lexer import Lexer
from my_parser import Parser
from codegen import CodeGen

import os
from pathlib import Path
import sys

"""
This section defines the behaviour of the command-line arguments to the compiler
"""

current_dir = os.getcwd()
args = []
for arg in sys.argv:
    args.append(arg)

# Golf mode
# if ("--golf" in args) or ("-g" in args):
#    with open(sys.argv[1]) as f:
#        if len(f.read()) > 5000:
#            print("File too long!")
#            print("In Golf mode, files must not exceed 5000 characters!")
#            exit()

# Shell mode
# if ("--shell" in args) or ("-s" in args):
#    input("golf> ")

if ("--clear" in args) or ("-c" in args):
    files = (Path(f"{sys.argv[1]}.ll"), "a.exe")
    path = Path(current_dir)
    for file in path.glob('*'):
        f = file.name + file.stem
        if f in files:
            os.remove(f)

if ("--help" in args) or ("-h" in args):
    args_list = "[[\"--help\", \"-h\"], [\"--clear\", \"-c\"], [\"--shell\", \"-s\"], [\"--golf\", \"-g\"]]"
    print("python main.py <source_file> " + args_list)
    print("""
        This compiler generates a file with a .ll extension in the same directory as 
        the source file, which must then be passed into clang to generate a runnable
        executable file.

        --help,  -h : list the available compiler flags
        --clear, -c : delete the compiled files from the previous run to generate new ones
        --shell, -s : enter the interpreter shell
        --golf,  -g : enter golf mode
    """)
    exit()
"""
End of command line section
"""


# Finding the source file in the directory tree
def find_file():
    file_arg = sys.argv[1]
    p = Path("golf_files")

    for file in p.rglob("*"):
        if file.name == file_arg:
            parents = list(file.parents)
            idx_0 = str(parents[0])
            # Change directory
            os.chdir(idx_0)
            # Reading the source file
            with open(file_arg) as source:
                return source.read()


text_input = find_file()

# Creating a lexer and passing the source code into it
lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

# for tok in tokens:
#   print(tok)

# Create a code generator object
codegen = CodeGen()

# # Assign the variables to the code generator
module = codegen.module
builder = codegen.builder
printf = codegen.printf
# printf_str = codegen.printf_str

# Create a parser object and parse the list of tokens created by the lexer.
pg = Parser(module, builder, printf) # , printf_str)
pg.parse()
parser = pg.get_parser()
# print(parser.parse(tokens))

# Loop through the list of statements, and evaluate each one.
for stmt in parser.parse(tokens):
    codegen.visit(stmt)
     # print(stmt)

# Save the IR representation into an LL file
codegen.create_ir()

if platform.system() in ["Windows", "Linux", "Darwin"]:
    os.chdir(current_dir)
    os.chdir("compiled_tests")
    codegen.save_ir(f"{Path(sys.argv[1]).stem}.ll")
else:
    print(f"We do not support {platform.system()}!")
    print("Sorry about that!")
