"""Data for v24 (hot spots): Neumann eigenfunctions and heat flow on a smooth non-convex simply connected domain.

Finite differences: the 5-point graph Laplacian on grid cells inside the domain (no-flux across the boundary)
approximates the Neumann Laplacian."""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as sla

out = {}
th = np.linspace(0, 2 * np.pi, 721)


def rad(t):
    return 1.0 + 0.28 * np.cos(2 * t - 0.3) + 0.16 * np.sin(3 * t + 0.4) + 0.06 * np.cos(5 * t + 1.0)


bx, by = rad(th) * np.cos(th) * 1.35, rad(th) * np.sin(th)
out["boundary"] = np.stack([bx, by], 1)
n = 220
xs = np.linspace(-2.0, 2.0, n)
ys = np.linspace(-1.55, 1.55, int(n * 3.1 / 4.0))
h = xs[1] - xs[0]
Xg, Yg = np.meshgrid(xs, ys)
T = np.arctan2(Yg, Xg / 1.35)
R = np.hypot(Xg / 1.35, Yg)
mask = R < rad(T)
idx = -np.ones(mask.shape, int)
idx[mask] = np.arange(mask.sum())
N = mask.sum()
rows, cols = [], []
for di, dj in ((0, 1), (1, 0)):
    a = mask[: mask.shape[0] - di, : mask.shape[1] - dj] & mask[di:, dj:]
    i1 = idx[: mask.shape[0] - di, : mask.shape[1] - dj][a]
    i2 = idx[di:, dj:][a]
    rows += [i1, i2]
    cols += [i2, i1]
rows, cols = np.concatenate(rows), np.concatenate(cols)
A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(N, N))
L = (sp.diags(np.asarray(A.sum(1)).ravel()) - A) / h ** 2
K = 60
vals, vecs = sla.eigsh(L.tocsc(), k=K, sigma=-1e-3, which="LM")
o = np.argsort(vals)
vals, vecs = vals[o], vecs[:, o]
print("cells", N, "first eigenvalues", vals[:6].round(4))


def field(v):
    F = np.full(mask.shape, np.nan)
    F[mask] = v
    return F


phi = vecs[:, 1] * np.sign(vecs[:, 1][np.argmax(np.abs(vecs[:, 1]))])
F1 = field(phi)
imax, imin = np.nanargmax(F1), np.nanargmin(F1)
print("phi1 max at", Xg.flat[imax], Yg.flat[imax], " min at", Xg.flat[imin], Yg.flat[imin])
# distance of extrema from boundary (in cells): count neighbours outside mask
def bdist(i):
    r, c = np.unravel_index(i, mask.shape)
    for d in range(0, 50):
        if not mask[max(r - d, 0):r + d + 1, max(c - d, 0):c + d + 1].all():
            return d
print("extrema distance to boundary (cells):", bdist(imax), bdist(imin))
out["phi1"] = F1.astype(np.float32)
out["mu"] = vals[:6]
# gradient of phi1 on a coarse subgrid
gy, gx = np.gradient(np.nan_to_num(F1), h)
step = 11
sub = np.zeros(mask.shape, bool)
sub[step // 2::step, step // 2::step] = True
ok = sub & mask
# require all neighbours inside to avoid one-sided gradients at the boundary
inner = mask.copy()
inner[1:-1, 1:-1] = mask[1:-1, 1:-1] & mask[:-2, 1:-1] & mask[2:, 1:-1] & mask[1:-1, :-2] & mask[1:-1, 2:]
ok &= inner
out["arrows"] = np.stack([Xg[ok], Yg[ok], gx[ok], gy[ok]], 1)
gm = np.hypot(gx, gy)
gm[~inner] = np.nan
print("min |grad phi1| over interior cells:", np.nanmin(gm), " median", np.nanmedian(gm))
# heat flow from a lumpy initial temperature
rng = np.random.default_rng(5)
u0 = np.exp(-((Xg + 0.15) ** 2 + (Yg - 0.1) ** 2) / 0.08) * 1.0
for _ in range(7):
    cx, cy = rng.uniform(-1.4, 1.4), rng.uniform(-0.9, 0.9)
    u0 += rng.uniform(-0.5, 0.6) * np.exp(-((Xg - cx) ** 2 + (Yg - cy) ** 2) / 0.12)
c = vecs.T @ u0[mask]
times = np.concatenate([[0], np.geomspace(2e-3, 6.0 / vals[1], 89)])
frames, hot, cold = [], [], []
for t in times:
    v = vecs @ (c * np.exp(-vals * t))
    F = field(v)
    frames.append(F.astype(np.float32))
    i, j = np.nanargmax(F), np.nanargmin(F)
    hot.append([Xg.flat[i], Yg.flat[i]])
    cold.append([Xg.flat[j], Yg.flat[j]])
out.update(frames=np.array(frames), times=times, hot=np.array(hot), cold=np.array(cold),
           extent=np.array([xs[0], xs[-1], ys[0], ys[-1]]), mask=mask)
print("hot spot path end", hot[-1], "cold end", cold[-1])
np.savez_compressed("videos/data/v24.npz", **out)
