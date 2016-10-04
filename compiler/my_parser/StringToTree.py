from my_parser.CodeBlock import CodeBlock
from my_parser.EvaluationTree import NodeFloat, NodeVariable, NodeMacro, NodeOperator, NodeAssignment, TreeNode, \
    NodeCast, NodeInteger, NodeString, NodeBoolean
from my_parser.Statement import Statement, TokenFloat, TokenIdentifier, TokenOperator, TokenMacro, TokenCast, \
    TokenInteger, TokenString, TokenBoolean
from my_parser.exceptions.compiler_error import CompilerError
from my_parser.scope import Scope


def rpn_to_tree(rpn, scope, code_block: CodeBlock):
    stack = []

    for token in rpn:
        line = code_block.line
        column = code_block.column + 1 + token.column

        if isinstance(token, TokenInteger):
            stack.append(NodeInteger(token.content, line, column))
        elif isinstance(token, TokenFloat):
            stack.append(NodeFloat(token.content, line, column))
        elif isinstance(token, TokenBoolean):
            stack.append(NodeBoolean(token.content, line, column))
        elif isinstance(token, TokenString):
            stack.append(NodeString(token.content, line, column))
        elif isinstance(token, TokenIdentifier):
            stack.append(NodeVariable(token.content, line, column))
            scope.add_variable(token.content)
        elif isinstance(token, TokenCast):
            node = NodeCast(token.content, line, column)
            if len(stack) < 1:
                raise CompilerError(code_block.line, code_block.column + 1, "Cast requires argument")
            node.left = stack.pop()
            stack.append(node)
        elif isinstance(token, TokenMacro):
            node = NodeMacro(token.content, line, column)
            if token.get_arguments_count() >= 1:
                if len(stack) < 1:
                    raise CompilerError(code_block.line, code_block.column + 1, "Macro requires more arguments")
                node.left = stack.pop()
            stack.append(node)
        elif isinstance(token, TokenOperator):
            if token.content == "=":
                node = NodeAssignment(line, column)
            else:
                node = NodeOperator(token.content, line, column)
            if len(stack) < token.get_arguments_count():
                raise CompilerError(code_block.line, code_block.column + 1, "Error in expression")
            if token.get_arguments_count() >= 2:
                node.right = stack.pop()
            if token.get_arguments_count() >= 1:
                node.left = stack.pop()
            stack.append(node)

    if len(stack) != 1:
        raise CompilerError(code_block.line, code_block.column + 1, "Error in expression")

    build_all_nodes(stack[0], scope)

    return stack[0]


def build_all_nodes(root: TreeNode, scope: Scope):
    if root.left is not None:
        build_all_nodes(root.left, scope)
    if root.right is not None:
        build_all_nodes(root.right, scope)

    root.build(scope)


def statement_to_rpn(statement: Statement, code_block: CodeBlock):
    output = []
    stack = []

    for token in statement.tokens:
        if isinstance(token, TokenInteger) \
                or isinstance(token, TokenFloat) \
                or isinstance(token, TokenBoolean) \
                or isinstance(token, TokenString) \
                or isinstance(token, TokenIdentifier):
            output.append(token)
        elif isinstance(token, TokenMacro) or isinstance(token, TokenCast):
            stack.append(token)
        elif isinstance(token, TokenOperator) and token.content == '(':
            stack.append(token)
        elif isinstance(token, TokenOperator) and token.content == ')':
            while len(stack) > 0 and stack[-1].content != '(':
                output.append(stack.pop())
            if len(stack) == 0:
                raise CompilerError(code_block.line, code_block.column + 1, "Error in expression, missing '('")
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
        if output[-1].content == '(':
            raise CompilerError(code_block.line, code_block.column + 1, "Error in expression, missing ')'")

    return output


def string_to_tree(string: str, scope: Scope, code_block: CodeBlock) -> TreeNode:
    s = Statement(string)
    rpn = statement_to_rpn(s, code_block)
    tree = rpn_to_tree(rpn, scope, code_block)
    return tree
