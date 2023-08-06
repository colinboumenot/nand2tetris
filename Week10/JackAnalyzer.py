import os
import JackTokenizer
import CompilationEngine

def main():
    userInput = input('Input File or Directory Name: ')
    if os.path.isdir(userInput):
        if not userInput.endswith('/'):
            userInput += '/'
        files = os.listdir(userInput)
        for file in files:
            if file.endswith('.jack'):
                fileName = file.split('.')[0]
                compiler = CompilationEngine.CompilationEngine(userInput + file, userInput + fileName + '.xmla')
                compiler.CompileClass()
    elif os.path.isfile(userInput):
        userInput = userInput.split('.')[0]
        compiler = CompilationEngine.CompilationEngine(userInput + '.jack', userInput + '.xmla')
        compiler.CompileClass()

if __name__ == '__main__':
    main()