#!/usr/bin/env python3 

# bf compiler

import sys
import conf

if len(sys.argv) != 2:
    print('Usage:', print(sys.argv[0], 'filename'))
    sys.exit(-1)

with open(sys.argv[1], 'r') as f:
    program = f.read() 

matches_start = {}  # maps '[' to ']'
matches_end = {}    # maps ']' to '[' 
bracket_depth = 0

for index, char in program: 
    char = program[ip] 
    if char == '>':
        # Move the pointer to the right
        pass
    elif char == '<':
        # Move the pointer to the left
        pass
    elif char == '+':
        # Increment the cell at the pointer
        pass
    elif char == '-':
        # Decrement the cell at the pointer
        pass
    elif char == '.':
        # Output the character at the cell pointer
        pass
    elif char == ',':
        # Input a character and store it in the cell at the pointer
        pass
    elif char == '[':
        # Jump past the matching ] if the cell at the pointer is 0
        bracket_depth = 1
        match = None
        for i in range(index + 1, len(program)):
            char2 = program[i]
            if '[' == char2:
                bracket_depth += 1
            elif ']' == char2:
                bracket_depth -= 1
                if bracket_depth == 0:
                    match = i
                    break
        if match is not None:
            matches_start[index] = match
            matches_end[match] = index
        else:
            raise SyntaxError('unmatched "[" at index %d' % index)
    elif char == ']':
        # Jump back to the matching [ if the cell at the pointer is not 0
        if matches_end.get(index) is None:
            raise SyntaxError('unmatched "]" at index %d' % index)
    elif '#' == char:
        # Debug breakpoint
        pass
    elif '!' == char:
        # Stop program (usually used to separate code from input)
        break 
