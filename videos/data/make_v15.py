"""Data for v15 (Catalan's constant).

- partial sums of G = sum (-1)^j/(2j+1)^2 and of Leibniz pi/4
- domino tilings of 2n x 2n boards (Kasteleyn / Temperley-Fisher product), log T/area -> G/pi
"""
import numpy as np
import mpmath as mp

mp.mp.dps = 80
G = +mp.catalan
print("G =", mp.nstr(G, 20), " G/pi =", mp.nstr(G / mp.pi, 12), " 4G =", mp.nstr(4 * G, 12))

J = 40
ps = np.cumsum([(-1) ** j / (2 * j + 1) ** 2 for j in range(J)])


def tilings(m, n):
    """Number of domino tilings of an m x n board (Kasteleyn, Temperley-Fisher)."""
    t = mp.mpf(1)
    for j in range(1, (m + 1) // 2 + 1):
        for k in range(1, (n + 1) // 2 + 1):
            t *= 4 * mp.cos(mp.pi * j / (m + 1)) ** 2 + 4 * mp.cos(mp.pi * k / (n + 1)) ** 2
    return int(mp.nint(t))


rows = []
for n in range(1, 41):
    T = tilings(2 * n, 2 * n)
    rows.append((2 * n, float(mp.log(T) / (4 * n * n)), len(str(T))))
    if n <= 5:
        print(2 * n, T)
rows = np.array(rows)
print(rows[-1], float(G / mp.pi))
assert tilings(8, 8) == 12988816

np.savez("videos/data/v15.npz", ps=ps, G=float(G), dom=rows)
