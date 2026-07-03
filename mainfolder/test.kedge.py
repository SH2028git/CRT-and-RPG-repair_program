import networkx as nx
import Wi_bit_code_2
import binary_to_perm_3
import inverse_permutation_4
import Pi_str_to_RPG_5
import edge_deletion_attack_6
import test_HP_repair
import RPG_DAGtree_8
import copy
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout



i = 1000

bit = Wi_bit_code_2.wi_bit_code(i)
perm = binary_to_perm_3.binary_to_perm(bit)
inv = inverse_permutation_4.inverse_permutation(perm)
print(inv)
G = Pi_str_to_RPG_5.show_direct_dominance_graph(inv)

G_attacked=edge_deletion_attack_6.edge_deletion_attack(G,20)

HP_repaired_G = test_HP_repair.repair_HP(G_attacked)

# 弱連結成分を取得/n+1,2n+1を追加
component = RPG_DAGtree_8.RPG_DAG(HP_repaired_G)
n = int((component.number_of_nodes()-2)/2)
root = int(2*n+2)
if not component.has_edge(root,int(n+1)):component.add_edge(root,int(n+1))
if not component.has_edge(root,int(2*n+1)):component.add_edge(root,int(2*n+1))
weaklyconnected = list(nx.weakly_connected_components(component))

print(n)
print(weaklyconnected)

#弱連結成分それぞれに対してパターンを試す
# 各成分のルートを求める
roots = []
for comp in weaklyconnected:
    subG = component.subgraph(comp)
    # 各成分のrootを取得
    comp_roots = [n for n in subG.nodes if subG.in_degree(n) == 0]
    # まとめて追加
    roots.extend(comp_roots)

roots.sort(reverse=True)
if roots:  # 空リストでエラーを防ぐ
    roots.pop(0)

print("root_per", roots)

def rearrange(arr, n):
    arr = arr[::-1]  # 反転

    if 1 not in arr:
        return arr

    # 1 を削除（一時的に取り出す）
    arr.remove(1)

    # n 以下の最大の数を探す
    max_le_n = max([x for x in arr if x <= n], default=None)

    if max_le_n is None:
        # n 以下がなければ最後に 1 を付ける
        return arr + [1]

    # 挿入位置
    idx = arr.index(max_le_n) + 1

    # 1 を挿入
    arr.insert(idx, 1)

    return arr


"""
n以下の数の並びを反転
small = [x for x in roots if x <= n][::-1]
result = [small.pop(0) if x <= n else x for x in roots]
print("result",result)
roots_per_components = list(reversed(result))
print(roots_per_components)
"""

roots_per_components=rearrange(roots,n)
count = len(roots)-1


def draw_hierarchical_graph(G, root=None, figsize=(6,10)):
    """
    networkx の有向グラフ G を、
    Graphviz の dot レイアウトで階層構造として描画する関数。

    Parameters:
        G      : networkx.DiGraph
        root   : ルートノード（None の場合は入次数0のノードを自動選択）
        figsize: 図の大きさ
    """
    # ルートが指定されない場合、入次数が 0 のノードを探す
    if root is None:
        roots = [v for v in G.nodes if G.in_degree(v) == 0]
        if not roots:
            raise ValueError("root を指定するか、入次数が 0 のノードが必要です")
        root = roots[0]

    # Graphviz の dot レイアウトを利用
    pos = graphviz_layout(G, prog='dot')

    plt.figure(figsize=figsize)
    nx.draw(
        G, pos,
        with_labels=True,
        arrows=True,
        node_size=1200,
        node_color="white",
        edgecolors="black",
        font_size=14
    )
    plt.show()


def bfs_order_true(G, root):
    edges = nx.bfs_edges(G, root, sort_neighbors=lambda x: sorted(x))
    order = [root] + [v for _, v in edges]
    return order

def longest_decreasing_chain(G, start):
    """
    start から始まる連続減少チェーン（v, v-1, v-2, ...）のうち、
    最長のものを返す。枝分かれも完全対応。
    """
    best = []

    def dfs(v, path):
        nonlocal best

        # 現在のパスが最長なら更新
        if len(path) > len(best):
            best = path[:]

        # 次の候補は v - 1 のみ（連続減少条件）
        for u in G.successors(v):
            if u == v - 1:
                dfs(u, path + [u])

    dfs(start, [start])
    
    return best


def check_large(G,n):
    bfs_order = bfs_order_true(G,2*n+2)
    
    # n以上のノードを探索順から抽出
    nodes_ge_n = [v for v in bfs_order if v > n]
    if not nodes_ge_n:
        #print("n以上のノードが存在しません。")
        return False

    # 最後に訪問されたノード
    last_node = nodes_ge_n[-1]
    
    # dfs木における親関係を取得
    predecessors = nx.dfs_predecessors(G,2*n+2)
    parent = predecessors.get(last_node)
    
    if parent is None:
        #print(f"{last_node} はルートなので親がいません。")
        return False
    
    # 出次数を確認
    for node in nodes_ge_n:
        if node == 2*n+2:
            continue  # 2n+2は除外
        if node not in {last_node,parent} and G.out_degree(node)>=2:
            return False
    
    return True
    
def check_RPG(G,n):
    sequence = bfs_order_true(G,2*n+2)
    del sequence[0]
    
    for i in range(2*n):
        if i+1 != sequence[sequence[i]-1]:
            print("False",sequence)
            return False
    print("True SiP",sequence)
    return True
    
def repair_kedge(G,root,n,roots_per_components,count):
    Gcopy = copy.deepcopy(G)
    
    #弱連結成分のrootの中で最も大きいものから再帰的に処理
    #弱連結成分が木なのか葉なのかで処理を変更
    
    if roots_per_components[count]>n:
        #I2に接続(葉、木)
        bfs_nodes = bfs_order_true(G,root)
        nodes_ge_n = [v for v in bfs_nodes if v > n and v!= 2*n+2]
        last_node = nodes_ge_n[-1] if nodes_ge_n else None
        
        if last_node>roots_per_components[count]:
            Gcopy.add_edge(last_node,roots_per_components[count])
            if count ==0: 
                check_RPG(Gcopy,n)
                Gcopy = copy.deepcopy(G)
            else:
                repair_kedge(Gcopy,root,n,roots_per_components,count-1)
                Gcopy = copy.deepcopy(G)
        
        #2n+2に接続(葉)
        if Gcopy.degree(roots_per_components[count])==0:
            Gcopy.add_edge(root,roots_per_components[count])
            if count ==0: 
                check_RPG(Gcopy,n)
                Gcopy = copy.deepcopy(G)
            else:
                repair_kedge(Gcopy,root,n,roots_per_components,count-1)
                Gcopy = copy.deepcopy(G)
    
    #alpha,betaに対して追加するノードの条件が曖昧
    #k+1から同定
    
    #largeに対してA,I2の制約条件から判別
    #smallに対する判別 
    elif check_large(Gcopy,n) == True:
        alpha = (lambda a: a[-1] if a else None)([v for v in bfs_order_true(Gcopy,root) if v > n])
        beta = next(Gcopy.predecessors(alpha), None)

        children_under_beta = sorted([v for v in Gcopy.successors(beta) if v < n])
        bfs_nodes = longest_decreasing_chain(Gcopy,n)
        one_to_k=consecutive_children(Gcopy,n)
        
        #1が孤立頂点なら、βに追加(最優先)
        if roots_per_components[count]==1 and Gcopy.degree(roots_per_components[count])==0:
            Gcopy.add_edge(beta,roots_per_components[count])
            if count ==0: 
                check_RPG(Gcopy,n)
                Gcopy = copy.deepcopy(G)
            else:
                repair_kedge(Gcopy,root,n,roots_per_components,count-1)
                Gcopy = copy.deepcopy(G)
        
        #1~kと一致するならβに追加(葉)(2番目に優先)
        elif min(children_under_beta)<=roots_per_components[count]<=max(children_under_beta) and (roots_per_components[count] not in children_under_beta) and Gcopy.degree(roots_per_components[count])==0:
            Gcopy.add_edge(beta,roots_per_components[count])
            if count ==0: 
                check_RPG(Gcopy,n)
                Gcopy = copy.deepcopy(G)
            else:
                repair_kedge(Gcopy,root,n,roots_per_components,count-1)
                Gcopy = copy.deepcopy(G)
        
       
        else:
            #k+1と一致するなら追加(葉)
            if roots_per_components[count]==max(children_under_beta)+1 and Gcopy.degree(roots_per_components[count])==0:
                Gcopy.add_edge(beta,roots_per_components[count])
                if count ==0: 
                    check_RPG(Gcopy,n)
                    Gcopy = copy.deepcopy(G)
                else:
                    repair_kedge(Gcopy,root,n,roots_per_components,count-1)
                    Gcopy = copy.deepcopy(G)
            
            #γ-1と一致するなら追加(木、葉) 7の処理の後に9->8を処理すると全探索されない
            if roots_per_components[count]==bfs_nodes[-1]-1:
                Gcopy.add_edge(bfs_nodes[-1],roots_per_components[count])
                if count ==0: 
                    check_RPG(Gcopy,n)
                    Gcopy = copy.deepcopy(G)
                else:
                    repair_kedge(Gcopy,root,n,roots_per_components,count-1)
                    Gcopy = copy.deepcopy(G)
        
            #それ以外ならα、n->γに追加(葉) check
            if Gcopy.degree(roots_per_components[count])==0 and roots_per_components[count]!=n:
                for i in [alpha] + bfs_nodes:
                    #print("i,roots",i,roots_per_components[count])
                    if i > roots_per_components[count]:
                        Gcopy.add_edge(i,roots_per_components[count])
                        if count ==0: 
                            check_RPG(Gcopy,n)
                            Gcopy = copy.deepcopy(G)
                        else:
                            repair_kedge(Gcopy,root,n,roots_per_components,count-1)
                            Gcopy = copy.deepcopy(G)
        
            #nをalphaに接続
            if roots_per_components[count] == n:
            
                Gcopy.add_edge(alpha,roots_per_components[count])
                #draw_hierarchical_graph(Gcopy,root)
                if count ==0: 
                    check_RPG(Gcopy,n)
                    Gcopy = copy.deepcopy(G)
                else:
                    repair_kedge(Gcopy,root,n,roots_per_components,count-1)
                    Gcopy = copy.deepcopy(G)

repair_kedge(component,root,n,roots_per_components,count)