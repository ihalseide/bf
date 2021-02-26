#!/usr/bin/env python3 

# BFC interpreter [[https://esolangs.org/wiki/BFC]]

import sys, array, string

# --- Customizable settings --- {

# BF characters that actually do stuff
bf_chars = '[]<>,.+-'

# How many cells to print out in debug
num_debug_cells = 20     

# Number of memory cells
num_cells = 65536 

# Range of values allowed in the memory cells,
# The bf standard is 1 unsigned byte / the range 0-255 ('b')
# Codes are from Python's [array] module:
#   'b' signed char
#   'B' unsigned char
#   'u' wchar_t
#   'h' signed short
#   'H' unsigned short
#   'i' signed int
#   'I' unsigned int 
#   'l' signed long
#   'L' unsigned long 
#   'q' signed long long 
#   'Q' unsigned long long 
cell_type = 'B'
assert cell_type in array.typecodes

# Input End of File settings
EOF_is_overwrite = False 
EOF_value = 0            

# --- End of customizable settings --- }

if len(sys.argv) != 2:
    print('Usage:', print(sys.argv[0], 'filename'))
    sys.exit(-1)

with open(sys.argv[1], 'r') as f:
    program = f.read() 

memory = array.array(cell_type, [0 for x in range(num_cells)])
cp = 0              # cell/memory pointer
ip = 0              # intruction pointer
cycles = 0          # keep track of absolute number of instructions processed

def debug ():
    # TODO
    input('debug...')

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
num = None
while ip < len(program): 
    char = program[ip] 
    if char == '>':
        # Move the pointer to the right
        if num is None:
            num = 1
        cp += num
        num = None
    elif char == '<':
        # Move the pointer to the left
        if num is None:
            num = 1
        cp -= num
        num = None
    elif char == '+':
        # Increment the cell at the pointer
        if num is None:
            num = 1
        n = memory[cp]
        n += num
        memory[cp] = n
        num = None
    elif char == '-':
        # Decrement the cell at the pointer
        if num is None:
            num = 1
        n = memory[cp]
        n -= num
        memory[cp] = n
        num = None
    elif char == '.':
        # Output the character at the cell pointer
        if num is None:
            num = 1 
        for i in range(num):
            c = chr(memory[cp])
            sys.stdout.write(c)
        num = None
    elif char == ',':
        # Input a character and store it in the cell at the pointer
        if num is None:
            num = 1 
        for i in range(num):
            c = sys.stdin.read(1)
            if c:
                memory[cp] = c
            elif EOF_is_overwrite: # `c` will be '' when EOF in Python
                memory[cp] = EOF_value
        num = None
    elif char == '[':
        # Jump past the matching ] if the cell at the pointer is 0
        if num is not None:
            raise SyntaxError('cannot have a quantifer before a "[", index %d' % ip)
        if memory[cp] == 0: 
            ip = matches_start[ip]
    elif char == ']':
        # Jump back to the matching [ if the cell at the pointer is not 0
        if num is not None:
            raise SyntaxError('cannot have a quantifer before a "]", index %d' % ip)
        if memory[cp] != 0:
            ip = matches_end[ip]
    elif '#' == char:
        # Debug breakpoint
        debug()
    elif '!' == char:
        # Stop program (usually used to separate code from input)
        break 
    elif '_' == char:
        # BFC Layer 1, zero operator: set the current cell to zero
        memory[cp] = 0
    elif char in string.digits:
        # BFC Layer 1, quantifiers: do the next non-bracket bf instruction N times
        # (affects the next instruction)
        look_index = ip
        while program[look_index] in string.digits:
            look_index += 1
        num = int(program[ip:look_index])
        ip = look_index - 1
    ip += 1
    cycles += 1
