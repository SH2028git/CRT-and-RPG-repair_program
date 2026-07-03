import S_W_Code_1
import Wi_bit_code_2
import binary_to_perm_3
import inverse_permutation_4
import Pi_str_to_RPG_5
import edge_deletion_attack_6
import repair_HP_7
import RPG_DAGtree_8
import find_f_9
import find_rootchild_10
import get_Wi_11
import repair_kedge
import upgrade_kedge_repair

import S_W_Basic
import W_S_Basic_CRT

import time


S = 10000000
Prime_min = 3162
Prime_max = 3200
abs_result=[]
Nabs_tmp=[]
Nabs_result=[]
sig=[]
count_True = 0

roop_count = 100#繰り返しの回数

#CRT適用
Wi,sig = S_W_Basic.CRT_split_sieve(S,Prime_min,Prime_max)
print("sig",sig)
print("Wi",Wi)

for k in range(roop_count):
    start = time.time()
    
    for i in Wi:
        #それぞれのWiをRPGに変換
        bit = Wi_bit_code_2.wi_bit_code(i)
        perm = binary_to_perm_3.binary_to_perm(bit)
        inv = inverse_permutation_4.inverse_permutation(perm)
        #print(inv)
        G = Pi_str_to_RPG_5.show_direct_dominance_graph(inv)
        
        #RPGに攻撃
        G_attacked=edge_deletion_attack_6.edge_deletion_attack(G,0.7)
        
        #RPG復元
        count,HP_repaired_G = repair_HP_7.repair_HP(G_attacked)
        DAG_tree=RPG_DAGtree_8.RPG_DAG(HP_repaired_G)
        if count>2:
            ##print("削除数が2より大きい")
            #result = repair_kedge.repair_k_edge_deletion(DAG_tree)
            result = upgrade_kedge_repair.repair_k_edge_deletion(DAG_tree)
            #print("result",result)
            if result ==[]:
                result=upgrade_kedge_repair.repair_k_edge_deletion(DAG_tree)
            for v in result:
                Nabs_tmp.append(get_Wi_11.get_Wi(HP_repaired_G,v))
            Nabs_result.append(Nabs_tmp)
            Nabs_tmp=[]
        else:
            #削除数が2以下
            Nabs_result.append([
                (get_Wi_11.get_Wi(HP_repaired_G,find_rootchild_10.find_ascending_vertices(DAG_tree,find_f_9.define_f(DAG_tree))))])
    #print(Wi)
    #print("abs",abs_result)
    #print("Nabs",Nabs_result)
    
    if W_S_Basic_CRT.W_S_Basic(sig,Nabs_result,S):
        #print("true")
        count_True+=1
    
    end = time.time()
    x=end-start
    avg=0
    avg += (x-avg)/(k+1)
    
    sorted_lists = sorted(Nabs_result, key=len)
    # 最短2つを取り出す
    shortest_two = sorted_lists[:2]
    #print("最も短い",shortest_two)
    #print("sig",sig)
    
    abs_result=[]
    Nabs_result=[]
    
    #absが2以上ならabsのみ利用
    #absが1,Nabsが1以上ならNabsの中でも候補が少ないものを優先
    #absが0,Nabsが2以上なら、Nabsのみ利用(候補が最も少ない2つを利用?)

print("実行時間の平均",avg)
print("復元率",count_True/roop_count)
    
    #それぞれの試行ごとに実行時間を測る
    #