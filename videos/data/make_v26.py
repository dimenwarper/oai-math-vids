"""Data for v26 (L = RL = BPL): a small layered configuration graph and its exact acceptance probabilities."""
from fractions import Fraction
from pathlib import Path

import numpy as np

rng = np.random.default_rng(3)
sizes = [1, 2, 3, 3, 3]
best = None
for trial in range(2000):
    succ = []  # succ[layer][node] = (a, b) indices in next layer (coin 0, coin 1)
    for li in range(len(sizes) - 1):
        nxt = sizes[li + 1]
        layer = []
        for v in range(sizes[li]):
            a, b = rng.choice(nxt, size=2, replace=False)
            layer.append((int(a), int(b)))
        succ.append(layer)
    acc = rng.integers(0, 2, size=sizes[-1])
    # every next-layer node must have a predecessor
    ok = all(set(x for pr in succ[li] for x in pr) == set(range(sizes[li + 1])) for li in range(len(succ)))
    if not ok or acc.sum() in (0, sizes[-1]):
        continue
    vals = [None] * len(sizes)
    vals[-1] = [Fraction(int(x)) for x in acc]
    for li in range(len(sizes) - 2, -1, -1):
        vals[li] = [(vals[li + 1][a] + vals[li + 1][b]) / 2 for a, b in succ[li]]
    p0 = vals[0][0]
    if p0 in (Fraction(11, 16), Fraction(5, 8), Fraction(3, 4), Fraction(13, 16)):
        best = (succ, acc, vals)
        break
succ, acc, vals = best
print("p0 =", vals[0][0])
for li, v in enumerate(vals):
    print(li, [str(x) for x in v])
E = [(li, v, int(w)) for li in range(len(succ)) for v in range(sizes[li]) for w in succ[li][v]]
num = [[x.numerator for x in v] + [0] * (3 - len(v)) for v in vals]
den = [[x.denominator for x in v] + [1] * (3 - len(v)) for v in vals]

# schematic estimates over 64 environments: most accurate, a minority arbitrary
p = float(vals[0][0])
good = p + rng.normal(0, 0.025, size=52)
bad = rng.uniform(0, 1, size=12)
est = rng.permutation(np.concatenate([good, bad]))
est = np.clip(est, 0.01, 0.99)
print("median", np.median(est))
np.savez(Path(__file__).with_name("v26.npz"), sizes=np.array(sizes), E=np.array(E), acc=acc, num=np.array(num),
         den=np.array(den), est=est, p0=p, isgood=np.abs(est - p) < 0.1)
