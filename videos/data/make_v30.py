"""Data for v30 (Subset Sum): meet-in-the-middle instance, two-pointer trace, phase checksum demo."""
import itertools
from pathlib import Path

import numpy as np

A = [28, 9, 33, 43, 59, 6, 15, 7]
T = 103
LEFT, RIGHT = A[:4], A[4:]


def sums(xs):
    out = []
    for r in range(len(xs) + 1):
        for J in itertools.combinations(range(len(xs)), r):
            out.append((sum(xs[i] for i in J), J))
    return sorted(out)


Ls, Rs = sums(LEFT), sums(RIGHT)
Lv = np.array([s for s, _ in Ls])
Rv = np.array([s for s, _ in Rs])
assert len(set(Lv)) == 16 and len(set(Rv)) == 16

# two-pointer trace: left ascending, right descending
trace = []
i, j = 0, 15
while i < 16 and j >= 0:
    s = Lv[i] + Rv[j]
    trace.append((i, j, s))
    if s == T:
        break
    if s < T:
        i += 1
    else:
        j -= 1
trace = np.array(trace)

# all subsets of the 8 numbers
subs = [J for r in range(9) for J in itertools.combinations(range(8), r)]
ssum = np.array([sum(A[i] for i in J) for J in subs])
exact = [k for k, s in enumerate(ssum) if s == T]
assert len(exact) == 1

# phase checksum with a small prime (illustration; the paper uses a huge random prime)
P = 13
rng = np.random.default_rng(5)
phi = rng.integers(0, P, size=8)
mod_hits = [k for k, s in enumerate(ssum) if s % P == T % P]
aliases = [k for k in mod_hits if ssum[k] != T]
ph = np.array([sum(phi[i] for i in subs[k]) % P for k in mod_hits])
is_alias = np.array([ssum[k] != T for k in mod_hits])
vecs = np.exp(2j * np.pi * ph / P)
M = vecs.sum()
Aal = vecs[is_alias].sum()
E = vecs[~is_alias].sum()
print("mod hits", len(mod_hits), "aliases", len(aliases), "M", M, "alias", Aal, "exact", E, abs(E))
hit_sums = np.array([ssum[k] for k in mod_hits])

# deficiency demo: structured half with colliding sums
STRUCT = [5, 10, 15, 20]
Sv = np.array(sorted(s for s, _ in sums(STRUCT)))
print("structured distinct", len(set(Sv)))

np.savez(Path(__file__).with_name("v30.npz"), A=np.array(A), T=T, Lv=Lv, Rv=Rv, trace=trace, P=P, phi=phi,
         ph=ph, is_alias=is_alias, hit_sums=hit_sums, Sv=Sv, STRUCT=np.array(STRUCT))
print(trace)
