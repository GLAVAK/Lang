class CompilerWarning(Exception):
    def __init__(self, line: int, column: int, text: str):
        self.line = line
        self.column = column
        self.text = text

    def __str__(self) -> str:
        return "Warning ({}:{}) {}".format(self.line, self.column, self.text)
