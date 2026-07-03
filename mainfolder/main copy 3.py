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

from tqdm import tqdm

import time

import numpy as np

import csv

S = 10000000
Prime_min = 3162
Prime_max = 3252
abs_result=[]
Nabs_tmp=[]
Nabs_result=[]
sig=[]
count_True = 0
count_Wi=0
Pmnum=[3192,3204,3209,3218,3222,3230,3252,3254,3258,3260,3272]

roop_count = 10000#繰り返しの回数
for Prime_max in Pmnum:

    #CRT適用
    Wi,sig = S_W_Basic.CRT_split_sieve(S,Prime_min,Prime_max)
    print("sig",sig)
    print("Wi",Wi)

    start_pro=time.time()
    count_True=0
    avg =0
    for k in tqdm(range(roop_count)):
        start = time.time()
        
        for i in Wi:
            #それぞれのWiをRPGに変換
            bit = Wi_bit_code_2.wi_bit_code(i)
            perm = binary_to_perm_3.binary_to_perm(bit)
            inv = inverse_permutation_4.inverse_permutation(perm)
            #print(inv)
            G = Pi_str_to_RPG_5.show_direct_dominance_graph(inv)
            
            #RPGに攻撃
            j=0.65
            G_attacked=edge_deletion_attack_6.edge_deletion_attack(G,j)
            
            #RPG復元
            count,HP_repaired_G = repair_HP_7.repair_HP(G_attacked)
            DAG_tree=RPG_DAGtree_8.RPG_DAG(HP_repaired_G)
            if count>2:
                ##print("削除数が2より大きい")
                #result = repair_kedge.repair_k_edge_deletion(DAG_tree)
                result = upgrade_kedge_repair.repair_k_edge_deletion(DAG_tree)
                if len(result)==1 and i==1757:
                    count_Wi+=1
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
                if i ==1757:
                    count_Wi+=1
                
            
        #print(Wi)
        #print("abs",abs_result)
        #print("Nabs",Nabs_result)
        
        if W_S_Basic_CRT.W_S_Basic(sig,Nabs_result,S):
            #print("true")
            count_True+=1
        
        end = time.time()
        x=end-start
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
    
    
    print("1757",count_Wi/roop_count)
    count_Wi=0
    
    end_pro=time.time()
    
    print("削除率",j)
    print("実行時間の平均",avg)
    print("復元率",count_True/roop_count)
    with open("result_Wi.csv", "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([j,avg,count_True/roop_count])
    
        #それぞれの試行ごとに実行時間を測る
        #