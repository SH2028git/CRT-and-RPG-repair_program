import random
import networkx as nx

def edge_deletion_attack(G, delete_ratio, random_seed=None):
    """
    エッジ削除攻撃（割合指定版）
    G : 攻撃対象グラフ (nx.DiGraph)
    delete_ratio : 削除割合 (0〜1, 例: 0.2 → 20%削除)
    random_seed : 再現性のための乱数シード
    """
    if random_seed is not None:
        random.seed(random_seed)

    G_attacked = G.copy()
    edges = list(G_attacked.edges())

    # 削除する本数を計算
    num_delete = int(len(edges) * delete_ratio)

    # 削除エッジをランダムに選択
    removed_edges = random.sample(edges, num_delete)

    # エッジ削除
    G_attacked.remove_edges_from(removed_edges)

    return G_attacked
