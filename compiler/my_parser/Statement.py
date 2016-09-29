class Token:
    pass


class TokenOperator(Token):
    def __init__(self, content: str):
        self.content = content

    def get_priority(self) -> int:
        if self.content == '*' or self.content == '/':
            return 10
        elif self.content == '+' or self.content == '-':
            return 8
        elif self.content == '>' or self.content == '<':
            # greater/less
            return 6
        elif self.content == '=':
            return 4
        elif self.content == '(' or self.content == ')':
            return 2
        else:
            return -1

    def is_right_associative(self) -> bool:
        if self.content == '=':
            return True
        else:
            return False


class TokenInteger(Token):
    def __init__(self, content: int):
        self.content = content


class TokenIdentifier(Token):
    def __init__(self, content: str):
        self.content = content


class TokenMacro(Token):
    def __init__(self, content: str):
        self.content = content
        if content == 'write':
            self.operands = 1
        elif content == 'read' or content == 'exit':
            self.operands = 0


def is_operand(char: str) -> bool:
    return char == '+' \
           or char == '-' \
           or char == '/' \
           or char == '*' \
           or char == '=' \
           or char == '<' \
           or char == '>' \
           or char == '(' \
           or char == ')'


def is_macro(identifier: str) -> bool:
    return identifier == 'write' or identifier == 'read' or identifier == 'exit'


def create_token(string: str) -> Token:
    try:
        return TokenInteger(int(string))
    except ValueError:
        if is_operand(string):
            return TokenOperator(string)
        elif is_macro(string):
            return TokenMacro(string)
        else:
            return TokenIdentifier(string)


def parse_on_tokens(text):
    text = text.strip()

    last_token = ""
    tokens = []

    for char in text:
        if is_operand(char):
            if last_token != "":
                tokens.append(create_token(last_token))
                last_token = ""
            tokens.append(create_token(char))

        elif char == " " or char == "\t":
            if last_token != "":
                tokens.append(create_token(last_token))
                last_token = ""

        else:
            last_token += char

    if last_token != "":
        tokens.append(create_token(last_token))

    return tokens


class Statement:
    def __init__(self, text):
        self.tokens = parse_on_tokens(text)
