import platform

from lexer import Lexer
from my_parser import Parser
from codegen import CodeGen

from error import FileNotExistsError
from error import LexerError

import os
from pathlib import Path
import sys

"""
This section defines the behaviour of the command-line arguments to the compiler
"""

current_dir = os.getcwd()
args = [arg for arg in sys.argv]
# print(args)

for arg in args:
    match arg:
        case "-g" | "--golf":
            # Golf mode
                with open(sys.argv[1]) as f:
                    if len(f.read()) > 5000:
                        print("""File too long! In Golf mode, files must not exceed 5000 characters!""")
                        exit()

        case "-s" | "--shell":
            # Shell mode
            input("golf> ")
        
        case "-c" | "--clear":
            # Clear
                # Find the correct extension for the output file
                os = platform.system()
                ext = ""
                match os:
                    case "Linux" | "Darwin":
                        ext += ".out"
                    case "Windows":
                        ext += ".exe"
                    case _:
                        print("OS not supported. Exiting program...")
                        exit()

                files = (Path(f"{sys.argv[1]}.ll"), f"a{ext}")
                path = Path(current_dir)
                for file in path.glob('*'):
                    full_name = file.name + file.stem
                    if full_name in files:
                        os.remove(full_name)
        
        case "-h" | "--help":
                args_list = "[[\"--help\", \"-h\"], [\"--clear\", \"-c\"], [\"--shell\", \"-s\"], [\"--golf\", \"-g\"]]"
                print(f"python main.py <source_file> {args_list}")
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
    
    # First, check if the file exists
    # If the file exists, read the file 
    for file in p.rglob("*"):
        if file.name == file_arg:
            parents = list(file.parents)
            idx_0 = str(parents[0])
            # Change directory
            os.chdir(idx_0)
            # Reading the source file
            with open(file_arg) as source:
                return source.read()
    # If the file does not exist, error
    else:
        raise FileNotExistsError("The file does not exist!")

text_input = find_file()

# Creating a lexer and passing the source code into it
lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

# Create a code generator object
codegen = CodeGen()

# Assign the variables to the code generator
module = codegen.module
builder = codegen.builder
printf = codegen.printf
# printstr = codegen.printstr

# Create a parser object and parse the list of tokens created by the lexer.
pg = Parser(module, builder, printf) # , printstr)
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
