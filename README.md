<p align="center">
<img width="200" height="300" src="images/golf_pl_logo.png"></img>
</p>

# Compiler
This repository contains the source code for my compiler. I have also included source files for the language that is being compiled. The language I am compiling is of my own devising. This compiler was written for my BSc research project as part of my degree at the University of Kent. 

# Version History
Version 0.0.1
---
This version of the compiler is a very rudimentary edition, and acts like a calculator. It features all the basic arithmetic operations, including addition, subtraction, multiplication and division. It also supports the modulus operation. 

Version 0.0.2
---
Version 0.0.2 introduces the capability to parse multiple statements from a file, so that programs longer than a single line are able to be handled by the compiler. It also adds the capability to perform comparisons with Boolean results, using operators such as `>`, `>=`, `<`, `<=`, `==`, and `/=`. The Boolean values of `true` and `false` are represented as `1` and `0` respectively,  

This version of the compiler also adds support for variables. It uses the LLVMlite library in Python to allocate the amount of space required on the stack for the type of variable in question, then it stores the specified value in that newly-allocated space on the stack. When the variable is required, the value is loaded into memory and returned. 

Version 0.0.3
---
Version 0.0.3 of the compiler adds types for strings and characters, so that the functionality can be extended beyond basic arithmetical expressions. Version 0.0.3 also adds `if-then` and `if-then-else` blocks to the language, allowing the programmer to perform operations based on Boolean conditions.

Version 0.0.4
---
Version 0.0.4 introduces the capability to increment and decrement the value of variables using the `+=` and `-=` operators, as well as the `while` loop and the ability for users to write their own functions. 

**References**
- https://blog.usejournal.com/writing-your-own-programming-language-and-compiler-with-python-a468970ae6df
- https://tomassetti.me/ebnf/
