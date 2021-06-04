#!/usr/bin/env python3 

# bf interpretter

import sys, argparse

DEBUG_RANGE = 5 # number of debug cells to show around the pointer

def error (fatal=True, *args, **kwargs):
    print(sys.argv[0]+':', *args, **kwargs, file=sys.stderr)
    if fatal:
        sys.exit(-1)

def spaces (n):
    return ' ' * int(n)

parser = argparse.ArgumentParser()
parser.add_argument('file', help='the bf program, a "-" signifies to read from stdin')
parser.add_argument('-n', dest='num_cells', default=65535, type=int, help='number of cells on the tape (default is 65535)')
parser.add_argument('-d', dest='debug', action='store_true', help='debug flag')
parser.add_argument('--EOF_value', type=int, default=None, help='end-of-file value in the range 0-255 (default is not to write any value)')
args = parser.parse_args()

if args.EOF_value is not None and args.EOF_value not in range(255):
    error('error:', 'agument:', 'EOF_value must be in range(0, 255)')

if args.file == '-':
    # Read program from STDIN until a '!'
    program = ''
    while (c := sys.stdin.read(1)) not in ('', '!'):
        program += c
else:
    # Read program from FILE
    with open(args.file, 'r') as f:
        program = f.read() 

# Preprocess the brackets matches
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
            line_stack.pop()
        except IndexError:
            error('syntax error:', 'unmatched "]" on line %d, column %d' % (line, i + 1))
        matches_start[start_i] = i
        matches_end[i] = start_i
    elif '\n' == char:
        line += 1
if start_stack:
    i = start_stack.pop()
    error('syntax error:', 'unmatched "[" on line %d, column %d' % (line_stack.pop(), i + 1))

# these are explicitly temporary
del start_stack
del line_stack

# run the bf program
memory = bytearray([0 for x in range(args.num_cells)])
cp = 0 # cell/memory tape pointer
ip = 0 # intruction pointer
try:
    # Start running the program
    while ip < len(program): 
        char = program[ip] 
        if '>' == char:
            # Move the cell pointer to the right
            cp += 1
        elif '<' == char:
            # Move the cell pointer to the left
            cp -= 1
            if cp < 0:
                error("bf error:", "at index %d, the pointer moved to a negative address off of the memory tape" %(ip+1))
        elif '+' == char:
            # Increment the cell at the pointer
            n = memory[cp]
            n = (n + 1) % 256
            memory[cp] = n
        elif '-' == char:
            # Decrement the cell at the pointer
            n = memory[cp]
            n = (n - 1) % 256
            memory[cp] = n
        elif '.' == char:
            # Output the character at the cell pointer
            c = chr(memory[cp])
            sys.stdout.write(c)
        elif ',' == char:
            # Input a character and store it in the cell at the pointer
            c = sys.stdin.read(1) # Note: will be str('') upon EOF in Python
            if c:
                memory[cp] = ord(c)
            elif args.EOF_value is not None: 
                memory[cp] = args.EOF_value
        elif '[' == char:
            # Jump past the matching ] if the cell at the pointer is 0
            if memory[cp] == 0: 
                ip = matches_start[ip]
        elif ']' == char:
            # Jump back to the matching [ if the cell at the pointer is not 0
            if memory[cp] != 0:
                ip = matches_end[ip]
        elif '#' == char and args.debug:
            # Debug: print a few cells around the cell pointer
            before = max(0, cp - DEBUG_RANGE)
            after = min(len(memory) - 1, cp + DEBUG_RANGE)
            f = lambda x: '({:3d})'.format(memory[x]) if (x == cp) else '{:3d}'.format(memory[x])
            s = ', '.join(f(x) for x in range(before, after + 1)) 
            print('cp:{:3d}, ip:{:3d}, tape:'.format(cp, ip), '['+s+']')
        ip += 1
except Exception as e:
    error('bf error:', 'at index %d with pointer at cell %d' % (ip, cp), fatal=False)
    raise e
