class CompilationEngine:

    keywords = {'class', 'constructor', 'function', 'method', 'field', 'static',
                'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
                'this', 'let', 'do', 'if', 'else', 'while', 'return',}
    symbols = {'{', '}', '(', ')', '[', ']', '|', '.', ',', ';', '+', '-', '*', '/',
               '&', '<', '>', '=', '~',}

    def __init__(self, inputFile, outputFile):
        self.inputFile = inputFile
        self.outputFile = open(outputFile, 'w+')
        self.spacesIndented = 0

    def CompileClass(self):
        if self.inputFile.hasMoreTokens():
            self.inputFile.advance()
            self.outputFile.write('<class>\n')
            self.spacesIndented += 1
            self.outputFile.write(' ' * self.spacesIndented + '<keyword> ' + self.inputFile.keyWord() + ' </keyword>\n')
            self.inputFile.advance()
            self.outputFile.write(' ' * self.spacesIndented + '<identifier> ' + self.inputFile.identifier() + ' </identifier>\n')
            self.inputFile.advance()
            symbol = self.inputFile.symbol()
            if symbol == '<':
                addString = '&lt'
            elif symbol == '>':
                addString = '&gt'
            elif symbol == '&':
                addString = '&amp'
            else:
                addString = ''
            self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
            self.inputFile.advance()
            while self.inputFile.keyWord() in ['static', 'field']:
                self.CompileClassVarDec()
            while self.inputFile.keyWord in ['constructor', 'function', 'method']:
                self.CompileSubroutineDec()
            symbol = self.inputFile.symbol()
            if symbol == '<':
                addString = '&lt'
            elif symbol == '>':
                addString = '&gt'
            elif symbol == '&':
                addString = '&amp'
            else:
                addString = ''
            self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
            self.spacesIndented -= 1
            self.outputFile.write('</class>\n')
            self.outputFile.close()

    def CompileClassVarDec(self):
        self.outputFile.write(' ' * self.spacesIndented + '<classVarDec>\n')
        self.spacesIndented += 1
        self.outputFile.write(' ' * self.spacesIndented + '<keyword> ' + self.inputFile.keyWord() + ' </keyword>\n')
        self.inputFile.advance()

        if self.inputFile.tokenType() == 'KEYWORD':
            self.outputFile.write(' ' * self.spacesIndented + '<keyword> ' + self.inputFile.keyWord() + ' </keyword>\n')
        elif self.inputFile.tokenType() == 'IDENTIFIER':
            self.outputFile.write(' ' * self.spacesIndented + '<identifier> ' + self.inputFile.identifier() + ' </identifier>\n')

        self.inputFile.advance()
        self.outputFile.write(' ' * self.spacesIndented + '<identifier> ' + self.inputFile.identifier() + ' </identifier>\n')
        self.inputFile.advance()

        while self.inputFile.symbol() == ',':
            symbol = self.inputFile.symbol()
            if symbol == '<':
                addString = '&lt'
            elif symbol == '>':
                addString = '&gt'
            elif symbol == '&':
                addString = '&amp'
            else:
                addString = ''
            self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
            self.inputFile.advance()
            self.outputFile.write(' ' * self.spacesIndented + '<identifier> ' + self.inputFile.identifier() + ' </identifier>\n')
            self.inputFile.advance()

        symbol = self.inputFile.symbol()
        if symbol == '<':
            addString = '&lt'
        elif symbol == '>':
            addString = '&gt'
        elif symbol == '&':
            addString = '&amp'
        else:
            addString = ''
        self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')

        self.inputFile.advance()
        self.spacesIndented -= 1
        self.outputFile.write(' ' * self.spacesIndented + '</classVarDec>\n')

    def CompileSubroutineDec(self):
        self.outputFile.write(' ' * self.spacesIndented + '<subroutineDec>\n')
        self.spacesIndented += 1
        self.outputFile.write(' ' * self.spacesIndented + '<keyword> ' + self.inputFile.keyWord() + ' </keyword>\n')
        self.inputFile.advance()

        if self.inputFile.tokenType() == 'KEYWORD':
            self.outputFile.write(' ' * self.spacesIndented + '<keyword> ' + self.inputFile.keyWord() + ' </keyword>\n')
        elif self.inputFile.tokenType() == 'IDENTIFIER':
            self.outputFile.write(' ' * self.spacesIndented + '<identifier> ' + self.inputFile.identifier() + ' </identifier>\n')
        self.inputFile.advance()

        self.outputFile.write(' ' * self.spacesIndented + '<identifier> ' + self.inputFile.identifier() + ' </identifier>\n')
        self.inputFile.advance()
        symbol = self.inputFile.symbol()
        if symbol == '<':
            addString = '&lt'
        elif symbol == '>':
            addString = '&gt'
        elif symbol == '&':
            addString = '&amp'
        else:
            addString = ''
        self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
        self.inputFile.advance()

        self.compileParameterList()
        symbol = self.inputFile.symbol()
        if symbol == '<':
            addString = '&lt'
        elif symbol == '>':
            addString = '&gt'
        elif symbol == '&':
            addString = '&amp'
        else:
            addString = ''
        self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
        self.inputFile.advance()
        self.compileSubroutineBody()
        self.outputFile.write(' ' * self.spacesIndented + '</subroutineDec>\n')
        self.inputFile.advance()

    def compileParameterList(self):
        self.outputFile.write(' ' * self.spacesIndented + '<parameterList>\n')
        self.spacesIndented += 1

        while self.inputFile.tokenType() != "SYMBOL":
            if self.inputFile.tokenType() == 'IDENTIFIER':
                self.outputFile.write(' ' * self.spacesIndented + '<identifier> ' + self.inputFile.identifier() + ' </identifier>\n')
            elif self.inputFile.tokenType() == 'KEYWORD':
                self.outputFile.write(' ' * self.spacesIndented + '<keyword> ' + self.inputFile.keyWord() + ' </keyword>\n')
            self.inputFile.advance()
            self.outputFile.write(' ' * self.spacesIndented + '<identifier> ' + self.inputFile.identifier() + ' </identifier>\n')
            self.inputFile.advance()
            if self.inputFile.symbol() == ',':
                symbol = self.inputFile.symbol()
                if symbol == '<':
                    addString = '&lt'
                elif symbol == '>':
                    addString = '&gt'
                elif symbol == '&':
                    addString = '&amp'
                else:
                    addString = ''
                self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
                self.inputFile.advance()

            self.spacesIndented -= 1
            self.outputFile.write(' ' * self.spacesIndented + '</parameterList>\n')

    def compileSubroutineBody(self):
        self.outputFile.write(' ' * self.spacesIndented + '<subroutineBody>\n')
        self.spacesIndented += 1
        symbol = self.inputFile.symbol()
        if symbol == '<':
            addString = '&lt'
        elif symbol == '>':
            addString = '&gt'
        elif symbol == '&':
            addString = '&amp'
        else:
            addString = ''
        self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
        self.inputFile.advance()

        while self.inputFile.keyWord() == 'var':
            self.compileVarDec()

        self.compileStatements()
        symbol = self.inputFile.symbol()
        if symbol == '<':
            addString = '&lt'
        elif symbol == '>':
            addString = '&gt'
        elif symbol == '&':
            addString = '&amp'
        else:
            addString = ''
        self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
        self.spacesIndented -= 1
        self.outputFile.write(' ' * self.spacesIndented + '</subroutineBody>\n')

    def compileVarDec(self):
        self.outputFile.write(' ' * self.spacesIndented + '<varDec>\n')
        self.spacesIndented += 1
        self.outputFile.write(' ' * self.spacesIndented + '<keyword> ' + self.inputFile.keyWord() + ' </keyword>\n')
        self.inputFile.advance()
        if self.inputFile.tokenType() == 'KEYWORD':
            self.outputFile.write(' ' * self.spacesIndented + '<keyword> ' + self.inputFile.keyWord() + ' </keyword>\n')
        elif self.inputFile.tokenType() == 'IDENTIFIER':
            self.outputFile.write(
                ' ' * self.spacesIndented + '<identifier> ' + self.inputFile.identifier() + ' </identifier>\n')

        self.inputFile.advance()
        self.outputFile.write(
            ' ' * self.spacesIndented + '<identifier> ' + self.inputFile.identifier() + ' </identifier>\n')
        self.inputFile.advance()

        while self.inputFile.symbol() == ',':
            symbol = self.inputFile.symbol()
            if symbol == '<':
                addString = '&lt'
            elif symbol == '>':
                addString = '&gt'
            elif symbol == '&':
                addString = '&amp'
            else:
                addString = ''
            self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
            self.inputFile.advance()
            self.outputFile.write(' ' * self.spacesIndented + '<identifier> ' + self.inputFile.identifier() + ' </identifier>\n')
            self.inputFile.advance()

        symbol = self.inputFile.symbol()
        if symbol == '<':
            addString = '&lt'
        elif symbol == '>':
            addString = '&gt'
        elif symbol == '&':
            addString = '&amp'
        else:
            addString = ''
        self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')

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
        self.outputFile.write(' ' * self.spacesIndented + '<keyword> ' + self.inputFile.keyWord() + ' </keyword>\n')
        self.inputFile.advance()
        self.outputFile.write(' ' * self.spacesIndented + '<identifier> ' + self.inputFile.identifier() + ' </identifier>\n')
        self.inputFile.advance()

        if self.inputFile.symbol() == '[':
            symbol = self.inputFile.symbol()
            if symbol == '<':
                addString = '&lt'
            elif symbol == '>':
                addString = '&gt'
            elif symbol == '&':
                addString = '&amp'
            else:
                addString = ''
            self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
            self.inputFile.advance()
            self.CompileExpression()
            symbol = self.inputFile.symbol()
            if symbol == '<':
                addString = '&lt'
            elif symbol == '>':
                addString = '&gt'
            elif symbol == '&':
                addString = '&amp'
            else:
                addString = ''
            self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
            self.inputFile.advance()

        symbol = self.inputFile.symbol()
        if symbol == '<':
            addString = '&lt'
        elif symbol == '>':
            addString = '&gt'
        elif symbol == '&':
            addString = '&amp'
        else:
            addString = ''
        self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
        self.inputFile.advance()
        self.CompileExpression()
        symbol = self.inputFile.symbol()
        if symbol == '<':
            addString = '&lt'
        elif symbol == '>':
            addString = '&gt'
        elif symbol == '&':
            addString = '&amp'
        else:
            addString = ''
        self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
        self.spacesIndented -= 1

        self.outputFile.write(' ' * self.spacesIndented + '</letStatement>\n')
        self.inputFile.advance()

    def compileIf(self):
        self.outputFile.write(' ' * self.spacesIndented + '<ifStatement>\n')
        self.spacesIndented += 1
        self.outputFile.write(' ' * self.spacesIndented + '<keyword> ' + self.inputFile.keyWord() + ' </keyword>\n')
        self.inputFile.advance()
        symbol = self.inputFile.symbol()
        if symbol == '<':
            addString = '&lt'
        elif symbol == '>':
            addString = '&gt'
        elif symbol == '&':
            addString = '&amp'
        else:
            addString = ''
        self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
        self.inputFile.advance()
        self.CompileExpression()
        symbol = self.inputFile.symbol()
        if symbol == '<':
            addString = '&lt'
        elif symbol == '>':
            addString = '&gt'
        elif symbol == '&':
            addString = '&amp'
        else:
            addString = ''
        self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
        self.inputFile.advance()
        symbol = self.inputFile.symbol()
        if symbol == '<':
            addString = '&lt'
        elif symbol == '>':
            addString = '&gt'
        elif symbol == '&':
            addString = '&amp'
        else:
            addString = ''
        self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
        self.inputFile.advance()
        self.compileStatements()
        symbol = self.inputFile.symbol()
        if symbol == '<':
            addString = '&lt'
        elif symbol == '>':
            addString = '&gt'
        elif symbol == '&':
            addString = '&amp'
        else:
            addString = ''
        self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
        self.inputFile.advance()

        if self.inputFile.tokenType() == 'KEYWORD' and self.inputFile.keyWord() == 'else':
            self.outputFile.write(' ' * self.spacesIndented + '<keyword> ' + self.inputFile.keyWord() + ' </keyword>\n')
            self.inputFile.advance()
            symbol = self.inputFile.symbol()
            if symbol == '<':
                addString = '&lt'
            elif symbol == '>':
                addString = '&gt'
            elif symbol == '&':
                addString = '&amp'
            else:
                addString = ''
            self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
            self.inputFile.advance()
            self.compileStatements()
            symbol = self.inputFile.symbol()
            if symbol == '<':
                addString = '&lt'
            elif symbol == '>':
                addString = '&gt'
            elif symbol == '&':
                addString = '&amp'
            else:
                addString = ''
            self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
            self.inputFile.advance()

        self.spacesIndented -= 1
        self.outputFile.write(' ' * self.spacesIndented + '</ifStatement>\n'
                              )
    def compileWhile(self):
        self.outputFile.write(' ' * self.spacesIndented + '<whileStatement>\n')
        self.spacesIndented += 1
        self.outputFile.write(' ' * self.spacesIndented + '<keyword> ' + self.inputFile.keyWord() + ' </keyword>\n')
        self.inputFile.advance()
        symbol = self.inputFile.symbol()
        if symbol == '<':
            addString = '&lt'
        elif symbol == '>':
            addString = '&gt'
        elif symbol == '&':
            addString = '&amp'
        else:
            addString = ''
        self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
        self.inputFile.advance()
        self.CompileExpression()
        symbol = self.inputFile.symbol()
        if symbol == '<':
            addString = '&lt'
        elif symbol == '>':
            addString = '&gt'
        elif symbol == '&':
            addString = '&amp'
        else:
            addString = ''
        self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
        self.inputFile.advance()
        symbol = self.inputFile.symbol()
        if symbol == '<':
            addString = '&lt'
        elif symbol == '>':
            addString = '&gt'
        elif symbol == '&':
            addString = '&amp'
        else:
            addString = ''
        self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
        self.inputFile.advance()
        self.compileStatements()
        symbol = self.inputFile.symbol()
        if symbol == '<':
            addString = '&lt'
        elif symbol == '>':
            addString = '&gt'
        elif symbol == '&':
            addString = '&amp'
        else:
            addString = ''
        self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')

        self.spacesIndented -= 1
        self.outputFile.write(' ' * self.spacesIndented + '</whileStatement>\n')
        self.inputFile.advance()

    def compileDo(self):
        self.outputFile.write(' ' * self.spacesIndented + '<doStatement>\n')
        self.spacesIndented += 1
        self.outputFile.write(' ' * self.spacesIndented + '<keyword> ' + self.inputFile.keyWord() + ' </keyword>\n')
        self.inputFile.advance()
        self.outputFile.write(' ' * self.spacesIndented + '<identifier> ' + self.inputFile.identifier() + ' </identifier>\n')
        self.inputFile.advance()

        if self.inputFile.symbol() == '.':
            symbol = self.inputFile.symbol()
            if symbol == '<':
                addString = '&lt'
            elif symbol == '>':
                addString = '&gt'
            elif symbol == '&':
                addString = '&amp'
            else:
                addString = ''
            self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
            self.inputFile.advance()
            self.outputFile.write(' ' * self.spacesIndented + '<identifier> ' + self.inputFile.identifier() + ' </identifier>\n')
            self.inputFile.advance()

        symbol = self.inputFile.symbol()
        if symbol == '<':
            addString = '&lt'
        elif symbol == '>':
            addString = '&gt'
        elif symbol == '&':
            addString = '&amp'
        else:
            addString = ''
        self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
        self.inputFile.advance()
        self.CompileExpressionList()
        symbol = self.inputFile.symbol()
        if symbol == '<':
            addString = '&lt'
        elif symbol == '>':
            addString = '&gt'
        elif symbol == '&':
            addString = '&amp'
        else:
            addString = ''
        self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
        self.inputFile.advance()
        symbol = self.inputFile.symbol()
        if symbol == '<':
            addString = '&lt'
        elif symbol == '>':
            addString = '&gt'
        elif symbol == '&':
            addString = '&amp'
        else:
            addString = ''
        self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')

        self.spacesIndented -= 1
        self.outputFile.write(' ' * self.spacesIndented + '</doStatement>\n')
        self.inputFile.advance()

    def compileReturn(self):
        self.outputFile.write(' ' * self.spacesIndented + '<returnStatement>\n')
        self.spacesIndented += 1
        self.outputFile.write(' ' * self.spacesIndented + '<keyword> ' + self.inputFile.keyWord() + ' </keyword>\n')
        self.inputFile.advance()

        if self.inputFile.tokenType() != 'SYMBOL' and self.inputFile.symbol() != ';':
            self.CompileExpression()

        symbol = self.inputFile.symbol()
        if symbol == '<':
            addString = '&lt'
        elif symbol == '>':
            addString = '&gt'
        elif symbol == '&':
            addString = '&amp'
        else:
            addString = ''
        self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')

        self.spacesIndented -= 1
        self.outputFile.write(' ' * self.spacesIndented + '</returnStatement>\n')
        self.inputFile.advance()

    def CompileExpression(self):
        self.outputFile.write(' ' * self.spacesIndented + '<expression>\n')
        self.spacesIndented += 1
        self.CompileTerm()

        while self.inputFile.tokenType() == 'SYMBOL' and self.inputFile.symbol() in ['=', '+', '-', '*', '/', '&', '|', '>', '<']:
            symbol = self.inputFile.symbol()
            if symbol == '<':
                addString = '&lt'
            elif symbol == '>':
                addString = '&gt'
            elif symbol == '&':
                addString = '&amp'
            else:
                addString = ''
            self.outputFile.write(' ' * self.spacesIndented + '<symbol> ' + addString + ' </symbol>\n')
            self.inputFile.advance()
            self.CompileTerm()

        self.spacesIndented -= 1
        self.outputFile.write(' ' * self.spacesIndented + '</expression>\n')

    def CompileTerm(self):
        pass

    def CompileExpressionList(self):
        pass
