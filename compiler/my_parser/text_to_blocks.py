from typing import List

from my_parser.code_block import CodeBlockEmpty, CodeBlockStatement, CodeBlockCondition, MovingDirection, CodeBlock
from my_parser.exceptions.compiler_error import CompilerError
from my_parser.exceptions.compiler_warning import CompilerWarning
from my_parser.scope import Scope
from my_parser.string_to_tree import string_to_tree


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
def text_to_block(file, scope: Scope) -> List[CodeBlock]:
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

        is_in_comment = False

        for column_num, char in enumerate(line, 1):

            if char == '\t':
                raise CompilerError(line_num, column_num, "Tabulation character. Please replace it with spaces "
                                                          "for proper code align")

            if char == '/' and current_block is None:
                is_in_comment = not is_in_comment
                continue

            if is_in_comment:
                continue

            elif (char == '[' or char == '{') and current_block is None:
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
                    if block_content.strip() == "":
                        new_block = CodeBlockEmpty(current_block.line, current_block.column)

                        new_block.direction = current_block.direction
                        new_block.width = current_block.width
                        new_block.is_arrow_on_right = current_block.is_arrow_on_right

                        current_block = new_block
                    else:
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
                        if isinstance(previous_block, CodeBlockStatement) or isinstance(previous_block, CodeBlockEmpty):
                            if previous_block.direction != MovingDirection.undefined:
                                raise CompilerError(line_num, column_num, "Block has two directional symbols")
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

        if is_in_comment:
            scope.warnings.append(
                CompilerWarning(line_num, len(line) - 1, "Comment block not closed to the end of the line"))

        if empty_block is not None:
            empty_block.direction = char_to_direction(previous_char)
            blocks.append(empty_block)

    return blocks
