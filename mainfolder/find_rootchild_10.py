import networkx as nx

def find_ascending_vertices(F, f):
    n = (F.number_of_nodes()-2)/2
    #print("nは",n)
    #print("fは",f)
    root = 2*n + 2
    Xc = [v for v in F.nodes() if (n+1 <= v <= 2*n+1) and v != f]
    #print("Xcは",Xc)
    
    # Gsub = induced subgraph on Xc plus the root
    nodes_sub = set(Xc) | {root}
    Gsub = F.subgraph(nodes_sub)

    # 連結性（弱連結）を判定
    comps = list(nx.weakly_connected_components(Gsub))
    # components が 1 個なら connected
    #print("compは",comps)
    if len(comps) == 1:
        return set(F.successors(root))   # NF(root)

    # 孤立頂点の列挙（入/出辺ともないノード）
    isolated = [list(c)[0] for c in comps if len(c) == 1 and F.degree(list(c)[0]) == 0]
    #print("isolated:", isolated)

    if len(isolated) == 0:
        return set(F.successors(root)) | {2*n+1}

    if len(isolated) == 2:
        iso_nodes = set(isolated)
        return set(F.successors(root)) | iso_nodes

    # unique isolated
    #print("unique")
    if len(isolated) == 1:
        x=isolated[0]
        #print("xは",x)
        # compute N*_F(f) and its size and rightmost yr per paper defs
        Nstar_f = nx.descendants(F,f)|{f}   # 論文定義に従う補助関数
        #print("Nstar_f",(Nstar_f))
        if  len(Nstar_f)-1 == 2*n - f+1: #check
            F_sub = F.subgraph(Nstar_f)
            preorder_nodes = list(nx.dfs_preorder_nodes(F_sub, source=f))
            #print("preorder",preorder_nodes)
            yr = preorder_nodes[-1]
            
            if len(list(F.successors(root))) < yr: #check
            #if len(set(F.successors(root))) < yr:
                #print("<yr",set(F.successors(root)))
                return set(F.successors(root)) | {x, 2*n+1}
            else:
                #print(">yr",set(F.successors(root)))
                return set(F.successors(root))
        else:
            #print("else")
            return set(F.successors(root)) | {x}