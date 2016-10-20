from typing import List

from my_parser.data_type import DataType
from my_parser.exceptions.compiler_error import CompilerError
from my_parser.opcodes import Opcode


class Operator:
    def __init__(self, content: str, operand_types: List[DataType], return_type: DataType, opcode: Opcode,
                 calculate_function):
        """

        :param content:
        :param operand_types:
        :param return_type:
        :param opcode:
        :param calculate_function: Used to precalculate constants for optimization
        """
        self.content = content
        self.operand_types = operand_types
        self.return_type = return_type
        self.opcode = opcode
        self.calculate_function = calculate_function


def get_operator(content: str, operand_types: List[DataType], line: int, column: int) -> Operator:
    """
    Finds matching operator in legal operator list and returns it
    :param content:
    :param operand_types:
    :param line: Position in code, for error throwing
    :param column: Position in code, for error throwing
    :return: Operator, contains data about found operator
    """

    operators = [
        Operator("+", [DataType.integer, DataType.integer], DataType.integer, Opcode.OPCODE_ADD_I,
                 lambda a, b: a + b),
        Operator("+", [DataType.float, DataType.float], DataType.float, Opcode.OPCODE_ADD_F,
                 lambda a, b: a + b),
        Operator("+", [DataType.string, DataType.string], DataType.string, Opcode.OPCODE_CONCAT_S,
                 lambda a, b: a + b),

        Operator("-", [DataType.integer, DataType.integer], DataType.integer, Opcode.OPCODE_SUB_I,
                 lambda a, b: a - b),
        Operator("-", [DataType.float, DataType.float], DataType.float, Opcode.OPCODE_SUB_F,
                 lambda a, b: a - b),

        Operator("*", [DataType.integer, DataType.integer], DataType.integer, Opcode.OPCODE_MUL_I,
                 lambda a, b: a * b),
        Operator("*", [DataType.float, DataType.float], DataType.float, Opcode.OPCODE_MUL_F,
                 lambda a, b: a * b),
        Operator("*", [DataType.string, DataType.integer], DataType.string, Opcode.OPCODE_REPEAT_S,
                 lambda a, b: a * b),

        Operator("/", [DataType.integer, DataType.integer], DataType.integer, Opcode.OPCODE_DIV_I,
                 lambda a, b: a / b),
        Operator("/", [DataType.float, DataType.float], DataType.float, Opcode.OPCODE_DIV_F,
                 lambda a, b: a / b),

        Operator("#", [DataType.integer], DataType.integer, Opcode.OPCODE_INVERT_I,
                 lambda a: -a),
        Operator("#", [DataType.float], DataType.float, Opcode.OPCODE_INVERT_F,
                 lambda a: -a),

        Operator("==", [DataType.integer, DataType.integer], DataType.boolean, Opcode.OPCODE_EQUALS_I,
                 lambda a, b: a == b),
        Operator("==", [DataType.float, DataType.float], DataType.boolean, Opcode.OPCODE_EQUALS_F,
                 lambda a, b: a == b),
        Operator("==", [DataType.string, DataType.string], DataType.boolean, Opcode.OPCODE_EQUALS_S,
                 lambda a, b: a == b),

        Operator("!=", [DataType.integer, DataType.integer], DataType.boolean, Opcode.OPCODE_NOT_EQUALS_I,
                 lambda a, b: a != b),
        Operator("!=", [DataType.float, DataType.float], DataType.boolean, Opcode.OPCODE_NOT_EQUALS_F,
                 lambda a, b: a != b),
        Operator("!=", [DataType.string, DataType.string], DataType.boolean, Opcode.OPCODE_NOT_EQUALS_S,
                 lambda a, b: a != b),

        Operator(">", [DataType.integer, DataType.integer], DataType.boolean, Opcode.OPCODE_GREATER_I,
                 lambda a, b: a > b),
        Operator(">", [DataType.float, DataType.float], DataType.boolean, Opcode.OPCODE_GREATER_F,
                 lambda a, b: a > b),
        Operator(">", [DataType.string, DataType.string], DataType.boolean, Opcode.OPCODE_GREATER_S,
                 lambda a, b: a > b),

        Operator("<", [DataType.integer, DataType.integer], DataType.boolean, Opcode.OPCODE_LESS_I,
                 lambda a, b: a < b),
        Operator("<", [DataType.float, DataType.float], DataType.boolean, Opcode.OPCODE_LESS_F,
                 lambda a, b: a < b),
        Operator("<", [DataType.string, DataType.string], DataType.boolean, Opcode.OPCODE_LESS_S,
                 lambda a, b: a < b),

        Operator(">=", [DataType.integer, DataType.integer], DataType.boolean, Opcode.OPCODE_GREATER_EQUAL_I,
                 lambda a, b: a >= b),
        Operator(">=", [DataType.float, DataType.float], DataType.boolean, Opcode.OPCODE_GREATER_EQUAL_F,
                 lambda a, b: a >= b),
        Operator(">=", [DataType.string, DataType.string], DataType.boolean, Opcode.OPCODE_GREATER_EQUAL_S,
                 lambda a, b: a >= b),

        Operator("<=", [DataType.integer, DataType.integer], DataType.boolean, Opcode.OPCODE_LESS_EQUAL_I,
                 lambda a, b: a <= b),
        Operator("<=", [DataType.float, DataType.float], DataType.boolean, Opcode.OPCODE_LESS_EQUAL_F,
                 lambda a, b: a <= b),
        Operator("<=", [DataType.string, DataType.string], DataType.boolean, Opcode.OPCODE_LESS_EQUAL_S,
                 lambda a, b: a <= b),

        Operator("&", [DataType.boolean, DataType.boolean], DataType.boolean, Opcode.OPCODE_AND,
                 lambda a, b: a and b),
        Operator("|", [DataType.boolean, DataType.boolean], DataType.boolean, Opcode.OPCODE_OR,
                 lambda a, b: a or b),
        Operator("!", [DataType.boolean], DataType.boolean, Opcode.OPCODE_NOT,
                 lambda a: not a),
    ]

    for operator in operators:
        if operator.content == content and operator.operand_types == operand_types:
            return operator

    raise CompilerError(line, column, "No operator math for operator '" + content + "' and data types '" +
                        ",".join(x.name for x in operand_types) + "' (missing cast?)")
