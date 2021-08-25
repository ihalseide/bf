# Brainf\*ck Interpreter and Compiler

This project has two Python scripts that you can run: `bf.py`, which is an interpreter, and `bfc.py` which is a compiler. Brainf\*ck is proven to be Turing-complete, and since this project shows that Python can simulate brainf\*ck, it follows that Python is Turing-complete. Hehe.

## The Interpreter

The interpreter is a Python program that interprets bf code. Run `$ python bf.py (file)` to run the interpreter on a bf program file.

    usage: bf.py [-h] [-n NUM_CELLS] [--EOF_value EOF_VALUE] file
    
    positional arguments:
      file                  the bf program, a "-" signifies to read from stdin
    
    optional arguments:
      -h, --help            show this help message and exit
      -n NUM_CELLS          number of cells on the tape (default is 65535)
      --EOF_value EOF_VALUE
                            end-of-file value in the range 0-255 (default is not to write any value)

Use '-' as file to read the program from stdin. When reading from stdin, the '!' exclamation mark character denotes the end of the program and the start of the data.

## The Compiler

The compiler is a Python program that transforms bf code into C code. Run `$ python bfc.py (file)` to compile a bf program file. The compiler does the small optimization of compressing strings of +- and separately >< down to single C statements.

    usage: bfc.py [-h] [-s] [-num_cells NUM_CELLS] [--EOF_value EOF_VALUE] file
    
    positional arguments:
      file
    
    optional arguments:
      -h, --help            show this help message and exit
      -num_cells NUM_CELLS  number of memory tape cells (default is 65535)
	  -s                    small code formatting for C output
      --EOF_value EOF_VALUE
                            end-of-file value in the range 0-255 (default is not to write any value)

## Example Program

You can run `$ python bf.py -` and then type `,[.[-],]!`. That runs a "cat" program (a program that repeats its input).

## Brainf\*ck Language Description

The brainf\*ck machine consists of a tape of memory cells initially set to zero and a memory pointer. Each memory cell on the tape is represented by a single byte and can hold any value between 0 and 255, inclusive. The cell values overflow and underflow, so if a memory cell is incremented above 255, the value wraps back around to 0, or if a memory cell is decremented below 0, the value wraps back around to 255. The memory pointer can point to any of the memory cells and initially points to the first one. A program consists of a sequence of 1-character commands that affect the pointer and control flow. The commands are:

* \>	Move the pointer to the right
* <	Move the pointer to the left (but the pointer cannot be negative)
* \+	Increment the memory cell at the pointer
* \-	Decrement the memory cell at the pointer
* .	Output the character signified by the cell at the pointer
* ,	Input a character and store it in the cell at the pointer
* [	Jump past the matching ] if the cell at the pointer is 0 (flow control)
* ]	Jump back to the matching [ if the cell at the pointer is nonzero (flow control)

All characters other than the commands are considered comments and ignored, except for the '!' exclamation mark when reading from stdin.

## Disclaimer

I did not invent the programming language in question. This project's code is just my implementation! For more information, I recommend reading this webpage: [https://esolangs.org/wiki/Brainfuck].

## License

This project is licensed under the MIT License. See the file called LICENSE.txt for more information.

