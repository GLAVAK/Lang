class CompilerError(Exception):
    def __init__(self, line: int, column: int, text: str):
        self.line = line
        self.column = column
        self.text = text

    def __str__(self) -> str:
        if self.column is None:
            return "Error (line {}) {}".format(self.line, self.text)
        else:
            return "Error ({}:{}) {}".format(self.line, self.column, self.text)
