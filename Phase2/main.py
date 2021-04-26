from Instruction import ISB,ControlUnit,BranchTargetBuffer
import sys


def data_hazard(state_):
    new_states=[state_[0]]
    data_forwards= 0
    de=state_[1]
    ex=state_[2]
    me=state_[3]
    wb=state_[4]
    Hazard =False
    stall=False    #0 / 1
    w_stall=3
    de_opcode=de.opcode
    ex_opcode=ex.opcode
    me_opcode=me.opcode
    wb_opcode=wb.opcode
    if(wb_opcode==3 and me_opcode==35) and (wb.rd>0 and wb.rd==me.rs2):
            Hazard=True
            me.RB=wb.MDR
            data_forwards+=1
    if wb.rd >0:
        if wb.rd==ex.rs1:
            ex.RA=wb.MDR
            Hazard=True
            data_forwards+=1
        
        if wb.rd==ex.rs2:
            ex.RB=wb.MDR
            Hazard=True
            data_forwards+=1
    if me.rd>0:
        if me_opcode==3:
            if ex_opcode==35:
                if ex.rs1==me.rd:
                    Hazard=True
                    stall=True
                    w_stall=min(w_stall,1)
            else:
                Hazard=True
                stall=True
                w_stall=min(w_stall,1)

        else:
            if (ex.rs1==me.rd):
                ex.RA=me.Alu_out
                Hazard=True
                data_forwards=True
            if (ex.rs2==me.rd):
                ex.RB=me.Alu_out
                Hazard=True
                data_forwards+=1
        
    if (de_opcode==99 or de_opcode==103):
        if wb.rd>0:
            if wb.rd==de.rs1:
                de.branchRA=wb.MDR
                Hazard=True
                data_forwards+=1
            if wb.rd==de.rs2:
                de.branchRB=wb.MDR
                Hazard=True
                data_forwards+=1
        if me.rd>0 :
            if me_opcode ==3:
                Hazard=True
                stall=True
                w_stall=min(w_stall,2)	
            else:
                if me.rd==de.rs1:
                    de.branchRA=me.Alu_out
                    Hazard=True
                    data_forwards+=1
                if me.rd ==de.rs2 :
                    de.branchRB=me.Alu_out
                    Hazard=True
                    data_forwards+=1
        if ex.rd > 0 and (ex.rd== de.rs1 or ex.rd ==de.rs2):
            Hazard=True
            stall=True
            w_stall=min(w_stall,2)
 		   
    new_states= new_states + [de,ex,me,wb]
    return [Hazard,stall,new_states,w_stall,data_forwards]
def check_data_haz_stall(states):
    de=states[2]
    ex=states[3]
    me=states[4]
    if 	ex.is_actual_instruction and de.is_actual_instruction and ex.rd>0:
        if ex.rd==de.rs1:
            return [True,2]
        if ex.rd==de.rs2:
            return [True,2]
    if me.is_actual_instruction and de.is_actual_instruction and me.rd>0:
        if me.rd==de.rs1:
            return [True,1]
        if me.rd==de.rs2:
            return [True,1]
    return [False,-1]

if len(sys.argv)<2:
    print("Invalid Number of arguments")
else:
    filename=sys.argv[1]
    ComputerState=ControlUnit(filename)
    PC=0
    clock=0
    pipelined_execution=True
    data_forwarding=True
    btb=BranchTargetBuffer()
    if pipelined_execution:
        in_states=[ISB() for i in range(5)]
        out_states=[]
        data_hazard_count=0
        if data_forwarding:
            while 1:
                is_hazard=False
                stall=False
                w_stall=3 #3=> no stalling
                for i in range(4,-1,-1):
                    if i==4:
                        overflow=ComputerState.write_back(in_states[4])
                        hazard=data_hazard(in_states)
                        in_states[3]=hazard[2][3]
                        data_hazard_count+=hazard[4]
                    if i==3:
                        out_states.append(ComputerState.memory_access(in_states[3]))
                    if i==2:
                        out_states.append(ComputerState.execute(in_states[2]))
                    if i==1:
                        control_hazard,control_hazard_pc,tempstate=ComputerState.decode(in_states[1],btb)
                        out_states.append(tempstate)
                    if i==0:
                        control_change,control_change_pc,tempstate=ComputerState.fetch(in_states[0],btb)
                        out_states.append(tempstate)
                    if i!=4:
                        hazard=data_hazard(in_states)
                        in_states=hazard[2]
                        is_hazard=is_hazard|hazard[0]
                        stall=stall|hazard[1]
                        w_stall=min(w_stall,hazard[3])
                        data_hazard_count+=hazard[4]
                out_states=out_states[::-1]

                if out_states[0].is_actual_instruction and (stall==False):
                    PC+=4
                if control_change and stall==False:
                    PC=control_change_pc
                if control_hazard and stall==False:
                    PC=control_hazard_pc
                    out_states[0]=ISB(0)
                if stall:
                    print('\n\nSTALLING\n\n')
                    if w_stall==1:
                        out_states=[in_states[1],in_states[2],ISB(),out_states[3]]
                    else:
                        out_states=[in_states[1],ISB(),out_states[2],out_states[3]]
                if not (out_states[0].is_actual_instruction or out_states[1].is_actual_instruction or out_states[2].is_actual_instruction or out_states[3].is_actual_instruction):
                        break
                in_states=[ISB(PC)]+out_states
                out_states=[]
                ComputerState.store_State('pipelined_data_forwarding.txt')
                input()
              
        #if data is not forwarded we implement stalling
        else:
            while 1:
                data_hazards=check_data_haz_stall(in_states)
                reversed_states=[(idx,val) for idx,val in enumerate(in_states)][::-1]
                for idx,state in reversed_states:
                    if idx==4:
                        overflow=ComputerState.write_back(state)
                    if idx==3:
                        out_states.append(ComputerState.memory_access(state))
                    if idx==2:
                        out_states.append(ComputerState.execute(state))
                    if idx==1:
                        control_hazard,control_hazard_pc,tempstate=ComputerState.decode(state,btb)
                        out_states.append(tempstate)
                    if idx==0:
                        outcome,new_pc,tempstate=ComputerState.fetch(state,btb)
                        out_states.append(tempstate)
                out_states=out_states[::-1]
                if out_states[0].is_actual_instruction and not data_hazards[0]:
                    PC+=4
                if outcome and not data_hazards[0]:
                    PC=new_pc
                if control_hazard and not data_hazards[0]:
                    PC=control_hazard_pc
                    out_states[0]=ISB()
                if data_hazards[0]:
                    if data_hazards[1]==2:
                        in_states=[in_states[0],in_states[1],in_states[2],ISB(),out_states[3]]
                        continue
                    else:
                        in_states=[in_states[0],in_states[1],ISB(),out_states[2],out_states[3]]
                        continue
                if not (out_states[0].is_actual_instruction or out_states[1].is_actual_instruction or out_states[2].is_actual_instruction or out_states[3].is_actual_instruction):
                    break
                in_states=[ISB(PC)]+out_states
                out_states=[]
                ComputerState.store_State('pipelined_not_data_forwarding.txt')
                input()



            

    else:
        Simulator=ISB(0)
        while 1:
            Simulator=ComputerState.fetch(Simulator,0)
            if not Simulator.is_actual_instruction:
                break
            Simulator=ComputerState.decode(Simulator,0)
            Simulator=ComputerState.execute(Simulator)
            Simulator=ComputerState.memory_access(Simulator)
            Simulator=ComputerState.write_back(Simulator)
            input()
        ComputerState.store_State()
