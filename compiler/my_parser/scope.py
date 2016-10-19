from my_parser.variable import Variable


class Scope:
    def __init__(self):
        self.names_table = {}
        self.warnings = []

    def add_variable(self, name: str) -> None:
        if name not in self.names_table:
            self.names_table[name] = Variable(name, len(self.names_table))
