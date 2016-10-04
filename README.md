# Programming language with no name yet
## Why?
Because I can. Language have no real practical meaning, except, maybe, visual block diagram-like style.

## Idea
You write code by drawing ASCII-graphics block diagram of your program in txt file
Here is the example of counting 10 fibbonachi numbers:
```
             v[count = 11]
             v[a1 = 0]
             v[a2 = 1]
             v                      <
             v[a3 = a1 + a2]
             v[a1 = a2]
[exit()]     v[a2 = a3]             ^[write(a1)]
             v[count = count - 1]
^            <{count > 0}>          ^
```

Statements are in square brackets, arrow (<, >, v, ^) at the right or left of it defines the control flow direction. Just arrows redirects the flow. And conditions are in curly brackets, with arrows on both sides, if the statement inside is true flow goes right, otherwise it goes left
You can assign only integer numbers(yet) to the vars, by just assigning to them

## VM, bytecode and realization details
For planned features support (maybe I'll be able to add some OOP and GC), and rather just because I want to, this gets compiled not to real machine code, but to bytecode. It's similar to Java bytecode, for stack virtual machine. Specs of bytecode is in `docs` folder. VM are written in C (in a very bad perfomance way yet), and the compiler on python3
