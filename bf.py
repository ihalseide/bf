#!/usr/bin/env python3 

# bf interpretter

import sys, argparse

def error (*args, **kwargs):
    print(sys.argv[0]+':', *args, **kwargs, file=sys.stderr)
    sys.exit(-1)

parser = argparse.ArgumentParser()
parser.add_argument('file', help='the bf program input file, default is to read stdin')
parser.add_argument('-num_cells', default=65535, type=int, help='number of memory cells')
parser.add_argument('-debug', action='store_true')
parser.add_argument('--EOF_value', type=int, default=None, help='End Of File value, default is not to write any value upon EOF')
args = parser.parse_args()

if args.EOF_value is not None and args.EOF_value not in range(255):
    error('error:', 'agument:', 'EOF_value must be in range(0, 255)')

num_cells = args.num_cells
if args.file == '-':
    # Read program from stdin until a '!'
    program = ''
    while (c := sys.stdin.read(1)) not in ('', '!'):
        program += c
else:
    # Read program from file
    with open(args.file, 'r') as f:
        program = f.read() 

# Preprocess the brackets matches to increase efficiency a little
matches_start = {}  # maps '[' to ']'
matches_end = {}    # maps ']' to '['
start_stack = []
line_stack = []
line = 1
for i, char in enumerate(program):
    if '[' == char:
        start_stack.append(i)
        line_stack.append(line)
    elif ']' == char:
        try:
            start_i = start_stack.pop()
        except IndexError:
            error('syntax error:', 'unmatched "]" on line %d, column %d' % (line, i + 1))
        matches_start[start_i] = i
        matches_end[i] = start_i
    elif '\n' == char:
        line += 1
if start_stack:
    i = start_stack.pop()
    error('syntax error:', 'unmatched "[" on line %d, column %d' % (line_stack.pop(), i + 1))

del start_stack
del line_stack

memory = bytearray([0 for x in range(num_cells)])
cp = 0 # cell/memory pointer
ip = 0 # intruction pointer

try:
    # Start running the program
    while ip < len(program): 
        char = program[ip] 
        if char == '>':
            # Move the pointer to the right
            cp += 1
        elif char == '<':
            # Move the pointer to the left
            cp -= 1
            if cp < 0:
                error("bf error:", "at index %d, pointer moved to negative address on the tape" %ip)
        elif char == '+':
            # Increment the cell at the pointer
            n = memory[cp]
            n = (n + 1) % 256
            memory[cp] = n
        elif char == '-':
            # Decrement the cell at the pointer
            n = memory[cp]
            n = (n - 1) % 256
            memory[cp] = n
        elif char == '.':
            # Output the character at the cell pointer
            c = chr(memory[cp])
            sys.stdout.write(c)
        elif char == ',':
            # Input a character and store it in the cell at the pointer
            c = sys.stdin.read(1) # Note: will be str('') upon EOF in Python
            if c:
                memory[cp] = ord(c)
            elif args.EOF_value is not None: 
                memory[cp] = args.EOF_value
        elif char == '[':
            # Jump past the matching ] if the cell at the pointer is 0
            if memory[cp] == 0: 
                ip = matches_start[ip]
        elif char == ']':
            # Jump back to the matching [ if the cell at the pointer is not 0
            if memory[cp] != 0:
                ip = matches_end[ip]
        elif '#' == char:
            # Debug: print first few cells 
            print('\n[%s...]' % ','.join('%x' % x for x in memory[:num_debug_cells]))
        ip += 1
except Exception as e:
    print('bf: at index %d with pointer at cell %d' % (ip, cp), file=sys.stderr)
    raise e
