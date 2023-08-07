class VMWriter:

    def __init__(self, outputFile):
        self.outputFile = open(outputFile, 'w+')

    def writePush(self, segment, index):
        segment = segment.lower()

        if segment == 'arg':
            segment = 'argument'
        elif segment == 'const':
            segment = 'constant'

        self.outputFile.write('push ' + segment + ' ' + str(index) + '\n')

    def writePop(self, segment, index):
        segment = segment.lower()

        if segment == 'arg':
            segment = 'argument'
        elif segment == 'const':
            segment = 'constant'

        self.outputFile.write('pop ' + segment + ' ' + str(index) + '\n')

    def writeArithmetic(self, command):
        command = command.lower()
        self.outputFile.write(command + '\n')

    def WriteLabel(self, label):
        self.outputFile.write('label ' + label + '\n')

    def WriteGoto(self, label):
        self.outputFile.write('goto ' + label + '\n')

    def WriteIf(self, label):
        self.outputFile.write('if-goto ' + label + '\n')

    def writeCall(self, name, nArgs):
        self.outputFile.write('call ' + name + ' ' + str(nArgs) + '\n')

    def writeFunction(self, name, nLocals):
        self.outputFile.write('function ' + name + ' ' + str(nLocals) + '\n')

    def writeReturn(self):
        self.outputFile.write('return\n')

    def close(self):
        self.outputFile.close()
