import numpy as np
import networkx as nx

def define_f(G):
    #f=2n+1
    maxnodes=G.number_of_nodes()
    n=int((maxnodes-2)/2)
    check=True
    if G.out_degree(2*n+1) == 0:
        for i in range(1,n+1):
            if not (G.has_edge(2*n,i) or (G.degree(i) == 0)):
                check = False
                break
    else:
        check = False

    if check == True:
        #print(2*n+1)
        return 2*n+1
    
    #f<2n+1 
    #(i)
    for i in range (1,G.number_of_nodes()):
        if G.out_degree(i) >= 2 and max(G.successors(i))>n:
            #print("i")
            return max(G.successors(i))

    # (ii) Theorem 26(ii): x が root(2n+2) の子でなく、Y1,Y2 が条件を満たす場合
    components = [set(c) for c in nx.weakly_connected_components(G)]
    root = 2 * n + 2
    
    for x in range(n + 1, 2 * n + 1):  # x ≤ 2n の大頂点
    # rootの子は(ii)の対象外
        if G.has_edge(root, x):
            continue
        
        Y_dash = set(range(x - n, n + 1))  # Y' = {x-n, ..., n}
        Y1 = {k for k in nx.descendants(G,x) if 1 <= k <= n}  # 小頂点の直接子

    # Y1 が空でなく、すべて Y' に含まれる場合
        if Y1 and Y1.issubset(Y_dash):
            Y2 = Y_dash - Y1  # Y2 = Y' - Y1

        # Y2 が F の連結成分の1つと一致するか？
        #if any(Y2 == comp for comp in components) or Y2 ==None:
            #print("ii")
            return x

    """
    components = [set(c) for c in nx.weakly_connected_components(G)]
    #部分偽の頂点集合を返す
    for x in range(n + 1, 2 * n+1) and x!=G.successors(2*n+2):
        Y_dash = list(range(x - n, n+1))
        Y1 = list(G.successors(x))
        if all(x - n < k < n+1 for k in Y1) and len(Y1) != 0:
            Y2 = [k for k in Y_dash if k not in Y1]
            if any(Y2 == comp for comp in components):
                print("ii")
                return x
    """
    #(iii)
    rightmost=[]
    for comp in nx.weakly_connected_components(G):
        subG = G.subgraph(comp).copy()
        # DFS開始ノードはその木の中で最小ラベル（根の仮定）
        root = next(v for v in subG.nodes() if G.in_degree(v) == 0)
        # DFS順序
        dfs_order = list(nx.dfs_preorder_nodes(subG, source=root))
        # 最後に訪問されたノードを記録
        rightmost.append(dfs_order[-1])
    #print("rightmost",rightmost)
    #print("(iii)")
    return max(rightmost)