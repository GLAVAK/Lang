from my_parser.EvaluationTree import NodeConstant, NodeVariable, NodeMacro, NodeOperator, NodeAssignment, TreeNode
from my_parser.Statement import Statement, TokenInteger, TokenIdentifier, TokenOperator, TokenMacro


def rpn_to_tree(rpn, name_table):
    stack = []

    for token in rpn:
        if isinstance(token, TokenInteger):
            stack.append(NodeConstant(token.content))
        elif isinstance(token, TokenIdentifier):
            stack.append(NodeVariable(token.content))
            if token.content not in name_table:
                name_table[token.content] = len(name_table)
        elif isinstance(token, TokenMacro):
            node = NodeMacro(token.content)
            if token.operands >= 1:
                node.left = stack.pop()
            stack.append(node)
        elif isinstance(token, TokenOperator):
            if token.content == "=":
                node = NodeAssignment()
            else:
                node = NodeOperator(token.content)
            node.right = stack.pop()
            node.left = stack.pop()
            stack.append(node)

    assert len(stack) == 1
    return stack[0]


def statement_to_rpn(statement: Statement):
    output = []
    stack = []

    for token in statement.tokens:
        if isinstance(token, TokenInteger) or isinstance(token, TokenIdentifier):
            output.append(token)
        elif isinstance(token, TokenMacro):
            stack.append(token)
        elif isinstance(token, TokenOperator) and token.content == '(':
            stack.append(token)
        elif isinstance(token, TokenOperator) and token.content == ')':
            while stack[-1].content != '(':
                output.append(stack.pop())
            stack.pop()  # Pop "("
        elif isinstance(token, TokenOperator):
            if token.is_right_associative():
                while len(stack) > 0 and token.get_priority() < stack[-1].get_priority():
                    output.append(stack.pop())
            else:
                while len(stack) > 0 and token.get_priority() <= stack[-1].get_priority():
                    output.append(stack.pop())
            stack.append(token)

    while len(stack) > 0:
        output.append(stack.pop())

    return output


def string_to_tree(string: str, name_table) -> TreeNode:
    s = Statement(string)
    rpn = statement_to_rpn(s)
    tree = rpn_to_tree(rpn, name_table)
    return tree
