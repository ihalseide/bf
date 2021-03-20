/* brainfuck code
 * from the file "bf examples/hello world.txt"
 * compiled with "bfc.py"
 */

#include <stdio.h>

char mem [65535];
char * p; 

int main (int argc, int ** argv) {
    p = &mem;
    *p += 8;
    while (*p) {
        p += 1;
        *p += 4;
        while (*p) {
            p += 1;
            *p += 2;
            p += 1;
            *p += 3;
            p += 1;
            *p += 3;
            p += 1;
            *p += 1;
            p += -4;
            *p += -1;
        }
        p += 1;
        *p += 1;
        p += 1;
        *p += 1;
        p += 1;
        *p += -1;
        p += 2;
        *p += 1;
        while (*p) {
            p += -1;
        }
        p += -1;
        *p += -1;
    }
    p += 2;
    putchar(*p);
    p += 1;
    *p += -3;
    putchar(*p);
    *p += 7;
    putchar(*p);
    putchar(*p);
    *p += 3;
    putchar(*p);
    p += 2;
    putchar(*p);
    p += -1;
    *p += -1;
    putchar(*p);
    p += -1;
    putchar(*p);
    *p += 3;
    putchar(*p);
    *p += -6;
    putchar(*p);
    *p += -8;
    putchar(*p);
    p += 2;
    *p += 1;
    putchar(*p);
    p += 1;
    *p += 2;
    putchar(*p);
}
