# Brainfuck Interpreter and Compiler

This project has two Python scripts that you can run: `bf.py`, which is an interpreter, and `bfc.py` which is a compiler.

## The Interpreter

The interpreter is a Python program that interprets bf code. Run `$ python bf.py (file)` to run the interpreter on a bf program file.

    usage: bf.py [-h] [-n NUM_CELLS] [-d] [--EOF_value EOF_VALUE] file
    
    positional arguments:
      file                  the bf program, a "-" signifies to read from stdin
    
    optional arguments:
      -h, --help            show this help message and exit
      -n NUM_CELLS          number of cells on the tape (default is 65535)
      -d                    debug flag
      --EOF_value EOF_VALUE
                            end-of-file value in the range 0-255 (default is not to write any value)

## The Compiler

The compiler is a Python program that transforms bf code into C code. Run `$ python bfc.py (file)` to compile a bf program file. The compiler does the small optimization of compressing strings of +- and separately >< down to single C statements.

    usage: bfc.py [-h] [-d] [-num_cells NUM_CELLS] file
    
    positional arguments:
      file
    
    optional arguments:
      -h, --help            show this help message and exit
      -d                    whether to generate debug comments in the C output
      -num_cells NUM_CELLS  number of memory tape cells (default is 65535)

## Example Program

You can run `$ python bf.py -` and then type ",[.[-],]!" to run a "cat" program (a program that repeats all of it's input).

## Brainfuck Language Description

Brainfuck operates on an array of memory cells, each initially set to zero. A memory cell can hold any value between 0 and 255, inclusive. If a memory cell is incremented above 255, the value wraps back around to 0. Also, if a memory cell is decremented below 0, the value wraps back around to 255. There is a pointer to the array of memory cells that initially points to the first memory cell. A program consists of a sequence of commands. The commands are:

* \>	Move the pointer to the right
* <	Move the pointer to the left (but the pointer cannot be negative)
* \+	Increment the memory cell at the pointer
* \-	Decrement the memory cell at the pointer
* .	Output the character signified by the cell at the pointer
* ,	Input a character and store it in the cell at the pointer
* [	Jump past the matching ] if the cell at the pointer is 0
* ]	Jump back to the matching [ if the cell at the pointer is nonzero

All characters other than the commands are considered comments and ignored. 

## Disclaimer

I did not invent the programming language in question. This project's code is just my implementation! For more information, I recommend reading this webpage: [https://esolangs.org/wiki/Brainfuck].

## License

This project is licensed under the MIT License. See the file called LICENSE.txt for more information.

