#!/usr/bin/env python3

'''brainf*ck (bf) interpretter'''

import sys, argparse

# Allowed bf characters
ALLOWED = '+-<>,.[]'

# Split program and data based on this character when reading the program from stdin
SPECIAL = '!'

# Print error
def perror (*args, **kwargs):
    print(sys.argv[0]+':', *args, **kwargs, file=sys.stderr)
    
# Print error and fail
def error (*args, **kwargs):
    perror(*args, **kwargs)
    sys.exit(-1)

# Process command line args:
parser = argparse.ArgumentParser()
parser.add_argument('file', help='the bf program, a "-" signifies to read from stdin')
parser.add_argument('-n', dest='num_cells', default=65535, type=int, help='number of cells on the tape (default is 65535)')
parser.add_argument('--EOF', dest='EOF_value', type=int, default=None, help='end-of-file value within 0-255 (default is not to write any value)')
args = parser.parse_args()
# Validate EOF value
if args.EOF_value is not None and args.EOF_value not in range(255):
    error('error:', 'agument:', 'the EOF value must be in between 0 and 255')
# Read the program
if '-' == args.file:
    # Read from STDIN until a '!'
    program = ''
    while (c := sys.stdin.read(1)) not in ('', SPECIAL):
        program += c
else:
    # Read from FILE
    with open(args.file, 'r') as f:
        program = f.read() 

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
            error('syntax error:', 'unmatched "]" on line %d, column %d' % (line, i + 1))
        matches_start[start_i] = i
        matches_end[i] = start_i
    elif '\n' == char:
        line += 1
if start_stack:
    while start_stack:
        perror('syntax error:', 'unmatched "[" on line %d, column %d' % (line_stack.pop(), start_stack.pop() + 1), fatal=False)
    sys.exit(-1)
del start_stack, line_stack

# Initialize the machine
memory = bytearray([0 for x in range(args.num_cells)])
cp = 0 # cell/memory tape pointer
ip = 0 # intruction pointer

# Start interpreting
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
        elif args.EOF_value is not None: 
            memory[cp] = args.EOF_value
    elif '[' == char and not memory[cp]:
        # Jump past the matching ] if the cell at the pointer is 0
        ip = matches_start[ip]
    elif ']' == char and memory[cp]:
        # Jump back to the matching [ if the cell at the pointer is not 0
        ip = matches_end[ip]
    if cp not in range(args.num_cells):
        error('bf error:', 'at program index %d, the pointer moved off of the memory tape (to cell %d)' %(ip + 1, cp))
    ip += 1

