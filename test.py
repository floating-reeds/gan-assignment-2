import networkx as nx
import numpy as np
import matplotlib.path as mpath

def is_adjacent(rect1, rect2):
    r1,c1,h1,w1=rect1[0],rect1[1],rect1[2],rect1[3]
    r2,c2,h2,w2=rect2[0],rect2[1],rect2[2],rect2[3]
    vert = ((r1 + h1 == r2 or r2 + h2 == r1) and max(c1, c2) < min(c1 + w1, c2 + w2))
    horiz = ((c1 + w1 == c2 or c2 + w2 == c1) and max(r1, r2) < min(r1 + h1, r2 + h2))
    return horiz or vert


n=3
e=[(0,1),(0,2),(1,2),(1,0),(2,0),(2,1)]
boundary=np.array([(0,0),(0,2),(3,2),(3,1),(4,1),(4,0),(0,0)])
bpath=mpath.Path(boundary)
x=4
y=2
matrix=np.zeros((y,x))
for i in range(y):
    for j in range(x):
        if bpath.contains_point((j+0.5,i+0.5)):
            matrix[i][j]=1 
#for i in matrix[::-1]:
    #print(i)
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
#print(rectangles)
#print(len(rectangles))
G=nx.DiGraph()
source, sink = "S", "T"
G.add_node(source)
G.add_node(sink)
grid_nodes={}
for x in range(len(matrix)):
    for y in range(len(matrix[0])):
        if matrix[x][y]: #adds a node for each grid cell that is inside the boundary
            node_name=f"G_{x}_{y}"
            grid_nodes[(x,y)]=node_name
            G.add_edge(node_name, source, capacity=1, weight=0)
#print(G.nodes)
#print(G.edges)
#print(len(G.nodes))
#print(len(G.edges))
#print(grid_nodes)
rect_nodes={}
for i in range(n):
    for (r,c,h,w,a) in rectangles:
        rect_node=f"R_{i}_{r}_{c}_{h}_{w}"
        rect_nodes[(i,r,c,h,w)]=rect_node
        G.add_edge(source, rect_node, capacity=a, weight=0)
        for dh in range(h+1):
            for dw in range(w+1):
                #print(h+dh, w+dw)
                if(h+dh, w+dw) in grid_nodes:
                    G.add_edge(rect_node, grid_nodes[(h+dh, w+dw)], capacity=1, weight=0)
#print(G.nodes)
#print(G.edges)
#print(len(G.nodes))
#print(len(G.edges))  
for (i,j) in e:
    for (r1, c1, h1, w1, a1) in rectangles:
        for (r2, c2, h2, w2, a2) in rectangles:
            if is_adjacent((r1,c1,h1+1,w1+1), (r2,c2,h2+1,w2+1)):
                node1=f"R_{i}_{r1}_{c1}_{h1}_{w1}"
                node2=f"R_{j}_{r2}_{c2}_{h2}_{w2}"
                G.add_edge(node1, node2, capacity=min(a1,a2), weight=-1)
                G.add_edge(node2, node1, capacity=min(a1,a2), weight=-1)
                #print("x1:",c1, "y1:",r1,"x2:",c2,"y2:",r2, "w1:",w1+1,"h1:",h1+1,"w2:",w2+1,"h2:",h2+1)
#print(G.nodes)
#print(G.edges)
#print(len(G.nodes))
#print(len(G.edges)) 
flow_dict=nx.max_flow_min_cost(G, source, sink)
'''H = nx.DiGraph()
H.add_node(source)
H.add_node(sink)
H.add_edge(source, "G_0_0", capacity=1, weight=0)
H.add_edge("G_0_0", sink, capacity=1, weight=0)
H.add_edge(source, "G_0_1", capacity=1, weight=0)
H.add_edge("G_0_1", sink, capacity=1, weight=0)
flow_dict=nx.min_cost_flow(H)'''
#layout={}
#for bleh in flow_dict:
    #for node in flow_dict[bleh]:
        #if flow_dict[bleh][node] > 0:
            #print(bleh, node, flow_dict[bleh][node])

#print(G['R_1_1_0_0_2']['T']['capacity'])
for (i,r,c,h,w), node in rect_nodes.items():
    flow_to_sink=flow_dict[node][sink]
    print(f"Flow from {node} to sink: {flow_to_sink} / {G[node][sink]['capacity']}")

#print(flow_dict)
#print(nx.cost_of_flow(G, flow_dict))