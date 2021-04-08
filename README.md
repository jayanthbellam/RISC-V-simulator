# RISC-V-simulator
================================================
Functional Simulator for RISCV Processor
================================================

README

Team Members' names:
Bellam Jayanth	2019CSB1080
Sagina Jaya Govinda Venkata Sai Teja	2019CSB1114
Rohit Dagar	2019EEB1186
Satia	2019CSB1118
Keshav Goyal	2019CSB1165

Table of contents
1. Directory Structure
2. How to build
3. How to execute


Directory Structure:
--------------------
CS204-Project
  |
  |- bin
      |
      |- myRISCVSim
  |- doc
      |
      |- design-doc.docx
  |- include
      |
      |- myRISCVSim.h
  |- src
      |- main.c
      |- Makefile
      |- myRISCVSim.h
  |- test
      |- simple_add.mc
      |- fib.mc
      |- array_add.mc
      |- fact.mc
      |- bubble.mc
      
How to build
------------
For building:
	$cd src
	$make

For cleaning the project:
	$cd src
	$make clean


How to execute
--------------
./myRISCVSim test/simple_add.mc

