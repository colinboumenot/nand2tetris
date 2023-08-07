import JackTokenizer
from SymbolTable import SymbolTable
class CompilationEngine:

    keywords = {'class', 'constructor', 'function', 'method', 'field', 'static',
                'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
                'this', 'let', 'do', 'if', 'else', 'while', 'return'}
    symbols = {'{', '}', '(', ')', '[', ']', '|', '.', ',', ';', '+', '-', '*', '/',
               '&', '<', '>', '=', '~'}

    def __init__(self, inputFile, outputFile):
        self.inputFile = JackTokenizer.JackTokenizer(inputFile)
        self.outputFile = outputFile
        self.symbolTable = SymbolTable()
        self.className = None
        self.subName = None
        self.ifCounter = 0
        self.whileCounter = 0
        self.let = 0

    def CompileClass(self):
        self.inputFile.advance()
        self.inputFile.advance()
        self.className = self.inputFile.currentToken
        self.inputFile.advance()
        self.inputFile.advance()

        if self.inputFile.currentToken in ['static', 'field']:
            self.CompileClassVarDec()
        while self.inputFile.currentToken in ['constructor', 'method', 'function']:
            self.CompileSubroutineDec()
            self.inputFile.advance()
        self.outputFile.close()

    def CompileClassVarDec(self):
        while self.inputFile.currentToken in ['static', 'field']:
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
        subroutineType = self.inputFile.currentToken
        self.inputFile.advance()
        self.inputFile.advance()
        self.subName = self.className + '.' + self.inputFile.currentToken
        self.inputFile.advance()
        self.symbolTable.startSubroutine()
        self.compileParameterList(subroutineType)
        self.inputFile.advance()
        self.compileSubroutineBody(subroutineType)


    def compileParameterList(self, subroutineType):
        if subroutineType == 'method':
            self.symbolTable.define('this', 'self', 'arg')
        self.inputFile.advance()
        while self.inputFile.tokenType() != 'SYMBOL':
            type = self.inputFile.currentToken
            self.inputFile.advance()
            name = self.inputFile.currentToken
            self.symbolTable.define(name, type, 'arg')
            self.inputFile.advance()
            if self.inputFile.currentToken == ',':
                self.inputFile.advance()

    def compileSubroutineBody(self,  subroutineType):
        self.inputFile.advance()
        while self.inputFile.currentToken == 'var':
            self.compileVarDec()
        nVars = self.symbolTable.VarCount('var')
        self.outputFile.writeFunction(self.subName, nVars)
        if subroutineType == 'method':
            self.outputFile.writePush('argument', 0)
            self.outputFile.writePop('pointer', 0)
        if subroutineType == 'constructor':
            fieldCount = self.symbolTable.VarCount('FIELD')
            self.outputFile.writePush('constant', fieldCount)
            self.outputFile.writeCall('Memory.alloc', 1)
            self.outputFile.writePop('pointer', 0)
        self.compileStatements()
        self.inputFile.advance()

    def compileVarDec(self):
        kind = self.inputFile.currentToken
        self.inputFile.advance()
        type = self.inputFile.currentToken
        self.inputFile.advance()
        name = self.inputFile.currentToken
        self.inputFile.advance()
        self.symbolTable.define(name, type, kind)
        while self.inputFile.currentToken == ',':
            self.inputFile.advance()
            name = self.inputFile.currentToken
            self.symbolTable.define(name, type, kind)
            self.inputFile.advance()
        self.inputFile.advance()

    def compileStatements(self):
        while self.inputFile.currentToken in ['let', 'if', 'while', 'do', 'return']:
            if self.inputFile.currentToken == 'let':
                self.compileLet()
            elif self.inputFile.currentToken == 'if':
                self.compileIf()
            elif self.inputFile.currentToken == 'while':
                self.compileWhile()
            elif self.inputFile.currentToken == 'do':
                self.compileDo()
            elif self.inputFile.currentToken == 'return':
                self.compileReturn()

    def compileLet(self):
        self.inputFile.advance()
        arrayPresent = False
        name = self.inputFile.currentToken
        self.inputFile.advance()
        if self.inputFile.currentToken == '[':
            arrayPresent = True
            self.compileArray()
        self.inputFile.advance()
        self.CompileExpression()
        if arrayPresent:
            self.outputFile.writePop('temp', 0)
            self.outputFile.writePop('pointer', 1)
            self.outputFile.writePush('temp', 0)
            self.outputFile.writePop('that', 0)
        else:
            if self.symbolTable.KindOf(name) != 'None':
                if self.symbolTable.KindOf(name) == 'VAR':
                    self.outputFile.writePop('local', self.symbolTable.IndexOf(name))
                elif self.symbolTable.KindOf(name) == 'ARG':
                    self.outputFile.writePop('argument', self.symbolTable.IndexOf(name))
                elif self.symbolTable.KindOf(name) == 'STATIC':
                    self.outputFile.writePop('static', self.symbolTable.IndexOf(name))
                else:
                    self.outputFile.writePop('this', self.symbolTable.IndexOf(name))
        if self.inputFile.currentToken == ';':
            self.inputFile.advance()
    def compileIf(self):
        self.inputFile.advance()
        self.inputFile.advance()
        self.CompileExpression()
        self.inputFile.advance()
        self.outputFile.WriteIf('IF_TRUE' + str(self.ifCounter))
        self.outputFile.WriteGoto('IF_FALSE' + str(self.ifCounter))
        self.outputFile.WriteLabel('IF_TRUE' + str(self.ifCounter))
        self.inputFile.advance()
        self.compileStatements()
        self.inputFile.advance()
        if self.inputFile.currentToken == 'else':
            self.outputFile.WriteGoto('IF_END' + str(self.ifCounter))
            self.outputFile.WriteLabel('IF_FALSE' + str(self.ifCounter))
            self.inputFile.advance()
            self.inputFile.advance()
            self.compileStatements()
            self.inputFile.advance()
            self.outputFile.WriteLabel('IF_END' + str(self.ifCounter))
        else:
            self.outputFile.WriteLabel('IF_FALSE', str(self.ifCounter))
        self.ifCounter += 1

    def compileWhile(self):
        self.outputFile.WriteLabel('WHILE_START' + str(self.whileCounter))
        self.inputFile.advance()
        self.inputFile.advance()
        self.CompileExpression()
        self.outputFile.writeArithmetic('not')
        self.outputFile.WriteIf('WHILE_END' + str(self.whileCounter))
        self.inputFile.advance()
        self.inputFile.advance()
        self.compileStatements()
        self.outputFile.WriteGoto('WHILE_START' + str(self.whileCounter))
        self.outputFile.WriteLabel('WHILE_END' + str(self.whileCounter))
        if self.inputFile.currentToken == '}':
            self.inputFile.advance()
        self.whileCounter += 1

    def compileDo(self):
        self.inputFile.advance()
        nLocals = 0
        name = self.inputFile.currentToken
        self.inputFile.advance()
        if self.inputFile.currentToken == '.':
            self.inputFile.advance()
            functionName = self.inputFile.currentToken
            if self.symbolTable.KindOf(name) != 'None':
                if self.symbolTable.KindOf(name) == 'VAR':
                    self.outputFile.writePush('local', self.symbolTable.IndexOf(name))
                elif self.symbolTable.KindOf(name) == 'ARG':
                    self.outputFile.writePush('argument', self.symbolTable.IndexOf(name))
                elif self.symbolTable.KindOf(name) == 'STATIC':
                    self.outputFile.writePush('static', self.symbolTable.IndexOf(name))
                else:
                    self.outputFile.writePush('this', self.symbolTable.IndexOf(name))
                finalName = self.symbolTable.TypeOf(name) + '.' + functionName
                nLocals += 1
            else:
                finalName = name + '.' + functionName
        else:
            self.outputFile.writePush('pointer', 0)
            nLocals += 1
            finalName = self.className + '.' + name
        self.inputFile.advance()
        nLocals += self.CompileExpressionList()
        self.outputFile.writeCall(finalName, nLocals)
        self.inputFile.advance()
        self.outputFile.writePop('temp', 0)
        self.inputFile.advance()

    def compileReturn(self):
        self.inputFile.advance()
        empty = True
        while self.inputFile.currentToken in ['-', '~', 'true', 'false', 'null', 'this'] or self.inputFile.tokenType in ['INT_CONST', 'STRING_CONST', 'IDENTIFIER']:
            empty = False
            self.CompileExpression()
        if empty:
            self.outputFile.writePush('constant', 0)
        self.outputFile.writeReturn()
        self.inputFile.advance()


    def CompileExpression(self):
        self.CompileTerm()
        self.inputFile.advance()
        while self.inputFile.currentToken in ['+', '-', '*', '/', '|', '=', '<', '>', '&']:
            operator = self.inputFile.currentToken
            self.inputFile.advance()
            self.CompileTerm()
            if operator == '+':
                self.outputFile.writeArithmetic('add')
            elif operator == '-':
                self.outputFile.writeArithmetic('sub')
            elif operator == '*':
                self.outputFile.writeCall('Math.multiply', 2)
            elif operator == '/':
                self.outputFile.writeCall('Math.divide', 2)
            elif operator == '|':
                self.outputFile.writeArithmetic('or')
            elif operator == '=':
                self.outputFile.writeArithmetic('eq')
            elif operator == '<':
                self.outputFile.writeArithmetic('lt')
            elif operator == '>':
                self.outputFile.writeArithmetic('gt')
            else:
                self.outputFile.writeArithmetic('and')

    def CompileTerm(self):
        arrayPresent = False
        if self.inputFile.tokenType() == 'INT_CONST':
            value = self.inputFile.currentToken
            self.outputFile.writePush('constant', value)
        elif self.inputFile.tokenType() == 'STRING_CONST':
            value = self.inputFile.currentToken
            self.outputFile.writePush('constant', len(value))
            self.outputFile.writeCall('String.new', 1)
            for char in value:
                self.outputFile.writePush('constant', ord(char))
                self.outputFile.writeCall('String.appendChar', 2)
        elif self.inputFile.currentToken in ['true', 'false', 'null', 'this']:
            value = self.inputFile.currentToken
            if value == 'this':
                self.outputFile.writePush('pointer', 0)
            else:
                self.outputFile.writePush('constant', 0)
                if value == 'true':
                    self.outputFile.writeArithmetic('not')
        elif self.inputFile.tokenType() == 'IDENTIFIER':
            nLocals = 0
            name = self.inputFile.currentToken
            self.inputFile.advance()
            if self.inputFile.currentToken == '[':
                arrayPresent = True
                self.compileArray()
            if self.inputFile.currentToken == '(':
                nLocals += 1
                self.outputFile.writePush('pointer', 0)
                self.inputFile.advance()
                nLocals += self.CompileExpressionList()
                self.inputFile.advance()
                self.outputFile.writeCall(self.className + '.' + name, nLocals)
            elif self.inputFile.currentToken == '.':
                self.inputFile.advance()
                subroutineName = self.inputFile.currentToken
                if self.symbolTable.KindOf(subroutineName) != 'None':
                    if self.symbolTable.KindOf(name) == 'VAR':
                        self.outputFile.writePush('local', self.symbolTable.IndexOf(name))
                    elif self.symbolTable.KindOf(name) == 'ARG':
                        self.outputFile.writePush('argument', self.symbolTable.IndexOf(name))
                    elif self.symbolTable.KindOf(name) == 'STATIC':
                        self.outputFile.writePush('static', self.symbolTable.IndexOf(name))
                    else:
                        self.outputFile.writePush('this', self.symbolTable.IndexOf(name))
                    name = self.symbolTable.TypeOf(name) + '.' + subroutineName
                    nLocals += 1
                else:
                    name = name + '.' + subroutineName
                self.inputFile.advance()
                nLocals += self.CompileExpressionList()
                self.inputFile.advance()
                self.outputFile.writeCall(name, nLocals)
            else:
                if arrayPresent:
                    self.outputFile.writePop('pointer', 1)
                    self.outputFile.writePush('that', 0)
                elif self.symbolTable.KindOf(name) != 'None':
                    if self.symbolTable.KindOf(name) == 'VAR':
                        self.outputFile.writePush('local', self.symbolTable.IndexOf(name))
                    elif self.symbolTable.KindOf(name) == 'ARG':
                        self.outputFile.writePush('argument', self.symbolTable.IndexOf(name))
                    elif self.symbolTable.KindOf(name) == 'STATIC':
                        self.outputFile.writePush('static', self.symbolTable.IndexOf(name))
                    else:
                        self.outputFile.writePush('this', self.symbolTable.IndexOf(name))
        elif self.inputFile.currentToken in ['-', '~']:
            operator = self.inputFile.currentToken
            self.inputFile.advance()
            self.CompileTerm()
            if operator == '-':
                self.outputFile.writeArithmetic('neg')
            else:
                self.outputFile.writeArithmetic('not')
        elif self.inputFile.currentToken == '(':
            self.inputFile.advance()
            self.CompileExpression()
            self.inputFile.advance()

    def compileArray(self, name):
        self.CompileExpression()
        self.inputFile.advance()
        if self.symbolTable.KindOf(name) != 'None':
            if self.symbolTable.KindOf(name) == 'VAR':
                self.outputFile.writePush('local', self.symbolTable.IndexOf(name))
            elif self.symbolTable.KindOf(name) == 'ARG':
                self.outputFile.writePush('argument', self.symbolTable.IndexOf(name))
            elif self.symbolTable.KindOf(name) == 'STATIC':
                self.outputFile.writePush('static', self.symbolTable.IndexOf(name))
            else:
                self.outputFile.writePush('this', self.symbolTable.IndexOf(name))
        self.outputFile.writeArithmetic('add')

    def CompileExpressionList(self):
        expressions = 0
        self.inputFile.advance()
        if self.inputFile.currentToken in ['-', '~', 'true', 'false', 'null', 'this'] or self.inputFile.tokenType() in ['INT_CONST', 'STRING_CONST', 'IDENTIFIER']:
            self.CompileExpression()
            expressions += 1
        while self.inputFile.currentToken == ',':
            self.inputFile.advance()
            self.CompileExpression()
            expressions += 1
        return expressions

