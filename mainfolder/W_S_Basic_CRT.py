def W_S_Basic(primes,lst,S):
    if sum(len(x) == 1 for x in lst) >= 2:        
        Min = primes[0]*primes[1]
        # (index, sublist) を長さでソートして先頭2つ
        pairs = sorted(
            enumerate(lst),
            key=lambda x: len(x[1])
            )[:2]
        
        R = [lst[i][0] for i, _ in pairs]
        P = [primes[i] for i, _ in pairs]
        
        inv = pow(P[0],-1,P[1])
        result = (R[0] + P[0] * ((R[1] - R[0]) * inv % P[1])) % (P[0] * P[1])
        
        if result == S:
            return True
    else:
        return False