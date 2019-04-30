# Implementation of simple graph operations 
# Programmed by Olac Fuentes
# Last modified April 15, 2019
import random
import dsf
import numpy as np
import matplotlib.pyplot as plt
import math

def adj_list_to_adj_mat(G):
    g = np.zeros((len(G),len(G)),dtype=bool)
    for source in range(len(G)):
        for dest in G[source]:
            g[source,dest] = True
            g[dest,source] = True  #Comment out if graph is directed
    return g

def adj_list_to_edge_list(G):
    g = []
    for source in range(len(G)):
        for dest in G[source]:
            if dest>=source: #ignore duplicate edges
                g.append([source,dest])
    return g

def random_graph(vertices, edges, duplicate=False):
    # Generates random graph with given number of vertices and edges
    # If duplicate is true, each edge is included twice in the list
    # that is, for edge (u,v), u is in G[v] and v is in G[u]
    G = [ [] for i in range(vertices) ]
    n=0
    while n<edges:
        s = random.randint(0, vertices-1)
        d = random.randint(0, vertices-1)
        if s<d and d not in G[s]:
            G[s].append(d)
            if duplicate:
                G[d].append(s)
            n+=1
    return G

def random_graph2(vertices):
    G =[]
    for i in range(vertices):
        G.append([])
    for s in range(vertices):
        d = random.randint(1, vertices-1)
        d = (d+s)%vertices
        G[s].append(d)
    return G

def connected_components(G,diplay_dsf=False):
    S= dsf.DisjointSetForest(len(G))
    for source in range(len(G)):
        for dest in G[source]:
            dsf.union_by_size(S,source,dest)
            if diplay_dsf:
                dsf.draw_dsf(S)
    return dsf.NumSets(S), S
        
def draw_graph(G):
    fig, ax = plt.subplots()
    n = len(G)
    r = 30
    coords =[]
    for i in range(n):
        theta = 2*math.pi*i/n+.001 # Add small constant to avoid drawing horizontal lines, which matplotlib doesn't do very well
        coords.append([-r*np.cos(theta),r*np.sin(theta)])
    for i in range(n):
        for dest in G[i]:
            ax.plot([coords[i][0],coords[dest][0]],[coords[i][1],coords[dest][1]],
                     linewidth=1,color='k')
    for i in range(n):
        ax.text(coords[i][0],coords[i][1],str(i), size=10,ha="center", va="center",
         bbox=dict(facecolor='w',boxstyle="circle"))
    ax.set_aspect(1.0)
    ax.axis('off') 

if __name__ == "__main__":     

    plt.close("all")   
    random.seed(a=86)
    G=random_graph(8,6,True)
    draw_graph(G)
    print('Adjacency list representation:')
    print(G)
    AM = adj_list_to_adj_mat(G)
    print('Adjacency matrix representation:')
    print(AM)
    print('Edge list representation:')
    EL = adj_list_to_edge_list(G)
    print(EL)
    n,S = connected_components(G,True)
    print('Connected components=',n)
    dsf.draw_dsf(S)
    print('Sets:',dsf.dsfToSetList(S))
      
