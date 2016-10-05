from my_parser.CodeBlock import CodeBlockEmpty, CodeBlockStatement, CodeBlockCondition, MovingDirection
from my_parser.StringToTree import string_to_tree
from my_parser.exceptions.compiler_error import CompilerError
from my_parser.scope import Scope


def is_direction_char(char: str) -> bool:
    return char_to_direction(char) is not None


def char_to_direction(char: str) -> MovingDirection:
    if char == '>':
        return MovingDirection.right
    elif char == '^':
        return MovingDirection.up
    elif char == '<':
        return MovingDirection.left
    elif char == 'v' or char == 'V':
        return MovingDirection.down
    else:
        return None


# TODO: too long function, a bit of refactoring would be nice
def text_to_block(file, scope: Scope):
    """
    Parses all blocks from code file, without linking them to each other
    :param file: file from where to read code
    :param scope: scope, which will be filled with var's names and their
                       positions in memory
    :return: list of blocks in code
    """

    # Add block to the beginning of program, to define initial position and direction
    starting_block = CodeBlockEmpty(1, 0)
    starting_block.direction = MovingDirection.right

    blocks = [starting_block]

    for line_num, line in enumerate(file, 1):

        current_block = None
        block_content = ""
        empty_block = None  # to process "<" blocks

        previous_char = None  # to process "<[a = 1]" blocks
        previous_block = None  # to process "[a = 1]>" blocks

        for column_num, char in enumerate(line, 1):

            if (char == '[' or char == '{') and current_block is None:
                # block started:

                if char == '[':
                    current_block = CodeBlockStatement(line_num, column_num)
                else:
                    current_block = CodeBlockCondition(line_num, column_num)

                if previous_char is not None:
                    # "<[a = 1]" situation

                    current_block.column -= 1
                    current_block.width += 1

                    if char == '[':
                        current_block.direction = char_to_direction(previous_char)
                    else:
                        current_block.false_direction = char_to_direction(previous_char)

                    empty_block = None

            elif char == ']' or char == '}':
                # block ended:

                current_block.width += len(block_content)

                if char == ']' and isinstance(current_block, CodeBlockStatement):
                    current_block.evaluation_tree = string_to_tree(block_content, scope, current_block)
                elif char == '}' and isinstance(current_block, CodeBlockCondition):
                    current_block.evaluation_tree = string_to_tree(block_content, scope, current_block)

                blocks.append(current_block)
                previous_block = current_block
                current_block = None
                block_content = ""

            elif current_block is not None:
                # reading block content:

                block_content += char

            else:
                if empty_block is not None:
                    empty_block.direction = char_to_direction(previous_char)
                    blocks.append(empty_block)
                    empty_block = None

                if is_direction_char(char):
                    previous_char = char
                    if previous_block is not None:
                        # "[a = 1]>" situation

                        previous_block.width += 1
                        if isinstance(previous_block, CodeBlockStatement):
                            previous_block.direction = char_to_direction(char)
                            previous_block.is_arrow_on_right = True
                        elif isinstance(previous_block, CodeBlockCondition):
                            previous_block.true_direction = char_to_direction(char)
                    else:
                        # " <?" situation
                        # create empty_block, in case there are no '[' or "{" after
                        empty_block = CodeBlockEmpty(line_num, column_num)
                elif char != ' ' and char != '\n':
                    raise CompilerError(line_num, column_num, "Unknown char outside of a block")

                previous_block = None

        if current_block is not None:
            raise CompilerError(line_num, current_block.column, "Block not closed, but end of line reached")

        if empty_block is not None:
            empty_block.direction = char_to_direction(previous_char)
            blocks.append(empty_block)

    return blocks
