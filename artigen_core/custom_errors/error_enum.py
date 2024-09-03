from enum import Enum

class ErrorCode(Enum):

    def __init__(self, code, message):
        self.code = code
        self.message = message


