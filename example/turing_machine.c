/* brainfuck code converted to C */

#include <stdio.h>

char mem [65536];
char * p; 

int main (int argc, int ** argv) {
    p = &mem;
    *p += 3;
    p += 1;
    *p += 2;
    p += 3;
    *p += 1;
    while (*p) {
        p += 2;
        *p = getchar();
        while (*p) {
            p += 1;
            *p += 5;
            p += -1;
            while (*p) {
                while (*p) {
                    *p += -1;
                    p += 1;
                }
                p += -2;
            }
            p += -1;
            while (*p) {
                p += 1;
            }
            p += 1;
        }
        p += 1;
        *p += -1;
        while (*p) {
            p += -2;
            *p += 5;
            p += 2;
            *p += -1;
            while (*p) {
                p += -2;
                *p += -4;
                p += 2;
                *p += -1;
                while (*p) {
                    *p += -1;
                    p += 1;
                }
                p += -1;
            }
        }
        p += -1;
        while (*p) {
            p += -1;
            *p += -1;
            p += -1;
            while (*p) {
                p += -1;
            }
            *p += 1;
            p += -1;
            *p += 1;
            while (*p) {
                p += 1;
            }
            p += -2;
            *p += 1;
            p += 1;
            *p += -1;
            p += 3;
        }
        p += -1;
    }
    p += -1;
    while (*p) {
        p += -1;
    }
    p += 1;
    while (*p) {
        *p += -1;
        while (*p) {
            p += 1;
            *p += 6;
            p += -1;
            *p += -1;
        }
        p += 1;
        while (*p) {
            p += -1;
            *p += 1;
            p += 1;
            *p += -1;
        }
        *p += 1;
        p += -3;
        *p += 3;
        p += 1;
        *p += 1;
        p += 1;
        while (*p) {
            *p += -1;
            while (*p) {
                p += -2;
                *p += 1;
                p += 1;
                *p += -1;
                p += 1;
                *p += -1;
                while (*p) {
                    p += -2;
                    while (*p) {
                        *p += -1;
                    }
                    p += 2;
                    *p += -1;
                    while (*p) {
                        p += -2;
                        *p += 2;
                        p += 1;
                        *p += 1;
                        p += 1;
                        *p += -1;
                        while (*p) {
                            p += -2;
                            *p += -2;
                            p += 1;
                            *p += -1;
                            p += 2;
                            *p += 3;
                            p += -1;
                            *p += -1;
                            while (*p) {
                                p += -2;
                                *p += 1;
                                p += 1;
                                *p += 1;
                                p += 2;
                                *p += -2;
                                p += -1;
                                *p += -1;
                                while (*p) {
                                    p += -2;
                                    *p += -1;
                                    p += 1;
                                    *p += -1;
                                    p += 1;
                                    *p += -1;
                                    while (*p) {
                                        p += -2;
                                        *p += 4;
                                        p += 1;
                                        *p += 1;
                                        p += 2;
                                        *p += 1;
                                        p += -1;
                                        *p += -1;
                                        while (*p) {
                                            p += 1;
                                            *p += -1;
                                            p += -1;
                                            *p += -1;
                                            while (*p) {
                                                p += -2;
                                                *p += -1;
                                                p += 1;
                                                *p += -1;
                                                p += 1;
                                                *p += -1;
                                                while (*p) {
                                                    p += -2;
                                                    *p += -1;
                                                    p += 2;
                                                    *p += -1;
                                                    while (*p) {
                                                        p += -2;
                                                        *p += 3;
                                                        p += 3;
                                                        *p += -1;
                                                        p += -1;
                                                        *p += -1;
                                                        while (*p) {
                                                            p += -2;
                                                            *p += -4;
                                                            p += 3;
                                                            *p += 2;
                                                            p += -1;
                                                            *p += -1;
                                                            while (*p) {
                                                                p += -2;
                                                                *p += 2;
                                                                p += 3;
                                                                *p += 1;
                                                                p += -1;
                                                                *p += -1;
                                                                while (*p) {
                                                                    p += 1;
                                                                    while (*p) {
                                                                        *p += -1;
                                                                    }
                                                                    p += -1;
                                                                    *p += -1;
                                                                    while (*p) {
                                                                        p += -2;
                                                                        *p += -1;
                                                                        p += 3;
                                                                        *p += 3;
                                                                        p += -1;
                                                                        *p += -1;
                                                                        while (*p) {
                                                                            p += -2;
                                                                            *p += -1;
                                                                            p += 3;
                                                                            *p += -2;
                                                                            p += -1;
                                                                            *p += -1;
                                                                            while (*p) {
                                                                                p += -2;
                                                                                *p += 4;
                                                                                p += 1;
                                                                                *p += 1;
                                                                                p += 2;
                                                                                *p += 1;
                                                                                p += -1;
                                                                                *p += -1;
                                                                                while (*p) {
                                                                                    p += -2;
                                                                                    while (*p) {
                                                                                        *p += -1;
                                                                                    }
                                                                                    p += 1;
                                                                                    *p += -1;
                                                                                    p += 2;
                                                                                    *p += 2;
                                                                                    p += -1;
                                                                                    *p += -1;
                                                                                    while (*p) {
                                                                                        p += -2;
                                                                                        *p += 5;
                                                                                        p += 1;
                                                                                        *p += 1;
                                                                                        p += 2;
                                                                                        *p += -2;
                                                                                        p += -1;
                                                                                        *p += -1;
                                                                                        while (*p) {
                                                                                            p += -1;
                                                                                            *p += -1;
                                                                                            p += 2;
                                                                                            *p += 2;
                                                                                            p += -1;
                                                                                            while (*p) {
                                                                                                p += -2;
                                                                                                *p += -1;
                                                                                                p += 2;
                                                                                                *p += -1;
                                                                                            }
                                                                                        }
                                                                                    }
                                                                                }
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        p += -1;
        while (*p) {
            *p += -1;
            p += 2;
            while (*p) {
                p += -2;
                *p += 1;
                p += 2;
                *p += -1;
            }
            p += -3;
            while (*p) {
                p += 3;
                *p += 1;
                p += -3;
                *p += -1;
            }
            p += -1;
            while (*p) {
                p += 3;
                *p += 1;
                p += -3;
                *p += -1;
            }
        }
        p += 2;
    }
    p += 1;
    while (*p) {
        *p += -1;
        while (*p) {
            *p += -3;
            while (*p) {
                *p += -1;
                p += -1;
            }
        }
        p += 1;
    }
    p += 1;
    while (*p) {
        *p += 3;
        while (*p) {
            p += -1;
            *p += 5;
            p += 1;
            *p += -2;
        }
        p += 1;
    }
    *p += 1;
    p += -1;
    *p += 2;
    while (*p) {
        while (*p) {
            p += 1;
            *p += 5;
            p += -1;
            *p += -1;
        }
        p += -1;
    }
    p += 2;
    while (*p) {
        *p += -1;
        putchar(*p);
        p += 1;
    }
}
