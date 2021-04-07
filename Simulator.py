global Reg,Mem,PC,IR,rs1,rs2,rd,imm,operation

def readFile(file):
    File=open(file,'r')
    global MachineCode
    MachineCode=[]
    while True:
        inst=File.readline()
        if inst:
            _,inst=inst.split()
            inst=bin(int(inst,base=16))
            MachineCode.append(inst)
        else:
            break
    File.close()

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


PC=0
#register File
Reg=['0' for j in range(32)]

#memory
Mem=['0'*32]*4000

    
def fetch():
    global IR,PC
    IR=MachineCode[PC//4]
    PC+=4
def decode():
    global rs1,rs2,rd,imm,operation
    operation=''
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
        print("the machine code is decoded successfully", "instruction is=" operation)

def execute():
    global PC,ALU_output,operation
    ALU_output=''
    arg1=int(rs1,base=2)
    arg2=int(rs2,base=2)
    if operation=="add":
        ALU_output=dectobin(bintodec(Reg[arg1])+bintodec(Reg[arg2]),32)
    if operation=="sub":
        ALU_output=dectobin(bintodec(Reg[arg1])-bintodec(Reg[arg2]),32)    
    if operation=="sll":
        shif=bintodec(Reg[arg2])
        temp=Reg[arg1][shif:]+'0'*shif
        ALU_output=temp
    if operation=="slt":
        r1=bintodec(Reg[arg1])
        r2=bintodec(Reg[arg2])
        ALU_output=1 if r1<r2 else 0
    if operation=="sltu":
        ALU_output=1 if int(r1,base=2)<int(r2,base=2) else 0
    if operation=="xor":
        ALU_output=dectobin(bintodec(Reg[arg1])^bintodec(Reg[arg2]),32)
    if operation=="srl":
        shif=bintodec(Reg[arg2])
        temp='0'*shif+Reg[arg1][:-shif]
        ALU_output=temp
    if operation=="sra":
        shif=bintodec(Reg[arg2])
        temp='1'*shif+Reg[arg1][:-shif]
        ALU_output=temp
    if operation=="or":
        temp=bintodec(Reg[arg1])|bintodec(Reg[arg2])
        ALU_output=dectobin(temp, 32)
    if operation=="and":
        temp=bintodec(Reg[arg1])&bintodec(Reg[arg2])
        ALU_output=dectobin(temp,32)
    if operation=="mul":
        temp=bintodec(Reg[arg1]) * bintodec(Reg[arg2])
        ALU_output=dectobin(temp,32)
    if operation=="div":
        temp=bintodec(Reg[arg1]) // bintodec(Reg[arg2])
        ALU_output=dectobin(temp,32)        
    if operation=="rem":
        temp=bintodec(Reg[arg1]) % bintodec(Reg[arg2])
        ALU_output=dectobin(temp,32)
    if operation=="addi":
        temp=bintodec(Reg[arg1])+bintodec(imm)
        ALU_output=dectobin(temp,32)
    if operation=="ori":
        temp=bintodec(Reg[arg1])|bintodec(imm)
        ALU_output=dectobin(temp,32)
    if operation=="andi":
        temp=bintodec(Reg[arg1])&bintodec(imm)
        ALU_output=dectobin(temp,32)
    if operation in ["lb","lw","lh","sb","sh","sw"]:
        temp=bintodec(Reg[rs1])+bintodec(imm)
        ALU_output=dectobin(temp,32)
    if operation=="jalr":
        temp=bintodec(Reg[rs1])+bintodec(imm)
        temp2=PC
        PC=temp
        ALU_output=temp2
    if operation in ["beg","bne","bge","blt","auipc"]:
        PC+=bintodec(imm)
    if operation=="lui":
        ALU_output=imm
    if operation=="jal":
        temp=bintodec(imm)
        temp2=PC
        PC=temp
        ALU_ouput=temp2
        print("the program is executed successfully", "the output after ALU operations done:" ALU_output )
def memoryAcess():
    global PC,ALU_output,operation,MDR
    ALu_output = bintodec(ALU_output)
    val = ALu_output%32
    MDR = ''
    if operation == "lw":
        for i in range(32):
            MDR+= Mem[Alu_output//32][ALu_output%32]
    elif operation == "lh":
         for i in range(16):
            MDR+= Mem[Alu_output//32][ALu_output%32]
            ALu_output+=1
    elif operation  == "lb":
         for i in range(8):
            MDR+= Mem[Alu_output//32][ALu_output%32]
            ALu_output+=1
    elif operation  == "sb":
         if val <=24:
             contents = Mem[ALu_output//32]
              k = contents[:val] + rs2 + contents[val + 8:]
              Mem[ALu_output//32] = k
          else:
              contents1= Mem[ALu_output//32]
              contents2 = Mem[ALu_output//32+1]
              a = 32 - val 
              b = 2 * val - 32
              k1 = contents1[:val] + rs2[:a]
              k2 = rs2[-b:] + contents2[b:]
              Mem[ALu_output//32] = k1
              Mem[ALu_output//32+1] = k2
    elif operation  == "sh":
         if val <=16:
              contents = Mem[ALu_output//32]
              k = contents[:val] + rs2 + contents[val + 8:]
              Mem[ALu_output//32] = k
          else:
              contents1= Mem[ALu_output//32]
              contents2 = Mem[ALu_output//32+1]
              a = 32 - val 
              b = 2 * val - 32
              k1 = contents1[:val] + rs2[:a]
              k2 = rs2[-b:] + contents2[b:]
              Mem[ALu_output//32] = k1
              Mem[ALu_output//32+1] = k2
    elif operation  == "sw":
          if val <=0:
             contents = Mem[ALu_output//32]
             k = contents[:val] + rs2 + contents[val + 16:]
             Mem[ALu_output//32] = k
          else:
             contents1= Mem[ALu_output//32]
             contents2 = Mem[ALu_output//32+1]
             a = 32 - val 
             b = 2 * val - 32
             k1 = contents1[:val] + rs2[:a]
             k2 = rs2[-b:] + contents2[b:]
             Mem[ALu_output//32] = k1
             Mem[ALu_output//32+1] = k2
            
    else:
        return 

def writeback(data):  #data from memory ,#   from excute for ALU instructions ,# rd destination register 
    rd1=int(rd,base=2)
    if(operation =="add" or operation=="slt" or operation=="and" or operation =="or" or operation=="sll" or operation=="sra" or operation=="mul"):
        Reg[rd1]=ALU_output
    elif(operation== "srl" or operation=="sub" or operation=="xor" or operation=="div" or operation=="rem" or operation=="addi" or operation=="andi" or operation=="ori"):
        Reg[rd1]=ALU_output
    elif(operation=="lb" or operation=="ld" or operation=="lh" or operation=="lw"):
        Reg[rd1]=data
    elif(operation=="jalr" or operation=="jal"):
        Reg[rd1]=PC
    elif(operation=="lui" or operation=="auipc"):
        Reg[rd1]=ALU_output
        print("Memory write successful")
        
def setToStart():
    #restores the registers to the original state
    pass

def storeState():
    #creates a file which stores the current state of Registers and Memory
    pass

def run_RISCVsim():
    fetch()
    decode()
    execute()
    memoryAcess()
    writeback()
