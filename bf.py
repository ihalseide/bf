#!/usr/bin/env python3

import os, sys
from sys import stdout, stdin, stderr, exit

# Split program and data based on this character when reading the program from stdin
SPECIAL = '!'

# Whether to check the loop nesting level when compiling for Python.
# (Nice to have because the standard Python interpreter has a block stack limit)
NEST_CHECK = True

def perror (*args, **kwargs):
    print(sys.argv[0]+':', *args, **kwargs, file=stderr)

def simulate_program (program, matches_start, matches_end, EOF_value=None):
    memory = bytearray([0 for x in range(num_cells)])
    cp = 0 # cell/memory tape pointer
    ip = 0 # intruction pointer

    while ip < len(program):
        char = program[ip]
        if '>' == char:
            # Move the cell pointer to the right
            cp += 1
        elif '<' == char:
            # Move the cell pointer to the left
            cp -= 1
        elif '+' == char:
            # Increment the cell at the pointer
            memory[cp] = (memory[cp] + 1) % 256
        elif '-' == char:
            # Decrement the cell at the pointer
            memory[cp] = (memory[cp] - 1) % 256
        elif '.' == char:
            # Output the character at the cell pointer
            os.write(1, bytes([memory[cp]]))
        elif ',' == char:
            # Input a character and store it in the cell at the pointer
            c = os.read(0, 1) # Note: c will be empty str upon EOF
            if c:
                memory[cp] = ord(c)
            elif EOF_value is None:
                # Do not change the cell
                pass
            else:
                memory[cp] = EOF_value
        elif '[' == char and not memory[cp]:
            # Jump past the matching ] if the cell at the pointer is 0
            ip = matches_start[ip]
        elif ']' == char and memory[cp]:
            # Jump back to the matching [ if the cell at the pointer is not 0
            ip = matches_end[ip]
        else:
            # Ignore other characters
            pass

        if cp not in range(num_cells):
            perror('bf error:', 'at program index %d, the pointer moved off of the memory tape (to cell %d)' %(ip + 1, cp))
            exit(1)

        ip += 1

# Compile program to C
def compile_program_to_c(program, num_cells, out_file, EOF_value=None, pretty=False):
    # Indentation to make it look nice
    emit = None
    one_indent = '  '
    indent = 0
    if pretty:
        emit = lambda *args: print(one_indent*indent, *args, file=out_file, sep='')
    else:
        emit = lambda *args: print(*args, file=out_file, sep='')

    emit("#include <stdio.h>")
    emit("static unsigned int p = 0;")
    emit(f"static char m[{num_cells}] = {{}};")
    # Character input function
    if EOF_value is None:
        emit("void i(void) { int c = getchar(); if (c != EOF) m[p] = (char) c; }")
    else:
        emit(f"void i(void) {{ int c = getchar(); if (c != EOF) m[p] = (char) c; else c = {EOF_value}; }}")
    emit("int main(void) {")
    indent += 1

    label_counter = 0
    label_counter_stack = []

    i = 0
    while i < len(program):
        char = program[i]
        if char in "<>":
            # Combine multiple arrows
            ptr_change = 0
            while i < len(program) and program[i] in "<>":
                if "<" == program[i]:
                    ptr_change -= 1
                else:
                    ptr_change += 1
                i += 1
            if ptr_change > 0:
                emit(f"p += {ptr_change};")
            elif ptr_change < 0:
                ptr_change = -ptr_change
                emit(f"p -= {ptr_change};")
            # Ignore 0 change
            del ptr_change
            continue
        elif char in "+-":
            # Combine multiple increments/decrements
            val_change = 0
            while i < len(program) and program[i] in "+-":
                if '-' == program[i]:
                    val_change -= 1
                else:
                    val_change += 1
                i += 1
            if val_change > 0:
                # Positive
                emit(f"m[p] += {val_change};")
            elif val_change < 0:
                # Negative
                val_change = -val_change
                emit(f"m[p] -= {val_change};")
            # Ignore 0 change
            del val_change
            continue
        elif "[" == char:
            # Start of loop
            if NEST_CHECK and len(label_counter_stack) >= 20:
                perror(f"compile error: (at index {i}) cannot have more than 20 nested loops because it violates Python syntax")
                exit(1)
            emit(f"while (m[p]) {{ /* begin loop #{label_counter} */")
            label_counter_stack.append(label_counter)
            label_counter += 1
            # increase indentation level
            indent += 1
        elif "]" == char:
            # End of loop
            assert len(label_counter_stack) != 0, "There should be label_id's on the stack"
            label_id = label_counter_stack.pop()
            # decrease indentation level
            indent -= 1
            emit(f"}} /* end loop #{label_id} */")
            del label_id
        elif "." == char:
            # Output
            emit("putchar(m[p]);")
        elif "," == char:
            # Input
            emit("i();")
        else:
            # Ignore other characters
            pass
        # Next character
        i += 1
    emit("return 0;");
    # un-indent
    indent -= 1
    emit("}")

# Compile program to Python
def compile_program_to_python(program, num_cells, out_file, EOF_value=None):
    # Python: where indentation is required
    one_indent = ' '
    indent = ''

    emit = lambda *args: print(indent, *args, file=out_file, sep='')

    emit("# Program Init")
    emit("import os")
    emit("p = 0")
    emit(f"m = bytearray([0 for i in range({num_cells})])")
    if EOF_value is None:
        emit("def i(): c = os.read(0, 1); m[p] = ord(c) if c else m[p]")
    else:
        emit(f"def i(): c = os.read(0, 1); m[p] = ord(c) if c else {EOF_value}")
    emit("def o(): os.write(1, bytes([m[p]]))")
    emit("# Program Body Begin")

    label_counter = 0
    label_counter_stack = []

    i = 0
    while i < len(program):
        char = program[i]
        if char in "<>":
            # Combine multiple arrows
            ptr_change = 0
            while i < len(program) and program[i] in "<>":
                if "<" == program[i]:
                    ptr_change -= 1
                else:
                    ptr_change += 1
                i += 1
            if ptr_change > 0:
                emit(f"p += {ptr_change}")
            elif ptr_change < 0:
                ptr_change = -ptr_change
                emit(f"p -= {ptr_change}")
            # Ignore 0 change
            del ptr_change
            continue
        elif char in "+-":
            # Combine multiple increments/decrements
            val_change = 0
            while i < len(program) and program[i] in "+-":
                if '-' == program[i]:
                    val_change -= 1
                else:
                    val_change += 1
                i += 1
            if val_change > 0:
                # Positive
                emit(f"m[p] = (m[p] + {val_change}) % 256")
            elif val_change < 0:
                # Negative
                val_change = -val_change
                emit(f"m[p] = (m[p] - {val_change}) % 256")
            # Ignore 0 change
            del val_change
            continue
        elif "[" == char:
            # Start of loop
            if NEST_CHECK and len(label_counter_stack) >= 20:
                perror(f"compile error: (at index {i}) cannot have more than 20 nested loops because it violates Python syntax")
                exit(1)
            emit(f"while m[p]: # begin loop #{label_counter}")
            label_counter_stack.append(label_counter)
            label_counter += 1
            # increase indentation level
            indent += one_indent
        elif "]" == char:
            # End of loop
            assert len(label_counter_stack) != 0, "There should be label_id's on the stack"
            label_id = label_counter_stack.pop()
            emit(f"# end loop #{label_id}")
            # decrease indentation level
            indent = indent[:-len(one_indent)]
            del label_id
        elif "." == char:
            # Output
            emit("o()")
        elif "," == char:
            # Input
            emit("i()")
        else:
            # Ignore other characters
            pass
        # Next character
        i += 1
    emit("# Program Body End")

# Validate and create a lookup table for the bracket match locations within the program string
def process_brackets (program: str):
    # Preprocess the brackets matches:
    matches_start = dict() # maps '[' to ']'
    matches_end = dict() # maps ']' to '['
    start_stack = [] # stack of start bracket indices
    line_stack = [] # keep track of line numbers for reporting syntax errors
    line = 1 # source line number
    col = 1 # source column number
    for i, char in enumerate(program):
        if '[' == char:
            start_stack.append(i)
            line_stack.append(line)
        elif ']' == char:
            try:
                start_i = start_stack.pop()
                line_stack.pop()
            except IndexError:
                perror("syntax error:", f"unmatched \"]\" on line {line}, column {col}")
                exit(1)
            matches_start[start_i] = i
            matches_end[i] = start_i
        elif '\n' == char:
            line += 1
            col = 0
        col += 1

    if start_stack:
        while start_stack:
            perror('syntax error:', 'unmatched "[" on line %d, column %d' % (line_stack.pop(), start_stack.pop() + 1))
        exit(1)

    return matches_start, matches_end

def print_usage ():
    name = sys.argv[0]
    print(f"usage: {name} [-h] <OR> {name} subcommand [options] file")

def print_help ():
    print("  Program for interpretting or compiling brainfuck.")
    print()
    print("  Required arguments:")
    print("    file           File to read program from. Given `-` will")
    print("                   use standard input stream.")
    print("  Options:")
    print("    -h,            Print this help message and exit.")
    print("    -n numCells    Number of cells to allocate for the memory tape.")
    print("    -eof eofValue  Number between 0 and 255 to use as the")
    print("                   end-of-file value. If not specified,")
    print("                   the cell value will not be changed by default.")
    print()
    print("  Subcommand:")
    print("    com            Compile the program to Python.")
    print("    sim            Interpret the program.")
    print()
    print("  Compiling options:")
    print("    -t target      Compilation target: 'py' and 'c' are supported.")
    print("                   ('c' is the default)")
    print()

if __name__ == '__main__':
    HELP_LIST = ('h', 'help', '-h', '-help')

    # Default option values
    num_cells = 65535
    EOF_value = None
    out_file_name = None

    # Required to be set
    compile_mode = None
    filename = None

    # For `com` mode only
    target_value = None

    name = sys.argv[0]
    argv = sys.argv[1:]

    if len(argv) == 0:
        perror("error: not enough arguments")
        print_usage()
        exit(1)

    args_it = enumerate(argv)
    for i, arg in args_it:
        if arg.lower() in HELP_LIST:
            print_usage()
            print_help()
            exit(1)
        if i == 0:
            # (required) sub-command
            if arg.lower() == "com":
                # compile
                compile_mode = True
            elif arg.lower() == "sim":
                # simulate
                compile_mode = False
            else:
                perror("error: expected `com` or `sim` sub-command")
                print_usage()
                exit(1)
        elif arg.lower() == '-n':
            # (optional) number of cells
            if i == len(argv) - 1:
                perror("error: missing value for flag `-n`")
                print_usage()
                exit(1)
            value = next(args_it)[1]
            try:
                value = int(value)
                if value < 0:
                    perror("error: value for `-n` flag must be above 0")
                    print_usage()
                    exit(1)
                num_cells = value
            except ValueError:
                perror("error: value for `-n` flag must be an integer")
                print_usage()
                exit(1)
        elif arg.lower() == '-eof':
            # (optional) end of input value
            if i == len(argv) - 1:
                perror("error: missing value for flag `-eof`")
                print_usage()
                exit(1)
            value = next(args_it)[1]
            try:
                value = int(value)
                if value < 0 or value > 255:
                    perror("error: value for `-eof` flag must be in range 0..255")
                    print_usage()
                    exit(1)
                EOF_value = value
            except ValueError:
                perror("error: value for `-eof` flag must be an integer")
                exit(1)
        elif arg.lower() == '-t':
            # target
            if i == len(argv) - 1:
                perror("error: missing value for target `-t`")
                print_usage()
                exit(1)
            target_value = next(args_it)[1]
        elif arg == '--':
            break
        else:
            # (required) Filename
            if filename != None:
                # Extra arguments
                perror("error: unknown extra argument: %s" % repr(arg))
                print_usage()
                exit(1)
            filename = arg

    # The subcommand must have been set or we should have already returned an error
    assert compile_mode is not None

    # default compilation target
    if target_value is None:
        target_value = 'c'

    # check compilation targets
    targets = ('c', 'py')
    if target_value not in targets:
        perror(f"error: target specified by `-t` must be in {targets}")
        exit(1)

    # Filename is required
    if filename is None:
        perror("error: missing required argument `file`")
        print_usage()
        exit(1)

    # Read the program
    program = None
    if '-' == filename:
        # Read from STDIN until a '!'
        program = ''
        while (c := os.read(0, 1)) not in ('', SPECIAL):
            program += c
    else:
        # Read from FILE
        with open(filename, 'r') as f:
            program = f.read()

    # Process the bracket matches
    matches_start, matches_end = process_brackets(program)

    if compile_mode:
        # Compile to output file
        out_file = None
        if out_file_name == None:
            # Default output file name
            if '-' == filename:
                out_file = stdout
            else:
                out_file_name = filename + '.' + target_value

        # Log compile target
        print("compiling to", out_file_name)

        with open(out_file_name, "w+") as out_file:
            # Compile to the target
            if target_value == 'c':
                pretty = True
                compile_program_to_c(program, num_cells, out_file, EOF_value, pretty)
            elif target_value == 'py':
                compile_program_to_python(program, num_cells, out_file, EOF_value)
    else:
        # Simulate
        simulate_program(program, matches_start, matches_end, EOF_value)


