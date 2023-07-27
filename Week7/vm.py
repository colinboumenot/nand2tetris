class Parser:
    def __init__(self, input_file):
        self.vmFile = open(input_file, 'r')
        self.currentCommand = ['NULL']

    def hasMoreCommands(self):
        pass

    def advance(self):
        pass

    def commandType(self):
        pass

    def arg1(self):
        pass

    def arg2(self):
        pass


class CodeWriter:
    def __init__(self, input_file):
        self.asmFile = open(input_file, 'w')

    def writeArithmetic(self, command):
        pass

    def writePushPop(self, command, segment, index):
        pass

    def close(self):
        self.asmFile.close()




input_file = input('File Name: ')
vmFile = Parser('VMFiles/' + input_file + '.vm')
asmFile = CodeWriter('ASMFiles/' + input_file + '.asm')

while vmFile.hasMoreCommands():
    vmFile.advance()
    command_type = vmFile.commandType()
    if command_type in ['push', 'pop']:
        asmFile.writePushPop(command_type, vmFile.arg1(), vmFile.arg2())
    else:
        asmFile.writeArithmetic(vmFile.currentCommand[0])