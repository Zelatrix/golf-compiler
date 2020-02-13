# Compiler
This repository contains the source code for my compiler. I have also included source files for the language that is being compiled. The language I am compiling is of my own devising. This compiler was written for my BSc research project as part of my degree at the University of Kent. 

**Documentation**
To enter the compiler, open a terminal and type ``golf``. You can then type commands and run them directly from the terminal. In order to run pre-written files, open a text editor such as Visual Studio Code, and save the file with a ``.golf`` extension. Navigate to the folder where you have saved your file, and type ``golf <filename> [optional parameters]`` into the terminal. The result of running the code will then be displayed in the terminal. 

**Optional Flags**
As the name suggests, the Golf language has a feature that allows the programmer to play "code golf", that is, to write a program using the fewest lines of code as possible. To enter this mode, pass the flag ``--golf`` when you run your file from the terminal. This mode has a few features which should be noted, and these are listed below:

- Files run in golf mode must be less than 5000 characters 
- If a file exceeds this limit, an error will be thrown and the file will refuse to compile.  

**Version History**
----
version_number: 1.0.0
date: 10/02/20
---
This version of the compiler is a very rudimentary edition, and acts like a calculator. It features all the basic arithmetic operations, including addition, subtraction, multiplication and division. It also supports the modulus operation. 

version_number: 1.1.0
date: 10/02/20
---
This version of the compiler adds support for variables. It uses the LLVMlite library in Python to allocate the amount of space required on the stack for the type of variable in question, then it stores the specified value in that newly-allocated space on the stack. When the variable is required, the value is loaded into memory and returned. 

Version 1.1.0 also introduces the capability to parse multiple statements from a file, so that programs longer than a single line are able to be handled by the compiler. 

version_number: 1.2.0
date: 
---


version_number: 1.3.0
date: 
---


**References**
- https://blog.usejournal.com/writing-your-own-programming-language-and-compiler-with-python-a468970ae6df
- https://tomassetti.me/ebnf/
