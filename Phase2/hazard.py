from Instruction import State,ControlUnit
class HAZ:
    def __init__(self):
        self.E2E=0
        self.M2M=0
        self.M2E=0
        self.E2D=0
        self.M2D=0
    
    def data_hazard(self,state_):
        new_states=[state_[0]]
        data_forwards= 0
        de=state_[1]
        ex=state_[2]
        me=state_[3]
        wb=state_[4]
        Hazard =False     #  0/1
        stall=False    #0 / 1
        w_stall=3
        de_opcode=de.opcode
        ex_opcode=ex.opcode
        me_opcode=me.opcode
        wb_opcode=wb.opcode
	 
	    #m2m       3 for load 35 is store
        if(wb_opcode==3 and me_opcode==35) and (wb.rd>0 and wb.rd==me.rs2):
                Hazard=True
                me.RB=wb.MDR
                self.M2M=wb.MDR
                data_forwards+=1
	
	    #m2e     load 
        if wb.rd >0:
            if wb.rd==ex.rs1:
                ex.RA=wb.MDR
                Hazard=True
                self.M2E=wb.MDR
                data_forwards+=1
            
            if wb.rd==ex.rs2:
                ex.RB=wb.MDR
                Hazard=True
                self.M2E=wb.MDR
                data_forwards+=1

		 
 	        #e2e
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
                    self.E2E=me.Alu_out
                    Hazard=True
                    data_forwards=True
                if (ex.rs2==me.rd):
                    ex.RB=me.Alu_out
                    self.E2E=me.Alu_out
                    Hazard=True
                    data_forwards+=1
            
        if (de_opcode==99 or de_opcode==103):
                #M2D
            if wb.rd>0:
                if wb.rd==de.rs1:
                    de.branchRA=wb.MDR
                    self.M2D=wb.MDR
                    Hazard=True
                    data_forwards+=1
                if wb.rd==de.rs2:
                    de.branchRB=wb.MDR
                    Hazard=True
                    self.M2D=wb.MDR
                    data_forwards+=1
	        #E2D
            if me.rd>0 :
                if me_opcode ==3:
                    Hazard=True
                    stall=True
                    w_stall=min(w_stall,2)	
                else:
                    if me.rd==de.rs1:
                        de.branchRA=me.Alu_out
                        self.E2D=me.Alu_out
                        Hazard=True
                        data_forwards+=1
			
                    if me.rd ==de.rs2 :
                        de.branchRB=me.Alu_out
                        self.E2D=me.Alu_out
                        Hazard=True
                        data_forwards+=1
	
            if ex.rd > 0 and (ex.rd== de.rs1 or ex.rd ==de.rs2):
                Hazard=True
                stall=True
                w_stall=min(w_stall,2)
	    		   
        new_states= new_states + [de,ex,me,wb]
        return [Hazard,stall,new_states,w_stall,data_forwards]

    def check_data_haz_stall(self,states):
        de=states[2]
        ex=states[3]
        me=states[4]
        if 	ex.is_actual_instruction and de.is_actual_instruction:
            if ex.rd>0:
                print(de.rs1,de.rs2)
                if ex.rd==de.rs1:
                    return [True,2]
                if ex.rd==de.rs2:
                    return [True,2]
        if me.is_actual_instruction and de.is_actual_instruction:
            if me.rd>0:
                if me.rd==de.rs1:
                    return [True,1]
                if me.rd==de.rs2:
                    return [True,1]
        return [False,-1]
