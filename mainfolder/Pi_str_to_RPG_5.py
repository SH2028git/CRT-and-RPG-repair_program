import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout  # pygraphvizが必要

def nearest_left_greater(arr):
    """スタックで左側の直近の大きい要素を求める"""
    n = len(arr)
    dom_idx = [-1] * n
    stack = []  # (値, インデックス)
    for j in range(n):
        while stack and stack[-1][0] <= arr[j]:
            stack.pop()
        if stack:
            dom_idx[j] = stack[-1][1]
        stack.append((arr[j], j))
    return dom_idx

def show_direct_dominance_graph(perm):
    dom_idx = nearest_left_greater(perm)
    k=len(perm)

    # エッジ作成
    edges = []
    for j, di in enumerate(dom_idx):
        src = k+1 if di == -1 else int(perm[di])
        tgt = int(perm[j])
        edges.append((tgt, src))

    # グラフ構築
    G = nx.DiGraph()
    G.add_nodes_from([int(x) for x in perm])
    G.add_edges_from(edges)
    
    #ハミルトンパス構築
    for i in range(k+1,0,-1):
        G.add_edge(i,i-1)
    """
    # Graphvizレイアウト（階層構造）
    pos = graphviz_layout(G, prog="dot")
    # 描画/*
    plt.figure(figsize=(8, 5))
    nx.draw(G, pos, with_labels=True, node_size=1000, arrows=True, font_size=12)
    plt.title("Direct Dominance Graph (with terminal node t)")
    plt.show()
    

    print("エッジ:", edges)
    """
    return G

# 使用例
"""
perm = np.array([5,6,9,8,1,2,7,4,3])
show_direct_dominance_graph(perm)
"""
