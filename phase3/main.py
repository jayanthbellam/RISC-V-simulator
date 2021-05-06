from Simulator import ISB,ControlUnit,BranchTargetBuffer
import sys

forwarding_vals = {}
forwarding_vals['M2M'] = 0
forwarding_vals['E2E'] = 0
forwarding_vals['M2E'] = 0
forwarding_vals['M2D'] = 0
forwarding_vals['E2D'] = 0

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
            forwarding_vals['M2M'] = wb.MDR
            data_forwards+=1
    if wb.rd >0:
        if wb.rd==ex.rs1:
            ex.RA=wb.MDR
            Hazard=True
            forwarding_vals['M2E'] = wb.MDR
            data_forwards+=1
        
        if wb.rd==ex.rs2:
            ex.RB=wb.MDR
            Hazard=True
            forwarding_vals['M2E'] = wb.MDR
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
                forwarding_vals['E2E'] = me.Alu_out
            if (ex.rs2==me.rd):
                ex.RB=me.Alu_out
                Hazard=True
                data_forwards+=1
                forwarding_vals['E2E'] = me.Alu_out
        
    if (de_opcode==99 or de_opcode==103):
        if wb.rd>0:
            if wb.rd==de.rs1:
                de.branchRA=wb.MDR
                Hazard=True
                data_forwards+=1
                forwarding_vals['M2D'] = wb.MDR
            if wb.rd==de.rs2:
                de.branchRB=wb.MDR
                Hazard=True
                data_forwards+=1
                forwarding_vals['M2D'] = wb.MDR
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
                    forwarding_vals['E2D'] = me.Alu_out
                if me.rd ==de.rs2 :
                    de.branchRB=me.Alu_out
                    Hazard=True
                    data_forwards+=1
                    forwarding_vals['E2D'] = me.Alu_out
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
    PC=0
    count_data_hazard=0
    count_stall=0
    count_control_hazard=0
    count_data_stall=0
    count_control_stall=0
    knob1 = int(input("Enable(1)/Disable(0) pipelining: "))
    knob3 = int(input("Enable(1)/Disable(0) printing the values in the register file at the end of each cycle: "))
    knob4 = int(input("Enable(1)/Disable(0) printing information in the pipeline registers at the end of each cycle, along with cycle number. "))
    knob5 = int(input("Enter the instruction number for printing its pipeline register information/[Disable(-1)]: "))
    cahce_size=int(input("Enter the cache size in bytes: "))
    cahce_block_size=int(input("Enter Block size in bytes: "))
    no_of_ways=int(input("No of ways of associativity: "))
    ComputerState=ControlUnit(filename,cahce_size,cahce_block_size,no_of_ways)
    btb=BranchTargetBuffer()
    if knob1:
        in_states=[ISB() for i in range(5)]
        out_states=[]
        knob2 = int(input("Enable(1)/Disable(0) data forwarding: "))
        if knob2:
            while 1:
                is_hazard=False
                stall=False
                w_stall=3 #3=> no stalling
                for i in range(4,-1,-1):
                    ComputerState.cycles+=1
                    if i==4:
                        overflow=ComputerState.write_back(in_states[4])
                        hazard=data_hazard(in_states)
                        in_states[3]=hazard[2][3]
                        count_data_hazard+=hazard[4]
                        if knob5 != -1 and knob5 == in_states[4].PC:
                            print("M->M Forwarding: {0}, M->E Forwarding: {1}, M->D Forwarding: {2}, \nE->E Forwarding: {3}, E->D Forwarding: {4}".
                                  format(forwarding_vals['M2M'], forwarding_vals['M2E'], forwarding_vals['M2D'], forwarding_vals['E2E'], forwarding_vals['E2D']))
                    if i==3:
                        out_states.append(ComputerState.memory_access(in_states[3]))
                        if knob5 != -1 and knob5 == in_states[3].PC:
                            print("M->M Forwarding: {0}, M->E Forwarding: {1}, M->D Forwarding: {2}, \nE->E Forwarding: {3}, E->D Forwarding: {4}".
                                  format(forwarding_vals['M2M'], forwarding_vals['M2E'], forwarding_vals['M2D'], forwarding_vals['E2E'], forwarding_vals['E2D']))
                    if i==2:
                        out_states.append(ComputerState.execute(in_states[2]))
                        if knob5 != -1 and knob5 == in_states[2].PC:
                            print("M->M Forwarding: {0}, M->E Forwarding: {1}, M->D Forwarding: {2}, \nE->E Forwarding: {3}, E->D Forwarding: {4}".
                                  format(forwarding_vals['M2M'], forwarding_vals['M2E'], forwarding_vals['M2D'], forwarding_vals['E2E'], forwarding_vals['E2D']))
                    if i==1:
                        control_hazard,control_hazard_pc,tempstate=ComputerState.decode(in_states[1],btb)
                        out_states.append(tempstate)
                        if knob5 != -1 and knob5 == in_states[1].PC:
                            print("M->M Forwarding: {0}, M->E Forwarding: {1}, M->D Forwarding: {2}, \nE->E Forwarding: {3}, E->D Forwarding: {4}".
                                  format(forwarding_vals['M2M'], forwarding_vals['M2E'], forwarding_vals['M2D'], forwarding_vals['E2E'], forwarding_vals['E2D']))
                    if i==0:
                        control_change,control_change_pc,tempstate=ComputerState.fetch(in_states[0],btb)
                        out_states.append(tempstate)
                        if knob5 != -1 and knob5 == in_states[0].PC:
                            print("M->M Forwarding: {0}, M->E Forwarding: {1}, M->D Forwarding: {2}, \nE->E Forwarding: {3}, E->D Forwarding: {4}".
                                  format(forwarding_vals['M2M'], forwarding_vals['M2E'], forwarding_vals['M2D'], forwarding_vals['E2E'], forwarding_vals['E2D']))
                    if i!=4:
                        hazard=data_hazard(in_states)
                        in_states=hazard[2]
                        is_hazard=is_hazard|hazard[0]
                        stall=stall|hazard[1]
                        w_stall=min(w_stall,hazard[3])
                        count_data_hazard+=hazard[4]
                out_states=out_states[::-1]

                if out_states[0].is_actual_instruction and (stall==False):
                    PC+=4
                if control_change and stall==False:
                    PC=control_change_pc
                if control_hazard and stall==False:
                    count_control_hazard+=1
                    count_control_stall+=1
                    count_stall+=1
                    PC=control_hazard_pc
                    out_states[0]=ISB(0)
                if stall:
                    count_stall+=1
                    count_data_stall+=1
                    if w_stall==1:
                        out_states=[in_states[1],in_states[2],ISB(),out_states[3]]
                    else:
                        out_states=[in_states[1],ISB(),out_states[2],out_states[3]]
                if not (out_states[0].is_actual_instruction or out_states[1].is_actual_instruction or out_states[2].is_actual_instruction or out_states[3].is_actual_instruction):
                        break
                in_states=[ISB(PC)]+out_states
                out_states=[]
                if knob4:
                    print("M->M Forwarding: {0}, M->E Forwarding: {1}, M->D Forwarding: {2}, \nE->E Forwarding: {3}, E->D Forwarding: {4}".
                    format(forwarding_vals['M2M'], forwarding_vals['M2E'], forwarding_vals['M2D'], forwarding_vals['E2E'], forwarding_vals['E2D']))
                if knob3:
                    print("Register file: {}".format(ComputerState.RegisterFile))
            ComputerState.store_State('pipelined_data_forwarding.txt')              
        #if data is not forwarded we implement stalling
        else:
            while 1:
                data_hazards=check_data_haz_stall(in_states)
                reversed_states=[(idx,val) for idx,val in enumerate(in_states)][::-1]
                for idx,state in reversed_states:
                    ComputerState.cycles+=1
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
                    count_control_hazard+=1
                    PC=control_hazard_pc
                    out_states[0]=ISB()
                    count_control_stall+=1
                if data_hazards[0]:
                    count_data_hazard+=1
                    count_stall+=1
                    count_data_stall+=1
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
                if knob4:
                    print("M->M Forwarding: {0}, M->E Forwarding: {1}, M->D Forwarding: {2}, \nE->E Forwarding: {3}, E->D Forwarding: {4}".
                    format(forwarding_vals['M2M'], forwarding_vals['M2E'], forwarding_vals['M2D'], forwarding_vals['E2E'], forwarding_vals['E2D']))
                if knob3:
                    print("Register file: {}".format(ComputerState.RegisterFile))
            ComputerState.store_State('pipelined_not_data_forwarding.txt')

    else:
        Simulator=ISB(0)
        while 1:
            ComputerState.cycles+=1
            Simulator=ComputerState.fetch(Simulator,0)
            if not Simulator.is_actual_instruction:
                break
            Simulator=ComputerState.decode(Simulator,0)
            Simulator=ComputerState.execute(Simulator)
            Simulator=ComputerState.memory_access(Simulator)
            Simulator=ComputerState.write_back(Simulator)
            if knob3:
                print("Register file: {}".format(ComputerState.RegisterFile))
        ComputerState.store_State()
    print('The total number of cycles used: '+str(ComputerState.cycles))
    print('The total number of instructions: '+str(ComputerState.count_ins))
    print('CPI: '+str(ComputerState.cycles/ComputerState.count_ins))
    print('Data transfer Instructions: '+str(ComputerState.count_mem_ins))
    print('ALU instructions: '+str(ComputerState.count_alu_inst))
    print('Control Instructions: '+str(ComputerState.count_control_ins))
    print('Number of Stalls: '+str(count_stall))
    print('Number of data hazards: '+str(count_data_hazard))
    print('Number of control hazards: '+str(count_control_hazard))
    print('Number of branch mispredictions: '+str(ComputerState.branch_mispred))
    print('Number of stalls due to data hazards: '+str(count_data_stall))
    print('Number of stalls due to control hazards: '+str(count_control_stall))
    print('Number of accesses of Instruction Cache: '+str(ComputerState.InstructionCache.access))
    print('Number of hits of Instruction Cache: '+str(ComputerState.InstructionCache.hits))
    print('Number of misses of Instruction Cache: '+str(ComputerState.InstructionCache.miss))
    print('Number of accesses of Memory Cache: '+str(ComputerState.memoryCache.access))
    print('Number of hits of Memory Cache: '+str(ComputerState.memoryCache.hits))
    print('Number of misses of Memory Cache: '+str(ComputerState.memoryCache.miss))
