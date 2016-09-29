from my_parser.CodeBlock import CodeBlockEmpty, CodeBlockStatement, CodeBlockCondition
from my_parser.exceptions.compiler_error import CompilerError


def remove_empty_blocks(blocks):
    """
    Removes empty blocks from given list, keeping the program correct
    Ex:
        [a=1]>  >  >  [write(a)]>
        turns into
        [a=1]>  [write(a)]>
    """
    for block in blocks:
        if isinstance(block, CodeBlockEmpty):
            # We'll remove empty blocks later, after removing their dependencies
            continue
        elif isinstance(block, CodeBlockStatement):
            # TODO: handle cycling (Ex: [a=1]> > < )
            visited_blocks = []
            while isinstance(block.next_block, CodeBlockEmpty):
                block.next_block = block.next_block.next_block
                if block.next_block in visited_blocks:
                    # We have cycle (Ex: [a=1]> > < )
                    raise CompilerError(block.next_block.line, block.next_block.column,
                                        "Cycle in blocks with no content")
                visited_blocks.append(block.next_block)

        elif isinstance(block, CodeBlockCondition):
            # TODO: handle cycling (Ex: [a=1]> > < )
            visited_blocks = []
            while isinstance(block.true_block, CodeBlockEmpty):
                block.true_block = block.true_block.next_block
                if block.true_block in visited_blocks:
                    # We have cycle (Ex: [a=1]> > < )
                    raise CompilerError(block.true_block.line, block.true_block.column,
                                        "Cycle in blocks with no content")
                visited_blocks.append(block.true_block)
            visited_blocks.clear()
            while isinstance(block.false_block, CodeBlockEmpty):
                block.false_block = block.false_block.next_block
                if block.false_block in visited_blocks:
                    # We have cycle (Ex: [a=1]> > < )
                    raise CompilerError(block.false_block.line, block.false_block.column,
                                        "Cycle in blocks with no content")
                visited_blocks.append(block.false_block)

    # And remove empty blocks from list
    blocks[:] = [block for block in blocks if not isinstance(block, CodeBlockEmpty)]
