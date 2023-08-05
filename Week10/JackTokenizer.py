import re

keywords = {'class', 'constructor', 'function', 'method', 'field', 'static',
            'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
            'this', 'let', 'do', 'if', 'else', 'while', 'return', }

symbols = {'{', '}', '(', ')', '[', ']', '|', '.', ',', ';', '+', '-', '*', '/',
           '&', '<', '>', '=', '~', }


class JackTokenizer:

    def __init__(self, inputFile):
        file = open(inputFile, 'r+')
        self.input = file.read()
        self.input = ' '.join(re.sub(r'(?:(\/\*(.|\n)*?\*\/)|(//.*))', '', self.input).split())
        print(self.input.split(';'))
        self.currentToken = None
        self.tokens = [x for x in re.split(r'([\{\}\(\)\[\]\,\;\=\.\+\-\*\/\&\|\~\<\>]|(?:"[^"]*")| *)', self.input)
                       if x not in (' ', '')]

    def hasMoreTokens(self):
        if len(self.tokens) > 0:
            return True
        else:
            return False

    def advance(self):
        self.currentToken = self.tokens.pop(0)

    def tokenType(self):
        if self.currentToken in keywords:
            return 'KEYWORD'
        elif self.currentToken in symbols:
            return 'SYMBOL'
        elif self.currentToken.isdigit():
            return 'INT_CONST'
        elif self.currentToken.startswith("'") and self.currentToken.endswith("'"):
            return 'STRING_CONST'
        else:
            return 'IDENTIFIER'

    def keyWord(self):
        return self.currentToken

    def symbol(self):
        return self.currentToken

    def identifier(self):
        return self.currentToken

    def intVal(self):
        return int(self.currentToken)

    def stringVal(self):
        return self.currentToken[1:-1]

    def peek(self):
        return self.tokens[0]



if __name__ == "__main__":
    a = JackTokenizer("Square.jack")
    while a.hasMoreTokens():
        a.advance()
        print(a.keyWord())