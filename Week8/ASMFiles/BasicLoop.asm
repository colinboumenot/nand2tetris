// Init
@256
D=A
@SP
M=D
// Function
(OS)
//C_PUSH constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
//C_POP local 0
@1
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
(OS$LOOP_START)
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
//C_PUSH local 0
@1
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
// ADD
@SP
A=M-1
D=M
@SP
M=M-1
@SP
A=M-1
M=M+D
//C_POP local 0
@1
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
@OS$LOOP_START
D;JNE
//C_PUSH local 0
@1
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
