from typing import List

from my_parser.data_type import DataType


class Token:
    def __init__(self, column: int):
        self.column = column  # To show nice compiler errors messages


class TokenOperator(Token):
    def __init__(self, content: str, column: int):
        super().__init__(column)
        self.content = content

    def get_priority(self) -> int:
        return get_operator_priority(self.content)

    def is_right_associative(self) -> bool:
        if self.content == '=' or self.content == '!':
            return True
        else:
            return False

    def get_arguments_count(self):
        if self.content == '!' or self.content == '#':
            # '#' - unary minus
            return 1
        else:
            return 2


class TokenInteger(Token):
    def __init__(self, content: int, column: int):
        super().__init__(column)
        self.content = content


class TokenFloat(Token):
    def __init__(self, content: float, column: int):
        super().__init__(column)
        self.content = content


class TokenBoolean(Token):
    def __init__(self, content: bool, column: int):
        super().__init__(column)
        self.content = content


class TokenString(Token):
    def __init__(self, content: str, column: int):
        super().__init__(column)
        self.content = content


class TokenIdentifier(Token):
    def __init__(self, content: str, column: int):
        super().__init__(column)
        self.content = content


class TokenMacro(Token):
    def __init__(self, content: str, column: int):
        super().__init__(column)
        self.content = content

    def get_priority(self) -> int:
        return 1000  # should be higher than any operator priority

    def get_arguments_count(self):
        if self.content == 'write':
            return 1
        elif self.content == 'read' or self.content == 'exit':
            return 0


class TokenCast(Token):
    def __init__(self, content: str, column: int):
        super().__init__(column)
        if content == "i":
            self.content = DataType.integer
        elif content == "f":
            self.content = DataType.float
        elif content == "s":
            self.content = DataType.string

    def get_priority(self) -> int:
        return 1000  # should be higher than any operator priority


def get_operator_priority(char: str) -> int:
    """
    Used to get operator priority, or to check if char is correct operator
    :param char: Operator
    :return: Operator priority (positive), or -1 if char is not correct operator
    """
    if char == '!' or char == '#':
        # '#' - unary minus
        return 12
    elif char == '*' or char == '/':
        return 10
    elif char == '+' or char == '-':
        return 8
    elif char == '>' or char == '<' \
            or char == '>=' or char == '<=' \
            or char == '==' or char == '!=':
        return 6
    elif char == '&' or char == '|':
        return 5
    elif char == '=':
        return 4
    elif char == '(' or char == ')':
        return 2
    else:
        return -1


def is_operator(char: str) -> bool:
    """
    Used to check if char is correct operator, uses get_operator_priority()
    :param char: Operator
    :return: Is char a correct operator
    """
    return get_operator_priority(char) != -1


def get_cast_function_target_type(char: str) -> DataType:
    if char == "f":
        return DataType.float
    elif char == "i":
        return DataType.integer
    elif char == "s":
        return DataType.string
    else:
        return DataType.undefined


def is_cast_function(char: str) -> bool:
    return get_cast_function_target_type(char) != DataType.undefined


def is_macro(identifier: str) -> bool:
    return identifier == 'write' or identifier == 'read' or identifier == 'exit'


def create_token(string: str, column: int) -> Token:
    if string == "true":
        return TokenBoolean(True, column)
    elif string == "false":
        return TokenBoolean(False, column)
    else:
        try:
            return TokenInteger(int(string), column)
        except ValueError:
            try:
                return TokenFloat(float(string), column)
            except ValueError:
                if is_operator(string):
                    return TokenOperator(string, column)
                elif is_macro(string):
                    return TokenMacro(string, column)
                elif is_cast_function(string):
                    return TokenCast(string, column)
                else:
                    return TokenIdentifier(string, column)


def parse_on_tokens(text: str) -> List[Token]:
    text = text.strip()

    last_token = ""
    tokens = []

    num = 0
    is_string_literal = False
    while num < len(text):
        if is_string_literal:
            if text[num] == '"':
                is_string_literal = False
                tokens.append(TokenString(last_token, num))
                last_token = ""
            else:
                last_token += text[num]
            num += 1

        elif text[num] == '"':
            is_string_literal = True
            if last_token != "":
                tokens.append(create_token(last_token, num))
                last_token = ""
            num += 1

        elif is_operator(text[num:num + 2]):
            if last_token != "":
                tokens.append(create_token(last_token, num))
                last_token = ""
            tokens.append(create_token(text[num:num + 2], num))
            num += 2

        elif is_operator(text[num]):
            if last_token != "":
                tokens.append(create_token(last_token, num))
                last_token = ""
            if text[num] == '-' and len(tokens) > 0 and isinstance(tokens[-1], TokenOperator):
                # unary minus
                tokens.append(create_token("#", num))
            else:
                tokens.append(create_token(text[num], num))
            num += 1

        elif text[num] == " " or text[num] == "\t":
            if last_token != "":
                tokens.append(create_token(last_token, num))
                last_token = ""
            num += 1

        else:
            last_token += text[num]
            num += 1

    if last_token != "":
        tokens.append(create_token(last_token, num))

    return tokens


class Statement:
    def __init__(self, text):
        self.tokens = parse_on_tokens(text)
