from Instruction import State,ControlUnit,BranchTargetBuffer
from Hazard import HAZ
import sys

if len(sys.argv)<2:
    print("Invalid Number of arguments")
else:
    filename=sys.argv[1]
    ComputerState=ControlUnit(filename)
    PC=0
    clock=0
    knob1 = int(input("Enable(1)/Disable(0) pipelining: "))
    knob3 = int(input("Enable(1)/Disable(0) printing the values in the register file at the end of each cycle: "))
    knob4 = int(input("Enable(1)/Disable(0) printing information in the pipeline registers at the end of each cycle, along with cycle number. "))
    knob5 = int(input(" Enter the instruction number for printing its pipeline register information/[Disable(-1)]: "))
    
    btb = BranchTargetBuffer()
    hazards = HAZ()
    if knob1:   #pipelining
        in_states=[State() for i in range(5)]
        out_states=[]
        data_hazard_count=0
        #If data forwarding is disabled then pipeline is executed with stalling
        knob2 = int(input("Enable(1)/Disable(0) data forwarding: "))
        if knob2: #data forwarding 
            while 1:
                is_hazard=False
                stall=False
                w_stall= 3 #3=> no stalling
                for i in range(4,-1,-1):
                    if i==4:
                        overflow=ComputerState.write_back(in_states[4])
                        hazard=hazards.data_hazard(in_states)
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
                        hazard=hazards.data_hazard(in_states)
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
                    out_states[0]=State(0)
                if stall:
                    print('\n\nSTALLING\n\n')
                    if w_stall==1:
                        out_states=[in_states[1],in_states[2],State(),out_states[3]]
                    else:
                        out_states=[in_states[1],State(),out_states[2],out_states[3]]
                if not (out_states[0].is_actual_instruction or out_states[1].is_actual_instruction or out_states[2].is_actual_instruction or out_states[3].is_actual_instruction):
                        break
                in_states=[State(PC)]+out_states
                out_states=[]
                ComputerState.store_State('pipelined_data_forwarding.txt')
                input()
            
                
        #if data is not forwarded we implement stalling
        else:
            while 1:
                data_hazards=hazards.check_data_haz_stall(in_states)
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
                    print(PC)
                    out_states[0]=State()
                if data_hazards[0]:
                    print('\n\ntrue\n\n')
                    out_states=[in_states[1],State()]+out_states[2:]
                if not (out_states[0].is_actual_instruction or out_states[1].is_actual_instruction or out_states[2].is_actual_instruction or out_states[3].is_actual_instruction):
                    break
                in_states=[State(PC)]+out_states
                out_states=[]
                ComputerState.store_State('pipelined_not_data_forwarding.txt')
                input()



            
    #non-pipelined
    else:
        Simulator=State(0)
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
