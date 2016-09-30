from my_parser.BytecodeLine import BytecodeLine, NumericArg, MemoryAddressArg
from my_parser.Opcodes import Opcode


class TreeNode:
    def __init__(self):
        self.left = None
        self.right = None

    def get_byte_code(self, names_table):
        """
        :returns byte code, in result of execution of which, the expression will be evaluated
        and the result will be on top of the stack
        """
        pass


class NodeOperator(TreeNode):
    def __init__(self, operator: str):
        super().__init__()
        self.operator = operator

    def get_operator_opcode(self) -> Opcode:
        if self.operator == '+':
            return Opcode.OPCODE_ADD
        elif self.operator == '-':
            return Opcode.OPCODE_SUB
        elif self.operator == '*':
            return Opcode.OPCODE_MUL
        elif self.operator == '/':
            return Opcode.OPCODE_DIV
        elif self.operator == '+-':
            return Opcode.OPCODE_INVERT
        elif self.operator == '>':
            return Opcode.OPCODE_GREATER
        elif self.operator == '<':
            return Opcode.OPCODE_LESS
        elif self.operator == '!':
            return Opcode.OPCODE_NOT

    def get_byte_code(self, names_table):
        expression_to_assign = self.left.get_byte_code(names_table)

        if self.right is not None:
            expression_to_assign.extend(self.right.get_byte_code(names_table))

        code_line = BytecodeLine(self.get_operator_opcode())
        expression_to_assign.append(code_line)

        return expression_to_assign


class NodeConstant(TreeNode):
    def __init__(self, value: int):
        super().__init__()
        self.value = value

    def get_byte_code(self, names_table):
        code_line = BytecodeLine(Opcode.OPCODE_PUSH_VAL)
        code_line.args.append(NumericArg(self.value))
        return [code_line]


class NodeVariable(TreeNode):
    def __init__(self, var_name: str):
        super().__init__()
        self.var_name = var_name

    def get_byte_code(self, names_table):
        code_line = BytecodeLine(Opcode.OPCODE_PUSH_MEM)
        code_line.args.append(MemoryAddressArg(names_table[self.var_name]))
        return [code_line]


class NodeMacro(TreeNode):
    def __init__(self, macro_name: str):
        super().__init__()
        self.macro_name = macro_name

    def get_byte_code(self, names_table):
        expression_to_assign = []

        if self.macro_name == 'write':
            expression_to_assign = self.left.get_byte_code(names_table)
            expression_to_assign.append(BytecodeLine(Opcode.OPCODE_WRITE))
        elif self.macro_name == 'read':
            expression_to_assign.append(BytecodeLine(Opcode.OPCODE_READ))
        elif self.macro_name == 'exit':
            expression_to_assign.append(BytecodeLine(Opcode.OPCODE_EXIT))

        return expression_to_assign


class NodeAssignment(TreeNode):
    def __init__(self):
        super().__init__()

    def get_byte_code(self, names_table):
        expression_to_assign = self.right.get_byte_code(names_table)

        # Use SEEK, not POP, to leave result on the stack for chaining (a=b=c)
        code_line = BytecodeLine(Opcode.OPCODE_SEEK_MEM)
        code_line.args.append(MemoryAddressArg(names_table[self.left.var_name]))
        expression_to_assign.append(code_line)

        return expression_to_assign
