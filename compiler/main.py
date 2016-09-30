from my_parser.CodeBlock import CodeBlockCondition, CodeBlockStatement
from my_parser.CompileBlocks import compile_blocks
from my_parser.LinkBlocks import link_blocks
from my_parser.SimpleOptimizations import remove_empty_blocks
from my_parser.TextToBlocks import text_to_block

# First, read all blocks from file, define their types (Empty, Statement, Condition),
# direction to the next block, it's position in the world, and also parse the text in
# the block to EvaluationTree using string_to_tree() function. It also fills name_table
# for us, which contains var's names and their positions in memory
names_table = {}
blocks = text_to_block(open("code_examples/unary.txt"), names_table)

# Then connect all the blocks to each other, using their next block direction and
# position, and save this information in the next_block field
link_blocks(blocks)

# Remove empty blocks, keeping connections correct
remove_empty_blocks(blocks)

# Get actual list of opcodes for each block, and store it in it's bytecode field (without
# GOTO's and IF's yet)
for block in blocks:
    if isinstance(block, CodeBlockCondition) or isinstance(block, CodeBlockStatement):
        block.bytecode = block.evaluation_tree.get_byte_code(names_table)

# here goes optimizations that can change bytecode length

# TODO: sort the graph here, to minimize GOTO's count

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
file = open("../program", "wb")
for bytecode_line in final_program:
    bytecode_line.pack(file)

# TODO: figure out how to call files, functions and classes to avoid import conflicts

print("Compilation successful")
