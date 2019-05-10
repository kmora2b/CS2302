"""
Course: CS 2302 [MW 1:30-2:50] 
Author: Kimberly Morales
Assignment: Lab 8
Instructor: Olac Fuentes
TA(s): Anindita Nath , Maliheh Zargaran 
Date: 5/9/2019
Date of last modification: 5/9/2019

Purpose of program: 
To implement interesting algorithms to solve problems that often require a
more efficient algorithm with faster times. 
These two problems are to discover trig identities with a randomized algorithm 
and to find two equal subsets of a set with backtracking. 


"""
import random
import numpy as np
import math
import mpmath
from math import *

#################################################################################################
#TRIG DISCOVERY METHODS
#################################################################################################
#Finds equivalent identiites and is modified to accomodate sec
def equal(f1, f2, tries=1000,tolerance=0.0001):
    for i in range(tries):
        x = random.uniform(-math.pi,math.pi)
        
        if f1 == 'sec(x)':
            f1 = 'mpmath.sec(x)'
            
        if f2 == 'sec(x)':
            f2 = 'mpmath.sec(x)'
            
        y1 = eval(f1)
        y2 = eval(f2)
        if np.abs(y1-y2)>tolerance:
            return False
    return True

#Gets list of strings read from the file and inserts random values where x is 
def gen_rand_trig(exp,x):
    for l in exp:
        if l == "x":
            exp = exp.replace(l,str(x))
    return exp

def discover_trig(fx):
    found = 0   #found: Counts the total number of identities found
    allE = []   #allE: All expressions
    E = []      #Contains only indentities
    print('Equivalent Identities')
    
    #Goes through each trig function read from the file
    for i in range(len(fx)):
        for j in range(len(fx)-1):
            #Make sure no functions are repeated
            if i != j:
                f1 = fx[i]
                f2 = fx[j]
                allE.append([f1,f2])
                
                #If the functions are equal then add to E and count
                if equal(f1,f2):
                    print(f1, ' = ', f2)
                    E.append([f1,f2])
                    found += 1
    #Returns the number of identities found, equivalent identities, and all expressions
    return found,E,allE

#Tests each expression with randomized values
def test_equals(stmt,tries=1000,tolerance=0.0001):
    for e in stmt:
        b = True        #b: boolean flag to see if expression is equal
        x = random.uniform(-math.pi,math.pi)
        
        #Replaces x with random value for both functions
        t1 = gen_rand_trig(e[0],x)  
        t2 = gen_rand_trig(e[1],x)  
        
        #Concatenates strings for sec functions
        if t1 == 'sec(' + str(x) + ')':
            t1 = 'mpmath.sec(' + str(x) + ')'
            
        if t2 == 'sec(' + str(x) + ')':
            t2 = 'mpmath.sec(' + str(x) + ')'
        y1 = eval(t1)
        y2 = eval(t2)
        
    
        if np.abs(y1-y2)>tolerance:
            b = False
        
        #Identities are printed if true with '='
        # '!=' indicates it is not equivalent
        if b:
            print(t1, ' = ', t2)
        else:
            print(t1, ' != ', t2)
            
#Reads in trig functions from a text file and appends to a string list
def read_file(filename):
    fx = []
    with open(filename) as f:
        for line in f:
            fx.append(line.replace('\n',''))
    return fx


#################################################################################################
#PARTITION SUBSETSUM METHODS
#################################################################################################

def subsetsum(S,last,goal):
    if goal ==0:
        return True, []
    if goal<0 or last<0:
        return False, []
    res, subset = subsetsum(S,last-1,goal-S[last]) # Take S[last]
    if res:
        subset.append(S[last])
        return True, subset
    else:
        return subsetsum(S,last-1,goal) # Don't take S[last]
    
#Finds two equal subsets of set S
def partition(S):
    p_exist = False   #p_exist: If a subset can exist
    
    #If the sum of the set is even then a solution is possible
    if sum(S) % 2 == 0 :
        #The goal is half of the set since the two subsets will equal to S
        p_exist,s = subsetsum(S,len(S)-1,sum(S)/2)
        
        if p_exist:
            print("Partition Exists for ",S)
            
            #Since subsetsum gets one solution, look through other half of list for second solution
            for se in s:
                index = 0
                for se2 in S:
                    if se == se2:
                        S.pop(index)
                    index += 1
            return s, S
        else:
            print("There are no equal subsets")

    else:
        print("Partition does not exist")
    return p_exist


#################################################################################################
#MAIN
#################################################################################################
if __name__ == "__main__":
    #Reads in file with trig identities and prints list
    print("DISCOVER TRIG IDENTITIES")
    fx = read_file('t.txt')
    
    #If the file cannot be read due to OS then here is the hardcoded list
    """
    fx = ['sin(x)', 'cos(x)', 'tan(x)', 'sec(x)', '-sin(x)', '-cos(x)', '-tan(x)', 
    'sin(-x)', 'cos(-x)', 'tan(-x)', 'sin(x)/cos(x)', '2*sin(x/2)*cos(x/2)', 
    'sin(x)*sin(x)', '1-(cos(x) * cos(x))', '(1-cos(2*x))/(2)', '(1)/(cos(x))']
    """
    
    print('Identities read from file: ')
    print(fx)
    print()
    results = discover_trig(fx)
    
    #Prints results and equality test
    print('Found: ', results[0])
    
    #If you do not want to see the dump then comment out here
    #########################################################
    #print('\nTest Equalties: ')
    #test_equals(results[2])
    #########################################################
    print()
    
    #Answers question two with partitions
    print("PARTITION SUBSETSUM")
    S = [20,0,10,10]
    print("Sum of S: ", sum(S))
    print(partition(S))

