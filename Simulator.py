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


global Reg,Mem,ControlSignals
#register File
Reg=[0 for j in range(32)]

#memory
Mem=[0]*4000

#Control Signals
#A dictionary for holding the control signals
#use keys like MUXB, MUXY,RY,RZ (same as in lectures) for uniformity
ControlSignals={}
def readFile(K):
    #should return a line every time it is caled 
    return K.readline()

def fetch(inst):
    Reg[0],temp=[int(x) for x in inst.split()]
    return temp

def decode():
    #should update the CONTROL_SIGNALS
    pass
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

def memoryAcess():
    pass

def writeBack():
    pass

def setToStart():
    #restores the registers to the original state
    pass

def storeState():
    #creates a file which stores the current state of Registers and Memory
    pass

def run_RISCVsim():
    #put it all together
    pass
