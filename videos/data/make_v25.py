"""Data for v25 (Littlewood): |p(e^{it})|/sqrt(N) for actual polynomials, merit factors, chirp experiments."""
import numpy as np

out = {}
M = 4096
ts = np.arange(M) / M  # t in turns: z = e^{2 pi i t}


def curve(c):
    return np.abs(np.fft.fft(c, M)) / np.sqrt(len(c))


def merit(c):
    N = len(c)
    C = np.correlate(c, c, "full")[N:]
    return N ** 2 / (2 * (C ** 2).sum())


def rudin_shapiro(n):
    p, q = np.array([1.0]), np.array([1.0])
    for _ in range(n):
        p, q = np.r_[p, q], np.r_[p, -q]
    return p


rng = np.random.default_rng(1)
N = 128
rand = rng.choice([-1.0, 1.0], N)
rs = rudin_shapiro(7)
p = 127
leg = np.array([1] + [1 if pow(x, (p - 1) // 2, p) == 1 else -1 for x in range(1, p)], float)
leg = np.roll(leg, -(p // 4))  # Legendre sequence rotated by a quarter: merit factor near 6
small = rng.choice([-1.0, 1.0], 16)
for name, c in (("rand", rand), ("rs", rs), ("leg", leg), ("small", small)):
    out[name] = c
    out[name + "_mod"] = curve(c)
    out[name + "_merit"] = merit(c)
    print(name, len(c), "max %.3f min %.3f merit %.3f" % (curve(c).max(), curve(c).min(), merit(c)))
# chirps, N = 512
N2 = 512
k = np.arange(N2)
ph = 2 * np.pi * k ** 2 / (4 * N2)  # instantaneous frequency k/(2N) sweeps half the circle once
ccos = np.cos(ph)
csgn = np.where(np.cos(ph) >= 0, 1.0, -1.0)
cplx = np.exp(1j * np.pi * k ** 2 / N2)  # unimodular quadratic phases
for name, c in (("ccos", ccos), ("csgn", csgn), ("cplx", cplx)):
    out[name] = c
    out[name + "_mod"] = curve(c)
    m = curve(c)
    print(name, "max %.3f min %.3f p10 %.3f p90 %.3f mean|c|^2 %.3f" % (m.max(), m.min(), *np.percentile(m, [10, 90]),
                                                                     np.mean(np.abs(c) ** 2)))
# a single chirp block: footprint on the circle
Nb = 512
x = np.arange(Nb) / Nb
blk = np.zeros(Nb)
x0, wdt, lam, eta = 0.5, 0.25, 0.10, 0.20  # centre, half-width (in x), curvature, linear frequency
cut = np.clip(1 - ((x - x0) / wdt) ** 2, 0, None) ** 2
blk = cut * np.cos(2 * np.pi * Nb * (lam / 2 * (x - x0) ** 2 + eta * x))
out["blk"] = blk
out["blk_mod"] = curve(blk)
out["blk_params"] = np.array([x0, wdt, lam, eta])
out["ts"] = ts
np.savez("videos/data/v25.npz", **out)
