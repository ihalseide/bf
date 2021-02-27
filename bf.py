#!/usr/bin/env python3 

# bf interpretter

import sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-num_cells', default=65535, type=int, help='number of memory cells')
parser.add_argument('-file', help='the bf program input file, default is to read stdin')
parser.add_argument('-debug', action='store_true')
parser.add_argument('--EOF_value', type=int, default=None, help='End Of File value, default is not to write any value upon EOF')
args = parser.parse_args()

if args.EOF_value is not None and args.EOF_value not in range(255):
    raise ValueError('EOF_value must be in range(0, 255)')

num_cells = args.num_cells
if args.file is None:
    # Read program from stdin until a '!'
    program = ''
    while (c := sys.stdin.read(1)) not in ('', '!'):
        program += c
else:
    # Read program from file
    with open(args.file, 'r') as f:
        program = f.read() 

def error (*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)
    sys.exit(-1)

# Preprocess the brackets matches to increase efficiency a little
matches_start = {}  # maps '[' to ']'
matches_end = {}    # maps ']' to '['
for i, char in enumerate(program):
    if '[' == char:
        # Search for the matching ']'
        depth = 0
        match = None
        for i2, char2 in enumerate(program[i:]):
            if '[' == char2:
                depth += 1
            elif ']' == char2:
                depth -= 1
                if depth == 0:
                    match = i + i2
                    break
        if match is None:
            error('syntax error:', 'unmatched "[" at index %d' % i)
        matches_start[i] = match
        matches_end[match] = i 
    elif ']' == char:
        # Make sure there was a matching '['
        if matches_end.get(i) is None:
            error('syntax error:', 'unmatched "]" at index %d' % i)

memory = bytearray([0 for x in range(num_cells)])
cp = 0              # cell/memory pointer
ip = 0              # intruction pointer

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
    print('bf: at index %d with pointer at cell %d' % (ip, cp))
    raise e
