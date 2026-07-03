from sympy import sieve

def CRT_split_sieve(S: int, PrimeMin: int, PrimeMax: int):
    """
    sympy.sieve を用いて
    整数 S を CRT 用の剰余に分割する
    """

    primes = list(sieve.primerange(PrimeMin, PrimeMax + 1))
    residues = [S % p for p in primes]

    return residues,primes
