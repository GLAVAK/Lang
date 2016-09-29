// Uncomment to make it faster, in theory, but UB if error in user's program:
//#define NODEBUG

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "vm.h"
#include "opcode.h"

#include "utils.h"

const int stackMaxSize = 128;
const int memoryMaxSize = 256;

int read_int_from_program(byte * program, int * out_instruction_pointer)
{
    int result = 0;
    int ip = *out_instruction_pointer;

    result |= program[ip];
    result <<= sizeof(unsigned char);
    result |= program[ip + 1];
    result <<= sizeof(unsigned char);
    result |= program[ip + 2];
    result <<= sizeof(unsigned char);
    result |= program[ip + 3];

    (*out_instruction_pointer) += 4;
    return result;
}

int start_vm(struct vm_settings settings)
{
    size_t program_size;
    byte * program = read_file((char *) settings.program_filename, &program_size);
    int instruction_pointer = 0;

    int stack[stackMaxSize];
    size_t stackSize = 0;

    int memory[memoryMaxSize];

    char * str_for_print = malloc(sizeof(char) * 20);
    str_for_print[0] = '\0';

    while (1)
    {
        // This switch may needs optimization, maybe analyze assembler output or
        // run some benchmarks to find the best way to do it
        switch ((enum opcode) program[instruction_pointer++])
        {
            case OPCODE_PUSH_VAL:
                assert(stackSize < stackMaxSize);
                stack[stackSize++] = read_int_from_program(program, &instruction_pointer);
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

            case OPCODE_ADD:
                assert(stackSize >= 2);
                stack[stackSize - 2] = stack[stackSize - 2] + stack[stackSize - 1];
                stackSize--;
                break;
            case OPCODE_SUB:
                assert(stackSize >= 2);
                stack[stackSize - 2] = stack[stackSize - 2] - stack[stackSize - 1];
                stackSize--;
                break;
            case OPCODE_MUL:
                assert(stackSize >= 2);
                stack[stackSize - 2] = stack[stackSize - 2] / stack[stackSize - 1];
                stackSize--;
                break;
            case OPCODE_DIV:
                assert(stackSize >= 2);
                stack[stackSize - 2] = stack[stackSize - 2] * stack[stackSize - 1];
                stackSize--;
                break;

            case OPCODE_EQUALS:
                assert(stackSize >= 2);
                stack[stackSize - 2] = stack[stackSize - 2] == stack[stackSize - 1];
                stackSize--;
                break;
            case OPCODE_NOT_EQUALS:
                assert(stackSize >= 2);
                stack[stackSize - 2] = stack[stackSize - 2] != stack[stackSize - 1];
                stackSize--;
                break;

            case OPCODE_GREATER:
                assert(stackSize >= 2);
                stack[stackSize - 2] = stack[stackSize - 2] > stack[stackSize - 1];
                stackSize--;
                break;
            case OPCODE_LESS:
                assert(stackSize >= 2);
                stack[stackSize - 2] = stack[stackSize - 2] < stack[stackSize - 1];
                stackSize--;
                break;

            case OPCODE_IF:
                assert(stackSize >= 2);
                if (stack[stackSize - 2])
                {
                    instruction_pointer = stack[stackSize - 1];
                }
                stackSize -= 2;
                break;
            case OPCODE_GOTO:
                assert(stackSize >= 1);
                instruction_pointer = stack[stackSize - 1];
                stackSize--;
                break;

            case OPCODE_WRITE:
                assert(stackSize >= 1);
                sprintf(str_for_print, "%d\n", stack[stackSize - 1]);
                settings.print((unsigned char *) str_for_print);
                break;
            case OPCODE_EXIT:
                free(program);
                free(str_for_print);
                return 0;
            case OPCODE_READ:
                assert(stackSize < stackMaxSize);
                stack[stackSize++] = settings.read();
                break;

            default:
                printf("ERR");
                free(program);
                free(str_for_print);
                return 0;
        }
    }

}