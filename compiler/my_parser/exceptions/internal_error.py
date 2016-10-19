class InternalError(Exception):
    def __init__(self, text: str):
        self.text = text

    def __str__(self) -> str:
        return "Internal compiler error: {}".format(self.text)
