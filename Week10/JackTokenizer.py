import re

keywords = {'class', 'constructor', 'function', 'method', 'field', 'static',
            'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
            'this', 'let', 'do', 'if', 'else', 'while', 'return', }

symbols = {'{', '}', '(', ')', '[', ']', '|', '.', ',', ';', '+', '-', '*', '/',
           '&', '<', '>', '=', '~', }


class JackTokenizer:

    def __init__(self, inputFile):
        self.inputFile = open(inputFile, 'r').read()
        self.cleanup()
        self.currentToken = None
        self.tokens = [x for x in re.split(r'([\{\}\(\)\[\]\.\,\;\+\-\*\/\&\<\>\=\~\|]|(?:"[^"]*")| *)', self.inputFile)
                       if x not in (' ', '')]

    def cleanup(self):
        self.inputFile = ''.join(re.sub(r'(?:(\/\*(.|\n)*?\*\/)|(//.*))', '', self.inputFile))

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



