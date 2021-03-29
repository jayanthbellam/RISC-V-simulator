# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 21:50:33 2021

@author: jayanth
"""
global Reg,Mem,ControlSignals
#register File
Reg=[0 for j in range(32)]

#memory
Mem=[0]*4000

#Control Signals
#A dictionary for holding the control signals
#use keys like MUXB, MUXY,RY,RZ (same as in lectures) for uniformity
ControlSignals={}
def readFile(K):
    #should return a line every time it is caled 
    return K.readline()

def fetch(inst):
    Reg[0],temp=[int(x) for x in inst.split()]
    return temp

def decode():
    #should update the CONTROL_SIGNALS
    pass

def execute():
    pass

def memoryAcess():
    pass

def writeBack():
    pass

def setToStart():
    #restores the registers to the original state
    pass

def storeState():
    #creates a file which stores the current state of Registers and Memory
    pass

def run_RISCVsim():
    #put it all together
    pass
