from my_parser.BytecodeLine import BytecodeLine, FloatArg, MemoryAddressArg, IntegerArg, StringArg
from my_parser.Opcodes import Opcode
from my_parser.data_type import DataType
from my_parser.exceptions.compiler_error import CompilerError
from my_parser.exceptions.internal_error import InternalError
from my_parser.scope import Scope


class TreeNode:
    def __init__(self):
        self.left = None
        self.right = None

    def get_byte_code(self, scope: Scope):
        """
        :returns byte code, in result of execution of which, the expression will be evaluated
        and the result will be on top of the stack
        """
        pass

    def get_return_type(self, scope: Scope) -> DataType:
        pass

    def build(self, scope: Scope):
        """
        Should be called when all or node children defined
        """
        pass


class NodeOperator(TreeNode):
    def __init__(self, operator: str):
        super().__init__()
        self.data_type = DataType.undefined
        self.operator = operator

    def get_operator_opcode(self, operands_type: DataType) -> Opcode:
        if self.operator == '+':
            if operands_type is DataType.integer:
                return Opcode.OPCODE_ADD_I
            elif operands_type is DataType.float:
                return Opcode.OPCODE_ADD_F

        elif self.operator == '-':
            if operands_type is DataType.integer:
                return Opcode.OPCODE_SUB_I
            elif operands_type is DataType.float:
                return Opcode.OPCODE_SUB_F

        elif self.operator == '*':
            if operands_type is DataType.integer:
                return Opcode.OPCODE_MUL_I
            elif operands_type is DataType.float:
                return Opcode.OPCODE_MUL_F

        elif self.operator == '/':
            if operands_type is DataType.integer:
                return Opcode.OPCODE_MUL_I
            elif operands_type is DataType.float:
                return Opcode.OPCODE_MUL_F

        elif self.operator == '#':
            if operands_type is DataType.integer:
                return Opcode.OPCODE_INVERT_I
            elif operands_type is DataType.float:
                return Opcode.OPCODE_INVERT_F

        elif self.operator == '==':
            if operands_type is DataType.integer:
                return Opcode.OPCODE_EQUALS_I
            elif operands_type is DataType.float:
                return Opcode.OPCODE_EQUALS_F

        elif self.operator == '!=':
            if operands_type is DataType.integer:
                return Opcode.OPCODE_NOT_EQUALS_I
            elif operands_type is DataType.float:
                return Opcode.OPCODE_NOT_EQUALS_F

        elif self.operator == '>':
            if operands_type is DataType.integer:
                return Opcode.OPCODE_GREATER_I
            elif operands_type is DataType.float:
                return Opcode.OPCODE_GREATER_F

        elif self.operator == '<':
            if operands_type is DataType.integer:
                return Opcode.OPCODE_LESS_I
            elif operands_type is DataType.float:
                return Opcode.OPCODE_LESS_F

        elif self.operator == '>=':
            if operands_type is DataType.integer:
                return Opcode.OPCODE_GREATER_EQUAL_I
            elif operands_type is DataType.float:
                return Opcode.OPCODE_GREATER_EQUAL_F

        elif self.operator == '<=':
            if operands_type is DataType.integer:
                return Opcode.OPCODE_LESS_EQUAL_I
            elif operands_type is DataType.float:
                return Opcode.OPCODE_LESS_EQUAL_F

        elif self.operator == '!':
            return Opcode.OPCODE_NOT

        else:
            raise InternalError("Undefined operator with content '" + self.operator + "'")

    def get_byte_code(self, scope: Scope):

        expression_to_assign = self.left.get_byte_code(scope)

        if self.right is not None:
            expression_to_assign.extend(self.right.get_byte_code(scope))
        self.data_type = self.get_return_type(scope)

        operands_type = self.left.get_return_type(scope)

        code_line = BytecodeLine(self.get_operator_opcode(operands_type))
        expression_to_assign.append(code_line)

        return expression_to_assign

    def get_return_type(self, scope: Scope):
        if self.right is not None:
            # Two operands
            if self.right.get_return_type(scope) == self.left.get_return_type(scope):
                if self.left.get_return_type(scope) is DataType.integer or self.left.get_return_type(
                        scope) is DataType.float:
                    if self.operator == '+' or \
                                    self.operator == '-' or \
                                    self.operator == '*' or \
                                    self.operator == '/':
                        return self.right.get_return_type(scope)
                    elif self.operator == '==' or \
                                    self.operator == '!=' or \
                                    self.operator == '>' or \
                                    self.operator == '<' or \
                                    self.operator == '>=' or \
                                    self.operator == '<=':
                        return DataType.boolean
                    else:
                        raise CompilerError(0, 0, "Invalid operand type")
            else:
                # TODO: error line and col
                raise CompilerError(0, 0, "Operation on different types, explicit conversion required")
        else:
            if self.operator == '!' and self.left.get_return_type(scope) is DataType.boolean:
                return DataType.boolean
            elif self.operator == '#' and (
                            self.left.get_return_type(scope) is DataType.integer or
                            self.left.get_return_type(scope) is DataType.float):
                return self.left.get_return_type(scope)
            else:
                raise CompilerError(0, 0, "Invalid operand type")


class NodeInteger(TreeNode):
    def __init__(self, value: int):
        super().__init__()
        self.value = value

    def get_byte_code(self, scope: Scope):
        code_line = BytecodeLine(Opcode.OPCODE_PUSH_VAL_I)
        code_line.args.append(IntegerArg(self.value))
        return [code_line]

    def get_return_type(self, scope: Scope):
        return DataType.integer


class NodeFloat(TreeNode):
    def __init__(self, value: float):
        super().__init__()
        self.value = value

    def get_byte_code(self, scope):
        code_line = BytecodeLine(Opcode.OPCODE_PUSH_VAL_F)
        code_line.args.append(FloatArg(self.value))
        return [code_line]

    def get_return_type(self, scope: Scope):
        return DataType.float


class NodeBoolean(TreeNode):
    def __init__(self, value: bool):
        super().__init__()
        self.value = value

    def get_byte_code(self, scope):
        code_line = BytecodeLine(Opcode.OPCODE_PUSH_VAL_I)
        if self.value:
            code_line.args.append(IntegerArg(1))
        else:
            code_line.args.append(IntegerArg(0))
        return [code_line]

    def get_return_type(self, scope: Scope):
        return DataType.boolean


class NodeString(TreeNode):
    def __init__(self, value: str):
        super().__init__()
        self.value = value

    def get_byte_code(self, scope: Scope):
        code_line = BytecodeLine(Opcode.OPCODE_PUSH_VAL_S)
        code_line.args.append(StringArg(self.value))
        return [code_line]

    def get_return_type(self, scope: Scope):
        return DataType.string


class NodeVariable(TreeNode):
    def __init__(self, var_name: str):
        super().__init__()
        self.var_name = var_name

    def get_byte_code(self, scope: Scope):
        code_line = BytecodeLine(Opcode.OPCODE_PUSH_MEM)
        code_line.args.append(MemoryAddressArg(scope.names_table[self.var_name].address))
        return [code_line]

    def get_return_type(self, scope: Scope):
        return scope.names_table[self.var_name].type


class NodeMacro(TreeNode):
    def __init__(self, macro_name: str):
        super().__init__()
        self.macro_name = macro_name

    def get_byte_code(self, scope: Scope):
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

    def get_return_type(self, scope: Scope):
        if self.macro_name == 'write':
            return self.left.get_return_type(scope)
        elif self.macro_name == 'read':
            return DataType.string


class NodeCast(TreeNode):
    def __init__(self, target_type: DataType):
        super().__init__()
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

    def get_byte_code(self, scope: Scope):
        expression_to_assign = self.left.get_byte_code(scope)

        opcode = self.get_cast_opcode(scope)

        if opcode is not None:
            # TODO: leave warning (redutand cast)
            expression_to_assign.append(BytecodeLine(opcode))

        return expression_to_assign

    def get_return_type(self, scope: Scope):
        return self.target_type


class NodeAssignment(TreeNode):
    def __init__(self):
        super().__init__()
        self.data_type = DataType.undefined

    def get_byte_code(self, scope: Scope):
        expression_to_assign = self.right.get_byte_code(scope)

        # Use SEEK, not POP, to leave result on the stack for chaining (a=b=c)
        code_line = BytecodeLine(Opcode.OPCODE_SEEK_MEM)
        code_line.args.append(MemoryAddressArg(scope.names_table[self.left.var_name].address))
        expression_to_assign.append(code_line)

        return expression_to_assign

    def build(self, scope: Scope):
        if not isinstance(self.left, NodeVariable):
            raise CompilerError(0, 0, "You can only assign to variables")  # TODO: error line and col

        var_data_type = scope.names_table[self.left.var_name].type
        if var_data_type == DataType.undefined:
            self.data_type = self.right.get_return_type(scope)
            scope.names_table[self.left.var_name].type = self.right.get_return_type(scope)
        elif var_data_type == self.right.get_return_type(scope):
            self.data_type = var_data_type
        else:
            raise CompilerError(0, 0, "You can't change variable type")  # TODO: error line and col

    def get_return_type(self, scope: Scope):
        return self.right.get_return_type(scope)
