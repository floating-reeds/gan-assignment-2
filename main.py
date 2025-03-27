import networkx as nx
import numpy as np
import matplotlib.path as mpath

'''def graph_input():
    G=nx.Graph()
    n=int(input("Enter no. of nodes:"))
    for i in range(n):
        G.add_node(i+1)
    e=int(input("Enter no. of edges:"))
    print("Enter edges (space separated node pairs eg. 1 2):")
    for i in range(e):
        a,b=map(int,input().split())
        G.add_edge(a,b) 
    return G



g=graph_input()'''
#is_planar = nx.is_planar(G)

#print(G.nodes)
#print(G.edges)

def boundary_input():
    print("Enter boundary vertices (space separated node pairs eg. 1 2), and after the last vertex enter the coords of the first vertex(to close the boundary).")
    boundary=[]
    a,b=map(int,input().split())
    boundary.append((a,b))
    max_x,max_y=a,b
    while True:
        a,b=map(int,input().split())
        boundary.append((a,b))
        if a>max_x:
            max_x=a
        if b>max_y:
            max_y=b
        if a==boundary[0][0] and b==boundary[0][1]:
            break
    bpath=mpath.Path(boundary)
    matrix=np.zeros((max_y,max_x))
    for i in range(0,max_y):
        for j in range(0,max_x):
            if bpath.contains_point((j+0.5,i+0.5)):
                matrix[i][j]=1  
    return matrix

m = boundary_input()

