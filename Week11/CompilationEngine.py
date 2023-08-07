import JackTokenizer
from SymbolTable import SymbolTable
class CompilationEngine:

    keywords = {'class', 'constructor', 'function', 'method', 'field', 'static',
                'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
                'this', 'let', 'do', 'if', 'else', 'while', 'return',}
    symbols = {'{', '}', '(', ')', '[', ']', '|', '.', ',', ';', '+', '-', '*', '/',
               '&', '<', '>', '=', '~',}

    def __init__(self, inputFile, outputFile):
        self.inputFile = JackTokenizer.JackTokenizer(inputFile)
        self.outputFile = open(outputFile, 'w+')
        self.symbolTable = SymbolTable()
        self.spacesIndented = 0

    def CompileClass(self):
        if self.inputFile.hasMoreTokens():
            self.inputFile.advance()
            self.outputFile.write('<class>\n')
            self.spacesIndented += 1
            self.compileKeyword()
            self.inputFile.advance()
            self.compileIdentifier()
            self.inputFile.advance()
            self.compileSymbol()
            self.inputFile.advance()
            while self.inputFile.keyWord() in ['static', 'field']:
                self.CompileClassVarDec()
            while self.inputFile.keyWord() in ['constructor', 'function', 'method']:
                self.CompileSubroutineDec()
            self.compileSymbol()
            self.spacesIndented -= 1
            self.outputFile.write('</class>\n')
            self.outputFile.close()

    def CompileClassVarDec(self):
        while self.inputFile.currentToken in ['static, field']:
            kind = self.inputFile.currentToken
            self.inputFile.advance()
            type = self.inputFile.currentToken
            self.inputFile.advance()
            name = self.inputFile.currentToken
            self.inputFile.advance()

            self.symbolTable.define(name, type, kind)

            while self.inputFile.symbol() == ',':
                self.inputFile.advance()
                self.symbolTable.define(self.inputFile.currentToken, type, kind)
                self.inputFile.advance()
            self.inputFile.advance()


    def CompileSubroutineDec(self):
        self.outputFile.write(' ' * self.spacesIndented + '<subroutineDec>\n')
        self.spacesIndented += 1
        self.compileKeyword()
        self.inputFile.advance()

        if self.inputFile.tokenType() == 'KEYWORD':
            self.compileKeyword()
        elif self.inputFile.tokenType() == 'IDENTIFIER':
            self.compileIdentifier()
        self.inputFile.advance()

        self.compileIdentifier()
        self.inputFile.advance()
        self.compileSymbol()
        self.inputFile.advance()

        self.compileParameterList()
        self.compileSymbol()
        self.inputFile.advance()
        self.compileSubroutineBody()
        self.outputFile.write(' ' * self.spacesIndented + '</subroutineDec>\n')
        self.inputFile.advance()

    def compileParameterList(self):
        self.outputFile.write(' ' * self.spacesIndented + '<parameterList>\n')
        self.spacesIndented += 1

        while self.inputFile.tokenType() != "SYMBOL":
            if self.inputFile.tokenType() == 'IDENTIFIER':
                self.compileIdentifier()
            elif self.inputFile.tokenType() == 'KEYWORD':
                self.compileKeyword()
            self.inputFile.advance()
            self.compileIdentifier()
            self.inputFile.advance()
            if self.inputFile.symbol() == ',':
                self.compileSymbol()
                self.inputFile.advance()

        self.spacesIndented -= 1
        self.outputFile.write(' ' * self.spacesIndented + '</parameterList>\n')

    def compileSubroutineBody(self):
        self.outputFile.write(' ' * self.spacesIndented + '<subroutineBody>\n')
        self.spacesIndented += 1
        self.compileSymbol()
        self.inputFile.advance()

        while self.inputFile.keyWord() == 'var':
            self.compileVarDec()

        self.compileStatements()
        self.compileSymbol()
        self.spacesIndented -= 1
        self.outputFile.write(' ' * self.spacesIndented + '</subroutineBody>\n')

    def compileVarDec(self):
        self.outputFile.write(' ' * self.spacesIndented + '<varDec>\n')
        self.spacesIndented += 1
        self.compileKeyword()
        self.inputFile.advance()
        if self.inputFile.tokenType() == 'KEYWORD':
            self.compileKeyword()
        elif self.inputFile.tokenType() == 'IDENTIFIER':
            self.compileIdentifier()

        self.inputFile.advance()
        self.compileIdentifier()
        self.inputFile.advance()

        while self.inputFile.symbol() == ',':
            self.compileSymbol()
            self.inputFile.advance()
            self.compileIdentifier()
            self.inputFile.advance()

        self.compileSymbol()

        self.inputFile.advance()
        self.spacesIndented -= 1
        self.outputFile.write(' ' * self.spacesIndented + '</varDec>\n')

    def compileStatements(self):
        self.outputFile.write(' ' * self.spacesIndented + '<statements>\n')
        self.spacesIndented += 1

        while self.inputFile.tokenType() == 'KEYWORD':
            if self.inputFile.keyWord() == 'return':
                self.compileReturn()
            elif self.inputFile.keyWord() == 'if':
                self.compileIf()
            elif self.inputFile.keyWord() == 'do':
                self.compileDo()
            elif self.inputFile.keyWord() == 'let':
                self.compileLet()
            elif self.inputFile.keyWord() == 'while':
                self.compileWhile()

        self.spacesIndented -= 1
        self.outputFile.write(' ' * self.spacesIndented + '</statements>\n')

    def compileLet(self):
        self.outputFile.write(' ' * self.spacesIndented + '<letStatement>\n')
        self.spacesIndented += 1
        self.compileKeyword()
        self.inputFile.advance()
        self.compileIdentifier()
        self.inputFile.advance()

        if self.inputFile.symbol() == '[':
            self.compileSymbol()
            self.inputFile.advance()
            self.CompileExpression()
            self.compileSymbol()
            self.inputFile.advance()

        self.compileSymbol()
        self.inputFile.advance()
        self.CompileExpression()
        self.compileSymbol()
        self.spacesIndented -= 1

        self.outputFile.write(' ' * self.spacesIndented + '</letStatement>\n')
        self.inputFile.advance()

    def compileIf(self):
        self.outputFile.write(' ' * self.spacesIndented + '<ifStatement>\n')
        self.spacesIndented += 1
        self.compileKeyword()
        self.inputFile.advance()
        self.compileSymbol()
        self.inputFile.advance()
        self.CompileExpression()
        self.compileSymbol()
        self.inputFile.advance()
        self.compileSymbol()
        self.inputFile.advance()
        self.compileStatements()
        self.compileSymbol()
        self.inputFile.advance()

        if self.inputFile.tokenType() == 'KEYWORD' and self.inputFile.keyWord() == 'else':
            self.compileKeyword()
            self.inputFile.advance()
            self.compileSymbol()
            self.inputFile.advance()
            self.compileStatements()
            self.compileSymbol()
            self.inputFile.advance()

        self.spacesIndented -= 1
        self.outputFile.write(' ' * self.spacesIndented + '</ifStatement>\n'
                              )
    def compileWhile(self):
        self.outputFile.write(' ' * self.spacesIndented + '<whileStatement>\n')
        self.spacesIndented += 1
        self.compileKeyword()
        self.inputFile.advance()
        self.compileSymbol()
        self.inputFile.advance()
        self.CompileExpression()
        self.compileSymbol()
        self.inputFile.advance()
        self.compileSymbol()
        self.inputFile.advance()
        self.compileStatements()
        self.compileSymbol()

        self.spacesIndented -= 1
        self.outputFile.write(' ' * self.spacesIndented + '</whileStatement>\n')
        self.inputFile.advance()

    def compileDo(self):
        self.outputFile.write(' ' * self.spacesIndented + '<doStatement>\n')
        self.spacesIndented += 1
        self.compileKeyword()
        self.inputFile.advance()
        self.compileIdentifier()
        self.inputFile.advance()

        if self.inputFile.symbol() == '.':
            self.compileSymbol()
            self.inputFile.advance()
            self.compileIdentifier()
            self.inputFile.advance()

        self.compileSymbol()
        self.inputFile.advance()
        self.CompileExpressionList()
        self.compileSymbol()
        self.inputFile.advance()
        self.compileSymbol()

        self.spacesIndented -= 1
        self.outputFile.write(' ' * self.spacesIndented + '</doStatement>\n')
        self.inputFile.advance()

    def compileReturn(self):
        self.outputFile.write(' ' * self.spacesIndented + '<returnStatement>\n')
        self.spacesIndented += 1
        self.compileKeyword()
        self.inputFile.advance()

        if self.inputFile.tokenType() != 'SYMBOL' and self.inputFile.symbol() != ';':
            self.CompileExpression()

        self.compileSymbol()

        self.spacesIndented -= 1
        self.outputFile.write(' ' * self.spacesIndented + '</returnStatement>\n')
        self.inputFile.advance()

    def compileSymbol(self):
        symbol = self.inputFile.symbol()
        if symbol == '<':
            addString = '&lt;'
        elif symbol == '>':
            addString = '&gt;'
        elif symbol == '&':
            addString = '&amp;'
        else:
            addString = self.inputFile.symbol()
        self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')

    def compileIdentifier(self):
        self.outputFile.write(' ' * self.spacesIndented + '<identifier> ' + self.inputFile.identifier() + ' </identifier>\n')

    def compileKeyword(self):
        keyword = self.inputFile.keyWord()

        if keyword == 'this':
            self.outputFile.writePush('pointer', 0)
        else:
            self.outputFile.writePush('constant', 0)
            if keyword == 'true':
                self.outputFile.writeArithmetic('not')

    def CompileExpression(self):
        self.outputFile.write(' ' * self.spacesIndented + '<expression>\n')
        self.spacesIndented += 1
        self.CompileTerm()

        while self.inputFile.tokenType() == 'SYMBOL' and self.inputFile.symbol() in ['=', '+', '-', '*', '/', '&', '|', '>', '<']:
            self.compileSymbol()
            self.inputFile.advance()
            self.CompileTerm()

        self.spacesIndented -= 1
        self.outputFile.write(' ' * self.spacesIndented + '</expression>\n')

    def CompileTerm(self):
        self.outputFile.write(' ' * self.spacesIndented + '<term>\n')
        self.spacesIndented += 1
        move = True
        if self.inputFile.tokenType() == 'INT_CONST':
            self.outputFile.write(' ' * self.spacesIndented + '<integerConstant> ' + self.inputFile.identifier() + '</integerConstant>\n')
        elif self.inputFile.tokenType() == 'STRING_CONST':
            self.outputFile.write(' ' * self.spacesIndented + '<stringConstant> ' + self.inputFile.stringVal() + '</stringConstant>\n')
        elif self.inputFile.tokenType() == 'KEYWORD':
            self.compileKeyword()
        elif self.inputFile.tokenType() == 'IDENTIFIER':
            move = False
            self.compileIdentifier()
            self.inputFile.advance()
            if self.inputFile.symbol() == '[':
                move = True
                self.compileSymbol()
                self.inputFile.advance()
                self.CompileExpression()
                self.compileSymbol()
            elif self.inputFile.symbol() == '.':
                move = True
                self.compileSymbol()
                self.inputFile.advance()
                self.compileIdentifier()
                self.inputFile.advance()
                self.compileSymbol()
                self.inputFile.advance()
                self.CompileExpressionList()
                self.compileSymbol()
            elif self.inputFile.symbol() == '(':
                move = True
                self.compileSymbol()
                self.inputFile.advance()
                self.CompileExpressionList()
                self.compileSymbol()
        elif self.inputFile.symbol() == '(':
            self.compileSymbol()
            self.inputFile.advance()
            self.CompileExpression()
            self.compileSymbol()
        elif self.inputFile.symbol() in ['~', '-']:
            self.compileSymbol()
            self.inputFile.advance()
            self.CompileTerm()
            move = False

        if move:
            self.inputFile.advance()

        self.spacesIndented -= 1
        self.outputFile.write(' ' * self.spacesIndented + '</term>\n')

    def CompileExpressionList(self):
        self.outputFile.write(' ' * self.spacesIndented + '<expressionList>\n')
        self.spacesIndented += 1

        if self.inputFile.tokenType() != 'SYMBOL' and self.inputFile.symbol() != ')':
            self.CompileExpression()
            while self.inputFile.tokenType() == 'SYMBOL' and self.inputFile.symbol() == ',':
                self.compileSymbol()
                self.inputFile.advance()
                self.CompileExpression()
        if self.inputFile.symbol() == '(':
            self.CompileExpression()
            while self.inputFile.tokenType() == 'SYMBOL' and self.inputFile.symbol() == ',':
                self.compileSymbol()
                self.inputFile.advance()
                self.CompileExpression()

        self.spacesIndented -= 1
        self.outputFile.write(' ' * self.spacesIndented + '</expressionList>\n')
