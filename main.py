import networkx as nx
import numpy as np
import matplotlib.path as mpath


def graph_input():
    n=int(input("Enter no. of nodes:"))
    e=int(input("Enter no. of edges:"))
    print("Enter edges (space separated node pairs eg. 1 2)(Start numbering from 0, if nodes are 1 through 10 consider them as 0 through 9):")
    edges=[]
    for i in range(e):
        a,b=map(int,input().split())
        edges.append((a,b))  
        edges.append((b,a))
    return n,edges #getting in adjacencies as a list of tuples

def boundary_input():
    print("Enter boundary vertices (space separated node pairs eg. 1 2), and after the last vertex enter the coords of the first vertex(to close the boundary).")
    boundary=[]
    a,b=map(int,input().split())
    boundary.append((a,b))
    max_x,max_y=a,b #keeps track of the smallest possible rectangle that encloses the path completely
    while True:
        a,b=map(int,input().split())
        boundary.append((a,b))
        if a>max_x:
            max_x=a
        if b>max_y:
            max_y=b
        if a==boundary[0][0] and b==boundary[0][1]:
            break
    bpath=mpath.Path(boundary) #list of 2d vertices form a polygon if closed, can be used to check if things are inside polygon
    matrix=np.zeros((max_y,max_x))
    area=0
    for i in range(0,max_y):
        for j in range(0,max_x):
            if bpath.contains_point((j+0.5,i+0.5)):
                matrix[i][j]=1 #cells inside the boundary are 1, outside are 0
                area+=1
    return matrix, area
#coordinates across this program are of form (y,x) which is very weird but idc fam
def find_rectangles(matrix):
    rows, cols = len(matrix), len(matrix[0]) # rows in the matrix contribute to height, columns in the matrix are width, matrix display is done in reverse order
    rectangles = []
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == 1:
                max_width = cols - c  #max width possible
                for w in range(max_width):
                    if matrix[r][c + w] == 0: 
                        break
                    max_height = rows - r  #max height possible
                    for h in range(max_height):
                        if any(matrix[r + h][c + i] == 0 for i in range(w + 1)):  
                            break  
                        rectangles.append([r,c,h,w,(h+1)*(w+1)]) #positions, dimensions, area
    return rectangles
    
def is_adjacent(rect1, rect2):
    r1,c1,h1,w1=rect1[0],rect1[1],rect1[2],rect1[3]
    r2,c2,h2,w2=rect2[0],rect2[1],rect2[2],rect2[3]
    horiz= (c1 + w1 == c2 or c2 + w2 == c1) and (r1 < r2 + h2 and r2 < r1 + h1)
    vert=(r1 + h1 == r2 or r2 + h2 == r1) and (c1 < c2 + w2 and c2 < c1 + w1)
    return horiz or vert

def flow_graph(bgrid, nodes, placements, adjacency):
    G=nx.DiGraph()
    source, sink = "S", "T"
    G.add_node(source)
    G.add_node(sink)
    grid_nodes={}
    for x in range(len(bgrid)):
        for y in range(len(bgrid[0])):
            if bgrid[x][y]: #adds a node for each grid cell that is inside the boundary
                node_name=f"G_{x}_{y}"
                grid_nodes[(x,y)]=node_name
                G.add_edge(source, node_name, capacity=1, weight=0)
    rectangle_nodes={}
    for i in range(nodes):
        for (r,c,h,w,a) in placements:
            rect_node=f"R_{i}_{r}_{c}_{h}_{w}"
            rectangle_nodes[(i,r,c,h,w)]=rect_node
            G.add_edge(rect_node, sink, capacity=a, weight=0)
            for dy in range(h):
                for dx in range(w):
                    if(x+dx, y+dy) in grid_nodes:
                        G.add_edge(grid_nodes[(x+dx, y+dy)], rect_node, capacity=1, weight=0)
    for (i,j) in adjacency:
        for (r1, c1, h1, w1, a1) in placements:
            for (r2,c2, h2, w2, a2) in placements:
                if is_adjacent((r1,c1,h1,w1), (r2,c2,h2,w2)):
                    node1=f"R_{i}_{r1}_{c1}_{h1}_{w1}"
                    node2=f"R_{j}_{r2}_{c2}_{h2}_{w2}"
                    G.add_edge(node1, node2, capacity=min(a1,a2), weight=-1)
    return G, source, sink, rectangle_nodes

def solve_mcmf(G,source,sink):
    flow_dict=nx.min_cost_flow(G)
    return flow_dict

def lay(flow_dict, rectangle_nodes):
    layout={}
    for (i,r,c,h,w), node in rectangle_nodes.items():
        if sum(flow_dict[node].values()) == w*h:
            layout[i] = (r,c,h,w)
    return layout

nodecount, adjacency = graph_input()
bmatrix, area = boundary_input()
rects=find_rectangles(bmatrix)
G, source, sink, rectangle_nodes=flow_graph(bmatrix, nodecount, rects, adjacency)
flow_dict=solve_mcmf(G,source,sink)
layout=lay(flow_dict, rectangle_nodes)
print(layout)
