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


global Reg,Mem
#register File
Reg=['0' for j in range(32)]

#memory
Mem=['0'*32]*4000


def readFile(PC):
    #should return a line every time it is caled 
    contents = Mem[PC:PC+16]
    return contents
def saveFile(PC,ALUout):
    for i, val in enumerate(ALUout):
        Mem[PC +i] = val
    
def fetch(inst):
    global IR,PC
    Reg[0],temp=[int(x) for x in inst.split()]
    return temp
def decode():
    global rs1,rs2,rd,imm,operation
    opcode=IR[-7:]
    rd=IR[-12:-7]
    func3=IR[-15:-12]
    rs1=IR[-20:-15]
    rs2=IR[-25:-20]
    func7=IR[-32:-25]
    if(opcode=="0110011"):
        if(opcode=="0110011"):
            if(func3=="000" and func7=="0000000"):
                operation="add"
            elif(func3=="000" and func7=="0100000"):
                operation="sub"
            elif(func3=="001"):
                operation="sll"
            elif(func3=="010"):
                operation="slt"
            elif(func3=="011"):
                operation="sltu"
            elif(func3=="100"):
                operation="xor"
            elif(func3=="101" and func7=="0000000"):
                operation="slr"
            elif(func3=="101" and func7=="0100000"):
                operation="sra"
            elif(func3=="110"):
                operation="or"
            elif(func3=="111"):
                operation="and"
            elif(func3=="000" and func7=="0000001"):
                operation="mul"
            elif(func3=="100" and func7=="0000001"):
                operation="div"
            elif(func3=="110" and func7=="0000001"):
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
        imm=func7[0]+rd[-1]+func7[1:]+rd[0:-1]+"0"
        if(func3=="000"):
            operation="beq"
        elif(func3=="001"):
            operation="bne"
        elif(func3=="101"):
            operation="bge"
        elif(func3=="100"):
            operation="blt"
    elif(opcode=="0010111"):
        imm=func7+rs2+rs1+func3+"000000000000"
        operation="auipc"
    elif(opcode=="0110111"):
        imm=func7+rs2+rs1+func3+"000000000000"
        operation="lui"
    elif(opcode=="1101111"):
        imm=func7[0]+rs1+func3+rs2[-1]+func7[1:]+rs2[:-1]+"0"
        operation="jal"

def execute():
    global PC
    arg1=int(rs1,base=2)
    arg2=int(rs2,base=2)
    if operation=="add":
        return dectobin(bintodec(Reg[arg1])+bintodec(Reg[arg2]),32)
    if operation=="sub":
        return dectobin(bintodec(Reg[arg1])-bintodec(Reg[arg2]),32)    
    if operation=="sll":
        shif=bintodec(Reg[arg2])
        temp=Reg[arg1][shif:]+'0'*shif
        return temp
    if operation=="slt":
        r1=bintodec(Reg[arg1])
        r2=bintodec(Reg[arg2])
        return 1 if r1<r2 else 0
    if operation=="sltu":
        return 1 if int(r1,base=2)<int(r2,base=2) else 0
    if operation=="xor":
        return dectobin(bintodec(Reg[arg1])^bintodec(Reg[arg2]),32)
    if operation=="srl":
        shif=bintodec(Reg[arg2])
        temp='0'*shif+Reg[arg1][:-shif]
        return temp
    if operation=="sra":
        shif=bintodec(Reg[arg2])
        temp='1'*shif+Reg[arg1][:-shif]
        return temp
    if operation=="or":
        temp=bintodec(Reg[arg1])|bintodec(Reg[arg2])
        return dectobin(temp, 32)
    if operation=="and":
        temp=bintodec(Reg[arg1])&bintodec(Reg[arg2])
        return dectobin(temp,32)
    if operation=="mul":
        temp=bintodec(Reg[arg1]) * bintodec(Reg[arg2])
        return dectobin(temp,32)
    if operation=="div":
        temp=bintodec(Reg[arg1]) // bintodec(Reg[arg2])
        return dectobin(temp,32)        
    if operation=="rem":
        temp=bintodec(Reg[arg1]) % bintodec(Reg[arg2])
        return dectobin(temp,32)
    if operation=="addi":
        temp=bintodec(Reg[arg1])+bintodec(imm)
        return dectobin(temp,32)
    if operation=="ori":
        temp=bintodec(Reg[arg1])|bintodec(imm)
        return dectobin(temp,32)
    if operation=="andi":
        temp=bintodec(Reg[arg1])&bintodec(imm)
        return dectobin(temp,32)
    if operation in ["lb","lw","lh","sb","sh","sw"]:
        temp=bintodec(Reg[rs1])+bintodec(imm)
        return dectobin(temp,32)
    if operation=="jalr":
        temp=bintodec(Reg[rs1])+bintodec(imm)
        temp2=PC+4
        PC=temp
        return temp2
    if operation in ["beg","bne","bge","blt","auipc"]:
        PC+=bintodec(imm)
    if operation in ["lui","jal"]:
        return imm
    
def memoryAcess(PC,ALUout,opcode):
    if(str(opcode) == "0000011"):
        return readFile(PC)
    elif(str(opcode) == "0100011"):
        saveFile(ALUout,PC)
    else:
       return -1 

def writeback(data,rm,PC):  #data from memory ,# rm  from excute for ALU instructions ,# rd destination register 
    rd1=int(rd,base=2)
    if(operation =="add" or operation=="slt" or operation=="and" or operation =="or" or operation=="sll" or operation=="sra" or operation=="mul"):
        Reg[rd1]=rm
    elif(operation== "srl" or operation=="sub" or operation=="xor" or operation=="div" or operation=="rem" or operation=="addi" or operation=="andi" or operation=="ori"):
        Reg[rd1]=rm
    elif(operation=="lb" or operation=="ld" or operation=="lh" or operation=="lw"):
        Reg[rd1]=data
    elif(operation=="jalr" or operation=="jal"):
        Reg[rd1]=PC
    elif(operation=="lui" or operation=="auipc"):
        Reg[rd1]=rm
        
def setToStart():
    #restores the registers to the original state
    pass

def storeState():
    #creates a file which stores the current state of Registers and Memory
    pass

def run_RISCVsim():
    #put it all together
    pass

