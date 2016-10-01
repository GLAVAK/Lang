from my_parser.BytecodeLine import BytecodeLine, ProgramAddressArg
from my_parser.CodeBlock import CodeBlockCondition, CodeBlockStatement, CodeBlock
from my_parser.Opcodes import Opcode


def append_jump(final_program, target: CodeBlock, type: Opcode):
    push_addr = BytecodeLine(Opcode.OPCODE_PUSH_VAL)
    push_addr.args.append(ProgramAddressArg(target))
    final_program.append(push_addr)

    jump = BytecodeLine(type)
    final_program.append(jump)


def compile_blocks(blocks):
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
