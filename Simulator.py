# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 21:50:33 2021

@author: jayan
"""

Registers=[0 for j in range(32)]

def readfile(K):
    #should return a line every time it is caled 
    return K.readline()

def Fetch(inst):
    Registers[0],temp=[int(x) for x in inst.split()]
    return temp

def Decode():
    #should return opcode,fun3,func6/7,rs1,rs2,rd,imm
    pass

def Execute():
    pass
def memoryAcess():
    pass

def WriteBack():
    pass
