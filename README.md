# Brainfuck Interpreter and Compiler

This project has one Python script that you can run: `bf.py`,
which is an interpreter and a compiler.
Brainfuck is Turing-complete,
and since this project shows that Python can simulate brainfuck,
it follows that Python is Turing-complete.
The GitHub repository for this project is https://github.com/ihalseide/bf.

For more information, I recommend reading this webpage: [https://esolangs.org/wiki/Brainfuck].

## Quick start

This interprets/simulates/runs a "hello world" example program.

```console
python bf.py sim examples/hello.bf
```

## Features

This program is both an interpreter and a compiler.
Programs may be compiled to Python source or to C source.
This program checks the given source code for balanced brackets before running or compiling the program.
It reports errors with location information if there is an unbalanced bracket.

## Language Description

(This description is almost an exact copy from Esolangs.org).

The brainfuck machine consists of a tape of memory cells initially set to zero and a memory pointer.
Each memory cell on the tape is represented by a single byte and can hold any value between 0 and 255, inclusive.
The cell values overflow and underflow,
so if a memory cell is incremented above 255,
the value wraps back around to 0,
or if a memory cell is decremented below 0,
the value wraps back around to 255.
The memory pointer can point to any of the memory cells and initially points to the first one.
A program consists of a sequence of 1-character commands that affect the pointer and control flow.

The commands are:
* `>`	Move the pointer to the right
* `<`	Move the pointer to the left (but the pointer cannot be negative)
* `+`	Increment the memory cell at the pointer
* `-`	Decrement the memory cell at the pointer
* `.`	Output the character signified by the cell at the pointer
* `,`	Input a character and store it in the cell at the pointer
* `[`	Jump past the matching ] if the cell at the pointer is 0 (flow control)
* `]`	Jump back to the matching [ if the cell at the pointer is nonzero (flow control)

All characters other than the commands are considered comments and ignored,
except for the '!' exclamation mark when reading from the standard input stream.

## License

MIT license.
See the LICENSE file for more info.

