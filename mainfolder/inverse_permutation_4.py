import numpy as np

def inverse_permutation(p:np.ndarray):
    n = int(len(p)/2)
    inv = np.zeros(len(p),dtype=int)
    for i in range(0,len(p)):
        if i<n:
            inv[i] = p[i]
        elif np.any(inv == i+1):
            inv[i] = np.where(inv == i+1)[0][0] + 1
        else:
            inv[i] = i+1
    return inv