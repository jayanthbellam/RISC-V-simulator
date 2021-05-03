class Cache:
    def __init__(self,cache_size,cache_block_size,no_of_ways):
        self.access=0
        self.hits=0
        self.miss=0
        self.cache_size=cache_size
        self.cache_block_size=cache_block_size
        self.no_of_ways=no_of_ways
        self.blocks=cache_block_size//cache_size
        self.array=[[[-1,-1]*no_of_ways]*self.blocks] #Cache.array[i][0]->Tag Array Cache.array[i][1]->Data Array
    
    def search(self,address):
        self.access+=1
        block=address%(self.blocks)
        block=self.array[block]
        for i in block:
            if i[0]==address:
                self.hits+=1
                self.array.remove(i)
                self.array.insert(0,i)
                return i[1]
        self.miss+=1
        return 'Not Found'
    
    def write(self,address,data):
        block=address%(self.blocks)
        block.pop()
        block.append([address,data])
        
class ISB:
    def __init__(self,pc=0):
        self.operation=-1
        self.opcode=-1
        self.rs1=-1
        self.rs2=-1
        self.rd=-1
        self.imm=-1
        self.PC=pc
        self.PC_temp=0
        self.IR=0
        self.RA=0
        self.RB=0
        self.MDR=0
        self.Alu_out=-1
        self.is_actual_instruction=False
        self.branchRA=-1
        self.branchRB=-1

class ControlUnit:

    def __init__(self,file_name):
        self.MEM={}
        self.MachineCode={}
        self.RegisterFile=[0 for i in range(32)]
        self.RegisterFile[2]=int('0x7FFFFFF0',16)
        self.RegisterFile[3]=int('0x10000000',16)
        self.cycles=0
        self.count_mem_ins=0
        self.count_ins=0
        self.count_control_ins=0
        self.count_alu_inst=0
        self.stalls=0
        self.branch_mispred=0
        self._program_memory(file_name)

    def _program_memory(self,file_name):
        File=open(file_name)
        while True:
            inst=File.readline()
            try:
                _,inst=inst.split()
                _=int(_,16)
                inst=int(inst,16)
                self.MachineCode[_]=inst
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

    def twoscomplement(self,decimal_number,length):
        binary=bin(decimal_number).replace('0b','')
        binary='0'*(length-len(binary))+binary
        if binary[0]=='0':
            return decimal_number
        return decimal_number-(2**length)

    def store_State(self,file_name='Store.txt'):
        file=open(file_name,'w')
        file.write('Registers\n')
        file.write('-'*20)
        file.write('\n')
        for i in range(32):
            file.write(str(self.RegisterFile[i]))
            file.write('\n')
        file.write('-'*20)
        file.write('\n')
        file.write('Memory')
        file.write('\n')
        file.write('-'*20)
        file.write('\n')
        file.write("Memory : Value")
        file.write('\n')
        for key in self.MEM.keys():
            file.write(str(key)+" : "+str(self.MEM[key]))
            file.write('\n')

    def fetch(self,state,btb):
        try:
            state.IR=self.MachineCode[state.PC]
            state.PC_temp=state.PC+4
            state.is_actual_instruction=True
            opcode=state.IR &(0x7F)
            state.opcode=opcode
            if opcode==99:
                rs1=state.IR&(0xF8000)
                rs1=rs1>>15
                state.rs1=rs1
                rs2=state.IR&(0x1F00000)
                rs2=rs2>>20
                state.rs2=rs2
                func3=state.IR&(0x7000)
                func3=func3>>12
                temp=bin(state.IR).replace('0b','')
                temp='0'*(32-len(temp))+temp
                immediate=temp[0]+temp[-8]+temp[1:7]+temp[20:24]+'0'
                state.imm=int(immediate,2)
                if func3==0:
                    state.operation='beq'
                elif func3==1:
                    state.operation='bne'
                elif func3==5:
                    state.operation='bge'
                elif func3==4:
                    state.operation='blt'
            elif opcode==103:
                rs1=state.IR&(0xF8000)
                rs1=rs1>>15
                state.rs1=rs1
                imm=state.IR&(0xFFF00000)
                imm=imm>>20
                state.imm=imm
                rd=state.IR&(0xF80)
                rd=rd>>7
                state.rd=rd
                func3=state.IR&(0x7000)
                func3=func3>>12
                state.RA=self.RegisterFile[rs1] 
                state.operation='jalr'                         
            if btb==0:
                return state
            new_pc=0
            outcome=False
            if btb.targetBTB(state.PC)!=-1:
                new_pc=btb.targetBTB(state.PC)
                outcome=True
            return  outcome,new_pc,state
        except KeyError:
            state.IR=0
            state.is_actual_instruction=False
            if btb==0:
                return state
            return False,0,state

    def decode(self,state,btb):
        control_hazard=False
        new_pc=0
        state.Alu_out=-1
        if state.is_actual_instruction==False:
            return control_hazard, new_pc, state
        opcode=state.IR & (0x7F)
        state.opcode=opcode
        #R type instructions
        if opcode==51:
            self.count_alu_inst+=1
            rs1=state.IR&(0xF8000)
            rs1=rs1>>15
            state.rs1=rs1
            rs2=state.IR&(0x1F00000)
            rs2=rs2>>20
            state.rs2=rs2
            rd=state.IR&(0xF80)
            rd=rd>>7
            state.rd=rd
            func7=state.IR&(0xFE000000)
            func7=func7>>25
            func3=state.IR&(0x7000)
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

        #I type instructions
        elif opcode==19 or opcode==3:
            rs1=state.IR&(0xF8000)
            rs1=rs1>>15
            state.rs1=rs1
            imm=state.IR&(0xFFF00000)
            imm=imm>>20
            state.imm=imm
            rd=state.IR&(0xF80)
            rd=rd>>7
            state.rd=rd
            func3=state.IR&(0x7000)
            func3=func3>>12
            if opcode==19:
                self.count_alu_inst+=1
                if func3==0:
                    state.operation='addi'
                elif func3==7:
                    state.operation='andi'
                elif func3==6:
                    state.operation='ori'
            elif opcode==3:
                self.count_mem_ins+=1
                if func3==0:
                    state.operation='lb'
                elif func3==1:
                    state.operation='lh'
                elif func3==2:
                    state.operation='lw'

        elif opcode==103:
            self.count_control_ins+=1
            temp=self.RegisterFile[state.rs1]+self.twoscomplement(state.imm,12)
            state.PC_temp=temp
            state.Alu_out=state.PC+4
            if btb!=0:
                if not btb.checkBTB(state.PC):
                    btb.updateBTB(state.PC,state.PC_temp)
                    self.branch_mispred+=1
                    control_hazard=True
                    new_pc=state.PC_temp
        elif opcode==35:
            self.count_mem_ins+=1
            rs1=state.IR&(0xF8000)
            rs1=rs1>>15
            state.rs1=rs1
            rs2=state.IR&(0x1F00000)
            rs2=rs2>>20
            state.rs2=rs2
            func7=state.IR&(0xFE00000)
            func7=func7>>25
            func3=state.IR&(0x7000)
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

        elif opcode==99:
            self.count_control_ins+=1
            state.RA=self.RegisterFile[state.rs1] if state.branchRA!=-1 else state.branchRA
            state.RB=self.RegisterFile[state.rs1] if state.branchRB!=-1 else state.branchRB

            if state.operation=='beq':
                if self.RegisterFile[state.rs1]==self.RegisterFile[state.rs2]:
                    state.PC_temp=state.PC+self.twoscomplement(state.imm,12)
                    state.Alu_out=1
                else:
                    state.Alu_out=0
            elif state.operation=='blt':
                if self.RegisterFile[state.rs1]<self.RegisterFile[state.rs2]:
                    state.PC_temp=state.PC+self.twoscomplement(state.imm,12)
                    state.Alu_out=1
                else:
                    state.Alu_out=0
            elif state.operation=='bge':
                if self.RegisterFile[state.rs1]>=self.RegisterFile[state.rs2]:
                    state.PC_temp=state.PC+self.twoscomplement(state.imm,12)
                    state.Alu_out=1
                else:
                    state.Alu_out=0
            elif state.operation=='bne':
                if self.RegisterFile[state.rs1]!=self.RegisterFile[state.rs2]:
                    state.PC_temp=state.PC+self.twoscomplement(state.imm,12)
                    state.Alu_out=1
                else:
                    state.Alu_out=0
            if btb!=0:
                if self.twoscomplement(state.imm,12)<0:
                    if not btb.checkBTB(state.PC):
                        btb.updateBTB(state.PC,state.PC_temp)
                        if state.Alu_out==1:
                            self.branch_mispred+=1
                            control_hazard=True
                            new_pc=state.PC_temp
                    else:
                        if state.Alu_out==0:
                            self.branch_mispred+=1
                            control_hazard=True
                            new_pc=state.PC_temp
                else:
                    if state.Alu_out==1:
                        self.branch_mispred+=1
                        control_hazard=True
                        new_pc=state.PC_temp
        elif opcode==23:
            rd=state.IR&(0xF80)
            rd=rd>>7
            state.rd=rd
            imm=state.IR&(0xFFFFF000)
            state.imm=imm
            state.operation='auipc'

        elif opcode==55:
            self.count_alu_inst+=1
            rd=state.IR&(0xF80)
            rd=rd>>7
            state.rd=rd
            imm=state.IR&(0xFFFFF000)
            state.imm=imm
            state.operation='lui'

        elif opcode==111:
            self.count_control_ins+=1
            rd=state.IR&(0xF80)
            rd=rd>>7
            state.rd=rd
            temp=bin(state.IR).replace('0b','')
            temp='0'*(32-len(temp))+temp
            imm=temp[0]
            imm+=temp[12:20]
            imm+=temp[11]
            imm+=temp[1:11]+'0'
            state.imm=int(imm,2)
            state.operation='jal'
            temp=self.twoscomplement(state.imm,21)
            state.PC_temp=state.PC+temp
            if btb!=0:
                if not btb.checkBTB(state.PC):
                    btb.updateBTB(state.PC,state.PC_temp)
                    self.branch_mispred+=1
                    control_hazard=True
                    new_pc=state.PC_temp
            state.Alu_out=state.PC+4
        if btb==0:
            return state
        return control_hazard,new_pc,state
    
    def execute(self,state):
        if state.is_actual_instruction==False:
            return state
        self.count_ins+=1
        if state.opcode==51:
            state.RA=self.RegisterFile[state.rs1]
            state.RB=self.RegisterFile[state.rs2]
            if state.operation=='add':
                state.Alu_out=self.twoscomplement(state.RA,32)+self.twoscomplement(state.RB,32)
            elif state.operation=='and':
                state.Alu_out=self.twoscomplement(state.RA,32)&self.twoscomplement(state.RB,32)
            elif state.operation=='or':
                state.Alu_out=self.twoscomplement(state.RA,32)|self.twoscomplement(state.RB,32)
            elif state.operation=='sll':
                temp=bin(state.RA)
                temp='0'*(32-len(temp))+temp
                temp=temp[self.twoscomplement(state.RB)%32:]+'0'*self.twoscomplement(state.RB,32)%32
                state.Alu_out=int(temp,2)
            elif state.operation=='slt':
                if self.twoscomplement(state.RA,32)<self.twoscomplement(state.RB,32):
                    state.Alu_out=1
                else:
                    state.Alu_out=0
            elif state.operation=='sra':
                temp=bin(state.RA)
                temp='0'*(32-len(temp))+temp
                temp='1'*self.twoscomplement(state.RB,32)%32+temp[:self.twoscomplement(self.RegisterFile[state.RB],32)%32]
            elif state.operation=='srl':
                temp=bin(state.RA)
                temp='0'*(32-len(temp))+temp
                temp=temp[self.twoscomplement(state.RB,32)%32:]+'1'*self.twoscomplement(state.RB,32)%32
                state.Alu_out=int(temp,2)
            elif state.operation=='sub':
                state.Alu_out=self.twoscomplement(state.RA,32)-self.twoscomplement(state.RB,32)
            elif state.operation=='xor':
                state.Alu_out= self.twoscomplement(state.RA,32)^self.twoscomplement(state.RB,32)
            elif state.operation=='mul':
                state.Alu_out=self.twoscomplement(state.RA,32)*self.twoscomplement(state.RB,32)
            elif state.operation=='div':
                try:
                    state.Alu_out=self.twoscomplement(state.RA,32)//self.twoscomplement(state.RB,32)
                except ZeroDivisionError:
                    state.Alu_out=0xFFFFFFFF
            elif state.operation=='rem':
                try:
                    state.Alu_out=self.twoscomplement(state.RA,32)%self.twoscomplement(state.RB,32)
                except ZeroDivisionError:
                    state.Alu_out=self.twoscomplement(state.RA,32)
        if state.opcode in [19,3,103]:
            state.RA=self.RegisterFile[state.rs1]
            if state.operation=='addi':
                state.Alu_out=self.twoscomplement(state.RA,32)+self.twoscomplement(state.imm,12)
            elif state.operation=='andi':
                state.Alu_out=self.twoscomplement(state.RA,32)&self.twoscomplement(state.imm,12)
            elif state.operation=='ori':
                state.Alu_out=self.twoscomplement(state.RA,32)|self.twoscomplement(state.imm,12)
            elif state.operation in ['lb','lw','lh']:
                state.Alu_out=self.RegisterFile[state.rs1]+self.twoscomplement(state.imm,12)
        if state.operation in ['sb','sh','sw']:
            state.RA=self.RegisterFile[state.rs1]
            state.Alu_out=state.RA+self.twoscomplement(state.imm,12)
        elif state.operation=='auipc':
            state.Alu_out=state.PC+self.twoscomplement(state.imm,32)
        elif state.operation=='lui':
            state.Alu_out=state.imm
        state.PC=state.PC_temp
        return state
    
    def memory_access(self,state):
        if state.is_actual_instruction==False:
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
            data=self.RegisterFile[state.rs2]
            for i in range(1):
                d_in=(data>>(8*i))&(0xFF)
                self.MEM[adr]=d_in
                adr=adr+1
        elif state.operation=='sh':
            adr=state.Alu_out
            data=self.RegisterFile[state.rs2]
            for i in range(2):
                d_in=(data>>(8*i))&(0xFF)
                self.MEM[adr]=d_in
                adr=adr+1
        elif state.operation=='sw':
            adr=state.Alu_out
            data=self.RegisterFile[state.rs2]
            for i in range(4):
                d_in=(data>>(8*i))&(0xFF)
                self.MEM[adr]=d_in
                adr=adr+1
        return state

    def write_back(self,state):
        if state.is_actual_instruction==False:
            return state
        if state.rd==0:
            return state
        if state.operation in ['add','and','or','sll','slt','sra','srl','sub','xor','mul','div','rem','addi','andi','ori']:
            self.RegisterFile[state.rd]=state.Alu_out
        elif state.operation in ['lb','lh','lw']:
            self.RegisterFile[state.rd]=state.MDR
        elif state.operation in ['jalr','jal','lui','auipc']:
            self.RegisterFile[state.rd]=state.Alu_out
        return state

class BranchTargetBuffer:
    table={}
    
    def updateBTB(self,PC,target_PC):
        self.table[PC]=target_PC
    
    def checkBTB(self,PC):
        if PC in self.table.keys():
            return True
        return False
    
    def targetBTB(self,PC):
        if self.checkBTB(PC):
            return self.table[PC]
        return -1
    
