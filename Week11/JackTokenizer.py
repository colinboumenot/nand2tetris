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
        # removing comments
        self.input = ' '.join(re.sub(r'(?:(\/\*(.|\n)*?\*\/)|(//.*))', '', self.input).split())
        self.currentToken = None
        self.tokens = [x for x in self.split(self.input)]

    def split(self, line):
        # split at end of each token
        regex = re.compile(
            '(?!\w)|'.join(keywords) + '(?!\w)|' + '[' + re.escape('|'.join(symbols)) + ']|\d+|"[^"\n]*"|[\w]+')
        return regex.findall(line)

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
        elif self.currentToken.startswith('"') and self.currentToken.endswith('"'):
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

# peek and peekTokenType should only be called if there are more tokens
    def peek(self):
        return self.tokens[0]

    def peekTokenType(self):
        if self.tokens[0] in keywords:
            return 'KEYWORD'
        elif self.tokens[0] in symbols:
            return 'SYMBOL'
        elif self.tokens[0].isdigit():
            return 'INT_CONST'
        elif self.tokens[0].startswith('"') and self.tokens[0].endswith('"'):
            return 'STRING_CONST'
        else:
            return 'IDENTIFIER'


if __name__ == "__main__":
    a = JackTokenizer("Square.jack")
    while a.hasMoreTokens():
        a.advance()
        print(a.keyWord() + ' ' + a.tokenType())
