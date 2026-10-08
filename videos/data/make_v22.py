"""Data for v22 (Falconer): four-corner Cantor dust (ratio 1/3, dim log4/log3) and its distance set."""
import numpy as np

out = {}
rng = np.random.default_rng(7)


def dust(n, ratio):
    pts = np.zeros((1, 2))
    side = 1.0
    for _ in range(n):
        side *= ratio
        offs = np.array([[0, 0], [1 - ratio, 0], [0, 1 - ratio], [1 - ratio, 1 - ratio]]) * side / ratio
        pts = (pts[:, None, :] + offs[None]).reshape(-1, 2)
    return pts + side / 2, side  # centres of the stage-n squares


P, side = dust(5, 1 / 3)
out["pts"] = P
out["side"] = side
i, j = np.triu_indices(len(P), 1)
D = np.hypot(*(P[i] - P[j]).T)
# distance set at resolution: union of [d - s, d + s] over all pairs, s = side*sqrt2
bins = np.linspace(0, np.sqrt(2), 401)
hist, _ = np.histogram(D, bins=bins)
out["bins"] = bins
out["hist"] = hist
print("fraction of distance bins hit:", (hist > 0).mean())
# random pairs for the animation
k = rng.choice(len(i), 160, replace=False)
out["pairs"] = np.stack([i[k], j[k]], 1)
out["pair_d"] = D[k]
# coverage of the resolution-delta distance set at each stage
cov = []
for n in range(1, 7):
    Q, s = dust(n, 1 / 3)
    a, b = np.triu_indices(len(Q), 1)
    d = np.sort(np.hypot(*(Q[a] - Q[b]).T))
    w = s * np.sqrt(2)
    lo, hi = d - w, d + w
    # merge intervals
    tot, cur_lo, cur_hi = 0.0, lo[0], hi[0]
    for l, h in zip(lo[1:], hi[1:]):
        if l > cur_hi:
            tot += cur_hi - cur_lo
            cur_lo, cur_hi = l, h
        else:
            cur_hi = max(cur_hi, h)
    tot += cur_hi - cur_lo
    cov.append(tot)
    print(n, len(Q), tot)
out["cov"] = np.array(cov)
np.savez("videos/data/v22.npz", **out)
