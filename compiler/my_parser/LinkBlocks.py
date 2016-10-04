from my_parser.CodeBlock import CodeBlockStatement, CodeBlockEmpty, MovingDirection
from my_parser.exceptions.internal_error import InternalError


def find_closest_block(arrow_start_line, arrow_start_column, arrow_direction, blocks):
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

    return best_fit


def link_blocks(blocks):
    """
    Links all the blocks to each other, using their coordinates
    :param blocks:
    :return:
    """
    for block in blocks:
        if isinstance(block, CodeBlockStatement) or isinstance(block, CodeBlockEmpty):
            block.next_block = find_closest_block(block.line, block.get_arrow_column(), block.direction, blocks)
        else:
            block.false_block = \
                find_closest_block(block.line, block.column, block.false_direction, blocks)
            block.true_block = \
                find_closest_block(block.line, block.get_right() - 1, block.true_direction, blocks)
