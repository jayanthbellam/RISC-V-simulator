class State:
    def __init__(self,pc):
        self.operation=-1
        self.opcode=-1
        self.rs1=-1
        self.rs2=-1
        self.rd=-1
        self.imm=-1
        self.PC=pc
        self.PC_temp=0
        self.IR=0
        self.MDR=0
        self.Alu_out=0
        self.is_actual_instruction=False

class ControlUnit:
    def __init__(self,file_name):
        self.MEM={}
        self.MachineCode=[]
        self.RegisterFile=[0 for i in range(32)]
        self.RegisterFile[2]=int('0x7FFFFFF0',16)
        self.RegisterFile[3]=int('0x10000000',16)
        self.count_mem_ins=0
        self.count_ins=0
        self.count_control_ins=0
        self.stalls=0
        self.branch_mispred=0
        self._program_memory(file_name)

    def _program_emmory(self,file_name):
        File=open(file_name)
        while True:
            inst=File.readline()
            try:
                _,inst=inst.split()
                inst=int(inst,16)
                self.MachineCode.append(inst)
            except ValueError:
                break
        while True:
            inst=File.readline()
            if inst:
                key,val=inst.split()
                self.MEM[int(key,16)]=int(val,16)
            else:
                break
        File.close()

    def twoscomplement(number,length):
        binary=bin(number).replace('0b','')
        binary='0'*(length-len(binary))+binary
        if binary[0]=='0':
            return number
        return number-(2**length)

    def fetch(self,state):
        state.IR=self.MachineCode[state.PC//4]
        state.PC_temp=state.PC+4
        if state.IR==0:
            print("SOme Error Occured")
            return
        state.is_actual_instruction=True
        return state

    def decode(self,state):
        if state.is_actual_instruction==False:
            return state
        opcode=state.IR & (0x7F)
        state.opcode=opcode
        #R type instructions
        if opcode==51:
            rs1=state.IR&(0xF8000)
            rs1=rs1>>15
            state.rs1=rs1
            rs2=state.IR&(0x1F00000)
            rs2=rs2>>20
            state.rs2=rs2
            rd=state.IR&(0xF80)
            rd=rd>>7
            state.rd=rd
            func7=state.IR&(0xFE00000)
            func7=func7>>25
            func3=state.IR&(0x00007000)
            func3=func3>>12
            if func7==0 and func3==0:
                state.operation='add'
            elif func7==0 and func3==7:
                state.operation='and'
            elif func7==0 and func3==6:
                state.operation='or'
            elif func7==0 and func3==1:
                state.operation='sll'
            elif func7==0 and func3==2:
                state.operation='slt'
            elif func7==32 and func3==5:
                state.operation='sra'
            elif func7==0 and func3==5:
                state.operation='srl'
            elif func7==32 and func3==0:
                state.operation='sub'
            elif func7==0 and func3==4:
                state.operation='xor'
            elif func7==1 and func3==0:
                state.operation='mul'
            elif func7==1 and func3==4:
                state.operation='div'
            elif func7==1 and func3==6:
                state.operation='rem'
            else:
                print("INVALID OPERATION")
        elif opcode==19 or opcode==3 or opcode==103:
            rs1=state.IR&(0xF8000)
            rs1=rs1>>15
            state.rs1=rs1
            imm=state.IR&(0xFFF00000)
            imm=imm>>20
            state.imm=imm
            rd=state.IR&(0xF80)
            rd=rd>>7
            state.rd=rd
            func3=state.IR&(0x00007000)
            func3=func3>>12
            if opcode==19:
                if func3==0:
                    state.operation='addi'
                elif func3==7:
                    state.operation='andi'
                elif func3==6:
                    state.operation='ori'
            if opcode==3:
                if func3==0:
                    state.operation='lb'
                elif func3==1:
                    state.operation='lh'
                elif func3==2:
                    state.operation='lw'
            if opcode==103 and func3==0:
                state.operation='jalr'
        elif opcode==35:
            rs1=state.IR&(0xF8000)
            rs1=rs1>>15
            state.rs1=rs1
            rs2=state.IR&(0x1F00000)
            rs2=rs2>>20
            state.rs2=rs2
            func7=state.IR&(0xFE00000)
            func7=func7>>25
            func3=state.IR&(0x00007000)
            func3=func3>>12
            rd=state.IR&(0xF80)
            rd=rd>>7
            state.imm=(func7*(2**5))+rd
            if func3==0:
                state.operation='sb'
            elif func3==1:
                state.operation='sh'
            elif func3==2:
                state.operation='sw'
        elif opcode=99:
            rs1=state.IR&(0xF8000)
            rs1=rs1>>15
            state.rs1=rs1
            rs2=state.IR&(0x1F00000)
            rs2=rs2>>20
            state.rs2=rs2
            func3=state.IR&(0x00007000)
            func3=func3>>12
            immediate=state.IR&(0x80000000)
            immediate=immediate*2+ state.IR&(0x00000080)
            immediate=immediate*(2**6) + state.IR&(0x7E000000)
            immediate=immediate*(2**4)+ state.IR&(0x00000F00)
            immediate*=2
            state.imm=immediate
            if func3==0:
                state.operation='beq'
            elif func3==1:
                state.operation='bne'
            elif func3==5:
                state.operation='bge'
            elif func3==4:
                state.operation='blt'
        elif opcode==23:
            rd=state.IR&(0xF80)
            rd=rd>>7
            state.rd=rd
            imm=state.IR&(0xFFFFF000)
            state.imm=imm
            state.operation='auipc'
        elif opcode==55:
            rd=state.IR&(0xF80)
            rd=rd>>7
            state.rd=rd
            imm=state.IR&(0xFFFFF000)
            state.imm=imm
            state.operation='lui'
        elif opcode==111:
            rd=state.IR&(0xF80)
            rd=rd>>7
            state.rd=rd
            immediate=state.IR&(0x80000000)
            immediate=immediate*(2**8)+state.IR&(0x000FF000)
            immediate=immediate*2+state.IR&(0x00100000)
            immediate=immediate*(2**10)+state.IR&(0x7FE00000)
            immediate*=2
            state.imm=immediate
        return state
    
    def execute(self,state):
        if state.is_actual_operation==False:
            return state
        if state.operation=='add':
            state.Alu_out=self.twoscomplement(self.RegisterFile[state.rs1],32)+self.twoscomplement(self.RegisterFile[state.rs2],32)
        elif state.operation=='and':
            state.Alu_out=self.twoscomplement(self.RegisterFile[state.rs1],32)&self.twoscomplement(self.RegisterFile[state.rs2],32)
        elif state.operation=='or':
            state.Alu_out=self.twoscomplement(self.RegisterFile[state.rs1],32)|self.twoscomplement(self.RegisterFile[state.rs2],32)
        elif state.operation=='sll':
            temp=bin(self.RegisterFile[state.rs1],32)
            temp='0'*(32-len(temp))+temp
            temp=temp[self.twoscomplement(self.RegisterFile[state.rs2],32)%32:]+'0'*self.twoscomplement(self.RegisterFile[state.rs2],32)%32
            state.Alu_out=int(temp,2)
        elif state.operation=='slt':
            if self.twoscomplement(self.RegisterFile[state.rs1],32)<self.twoscomplement(self.RegisterFile[state.rs2],32):
                state.Alu_out=1
            else:
                state.Alu_out=0
        elif state.operation=='sra':
            temp=bin(self.RegisterFile[state.rs1],32)
            temp='0'*(32-len(temp))+temp
            temp='1'*self.twoscomplement(self.RegisterFile[state.rs2],32)%32+temp[:self.twoscomplement(self.RegisterFile[state.rs2],32)%32]
        elif state.operation=='srl':
            temp=bin(self.RegisterFile[state.rs1],32)
            temp='0'*(32-len(temp))+temp
            temp=temp[self.twoscomplement(self.RegisterFile[state.rs2],32)%32:]+'1'*self.twoscomplement(self.RegisterFile[state.rs2],32)%32
            state.Alu_out=int(temp,2)            
        elif state.operation=='sub':
            state.Alu_out=self.twoscomplement(self.RegisterFile[state.rs1],32)-self.twoscomplement(self.RegisterFile[state.rs2],32)
        elif state.operation=='xor':
           state.Alu_out= self.twoscomplement(self.RegisterFile[state.rs1],32)^self.twoscomplement(self.RegisterFile[state.rs2],32)
        elif state.operation=='mul':
            state.Alu_out=self.twoscomplement(self.RegisterFile[state.rs1],32)*self.twoscomplement(self.RegisterFile[state.rs2],32)
        elif state.operation=='div':
            state.Alu_out=self.twoscomplement(self.RegisterFile[state.rs1],32)//self.twoscomplement(self.RegisterFile[state.rs2],32)
        elif state.operation=='rem':
            state.Alu_out=self.twoscomplement(self.RegisterFile[state.rs1],32)%self.twoscomplement(self.RegisterFile[state.rs2],32)
        elif state.operation=='addi':
            state.Alu_out=self.twoscomplement(self.RegisterFile[state.rs1],32)+self.twoscomplement(state.imm)
        elif state.operation=='andi':
            state.Alu_out=self.twoscomplement(self.RegisterFile[state.rs1],32)&self.twoscomplement(state.imm)
        elif state.operation=='ori':
            state.Alu_out=self.twoscomplement(self.RegisterFile[state.rs1],32)|self.twoscomplement(state.imm)
        elif state.operation in ['lb','lw','lh','sb','sh','sw']:
            state.Alu_out=self.RegisterFile[state.rs1]+self.twoscomplement(state.imm)
        elif state.operation=='jalr':
            temp=self.RegisterFile[state.rs1]+self.twoscomplement(state.imm)
            state.PC_temp=temp
            state.Alu_out=state.PC            
        elif state.operation=='auipc':
            state.Alu_out=state.PC+self.twoscomplement(state.imm,32)
        elif state.operation=='lui':
            state.Alu_out=state.imm
        elif state.operation=='jal':
            temp=self.twoscomplement(imm,20)
            state.PC_temp=state.PC+temp
            state.Alu_out=state.PC
        return state
    
    def memory_access(self,state):
        if state.is_actual_operation==False:
            return state
        if state.operation=='lb':
            val=0
            for i in range(1):
                adr=state.Alu_out+i
                if adr in self.MEM.keys():
                    val=val+self.MEM[adr]*(1<<(8*i))
            state.MDR=self.twoscomplement(val,8)
        elif state.operation=='lh':
            val=0
            for i in range(2):
                adr=state.Alu_out+i
                if adr in self.MEM.keys():
                    val=val+self.MEM[adr]*(1<<(8*i))
            state.MDR=self.twoscomplement(val,16)
        elif state.operation=='lw':
            val=0
            for i in range(4):
                adr=state.Alu_out+i
                if adr in self.MEM.keys():
                    val=val+self.MEM[adr]*(1<<(8*i))
            state.MDR=self.twoscomplement(val,32)
        elif state.operation=='sb':
            adr=state.Alu_out
            data=self.RegisterFile[state.rs1]
            for i in range(1):
                d_in=(data>>(8*i))&(0xFF)
                self.MEM[adr]=d_in
                adr=adr+1
        elif state.operation=='sh':
            adr=state.Alu_out
            data=self.RegisterFile[state.rs1]
            for i in range(2):
                d_in=(data>>(8*i))&(0xFF)
                self.MEM[adr]=d_in
                adr=adr+1
        elif state.operation=='sw':
            adr=state.Alu_out
            data=self.RegisterFile[state.rs1]
            for i in range(4):
                d_in=(data>>(8*i))&(0xFF)
                self.MEM[adr]=d_in
                adr=adr+1
        return state

    def write_back(self,state):
        if state.is_actual_operation==False:
            return state
        if state.operation in ['add','and','or','sll','slt','sra','srl','sub','xor','mul','div','rem','addi','andi','ori']:
            self.RegisterFile[state.rd]=state.Alu_out
        elif state.operation in ['lb','lh','lw']:
            self.RegisterFile[state.rd]=state.MDR
        elif state.operation in ['jal','jalr']:
            state.PC=state.PC_temp


class BranchTargetBuffer:
    pass