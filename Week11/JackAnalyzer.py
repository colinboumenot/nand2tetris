import os
import JackTokenizer
import CompilationEngine
import VMWriter as vm

def main():
    userInput = input('Input File or Directory Name: ')
    if os.path.isdir(userInput):
        if not userInput.endswith('/'):
            userInput += '/'
        files = os.listdir(userInput)
        for file in files:
            if file.endswith('.jack'):
                fileName = file.split('.')[0]
                vmFile = vm.VMWriter(userInput + fileName + '.vm')
                compiler = CompilationEngine.CompilationEngine(userInput + file, vmFile)
                compiler.CompileClass()
    elif os.path.isfile(userInput):
        userInput = userInput.split('.')[0]
        vmFile = vm.VMWriter(userInput + '.vm')
        compiler = CompilationEngine.CompilationEngine(userInput + '.jack', vmFile)
        compiler.CompileClass()

if __name__ == '__main__':
    main()