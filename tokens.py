from dataclasses import dataclass
from enum import Enum

class TokenType(Enum):
    NUMBER = 0
    STRING = 1
    FUNCTION = 2
    BLOCK = 3
    VARIABLE = 4
    FUNCTION_CALL = 5
    VARIABLE_CREATE = 6
    INVOKE = 7
    SEP = 8
    

@dataclass
class Token:
    type: TokenType
    value: any = None

    def _print(self):
        return self.type.name + self.value