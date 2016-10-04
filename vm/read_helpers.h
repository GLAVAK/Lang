//
// Created by Glavak on 10/4/2016.
//

#ifndef VM_READ_HELPERS_H
#define VM_READ_HELPERS_H

#include "utils.h"
#include "data_cell.h"

struct data_cell create_empty_string();

struct data_cell read_f_from_program(byte * program, int * out_instruction_pointer);
struct data_cell read_i_from_program(byte * program, int * out_instruction_pointer);
struct data_cell read_s_from_program(byte * program, int * out_instruction_pointer);

#endif //VM_READ_HELPERS_H
