class InternalError(Exception):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return "Internal compiler error: {}".format(self.text)
