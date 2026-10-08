"""Data for v17 (distances): pinned distances in a grid, a lattice unit-distance graph, a product-formula example."""
import numpy as np
from fractions import Fraction
from math import log

out = {}
k = 7
G = np.array([(i, j) for i in range(k) for j in range(k)])
for name, pin in (("center", (3, 3)), ("corner", (0, 0))):
    d2 = sorted({(x - pin[0]) ** 2 + (y - pin[1]) ** 2 for x, y in G if (x, y) != pin})
    out["d2_" + name] = np.array(d2)
    print(name, "pin sees", len(d2), "distinct distances among", len(G) - 1, "other points")

# 8x8 grid, pairs at distance sqrt(5) (knight moves): rescaled, these are unit distances
k = 8
P = [(i, j) for i in range(k) for j in range(k)]
E = [(a, b) for a in range(len(P)) for b in range(a + 1, len(P))
     if (P[a][0] - P[b][0]) ** 2 + (P[a][1] - P[b][1]) ** 2 == 5]
print("8x8 grid: pairs at distance sqrt5 =", len(E), "; n^(4/3) =", round(64 ** (4 / 3)))
out["kn_P"] = np.array(P)
out["kn_E"] = np.array(E)

# product formula for 12/7: |q|_inf * |q|_2 * |q|_3 * |q|_7 = 1
q = Fraction(12, 7)
vals = {"inf": abs(q), "2": Fraction(1, 4), "3": Fraction(1, 3), "7": Fraction(7, 1)}
prod = 1
for v in vals.values():
    prod *= v
assert prod == 1
out["pf"] = np.array([log(float(v)) for v in vals.values()])
print("log|12/7|_v:", out["pf"], "sum", out["pf"].sum())
np.savez("videos/data/v17.npz", **out)
