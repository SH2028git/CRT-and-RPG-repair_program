import numpy as np
import inverse_permutation_4

def binary_to_perm(bits: np.ndarray) -> np.ndarray:#B*->πbの変換
    n = len(bits)
    base = np.arange(1, n+1)

    ones_idx  = np.where(bits == 1)[0]
    zeros_idx = np.where(bits == 0)[0]

    one_vals  = np.sort(base[ones_idx])        # 1 → 昇順
    zero_vals = np.sort(base[zeros_idx])[::-1] # 0 → 降順

    result = np.concatenate([one_vals, zero_vals])
    return result
    