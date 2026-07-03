import networkx as nx

#復元プログラム　ハミルトンパスの復元
def repair_HP(G):
    count=0
    max_node=max(G.nodes())
    k = G.number_of_nodes()-1
    for i in range(k,0,-1):
        edge = (i,i-1)
        
        if not edge in G.edges:
            #print("削除されたHP",edge)
            G.add_edge(*edge)
        
        if G.out_degree(i)<2 and i!=k:
            #print("出実数が2未満",i)
            count+=1
            
    return G