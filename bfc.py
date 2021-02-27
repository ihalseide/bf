#!/usr/bin/env python3 

# bf compiler

import sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('-debug', action='store_true', help='whether to generate comments in the C output')
parser.add_argument('-num_cells', default=65535, type=int, help='number of memory cells')
args = parser.parse_args()

with open(args.file, 'r') as f:
    program = f.read() 

indent = 1
def print_line (*args, **kwargs):
    print('    ' * indent, *args, sep='', end='\n', *kwargs)

# Emit the C Preamble
print(
'''\
/* brainfuck code
 * from the file "%s"
 * compiled with "%s"
 */

#include <stdio.h>

char mem [%d];
char * p; 

int main (int argc, int ** argv) {
    p = &mem;\
''' % (args.file, parser.prog, args.num_cells))


# Keep track of when brackets start and end
last_lbracket = 0
last_rbracket = 0

try:
    prog = enumerate(iter(program))
    index, char = next(prog)
    while True:
        if args.debug:
            print_line('// %s (index %d)' % (char, index))
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
            if num != 0:
                print_line('p += %d;' % num)
            del num
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
            if num != 0:
                print_line('*p += %d;' % num)
            del num
            continue
        elif '.' == char:
            # Output the character at the cell pointer
            print_line('putchar(*p);')
        elif ',' == char:
            # Input a character and store it in the cell at the pointer
            if EOF_is_overwrite:
                print_line('*p = getchar();')
            else:
                raise NotImplemented() 
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
        elif '#' == char:
            # Debug breakpoint
            pass
        elif '!' == char:
            # Stop compiling
            break 
        else:
            # Unknown char, so skip
            pass
        index, char = next(prog)
except StopIteration:
    pass

indent -= 1
print_line('}')

if indent > 0:
    raise SyntaxError('unmatched "[" at index %d' % last_rbracket)
elif indent < 0:
    raise SyntaxError('unmatched "]" at index %d' % last_lbracket)

