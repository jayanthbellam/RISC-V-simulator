# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 21:50:33 2021

@author: jayan
"""

Registers=[0 for j in range(32)]

def readFile(K):
    #should return a line every time it is caled 
    return K.readline()

def fetch(inst):
    Registers[0],temp=[int(x) for x in inst.split()]
    return temp

def decode():
    #should return opcode,fun3,func6/7,rs1,rs2,rd,imm
    pass

def execute():
    pass
def memoryAcess():
    pass

def writeBack():
    pass

def setToDefault():
    #this should make sure that after completion/before start of program registers and memory is set to its original state
    pass
