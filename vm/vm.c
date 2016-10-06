// Uncomment to make it faster, in theory, but UB if error in user's program:
//#define NODEBUG

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <mem.h>

#include "vm.h"
#include "opcode.h"
#include "data_cell.h"

#include "utils.h"
#include "read_helpers.h"

const int stackMaxSize = 128;
const int memoryMaxSize = 256;

int start_vm(struct vm_settings settings)
{
    size_t program_size;
    byte * program = read_file((char *) settings.program_filename, &program_size);
    int instruction_pointer = 0;

    struct data_cell stack[stackMaxSize];
    size_t stackSize = 0;

    struct data_cell memory[memoryMaxSize];

    char * str_for_print = malloc(sizeof(char) * 20);
    str_for_print[0] = '\0';

    while (1)
    {
        // This switch may needs optimization, maybe analyze assembler output or
        // run some benchmarks to find the best way to do it
        switch ((enum opcode) program[instruction_pointer++])
        {
            case OPCODE_PUSH_VAL_I:
                assert(stackSize < stackMaxSize);
                stack[stackSize++] = read_i_from_program(program, &instruction_pointer);
                break;
            case OPCODE_PUSH_VAL_F:
                assert(stackSize < stackMaxSize);
                stack[stackSize++] = read_f_from_program(program, &instruction_pointer);
                break;
            case OPCODE_PUSH_VAL_S:
                assert(stackSize < stackMaxSize);
                stack[stackSize++] = read_s_from_program(program, &instruction_pointer);
                break;

            case OPCODE_PUSH_MEM:
                assert(stackSize < stackMaxSize);
                stack[stackSize++] = memory[program[instruction_pointer++]];
                break;
            case OPCODE_POP_MEM:
                assert(stackSize >= 1);
                memory[program[instruction_pointer++]] = stack[--stackSize];
                break;
            case OPCODE_SEEK_MEM:
                assert(stackSize >= 1);
                memory[program[instruction_pointer++]] = stack[stackSize - 1];
                break;

            case OPCODE_ADD_I:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.i = stack[stackSize - 2].data.i + stack[stackSize - 1].data.i;
                stackSize--;
                break;
            case OPCODE_SUB_I:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.i = stack[stackSize - 2].data.i - stack[stackSize - 1].data.i;
                stackSize--;
                break;
            case OPCODE_MUL_I:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.i = stack[stackSize - 2].data.i * stack[stackSize - 1].data.i;
                stackSize--;
                break;
            case OPCODE_DIV_I:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.i = stack[stackSize - 2].data.i / stack[stackSize - 1].data.i;
                stackSize--;
                break;
            case OPCODE_INVERT_I:
                assert(stackSize >= 1);
                stack[stackSize - 1].data.i = -stack[stackSize - 1].data.i;
                break;

            case OPCODE_EQUALS_I:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.b = stack[stackSize - 2].data.i == stack[stackSize - 1].data.i;
                stackSize--;
                break;
            case OPCODE_NOT_EQUALS_I:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.b = stack[stackSize - 2].data.i != stack[stackSize - 1].data.i;
                stackSize--;
                break;
            case OPCODE_GREATER_I:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.b = stack[stackSize - 2].data.i > stack[stackSize - 1].data.i;
                stackSize--;
                break;
            case OPCODE_LESS_I:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.b = stack[stackSize - 2].data.i < stack[stackSize - 1].data.i;
                stackSize--;
                break;
            case OPCODE_GREATER_EQUAL_I:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.b = stack[stackSize - 2].data.i >= stack[stackSize - 1].data.i;
                stackSize--;
                break;
            case OPCODE_LESS_EQUAL_I:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.b = stack[stackSize - 2].data.i <= stack[stackSize - 1].data.i;
                stackSize--;
                break;

            case OPCODE_ADD_F:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.f = stack[stackSize - 2].data.f + stack[stackSize - 1].data.f;
                stackSize--;
                break;
            case OPCODE_SUB_F:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.f = stack[stackSize - 2].data.f - stack[stackSize - 1].data.f;
                stackSize--;
                break;
            case OPCODE_MUL_F:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.f = stack[stackSize - 2].data.f * stack[stackSize - 1].data.f;
                stackSize--;
                break;
            case OPCODE_DIV_F:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.f = stack[stackSize - 2].data.f / stack[stackSize - 1].data.f;
                stackSize--;
                break;
            case OPCODE_INVERT_F:
                assert(stackSize >= 1);
                stack[stackSize - 1].data.f = -stack[stackSize - 1].data.f;
                break;

            case OPCODE_EQUALS_F:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.b = stack[stackSize - 2].data.f == stack[stackSize - 1].data.f;
                stackSize--;
                break;
            case OPCODE_NOT_EQUALS_F:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.b = stack[stackSize - 2].data.f != stack[stackSize - 1].data.f;
                stackSize--;
                break;
            case OPCODE_GREATER_F:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.b = stack[stackSize - 2].data.f > stack[stackSize - 1].data.f;
                stackSize--;
                break;
            case OPCODE_LESS_F:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.b = stack[stackSize - 2].data.f < stack[stackSize - 1].data.f;
                stackSize--;
                break;
            case OPCODE_GREATER_EQUAL_F:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.b = stack[stackSize - 2].data.f >= stack[stackSize - 1].data.f;
                stackSize--;
                break;
            case OPCODE_LESS_EQUAL_F:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.b = stack[stackSize - 2].data.f <= stack[stackSize - 1].data.f;
                stackSize--;
                break;

            case OPCODE_CONCAT_S:
                assert(stackSize >= 2);

                // Save first operand from stack:
                char * first_operand = stack[stackSize - 2].data.s;

                // Create new string, copy first_operand there and append second operand from stack:
                stack[stackSize - 2] = create_empty_string();
                strcpy(stack[stackSize - 2].data.s, first_operand);
                strcat(stack[stackSize - 2].data.s, stack[stackSize - 1].data.s);

                stackSize--;
                break;

            case OPCODE_REPEAT_S:
                assert(stackSize >= 2);

                // Save first operand from stack:
                char * str = stack[stackSize - 2].data.s;
                int count = stack[stackSize - 1].data.i;

                // Create new string, copy first_operand there and append second operand from stack:
                stack[stackSize - 2] = create_empty_string();
                stack[stackSize - 2].data.s[0] = '\0';
                for (int j = 0; j < count; ++j)
                {
                    strcat(stack[stackSize - 2].data.s, str);
                }

                stackSize--;
                break;

            case OPCODE_EQUALS_S:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.b = strcmp(stack[stackSize - 2].data.s, stack[stackSize - 1].data.s) == 0;
                stackSize--;
                break;
            case OPCODE_NOT_EQUALS_S:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.b = strcmp(stack[stackSize - 2].data.s, stack[stackSize - 1].data.s) != 0;
                stackSize--;
                break;
            case OPCODE_GREATER_S:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.b = strcmp(stack[stackSize - 2].data.s, stack[stackSize - 1].data.s) > 0;
                stackSize--;
                break;
            case OPCODE_LESS_S:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.b = strcmp(stack[stackSize - 2].data.s, stack[stackSize - 1].data.s) < 0;
                stackSize--;
                break;
            case OPCODE_GREATER_EQUAL_S:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.b = strcmp(stack[stackSize - 2].data.s, stack[stackSize - 1].data.s) >= 0;
                stackSize--;
                break;
            case OPCODE_LESS_EQUAL_S:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.b = strcmp(stack[stackSize - 2].data.s, stack[stackSize - 1].data.s) <= 0;
                stackSize--;
                break;

            case OPCODE_NOT:
                assert(stackSize >= 1);
                stack[stackSize - 1].data.b = !stack[stackSize - 1].data.b;
                break;
            case OPCODE_AND:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.b = stack[stackSize - 2].data.b && stack[stackSize - 1].data.b;
                stackSize--;
                break;
            case OPCODE_OR:
                assert(stackSize >= 2);
                stack[stackSize - 2].data.b = stack[stackSize - 2].data.b || stack[stackSize - 1].data.b;
                stackSize--;
                break;

            case OPCODE_ITOF:
                assert(stackSize >= 1);
                stack[stackSize - 1].data.f = (float) stack[stackSize - 1].data.i;
                break;
            case OPCODE_FTOI:
                assert(stackSize >= 1);
                stack[stackSize - 1].data.i = (int) stack[stackSize - 1].data.f;
                break;

            case OPCODE_ITOS:
                assert(stackSize >= 1);
                int i = stack[stackSize - 1].data.i;
                stack[stackSize - 1] = create_empty_string();
                itoa(i, stack[stackSize - 1].data.s, 10);
                break;
            case OPCODE_STOI:
                assert(stackSize >= 1);
                stack[stackSize - 1].data.i = atoi(stack[stackSize - 1].data.s);
                break;

            case OPCODE_FTOS:
                assert(stackSize >= 1);
                double f = stack[stackSize - 1].data.f;
                stack[stackSize - 1] = create_empty_string();
                sprintf(stack[stackSize - 1].data.s, "%lf", f);
                break;
            case OPCODE_STOF:
                assert(stackSize >= 1);
                stack[stackSize - 1].data.f = atof(stack[stackSize - 1].data.s);
                break;

            case OPCODE_IF:
                assert(stackSize >= 2);
                if (stack[stackSize - 2].data.b)
                {
                    instruction_pointer = stack[stackSize - 1].data.i;
                }
                stackSize -= 2;
                break;
            case OPCODE_GOTO:
                assert(stackSize >= 1);
                instruction_pointer = stack[stackSize - 1].data.i;
                stackSize--;
                break;

            case OPCODE_EXIT:
                free(program);
                free(str_for_print);
                return 0;
            case OPCODE_READ:
                assert(stackSize < stackMaxSize);
                stack[stackSize++].data.s = settings.read();
                break;
            case OPCODE_WRITE_I:
                assert(stackSize >= 1);
                sprintf(str_for_print, "i:%d\n", stack[stackSize - 1].data.i);
                settings.print((unsigned char *) str_for_print);
                break;
            case OPCODE_WRITE_F:
                assert(stackSize >= 1);
                sprintf(str_for_print, "f:%lf\n", stack[stackSize - 1].data.f);
                settings.print((unsigned char *) str_for_print);
                break;
            case OPCODE_WRITE_B:
                assert(stackSize >= 1);
                if (stack[stackSize - 1].data.b)
                {
                    settings.print((unsigned char *) "b:true\n");
                }
                else
                {
                    settings.print((unsigned char *) "b:false\n");
                }
                break;
            case OPCODE_WRITE_S:
                assert(stackSize >= 1);
                sprintf(str_for_print, "s:%s\n", stack[stackSize - 1].data.s);
                settings.print((unsigned char *) str_for_print);
                break;

            default:
                printf("Unknown opcode %X at position %d", program[instruction_pointer - 1], instruction_pointer - 1);
                free(program);
                free(str_for_print);
                return 0;
        }
    }

}