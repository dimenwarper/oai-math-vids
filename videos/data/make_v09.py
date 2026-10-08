import numpy as np, mpmath as mp
mp.mp.dps = 200
pi = +mp.pi
# continued fraction convergents
a, x = [], pi
for _ in range(60):
    ai = int(mp.floor(x)); a.append(ai); x = 1 / (x - ai)
p0, q0, p1, q1 = 1, 0, a[0], 1
conv = [(p1, q1)]
for ai in a[1:]:
    p0, q0, p1, q1 = p1, q1, ai * p1 + p0, ai * q1 + q0
    conv.append((p1, q1))
rows = []
for p, q in conv[1:]:
    err = abs(pi - mp.mpf(p) / q)
    rows.append((float(mp.log10(q)), float(-mp.log(err) / mp.log(q))))
rows = np.array(rows)
n = np.arange(1, 200001, dtype=np.float64)
terms = 1 / (n**3 * np.sin(n) ** 2)
S = np.cumsum(terms)
idx = np.unique(np.concatenate([np.geomspace(1, 200000, 1500).astype(int) - 1, np.array([0, 1, 2, 21, 332, 354, 355])]))
np.savez("videos/data/v09.npz", cf=rows, a=np.array(a[:12]), Sx=n[idx], Sy=S[idx])
print(a[:12]); print(rows[:12]); print(S[[0, 2, 21, 353, 354, 199999]])
