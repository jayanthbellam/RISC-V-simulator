
def readFile(file):
    File=open(file,'r')
    global MachineCode
    MachineCode=[]
    while True:
        inst=File.readline()
        try:
            _,inst=inst.split()
            inst=bin(int(inst,base=16)).replace('0b','')
            inst='0'*(32-len(inst))+inst
            MachineCode.append(inst)
        except ValueError:
            break
    while True:
        inst=File.readline()
        if inst:
            key,val=inst.split()
            val=bin(int(val,base=16)).replace('0b','')
            val='0'*(32-len(val))+val
            Mem[hex(int(key,base=16))]=val
        else:
            break
    File.close()

def bintodec(binary):
    length=len(binary)
    number=int(binary,base=2)
    if binary[0]=='0':
        return number
    return number-2**(length)

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

#register File
Reg=['0'*32 for j in range(32)]

#memory
Mem={}

    
def fetch(PC):
    IR=MachineCode[PC//4]
    PC+=4
    print("The instruction is "+str(hex(int(IR,2))))
    print("PC incremented from "+str(PC-4)+" to "+str(PC))
    return PC,IR
def decode(IR):
    operation=''
    opcode=IR[-7:]
    rd=IR[-12:-7]
    func3=IR[-15:-12]
    rs1=IR[-20:-15]
    rs2=IR[-25:-20]
    func7=IR[:7]
    arg1=int(rs1,base=2)
    arg2=int(rs2,base=2)
    ret=int(rd,base=2)
    arguments={'rs1':rs1,'rs2':rs2,'rd':rd,'imm':'0'}
    if(opcode=="0110011"):
        if(func3=="000" and func7=="0000000"):
            operation="add"
            print("The operation is "+operation+". Rs1: x"+str(arg1)+" Rs2: x"+str(arg2)+" Rd: "+str(ret))
            return operation,arguments
        elif(func3=="000" and func7=="0100000"):
            operation="sub"
            print("The operation is "+operation+". Rs1: x"+str(arg1)+" Rs2: x"+str(arg2)+" Rd: "+str(int(rd,base=2)))
            return operation,arguments
        elif(func3=="001"):
            operation="sll"
            print("The operation is "+operation+". Rs1: x"+str(arg1)+" Rs2: x"+str(arg2)+" Rd: "+str(int(rd,base=2)))
            return operation,arguments
        elif(func3=="010"):
            operation="slt"
            print("The operation is "+operation+". Rs1: x"+str(arg1)+" Rs2: x"+str(arg2)+" Rd: "+str(int(rd,base=2)))
            return operation,arguments
        elif(func3=="011"):
            operation="sltu"
            print("The operation is "+operation+". Rs1: x"+str(arg1)+" Rs2: x"+str(arg2)+" Rd: "+str(int(rd,base=2)))
            return operation,arguments
        elif(func3=="100"):
            operation="xor"
            print("The operation is "+operation+". Rs1: x"+str(arg1)+" Rs2: x"+str(arg2)+" Rd: "+str(int(rd,base=2)))
            return operation,arguments
        elif(func3=="101" and func7=="0000000"):
            operation="srl"
            print("The operation is "+operation+". Rs1: x"+str(arg1)+" Rs2: x"+str(arg2)+" Rd: "+str(int(rd,base=2)))
            return operation,arguments
        elif(func3=="101" and func7=="0100000"):
            operation="sra"
            print("The operation is "+operation+". Rs1: x"+str(arg1)+" Rs2: x"+str(arg2)+" Rd: "+str(int(rd,base=2)))
            return operation,arguments
        elif(func3=="110"):
            operation="or"
            print("The operation is "+operation+". Rs1: x"+str(arg1)+" Rs2: x"+str(arg2)+" Rd: "+str(int(rd,base=2)))
            return operation,arguments
        elif(func3=="111"):
            operation="and"
            print("The operation is "+operation+". Rs1: x"+str(arg1)+" Rs2: x"+str(arg2)+" Rd: "+str(int(rd,base=2)))
            return operation,arguments
        elif(func3=="000" and func7=="0000001"):
            operation="mul"
            print("The operation is "+operation+". Rs1: x"+str(arg1)+" Rs2: x"+str(arg2)+" Rd: "+str(int(rd,base=2)))
            return operation,arguments
        elif(func3=="100" and func7=="0000001"):
            operation="div"
            print("The operation is "+operation+". Rs1: x"+str(arg1)+" Rs2: x"+str(arg2)+" Rd: "+str(int(rd,base=2)))
            return operation,arguments
        elif(func3=="110" and func7=="0000001"):
            operation="rem"
            print("The operation is "+operation+". Rs1: x"+str(arg1)+" Rs2: x"+str(arg2)+" Rd: "+str(int(rd,base=2)))
            return operation,arguments
    elif(opcode=="0010011"):
        imm=func7+rs2
        if(func3=="000"):
            operation="addi"
            print("The operation is "+operation+". Rs1: "+str(arg1)+" Rd: "+str(int(rd,base=2))+" imm: "+str(bintodec(imm)))
            arguments['imm']=imm
            return operation,arguments
        elif(func3=="110"):
            operation="ori"
            print("The operation is "+operation+". Rs1: "+str(arg1)+" Rd: "+str(int(rd,base=2))+" imm: "+str(bintodec(imm)))
            arguments['imm']=imm
            return operation,arguments
        elif(func3=="111"):
            operation="andi"
            print("The operation is "+operation+". Rs1: "+str(arg1)+" Rd: "+str(int(rd,base=2))+" imm: "+str(bintodec(imm)))
            arguments['imm']=imm
            return operation,arguments
    elif(opcode=="0000011"):
        imm=func7+rs2
        if(func3=="000"):
            operation="lb"
            print("The operation is "+operation+". Rs1: "+str(arg1)+" Rd: "+str(int(rd,base=2))+" imm: "+str(bintodec(imm)))
            arguments['imm']=imm
            return operation,arguments
        elif(func3=="001"):
            operation="lh"
            print("The operation is "+operation+". Rs1: "+str(arg1)+" Rd: "+str(int(rd,base=2))+" imm: "+str(bintodec(imm)))
            arguments['imm']=imm
            return operation,arguments
        elif(func3=="010"):
            operation="lw"
            print("The operation is "+operation+". Rs1: "+str(arg1)+" Rd: "+str(int(rd,base=2))+" imm: "+str(bintodec(imm)))
            arguments['imm']=imm
            return operation,arguments
    elif(opcode=="1100111"):
        imm=func7+rs2
        if(func3=="000"):
            operation="jalr"
            print("The operation is "+operation+". Rs1: "+str(arg1)+" Rd: "+str(int(rd,base=2))+" imm: "+str(bintodec(imm)))
            arguments['imm']=imm
            return operation,arguments
    elif(opcode=="0100011"):
        imm=func7+rd
        if(func3=="000"):
            operation="sb"
            print("The operation is "+operation+". Rs1: "+str(arg1)+" Rs2: "+str(arg2)+" imm: "+str(bintodec(imm)))
            arguments['imm']=imm
            return operation,arguments
        elif(func3=="001"):
            operation="sh"
            print("The operation is "+operation+". Rs1: "+str(arg1)+" Rs2: "+str(arg2)+" imm: "+str(bintodec(imm)))
            arguments['imm']=imm
            return operation,arguments
        elif(func3=="010"):
            operation="sw"
            print("The operation is "+operation+". Rs1: "+str(arg1)+" Rs2: "+str(arg2)+" imm: "+str(bintodec(imm)))
            arguments['imm']=imm
            return operation,arguments
    elif(opcode=="1100011"):
        imm=func7[0]+rd[-1]+func7[1:]+rd[0:-1]+"0"
        if(func3=="000"):
            operation="beq"
            print("The operation is "+operation+". Rs1: "+str(arg1)+" Rs2: "+str(bintodec(rs2))+" imm: "+str(bintodec(imm)))
            arguments['imm']=imm
            return operation,arguments
        elif(func3=="001"):
            operation="bne"
            print("The operation is "+operation+". Rs1: "+str(arg1)+" Rs2: "+str(bintodec(rs2))+" imm: "+str(bintodec(imm)))
            arguments['imm']=imm
            return operation,arguments
        elif(func3=="101"):
            operation="bge"
            print("The operation is "+operation+". Rs1: "+str(arg1)+" Rs2: "+str(bintodec(rs2))+" imm: "+str(bintodec(imm)))
            arguments['imm']=imm
            return operation,arguments
        elif(func3=="100"):
            operation="blt"
            print("The operation is "+operation+". Rs1: "+str(arg1)+" Rs2: "+str(bintodec(rs2))+" imm: "+str(bintodec(imm)))
            arguments['imm']=imm
            return operation,arguments
    elif(opcode=="0010111"):
        imm=func7+rs2+rs1+func3+"000000000000"
        operation="auipc"
        print("The operation is "+operation+" Rd: "+str(int(rd,base=2))+" imm: "+str(bintodec(imm)))
        arguments['imm']=imm
        return operation,arguments
    elif(opcode=="0110111"):
        imm=func7+rs2+rs1+func3+"000000000000"
        operation="lui"
        print("The operation is "+operation+" Rd: "+str(int(rd))+" imm: "+str(bintodec(imm)))
        arguments['imm']=imm
        return operation,arguments
    elif(opcode=="1101111"):
        imm=func7[0]+rs1+func3+rs2[-1]+func7[1:]+rs2[:-1]+"0"
        operation="jal"
        print("The operation is "+operation+" Rd: "+str(int(rd,base=2))+" imm: "+str(bintodec(imm)))
        arguments['imm']=imm
        return operation,arguments
    print("Invalid Operation")

def execute(operation,arguments,PC):
    ALU_output=''
    arg1=int(arguments['rs1'],base=2)
    arg2=int(arguments['rs2'],base=2)
    imm=arguments['imm']
    if operation=="add":
        ALU_output=dectobin(bintodec(Reg[arg1])+bintodec(Reg[arg2]),32)
        print(operation+" of x" +str(arg1)+" and x"+str(arg2)+" is "+str(bintodec(ALU_output)))
    elif operation=="sub":
        ALU_output=dectobin(bintodec(Reg[arg1])-bintodec(Reg[arg2]),32)
        print(operation+" of x"+str(arg1)+" and x"+str(arg2)+" is "+str(bintodec(ALU_output)))
    elif operation=="sll":
        shif=bintodec(Reg[arg2])
        temp=Reg[arg1][shif:]+'0'*shif
        ALU_output=temp
        print(operation+" of x"+str(arg1)+" and x"+str(arg2)+" is "+str(bintodec(ALU_output)))
    elif operation=="slt":
        r1=bintodec(Reg[arg1])
        r2=bintodec(Reg[arg2])
        ALU_output=1 if r1<r2 else 0
        print(operation+" of x"+str(arg1)+" and x"+str(arg2)+" is "+str(bintodec(ALU_output)))
    elif operation=="sltu":
        ALU_output=1 if int(Reg[arg1],base=2)<int(Reg[arg2],base=2) else 0
        print(operation+" of x"+str(arg1)+" and x"+str(arg2)+" is "+str(bintodec(ALU_output)))
    elif operation=="xor":
        ALU_output=dectobin(bintodec(Reg[arg1])^bintodec(Reg[arg2]),32)
        print(operation+" of x"+str(arg1)+" and x"+str(arg2)+" is "+str(bintodec(ALU_output)))
    elif operation=="srl":
        shif=bintodec(Reg[arg2])
        temp='0'*shif+Reg[arg1][:-shif]
        ALU_output=temp
        print(operation+" of x"+str(arg1)+" and x"+str(arg2)+" is "+str(bintodec(ALU_output)))
    elif operation=="sra":
        shif=bintodec(Reg[arg2])
        temp='1'*shif+Reg[arg1][:-shif]
        ALU_output=temp
        print(operation+" of x"+str(arg1)+" and x"+str(arg2)+" is "+bintodec(ALU_output))
    elif operation=="or":
        temp=bintodec(Reg[arg1])|bintodec(Reg[arg2])
        ALU_output=dectobin(temp, 32)
        print(operation+" of x"+str(arg1)+" and x"+str(arg2)+" is "+str(bintodec(ALU_output)))
    elif operation=="and":
        temp=bintodec(Reg[arg1])&bintodec(Reg[arg2])
        ALU_output=dectobin(temp,32)
        print(operation+" of x"+str(arg1)+" and x"+str(arg2)+" is "+str(bintodec(ALU_output)))
    elif operation=="mul":
        temp=bintodec(Reg[arg1]) * bintodec(Reg[arg2])
        ALU_output=dectobin(temp,32)
        print(operation+" of x"+str(arg1)+" and x"+str(arg2)+" is "+str(bintodec(ALU_output)))
    elif operation=="div":
        temp=bintodec(Reg[arg1]) // bintodec(Reg[arg2])
        ALU_output=dectobin(temp,32) 
        print(operation+" of x"+str(arg1)+" and x"+str(arg2)+" is "+str(bintodec(ALU_output)))
    elif operation=="rem":
        temp=bintodec(Reg[arg1]) % bintodec(Reg[arg2])
        ALU_output=dectobin(temp,32)
        print(operation+" of x"+str(arg1)+" and x"+str(arg2)+" is "+str(bintodec(ALU_output)))
    elif operation=="addi":
        temp=bintodec(Reg[arg1])+bintodec(imm)
        ALU_output=dectobin(temp,32)
        print(operation+" of x"+str(arg1)+" and "+str(bintodec(imm))+" is "+str(bintodec(ALU_output)))
    elif operation=="ori":
        temp=bintodec(Reg[arg1])|bintodec(imm)
        ALU_output=dectobin(temp,32)
        print(operation+" of x"+str(arg1)+" and "+str(bintodec(imm))+" is "+str(bintodec(ALU_output)))
    elif operation=="andi":
        temp=bintodec(Reg[arg1])&bintodec(imm)
        ALU_output=dectobin(temp,32)
        print(operation+" of x"+str(arg1)+" and "+str(bintodec(imm))+" is "+str(bintodec(ALU_output)))
    elif operation in ["lb","lw","lh","sb","sh","sw"]:
        temp=int(Reg[arg1],2)+bintodec(imm)
        ALU_output=dectobin(temp,32)
        print("The effective address for "+operation+" is "+str(bintodec(ALU_output)))
    elif operation=="jalr":
        temp=int(Reg[arg1],base=2)+bintodec(imm)
        temp2=bin(PC).replace('0b','')
        PC=temp
        ALU_output=temp2
        print("The effective address for "+operation+" is "+str(bintodec(ALU_output)))
        print("The PC has been changed to "+str(PC))
    elif operation=="beq":
        if Reg[arg1]==Reg[arg2]:
            PC+=bintodec(imm)-4
            print("The condition is true")
            print("The PC has been updated to "+str(PC))
        else:
            print("The condition is false.")
    elif operation=="bne":
        if Reg[arg1]!=Reg[arg2]:
            PC+=bintodec(imm)-4
            print("The condition is true")
            print("The PC has been updated to "+str(PC))
        else:
            print("The condition is false.")
    elif operation=="bge":
        if Reg[arg1]>=Reg[arg2]:
            PC+=bintodec(imm)-4
            print("The condition is true")
            print("The PC has been updated to "+str(PC))
        else:
            print("The condition is false.")
    elif operation=="blt":
        if Reg[arg1]<Reg[arg2]:
            PC+=bintodec(imm)-4
            print("The condition is true")
            print("The PC has been updated to "+str(PC))
        else:
            print("The condition is false.")
    elif operation =="auipc":
        PC+=bintodec(imm)-4
        print("The effective address for "+operation+" is "+str(bintodec(ALU_output)))
    elif operation=="lui":
        ALU_output=imm
        print(operation+" is done")
    elif operation=="jal":
        temp=bintodec(imm)
        temp2=bin(PC).replace('0b','')
        PC+=temp-4
        ALU_output='0'*(32-len(temp2))+temp2
        print(operation+" is done")
    return ALU_output

def memoryAcess(operation,ALU_output,arguments):
    if not ALU_output:
        return 0
    ALu_output = int(ALU_output,base=2)
    key=hex(ALu_output)
    rs2=arguments['rs2']
    MDR = ''
    if operation=="lw":
        try:
            MDR=Mem[key]
        except KeyError:
            MDR='0'*32
        print("we retrieved the word of value:"+str(bintodec(MDR))+"at memory address:"+str(int(ALU_output,base=2)))
    elif operation=="lh":
        try:
            MDR='0'*16 + Mem[key][:16]
        except KeyError:
            MDR='0'*32
        print("we retrieved the halfword of value:"+str(bintodec(MDR))+"at memory address:"+str(int(ALU_output,base=2)))
    elif operation=="lb":
        try:
            MDR='0'*24 + Mem[key][:8]
        except KeyError:
            MDR='0'*32
        print("we retrieved the byte of value:"+str(bintodec(MDR))+"at memory address:"+str(int(ALU_output,base=2)))
    elif operation=="sw":
        Mem[key]=Reg[int(rs2,2)]
        print("We stored the word "+Reg[int(rs2,2)]+" at the address"+str(key))
    elif operation=="sh":
        Mem[key]='0'*16+Reg[int(rs2,2)][:16]
        print("We stored the halfword "+Reg[int(rs2,2)][:16]+" at the address"+str(key))
    elif operation=="sb":
        Mem[key]='0'*24+Reg[int(rs2,2)][:8]
        print("We stored the byte "+Reg[int(rs2,2)][:8]+" at the address"+str(key))
    return MDR


def writeback(operation,arguments,MDR,ALU_output):  #data from memory ,#   from excute for ALU instructions ,# rd destination register 
    rd=arguments['rd']
    rd1=int(rd,base=2)
    if rd1==0:
        return
    if(operation in ["add","slt","and","or","sll","sra","mul","srl","sub","xor","div","rem","addi","andi","ori"]):
        Reg[rd1]=ALU_output
        print("the result "+str(bintodec(ALU_output))+" is updated in the register x"+str(rd1))
    elif operation in ["lb,lh,lw"]:
        Reg[rd1]=MDR
        print("the result "+str(int(MDR,base=2))+" is updated in the register x"+str(rd1))
    elif operation in ["jalr","jal","lui","auipc"]:
        Reg[rd1]=ALU_output
        print("The result "+str(int(ALU_output,base=2))+" is updated in the register x"+str(rd1))

def setToStart():
    global Reg,Mem
    Reg=['0'*32]*32
    Mem={}
    Reg[2]='01111111111111111111111111110000'
    Reg[3]='00010000000000000000000000000000'

def storeState():
    global Reg,Mem
    f=open("store.txt","w+")
    f.write("Registers\n")
    for i in range(32):
        f.write("x"+str(i)+":"+hex(int(Reg[i],2)))         #Registers: 0000..... 0000....1 ......
        f.write("\n")            #Memory:00.000 0012.. 
    f.write("\n\n")
    f.write("Memory\n")
    for key in Mem.keys():
        f.write(str(key)+" "+str(hex(int(Mem[key],2))))
        f.write('\n')
    f.close()    
       
def run_RISCVsim():
    instructions=len(MachineCode)
    count=0
    PC=0
    while PC<=(instructions-1)*4:
        PC,IR=fetch(PC)
        operation,arguments=decode(IR)
        ALU_output=execute(operation,arguments,PC)
        MDR=memoryAcess(operation,ALU_output,arguments)
        writeback(operation,arguments,MDR,ALU_output)
        count+=1
        input()
    storeState()
    print("The total number of clock cycles used ",count)
