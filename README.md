<p align="center">
<img width="200" height="300" src="images/golf_pl_logo.png"></img>
</p>

# Compiler
This repository contains the source code for my compiler. I have also included source files for the language that is being compiled. The language I am compiling is of my own devising. This compiler was written for my BSc research project as part of my degree at the University of Kent. 

NOTE: The file must be located in the same directory as the compiler's source files so it can find the file correctly. The structure is only to improve the organisation, and I am working on a way to dynamically provide an absolute file path!

# Version History
Version 0.0.1
---
This version of the compiler is a very rudimentary edition, and acts like a calculator. It features all the basic arithmetic operations, including addition, subtraction, multiplication and division. It also supports the modulus operation. 

Version 0.0.2
---
Version 0.0.2 introduces the capability to parse multiple statements from a file, so that programs longer than a single line are able to be handled by the compiler. It also adds the capability to perform comparisons with Boolean results, using operators such as `>`, `>=`, `<`, `<=`, `==`, and `/=`. The Boolean values of `true` and `false` are represented as `1` and `0` respectively,  

This version of the compiler also adds support for variables. It uses the LLVMlite library in Python to allocate the amount of space required on the stack for the type of variable in question, then it stores the specified value in that newly-allocated space on the stack. When the variable is required, the value is loaded into memory and returned. 

Version 0.2.1
---
Version 0.2.1 of the compiler adds types for strings and characters, so that the functionality can be extended beyond basic arithmetical expressions. Version 0.0.3 also adds `if-then` and `if-then-else` blocks to the language, allowing the programmer to perform operations based on Boolean conditions.

Version 0.3.0
---
Version 0.3.0 introduces the capability to increment and decrement the value of variables using the `+=` and `-=` operators, as well as the `while` loop and the ability for users to write their own functions. Functions in GOLF are defined using the `function` keyword, and the main body of the function is denoted using a pair of curly braces. 

Also in this iteration of the compiler, are two new operations to acompany the `+=` and `-=` operations, namely, the `*=` and `/=` operations to multiply or divide the value of a variable by a specified amount. This iteration also changes the syntax slightly for Boolean negation, as the operator was already in use. To avoid the clash, the Boolean negation operation has been changed to a more Java-like syntax as opposed to a Haskell-like syntax, and it can now be used with the `!=` operator, but it functions the same as before. 

Version 0.3.1
---
Version 0.3.1 adds a suite of automated tests to allow for easier use and program verification. The user will be able to test multiple source files with a single command, rather than running each of the test files individually, which is a potentially time-consuming process.    

Version 0.3.2
---
This version introduces the ability for users to add specifications to the file, which are of the form `{x = 0}`. Such a specification means that the compiler is expecting the variable `x` to have a value of 0, and this can then be used to verify whether the provided specifications are valid


**References**
- https://blog.usejournal.com/writing-your-own-programming-language-and-compiler-with-python-a468970ae6df
- https://tomassetti.me/ebnf/
- https://llvm.discourse.group/t/implementing-in-llvm-ir/3744
- https://github.com/numba/llvmlite/issues/742
