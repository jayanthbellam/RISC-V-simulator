def bintodec(binary):
    length=len(binary)
    number=int(binary[1:],base=2)
    if binary[0]=='0':
        return number
    return number-2**(length-1)

def dectobin(integer,length):
    if integer>=0:
        temp=bin(integer).replace('0b','')
        le=len(temp)
        binary='0'*(length-le)+temp
    else:
        integer+=2**(length-1)
        temp=bin(integer).replace('0b','')
        le=len(temp)
        binary='1'+'0'*(length-1-le)+temp        
    return binary


global Reg,Mem,operation,rd,rs1,rs2,imm
#register File
Reg=[0 for j in range(32)]

#memory
Mem=[0]*4000


def readFile(PC):
    #should return a line every time it is caled 
    contents = Mem[PC:PC+16]
    return contents
def saveFile(PC,ALUout):
    for i, val in enumerate(ALUout):
        Mem[PC +i] = val
    
def fetch(inst):
    Reg[0],temp=[int(x) for x in inst.split()]
    return temp

def decode(s):
    opcode=s[-7:-1]
    rd=s[-12:-8]
    func3=s[-15:-13]
    rs1=s[-20:-16]
    rs2=s[-25:-21]
    func7=s[-32:-26]
    if(opcode=="0110011"):
        if(opcode=="0110011"):
            if(func3=="000" && func7=="0000000"):
                operation="add"
            elif(func3=="000" && func7=="0100000"):
                operation="sub"
            elif(func3=="001"):
                operation="sll"
            elif(func3=="010"):
                operation="slt"
            elif(func3=="011"):
                operation="sltu"
            elif(func3=="100"):
                operation="xor"
            elif(func3=="101" && func7=="0000000"):
                operation="slr"
            elif(func3=="101" && func7=="0100000"):
                operation="sra"
            elif(func3=="110"):
                operation="or"
            elif(func3=="111"):
                operation="and"
            elif(func3=="000" && func7=="0000001"):
                operation="mul"
            elif(func3=="100" && func7=="0000001"):
                operation="div"
            elif(func3=="110" && func7=="0000001"):
                operation="rem"
    elif(opcode=="0010011"):
        imm=func7+rs2
        if(func3=="000"):
            operation="addi"
        elif(func3=="110"):
            operation="ori"
        elif(func3=="111"):
            operation="andi"
    elif(opcode=="0000011"):
        imm=func7+rs2
        if(func3=="000"):
            operation="lb"
        elif(func3=="001"):
            operation="lh"
        elif(func3=="010"):
            operation="lw"
    elif(opcode=="1100111"):
        imm=func7+rs2
        if(func3=="000"):
            operation="jalr"
    elif(opcode=="0100011"):
        imm=func7+rd
        if(func3=="000"):
            operation="sb"
        elif(func3=="001"):
            operation="sh"
        elif(operation=="010"):
            operation="sw"
    elif(opcode=="1100011"):
        imm=func7+rd
        if(func3=="000"):
            operation="beq"
        elif(func3=="001"):
            operation="bne"
        elif(func3=="101"):
            operation="bge"
        elif(func3=="100"):
            operation="blt"
    elif(opcode=="0010111"):
        imm=func7+rs2+rs1+func3
        operation="auipc"
    elif(opcode=="0110111"):
        imm=func7+rs2+rs1+func3
        operation="lui"
    elif(opcode=="1101111"):
        imm=func7+rs2+rs1+func3
        operation="jal"

def execute(arg1,arg2,ALU_control):
    '''
    0: signed addition
    1: bitwise AND
    2: bitwise OR
    3: SLL
    4: SLT
    5: SRA
    6: SRl
    7: SUB
    8: XOR
    9: MUL
    10: DIV
    11: REM
    12: unsigned addition
    '''
    if ALU_control==0:
        return arg1+arg2
    if ALU_control==1:
        return arg1&arg2
    if ALU_control==2:
        return arg1|arg2
    if ALU_control==3:
        temp=bin(arg1).replace('0b','')
        temp=temp[arg2:]
        temp=int(temp,base=2)
        return temp
    if ALU_control==4:
        return 1 if arg1<arg2 else 0
        pass
    if ALU_control==5:
        temp=bin(arg1).replace('0b', '')
        temp=temp[:-arg2]
        temp='1'*arg2 +temp
        return int(temp)
    if ALU_control==6:
        temp=bin(arg1).replace('0b', '')
        temp=temp[:-arg2]
        temp='0'*arg2 +temp
        return int(temp)
    if ALU_control==7:
        return arg1-arg2
    if ALU_control==8:
        return arg1^arg2
    if ALU_control==9:
        return arg1*arg2
    if ALU_control==10:
       if arg2==0: #convetion
           return bintodec('1'*32)
       return arg1//arg2
    if ALU_control==11:
        return arg1%arg2
    if ALU_control==12:
        return bin(int(arg1)+int(arg2)).replace('0b','')

def memoryAcess(PC,ALUout,opcode):
    if(str(opcode) == "0000011"):
        return readFile(PC)
    elif(str(opcode) == "0100011"):
        saveFile(ALUout,PC)
    else:
       return -1 

def writeback(data,rm,PC):   #data from memory ,# rm  from excute for ALU instructions ,# rd destination register 
    if(operation =="add" or operation=="slt" or operation=="and" or operation =="or" or operation=="sll" or operation=="sra" or operation=="mul"):
        Reg[rd]=rm
    elif(operation== "srl" or operation=="sub" or operation=="xor" or operation=="div" or operation=="rem" or operation=="addi" or operation=="andi" or operation=="ori"):
        Reg[rd]=rm
    elif(operation=="lb" or operation=="ld" or operation=="lh" or operation=="lw"):
        Reg[rd]=data
    elif(operation=="jalr" or operation=="jal"):
        Reg[rd]=PC
    elif(operation=="lui" or operation=="auipc"):
        Reg[rd]=rm
        
def setToStart():
    #restores the registers to the original state
    pass

def storeState():
    #creates a file which stores the current state of Registers and Memory
    pass

def run_RISCVsim():
    #put it all together
    pass
