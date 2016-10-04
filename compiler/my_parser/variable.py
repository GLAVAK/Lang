from my_parser.data_type import DataType


class Variable:
    def __init__(self, name: str, address: int):
        self.address = address
        self.name = name
        self.type = DataType.undefined
