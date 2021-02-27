# Brainf*ck Interpreter and Compiler

Run `bf.py [filename]` to run the interpreter on a bf program file, and run `bfc.py` to compile a bf program file. Both the interpreter and the compiler have a bunch of command line arguments to customize.

The compiler does a small optimization of compressing strings of +- and >< down to single C statements. The compiler compiles bf code to C code, which you can then pass through whatever C compiler.

## Example

You can run `bf.py` and then type ",[.[-],]!" to run a "cat" program (a program that repeats all of it's input).

## This is the normal language description

Brainf*ck operates on an array of memory cells, each initially set to zero. (In the original implementation, the array was 30,000 cells long, but this may not be part of the language specification; different sizes for the array length and cell size give different variants of the language). There is a pointer, initially pointing to the first memory cell. The commands are:

Command	Description

```
>	Move the pointer to the right
<	Move the pointer to the left
+	Increment the memory cell at the pointer
-	Decrement the memory cell at the pointer
.	Output the character signified by the cell at the pointer
,	Input a character and store it in the cell at the pointer
[	Jump past the matching ] if the cell at the pointer is 0
]	Jump back to the matching [ if the cell at the pointer is nonzero
```

All characters other than the ><+-.,[] are considered comments and ignored. 
