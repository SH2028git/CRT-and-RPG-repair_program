import copy
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
from itertools import accumulate


def repair_k_edge_deletion(G):
    #G:HPを復元した後のグラフ
    component = G
    n = int((component.number_of_nodes()-2)/2)
    root = int(2*n+2)
    if not component.has_edge(root,int(n+1)):component.add_edge(root,int(n+1))
    if not component.has_edge(root,int(2*n+1)):component.add_edge(root,int(2*n+1))
    weaklyconnected = list(nx.weakly_connected_components(component))

    #print(n)
    #print(weaklyconnected)

    #弱連結成分それぞれに対してパターンを試す
    # 各成分のルートを求める
    roots = []
    for comp in weaklyconnected:
        subG = component.subgraph(comp)
        # 各成分のrootを取得
        comp_roots = [node for node in subG.nodes if subG.in_degree(node) == 0 and node>n]
        # まとめて追加
        roots.extend(comp_roots)

    roots.sort(reverse=True)
    if roots:  # 空リストでエラーを防ぐ
        roots.pop(0)
    roots = roots[::-1]
    #print("root_per", roots)

    roots_per_components=roots
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
        #draw_hierarchical_graph(G,2*n+2)
        bfs_order = bfs_order_true(G,2*n+2)
        
        # n以上のノードを探索順から抽出
        nodes_ge_n = [v for v in bfs_order if v > n]
        if not nodes_ge_n:
            ##print("n以上のノードが存在しません。")
            return False

        # 最後に訪問されたノード
        last_node = nodes_ge_n[-1]
        
        # dfs木における親関係を取得
        predecessors = nx.dfs_predecessors(G,2*n+2)
        parent = predecessors.get(last_node)
        
        if parent is None:
            ##print(f"{last_node} はルートなので親がいません。")
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
                ##print("False",sequence)
                return False
        #print("True SiP",sequence)
        draw_hierarchical_graph(G,2*n+2)
        return set(G.successors(2*n+2))

    def consecutive_children(G, n):
        #Aのn+1~n+kまでの処理
        children = sorted(G.successors(2*n+2))

        expected = n + 1
        result = []

        for x in children:
            if x == expected:
                result.append(x)
                expected += 1
            else:
                break
        
        result_k = [x - n for x in result]
        return result_k
    
    def repair_under_n(Gcopy,alpha,beta,root):
        A_children=list(Gcopy.successors(root))
        A_children.sort()
        A_children.pop()
        
        #Aにおける(右隣の数との差-1)の累積和を調べる
        diff=[A_children[i+1] - A_children[i] - 1 for i in range(len(A_children)-1)]
        diff=[0]+diff
        
        Cumulativesum=list(accumulate(diff))
        
        #1,Aの2n+1以外のインデックスを調べて、それぞれまとめる->必ず葉になる
        num_neighbors = len(list(Gcopy.neighbors(root)))
        bfs_order = list(range(1,num_neighbors))
        
        for i in bfs_order:
            if Gcopy.out_degree(i)>=1:
                return False
        
        #2,求めたインデックス以外でn~2n+1のインデックスまでをつなげられるか検証
        under_n=list(range(n,0,-1))
        
        remove_set = set(bfs_order)
        chain = [x for x in under_n if x not in remove_set]
        chain.insert(0,alpha)
        chain.insert(0,beta)
        
        #beta,alpha,chainを接続
        for i in range(len(chain)-1):
            if not Gcopy.has_edge(chain[i],chain[i+1]):
                Gcopy.add_edge(chain[i],chain[i+1])
        
        #それぞれのbfs_orderを接続
        for i,v in enumerate(Cumulativesum,start=1):
            if not Gcopy.has_edge(chain[v],i):
                Gcopy.add_edge(chain[v],i)
        
        #draw_hierarchical_graph(Gcopy,root)
        #それぞれのノードに対して入次数が1になっている確認
        for i in [alpha,beta]+list(range(n,0,-1)):
            if Gcopy.in_degree(i)>1:
                return False
        
        return set(Gcopy.successors(root))
    

    def repair_kedge(G,root,n,roots_per_components,count,result):
        Gcopy=G.copy()
        #弱連結成分のrootの中で最も大きいものから再帰的に処理
        #弱連結成分が木なのか葉なのかで処理を変更
        if roots_per_components!=[]:
            #2n+2に接続(葉)
            if Gcopy.degree(roots_per_components[count])==0:
                Gcopy.add_edge(root,roots_per_components[count])
                if count!=0:
                    repair_kedge(Gcopy,root,n,roots_per_components,count-1,result)
                    Gcopy=G.copy()
                
                elif check_large(Gcopy,n) == True:
                
                    alpha = (lambda a: a[-1] if a else None)([v for v in bfs_order_true(Gcopy,root) if v > n])
                    beta = next(Gcopy.predecessors(alpha), None)
                    
                    check = repair_under_n(Gcopy,alpha,beta,root)
                        #bfsの結果をresultに追加
                    if check:
                        result.append(check)
                        
                    Gcopy=G.copy()
            
            #I2に接続(葉、木)
            bfs_nodes = bfs_order_true(G,root)
            nodes_ge_n = [v for v in bfs_nodes if v > n and v!= 2*n+2]
            last_node = nodes_ge_n[-1] if nodes_ge_n else None
            
            if last_node>roots_per_components[count]:
                Gcopy.add_edge(last_node,roots_per_components[count])
                if count!=0:
                    repair_kedge(Gcopy,root,n,roots_per_components,count-1,result)
                    Gcopy=G.copy()
                
                elif check_large(Gcopy,n) == True:
    
                    alpha = (lambda a: a[-1] if a else None)([v for v in bfs_order_true(Gcopy,root) if v > n])
                    beta = next(Gcopy.predecessors(alpha), None)
                    
                    check = repair_under_n(Gcopy,alpha,beta,root)
                        #bfsの結果をresultに追加
                    if check:
                        result.append(check)
                        
                    Gcopy=G.copy()    
        else:
            alpha = (lambda a: a[-1] if a else None)([v for v in bfs_order_true(Gcopy,root) if v > n])
            beta = next(Gcopy.predecessors(alpha), None)
            
            check = repair_under_n(Gcopy,alpha,beta,root)
                #bfsの結果をresultに追加
            if check:
                result.append(check)
    
        return result
    
    count_repair=0
    
    def repair_kedge_second(G,root,n,roots_per_components,count):
        nonlocal count_repair
        nonlocal result
        #if len(result)==1:
         #   print("result_1",result)
        count_repair+=1
        Gcopy=G.copy()
        if count_repair>100000:
            count_repair=count_repair-100000
            draw_hierarchical_graph(Gcopy,root)
        #弱連結成分のrootの中で最も大きいものから再帰的に処理
        #弱連結成分が木なのか葉なのかで処理を変更
        if roots_per_components!=[]and len(result)<2:
            #2n+2に接続(葉)
            if Gcopy.degree(roots_per_components[count])==0 and len(result)<2:
                Gcopy.add_edge(root,roots_per_components[count])
                if count!=0 and len(result)<2:
                    repair_kedge_second(Gcopy,root,n,roots_per_components,count-1)
                    Gcopy=G.copy()
                
                elif check_large(Gcopy,n) == True and len(result)<2:
                
                    alpha = (lambda a: a[-1] if a else None)([v for v in bfs_order_true(Gcopy,root) if v > n])
                    beta = next(Gcopy.predecessors(alpha), None)
                    
                    check = repair_under_n(Gcopy,alpha,beta,root)
                        #bfsの結果をresultに追加
                    if check:
                        #print("edge:",Gcopy.edges())
                        result.append(check)
                        
                    Gcopy=G.copy()
            
            #I2に接続(葉、木)
            bfs_nodes = bfs_order_true(G,root)
            nodes_ge_n = [v for v in bfs_nodes if v > n and v!= 2*n+2]
            last_node = nodes_ge_n[-1] if nodes_ge_n else None
            
            if last_node>roots_per_components[count]:
                Gcopy.add_edge(last_node,roots_per_components[count])
                if count!=0 and len(result)<2:
                    repair_kedge_second(Gcopy,root,n,roots_per_components,count-1)
                    Gcopy=G.copy()
                
                elif check_large(Gcopy,n) == True and len(result)<2:
    
                    alpha = (lambda a: a[-1] if a else None)([v for v in bfs_order_true(Gcopy,root) if v > n])
                    beta = next(Gcopy.predecessors(alpha), None)
                    
                    check = repair_under_n(Gcopy,alpha,beta,root)
                        #bfsの結果をresultに追加
                    if check:
                        result.append(check)
                        
                    Gcopy=G.copy()    
        elif len(result)<2:
            alpha = (lambda a: a[-1] if a else None)([v for v in bfs_order_true(Gcopy,root) if v > n])
            beta = next(Gcopy.predecessors(alpha), None)
            
            check = repair_under_n(Gcopy,alpha,beta,root)
                #bfsの結果をresultに追加
            if check:
                result.append(check)
                
        return result
    
    def dfs_last_node_ge_n_with_parent(edges, start, n):
        visited = []
        stack = [(start, None)]   # (現在ノード, 親ノード)
        last_ge_n = None
        parent_of_last = None

        while stack:
            u, parent = stack.pop()
            if u in visited:
                continue

            visited.append(u)

            if u >= n:
                last_ge_n = u
                parent_of_last = parent

            # 隣接ノード取得（listのみ）
            neighbors = []
            for a, b in edges:
                if a == u:
                    neighbors.append(b)
                elif b == u:          # 無向グラフ
                    neighbors.append(a)

            # DFS順を保つため逆順で積む
            for v in reversed(neighbors):
                if v not in visited:
                    stack.append((v, u))

        return last_ge_n, parent_of_last

    
        
    def repair_kedge_third(edges,n,roots_per_components,count):
        nonlocal result
        
        edge_copy=edges
        #弱連結成分のrootの中で最も大きいものから再帰的に処理
        #弱連結成分が木なのか葉なのかで処理を変更
        if roots_per_components!=[]:
            #2n+2に接続(葉)
            if sum(1 for u, v in edges if u == roots_per_components[count])==0:
                edge_copy.append((2*n+2,roots_per_components[count]))
                if count!=0 and len(result)<2:
                    repair_kedge_third(edge_copy,n,roots_per_components,count-1)
                    edge_copy=edges
                
                elif count==0:
                    
                    alpha,beta=dfs_last_node_ge_n_with_parent(edge_copy,2*n+2,n)
                    
                    check = repair_under_n(Gcopy,alpha,beta,root)
                        #bfsの結果をresultに追加
                    if check:
                        result.append(check)
                        
                    Gcopy=G.copy()
            
            #I2に接続(葉、木)
            bfs_nodes = bfs_order_true(G,root)
            nodes_ge_n = [v for v in bfs_nodes if v > n and v!= 2*n+2]
            last_node = nodes_ge_n[-1] if nodes_ge_n else None
            
            if last_node>roots_per_components[count]:
                Gcopy.add_edge(last_node,roots_per_components[count])
                if count!=0 and len(result)<2:
                    repair_kedge_second(Gcopy,root,n,roots_per_components,count-1)
                    Gcopy=G.copy()
                
                elif check_large(Gcopy,n) == True:
    
                    alpha = (lambda a: a[-1] if a else None)([v for v in bfs_order_true(Gcopy,root) if v > n])
                    beta = next(Gcopy.predecessors(alpha), None)
                    
                    check = repair_under_n(Gcopy,alpha,beta,root)
                        #bfsの結果をresultに追加
                    if check:
                        result.append(check)
                        
                    Gcopy=G.copy()    
        
        elif len(result)<2:
            alpha = (lambda a: a[-1] if a else None)([v for v in bfs_order_true(Gcopy,root) if v > n])
            beta = next(Gcopy.predecessors(alpha), None)
            
            check = repair_under_n(Gcopy,alpha,beta,root)
                #bfsの結果をresultに追加
            if check:
                result.append(check)
        return result
    
    result =[]
    edges=list(G.edges())
    nodes = list(G.nodes())
    
    albe=[]
    
    for u in roots_per_components:
        outdeg=0
        for a,b in edges:
            if a==u:
                outdeg +=1
        if outdeg >=2 and u!=2*n+2:
            albe.append(u)
    
    #return repair_kedge(component,root,n,roots_per_components,count,result)
    
    
    
    return repair_kedge_second(G,root,n,roots_per_components,count)
    #return repair_kedge_third(component,root,n,roots_per_components,count)