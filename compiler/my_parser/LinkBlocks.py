import copy

from my_parser.CodeBlock import CodeBlockStatement, CodeBlockEmpty, MovingDirection
from my_parser.exceptions.internal_error import InternalError


def find_closest_blocks(arrow_start_line, arrow_start_column, arrow_direction, blocks):
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
                    and (best_fit is None or best_fit.column < block.column):
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
                        and (best_fit is None or block.column < best_fit.column):
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


def get_next_block(block, blocks):
    if isinstance(block, CodeBlockStatement) or isinstance(block, CodeBlockEmpty):
        if block.next_blocks[0].is_fall_through_block():
            block.next_blocks[0].ft_block_instantiated = True
            block.next_block = copy.copy(block.next_blocks.pop(0))
            block.next_block.next_blocks = block.next_blocks
            blocks.append(block.next_block)
            get_next_block(block.next_block, blocks)
        else:
            block.next_block = block.next_blocks.pop(0)
    else:
        if block.false_blocks[0].is_fall_through_block():
            block.false_blocks[0].ft_block_instantiated = True
            block.false_block = copy.copy(block.false_blocks.pop(0))
            block.false_block.next_blocks = block.false_blocks
            blocks.append(block.false_block)
            get_next_block(block.false_block, blocks)
        else:
            block.false_block = block.false_blocks.pop(0)

        if block.true_blocks[0].is_fall_through_block():
            block.true_blocks[0].ft_block_instantiated = True
            block.true_block = copy.copy(block.true_blocks.pop(0))
            block.true_block.next_blocks = block.true_blocks
            blocks.append(block.true_block)
            get_next_block(block.true_block, blocks)
        else:
            block.true_block = block.true_blocks.pop(0)


def link_blocks(blocks):
    """
    Links all the blocks to each other, using their coordinates. If any FT blocks found, they are
    instantiated and added to blocks list with proper connections
    :param blocks:
    :return:
    """

    # At first for every block block.next_blocks get filled with fall-through blocks and
    # usual block at the end, and then duplicate fall-through blocks and connect them all properly

    for block in blocks:
        if block.is_fall_through_block():
            continue
        elif isinstance(block, CodeBlockStatement) or isinstance(block, CodeBlockEmpty):
            block.next_blocks = find_closest_blocks(block.line, block.get_arrow_column(), block.direction, blocks)
        else:
            block.false_blocks = \
                find_closest_blocks(block.line, block.column, block.false_direction, blocks)
            block.true_blocks = \
                find_closest_blocks(block.line, block.get_right() - 1, block.true_direction, blocks)

    for block in blocks:
        if block.is_fall_through_block():
            continue
        else:
            get_next_block(block, blocks)
