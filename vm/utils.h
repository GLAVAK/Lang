//
// Created by Glavak on 9/29/2016.
//

#ifndef VM_UTILS_H
#define VM_UTILS_H

#include <stdlib.h>
#include <stdio.h>

// Reads file to the end, returns null-terminated string
unsigned char * read_file(char * filename, size_t * out_size);

#endif //VM_UTILS_H
