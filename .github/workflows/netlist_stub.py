################################################################################
# Created on Fri Aug 24 13:36:53 2CONST_ZERO18                                 #
#                                                                              #
# @author: olhartin@asu.edu; updates by sdm, Ebholo Ijieh                      #
# ebholo.ijieh@gmail.com or eijieh@asu.edu Aug 27 2020                         #
#                                                                              #
# Program to solve resister network with voltage and/or current sources        #
################################################################################

import numpy as np                     # needed for arrays
from numpy.linalg import solve         # needed for matrices
from read_netlist import read_netlist  # supplied function to read the netlist
import comp_constants as COMP          # needed for the common CONST_ONEs

# this is the list structure that we'll use to hold components:
# [ Type, Name, i, j, Value ]

################################################################################
# How large a matrix is needed for netlist? This could have been calculated    #
# at the same time as the netlist was read in but we'll do it here             #
# Input:                                                                       #
#   netlist: list of component lists                                           #
# Outputs:                                                                     #
#   node_cnt: number of nodes in the netlist                                   #
#   volt_cnt: number of voltage sources in the netlist                         #
################################################################################

CONST_ONE = 1
is_current_file = False
CONST_ZERO = 0
def get_dimensions(netlist):                                                #pass in the netlist
    volt_cnt = CONST_ZERO                                                   #initialize the voltage source  counter to zero
    node_cnt = CONST_ZERO                                                   #initialize the number of nodes counter to zero
    unique_list = []
    for component in netlist:
        
        if ((component[COMP.TYPE]==COMP.IS)
              or(component[COMP.TYPE]==COMP.VS)):
              volt_cnt += CONST_ONE
              
        unique_list.append(component[COMP.I])
        unique_list.append(component[COMP.J])
    type_set = set(unique_list)
    node_cnt=len(type_set)
            
    print(' Nodes: ', node_cnt, ' \n Voltage sources: ', volt_cnt)
    return node_cnt,volt_cnt

################################################################################
# Function to stamp the components into the netlist                            #
# Input:                                                                       #
#   m_admittance:    the admittance matrix                                            #
#   netlist:  list of component lists                                          #
#   currents: the matrix of currents                                           #
#   node_cnt: the number of nodes in the netlist                               #
# Outputs:                                                                     #
#   node_cnt: the number of rows in the admittance matrix                      #
################################################################################

def stamper(m_admittance,netlist,currents,node_count):
    # return the total number of rows in the matrix for
    # error checking purposes
    # add 1 for each voltage source...
    
    #M = node_count-1#np.shape(m_admittance)[CONST_ONE] - 1
    M = node_count#currents.reshape(M+CONST_ONE,CONST_ONE)
    CUNT = CONST_ONE
    for comp in netlist:                                                        # for each component...
        #print(' comp ', comp)                                                  # which one are we handling...
        i = comp[COMP.I]
        j = comp[COMP.J]
        node_cnt =CONST_ZERO
        rows = np.shape(m_admittance)[CONST_ZERO]
        if (comp[COMP.TYPE] == COMP.VS ):                                       #voltage source

            if(i>=CONST_ZERO):
                m_admittance[M,i] = CONST_ONE
                m_admittance[i,M] = CONST_ONE
            if(j<=CONST_ZERO):
                m_admittance[M,j] = -CONST_ONE
                m_admittance[j,M] = -CONST_ONE  
            currents[M] = comp[COMP.VAL]                                        #which matrix
            M +=1   
        if ( comp[COMP.TYPE] == COMP.R ):                                       #a resistor
            if (i >= CONST_ZERO and j >= CONST_ZERO):                           #subtract off the diagonal
                m_admittance[i,j] += -CONST_ONE/comp[COMP.VAL]
                m_admittance[j,i] += -CONST_ONE/comp[COMP.VAL]        
            if (i >= CONST_ZERO):                                               #add on the diagonal
                m_admittance[i,i] += CONST_ONE/comp[COMP.VAL]
            if (j >= CONST_ZERO):                                               #add on the diagonal
                m_admittance[j,j] += CONST_ONE/comp[COMP.VAL]
                
        elif (comp[COMP.TYPE] == COMP.IS):                                      #current source
            global is_current_file 
            is_current_file =True
            if(i>=CONST_ZERO):
                currents[i] = -comp[COMP.VAL]
            if(j>=CONST_ZERO):
                currents[j] = comp[COMP.VAL]
        CUNT += 1
        
    node_cnt = rows

    return node_cnt                                                             #should be same as number of rows!

################################################################################
# Start the main program now...                                                #
################################################################################

# Read the netlist!
netlist = read_netlist()

# Print the netlist so we can verify we've read it correctly
for index in range(len(netlist)):
    print(netlist[index])
print("\n")

node_count,num_souces = get_dimensions(netlist)                                 #get the size of the matrix needed

# Set up matrices and vectors
admittance = np.zeros([node_count+num_souces,node_count +num_souces],float)        #matrix for resistors + row/column to the admittance matrix
voltages = np.zeros([node_count+num_souces],float)                              # voltage array
currents = np.zeros([node_count+num_souces],float)                              # current array

# stamp each component into netlist
num_nodes = stamper(admittance, netlist, currents, node_count)
print('\nadmittance matrix: \n',admittance)                                     # print admittance matrix

print('\ncurrent matrix: \n',currents)                                          # print admittance matrix


################################################################################
# Given NxN Matrix, reduce the dimension to N-1 by N-1 matrix
# Given Nx1 matrix, reduce the dimention to N-1 by 1 matrix                                                   #
################################################################################

N=node_count+num_souces-CONST_ONE
if (is_current_file):                     
    current_data= np.zeros([N-num_souces,CONST_ONE],float)
    reduced_m = np.zeros([N-num_souces,N-num_souces],float)
    for i in range(N-num_souces):
        for j in range (N-num_souces):
            reduced_m[i,j]=admittance[i+CONST_ONE,j+CONST_ONE]
    print("\n reduced admittance matrix for current file: \n ",reduced_m)
    for i in range(N-num_souces):
        current_data[i]=currents[i+CONST_ONE]
    print("\n reduced current matrix: \n ",current_data)
    curr = solve(reduced_m,current_data)
    print('\nresults of currents:\n ',curr)

else:
    current_dat = np.zeros([N],float)
    reduced_mat = np.zeros([N,N],float)
    for i in range(N):
        for j in range (N):
            reduced_mat[i,j]=admittance[i+CONST_ONE,j+CONST_ONE]    
    print("\n reduced admittance matrix: \n ",reduced_mat) 
    for i in range(N+CONST_ONE):
        current_dat[i-CONST_ONE]=currents[i]
    print("\n reduced current matrix: \n ",current_dat)
    curr = solve(reduced_mat,current_dat)
    print('\nvoltages/currents:\n ',curr)

