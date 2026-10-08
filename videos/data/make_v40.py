"""Bloch law curves, the cubic-lattice return probability, zeta(3/2) partial sums, and one sample of
Toth's random-interchange (exchange-loop) picture on a ring of spin-1/2 sites."""
import numpy as np
from scipy.special import ive, zeta

z32 = zeta(1.5)
c_bloch = z32 / (8 * np.pi ** 1.5)  # S - m ~ c_bloch * (T/S)^{3/2}, nearest neighbour, J = 1
print("zeta(3/2) =", z32, " Bloch coefficient =", c_bloch)

# magnetization curves for S = 1/2: leading Bloch law vs ideal magnons with the full lattice dispersion
S = 0.5
T = np.linspace(1e-3, 1.0, 300)
bloch = S - c_bloch * (T / S) ** 1.5


def ideal_density(beta, nmax=4000):
    n = np.arange(1, nmax + 1)
    a = 2 * beta * S
    return np.sum(ive(0, a * n) ** 3)


ideal = np.array([S - ideal_density(1 / t) for t in T])
print("T=0.5: bloch", S - c_bloch * (0.5 / S) ** 1.5, "ideal", S - ideal_density(2.0))

# return probability of the continuous-time walk on Z^3 (rate 1 per neighbour)
ts = np.geomspace(0.05, 200, 200)
pret = ive(0, 2 * ts) ** 3
asym = (4 * np.pi * ts) ** -1.5

# zeta(3/2) partial sums
nn = np.arange(1, 13)
terms = nn ** -1.5

# random interchange on a ring of L sites, one slot per site (S = 1/2), exchange rate 1/2 per bond
rng = np.random.default_rng(2)
L, beta, rate = 12, 3.0, 0.5
marks = []  # (time, left site) for bond (i, i+1 mod L)
for i in range(L):
    k = rng.poisson(rate * beta)
    for t in rng.uniform(0, beta, k):
        marks.append((t, i))
marks.sort()
marks = np.array(marks)


def next_mark(i, t):
    best = None
    for tm, b in marks:
        if tm <= t + 1e-12:
            continue
        if b == i or (b + 1) % L == i:
            return tm, (b + 1) % L if b == i else b
    return None


visited = set()
segs = []  # x0, t0, x1, t1, loop, kind (0 vertical, 1 jump)
loops = 0
wind = []
for i0 in range(L):
    if i0 in visited:
        continue
    i, t, w = i0, 0.0, 0
    while True:
        if t == 0.0:
            visited.add(i)
        nm = next_mark(i, t)
        if nm is None:
            segs.append((i, t, i, beta, loops, 0))
            t = 0.0
            w += 1
            if i == i0:
                break
            continue
        tm, j = nm
        segs.append((i, t, i, tm, loops, 0))
        segs.append((i, tm, j, tm, loops, 1))
        i, t = j, tm
    wind.append(w)
    loops += 1
print("loops", loops, "windings", wind, "marks", len(marks))
np.savez("videos/data/v40.npz", T=T, bloch=bloch, ideal=ideal, ts=ts, pret=pret, asym=asym, terms=terms,
         z32=z32, c_bloch=c_bloch, segs=np.array(segs, float), marks=marks, L=L, beta=beta,
         wind=np.array(wind))
