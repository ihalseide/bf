#!/usr/bin/env python3

'''
This is a brainf*ck interpreter. It runs text files
'''

import sys 

# Customizable settings
EOF_is_overwrite = False # Determines whether an EOF when getting input will overwrite the cell with an EOF value
EOF_value = 0            # Choose an End of File value
num_debug_cells = 200     # How many cells to print out in debug

if len(sys.argv) != 2:
    print('Usage:')
    print(sys.argv[0], '[filename]')
    sys.exit(-1)

filename = sys.argv[1]
# Take program from given file
# With program input from standard input
with open(filename, 'r') as f:
    program = f.read()

# Main program components
input_buffer = iter('')
memory = bytearray([0 for x in range(65536)]) 
pointer = 0         # memory pointer
program_counter = 0 # index into the program string
cycles = 0          # absolute number of instructions processed
matches_start = {}  # maps [ to ]
matches_end = {}    # maps ] to [

# Preprocess the [ bracket ] matches to increase speed
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
            raise SyntaxError('unmatched "["')
    elif ']' == char:
        if matches_end.get(index) is None:
            raise SyntaxError('unmatched "]"')

# Start running the program
while program_counter < len(program) and program[program_counter] != '!':

    char = program[program_counter]

    if char == '>':
        # Move the pointer to the right
        pointer += 1
        if pointer >= len(memory):
            # Double memory space if it runs out
            memory += bytearray([0 for x in memory])
    elif char == '<':
        # Move the pointer to the left
        pointer -= 1
    elif char == '+':
        # Increment the memory cell at the pointer
        n = memory[pointer]
        n = (n + 1) % 256
        memory[pointer] = n
    elif char == '-':
        # Decrement the memory cell at the pointer
        n = memory[pointer]
        n = (n - 1) % 256
        memory[pointer] = n
    elif char == '.':
        # Output the character signified by the cell at the pointer
        print(end=chr(memory[pointer]))
    elif char == ',':
        # Input a character and store it in the cell at the pointer
        c = None
        try:
            if input_buffer is not None:
                c = next(input_buffer)
        except StopIteration:
            input_buffer = iter(input())
            c = next(input_buffer)
        except EOFError:
            input_buffer = None
        if input_buffer is not None:
            memory[pointer] = int(ord(c))
        elif EOF_is_overwrite:
            memory[pointer] = EOF_value
    elif char == '[':
        # Jump past the matching ] if the cell at the pointer is 0
        if memory[pointer] == 0: 
            program_counter = matches_start[program_counter]
    elif char == ']':
        # Jump back to the matching [ if the cell at the pointer is not 0
        if memory[pointer] != 0:
            program_counter = matches_end[program_counter]
    elif '#' == char:
        # Debug: print first few cells 
        print('\n#[%s...]' % ','.join('%x' % x for x in memory[:num_debug_cells]))
        cycles -= 1
    elif '^' == char:
        # Debug: print pointer location
        print('\n^%d' % pointer)
        cycles -= 1
    elif '@' == char:
        # Debug: print cycle number
        print('\n@%d' % cycles)
        cycles -= 1

    program_counter += 1
    cycles += 1
