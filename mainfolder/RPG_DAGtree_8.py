import networkx as nx

def RPG_DAG(G):
    for i in range(G.number_of_nodes()-1,0,-1):
        G.remove_edge(i,i-1)
    
    G.remove_node(0)
    G=nx.reverse(G)
    return G