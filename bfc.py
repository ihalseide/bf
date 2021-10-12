#!/usr/bin/env python3 

# bf compiler

import sys, argparse

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
parser.add_argument('-s', dest='small', action='store_true', help='small code formatting for C output')
parser.add_argument('--EOF', dest='EOF_value', type=int, default=None, help='end-of-file value within 0-255 (default is not to write any value)')
args = parser.parse_args()
# Validate EOF value
if args.EOF_value is not None and args.EOF_value not in range(255):
    error('error:', 'agument:', 'the EOF value must be in between 0 and 255')
with open(args.file, 'r') as f:
    program = f.read() 

def squish (s):
    for target in ' \n':
        s = s.replace(target, '')
    return s

indent = 1
def print_line (s):
    global indent
    if args.small:
        print(squish(s), end='')
    else:
        print('    ' * indent, s)

# Emit the C Preamble
if args.small:
    preamble = '#include <stdio.h>\nchar m[%d],*p=&m;int main(int t){'
else:
    preamble = '#include <stdio.h>\nchar m[%d];\nchar *p = &m;\nint main (int t) {\n'
print(preamble % args.num_cells, end='')

last_lbracket = 0
last_rbracket = 0
line = 1 # source line number
line_start = 0 # index of the beginning of the line

try:
    prog = enumerate(iter(program))
    index, char = next(prog)
    while True:
        if char in '<>':
            # Move the pointer to the right or left
            num = 0
            while char in '<>':
                if char == '<':
                    num -= 1
                else:
                    assert char == '>'
                    num += 1
                index, char = next(prog)
            if num:
                neg = num < 0
                num = abs(num)
                if neg:
                    print_line('p -= %d;' % num)
                else:
                    print_line('p += %d;' % num)
            continue
        elif char in '+-':
            # Increment or decrement the cell at the pointer
            num = 0
            while char in '+-':
                if char == '-':
                    num -= 1
                else:
                    assert char == '+'
                    num += 1
                index, char = next(prog)
            if num:
                neg = num < 0
                num = abs(num)
                if neg:
                    print_line('*p -= %d;' % num)
                else:
                    print_line('*p += %d;' % num)
            continue
        elif '.' == char:
            # Output the character at the cell pointer
            print_line('putchar(*p);')
        elif ',' == char:
            # Input a character and store it in the cell at the pointer
            if args.EOF_value is None:
                print_line('t = getchar();')
                print_line('if (t != EOF) {')
                indent += 1
                print_line('*p=t;')
                indent -= 1
                print_line('}')
            else:
                print_line('t = getchar();')
                print_line('if (t == EOF) {')
                indent += 1
                print_line('t = %d;' % args.EOF_value)
                indent -= 1
                print_line('}')
                print_line('*p = t;')
        elif '[' == char:
            # Jump past the matching ] if the cell at the pointer is 0
            last_lbracket = index
            print_line('while (*p) {')
            indent += 1
        elif ']' == char :
            # Jump back to the matching [ if the cell at the pointer is not 0
            last_rbracket = index
            indent -= 1
            print_line('}')
        elif '!' == char:
            # Stop compiling if reading from stdin
            if args.file == '-':
                break 
        elif '\n' == char:
            # Track line numbers
            line += 1
            line_start = index
        index, char = next(prog)
except StopIteration:
    pass

indent -= 1
print_line('}')

if indent > 0:
    raise SyntaxError('unmatched "[" at index %d' % last_rbracket)
elif indent < 0:
    raise SyntaxError('unmatched "]" at index %d' % last_lbracket)

