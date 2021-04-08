import sys
import Simulator

if len(sys.argv)<2:
    print("Error")
else:
    Simulator.readFile(sys.argv[1])
    Simulator.run_RISCVsim()
