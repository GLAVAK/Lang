from my_parser.Opcodes import Opcode
from my_parser.data_type import DataType
from my_parser.exceptions.compiler_error import CompilerError


class Operator:
    def __init__(self, content: str, operand_types, return_type, opcode):
        self.content = content
        self.operand_types = operand_types
        self.return_type = return_type
        self.opcode = opcode


def get_operator(content: str, operand_types, line: int, column: int) -> Operator:
    """
    Finds matching operator in legal operator list and returns it
    :param content:
    :param operand_types:
    :param line: Position in code, for error throwing
    :param column: Position in code, for error throwing
    :return: Operator, contains data about found operator
    """
    operators = [
        Operator("+", [DataType.integer, DataType.integer], DataType.integer, Opcode.OPCODE_ADD_I),
        Operator("+", [DataType.float, DataType.float], DataType.float, Opcode.OPCODE_ADD_F),
        Operator("+", [DataType.string, DataType.string], DataType.string, Opcode.OPCODE_CONCAT_S),

        Operator("-", [DataType.integer, DataType.integer], DataType.integer, Opcode.OPCODE_SUB_I),
        Operator("-", [DataType.float, DataType.float], DataType.float, Opcode.OPCODE_SUB_F),

        Operator("*", [DataType.integer, DataType.integer], DataType.integer, Opcode.OPCODE_MUL_I),
        Operator("*", [DataType.float, DataType.float], DataType.float, Opcode.OPCODE_MUL_F),
        Operator("*", [DataType.string, DataType.integer], DataType.string, Opcode.OPCODE_REPEAT_S),

        Operator("/", [DataType.integer, DataType.integer], DataType.integer, Opcode.OPCODE_DIV_I),
        Operator("/", [DataType.float, DataType.float], DataType.float, Opcode.OPCODE_DIV_F),

        Operator("#", [DataType.integer], DataType.integer, Opcode.OPCODE_INVERT_I),
        Operator("#", [DataType.float], DataType.float, Opcode.OPCODE_INVERT_F),

        Operator("==", [DataType.integer, DataType.integer], DataType.boolean, Opcode.OPCODE_EQUALS_I),
        Operator("==", [DataType.float, DataType.float], DataType.boolean, Opcode.OPCODE_EQUALS_F),
        Operator("==", [DataType.string, DataType.string], DataType.boolean, Opcode.OPCODE_EQUALS_S),

        Operator("!=", [DataType.integer, DataType.integer], DataType.boolean, Opcode.OPCODE_NOT_EQUALS_I),
        Operator("!=", [DataType.float, DataType.float], DataType.boolean, Opcode.OPCODE_NOT_EQUALS_F),
        Operator("!=", [DataType.string, DataType.string], DataType.boolean, Opcode.OPCODE_NOT_EQUALS_S),

        Operator(">", [DataType.integer, DataType.integer], DataType.boolean, Opcode.OPCODE_GREATER_I),
        Operator(">", [DataType.float, DataType.float], DataType.boolean, Opcode.OPCODE_GREATER_F),
        Operator(">", [DataType.string, DataType.string], DataType.boolean, Opcode.OPCODE_GREATER_S),

        Operator("<", [DataType.integer, DataType.integer], DataType.boolean, Opcode.OPCODE_LESS_I),
        Operator("<", [DataType.float, DataType.float], DataType.boolean, Opcode.OPCODE_LESS_F),
        Operator("<", [DataType.string, DataType.string], DataType.boolean, Opcode.OPCODE_LESS_S),

        Operator(">=", [DataType.integer, DataType.integer], DataType.boolean, Opcode.OPCODE_GREATER_EQUAL_I),
        Operator(">=", [DataType.float, DataType.float], DataType.boolean, Opcode.OPCODE_GREATER_EQUAL_F),
        Operator(">=", [DataType.string, DataType.string], DataType.boolean, Opcode.OPCODE_GREATER_EQUAL_S),

        Operator("<=", [DataType.integer, DataType.integer], DataType.boolean, Opcode.OPCODE_LESS_EQUAL_I),
        Operator("<=", [DataType.float, DataType.float], DataType.boolean, Opcode.OPCODE_LESS_EQUAL_F),
        Operator("<=", [DataType.string, DataType.string], DataType.boolean, Opcode.OPCODE_LESS_EQUAL_S),

        Operator("&", [DataType.boolean, DataType.boolean], DataType.boolean, Opcode.OPCODE_AND),
        Operator("|", [DataType.boolean, DataType.boolean], DataType.boolean, Opcode.OPCODE_OR),
        Operator("!", [DataType.boolean], DataType.boolean, Opcode.OPCODE_NOT),
    ]

    for operator in operators:
        if operator.content == content and operator.operand_types == operand_types:
            return operator

    raise CompilerError(line, column, "No operator math for operator '" + content + "' and data types '" +
                        ",".join(x.name for x in operand_types) + "' (missing cast?)")
