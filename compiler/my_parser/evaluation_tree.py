from typing import List

from my_parser.bytecode_line import BytecodeLine, FloatArg, MemoryAddressArg, IntegerArg, StringArg
from my_parser.data_type import DataType
from my_parser.exceptions.compiler_error import CompilerError
from my_parser.exceptions.compiler_warning import CompilerWarning
from my_parser.opcodes import Opcode
from my_parser.operators import get_operator, Operator
from my_parser.scope import Scope


class TreeNode:
    def __init__(self, line: int, column: int):
        self.left = None
        self.right = None
        self.line = line
        self.column = column

    def get_byte_code(self, scope: Scope) -> List[BytecodeLine]:
        """
        :returns byte code, in result of execution of which, the expression will be evaluated
        and the result will be on top of the stack
        """
        pass

    def get_return_type(self, scope: Scope) -> DataType:
        pass

    def build(self, scope: Scope) -> None:
        """
        Should be called when all of node children defined
        """
        pass

    def is_constant(self)->bool:
        """
        Whether or not this node contains no children and have constant value
        """
        return False


class NodeOperator(TreeNode):
    def __init__(self, operator: str, line: int, column: int):
        super().__init__(line, column)
        self.operator = operator

    def get_operator(self, scope: Scope) -> Operator:
        operand_types = [self.left.get_return_type(scope)]
        if self.right is not None:
            # Two operands
            operand_types.append(self.right.get_return_type(scope))

        return get_operator(self.operator, operand_types, self.line, self.column)

    def get_byte_code(self, scope: Scope) -> List[BytecodeLine]:
        expression_to_assign = self.left.get_byte_code(scope)
        if self.right is not None:
            # Two operands
            expression_to_assign.extend(self.right.get_byte_code(scope))

        operator = self.get_operator(scope)

        code_line = BytecodeLine(operator.opcode)
        expression_to_assign.append(code_line)

        return expression_to_assign

    def get_return_type(self, scope: Scope) -> DataType:
        return self.get_operator(scope).return_type


class NodeInteger(TreeNode):
    def __init__(self, value: int, line: int, column: int):
        super().__init__(line, column)
        self.value = value

    def get_byte_code(self, scope: Scope) -> List[BytecodeLine]:
        code_line = BytecodeLine(Opcode.OPCODE_PUSH_VAL_I)
        code_line.args.append(IntegerArg(self.value))
        return [code_line]

    def get_return_type(self, scope: Scope) -> DataType:
        return DataType.integer

    def is_constant(self)->bool:
        return True


class NodeFloat(TreeNode):
    def __init__(self, value: float, line: int, column: int):
        super().__init__(line, column)
        self.value = value

    def get_byte_code(self, scope) -> List[BytecodeLine]:
        code_line = BytecodeLine(Opcode.OPCODE_PUSH_VAL_F)
        code_line.args.append(FloatArg(self.value))
        return [code_line]

    def get_return_type(self, scope: Scope) -> DataType:
        return DataType.float

    def is_constant(self)->bool:
        return True


class NodeBoolean(TreeNode):
    def __init__(self, value: bool, line: int, column: int):
        super().__init__(line, column)
        self.value = value

    def get_byte_code(self, scope) -> List[BytecodeLine]:
        code_line = BytecodeLine(Opcode.OPCODE_PUSH_VAL_I)
        if self.value:
            code_line.args.append(IntegerArg(1))
        else:
            code_line.args.append(IntegerArg(0))
        return [code_line]

    def get_return_type(self, scope: Scope) -> DataType:
        return DataType.boolean

    def is_constant(self)->bool:
        return True


class NodeString(TreeNode):
    def __init__(self, value: str, line: int, column: int):
        super().__init__(line, column)
        self.value = value

    def get_byte_code(self, scope: Scope) -> List[BytecodeLine]:
        code_line = BytecodeLine(Opcode.OPCODE_PUSH_VAL_S)
        code_line.args.append(StringArg(self.value))
        return [code_line]

    def get_return_type(self, scope: Scope) -> DataType:
        return DataType.string

    def is_constant(self)->bool:
        return True


class NodeVariable(TreeNode):
    def __init__(self, var_name: str, line: int, column: int):
        super().__init__(line, column)
        self.var_name = var_name

    def get_byte_code(self, scope: Scope) -> List[BytecodeLine]:
        code_line = BytecodeLine(Opcode.OPCODE_PUSH_MEM)
        code_line.args.append(MemoryAddressArg(scope.names_table[self.var_name].address))
        return [code_line]

    def get_return_type(self, scope: Scope) -> DataType:
        return scope.names_table[self.var_name].type


class NodeMacro(TreeNode):
    def __init__(self, macro_name: str, line: int, column: int):
        super().__init__(line, column)
        self.macro_name = macro_name

    def get_byte_code(self, scope: Scope) -> List[BytecodeLine]:
        expression_to_assign = []

        if self.macro_name == 'write':
            expression_to_assign = self.left.get_byte_code(scope)
            if self.left.get_return_type(scope) is DataType.integer:
                expression_to_assign.append(BytecodeLine(Opcode.OPCODE_WRITE_I))
            elif self.left.get_return_type(scope) is DataType.float:
                expression_to_assign.append(BytecodeLine(Opcode.OPCODE_WRITE_F))
            elif self.left.get_return_type(scope) is DataType.boolean:
                expression_to_assign.append(BytecodeLine(Opcode.OPCODE_WRITE_B))
            elif self.left.get_return_type(scope) is DataType.string:
                expression_to_assign.append(BytecodeLine(Opcode.OPCODE_WRITE_S))
        elif self.macro_name == 'read':
            expression_to_assign.append(BytecodeLine(Opcode.OPCODE_READ))
        elif self.macro_name == 'exit':
            expression_to_assign.append(BytecodeLine(Opcode.OPCODE_EXIT))

        return expression_to_assign

    def get_return_type(self, scope: Scope) -> DataType:
        if self.macro_name == 'write':
            return self.left.get_return_type(scope)
        elif self.macro_name == 'read':
            return DataType.string


class NodeCast(TreeNode):
    def __init__(self, target_type: DataType, line: int, column: int):
        super().__init__(line, column)
        self.target_type = target_type

    def get_cast_opcode(self, scope: Scope) -> Opcode:

        if self.target_type is DataType.integer:
            if self.left.get_return_type(scope) is DataType.integer:
                return None
            elif self.left.get_return_type(scope) is DataType.float:
                return Opcode.OPCODE_FTOI
            elif self.left.get_return_type(scope) is DataType.string:
                return Opcode.OPCODE_STOI

        elif self.target_type is DataType.float:
            if self.left.get_return_type(scope) is DataType.integer:
                return Opcode.OPCODE_ITOF
            elif self.left.get_return_type(scope) is DataType.float:
                return None
            elif self.left.get_return_type(scope) is DataType.string:
                return Opcode.OPCODE_STOF

        elif self.target_type is DataType.string:
            if self.left.get_return_type(scope) is DataType.integer:
                return Opcode.OPCODE_ITOS
            elif self.left.get_return_type(scope) is DataType.float:
                return Opcode.OPCODE_FTOS
            elif self.left.get_return_type(scope) is DataType.string:
                return None

    def get_byte_code(self, scope: Scope) -> List[BytecodeLine]:
        expression_to_assign = self.left.get_byte_code(scope)

        opcode = self.get_cast_opcode(scope)

        if opcode is not None:
            expression_to_assign.append(BytecodeLine(opcode))
        else:
            scope.warnings.append(CompilerWarning(self.line, self.column - 1,
                                                  "Redundant cast (" + self.target_type.name + " casted to " +
                                                  self.target_type.name + ")"))

        return expression_to_assign

    def get_return_type(self, scope: Scope) -> DataType:
        return self.target_type


class NodeAssignment(TreeNode):
    def __init__(self, line: int, column: int):
        super().__init__(line, column)
        self.data_type = DataType.undefined

    def get_byte_code(self, scope: Scope) -> List[BytecodeLine]:
        expression_to_assign = self.right.get_byte_code(scope)

        code_line = BytecodeLine(Opcode.OPCODE_POP_MEM)
        code_line.args.append(MemoryAddressArg(scope.names_table[self.left.var_name].address))
        expression_to_assign.append(code_line)

        return expression_to_assign

    def build(self, scope: Scope) -> None:
        if not isinstance(self.left, NodeVariable):
            raise CompilerError(self.line, self.column, "Not a variable name at the left of assignment")

        var_data_type = scope.names_table[self.left.var_name].type
        value_type = self.right.get_return_type(scope)
        if var_data_type == DataType.undefined:
            self.data_type = value_type
            scope.names_table[self.left.var_name].type = value_type
        elif var_data_type == value_type:
            self.data_type = var_data_type
        else:
            raise CompilerError(self.line, self.column, "Attempt to change variable '" + self.left.var_name +
                                "' type from " + var_data_type.name + " to " + value_type.name)

    def get_return_type(self, scope: Scope) -> DataType:
        return DataType.undefined
