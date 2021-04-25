from Instruction import State,ControlUnit,BranchTargetBuffer
import sys

if len(sys.argv)<2:
    print("Invalid Number of arguments")
else:
    filename=sys.argv[1]
    ComputerState=ControlUnit(filename)
    PC=0
    clock=0
    pipelined_execution=False
    data_forwarding=False
    btb=BranchTargetBuffer()
    if pipelined_execution:
        in_states=[State() for i in range(5)]
        out_states=[]
        if data_forwarding:
            pass
        #if data is not forwarded we implement stalling
        else:
            in_states=[(idx,val) for idx,val in enumerate(in_states)]
            in_states=in_states[::-1]
            for idx,val in in_states:
                if idx==4:
                    overflow=ControlUnit.write_back(val)
                if idx==3:
                    out_states.append(ControlUnit.memory_access(val))
                if idx==2:
                    out_states.append(ControlUnit.execute(val))
                if idx==1:
                    control_hazard,control_hazard_pc,tempstate=ControlUnit.decode(val,btb)
                    out_states.append(tempstate)
                if idx==0:
                    outcome,new_pc,tempstate=ControlUnit.fetch(val)
                    out_states.append(tempstate)
            out_states=out_states[::-1]
            if out_states[0].IR!=0:
                PC+=4
            

    else:
        Simulator=State(0)
        while 1:
            Simulator=ComputerState.fetch(Simulator)
            if not Simulator.is_actual_instruction:
                break
            Simulator=ComputerState.decode(Simulator)
            Simulator=ComputerState.execute(Simulator)
            Simulator=ComputerState.memory_access(Simulator)
            Simulator=ComputerState.write_back(Simulator)
            ComputerState.store_State()
