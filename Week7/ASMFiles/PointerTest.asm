//C_PUSH constant 3030
@3030
D=A
@SP
A=M
M=D
@SP
M=M+1
//C_POP pointer 0
@SP
M=M-1
A=M
D=M
@3
M=D
//C_PUSH constant 3040
@3040
D=A
@SP
A=M
M=D
@SP
M=M+1
//C_POP pointer 1
@SP
M=M-1
A=M
D=M
@4
M=D
//C_PUSH constant 32
@32
D=A
@SP
A=M
M=D
@SP
M=M+1
//C_POP this 2
@3
D=M
@2
D=D+A
@13
M=D
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
//C_PUSH constant 46
@46
D=A
@SP
A=M
M=D
@SP
M=M+1
//C_POP that 6
@4
D=M
@6
D=D+A
@13
M=D
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
//C_PUSH pointer 0
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
//C_PUSH pointer 1
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
// ADD
@SP
A=M-1
D=M
@SP
M=M-1
@SP
A=M-1
M=M+D
//C_PUSH this 2
@3
D=M
@2
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// SUB
@SP
A=M-1
D=M
@SP
M=M-1
@SP
A=M-1
M=M-D
//C_PUSH that 6
@4
D=M
@6
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// ADD
@SP
A=M-1
D=M
@SP
M=M-1
@SP
A=M-1
M=M+D
