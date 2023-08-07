class VMWriter:

    def __init__(self, outputFile):
        self.outputFile = outputFile

    def writePush(self, segment, index):
        segment = segment.lower()

        if segment == 'arg':
            segment = 'argument'
        elif segment == 'const':
            segment = 'constant'

        self.outputFile.write('push ' + segment + ' ' + index + '\n')

    def writePop(self, segment, index):
        segment = segment.lower()

        if segment == 'arg':
            segment = 'argument'
        elif segment == 'const':
            segment = 'constant'

        self.outputFile.write('pop ' + segment + ' ' + index + '\n')

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
        self.outputFile.write('call ' + name + ' ' + nArgs + '\n')

    def writeFunction(self, name, nLocals):
        self.outputFile.write('function ' + name + ' ' + nLocals + '\n')

    def writeReturn(self):
        self.outputFile.write('return\n')

    def close(self):
        self.outputFile.close()
