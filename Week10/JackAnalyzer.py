import os
import JackTokenizer
import CompilationEngine

def main():
    inputFiles = []
    userInput = input('Input File or Directory Name: ')
    if os.path.idsdir(userInput):
        if userInput.endswith('/'):
            userInput = userInput[:-1]
        os.chdir(userInput)
        for file in os.listdir('.'):
            if file.endswith('.jack'):
                inputFiles.append(file)
    elif os.path.isfile(userInput):
        inputFiles = [userInput]

    for file in inputFiles:
        inputFile = file.split('/')[-1].split('.')[0]
        outputFile = inputFile + '.xml'
        tokenizer = JackTokenizer(inputFile)
        compiler = CompilationEngine(tokenizer, outputFile)
        compiler.CompileClass()

if __name__ == '__main__':
    main()