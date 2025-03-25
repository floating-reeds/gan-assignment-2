import networkx as nx

def graph_input():
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

G=graph_input()
is_planar = nx.is_planar(G)
print(is_planar)
#print(G.nodes)
#print(G.edges)
