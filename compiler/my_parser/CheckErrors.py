from my_parser.CodeBlock import CodeBlockCondition
from my_parser.data_type import DataType
from my_parser.exceptions.compiler_error import CompilerError
from my_parser.scope import Scope


def check_errors(blocks, scope: Scope):
    """
    Checks for compiler errors, such as:
     - not boolean in condition
     - never assigned variables
    :param blocks:
    :param scope:
    """
    for var in scope.names_table.values():
        if var.type is DataType.undefined:
            raise CompilerError(None, None,
                                "Variable '" + var.name + "' is used but never assigned (can't define type)")

    for block in blocks:
        if isinstance(block, CodeBlockCondition) and \
                        block.evaluation_tree.get_return_type(scope) is not DataType.boolean:
            raise CompilerError(block.line, block.column + 2,
                                "Statement inside conditional block returns " +
                                block.evaluation_tree.get_return_type(scope).name + ", not boolean")
