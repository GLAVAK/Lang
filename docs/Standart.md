# Programming language with no name yet, standart
## Code block

Program consists of blocks, which is statements enclosed in square or curly brackets. Code blocks enclosed in square brackets (`[a = 3]v`) may have one of direction symbols before or after them. Code block enclosed in curly brackets (`<{a > 2}>`) is conditional block. They should have direction symbols on both sides.
Code block can contain only directional symbol, and be used to redirect the program execution.

Directional symbol - one of the: `>`, `^`, `<`, `v`. Symbols `o` and `x` will be used for layer navigation, which is not supported yet.

## Program execution

Abstract machine starts at the top-left corner of you programm, moving right. When it reaches code block, whether it is conditional, normal, or empty block, it evaluates statement in it, if any. After the block machine continues execution in the direction of block's directional symbol, at from symbol's exact position. If there are no blocks in this direction, it jumps to another side of file and starts over (like in a snake game)

## Fall-through blocks

If statement block have no directional symbols around, it is considered as fall-through block. This means that whenever abstract machine reached it, after it evaluates expression inside it continues from the exact point it hit the block. This behaviour allows to reduce amount of duplicate code, like in this example:
```
[italic = false]v
         v{italic}v

[write("<b>")] [write("<i>")]

      [write("content")]

[write("</b>")] [write("</i>")]

        [exit()]  <
```
Code block `[write("content")]` is written once, but included in both braches of condition.

## Conditions

After the abstract machine reaches this block, it evaluates statement inside, which has to have Boolean type (b). If the statement is true goes to direction set by direction symbol on the right, and if it is false on the left.

## Variables

*Note: there are no layers realization yet*

Variables can be local for current layer, or global for all programmm layers. Variables in a PascalCase will be global, when camelCase will be local. To define variable simply assign to it. You can read from variable before assigning to it, in this case default value of it's type will be returned. You can't read from a variable if it have no assignment in program.

## Types:

Every variable has it's predefined type, you can't write `[a = 42]>[a = 5.2]`. To declare floating point constant add a decimal point, `[a = 42.]`. Implicit conversion of all types forbidden. Variables must be explicitly converted to the same type to perform operations (write `<{42. > 5.2}>` instead of `<{42 > 5.2}>`). Explicit conversion is `i()`, `s()`, and `f()`. There are no conversion functions from or to boolean (~~`b()`~~)

| Shortcut | Type name | Constants format     |
| -------- | --------- | -------------------- |
| i        | Integer   | `42`, `-15`          |
| f        | Float     | `42.`, `.1`, `12.21` |
| b        | Boolean   | `true` or `false`    |
| s        | String    | `"string"`, `""`     |

## Statements

Statements always return a value. They can contain vars, constants, calls to macros and operators. Currently supported operators:

_Note: in this section "n" means i or f, and "x" means any type_

| Operator | Operands  | Returns | Description
| -------- | --------- | ------- | ---
| +        | n + n     | n       | Addition
| -        | n - n     | n       | Subtraction
| *        | n * n     | n       | Multiplication
| /        | n / n     | n       | Division
| -        | n         | n       | Invert number
| =        | Varname = x | -     | Assignment
| >        | n > n     | b       | Greater
| <        | n < n     | b       | Less
| >=       | n >= n    | b       | Greater or equal
| <=       | n <= n    | b       | Less or equal
| &        | b & b     | b       | Logical and
| |        | b | b     | b       | Logical or
| !        | b         | b       | Logical not

## Macros

Macros is a special functions to interact vith VM. Currently supported macros:

| Macro     | Operands | Returns        | Description
| --------- | -------- | -------------- | ---
| write(a)  | Any type | a              | Writes to console
| read()    | No       | Read value     | Reads from console
| exit()    | No       | Doesn't matter | Stops the program. Must be at the end