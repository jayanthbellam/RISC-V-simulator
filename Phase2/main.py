from Instruction import State,ControlUnit
import sys

if len(sys.argv)<2:
    print("Invalid Number of arguments")
else:
    filename=sys.argv[1]
    ComputerState=ControlUnit(filename)
    stages=[State() for i in range(5)]
    outstates=[]
    PC=0
    clock=0
