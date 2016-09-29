class CompilerWarning(Exception):
    def __init__(self, line, column, text):
        self.line = line
        self.column = column
        self.text = text

    def __str__(self):
        return "Warning ({}:{}) {}".format(self.line, self.column, self.text)
