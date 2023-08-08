import JackTokenizer
from SymbolTable import SymbolTable
class CompilationEngine:


    def __init__(self, inputFile, outputFile):
        self.inputFile = JackTokenizer.JackTokenizer(inputFile)
        self.outputFile = outputFile
        self.symbolTable = SymbolTable()
        self.className = ''
        self.subName = ''

    def CompileClass(self):
        self.inputFile.advance()
        self.inputFile.advance()
        self.className = self.inputFile.currentToken
        self.inputFile.advance()

        if self.inputFile.peek() in ['static', 'field']:
            self.CompileClassVarDec()
        while self.inputFile.peek() in ['constructor', 'method', 'function']:
            self.CompileSubroutineDec()
        self.inputFile.advance()
        self.outputFile.close()

    def CompileClassVarDec(self):
        while self.inputFile.peek() in ['static', 'field']:
            self.inputFile.advance()
            kind = self.inputFile.currentToken
            self.inputFile.advance()
            type = self.inputFile.currentToken
            self.inputFile.advance()
            name = self.inputFile.currentToken

            self.symbolTable.define(name, type, kind)

            while self.inputFile.peek() == ',':
                self.inputFile.advance()
                self.inputFile.advance()
                name = self.inputFile.currentToken
                self.symbolTable.define(name, type, kind)
            self.inputFile.advance()


    def CompileSubroutineDec(self):
        self.inputFile.advance()
        subroutineType = self.inputFile.currentToken
        self.inputFile.advance()
        self.inputFile.advance()
        self.subName = self.className + '.' + self.inputFile.currentToken
        self.symbolTable.startSubroutine(self.subName)
        self.symbolTable.scaleScope(self.subName)
        self.inputFile.advance()
        self.compileParameterList(subroutineType)
        self.inputFile.advance()
        self.compileSubroutineBody(subroutineType)


    def compileParameterList(self, subroutineType):
        if subroutineType == 'method':
            self.symbolTable.define('this', 'self', 'arg')
        while self.inputFile.peekTokenType() != 'SYMBOL':
            self.inputFile.advance()
            type = self.inputFile.currentToken
            self.inputFile.advance()
            name = self.inputFile.currentToken
            self.symbolTable.define(name, type, 'arg')
            if self.inputFile.peek() == ',':
                self.inputFile.advance()

    def compileSubroutineBody(self,  subroutineType):
        self.inputFile.advance()
        while self.inputFile.peek() == 'var':
            self.compileVarDec()
        nVars = self.symbolTable.VarCount('var')
        self.outputFile.writeFunction(self.subName, nVars)
        if subroutineType == 'method':
            self.outputFile.writePush('argument', 0)
            self.outputFile.writePop('pointer', 0)
        if subroutineType == 'constructor':
            fieldCount = self.symbolTable.ClassCount('FIELD')
            self.outputFile.writePush('constant', fieldCount)
            self.outputFile.writeCall('Memory.alloc', 1)
            self.outputFile.writePop('pointer', 0)
        self.compileStatements()
        self.inputFile.advance()
        self.symbolTable.scaleScope('field')

    def compileVarDec(self):
        self.inputFile.advance()
        kind = self.inputFile.currentToken
        self.inputFile.advance()
        type = self.inputFile.currentToken
        self.inputFile.advance()
        name = self.inputFile.currentToken
        self.symbolTable.define(name, type, kind)
        while self.inputFile.peek() == ',':
            self.inputFile.advance()
            self.inputFile.advance()
            name = self.inputFile.currentToken
            self.symbolTable.define(name, type, kind)
        self.inputFile.advance()

    def compileStatements(self):
        while self.inputFile.peek() in ['let', 'if', 'while', 'do', 'return']:
            if self.inputFile.peek() == 'let':
                self.compileLet()
            elif self.inputFile.peek() == 'if':
                self.compileIf()
            elif self.inputFile.peek() == 'while':
                self.compileWhile()
            elif self.inputFile.peek() == 'do':
                self.compileDo()
            elif self.inputFile.peek() == 'return':
                self.compileReturn()

    def compileLet(self):
        self.inputFile.advance()
        arrayPresent = False
        self.inputFile.advance()
        name = self.inputFile.currentToken
        if self.inputFile.peek() == '[':
            arrayPresent = True
            self.compileArray(name)
        self.inputFile.advance()
        self.CompileExpression()
        if arrayPresent:
            self.outputFile.writePop('temp', 0)
            self.outputFile.writePop('pointer', 1)
            self.outputFile.writePush('temp', 0)
            self.outputFile.writePop('that', 0)
        else:
            if name in self.symbolTable.currentScope:
                if self.symbolTable.KindOf(name) == 'VAR':
                    self.outputFile.writePop('local', self.symbolTable.IndexOf(name))
                elif self.symbolTable.KindOf(name) == 'ARG':
                    self.outputFile.writePop('argument', self.symbolTable.IndexOf(name))
            else:
                if self.symbolTable.KindOf(name) == 'STATIC':
                    self.outputFile.writePop('static', self.symbolTable.IndexOf(name))
                else:
                    self.outputFile.writePop('this', self.symbolTable.IndexOf(name))
        self.inputFile.advance()

    def compileIf(self):
        self.inputFile.advance()
        self.inputFile.advance()
        self.CompileExpression()
        self.inputFile.advance()
        counter = str(self.symbolTable.ifCounter)
        self.symbolTable.ifCounter += 1
        self.outputFile.WriteIf('IF_TRUE' + counter)
        self.outputFile.WriteGoto('IF_FALSE' + counter)
        self.outputFile.WriteLabel('IF_TRUE' + counter)
        self.inputFile.advance()
        self.compileStatements()
        self.inputFile.advance()
        if self.inputFile.peek() == 'else':
            self.outputFile.WriteGoto('IF_END' + counter)
            self.outputFile.WriteLabel('IF_FALSE' + counter)
            self.inputFile.advance()
            self.inputFile.advance()
            self.compileStatements()
            self.inputFile.advance()
            self.outputFile.WriteLabel('IF_END' + counter)
        else:
            self.outputFile.WriteLabel('IF_FALSE' + counter)


    def compileWhile(self):
        counter = str(self.symbolTable.whileCounter)
        self.symbolTable.whileCounter += 1
        self.outputFile.WriteLabel('WHILE_EXP' + counter)
        self.inputFile.advance()
        self.inputFile.advance()
        self.CompileExpression()
        self.outputFile.writeArithmetic('not')
        self.outputFile.WriteIf('WHILE_END' + counter)
        self.inputFile.advance()
        self.inputFile.advance()
        self.compileStatements()
        self.outputFile.WriteGoto('WHILE_EXP' + counter)
        self.outputFile.WriteLabel('WHILE_END' + counter)
        self.inputFile.advance()

    def compileDo(self):
        self.inputFile.advance()
        nLocals = 0
        self.inputFile.advance()
        name = self.inputFile.currentToken
        if self.inputFile.peek() == '.':
            self.inputFile.advance()
            self.inputFile.advance()
            functionName = self.inputFile.currentToken
            if name in self.symbolTable.currentScope or name in self.symbolTable.fieldScope:
                if name in self.symbolTable.currentScope:
                    if self.symbolTable.KindOf(name) == 'VAR':
                        self.outputFile.writePush('local', self.symbolTable.IndexOf(name))
                    elif self.symbolTable.KindOf(name) == 'ARG':
                        self.outputFile.writePush('argument', self.symbolTable.IndexOf(name))
                else:
                    if self.symbolTable.KindOf(name) == 'STATIC':
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
        while self.inputFile.peek() in ['-', '~', 'true', 'false', 'null', 'this', '('] or self.inputFile.peekTokenType() in ['INT_CONST', 'STRING_CONST', 'IDENTIFIER']:
            empty = False
            self.CompileExpression()
        if (empty):
            self.outputFile.writePush('constant', 0)
        self.outputFile.writeReturn()
        self.inputFile.advance()


    def CompileExpression(self):
        self.CompileTerm()
        while self.inputFile.peek() in ['+', '-', '*', '/', '|', '=', '<', '>', '&']:
            self.inputFile.advance()
            operator = self.inputFile.currentToken
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
            elif operator == '&':
                self.outputFile.writeArithmetic('and')

    def CompileTerm(self):
        arrayPresent = False
        if self.inputFile.peekTokenType() == 'INT_CONST':
            self.inputFile.advance()
            value = self.inputFile.currentToken
            self.outputFile.writePush('constant', value)
        elif self.inputFile.peekTokenType() == 'STRING_CONST':
            self.inputFile.advance()
            value = self.inputFile.currentToken
            self.outputFile.writePush('constant', len(value))
            self.outputFile.writeCall('String.new', 1)
            for char in value:
                self.outputFile.writePush('constant', ord(char))
                self.outputFile.writeCall('String.appendChar', 2)
        elif self.inputFile.peek() in ['true', 'false', 'null', 'this']:
            self.inputFile.advance()
            value = self.inputFile.currentToken
            if value == 'this':
                self.outputFile.writePush('pointer', 0)
            else:
                self.outputFile.writePush('constant', 0)
                if value == 'true':
                    self.outputFile.writeArithmetic('not')
        elif self.inputFile.peekTokenType() == 'IDENTIFIER':
            nLocals = 0
            self.inputFile.advance()
            name = self.inputFile.currentToken
            if self.inputFile.peek() == '[':
                arrayPresent = True
                self.compileArray(name)
            if self.inputFile.peek() == '(':
                nLocals += 1
                self.outputFile.writePush('pointer', 0)
                self.inputFile.advance()
                nLocals += self.CompileExpressionList()
                self.inputFile.advance()
                self.outputFile.writeCall(self.className + '.' + name, nLocals)
            elif self.inputFile.peek() == '.':
                self.inputFile.advance()
                self.inputFile.advance()
                subroutineName = self.inputFile.currentToken
                if name in self.symbolTable.currentScope or name in self.symbolTable.fieldScope:
                    if name in self.symbolTable.currentScope:
                        if self.symbolTable.KindOf(name) == 'VAR':
                            self.outputFile.writePush('local', self.symbolTable.IndexOf(name))
                        elif self.symbolTable.KindOf(name) == 'ARG':
                            self.outputFile.writePush('argument', self.symbolTable.IndexOf(name))
                    else:
                        if self.symbolTable.KindOf(name) == 'STATIC':
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
                elif name in self.symbolTable.currentScope:
                    if self.symbolTable.KindOf(name) == 'VAR':
                        self.outputFile.writePush('local', self.symbolTable.IndexOf(name))
                    elif self.symbolTable.KindOf(name) == 'ARG':
                        self.outputFile.writePush('argument', self.symbolTable.IndexOf(name))
                else:
                    if self.symbolTable.KindOf(name) == 'STATIC':
                        self.outputFile.writePush('static', self.symbolTable.IndexOf(name))
                    else:
                        self.outputFile.writePush('this', self.symbolTable.IndexOf(name))
        elif self.inputFile.peek() in ['-', '~']:
            self.inputFile.advance()
            operator = self.inputFile.currentToken
            self.CompileTerm()
            if operator == '-':
                self.outputFile.writeArithmetic('neg')
            else:
                self.outputFile.writeArithmetic('not')
        elif self.inputFile.peek() == '(':
            self.inputFile.advance()
            self.CompileExpression()
            self.inputFile.advance()

    def compileArray(self, name):
        self.inputFile.advance()
        self.CompileExpression()
        self.inputFile.advance()
        if name in self.symbolTable.currentScope:
            if self.symbolTable.KindOf(name) == 'VAR':
                self.outputFile.writePush('local', self.symbolTable.IndexOf(name))
            elif self.symbolTable.KindOf(name) == 'ARG':
                self.outputFile.writePush('argument', self.symbolTable.IndexOf(name))
        else:
            if self.symbolTable.KindOf(name) == 'STATIC':
                self.outputFile.writePush('static', self.symbolTable.IndexOf(name))
            else:
                self.outputFile.writePush('this', self.symbolTable.IndexOf(name))
        self.outputFile.writeArithmetic('add')

    def CompileExpressionList(self):
        expressions = 0
        if self.inputFile.peek() in ['-', '~', 'true', 'false', 'null', 'this', '('] or self.inputFile.peekTokenType() in ['INT_CONST', 'STRING_CONST', 'IDENTIFIER']:
            self.CompileExpression()
            expressions += 1
        while self.inputFile.peek() == ',':
            self.inputFile.advance()
            self.CompileExpression()
            expressions += 1
        return expressions

