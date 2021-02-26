#!/usr/bin/env python3 

# bf interpretter

import sys
from conf import *

if len(sys.argv) != 2:
    print('Usage:', print(sys.argv[0], 'filename'))
    sys.exit(-1)

with open(sys.argv[1], 'r') as f:
    program = f.read() 

memory = bytearray([0 for x in range(num_cells)])
cp = 0              # cell/memory pointer
ip = 0              # intruction pointer
cycles = 0          # keep track of absolute number of instructions processed

# Preprocess the brackets matches to increase efficiency a little
matches_start = {}  # maps '[' to ']'
matches_end = {}    # maps ']' to '['
for index, char in enumerate(program):
    if '[' == char:
        depth = 1
        match = None
        for i in range(index + 1, len(program)):
            char2 = program[i]
            if '[' == char2:
                depth += 1
            elif ']' == char2:
                depth -= 1
                if depth == 0:
                    match = i
                    break
        if match is not None:
            matches_start[index] = match
            matches_end[match] = index
        else:
            raise SyntaxError('unmatched "[" at index %d' % index)
    elif ']' == char:
        if matches_end.get(index) is None:
            raise SyntaxError('unmatched "]" at index %d' % index)

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
        c = sys.stdin.read(1)
        if c:
            memory[cp] = c
        elif EOF_is_overwrite: # `c` will be '' when EOF in Python
            memory[cp] = EOF_value
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
    elif '!' == char:
        # Extension: separate code from input
        # Since this is an interpreter, just take it to mean "halt"
        break 
    ip += 1
