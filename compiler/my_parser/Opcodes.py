from enum import Enum


class Opcode(Enum):
    OPCODE_PUSH_VAL_I = 0x01
    OPCODE_PUSH_VAL_F = 0x02
    OPCODE_PUSH_VAL_S = 0x03
    OPCODE_PUSH_MEM = 0x05

    OPCODE_POP_MEM = 0x15
    OPCODE_SEEK_MEM = 0x16

    OPCODE_ADD_I = 0x30
    OPCODE_SUB_I = 0x31
    OPCODE_MUL_I = 0x32
    OPCODE_DIV_I = 0x33
    OPCODE_INVERT_I = 0x34

    OPCODE_EQUALS_I = 0x3A
    OPCODE_NOT_EQUALS_I = 0x3B
    OPCODE_GREATER_I = 0x3C
    OPCODE_LESS_I = 0x3D
    OPCODE_GREATER_EQUAL_I = 0x3E
    OPCODE_LESS_EQUAL_I = 0x3F

    OPCODE_ADD_F = 0x40
    OPCODE_SUB_F = 0x41
    OPCODE_MUL_F = 0x42
    OPCODE_DIV_F = 0x43
    OPCODE_INVERT_F = 0x44

    OPCODE_EQUALS_F = 0x4A
    OPCODE_NOT_EQUALS_F = 0x4B
    OPCODE_GREATER_F = 0x4C
    OPCODE_LESS_F = 0x4D
    OPCODE_GREATER_EQUAL_F = 0x4E
    OPCODE_LESS_EQUAL_F = 0x4F

    OPCODE_CONCAT_S = 0x50
    OPCODE_REPEAT_S = 0x51
    OPCODE_LENGTH_S = 0x52

    OPCODE_EQUALS_S = 0x5A
    OPCODE_NOT_EQUALS_S = 0x5B
    OPCODE_GREATER_S = 0x5C
    OPCODE_LESS_S = 0x5D
    OPCODE_GREATER_EQUAL_S = 0x5E
    OPCODE_LESS_EQUAL_S = 0x5F

    OPCODE_NOT = 0x6A
    OPCODE_AND = 0x6B
    OPCODE_OR = 0x6C

    OPCODE_ITOF = 0x70
    OPCODE_FTOI = 0x71

    OPCODE_ITOS = 0x72
    OPCODE_STOI = 0x73

    OPCODE_FTOS = 0x74
    OPCODE_STOF = 0x75

    OPCODE_IF = 0x80
    OPCODE_GOTO = 0x81

    OPCODE_EXIT = 0xA1
    OPCODE_READ = 0xA2
    OPCODE_WRITE_I = 0xA3
    OPCODE_WRITE_F = 0xA4
    OPCODE_WRITE_B = 0xA5
    OPCODE_WRITE_S = 0xA6
