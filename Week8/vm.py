class Parser:
    def __init__(self, input_file):
        self.vmFile = open(input_file, 'r')
        self.lines = self.vmFile.readlines()
        self.currentCommand = None
        self.line_number = 0
        self.file_length = len(self.lines)

    def hasMoreCommands(self):
        if self.file_length > self.line_number:
            return True
        else:
            return False

    def advance(self):
        if self.hasMoreCommands():
            self.currentCommand = ''
            while self.currentCommand == '':
                self.currentCommand = self.lines[self.line_number]
                self.line_number += 1
                self.currentCommand = self.currentCommand.split('/')[0].strip()

    def commandType(self):
        if self.currentCommand.split(' ')[0] == 'push':
            return 'C_PUSH'
        elif self.currentCommand.split(" ")[0] == 'pop':
            return 'C_POP'
        elif self.currentCommand.split(' ')[0] == 'label':
            return 'C_LABEL'
        elif self.currentCommand.split(' ')[0] == 'goto':
            return 'C_GOTO'
        elif self.currentCommand.split(' ')[0] == 'if-goto':
            return 'C_IF'
        elif self.currentCommand.split(' ')[0] == 'function':
            return 'C_FUNCTION'
        elif self.currentCommand == 'return':
            return 'C_RETURN'
        return 'C_ARITHMETIC'

    def arg1(self):
        if self.commandType() == 'C_ARITHMETIC':
            return self.currentCommand.split(' ')[0]
        else:
            return self.currentCommand.split(' ')[1]

    def arg2(self):
        if self.commandType() in ['C_POP', 'C_PUSH', 'C_FUNCTION', 'C_RETURN']:
            return int(self.currentCommand.split(' ')[2])
        else:
            print("INVALID CALL OF ARG2")
            return None


class CodeWriter:
    def __init__(self, input_file, file_name):
        self.asmFile = open(input_file, 'w')
        self.file_name = file_name
        self.label_number = 0

    def writeArithmetic(self, command):
        if command == 'add':
            self.asmFile.write('// ADD\n')
            self.asmFile.write('@SP\nA=M-1\nD=M\n@SP\nM=M-1\n@SP\nA=M-1\nM=M+D\n')
        elif command == 'sub':
            self.asmFile.write('// SUB\n')
            self.asmFile.write('@SP\nA=M-1\nD=M\n@SP\nM=M-1\n@SP\nA=M-1\nM=M-D\n')
        elif command == 'neg':
            self.asmFile.write('// NEG\n')
            self.asmFile.write('@SP\nA=M-1\nM=-M\n')
        elif command == 'eq':
            self.asmFile.write('// EQ\n')
            label = '@EQ' + str(self.label_number)
            label_two = '@TWOEQ' + str(self.label_number)
            label_declared = '(EQ' + str(self.label_number) + ')'
            label_declared_two = '(TWOEQ' + str(self.label_number) + ')'
            self.label_number += 1
            self.asmFile.write('@SP\nA=M-1\nD=M\n@SP\nM=M-1\n@SP\nA=M-1\nD=M-D\n'+label+'\nD;JEQ\n@SP\nA=M-1\nM=0\n'+label_two+'\nD;JMP\n'+label_declared+'\n@SP\nA=M-1\nM=-1\n'+label_declared_two+'\n')
        elif command == 'gt':
            self.asmFile.write('// GT\n')
            label = '@GT' + str(self.label_number)
            label_two = '@TWOGT' + str(self.label_number)
            label_declared = '(GT' + str(self.label_number) + ')'
            label_declared_two = '(TWOGT' + str(self.label_number) + ')'
            self.label_number += 1
            self.asmFile.write('@SP\nA=M-1\nD=M\n@SP\nM=M-1\n@SP\nA=M-1\nD=M-D\n' + label + '\nD;JGT\n@SP\nA=M-1\nM=0\n' + label_two + '\nD;JMP\n' + label_declared + '\n@SP\nA=M-1\nM=-1\n' + label_declared_two + '\n')
        elif command == 'lt':
            self.asmFile.write('// LT\n')
            label = '@LT' + str(self.label_number)
            label_two = '@TWOLT' + str(self.label_number)
            label_declared = '(LT' + str(self.label_number) + ')'
            label_declared_two = '(TWOLT' + str(self.label_number) + ')'
            self.label_number += 1
            self.asmFile.write('@SP\nA=M-1\nD=M\n@SP\nM=M-1\n@SP\nA=M-1\nD=M-D\n' + label + '\nD;JLT\n@SP\nA=M-1\nM=0\n' + label_two + '\nD;JMP\n' + label_declared + '\n@SP\nA=M-1\nM=-1\n' + label_declared_two + '\n')
        elif command == 'and':
            self.asmFile.write('// AND\n')
            self.asmFile.write('@SP\nA=M-1\nD=M\n@SP\nM=M-1\n@SP\nA=M-1\nM=D&M\n')
        elif command == 'or':
            self.asmFile.write('// OR\n')
            self.asmFile.write('@SP\nA=M-1\nD=M\n@SP\nM=M-1\n@SP\nA=M-1\nM=D|M\n')
        elif command == 'not':
            self.asmFile.write('// NOT\n')
            self.asmFile.write('@SP\nA=M-1\nM=!M\n')

    def writePushPop(self, command, segment, index):
        self.asmFile.write('//' + command + ' ' + segment + ' ' + str(index) + '\n')
        if segment == 'local':
            self.asmFile.write('@1\nD=M\n@' + str(index) + '\n')
            if command == 'C_PUSH':
                self.asmFile.write('D=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif command == 'C_POP':
                self.asmFile.write('D=D+A\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D\n')
        elif segment == 'argument':
            self.asmFile.write('@2\nD=M\n@' + str(index) + '\n')
            if command == 'C_PUSH':
                self.asmFile.write('D=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif command == 'C_POP':
                self.asmFile.write('D=D+A\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D\n')
        elif segment == 'this':
            self.asmFile.write('@3\nD=M\n@' + str(index) + '\n')
            if command == 'C_PUSH':
                self.asmFile.write('D=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif command == 'C_POP':
                self.asmFile.write('D=D+A\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D\n')
        elif segment == 'that':
            self.asmFile.write('@4\nD=M\n@' + str(index) + '\n')
            if command == 'C_PUSH':
                self.asmFile.write('D=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif command == 'C_POP':
                self.asmFile.write('D=D+A\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D\n')
        elif segment == 'constant':
            if command == 'C_PUSH':
                self.asmFile.write('@'+str(index)+'\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif command == 'C_POP':
                print('CANNOT POP A CONSTANT')
        elif segment == 'static':
            if command == 'C_PUSH':
                self.asmFile.write('@'+self.file_name+'.'+str(index)+'\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif command == 'C_POP':
                self.asmFile.write('@SP\nM=M-1\nA=M\nD=M\n'+'@'+self.file_name+'.'+str(index)+'\nM=D\n')
        elif segment == 'temp':
            if command == 'C_PUSH':
                self.asmFile.write('@'+str(int(index) + 5)+'\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif command == 'C_POP':
                self.asmFile.write('@SP\nM=M-1\nA=M\nD=M\n@'+str(int(index)+5)+'\nM=D\n')
        elif segment == 'pointer':
            pointer_address = 3
            if command == 'C_PUSH':
                self.asmFile.write('@'+str(pointer_address+int(index))+'\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif command == 'C_POP':
                self.asmFile.write('@SP\nM=M-1\nA=M\nD=M\n@'+str(pointer_address+int(index))+'\nM=D\n')

    def close(self):
        self.asmFile.close()


input_file = input('File Name: ')
vmFile = Parser('VMFiles/' + input_file + '.vm')
asmFile = CodeWriter('ASMFiles/' + input_file + '.asm', input_file)

while vmFile.hasMoreCommands():
    vmFile.advance()
    command_type = vmFile.commandType()
    if command_type in ['C_PUSH', 'C_POP']:
        asmFile.writePushPop(command_type, vmFile.arg1(), vmFile.arg2())
    else:
        asmFile.writeArithmetic(vmFile.arg1())
asmFile.close()
