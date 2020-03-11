# Documentation
To enter the compiler, open a terminal and type ``golf``. You can then type commands and run them directly from the terminal. In order to run pre-written files, open a text editor such as Visual Studio Code, and save the file with a ``.golf`` extension. Navigate to the folder where you have saved your file, and type ``golf <filename> [optional parameters]`` into the terminal. The result of running the code will then be displayed in the terminal. 

**Optional Flags**
As the name suggests, the Golf language has a feature that allows the programmer to play "code golf", that is, to write a program using the fewest lines of code as possible. To enter this mode, pass the flag ``--golf`` when you run your file from the terminal. This mode has a few features which should be noted, and these are listed below:

- Files run in golf mode must be less than 5000 characters 
- If a file exceeds this limit, an error will be thrown and the file will refuse to compile.  

Arithmetic
---
Arithmetic in the GOLF programming language uses the familiar operators that most other languages use; addition, subtraction, multiplication, division, and the modulus operation. 

The language can accept integer arguments to these operations, but the results of the calculations that can be performed are returned as ``double``. This was done due to the fact that it made generating the code for arithmetic operators much easier, as each one returned the same type of value, which meant that there was no need to handle a specific case for any given arguments. The operators responsible for these operations are written as follows: 

| Operation       | Symbol    | Syntax    |
|-----------------|:---------:|:---------:|
| Addition        |    `+`    | `a + b`   |
| Subtraction     |    `-`    | `a - b`   |
| Multiplication  |    `*`    | `a * b`   |
| Division        |    `/`    | `a / b`   |
| Modulus         |   `mod`   | `a mod b` |

Boolean Operators
---
Boolean operators in the Golf language include `>`, `<`, `>=`, `<=`, `==`, `/=`

Variables
---
Variables are declared using the `var` keyword

Control Structures
---
