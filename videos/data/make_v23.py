"""Data for v23 (triangular lattice): Gaussian energies of density-one configurations, relaxation of repelling points."""
import numpy as np

out = {}
b = np.sqrt(3) / 2
M = 40
jj, kk = np.meshgrid(np.arange(-M, M + 1), np.arange(-M, M + 1))
tri = (np.stack([jj + kk / 2, kk * b], -1) / np.sqrt(b)).reshape(-1, 2)  # covolume one
sq = np.stack([jj, kk], -1).reshape(-1, 2).astype(float)
r2t = (tri ** 2).sum(1); r2t = r2t[r2t > 1e-12]
r2s = (sq ** 2).sum(1); r2s = r2s[r2s > 1e-12]
# honeycomb of density one: triangular lattice of covolume 2 plus a shifted copy
hc_l = tri * np.sqrt(2)
u = np.array([1, 0]) * np.sqrt(2) / np.sqrt(b)
v = np.array([0.5, b]) * np.sqrt(2) / np.sqrt(b)
s0 = (u + v) / 3
r2h_a = ((hc_l) ** 2).sum(1); r2h_a = r2h_a[r2h_a > 1e-12]
r2h_b = ((hc_l + s0) ** 2).sum(1)
alphas = np.linspace(0.3, 3.0, 28)
E = lambda r2, a: np.exp(-np.pi * a * r2).sum()
Et = np.array([E(r2t, a) for a in alphas])
Es = np.array([E(r2s, a) for a in alphas])
Eh = np.array([E(r2h_a, a) + E(r2h_b, a) for a in alphas])  # per particle, both sublattices equivalent
print(np.c_[alphas[::4], Et[::4], Es[::4], Eh[::4]])
out.update(alphas=alphas, Et=Et, Es=Es, Eh=Eh)
# shells in the coordinate s = b|x|^2 = j^2 + j l + l^2
shells = np.unique(np.round(b * r2t, 6))[:12]
print("shells", shells)
out["shells"] = shells

# relaxation of repelling points in a periodic box commensurate with the triangular lattice
m, k = 10, 12  # m points per row, k rows
a0 = 1 / np.sqrt(b)  # spacing for density one
W, H = m * a0, k * a0 * b
n = m * k
rng = np.random.default_rng(2)
X = rng.uniform([0, 0], [W, H], size=(n, 2))
alpha = 1.0


def grad(X, alpha):
    d = X[:, None, :] - X[None, :, :]
    d[..., 0] -= W * np.round(d[..., 0] / W)
    d[..., 1] -= H * np.round(d[..., 1] / H)
    r2 = (d ** 2).sum(-1)
    np.fill_diagonal(r2, np.inf)
    g = np.exp(-np.pi * alpha * r2)
    return (-2 * np.pi * alpha * g[..., None] * d).sum(1), g.sum() / n


nit = 20000
keep = set(np.unique(np.round(np.geomspace(1, nit, 90)).astype(int) - 1))
frames, energies = [X.copy()], [grad(X, alpha)[1]]
for it in range(nit):
    g, e = grad(X, alpha)
    X = X - 0.03 * g
    T = 0.05 * max(0, 1 - it / 15000) ** 2
    X += rng.normal(scale=T, size=X.shape)
    X[:, 0] %= W
    X[:, 1] %= H
    if it in keep:
        frames.append(X.copy())
        energies.append(e)
g, e = grad(X, alpha)
print("final energy per particle", e, "triangular", E(r2t, alpha), "frames", len(frames))
out["energies"] = np.array(energies)
out["E_final"] = e
out["E_tri"] = E(r2t, alpha)
out["frames"] = np.array(frames)
out["box"] = np.array([W, H])
np.savez("videos/data/v23.npz", **out)
