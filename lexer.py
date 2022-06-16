from tokens import *
import string

IGNORE = ' \n\t\r'
DIGITS = '0123456789'
ASCII = string.ascii_letters

class Lexer:
    def __init__(self, text):
        self.text = iter(text)
        self.raw = text
        self.index = 0
        self.advance()

    def advance(self):
        try:
            self.index += 1
            self.char = next(self.text)
        except StopIteration:
            self.char = None

    def parse(self):
        while self.char != None:
            if self.char in IGNORE:
                self.advance()
            elif self.char == '.' or self.char in DIGITS:
                yield self.buildNumber()
            elif self.char == "\"":
                yield self.buildString()
            elif self.raw[self.index-1:self.index + 2] == "fnc":
                self.advance()
                self.advance()
                self.advance()
                yield self.buildFunction()
            elif self.char == "{":
                yield self.buildCodeBlock()
            elif self.char == ":":
                self.advance()
                yield self.buildFunctionCall()
            elif self.char == "$":
                self.advance()
                yield self.buildVar()
            elif self.char == "#":
                self.advance()
                for token in self.preProcess():
                    yield token
            elif self.char == ";":
                self.advance()
                yield Token(TokenType.SEP)

            else:
                raise Exception(f"Illegal Token '{self.char}'")
    
    def preProcess(self):
        keyword = ""

        while self.char not in IGNORE:
            keyword += self.char
            self.advance()
        
        if keyword == "include":
            modname = ""
            self.advance()
            while self.char not in IGNORE:
                modname += self.char
                self.advance()
            with open(modname) as f:
                c = f.read()
                l = Lexer(c)
                t = l.parse()
                ll = list(t)
                return ll




    def buildFunctionCall(self):
        name = ""
        args = ""
        parsingquote = False


        while True:
            if parsingquote == False:
                if self.char == "(":
                    break
            if self.char == "\"":
                parsingquote = not parsingquote
            name += self.char
            self.advance()
        
        self.advance()

        while True:
            if parsingquote == False:
                if self.char == ")":
                    break
            if self.char == "\"":
                parsingquote = not parsingquote
            args += self.char
            self.advance()

        self.advance()

        tokens = list(Lexer(args.replace(",", " ")).parse())

        return Token(TokenType.FUNCTION_CALL, {"name":name, "args":tokens})

    def buildVar(self):
        name = ""

        while True:
            if self.char == "=":
                self.advance()
                return Token(TokenType.VARIABLE_CREATE, name)
            if self.char in IGNORE:
                self.advance()
                return Token(TokenType.VARIABLE, name)
            if not self.char in ASCII:
                self.advance()
                return Token(TokenType.VARIABLE, name)
            name += self.char
            self.advance()

    def buildCodeBlock(self):
        self.advance()
        block = ""

        while self.char != "}" and self.char != None:
            block += self.char
            self.advance()

        tokens = list(Lexer(block).parse())

        self.advance()
        return Token(TokenType.BLOCK, tokens)

    def buildFunction(self):
        name = ""
        args = ""
        parsingquote = False

        while True:
            if parsingquote == False:
                if self.char == "(":
                    break
            if self.char == "\"":
                parsingquote = not parsingquote
            name += self.char
            self.advance()
        
        self.advance()

        while True:
            if parsingquote == False:
                if self.char == ")":
                    break
            if self.char == "\"":
                parsingquote = not parsingquote
            args += self.char
            self.advance()

        self.advance()

        tokens = list(Lexer(args.replace(",", " ")).parse())

        return Token(TokenType.FUNCTION, {"name":name, "args":tokens})

    def buildNumber(self):
        number = self.char
        self.advance()

        while self.char != None and (self.char == '.' or self.char in DIGITS):
            number += self.char
            self.advance()
        
        if number.startswith('.'):
            number = "0" + number
        if number.endswith('.'):
            number = number + "0"

        return Token(TokenType.NUMBER, float(number))

    def buildString(self):
        string = ""
        lastchar = self.char
        self.advance()

        while self.char != None:
            if self.char == "\"":
                if not lastchar == "\\":
                    self.advance()
                    break
            string += self.char
            lastchar = self.char
            self.advance()

        return Token(TokenType.STRING, string)