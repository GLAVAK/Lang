class Token:
    pass


class TokenOperator(Token):
    def __init__(self, content: str):
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

    def get_priority(self) -> int:
        return 1000  # should be higher than any operator priority

    def get_arguments_count(self):
        if self.content == 'write':
            return 1
        elif self.content == 'read' or self.content == 'exit':
            return 0


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
    elif char == '>' or char == '<'\
            or char == '>=' or char == '<='\
            or char == '==' or char == '!=':
        return 6
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


def is_macro(identifier: str) -> bool:
    return identifier == 'write' or identifier == 'read' or identifier == 'exit'


def create_token(string: str) -> Token:
    try:
        return TokenInteger(int(string))
    except ValueError:
        if is_operator(string):
            return TokenOperator(string)
        elif is_macro(string):
            return TokenMacro(string)
        else:
            return TokenIdentifier(string)


def parse_on_tokens(text):
    text = text.strip()

    last_token = ""
    tokens = []
    # TODO: double chars operators (<= etc)

    num = 0
    while num < len(text):
        if is_operator(text[num:num+2]):
            if last_token != "":
                tokens.append(create_token(last_token))
                last_token = ""
            tokens.append(create_token(text[num:num+2]))
            num += 2

        elif is_operator(text[num]):
            if last_token != "":
                tokens.append(create_token(last_token))
                last_token = ""
            if text[num] == '-' and len(tokens) > 0 and isinstance(tokens[-1], TokenOperator):
                # unary minus
                tokens.append(create_token("#"))
            else:
                tokens.append(create_token(text[num]))
            num += 1

        elif text[num] == " " or text[num] == "\t":
            if last_token != "":
                tokens.append(create_token(last_token))
                last_token = ""
            num += 1

        else:
            last_token += text[num]
            num += 1

    if last_token != "":
        tokens.append(create_token(last_token))

    return tokens


class Statement:
    def __init__(self, text):
        self.tokens = parse_on_tokens(text)
