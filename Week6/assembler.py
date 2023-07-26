import re

COMP = {
    '0': '0101010',
    '1': '0111111',
    '-1': '0111010',
    'D': '0001100',
    'A': '0110000',
    'M': '1110000',
    '!D': '0001101',
    '!A': '0110001',
    '!M': '1110001',
    '-D': '0001111',
    '-A': '0110011',
    '-M': '1110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'M+1': '1110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'M-1': '1110010',
    'D+A': '0000010',
    'D+M': '1000010',
    'D-A': '0010011',
    'D-M': '1010011',
    'A-D': '0000111',
    'M-D': '1000111',
    'D&A': '0000000',
    'D&M': '1000000',
    'D|A': '0010101',
    'D|M': '1010101'
}

DEST = {
    'null': '000',
    'M': '001',
    'D': '010',
    'MD': '011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'AMD': '111'
}

JUMP = {
    'null': '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}

SYMBOL_TABLE = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'SCREEN': 16384,
    'KBD': 24576
}

memoryCounter = 16


def translateA(line):
    global memoryCounter

    if line[1].isalpha():
        variable = line[1:-1]
        if variable not in SYMBOL_TABLE:
            SYMBOL_TABLE[variable] = memoryCounter
            memoryCounter += 1
        value = SYMBOL_TABLE[variable]
    else:
        value = int(line[1:])
    return bin(value)[2:].zfill(16)


def translateC(line):
    line = line[:-1]
    if '=' not in line:
        line = 'null=' + line
    if ';' not in line:
        line = line + ';null'
    temp = line.split('=')
    destination = DEST[temp[0]]
    temp = temp[1].split(';')
    computation = COMP[temp[0]]
    jump = JUMP[temp[1]]
    return computation, destination, jump


def translate(line):
    if line.startswith('@'):
        return translateA(line)
    else:
        translation = translateC(line)
        return '111' + translation[0] + translation[1] + translation[2]


fileInput = input('File Name: ')

asmFile = open('Scripts/' + fileInput + '.asm', 'r')
tempFile = open('TempFiles/' + fileInput + '.txt', 'w')
currentLine = 0
for line in asmFile:
    newLine = re.sub(r'\/+.*\n|\n| *', '', line)
    if newLine != '':
        if newLine.startswith('('):
            SYMBOL_TABLE[newLine[1:-1]] = currentLine
            newLine = ''
        else:
            currentLine += 1
            tempFile.write(newLine + '\n')
asmFile.close()
tempFile.close()

tempFile = open('TempFiles/' + fileInput + '.txt', 'r')
hackFile = open('HackFiles/' + fileInput + '.hack', 'w')

for line in tempFile:
    translation = translate(line)
    hackFile.write(translation + '\n')
tempFile.close()
hackFile.close()