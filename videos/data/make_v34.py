"""Standard sine map f_k(x,y) = (x + y + k sin 2 pi x, y + k sin 2 pi x) mod 1 (the paper's normalization).
Phase portraits, a stretched blob, growth of transfer-matrix norms, and the shortfall e_n.
Output: videos/data/v34.npz"""
import numpy as np

TWO_PI = 2 * np.pi


def step(x, y, k):
    s = k * np.sin(TWO_PI * x)
    y2 = y + s
    return np.mod(x + y2, 1.0), np.mod(y2, 1.0)


def portrait(k, n_orb, n_it, rng):
    x = rng.uniform(0, 1, n_orb)
    y = rng.uniform(0, 1, n_orb)
    out = np.zeros((n_orb, n_it, 2), np.float32)
    for i in range(n_it):
        out[:, i, 0], out[:, i, 1] = x, y
        x, y = step(x, y, k)
    return out


rng = np.random.default_rng(7)
KS = [0.05, 0.14, 0.4, 1.5]
ports = np.stack([portrait(k, 70, 1200, rng) for k in KS])  # (4, 70, 1200, 2)

# a blob, stretched and folded (k = 1)
kb = 1.0
r = 0.03 * np.sqrt(rng.uniform(0, 1, 3000))
a = rng.uniform(0, 2 * np.pi, 3000)
bx, by = 0.12 + r * np.cos(a), 0.35 + r * np.sin(a)
blob = []
for i in range(5):
    blob.append(np.c_[bx, by])
    bx, by = step(bx, by, kb)
blob = np.array(blob, np.float32)


# transfer matrices in the paper's coordinates: q_{i+1} = phi(q_i) - q_{i-1}, A_i = [[v(q_i), -1], [1, 0]]
def growth_curves(k, n, samples, rng):
    """g(0, m) = log_M ||T_{0,m}|| for m = 1..n, with periodic renormalization."""
    K = TWO_PI * k
    M = K + 4
    x = rng.uniform(0, 1, samples)
    y = rng.uniform(0, 1, samples)
    T = np.tile(np.eye(2), (samples, 1, 1))
    logscale = np.zeros(samples)
    g = np.zeros((samples, n))
    for i in range(n):
        v = 2 + K * np.cos(TWO_PI * x)
        A = np.zeros((samples, 2, 2))
        A[:, 0, 0], A[:, 0, 1], A[:, 1, 0] = v, -1, 1
        T = A @ T
        nrm = np.linalg.norm(T, ord=2, axis=(1, 2))
        g[:, i] = (logscale + np.log(nrm)) / np.log(M)
        T = T / nrm[:, None, None]
        logscale += np.log(nrm)
        x, y = step(x, y, k)
    return g


NG = 48
curves = growth_curves(2.0, NG, 6, np.random.default_rng(3))
short = {}
for k in (0.5, 2.0, 8.0):
    g = growth_curves(k, 64, 20000, np.random.default_rng(11))
    n = np.arange(1, 65)
    short[k] = 1 - g.mean(axis=0) / n
    print(k, "e_1, e_8, e_64:", short[k][0], short[k][7], short[k][63])

np.savez_compressed("videos/data/v34.npz", ks=np.array(KS), ports=ports, blob=blob, curves=curves,
                    e05=short[0.5], e2=short[2.0], e8=short[8.0])
print("curves final", curves[:, -1], "slope approx", curves[:, -1] / NG)
