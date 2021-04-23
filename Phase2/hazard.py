from Instruction import State
class HDU:
    def __init__(self):
       
        self.E2E=0
        self.M2E=0
        self.M2M=0
        self.E2D=0
        self.M2D=0
        
    def check_data_hazard(self,states):
        forwarding_paths = set()
       
        new_states = []     # updated states
        new_states = [states[0]]
        toDecode = states[1]
        toExecute = states[2]
        toMem = states[3]
        toWB = states[4]
        isHazard = False    # is there a data hazard?
        doStall = False     # do we need to stall in case of data forwarding?
        stallWhere = 3      # stall at the decode stage or execute stage?
                            # 1 = at execute, 2 = at decode, 3 = don't stall
                            # Sorted according to priority

        toDecode_opcode = toDecode.IR & (0x7F)
        toExecute_opcode = toExecute.IR & (0x7F)
        toMem_opcode = toMem.IR & (0x7F)
        toWB_opcode = toWB.IR & (0x7F)
        
       

        # M->M forwarding
       
        if (toWB_opcode==3) and toMem_opcode==35:
            if toWB.rd > 0 and toWB.rd == toMem.rs2:
                toMem.RB = toWB.RY
                isHazard = True
                self.M2M=toWB.RY
                forwarding_paths.add("M->M")
