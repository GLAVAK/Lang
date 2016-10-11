//
// Created by Glavak on 10/4/2016.
//

#include <assert.h>
#include <mem.h>

#include "read_helpers.h"

struct data_cell create_empty_string()
{
    struct data_cell result;
    result.data.s = malloc(sizeof(char) * 256);

    //FIXME: memory leak
    //TODO: some kind of garbage collection

    return result;
}

int is_little_endian()
{
    int num = 1;

    return *(char *) &num == 1;
}

struct data_cell read_f_from_program(byte * program, int * out_instruction_pointer)
{
    struct data_cell result;
    int ip = *out_instruction_pointer;

    // TODO: Platform dependent as hell, fix it
    assert(sizeof(double) == 8);
    if (is_little_endian())
    {
        // Copy data inverting bytes
        union
        {
            double d;
            char c[8];
        } data;

        for (int i = sizeof(double) - 1; i >= 0; --i)
        {
            data.c[sizeof(double) - 1 - i] = program[ip + i];
        }

        result.data.f = data.d;
    }
    else
    {
        // Just copy data
        memcpy(&result.data.f, program + ip, sizeof(double));
    }

    (*out_instruction_pointer) += 8;
    return result;
}

struct data_cell read_i_from_program(byte * program, int * out_instruction_pointer)
{
    struct data_cell result;
    int ip = *out_instruction_pointer;

    if (is_little_endian())
    {
        // Copy data inverting bytes
        result.data.i = (int) program[ip + 3] |
                        (int) program[ip + 2] << 8 |
                        (int) program[ip + 1] << 16 |
                        (int) program[ip] << 24;
    }
    else
    {
        // Just copy data
        result.data.i = (int) program[ip] |
                        (int) program[ip + 1] << 8 |
                        (int) program[ip + 2] << 16 |
                        (int) program[ip + 3] << 24;
    }

    (*out_instruction_pointer) += 4;
    return result;
}

struct data_cell read_s_from_program(byte * program, int * out_instruction_pointer)
{
    struct data_cell result = create_empty_string();
    int ip = *out_instruction_pointer;
    int position = 0;

    while (program[ip + position] != '\0')
    {
        result.data.s[position] = program[ip + position];
        position++;
    }
    result.data.s[position] = '\0';

    (*out_instruction_pointer) += position + 1;
    return result;
}