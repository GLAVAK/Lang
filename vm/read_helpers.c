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

struct data_cell read_f_from_program(byte * program, int * out_instruction_pointer)
{
    struct data_cell result;
    int ip = *out_instruction_pointer;

    // FIXME: Platform dependent as hell
    // FIXME: Fucks up program array
    assert(sizeof(double) == 8);
    for (int i = 0; i < 4; ++i)
    {
        byte buffer = program[ip + i];
        program[ip + i] = program[ip + 7 - i];
        program[ip + 7 - i] = buffer;
    }

    memcpy(&result.data.f, program + ip, sizeof(double));

    (*out_instruction_pointer) += sizeof(double);
    return result;
}

struct data_cell read_i_from_program(byte * program, int * out_instruction_pointer)
{
    struct data_cell result;
    int ip = *out_instruction_pointer;
    result.data.i = 0;

    result.data.i |= program[ip];
    result.data.i <<= sizeof(unsigned char)*8;
    result.data.i |= program[ip + 1];
    result.data.i <<= sizeof(unsigned char)*8;
    result.data.i |= program[ip + 2];
    result.data.i <<= sizeof(unsigned char)*8;
    result.data.i |= program[ip + 3];

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

    (*out_instruction_pointer) += position+1;
    return result;
}