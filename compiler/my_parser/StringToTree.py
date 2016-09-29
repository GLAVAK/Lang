from my_parser.CodeBlock import CodeBlock
from my_parser.EvaluationTree import NodeConstant, NodeVariable, NodeMacro, NodeOperator, NodeAssignment, TreeNode
from my_parser.Statement import Statement, TokenInteger, TokenIdentifier, TokenOperator, TokenMacro
from my_parser.exceptions.compiler_error import CompilerError


def rpn_to_tree(rpn, name_table, code_block: CodeBlock):
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
                if len(stack) < 1:
                    raise CompilerError(code_block.line, code_block.column + 1, "Error in expression")
                node.left = stack.pop()
            stack.append(node)
        elif isinstance(token, TokenOperator):
            if token.content == "=":
                node = NodeAssignment()
            else:
                node = NodeOperator(token.content)
            if len(stack) < 2:
                raise CompilerError(code_block.line, code_block.column + 1, "Error in expression")
            node.right = stack.pop()
            node.left = stack.pop()
            stack.append(node)

    if len(stack) != 1:
        raise CompilerError(code_block.line, code_block.column + 1, "Error in expression")

    return stack[0]


def statement_to_rpn(statement: Statement, code_block: CodeBlock):
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


def string_to_tree(string: str, name_table, code_block: CodeBlock) -> TreeNode:
    s = Statement(string)
    rpn = statement_to_rpn(s, code_block)
    tree = rpn_to_tree(rpn, name_table, code_block)
    return tree
