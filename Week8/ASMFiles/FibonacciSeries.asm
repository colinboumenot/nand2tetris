// Init
@256
D=A
@SP
M=D
// Function
(OS)
//C_PUSH argument 1
@2
D=M
@1
D=D+A
A=D
D=M
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
//C_PUSH constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
//C_POP that 0
@4
D=M
@0
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
//C_PUSH constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
//C_POP that 1
@4
D=M
@1
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
//C_PUSH argument 0
@2
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
//C_PUSH constant 2
@2
D=A
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
//C_POP argument 0
@2
D=M
@0
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
// Label
(OS$MAIN_LOOP_START)
//C_PUSH argument 0
@2
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// If-Goto
@SP
M=M-1
A=M
D=M
@OS$COMPUTE_ELEMENT
D;JNE
// Goto
@OS$END_PROGRAM
0;JMP
// Label
(OS$COMPUTE_ELEMENT)
//C_PUSH that 0
@4
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
//C_PUSH that 1
@4
D=M
@1
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
//C_POP that 2
@4
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
//C_PUSH pointer 1
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
//C_PUSH constant 1
@1
D=A
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
//C_POP pointer 1
@SP
M=M-1
A=M
D=M
@4
M=D
//C_PUSH argument 0
@2
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
//C_PUSH constant 1
@1
D=A
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
//C_POP argument 0
@2
D=M
@0
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
// Goto
@OS$MAIN_LOOP_START
0;JMP
// Label
(OS$END_PROGRAM)
