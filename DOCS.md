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
The GOLF language has Boolean operators that test for equality, as well as if `x` is less than, greater than, less than or equal to, or greater than or equal to `y`. The following table shows the operators, along with the corresponding syntax:

| Operation                  | Symbol       | Syntax     |
|----------------------------|--------------|------------|
| Greater Than               |     `>`      |  5 > 3     |
| Less Than                  |     `<`      |  4 < 10    |
| Greater Than or Equal To   |     `>=`     |  x >= 10   |
| Less Than or Equal To      |     `<=`     |  y <= 6    |
| Equal To                   |     `==`     |  x == y    |
| Not Equal To               |     `/=`     |  x /= y    |

Variables
---
Variables in the GOLF language are declared using the `var` keyword. Identifiers, that is, the name of the variable, can be one or more characters in length, and they cannot start with a number or an undescore. In addition to these rules, it is not legal to use the name of a keyword as a variable name. The following are examples of legal identifiers in the GOLF language:

- `x`
- `Score`
- `letter_array`

Examples of non-legal identifiers include the following: 

| Identifier | Reason                    |
-----------------------------------------|
| `_myscore` | Starts with an underscore |
| `0x23`     | Starts with a number      |
| `if`       | `if` is a keyword         |

An example of a legal program is the following: 

    var x := 23;
    var y := 19;
    print (x + y);

In the above example, values are assigned to the variables `x` and `y`, then the values are added together and the result is returned to the user.

Control Flow
---
Control flow in GOLF has two main forms; if-then statements, and if-then-else statements. The former kind of statement has the following syntax:

    if expr then {
        expr
    };
    
Because they are statements, the block ends with a semicolon. This is different to a language like Java, which has if-then statements which do not end in a semcolon. The second type of conditional statement in GOLF is the if-then-else statement, which extends the standard if-then statement as in other languages to allow for multiple Boolean conditions to be checked. The syntax for this second for of conditional statement is the following: 

    if expr then {
        expr
    } else {
        expr
    };
