from my_parser.BytecodeLine import BytecodeLine, ProgramAddressArg
from my_parser.CodeBlock import CodeBlockCondition, CodeBlockStatement, CodeBlockEmpty
from my_parser.Opcodes import Opcode


def compile_blocks(blocks):
    final_program = []

    for block in blocks:
        block.bytecode_position = 0
        for bytecode_line in final_program:
            block.bytecode_position += bytecode_line.get_length_in_bytes()

        if isinstance(block, CodeBlockCondition) or isinstance(block, CodeBlockStatement):
            final_program.extend(block.bytecode)

        if isinstance(block, CodeBlockStatement) or isinstance(block, CodeBlockEmpty):
            # TODO: empty blocks should be removed on optimization stage, not compiled
            block_true_push_addr = BytecodeLine(Opcode.OPCODE_PUSH_VAL)
            block_true_push_addr.args.append(ProgramAddressArg(block.next_block))
            final_program.append(block_true_push_addr)

            block_exit_goto = BytecodeLine(Opcode.OPCODE_GOTO)
            final_program.append(block_exit_goto)
        elif isinstance(block, CodeBlockCondition):
            # if statement is true:
            block_true_push_addr = BytecodeLine(Opcode.OPCODE_PUSH_VAL)
            block_true_push_addr.args.append(ProgramAddressArg(block.true_block))
            final_program.append(block_true_push_addr)

            block_exit_if = BytecodeLine(Opcode.OPCODE_IF)
            final_program.append(block_exit_if)

            # else:
            block_false_push_addr = BytecodeLine(Opcode.OPCODE_PUSH_VAL)
            block_false_push_addr.args.append(ProgramAddressArg(block.false_block))
            final_program.append(block_false_push_addr)

            block_exit_goto = BytecodeLine(Opcode.OPCODE_GOTO)
            final_program.append(block_exit_goto)

    return final_program
