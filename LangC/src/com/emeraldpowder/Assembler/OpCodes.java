package com.emeraldpowder.Assembler;

/**
 * Created by glavak on Feb 16, 17.
 */

public class OpCodes
{
    static final int OPCODE_PUSH_VAL_I = 0x01;
    static final int OPCODE_PUSH_VAL_F = 0x02;
    static final int OPCODE_PUSH_VAL_S = 0x03;
    static final int OPCODE_PUSH_MEM = 0x05;

    static final int OPCODE_POP_MEM = 0x15;
    static final int OPCODE_SEEK_MEM = 0x16;

    static final int OPCODE_ADD_I = 0x30;
    static final int OPCODE_SUB_I = 0x31;
    static final int OPCODE_MUL_I = 0x32;
    static final int OPCODE_DIV_I = 0x33;
    static final int OPCODE_INVERT_I = 0x34;

    static final int OPCODE_EQUALS_I = 0x3A;
    static final int OPCODE_NOT_EQUALS_I = 0x3B;
    static final int OPCODE_GREATER_I = 0x3C;
    static final int OPCODE_LESS_I = 0x3D;
    static final int OPCODE_GREATER_EQUAL_I = 0x3E;
    static final int OPCODE_LESS_EQUAL_I = 0x3F;

    static final int OPCODE_ADD_F = 0x40;
    static final int OPCODE_SUB_F = 0x41;
    static final int OPCODE_MUL_F = 0x42;
    static final int OPCODE_DIV_F = 0x43;
    static final int OPCODE_INVERT_F = 0x44;

    static final int OPCODE_EQUALS_F = 0x4A;
    static final int OPCODE_NOT_EQUALS_F = 0x4B;
    static final int OPCODE_GREATER_F = 0x4C;
    static final int OPCODE_LESS_F = 0x4D;
    static final int OPCODE_GREATER_EQUAL_F = 0x4E;
    static final int OPCODE_LESS_EQUAL_F = 0x4F;

    static final int OPCODE_CONCAT_S = 0x50;
    static final int OPCODE_REPEAT_S = 0x51;
    static final int OPCODE_LENGTH_S = 0x52;

    static final int OPCODE_EQUALS_S = 0x5A;
    static final int OPCODE_NOT_EQUALS_S = 0x5B;
    static final int OPCODE_GREATER_S = 0x5C;
    static final int OPCODE_LESS_S = 0x5D;
    static final int OPCODE_GREATER_EQUAL_S = 0x5E;
    static final int OPCODE_LESS_EQUAL_S = 0x5F;

    static final int OPCODE_NOT = 0x6A;
    static final int OPCODE_AND = 0x6B;
    static final int OPCODE_OR = 0x6C;

    static final int OPCODE_ITOF = 0x70;
    static final int OPCODE_FTOI = 0x71;

    static final int OPCODE_ITOS = 0x72;
    static final int OPCODE_STOI = 0x73;

    static final int OPCODE_FTOS = 0x74;
    static final int OPCODE_STOF = 0x75;

    static final int OPCODE_IF = 0x80;
    static final int OPCODE_GOTO = 0x81;

    static final int OPCODE_EXIT = 0xA1;
    static final int OPCODE_READ = 0xA2;
    static final int OPCODE_WRITE_I = 0xA3;
    static final int OPCODE_WRITE_F = 0xA4;
    static final int OPCODE_WRITE_B = 0xA5;
    static final int OPCODE_WRITE_S = 0xA6;
}
