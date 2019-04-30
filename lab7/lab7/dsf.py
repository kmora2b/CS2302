# Implementation of disjoint set forest 
# Programmed by Olac Fuentes
# Last modified March 28, 2019
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate 

def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1

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

def NumSets(S):
    count =0
    for i in range(len(S)):
        if S[i]<0:
            count += 1
    return count
        
def draw_dsf(S):
    scale = 30
    fig, ax = plt.subplots()
    for i in range(len(S)):
        if S[i]<0: # i is a root
            ax.plot([i*scale,i*scale],[0,scale],linewidth=1,color='k')
            ax.plot([i*scale-1,i*scale,i*scale+1],[scale-2,scale,scale-2],linewidth=1,color='k')
        else:
            x = np.linspace(i*scale,S[i]*scale)
            x0 = np.linspace(i*scale,S[i]*scale,num=5)
            diff = np.abs(S[i]-i)
            if diff == 1: #i and S[i] are neighbors; draw straight line
                y0 = [0,0,0,0,0]
            else:      #i and S[i] are not neighbors; draw arc
                y0 = [0,-6*diff,-8*diff,-6*diff,0]
            f = interpolate.interp1d(x0, y0, kind='cubic')
            y = f(x)
            ax.plot(x,y,linewidth=1,color='k')
            ax.plot([x0[2]+2*np.sign(i-S[i]),x0[2],x0[2]+2*np.sign(i-S[i])],[y0[2]-1,y0[2],y0[2]+1],linewidth=1,color='k')
        ax.text(i*scale,0, str(i), size=20,ha="center", va="center",
         bbox=dict(facecolor='w',boxstyle="circle"))
    ax.axis('off') 
    ax.set_aspect(1.0)
    
if __name__ == "__main__":     
    plt.close("all")      
    S = DisjointSetForest(8)
    print(S)
    draw_dsf(S) 
    union(S,7,6)
    print(S) 
    draw_dsf(S)
    union(S,0,2)
    print(S)
    draw_dsf(S)
    union(S,6,3)
    print(S)
    draw_dsf(S)
    union(S,5,2)
    print(S)
    draw_dsf(S)
    union(S,4,6)
    print(S)
    draw_dsf(S)    
    print('Sets encoded by DSF:',dsfToSetList(S))
    
    
    T = DisjointSetForest(8)
    union(T, 7 , 0 )
    union(T, 1 , 6 )
    union(T, 3 , 0 )
    union(T, 0 , 6 )
    union(T, 3 , 4 )
    union(T, 2 , 5 )
    union(T, 6 , 0 )
    union(T, 0 , 3 )
    union(T, 4 , 2 )
    union(T, 1 , 7 )
    print(T)
    draw_dsf(T)    
    print('Sets encoded by DSF:',dsfToSetList(T))
    
    U = DisjointSetForest(8)
    for i in range(len(U)):
        union(U, i , 0 )
    print(U)
    draw_dsf(U)     
    
    Uc = DisjointSetForest(8)
    for i in range(len(Uc)):
        union_c(Uc, i , 0 )
    print(Uc)
    draw_dsf(Uc)     
    
    Us = DisjointSetForest(8)
    for i in range(len(Us)):
        union_by_size(Us, i , 0 )
    print(Us)
    draw_dsf(Us)     