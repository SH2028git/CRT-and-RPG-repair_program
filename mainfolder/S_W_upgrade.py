import numpy as np
from sympy import sieve

def compute_xk(W, m_i, m_j):
    modulus = m_i * m_j           # m_i m_j の積
    x_k = W % modulus             # 余りを求める
    return x_k

def double_sum(m, i_k, r):
    total = 0
    for p in range(1, i_k):  # p = 1 ... i_k-1
        for q in range(p + 1, r):  # q = p+1 ... r
            total += m[p] * m[q]  # Pythonは0-indexなので調整
    return total

def sum_formula(m, i_k, j_k):
    total = 0
    for p in range(1, j_k+1):  # p = 1 ... j_k-1
        total += m[i_k] * m[p]  # インデックス調整
    return total

def S_W_main(S: int, Prime_min: int, Prime_max: int):
    #Primes = list(sieve.primerange(Prime_min, Prime_max + 1))
    Primes =[13,17,31]
    r = len(Primes)
    
    #i,jのペアを作成
    i_idx, j_idx = np.triu_indices(r, k=1)
    
    i_idx = i_idx.tolist()
    j_idx = j_idx.tolist()
    
    result = []
    #S1計算
    for t in range(len(i_idx)):
        Wk=compute_xk(S,Primes[i_idx[t]],Primes[j_idx[t]])+double_sum(Primes,i_idx[t],r)+sum_formula(Primes,i_idx[t],j_idx[t])
        result.append(Wk)
    
    print("result",result)
    return result

S_W_main(6000,10,25)
    
    