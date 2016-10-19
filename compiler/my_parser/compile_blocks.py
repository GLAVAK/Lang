from typing import List

from my_parser.bytecode_line import BytecodeLine, ProgramAddressArg
from my_parser.code_block import CodeBlockCondition, CodeBlockStatement, CodeBlock
from my_parser.evaluation_tree import NodeMacro
from my_parser.opcodes import Opcode


def append_jump(final_program: List[BytecodeLine], target: CodeBlock, jump_type: Opcode) -> None:
    push_addr = BytecodeLine(Opcode.OPCODE_PUSH_VAL_I)
    push_addr.args.append(ProgramAddressArg(target))
    final_program.append(push_addr)

    jump = BytecodeLine(jump_type)
    final_program.append(jump)


def compile_blocks(blocks: List[CodeBlock]) -> List[BytecodeLine]:
    """
    Joins all block's bytecode fields into one list, according to their order in that list.
    Adds GOTO's and IF's where required
    :param blocks: List of blocks
    :return: List of BytecodeLines, which represents the program
    """
    final_program = []

    for block_num, block in enumerate(blocks):
        block.bytecode_position = 0
        for bytecode_line in final_program:
            block.bytecode_position += bytecode_line.get_length_in_bytes()

        final_program.extend(block.bytecode)

        if isinstance(block, CodeBlockStatement) and \
                isinstance(block.evaluation_tree, NodeMacro) and \
                        block.evaluation_tree.macro_name == "exit":
            # It's exit block, no further jumps required
            continue

        if isinstance(block, CodeBlockStatement):
            if block_num < len(blocks) - 1 and block.next_block == blocks[block_num + 1]:
                # GOTO isn't required, next block in the graph is next in the bytecode
                continue
            else:
                append_jump(final_program, block.next_block, Opcode.OPCODE_GOTO)
        elif isinstance(block, CodeBlockCondition):
            if block_num < len(blocks) - 1 and block.false_block == blocks[block_num + 1]:
                # GOTO isn't required, false block in the graph is next in the bytecode
                # Only add true conditional jump:
                append_jump(final_program, block.true_block, Opcode.OPCODE_IF)
            elif block_num < len(blocks) - 1 and block.true_block == blocks[block_num + 1]:
                # IF isn't required, true block in the graph is next in the bytecode
                # Invert value and add false conditional jump
                final_program.append(BytecodeLine(Opcode.OPCODE_NOT))
                append_jump(final_program, block.false_block, Opcode.OPCODE_IF)
            else:
                # Just add both conditional jump and GOTO:
                append_jump(final_program, block.true_block, Opcode.OPCODE_IF)
                append_jump(final_program, block.false_block, Opcode.OPCODE_GOTO)

    return final_program
