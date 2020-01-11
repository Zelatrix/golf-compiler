# Compiler
This repository contains the source code for my compiler. I have also included source files for the language that is being compiled. The language I am compiling is of my own devising. This compiler was written for my BSc research project as part of my degree at the University of Kent. 

**Documentation**
To enter the compiler, open a terminal and type ``golf``. You can then type commands and run them directly from the terminal. In order to run pre-written files, open a text editor such as Visual Studio Code, and save the file with a ``.golf`` extension. Navigate to the folder where you have saved your file, and type ``golf <filename> [optional parameters]`` into the terminal. The result of running the code will then be displayed in the terminal. 

**Optional Flags**
As the name suggests, the Golf language has a feature that allows the programmer to play "code golf", that is, to write a program using the fewest lines of code as possible. To enter this mode, pass the flag ``--golf`` when you run your file from the terminal. This mode has a few features which should be noted, and these are listed below:

- Files run in golf mode must be less than 5000 characters 
- If a file exceeds this limit, an error will be thrown and the file will refuse to compile.  

**References**
- https://blog.usejournal.com/writing-your-own-programming-language-and-compiler-with-python-a468970ae6df
- https://tomassetti.me/ebnf/
