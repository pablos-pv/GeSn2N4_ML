################################################################### 
# Program with which to transform the atomic indices given by SOD to those used in CELL
#
# It reads the file Atom_assignments_SOD.txt, which has the following format:
# - First column:    configuration number
# - Second column:   multiplicity
# - Rest of columns: numbers of the substituted atoms of the unit cell, given by SOD 
# 
# It also reads the file exchange_atoms_sod_cell.txt, which has a list of 32 pairs of numbers, 
# consisting of a first number (from 0 to 31), representing the number of an atom in the unit
# cell created by SOD (which has 32 atoms), and a second number (from 0 to 31), representing the
# number of an atom in the unit cell created by the CELL code.
#
# The output is the file decorations.txt, which has the decorations with the substitutions that
# the CELL code uses to calculate the cluster expansion coefficients.
#
# These decorations are used in the final part of the code to create a set of different CEEL input
# files, which are also run in this code. 
#
# Finally, the correlations are reported in the file correlation_matrix.txt
#################################################################### 

#coding:utf-8
import glob
import re
import os
import sys
import shutil
import math
import numpy as np
import shutil
import matplotlib.pyplot as plt
from matplotlib import pyplot
from numpy import savetxt
from matplotlib.pyplot import *
import subprocess


nsites   = 24 # Number of sites in which to insert the substituting atoms
nsubs    =  8  # Number of substitutions
siteOrig = 50 # Atomic number of the atom in the parent structure
siteSubs = 32 # Atomic number of the substituting atom 


# Open the file with the atom assignments given by SOD
inputfile = open("Atom_assignments_SOD.txt") 

# read file 
InpFile = inputfile.read() 
inputfile.seek(0) 
InpFile 

####################################################################
# Function that will return number of lines of a file           ####
def countlines(file): 
	line = 0
	for word in file: 
		if word == '\n': 
			line += 1
	return line
                                                               #####
####################################################################
nlines = countlines(InpFile) 
print('nlines=',nlines)

####################################################################
# Open the file with the information about how to convert the atom 
# assignments given by SOD to those used by CELL
changes = np.genfromtxt('exchange_atoms_sod_cell.txt')
ini = np.genfromtxt('exchange_atoms_sod_cell.txt', usecols=(0))
end = np.genfromtxt('exchange_atoms_sod_cell.txt', usecols=(1))
ini = changes[:, 0]+1
end = changes[:, 1]+1
print ("ini")
print (ini)
print ("end")
print (end)
print ("")
####################################################################


#####################################################################
alldata = np.genfromtxt(inputfile.name)
nconf = np.genfromtxt(inputfile.name, usecols=(0))
multi = np.genfromtxt(inputfile.name, usecols=(1))
atom0float = np.genfromtxt(inputfile.name, usecols=(2))     # 1
atom1float = np.genfromtxt(inputfile.name, usecols=(3))     # 2
atom2float = np.genfromtxt(inputfile.name, usecols=(4))     # 3
atom3float = np.genfromtxt(inputfile.name, usecols=(5))     # 4
atom4float = np.genfromtxt(inputfile.name, usecols=(6))     # 5
atom5float = np.genfromtxt(inputfile.name, usecols=(7))     # 6
atom6float = np.genfromtxt(inputfile.name, usecols=(8))     # 7
atom7float = np.genfromtxt(inputfile.name, usecols=(9))     # 8

atom0  = atom0float.astype(int)   # 1
atom1  = atom1float.astype(int)   # 2
atom2  = atom2float.astype(int)   # 3
atom3  = atom3float.astype(int)   # 4
atom4  = atom4float.astype(int)   # 5
atom5  = atom5float.astype(int)   # 6
atom6  = atom6float.astype(int)   # 7
atom7  = atom7float.astype(int)   # 8

config = list(zip(atom0,atom1,atom2,atom3,atom4,atom5,atom6,atom7))
print('config=',config[0:2][0:2][0:2][0:2][0:2][0:2][0:2][0:2])
confignew = config
print('type(confignew)=',type(confignew[0])) 
confignew = np.array(config)
print('confignew=',confignew[0]) 
print('type(confignew)=',type(confignew[0])) 

nconfs = len(config)
print('nconfs=',nconfs)


deco = np.full((len(config), nsites), siteOrig)

fout       = open('decorations.txt', "wt")

for i in range(nconfs):
	for j in range(nsubs):
		confignew[i][j] = end[config[i][j]-1]

	for j in range(nsites):
		for k in range(nsubs):
			if confignew[i][k] == j+1: 
				deco[i][j] = siteSubs

	fout.write('strset.add_structure(Structure(scell,[')
	for m in range(len(deco[i])):
		if m < len(deco[i])-1:
			fout.write(str(deco[i][m]) +', ')
		if m == len(deco[i])-1:
			fout.write(str(deco[i][m]))
	fout.write('] ),write_to_db=True)'+'\n')


fout.close()


###############################################################################################
# Prepare the CELL input files and run them, in batches, to make it faster
 


#############################################################
# Parameters:
# nRuns = 3
nConfs = 100
#############################################################

#############################################################
# Read the file with the decorations in the CELL input format
def readDecorations():
    with open('decorations.txt','r') as decorationsFile:
        decorations = decorationsFile.readlines()
#        decorations = decorationsFile.read().splitlines()
    print(decorations[-1])
    return decorations


#############################################################
# Divide decorations.txt into nRuns files
def divideDecorations(decorations,nConfs):
    
    # Calculate the number of decorations
    count = 0
    for line in decorations:
        count += 1
    
    nDecorations = count
    print('The number of decorations is',nDecorations)
    
    # Calculate the number of files to create
    nFiles = math.ceil(nDecorations / nConfs)
    print('The number of files to write is',nFiles)
    
    
    for File in range(nFiles):
        confIni = File*nConfs
        confFin = confIni+nConfs

        with open('file_'+str(File), 'w') as f:
            count = 0
            for line in decorations:
                if count >= confIni and count < confFin:
                    f.write(line)
                count += 1
                
    cwd = os.getcwd()


    try:
        os.remove('totalcorrelationmatrix.txt')
    except OSError as error:
        pass        
    
    # Create the CELL input files
    for i in range(nFiles):
        with open('ce_input_'+str(i)+'.py', 'w') as outFile:
          with open('cell_input_top.py', 'r') as ff1:
            shutil.copyfileobj(ff1, outFile)
          with open('file_'+str(i), 'r') as ff2:
            shutil.copyfileobj(ff2, outFile)
          with open('cell_input_bottom.py', 'r') as ff3:
            shutil.copyfileobj(ff3, outFile)

        file = 'ce_input_'+str(i)+'.py'
        path = 'ce_input_'+str(i)
        shutil.rmtree(path, ignore_errors=True)
        os.makedirs(path)
        shutil.copy(file, path)
        os.chdir(path)
        subprocess.call(["/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7",file,"> out"])


        matrix = [line.strip() for line in open("correlationmatrix.txt", 'r')]
        print('len(matrix)=',len(matrix))
        os.chdir(cwd)
        with open ('totalcorrelationmatrix.txt', 'a') as f:

            for ii in range(len(matrix)):
                for jj in range(len(matrix[ii])):
                    f.write(str(matrix[ii][jj]))
                
                f.write('\n')


decorations = readDecorations()
divideDecorations(decorations,nConfs)

try:
    os.remove('correlation_matrix.txt')
except OSError as error:
    pass

with open ('correlation_matrix.txt', 'a') as f:
    with open('totalcorrelationmatrix.txt', 'r') as inputfile:
        for line in inputfile.readlines():
            corr = line.split()[1:]
            for i in range(len(corr)):
                f.write(corr[i]+' ')

            f.write('\n')

