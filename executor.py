import enum
from tokens import Token, TokenType
import string
import pickle

IGNORE = ' \n\t\r'
DIGITS = '0123456789'
ASCII = string.ascii_letters

functions = []
vars = {}

class Function:
    def __init__(self, name:str, args:list, consumer:Token):
        self.consumer = consumer
        self.args = args
        self.name = name

    def call(self, argss):
        enm = []
        for i, arg in enumerate(self.args):
            if i < len(argss):
                arg2 = argss[i]
            else:
                arg2 = None
            enm.append(Token(TokenType.VARIABLE_CREATE, value=arg.value))
            enm.append(arg2)

        enm.append(self.consumer)
        return Executor(enm).parse()

class InbuiltFunction(Function):
    def __init__(self, name:str, args:list, consumer:str):
        self.name = name
        self.args = args
        self.consumer = consumer

    def call(self, argss):
        self.returner = None
        ss = ""
        for a, arg in enumerate(argss):
            kms = self.args[a]
            value = None
            if arg.type == TokenType.VARIABLE:
                value = vars[arg.value].value
            else:
                value = arg.value
            value = value.replace('\"', '\\\"')
            ss += f"{kms} = \"{value}\"\n"
        
        self.returner = None

        def fnc_returns(objec):
            self.returner = objec
        
        exec(ss + self.consumer)

        return self.returner

functions.append(InbuiltFunction(name="print", args=["vallue"], consumer="print(vallue)"))
functions.append(InbuiltFunction(name="pycall", args=["vallue"], consumer="exec(vallue)"))
functions.append(InbuiltFunction(name="puts", args=["chrr"], consumer="fnc_returns(chrr)"))
functions.append(InbuiltFunction(name='sys', args=['cmd'], consumer="__import__('os').system(cmd)"))
functions.append(InbuiltFunction(name="http_get", args=["uri"], consumer="fnc_returns(__import__('requests').get(uri).text)"))
functions.append(InbuiltFunction(name="strepl", args=['s', 'targ', 'value'], consumer="fnc_returns(s.replace(targ, value))"))
functions.append(InbuiltFunction(name="strcat", args=['a', 'b'], consumer="fnc_returns(a + b)"))

class Executor:
    def __init__(self, prgm):
        self.lst = iter(prgm)
        self.raw = prgm
        self.index = 0
        self.token:Token = None
        self.advance()

    def advance(self):
        try:
            self.index += 1
            self.token = next(self.lst)
        except StopIteration:
            self.token = None

    def parse(self):
        outte = None
        while self.token != None:
            match self.token.type:
                case TokenType.NUMBER:
                    pass
                case TokenType.STRING:
                    pass
                case TokenType.FUNCTION:
                    fdec = self.token.value
                    functions.append(Function(fdec['name'].strip(), fdec['args'], self.raw[self.index]))
                    self.advance()
                case TokenType.BLOCK:
                    block = self.token.value
                    Executor(block).parse()
                case TokenType.VARIABLE:
                    pass
                case TokenType.FUNCTION_CALL:
                    dup = self.token.value
                    for func in functions:
                        if func.name == dup['name']:
                            outte = func.call(dup['args'])
                            if outte != None:
                                token = self.raw[self.index - 2]
                                if token.type == TokenType.VARIABLE:
                                    vars[token.value] = Token(TokenType.STRING, value=outte)
                case TokenType.VARIABLE_CREATE:
                    dup = self.token.value
                    vars[dup] = self.raw[self.index]
                    self.advance()
                case TokenType.INVOKE:
                    pass

                case TokenType.SEP:
                    pass
            self.advance()
        return outte

with open("test.wbin", "rb") as f:
    program = pickle.load(f)
    Executor(program).parse()
