#!/usr/bin/env python3

import sys
from sys import stdout, stdin, stderr, exit

# Allowed bf characters
ALLOWED = '+-<>,.[]'

# Split program and data based on this character when reading the program from stdin
SPECIAL = '!'

def perror (*args, **kwargs):
    print(sys.argv[0]+':', *args, **kwargs, file=stderr)

def simulate_program (program, matches_start, matches_end):
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
            sys.stdout.write(chr(memory[cp]))
        elif ',' == char:
            # Input a character and store it in the cell at the pointer
            c = sys.stdin.read(1) # Note: c will be empty str upon EOF
            if c:
                memory[cp] = ord(c)
            elif EOF_value is not None: 
                memory[cp] = EOF_value
        elif '[' == char and not memory[cp]:
            # Jump past the matching ] if the cell at the pointer is 0
            ip = matches_start[ip]
        elif ']' == char and memory[cp]:
            # Jump back to the matching [ if the cell at the pointer is not 0
            ip = matches_end[ip]
        if cp not in range(num_cells):
            perror('bf error:', 'at program index %d, the pointer moved off of the memory tape (to cell %d)' %(ip + 1, cp))
            exit(1)
        ip += 1

def compile_program (program, num_cells, matches_start, matches_end, out_file):
    emit = lambda *args: print(*args, file=out_file)

    emit("    .section .data")
    emit("tape: .fill %d" % num_cells)
    emit("    .section .text")
    emit("    .global _start")
    emit("_start:")
    emit("    mov rax, tape")
    emit("    ; -- End of init. --")

    label_counter = 0
    label_counter_stack = []

    i = 0
    while i < len(program):
        char = program[i]
        if char in "<>":
            ptr_change = 0
            while char in "<>":
                char = program[i]
                if "<" == char:
                    ptr_change -= 1
                else:
                    ptr_change += 1
                i += 1

            emit("    add rax, %d" % ptr_change)

            del ptr_change
            i -= 1
            continue
        elif char in "+-":
            val_change = 0
            while char in "+-":
                char = program[i]
                if '-' == char:
                    val_change -= 1
                else:
                    val_change += 1
                i += 1

            emit("    mov [rax], bl")
            emit("    add bl, %d" % val_change)
            emit("    mov bl, [rax]")

            del val_change
            i -= 1
            continue
        elif "[" == char:
            emit("begin_%d:" % label_counter)
            emit("    mov [rax], bl")
            emit("    test bl, 0")
            emit("    jz end_%d" % label_counter)

            label_counter_stack.append(label_counter)
            label_counter += 1
        elif "]" == char:
            assert len(label_counter_stack) != 0, "There should be label_id's on the stack"
            label_id = label_counter_stack.pop()

            emit("    jmp begin_%d" % label_id)
            emit("end_%d:" % label_id)

            del label_id
        elif "." == char:
            assert False, "not implemented"
        elif "," == char:
            if eof_value == None:
                assert False, "not implemented"
            else:
                assert False, "not implemented"
        else:
            # ignore other characters
            pass
        i += 1

    emit("    ; -- Exit --")
    emit("    mov rax, 60")
    emit("    syscall")

def process_brackets (program: str):
    # Preprocess the brackets matches:
    matches_start = dict() # maps '[' to ']'
    matches_end = dict() # maps ']' to '['
    start_stack = [] # stack of start bracket indices
    line_stack = [] # keep track of line numbers for reporting syntax errors
    line = 1 # line number
    for i, char in enumerate(program):
        if '[' == char:
            start_stack.append(i)
            line_stack.append(line)
        elif ']' == char:
            try:
                start_i = start_stack.pop()
                line_stack.pop()
            except IndexError:
                perror('syntax error:', 'unmatched "]" on line %d, column %d' % (line, i + 1))
                exit(1)
            matches_start[start_i] = i
            matches_end[i] = start_i
        elif '\n' == char:
            line += 1

    if start_stack:
        while start_stack:
            perror('syntax error:', 'unmatched "[" on line %d, column %d' % (line_stack.pop(), start_stack.pop() + 1))
        exit(1)

    return matches_start, matches_end

def print_usage ():
    print("usage: %s [-help] subcommand [options] file" % sys.argv[0])

def print_help ():
    print("  Required arguments:")
    print("    file           File to read program from. Given `-` will")
    print("                   use standard input stream")
    print("  Options:")
    print("    -h,-?          Print this help message and exit")
    print("    -n numCells")
    print("    -eof eofValue")
    print("  Subcommand:")
    print("    com            Compile the program")
    print("    sim            Interpret the program")

if __name__ == '__main__':
    HELP_LIST = ('h', 'help', '-h', '--help', '-?', '-help', '--h')

    # Default option values
    num_cells = 65535
    EOF_value = None
    out_file_name = None

    # Required to be set
    compile_mode = None
    filename = None

    name = sys.argv[0]
    argv = sys.argv[1:]

    if len(argv) == 0:
        print_usage()
        perror("error: not enough arguments")
        exit(1)

    for i, arg in enumerate(argv):
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
            # (opt) number of cells
            if i == len(argv) - 1:
                perror("error: missing value for flag `-n`")
                print_usage()
                exit(1)
            value = argv[i + 1]
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
            # (opt) end of input value
            if i == len(argv) - 1:
                perror("error: missing value for flag `-eof`")
                print_usage()
                exit(1)
            value = argv[i + 1]
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
        else:
            # (required) Filename 
            if filename != None:
                # Extra arguments
                perror("error: unknown extra argument: %s" % repr(arg))
                print_usage()
                exit(1)
            filename = arg

    assert compile_mode != None

    # Filename is required
    if None == filename:
        perror("error: missing required argument `file`")
        print_usage()
        exit(1)

    # Read the program
    program = None
    if '-' == filename:
        # Read from STDIN until a '!'
        program = ''
        while (c := sys.stdin.read(1)) not in ('', SPECIAL):
            program += c
    else:
        # Read from FILE
        with open(filename, 'r') as f:
            program = f.read() 

    # Process the bracket matches
    matches_start, matches_end = process_brackets(program)

    if compile_mode:
        # Default output file name
        out_file = None
        if out_file_name == None:
            if '-' == filename:
                out_file = stdout
            else:
                without_ext = '.'.join(filename.split('.')[:-1])
                out_file_name = without_ext + '.out'
                out_file = open(out_file_name, "w+")
        else:
            out_file = open(out_file_name, "w+")
        compile_program(program, num_cells, matches_start, matches_end, out_file)
    else:
        simulate_program(program, matches_start, matches_end)


