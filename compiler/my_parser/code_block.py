from enum import Enum


class MovingDirection(Enum):
    undefined = 0
    right = 1
    up = 2
    left = 3
    down = 4


class CodeBlock:
    def __init__(self, line, column):
        self.line = line
        self.column = column

        self.width = 2
        self.bytecode = []
        self.bytecode_position = -1

    def get_right(self) -> int:
        return self.column + self.width

    def get_arrow_column(self) -> int:
        return self.column

    def is_fall_through_block(self) -> bool:
        return False


class CodeBlockEmpty(CodeBlock):
    def __init__(self, line, column):
        super().__init__(line, column)

        self.width = 1
        self.direction = MovingDirection.undefined

        self.is_arrow_on_right = False

        self.next_blocks = []
        self.next_block = None

    def get_arrow_column(self) -> int:
        if self.is_arrow_on_right:
            return self.column + self.width - 1
        else:
            return self.column


class CodeBlockStatement(CodeBlock):
    def __init__(self, line, column):
        super().__init__(line, column)

        self.direction = MovingDirection.undefined

        # If it's FT block, and this set to false, generate unreachable block warning:
        self.ft_block_instantiated = False

        self.next_blocks = []
        self.next_block = None
        self.is_arrow_on_right = False
        self.evaluation_tree = None

    def get_arrow_column(self) -> int:
        if self.is_arrow_on_right:
            return self.column + self.width - 1
        else:
            return self.column

    def is_fall_through_block(self) -> bool:
        return self.direction == MovingDirection.undefined


class CodeBlockCondition(CodeBlock):
    def __init__(self, line, column):
        super().__init__(line, column)

        self.true_blocks = []
        self.false_blocks = []
        self.false_direction = MovingDirection.left
        self.true_direction = MovingDirection.right
        self.false_block = None
        self.true_block = None
        self.evaluation_tree = None
