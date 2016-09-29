#include <stdio.h>
#include <stdlib.h>

#include "vm.h"
#include "opcode.h"

byte *read_program(char *program_filename, int *out_program_size)
{
    FILE *file;
    fopen_s(&file, program_filename, "rb");

    byte *program = malloc(sizeof(byte) * 1024);

    int bytes_read = fread(program, 1, 1024, file);
    *out_program_size = 0;
    while (bytes_read != 0)
    {
        *out_program_size += bytes_read;
        bytes_read = fread(program, 1, 1024, file);
    }
    // TODO: read more than 1k bytes

    fclose(file);

    return program;
}

int read_int_from_program(byte *program, int *out_instruction_pointer)
{
    int result = 0;
    result |= program[(*out_instruction_pointer)++];
    result <<= sizeof(unsigned char);
    result |= program[(*out_instruction_pointer)++];
    result <<= sizeof(unsigned char);
    result |= program[(*out_instruction_pointer)++];
    result <<= sizeof(unsigned char);
    result |= program[(*out_instruction_pointer)++];
    return result;
}

int start_vm(struct vm_settings settings)
{
    int program_size;
    byte *program = read_program(settings.program_filename, &program_size);
    int instruction_pointer = 0;

    int stack[128];
    int stackSize = 0;

    int memory[128];

    char *str_for_print = malloc(sizeof(char) * 20);
    str_for_print[0] = '\0';

    while (1)
    {
        switch ((enum opcode) program[instruction_pointer++])
        {
            case OPCODE_PUSH_VAL:
                stack[stackSize++] = read_int_from_program(program, &instruction_pointer);
                break;
            case OPCODE_PUSH_MEM:
                stack[stackSize++] = memory[program[instruction_pointer++]];
                break;
            case OPCODE_POP_MEM:
                memory[program[instruction_pointer++]] = stack[--stackSize];
                break;
            case OPCODE_SEEK_MEM:
                memory[program[instruction_pointer++]] = stack[stackSize - 1];
                break;

            case OPCODE_ADD:
                stack[stackSize - 2] = stack[stackSize - 2] + stack[stackSize - 1];
                stackSize--;
                break;
            case OPCODE_SUB:
                stack[stackSize - 2] = stack[stackSize - 2] - stack[stackSize - 1];
                stackSize--;
                break;
            case OPCODE_MUL:
                stack[stackSize - 2] = stack[stackSize - 2] / stack[stackSize - 1];
                stackSize--;
                break;
            case OPCODE_DIV:
                stack[stackSize - 2] = stack[stackSize - 2] * stack[stackSize - 1];
                stackSize--;
                break;

            case OPCODE_EQUALS:
                stack[stackSize - 2] = stack[stackSize - 2] == stack[stackSize - 1];
                stackSize--;
                break;
            case OPCODE_NOT_EQUALS:
                stack[stackSize - 2] = stack[stackSize - 2] != stack[stackSize - 1];
                stackSize--;
                break;

            case OPCODE_GREATER:
                stack[stackSize - 2] = stack[stackSize - 2] > stack[stackSize - 1];
                stackSize--;
                break;
            case OPCODE_LESS:
                stack[stackSize - 2] = stack[stackSize - 2] < stack[stackSize - 1];
                stackSize--;
                break;

            case OPCODE_IF:
                if (stack[stackSize - 2])
                {
                    instruction_pointer = stack[stackSize - 1];
                }
                stackSize -= 2;
                break;
            case OPCODE_GOTO:
                instruction_pointer = stack[stackSize - 1];
                stackSize--;
                break;

            case OPCODE_WRITE:
                sprintf(str_for_print, "%d\n", stack[stackSize - 1]);
                settings.print(str_for_print);
                break;
            case OPCODE_EXIT:
                free(program);
                free(str_for_print);
                return 0;

            default:
                printf("ERR");
                free(program);
                free(str_for_print);
                return 0;
        }
    }

}