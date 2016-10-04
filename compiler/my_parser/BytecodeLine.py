import struct

from my_parser.CodeBlock import CodeBlock
from my_parser.Opcodes import Opcode


class BytecodeLine:
    def __init__(self, opcode: Opcode):
        self.opcode = opcode
        self.args = []

    def pack(self, file):
        opcode_value = int(self.opcode.value)
        file.write(bytes([opcode_value]))
        for arg in self.args:
            arg.pack(file)

    def get_length_in_bytes(self):
        length = 1
        for arg in self.args:
            length += arg.get_length_in_bytes()
        return length

    def __str__(self):
        result = self.opcode.name
        for arg in self.args:
            result += arg.__str__()
        return result


class OpArg:
    def pack(self, data):
        pass

    def get_length_in_bytes(self):
        pass


class IntegerArg(OpArg):
    def __init__(self, num: int):
        self.num = num

    def pack(self, file):
        data = bytearray(self.get_length_in_bytes())
        struct.pack_into(">i", data, 0, self.num)
        file.write(data)

    def get_length_in_bytes(self):
        return 4

    def __str__(self):
        return " const(" + str(self.num) + ")"


class FloatArg(OpArg):
    def __init__(self, num: float):
        self.num = num

    def pack(self, file):
        data = bytearray(self.get_length_in_bytes())
        struct.pack_into(">d", data, 0, self.num)
        file.write(data)

    def get_length_in_bytes(self):
        return 8

    def __str__(self):
        return " const(" + str(self.num) + ")"


class StringArg(OpArg):
    def __init__(self, value: str):
        self.value = value

    def pack(self, file):
        data = bytearray(self.value, "ascii")
        file.write(data)
        file.write(bytes([0]))  # \0 to terminate string

    def get_length_in_bytes(self):
        return len(self.value) + 1

    def __str__(self):
        return " str(" + str(self.value) + ")"


class MemoryAddressArg(OpArg):
    def __init__(self, addr: int):
        self.addr = addr

    def pack(self, file):
        data = bytearray(self.get_length_in_bytes())
        struct.pack_into(">b", data, 0, self.addr)
        file.write(data)

    def get_length_in_bytes(self):
        return 1

    def __str__(self):
        return " mem(" + str(self.addr) + ")"


class ProgramAddressArg(OpArg):
    def __init__(self, target_block: CodeBlock):
        self.target_block = target_block

    def pack(self, file):
        data = bytearray(self.get_length_in_bytes())
        struct.pack_into(">I", data, 0, self.target_block.bytecode_position)
        file.write(data)

    def get_length_in_bytes(self):
        return 4

    def __str__(self):
        return " goto(" + str(self.target_block.bytecode_position) + ")"
