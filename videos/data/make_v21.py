"""Data for v21 (Kakeya): deltoid needle positions, a Kakeya-type needle family and its union areas."""
import numpy as np
from scipy.optimize import brentq

out = {}
# --- deltoid z(t) = r(2e^{it} + e^{-2it}) with r = 1/4: every tangent chord inside has length 4r = 1
r = 0.25
z = lambda t: r * (2 * np.exp(1j * t) + np.exp(-2j * t))
dz = lambda t: r * (2j * np.exp(1j * t) - 2j * np.exp(-2j * t))
ts = np.linspace(0, 2 * np.pi, 1201)
out["deltoid"] = np.stack([z(ts).real, z(ts).imag], 1)
# needle for tangent parameter t: intersect tangent line with the curve
needles = []
tt = np.linspace(0.02, 2 * np.pi / 3 * 3 - 0.02, 721)  # avoid cusps where the tangent degenerates
for t in np.linspace(0, 2 * np.pi, 721):
    p, d = z(t), np.exp(-0.5j * t)  # tangent direction at z(t) is +-e^{-it/2}; rotates continuously
    f = lambda s: ((z(s) - p) * np.conj(d)).imag
    ss = np.linspace(0, 2 * np.pi, 4001)
    v = f(ss)
    roots = []
    for a, b, va, vb in zip(ss[:-1], ss[1:], v[:-1], v[1:]):
        if va * vb < 0:
            try:
                roots.append(brentq(f, a, b))
            except ValueError:
                pass
    pts = [z(s) for s in roots] + [p]
    proj = [((q - p) * np.conj(d)).real for q in pts]
    i, j = int(np.argmin(proj)), int(np.argmax(proj))
    needles.append([pts[i].real, pts[i].imag, pts[j].real, pts[j].imag])
needles = np.array(needles)
L = np.hypot(needles[:, 2] - needles[:, 0], needles[:, 3] - needles[:, 1])
print("needle length range", L.min(), L.max())
out["needles"] = needles
out["deltoid_area"] = np.pi * 2 * r * r  # area of deltoid = 2 pi r^2


# --- Kakeya-type family: slope a = sum eps_k 2^-k, intercept b = -sum (k/n) eps_k 2^-k
def family(n):
    N = 2 ** n
    j = np.arange(N)
    eps = np.array([(j >> (n - k)) & 1 for k in range(1, n + 1)])
    w = 2.0 ** -np.arange(1, n + 1)
    a = (eps * w[:, None]).sum(0)
    b = -(eps * w[:, None] * (np.arange(1, n + 1)[:, None] / n)).sum(0)
    return a, b, eps, w


def union_area(n, nx=1500):
    N = 2 ** n
    a, b, eps, w = family(n)
    tot = 0.0
    for x in (np.arange(nx) + 0.5) / nx:
        y = np.sort(a * x + b)
        tot += np.minimum(np.diff(y), 1 / N).sum() + 1 / N
    return tot / nx


for n in (4, 6, 8):
    a, b, _, _ = family(n)
    out[f"fam{n}"] = np.stack([a, b], 1)
ns = np.arange(2, 15)
areas = np.array([union_area(int(n)) for n in ns])
print(list(zip(ns, areas.round(4))))
out["ns"] = ns
out["areas"] = areas
np.savez("videos/data/v21.npz", **out)
