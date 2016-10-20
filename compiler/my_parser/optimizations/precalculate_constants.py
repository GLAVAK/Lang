from my_parser.data_type import DataType
from my_parser.evaluation_tree import TreeNode, NodeOperator, NodeCast, NodeInteger, NodeFloat, NodeBoolean, NodeString
from my_parser.exceptions.internal_error import InternalError
from my_parser.scope import Scope


def get_constant_of_type(value, result_type: DataType, line: int, column: int) -> TreeNode:
    if result_type is DataType.integer:
        return NodeInteger(int(value), line, column)
    if result_type is DataType.float:
        return NodeFloat(float(value), line, column)
    if result_type is DataType.boolean:
        return NodeBoolean(value, line, column)
    if result_type is DataType.string:
        if isinstance(value, float):
            new_value = "{:.6f}".format(value)  # Needs to be the same format as conversion by vm
        else:
            new_value = str(value)
        return NodeString(new_value, line, column)

    raise InternalError("get_constant_of_type on undefined type")


def precalculate_constants(tree: TreeNode, scope: Scope) -> TreeNode:
    """
    Precalculates all constant sub-expressions in an evaluation tree
    :param tree:
    :param scope: Used to define variable types
    :returns New root of a tree
    """

    if tree.left is not None:
        tree.left = precalculate_constants(tree.left, scope)
    if tree.right is not None:
        tree.right = precalculate_constants(tree.right, scope)

    if isinstance(tree, NodeOperator) and tree.left.is_constant() and \
            (tree.right is None or tree.right.is_constant()):
        operator_info = tree.get_operator(scope)

        if tree.right is None:
            result_constant = operator_info.calculate_function(tree.left.value)
        else:
            result_constant = operator_info.calculate_function(tree.left.value, tree.right.value)

        return get_constant_of_type(result_constant, tree.get_return_type(scope), tree.line, tree.column)

    elif isinstance(tree, NodeCast) and tree.left.is_constant():
        return get_constant_of_type(tree.left.value, tree.get_return_type(scope), tree.line, tree.column)

    else:
        return tree
