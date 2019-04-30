"""
Course: CS 2302 [MW 1:30-2:50] 
Author: Kimberly Morales
Assignment: Lab 7
Instructor: Olac Fuentes
TA(s): Anindita Nath , Maliheh Zargaran 
Date: 4/28/2019
Date of last modification: 4/28/2019

Purpose of program: 



"""
import matplotlib.pyplot as plt
from scipy import interpolate 
import numpy as np
import random
import timeit
import math

import dsf
import graphs
from collections import deque
#################################################################################################
#MAZE METHODS
#################################################################################################

#Checks to see if two cells belong to different sets and removes a wall
#Uses standard union
def check_maze(S,w,mc,mr,m,case):
    if case == 1 or case == 2:
        while m != 0:
            dw = random.randint(0,len(w)-1) #dw: wall to remove
            c1 = dsf.find_c(S,w[dw][0])     #c1: cell 1
            c2 = dsf.find_c(S,w[dw][1])     #c2: cell 2

        #If the two cells are from different cells than remove a wall so to allow a path and combine them 
            if c1 != c2:
                del w[dw]
                dsf.union_by_size(S,c1,c2)
                m -= 1
        return w
    
    else:
        sets = num_sets(S)
        if m == len(w) or m > len(w):
            return w.clear()
        
        while m != 0:
            dw = random.randint(0,len(w)-1)
            c1 = dsf.find_c(S,w[dw][0])
            c2 = dsf.find_c(S,w[dw][1])

            if c1 != c2:
                del w[dw]
                dsf.union_by_size(S,c1,c2)
                m -= 1
                sets -= 1
        
            if sets == 1:
                del w[dw]
                m -= 1
                
        return w

#Checks to see if each cell has a simple path to another cell 
#Uses union by size and path compression 
def check_maze_uc(S,w,mc,mr,m,case):
    if case == 1 or case == 2:
        while m != 0:
            dw = random.randint(0,len(w)-1) #dw: wall to remove
            c1 = dsf.find_c(S,w[dw][0])     #c1: cell 1
            c2 = dsf.find_c(S,w[dw][1])     #c2: cell 2

        #If the two cells are from different cells than remove a wall so to allow a path and combine them 
            if c1 != c2:
                del w[dw]
                dsf.union_by_size(S,c1,c2)
                m -= 1
        return w
    
    else:
        #Checks sets and number of walls to delete
        sets = num_sets(S)
        
        #If there are more m than walls than clear the maze
        if m == len(w) or m > len(w):
            return w.clear()
        
        
        while m != 0:
            dw = random.randint(0,len(w)-1)
            c1 = dsf.find_c(S,w[dw][0])
            c2 = dsf.find_c(S,w[dw][1])

            if c1 != c2:
                del w[dw]
                dsf.union_by_size(S,c1,c2)
                m -= 1
                sets -= 1
            
            #If there is one more set then delete the last wall
            if sets == 1:
                del w[dw]
                m -= 1
                
        return w

#Counts the total number of sets
def num_sets(S):
    count = 0
    
    #Checks each set to see if they have similar parents
    for i in range(len(S)):
        ri = dsf.find(S,i)
        
        #If the element equal to the root then it is in the same set
        if i == ri:
            count+=1
    return count
#################################################################################################
#DRAW METHODS
#################################################################################################
              
def draw_maze(walls,maze_rows,maze_cols, cell_nums=False):
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

#Draws shortest path based on the path algorithms
def draw_path(v, maze_rows,maze_cols):
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

    ct = []
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    
    #Add in coordinates used for the text
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols

            ct.append([c+.5,r+.5])
               
            
    p = 0   #p: previous coordinate traveled to 
    
    #Traverse through each point in the path
    for i in v:
        ax.plot((ct[p][0],ct[i][0]),(ct[p][1],ct[i][1]), linewidth=2,color='r')
        
        #So that the path does not repeat and to point previous to the already plotted
        if i != 0:
            p = i

    ax.axis('off') 
    ax.set_aspect(1.0)
    

#Draws graphical representation of the maze based on the structure
def draw_graph_maze(G,r,c):
    fig, ax = plt.subplots()
    n = len(G)
    r = 30

    coords = []
    
    #These are in charge of maintaining the graph structure
    numr = 0    #Row num
    numc = 0    #Col num
    for i in range(r):
        for j in range(c):
            coords.append([numr,numc])
            numr += 1
        numr = 0
        numc += 1
        
    for i in range(n):
        for dest in G[i]:
            ax.plot([coords[i][0],coords[dest][0]],[coords[i][1],coords[dest][1]],
                     linewidth=1,color='k')
    for i in range(n):
       ax.text(coords[i][0],coords[i][1],str(i), size=10,ha="center", va="center",
        bbox=dict(facecolor='w',boxstyle="circle"))
        
        
    ax.set_aspect(1.0)
    ax.axis('off') 

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

def maze_adjlist(wo,w,cells):
    #Create empty list of size of cells so to generate a graph
    a = [ [] for i in range(cells) ]

    #Traverse through original list with no deleted walls
    for g in wo:
        #Check if the current wall was not deleted and if not then add it to the graph
        if g not in w:
            #Add adjacent connections
            a[g[0]].append(g[1])
            a[g[1]].append(g[0])
    return a


#Breadth first search 
def bfs(G,v):
    q = []
    q.append(v)
    visited[v] = True
    
    while(len(q) is not 0):
        u = q.pop(0)    #Pop the first element 
        for t in G[u]:
            if(visited[t] is False):
                visited[t] = True
                prev[t] = u
                q.append(t)
    return prev

#Depth first search with a stack 
#Very similar to bfs but replaced with a stack
def dfs_s(G, v):
    s = []
    s.append(v)
    visited[v] = True
    
    while len(s) != 0:
        u = s.pop() #Only pop the back element
        for t in G[u]:
            if(visited[t] is False):
                visited[t] = True
                prev[t] = u
                s.append(t)
    return prev

#Depth first search with recursion
#Uses global variables so that it doesn't forget
def dfs_rec(G, v, visited,prev):
    visited[v] = True
    for t in G[v]:
        if (visited[t] is False):
            prev[t] = v
            dfs_rec(G,t,visited,prev)
    return prev

#Prints path traversal
def print_path(prev, v):
    if prev[v] != -1:
        print_path(prev,prev[v])
        print('-',end='')
    print(v,end='')

#Uses print path code but instead returns an array
def gen_path(prev, v, path):
    if prev[v] != -1:
        gen_path(prev,prev[v],path)
        
    path.append(v)
    return path


#################################################################################################
#MAIN
#################################################################################################
if __name__ == "__main__":
    plt.close("all") 
    maze_size = 0                               #maze_size: Size of maze (rows * cols)
    maze_rows = int(input('Maze Rows: '))
    maze_cols = int(input('Maze Cols: '))
    
    walls = wall_list(maze_rows,maze_cols)
    walls_org = wall_list(maze_rows,maze_cols)
    
    n = maze_rows * maze_cols	                #num of cells n
    m = int(input('Num of walls to remove: '))  #num of walls to remove m
    
    #Cases so to appropriately draw the maze 
    if m < (n-1):
        print('A path from source to destination is not guaranteed to exist')
        case = 1
        
    elif m == (n-1):
        print('There is a unique path from source to destination')
        case = 2
        
    else:
        print('There is at least one path from source to destination')
        case = 3
        
    #Draws initial maze with numbers
    draw_maze(walls,maze_rows,maze_cols,cell_nums=True) 
    
    #Create dsf with the size of the maze(rows * cols)
    S = dsf.DisjointSetForest(n)
    
    #Create valid maze based on the previous case
    check_maze_uc(S,walls,maze_cols,maze_rows,m,case)
    draw_maze(walls,maze_rows,maze_cols) 
    
    #Make an adjacency list
    G = maze_adjlist(walls_org,walls,n)
    print('Adjacency List: ',G)
    
    #Draw the grapical representation of the maze
    draw_graph_maze(G,maze_rows,maze_cols)
    
    #Create global variables for the algorithms
    global visited
    global prev
    visited = [ False for i in range(len(G)) ]
    prev = [-1 for i in range(len(G))]
    
    #BFS
    print('Breadth First Search: ')
    global v
    v = gen_path(bfs(G,0),n-1,[])
    print(v)

    
    #DFS REC    
    dv = [ False for i in range(len(G)) ]
    dp = [-1 for i in range(len(G))]
    print('\nDepth First Search: ')
    v = gen_path(dfs_rec(G,0,dv,dp),n-1,[])
    print(v)
    
    #DFS
    print('\nDepth First Search /w Stack: ')
    v = gen_path(dfs_s(G,0),n-1,[])
    print(v)
    
    #Draw the path
    if len(v) != 1:
        draw_path(v,maze_rows,maze_cols)



