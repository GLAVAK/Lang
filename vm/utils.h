//
// Created by Glavak on 9/29/2016.
//

#ifndef VM_UTILS_H
#define VM_UTILS_H

#include <stdlib.h>
#include <stdio.h>

typedef unsigned char byte;

struct vm_settings
{
    unsigned char * program_filename;

    // Function, which will be called by vm when it want to print something to console
    void (*print)(unsigned char *);

    // Function, which will be called by vm when it want to read something from console
    char * (*read)();
};

// Reads file to the end, returns null-terminated string
unsigned char * read_file(char * filename, size_t * out_size);

#endif //VM_UTILS_H
