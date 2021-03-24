# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 20:48:31 2021

@author: jayanth
"""
import sys
import Simulator

if len(sys.argv)<2:
    print("Error")
    exit()

K=open(sys.argv[1],'r')
while True:
    inst=Simulator.readfile(K)
    print(inst)
    if(inst==""):
        break
    