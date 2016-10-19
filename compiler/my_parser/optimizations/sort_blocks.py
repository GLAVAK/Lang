from enum import Enum
from typing import List

from my_parser.code_block import CodeBlockStatement, CodeBlockCondition, CodeBlock
from my_parser.exceptions.compiler_warning import CompilerWarning
from my_parser.scope import Scope


class BlockColor(Enum):
    White = 0
    Gray = 1
    Black = 2


def sort_blocks_for_block(block: CodeBlock, stack: List[CodeBlock]) -> None:
    block.color = BlockColor.Gray

    if isinstance(block, CodeBlockStatement) and block.next_block.color == BlockColor.White:
        sort_blocks_for_block(block.next_block, stack)
    elif isinstance(block, CodeBlockCondition):
        if block.false_block.color == BlockColor.White:
            sort_blocks_for_block(block.false_block, stack)
        if block.true_block.color == BlockColor.White:
            sort_blocks_for_block(block.true_block, stack)

    stack.append(block)
    block.color = BlockColor.Black


def sort_blocks(blocks: List[CodeBlock], scope: Scope) -> None:
    """
    Topologically sorts blocks in given list, removing unreachable ones, and sorting reachable
    so that next block goes, when possible, right after previous, to minimize GOTO's around the
    program
    :param blocks: List to sort
    :param scope: Used for throwing warnings
    """
    stack = []

    for block in blocks:
        block.color = BlockColor.White

    # Start with only 1st block, because we don't care about blocks unreachable from entry
    # point, which will be deleted from program
    sort_blocks_for_block(blocks[0], stack)

    for block in blocks:
        if block not in stack and not (isinstance(block, CodeBlockStatement) and block.ft_block_instantiated):
            scope.warnings.append(CompilerWarning(block.line, block.column,
                                                  "Unreachable block found"))

    # Clear blocks, as all reachable blocks is in the stack
    blocks[:] = []

    stack.reverse()
    blocks[:] = stack
