//
// Created by Glavak on 9/29/2016.
//

#include <stdio.h>

#include "utils.h"

unsigned char * read_file(char * filename, size_t * out_size)
{
    FILE * file;
    fopen_s(&file, filename, "rb");

    const int read_by = 1024;
    unsigned char * result = malloc(sizeof(unsigned char) * (read_by + 1));
    size_t position = 0;

    size_t read = fread(result, 1, read_by, file);
    while (read > 0)
    {
        position += read;
        result = realloc(result, position + read_by + 1);
        read = fread(result + position, 1, read_by, file);
    }

    fclose(file);

    *out_size = position;
    result[position] = '\0';
    return result;
}
