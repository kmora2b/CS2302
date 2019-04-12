"""
Course: CS 2302 [MW 1:30-2:50] 
Author: Kimberly Morales
Assignment: Lab 6
Instructor: Olac Fuentes
TA(s): Anindita Nath , Maliheh Zargaran 
Date: 4/11/2019
Date of last modification: 4/11/2019

Purpose of program: 
To generate random mazes by knocking down walls and to have each cell have a simple path to each cell.
This requires using the disjoint set forest(dsf) class and utilizing the union and find methods.
Then to see the difference running times, use path compression and standard union.


"""
import matplotlib.pyplot as plt
from scipy import interpolate 
import numpy as np
import random
import timeit
#################################################################################################
#DISJOINT SET FOREST CLASS
#################################################################################################

def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1
        
def dsfToSetList(S):
    #Returns aa list containing the sets encoded in S
    sets = [ [] for i in range(len(S)) ]
    for i in range(len(S)):
        sets[find(S,i)].append(i)
    sets = [x for x in sets if x != []]
    return sets

def find(S,i):
    # Returns root of tree that i belongs to
    if S[i]<0:
        return i
    return find(S,S[i])

def find_c(S,i): #Find with path compression 
    if S[i]<0: 
        return i
    r = find_c(S,S[i]) 
    S[i] = r 
    return r
    
def union(S,i,j):
    # Joins i's tree and j's tree, if they are different
    ri = find(S,i) 
    rj = find(S,j)
    if ri!=rj:
        S[rj] = ri

def union_c(S,i,j):
    # Joins i's tree and j's tree, if they are different
    # Uses path compression
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj:
        S[rj] = ri
         
def union_by_size(S,i,j):
    # if i is a root, S[i] = -number of elements in tree (set)
    # Makes root of smaller tree point to root of larger tree 
    # Uses path compression
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj:
        if S[ri]>S[rj]: # j's tree is larger
            S[rj] += S[ri]
            S[ri] = rj
        else:
            S[ri] += S[rj]
            S[rj] = ri
#################################################################################################
#MAZE METHODS
#################################################################################################
    
def draw_maze(walls,maze_rows,maze_cols,cell_nums=False):
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0] ==1: #vertical wall
            x0 = (w[1]%maze_cols)
            x1 = x0
            y0 = (w[1]//maze_cols)
            y1 = y0+1
        else:#horizontal wall
            x0 = (w[0]%maze_cols)
            x1 = x0+1
            y0 = (w[1]//maze_cols)
            y1 = y0  
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    sx = maze_cols
    sy = maze_rows
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    if cell_nums:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r*maze_cols   
                ax.text((c+.5),(r+.5), str(cell), size=10,
                        ha="center", va="center")
    ax.axis('off') 
    ax.set_aspect(1.0)

def wall_list(maze_rows, maze_cols):
    # Creates a list with all the walls in the maze
    w =[]
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            if c!=maze_cols-1:
                w.append([cell,cell+1])
            if r!=maze_rows-1:
                w.append([cell,cell+maze_cols])
    return w

#################################################################################################
#LAB METHODS
#################################################################################################

#Checks to see if two cells belong to different sets and removes a wall
#Uses standard union
def check_maze(S,w,mc,mr):
    while num_sets(S) > 1:
        dw = random.randint(0,len(w)-1) #dw: wall to remove
        c1 = find(S,w[dw][0])           #c1: cell 1
        c2 = find(S,w[dw][1])           #c2: cell 2

        #If the two cells are from different cells than remove a wall so to allow a path and combine them 
        if c1 != c2:                    
            del w[dw]
            union(S,c1,c2)
    return w

#Checks to see if each cell has a simple path to another cell 
#Uses union by size and path compression 
def check_maze_uc(S,w,mc,mr):
    while num_sets(S) > 1:
        dw = random.randint(0,len(w)-1)
        c1 = find_c(S,w[dw][0])
        c2 = find_c(S,w[dw][1])

        if c1 != c2:
            del w[dw]
            union_by_size(S,c1,c2)
    return w

#Counts the total number of sets
def num_sets(S):
    count = 0
    
    #Checks each set to see if they have similar parents
    for i in range(len(S)):
        ri = find(S,i)
        
        #If the element equal to the root then it is in the same set
        if i == ri:
            count+=1
    return count

#################################################################################################
#MAIN
#################################################################################################
plt.close("all") 

maze_rows = int(input('Maze Rows: '))
maze_cols = int(input('Maze Cols: '))
walls = wall_list(maze_rows,maze_cols)

#Draws initial maze with numbers
draw_maze(walls,maze_rows,maze_cols,cell_nums=True) 

#Create dsf with the size of the maze(rows * cols)
S = DisjointSetForest(maze_rows*maze_cols)

#Time creation of maze with standard union
start = timeit.default_timer()	
check_maze(S,walls,maze_cols,maze_rows)
stop = timeit.default_timer()
print('Running time for Standard Union: ', stop - start)

#Time creation of maze with union by size
startC = timeit.default_timer()	
check_maze_uc(S,walls,maze_cols,maze_rows)
stopC = timeit.default_timer()
print('Running time for Union by Size /w Path Compression: ', stopC - startC)

#Draw final maze
draw_maze(walls,maze_rows,maze_cols) 


