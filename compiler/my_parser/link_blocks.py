import copy
from typing import List

from my_parser.code_block import CodeBlockStatement, CodeBlockEmpty, MovingDirection, CodeBlock, CodeBlockCondition
from my_parser.exceptions.internal_error import InternalError


def find_closest_blocks(arrow_start_line: int, arrow_start_column: int,
                        arrow_direction: MovingDirection, blocks: List[CodeBlock]) -> List[CodeBlock]:
    """
    Raycasts ray from given point to given direction, starting from another side, if
    necessary (snake game-like topology), and returns hit block
    :param arrow_start_line:
    :param arrow_start_column:
    :param arrow_direction:
    :param blocks:
    :return: Hit block
    """
    best_fit = None

    for block in blocks:
        if arrow_direction == MovingDirection.right:
            if arrow_start_line == block.line \
                    and arrow_start_column < block.column \
                    and (best_fit is None or block.column < best_fit.column):
                best_fit = block
        elif arrow_direction == MovingDirection.up:
            if block.column <= arrow_start_column < block.get_right() \
                    and block.line < arrow_start_line \
                    and (best_fit is None or best_fit.line < block.line):
                best_fit = block
        elif arrow_direction == MovingDirection.left:
            if arrow_start_line == block.line \
                    and block.column < arrow_start_column \
                    and (best_fit is None or best_fit.column < block.column) \
                    and block.column > 0:  # column > 0 not to hit starting_block (see text_to_block())
                best_fit = block
        elif arrow_direction == MovingDirection.down:
            if block.column <= arrow_start_column < block.get_right() \
                    and arrow_start_line < block.line \
                    and (best_fit is None or block.line < best_fit.line):
                best_fit = block

    if best_fit is None:
        # Cycle from side of the field (like in snake game)
        for block in blocks:
            if arrow_direction == MovingDirection.right:
                if arrow_start_line == block.line \
                        and (best_fit is None or block.column < best_fit.column) \
                        and block.column > 0:  # column > 0 not to hit starting_block (see text_to_block())
                    best_fit = block
            elif arrow_direction == MovingDirection.up:
                if block.column <= arrow_start_column < block.get_right() \
                        and (best_fit is None or best_fit.line < block.line):
                    best_fit = block
            elif arrow_direction == MovingDirection.left:
                if arrow_start_line == block.line \
                        and (best_fit is None or best_fit.column < block.column):
                    best_fit = block
            elif arrow_direction == MovingDirection.down:
                if block.column <= arrow_start_column < block.get_right() \
                        and (best_fit is None or block.line < best_fit.line):
                    best_fit = block

    if best_fit is None:
        raise InternalError("Block arrow points to no block, when it should at least point at the same block")

    result = [best_fit]
    if best_fit.is_fall_through_block():
        if arrow_direction == MovingDirection.left or arrow_direction == MovingDirection.right:
            result.extend(find_closest_blocks(arrow_start_line, best_fit.column, arrow_direction, blocks))
        else:
            result.extend(find_closest_blocks(best_fit.line, arrow_start_column, arrow_direction, blocks))

    return result


def get_next_block(next_blocks: List[CodeBlock], blocks: List[CodeBlock]) -> CodeBlock:
    """
    Pops block from next_blocks, instantiates it correctly adding to blocks if FT block,
    and returns it
    :param next_blocks:
    :param blocks: Instantiated FT blocks will be added to blocks
    :return:
    """
    if isinstance(next_blocks[0], CodeBlockStatement) and next_blocks[0].is_fall_through_block():
        next_blocks[0].ft_block_instantiated = True
        next_block = copy.copy(next_blocks.pop(0))
        # Put random moving direction, for their is_fall_through_block method to return false
        next_block.direction = MovingDirection.left
        next_block.next_blocks = next_blocks
        blocks.append(next_block)
        return next_block
    else:
        return next_blocks.pop(0)


def calculate_next_block(block: CodeBlock, blocks: List[CodeBlock]) -> None:
    """
    Sets next_block field for Statement or Empty block, or false_block and true_block
    fields for Condition block, taking first block from next_blocks field
    :param block:
    :param blocks: Instantiated FT blocks will be added to blocks
    """
    if isinstance(block, CodeBlockStatement) or isinstance(block, CodeBlockEmpty):
        block.next_block = get_next_block(block.next_blocks, blocks)
    elif isinstance(block, CodeBlockCondition):
        block.false_block = get_next_block(block.false_blocks, blocks)
        block.true_block = get_next_block(block.true_blocks, blocks)


def link_blocks(blocks: List[CodeBlock]) -> None:
    """
    Links all the blocks to each other, using their coordinates. If any FT blocks found, they are
    instantiated and added to blocks list with proper connections
    :param blocks:
    """

    # At first for every block block.next_blocks get filled with fall-through blocks and
    # usual block at the end, and then duplicate fall-through blocks and connect them all properly

    for block in blocks:
        if block.is_fall_through_block():
            continue
        elif isinstance(block, CodeBlockStatement) or isinstance(block, CodeBlockEmpty):
            block.next_blocks = find_closest_blocks(block.line, block.get_arrow_column(), block.direction, blocks)
        elif isinstance(block, CodeBlockCondition):
            block.false_blocks = \
                find_closest_blocks(block.line, block.column, block.false_direction, blocks)
            block.true_blocks = \
                find_closest_blocks(block.line, block.get_right() - 1, block.true_direction, blocks)

    block_num = 0
    while block_num < len(blocks):
        if blocks[block_num].is_fall_through_block():
            pass
        else:
            calculate_next_block(blocks[block_num], blocks)
        block_num += 1
