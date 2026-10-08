"""Data for v19 (Heilbronn): smallest triangles for random points and for Erdos's parabola mod p."""
import numpy as np
from itertools import combinations


def min_tri(P):
    best, arg = 9, None
    for a, b, c in combinations(range(len(P)), 3):
        ar = abs((P[b, 0] - P[a, 0]) * (P[c, 1] - P[a, 1]) - (P[b, 1] - P[a, 1]) * (P[c, 0] - P[a, 0])) / 2
        if ar < best:
            best, arg = ar, (a, b, c)
    return best, np.array(arg)


out = {}
rng = np.random.default_rng(7)
n = 17
R = rng.uniform(0.03, 0.97, (n, 2))
a, t = min_tri(R)
print("random 17 points: min area", a, "n^-2 =", 1 / n ** 2)
out.update(rand=R, rand_tri=t, rand_area=np.array([a]))

# Erdos: points (x, x^2 mod p)/p, x = 0..p-1; no three collinear, all lattice triangles have area >= 1/2
p = 17
E = np.array([(x, (x * x) % p) for x in range(p)], dtype=float)
aE, tE = min_tri(E)
print("parabola mod 17: min lattice area", aE)
assert abs(aE - 0.5) < 1e-9
Es = (E + 0.5) / p  # inside the unit square
aEs, _ = min_tri(Es)
print("scaled min area", aEs, "1/(2p^2) =", 1 / (2 * p * p))
out.update(erd=Es, erd_tri=tE, erd_area=np.array([aEs]), p=np.array([p]))

# random sampling + deletion: delete one point from every triangle of area < A0
rng2 = np.random.default_rng(11)
m = 30
S = rng2.uniform(0.04, 0.96, (m, 2))
A0 = 0.0008
bad = []
for a, b, c in combinations(range(m), 3):
    ar = abs((S[b, 0] - S[a, 0]) * (S[c, 1] - S[a, 1]) - (S[b, 1] - S[a, 1]) * (S[c, 0] - S[a, 0])) / 2
    if ar < A0:
        bad.append((a, b, c))
alive = set(range(m))
dele = []
for t in bad:
    if all(v in alive for v in t):
        v = max(t, key=lambda v: sum(v in u for u in bad))  # remove the point in most small triangles
        alive.discard(v)
        dele.append(v)
keep = np.array(sorted(alive))
a2, _ = min_tri(S[keep])
print("deletion demo:", m, "points,", len(bad), "small triangles, deleted", len(dele), "kept", len(keep),
      "min area after", a2)
assert a2 >= A0
out.update(del_S=S, del_bad=np.array(bad), del_rm=np.array(dele), del_A0=np.array([A0]))

# the explicit exponent of the paper: eta = 2/(45435 k + 16), with d = 41, M = C(4d-1, d), T = C(M, 3), k = T^2 + 1
from math import comb, log10
d = 41
M = comb(4 * d - 1, d)
k = comb(M, 3) ** 2 + 1
print("log10(1/eta) =", log10((45435 * k + 16) / 2))
np.savez("videos/data/v19.npz", **out)
