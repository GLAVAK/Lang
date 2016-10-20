import sys

from my_parser.check_errors import check_errors
from my_parser.code_block import CodeBlockCondition, CodeBlockStatement
from my_parser.compile_blocks import compile_blocks
from my_parser.link_blocks import link_blocks
from my_parser.optimizations.precalculate_constants import precalculate_constants
from my_parser.optimizations.remove_empty_blocks import remove_empty_blocks
from my_parser.optimizations.sort_blocks import sort_blocks
from my_parser.scope import Scope
from my_parser.text_to_blocks import text_to_block

scope = Scope()
blocks = text_to_block(open(sys.argv[1]), scope)

# Then connect all the blocks to each other, using their next block direction and
# position, and save this information in the next_block field
link_blocks(blocks)

check_errors(blocks, scope)

# Remove empty blocks, keeping connections correct
remove_empty_blocks(blocks)

# Get actual list of opcodes for each block, and store it in it's bytecode field (without
# GOTO's and IF's yet)
for block in blocks:
    block.evaluation_tree = precalculate_constants(block.evaluation_tree, scope)
    block.bytecode = block.evaluation_tree.get_byte_code(scope)

# Reorder blocks for least possible amount of jumps
sort_blocks(blocks, scope)

# Put all blocks to the final program, and define their position in there. GOTO's are put
# in the end of each block, but with auto addresses (ProgramAddressArg which points to the
# block we want to GO TO)
final_program = compile_blocks(blocks)

num = 0
for bytecode_line in final_program:
    print(num, bytecode_line)
    num += bytecode_line.get_length_in_bytes()

# Open file and write all bytecode lines (ops) to it. The ProgramAddressArg will take required
# address automatically, based on block.bytecode_position
file = open(sys.argv[2], "wb")
for bytecode_line in final_program:
    bytecode_line.pack(file)

if len(scope.warnings) > 0:
    print("Warnings:")
    for warning in scope.warnings:
        print(warning)
else:
    print("Compilation successful with no warnings")
