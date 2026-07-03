from sympy import sieve
import numpy as np

def double_sum_np(m, i_k, r):
    m = np.array(m)
    result = 0
    for p in range(1, i_k):
        result += m[p-1] * np.sum(m[p:r])
    return result

def S_W_Code(S: int, Prime_min: int, Prime_max: int):#整数Sを計算した剰余Wiに変換
    """
    sympy.sieve を使った S_Wi アルゴリズム実装
    （内部処理は NumPy によるベクトル演算）
    """
    # === sympyの篩で素数リストを取得 ===
    Primes = np.array(list(sieve.primerange(Prime_min, Prime_max + 1)), dtype=int)
    n = len(Primes)
    if n < 2:
        return np.array([], dtype=int)

    # === (i,j) の全組み合わせ（i < j）を一括生成 ===
    i_idx, j_idx = np.triu_indices(n, k=1)
    P_i = Primes[i_idx]
    P_j = Primes[j_idx]

    # --- Remainder 計算 ---
    Remainder = S % (P_i * P_j)
    
    #print(P_i*P_j)
    # --- S1 計算 ---
    pair_p, pair_q = np.triu_indices(n, k=1)
    pair_sum = Primes[pair_p] * Primes[pair_q]
    S1_partial = np.zeros(n, dtype=np.int64)
    for k in range(1, n):
        mask = pair_p < k
        S1_partial[k] = np.sum(pair_sum[mask])
    S1 = S1_partial[i_idx]

    # --- S2 計算 ---
    # Σ_{p2=1}^{j-1} (Pi * Pp2)
    cumsum = np.cumsum(Primes)
    S2 = P_i * cumsum[j_idx - 1]

    # --- 合成 ---
    Wi = Remainder
    sig =P_i*P_j
     
    return Wi,sig