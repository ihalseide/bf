# Brainf*ck interpreter

Run `bf.py [filename]` to run a bf program file. You can modify the python file to fit some variations among brainf*ck interpers / compilers, including the End of File value, and whether and End of File value will be written to a cell or not.

## This is the normal language description

Brainf*ck operates on an array of memory cells, each initially set to zero. (In the original implementation, the array was 30,000 cells long, but this may not be part of the language specification; different sizes for the array length and cell size give different variants of the language). There is a pointer, initially pointing to the first memory cell. The commands are:

Command	Description

>	Move the pointer to the right
<	Move the pointer to the left
+	Increment the memory cell at the pointer
-	Decrement the memory cell at the pointer
.	Output the character signified by the cell at the pointer
,	Input a character and store it in the cell at the pointer
[	Jump past the matching ] if the cell at the pointer is 0
]	Jump back to the matching [ if the cell at the pointer is nonzero

All characters other than ><+-.,[] are considered comments and ignored. But, a few debugging commands are added for convenience. See the extensions below:

## Extensions

Command Description

#	Print out the first few cells of the memory tape
^	Print out the current pointer location
@	Print out the number of cycles / instructions processed
