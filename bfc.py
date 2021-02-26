#!/usr/bin/env python3 

# bf compiler

import argparse
from conf import *

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('-comment', action='store_true', help='whether to generate comments in the C output')
parser.add_argument('-num_cells', default=65535, type=int, help='number of memory cells')
args = parser.parse_args()

comment_p = args.comment
num_cells = args.num_cells
with open(args.file, 'r') as f:
    program = f.read() 

# Emit the C Preamble
print(
'''\
/* brainfuck code converted to C */

#include <stdio.h>

char mem [%d];
char * p; 

int main (int argc, int ** argv) {
    p = &mem;\
''' % num_cells)

indent = 1 
emit = lambda string: print('    ' * indent, string, sep='') 

# Keep track of when brackets start and end
last_lbracket = 0
last_rbracket = 0

try:
    prog = enumerate(iter(program))
    index, char = next(prog)
    while True:
        if comment_p:
            emit('// %s (index %d)' % (char, index))
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
                emit('p += %d;' % num)
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
                emit('*p += %d;' % num)
            del num
            continue
        elif '.' == char:
            # Output the character at the cell pointer
            emit('putchar(*p);')
        elif ',' == char:
            # Input a character and store it in the cell at the pointer
            if EOF_is_overwrite:
                emit('*p = getchar();')
            else:
                raise NotImplemented() 
        elif '[' == char:
            # Jump past the matching ] if the cell at the pointer is 0
            last_lbracket = index
            emit('while (*p) {')
            indent += 1
        elif ']' == char :
            # Jump back to the matching [ if the cell at the pointer is not 0
            last_rbracket = index
            indent -= 1
            emit('}')
        elif '#' == char:
            # Debug breakpoint
            pass
        elif '!' == char:
            # Stop compiling
            break 
        index, char = next(prog)
except StopIteration:
    pass

indent -= 1
emit('}')

if indent > 0:
    raise SyntaxError('unmatched "[" at index %d' % last_rbracket)
elif indent < 0:
    raise SyntaxError('unmatched "]" at index %d' % last_lbracket)

