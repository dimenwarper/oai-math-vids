"""Data for v11 (BSD formula).

- multiples nP of P=(0,0) on 37a1: y^2 + y = x^3 - x (exact rationals)
- Birch--Swinnerton-Dyer products prod_{p<=x} N_p/p for 11a1, 37a1, 389a1, 5077a1
"""
from fractions import Fraction as Fr

import numpy as np

# a-invariants [a1, a2, a3, a4, a6]
CURVES = {
    "11a1": [0, -1, 1, -10, -20],   # rank 0
    "37a1": [0, 0, 1, -1, 0],       # rank 1
    "389a1": [0, 1, 1, -2, 0],      # rank 2
    "5077a1": [0, 0, 1, -7, 6],     # rank 3
}


# ---------------------------------------------------------------- group law on 37a1
def add(P, Q, a):
    a1, a2, a3, a4, a6 = a
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and y1 + y2 + a1 * x2 + a3 == 0:
        return None
    if x1 == x2:
        lam = (3 * x1 * x1 + 2 * a2 * x1 + a4 - a1 * y1) / (2 * y1 + a1 * x1 + a3)
    else:
        lam = (y2 - y1) / (x2 - x1)
    nu = y1 - lam * x1
    x3 = lam * lam + a1 * lam - a2 - x1 - x2
    y3 = -(lam + a1) * x3 - nu - a3
    return (x3, y3)


a37 = CURVES["37a1"]
P = (Fr(0), Fr(0))
mult, Q = [], None
for n in range(1, 13):
    Q = add(Q, P, a37)
    mult.append(Q)
    print(n, Q)
mx = np.array([float(q[0]) for q in mult])
my = np.array([float(q[1]) for q in mult])
mstr = [f"{q[0]}|{q[1]}" for q in mult]
digits = np.array([len(str(q[0].denominator)) for q in mult])

# ---------------------------------------------------------------- point counts
PMAX = 200_000
sieve = np.ones(PMAX + 1, bool)
sieve[:2] = False
for i in range(2, int(PMAX**0.5) + 1):
    if sieve[i]:
        sieve[i * i :: i] = False
primes = np.nonzero(sieve)[0]


def counts(a):
    a1, a2, a3, a4, a6 = a
    b2, b4, b6 = a1 * a1 + 4 * a2, 2 * a4 + a1 * a3, a3 * a3 + 4 * a6
    out = []
    for p in primes:
        p = int(p)
        if p == 2:
            n = 1 + sum(1 for x in range(2) for y in range(2)
                        if (y * y + a1 * x * y + a3 * y - x**3 - a2 * x * x - a4 * x - a6) % 2 == 0)
        else:
            chi = -np.ones(p, np.int64)
            chi[(np.arange(p, dtype=np.int64) ** 2) % p] = 1
            chi[0] = 0
            x = np.arange(p, dtype=np.int64)
            f = (((4 * x + b2) % p * x % p + 2 * b4) % p * x % p + b6) % p
            n = p + 1 + int(chi[f].sum())
        out.append(n)
    return np.array(out, dtype=np.float64)


logprod = {}
for name, a in CURVES.items():
    Np = counts(a)
    logprod[name] = np.cumsum(np.log(Np / primes))
    print(name, "N_p first:", Np[:8], " final log prod:", logprod[name][-1])

sel = np.unique(np.geomspace(1, len(primes), 500).astype(int) - 1)
np.savez("videos/data/v11.npz", mx=mx, my=my, mstr=np.array(mstr), digits=digits,
         px=primes[sel].astype(float),
         **{f"lp_{k}": v[sel] for k, v in logprod.items()})
