"""Data for v14 (Artin's primitive root conjecture).

- running proportion of primes p <= x for which 10 (resp. 2) is a primitive root
- counts in dyadic intervals (x, 2x)
- Artin's constant
"""
import numpy as np
import mpmath as mp

N = 4_000_000
spf = np.zeros(N + 1, dtype=np.int64)  # smallest prime factor sieve
for i in range(2, N + 1):
    if spf[i] == 0:
        spf[i] = i
        if i * i <= N:
            blk = spf[i * i :: i]
            blk[blk == 0] = i
primes = np.nonzero(spf == np.arange(N + 1))[0]
primes = primes[primes >= 2]


def prime_factors(n):
    out = []
    while n > 1:
        q = int(spf[n])
        out.append(q)
        while n % q == 0:
            n //= q
    return out


def is_prim_root(a, p):
    if a % p == 0:
        return False
    return all(pow(a, (p - 1) // q, p) != 1 for q in prime_factors(p - 1))


res = {}
for a in (10, 2):
    flags = np.array([is_prim_root(a, int(p)) for p in primes])
    res[a] = flags
    print(a, flags.sum(), len(primes), flags.mean())

# Artin's constant: prod over primes (1 - 1/(q(q-1)))
A = mp.mpf(1)
for q in primes[:200000]:
    q = mp.mpf(int(q))
    A *= 1 - 1 / (q * (q - 1))
print("Artin constant approx", A)

# running proportion sampled on a log grid
xs = np.unique(np.geomspace(20, N, 400).astype(np.int64))
idx = np.searchsorted(primes, xs, side="right")
prop10 = np.array([res[10][:k].sum() / max(1, np.sum((primes[:k] != 2) & (primes[:k] != 5))) for k in idx])
prop2 = np.array([res[2][:k].sum() / max(1, np.sum(primes[:k] != 2)) for k in idx])

# dyadic intervals for base 2: (x, 2x), x = 2^k
dy = []
for k in range(4, 21):
    x = 2**k
    m = (primes > x) & (primes < 2 * x)
    dy.append((k, m.sum(), res[2][m].sum()))
dy = np.array(dy)
print(dy)

# powers of 10 mod 7, mod 13, mod 17
cyc = {}
for p in (7, 13, 17):
    seq, r = [], 1
    while True:
        seq.append(r)
        r = r * 10 % p
        if r == 1:
            break
    cyc[p] = seq
    print(p, seq)

full = [int(p) for p, f in zip(primes, res[10]) if f][:15]
print("full reptend", full)
np.savez("videos/data/v14.npz", xs=xs, prop10=prop10, prop2=prop2, dy=dy, A=float(A),
         c7=np.array(cyc[7]), c13=np.array(cyc[13]), c17=np.array(cyc[17]), full=np.array(full))
