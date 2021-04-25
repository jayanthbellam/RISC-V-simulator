from Instruction import State,ControlUnit,BranchTargetBuffer
class HAZ:
    def __init__(self):
        self.E2E=0
        self.M2M=0
        self.M2E=0
        self.E2D=0
        self.M2D=0
    
    def data_hazard(self,state_):
        new_states=[]
        data_forwards= set()
        de=state_[1]
        ex=state_[2]
        me=state_[3]
        wb=state_[4]
        Hazard =0     #  0/1
        stall=0    #0 / 1
        w_stall=3
        de_opcode=de.opcode
        ex_opcode=ex.opcode
        me_opcode=me.opcode
        wb_opcode=wb.opcode
	 
	    #m2m       3 for load 35 is store
        if(wb_opcode==3 and me_opcode==35) and (wb.rd>0 and wb.rd==me.rs2):
                Hazard=1
                me.RB=wb.MDR
                self.M2M=wb.MDR
                data_forwards.add("M2M")
	
	    #m2e     load 
        if wb.rd >0:
            if wb.rd==ex.rs1:
                ex.RA=wb.MDR
                Hazard=1
                self.M2E=wb.MDR
                data_forwards.add("M2E")
            
            if wb.rd==ex.rs2:
                ex.RB=wb.MDR
                Hazard=1
                self.M2E=wb.MDR
                data_forwards.add("M2E")

		 
 	        #e2e
            if me.rd>0:
                if me_opcode==3:
                    if ex_opcode==35:
                        if ex.rs1==me.rd:
                            Hazard=1
                            stall=1
                            w_stall=min(w_stall,1)
                    else:
                        Hazard=1
                        stall=1
                        w_stall=min(w_stall,1)
			 
                else:
                    if (ex.rs1==me.rd):
                        ex.RA=me.ALU_out
                        self.E2E=me.ALU_out
                        Hazard=1
                        data_forwards.add("E2E")

                    if (ex.rs2==me.rd):
                        ex.RB=me.ALU_out
                        self.E2E=me.ALU_out
                        Hazard=1
                        data_forwards.add("E2E")
            
            if (de_opcode==99 or de_opcode==103):
                #M2D
                if wb.rd>0:
                    if wb.rd==de.rs1:
                        de.rs1=wb.MDR
                        self.M2D=wb.MDR
                        Hazard=1
                        data_forwards.add("M2D")
                    if wb.rd==de.rs2:
                        de.rs2=wb.MDR
                        Hazard=1
                        self.M2D=wb.MDR
                        data_forwards.add("M2D")
	        #E2D
                if me.rd>0 :
                    if me_opcode ==3:
                        Hazard=1
                        stall=1
                        w_stall=min(w_stall,2)	
                    else:
                        if me.rd==de.rs1:
                            de.rs1=me.ALU_out
                            self.E2D=me.ALU_out
                            Hazard=1
                            data_forwards.add("E2D")
			 
                        if me.rd ==de.rs2 :
                            de.rs2=me.ALU_out
                            self.E2D=me.ALU_out
                            Hazard=1
                            data_forwards.add("E2D")
	
                if ex.rd > 0 and (ex.rd== de.rs1 or ex.rd ==de.rs2):
                    Hazard=1
                    stall=1
                    w_stall=min(w_stall,2)
	    		   
        new_states= new_states + [de,ex,me,wb]
        return [Hazard,stall,new_states,w_stall,data_forwards]

    def check_data_haz_stall(self,states):
        de=states[1]
        fe=states[0]
        ex=states[2]
        me=states[3]
        if (ex.rd!=-1 and de.rs1!=-1) and (ex.is_actual_instruction!=False and de.is_actaul_instruction!=False): 
            if ex.rd == de.rs1 :
                if ex.rd!=0 :
                    return [True,2]
                
            if ex.rd==de.rs2:
                if ex.rd!=0:
                    return [True,2]
	            
        if (me.rd!=-1 and de.rs1!=-1) and (me.is_actual_instruction!=False and de.is_actual_instruction!=False):
            if me.rd == de.rs1:
                if me.rd!=0 :
                    return [True,1]
            
            if me.rd==de.rs2:
                if me.rd!=0:
                    return [True,1]	
        return [False,-1]
