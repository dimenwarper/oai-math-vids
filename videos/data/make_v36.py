"""Spectra of T_m T_m^*/m, T_m = 1 + sum of m free Haar unitaries (modelled by independent
N x N Haar random unitaries, which are asymptotically free), versus the limit law
dnu = (1/2pi) sqrt((4-x)/x) dx on (0,4) from Lemma 4.3 of the paper."""
import numpy as np

rng = np.random.default_rng(7)
N = 600


def haar(n):
    z = (rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))) / np.sqrt(2)
    q, r = np.linalg.qr(z)
    d = np.diag(r)
    return q * (d / np.abs(d))


edges = np.linspace(0, 5, 51)
out = {}
for m in [1, 2, 4, 8, 16, 32]:
    T = np.eye(N, dtype=complex)
    for _ in range(m):
        T += haar(N)
    ev = np.linalg.eigvalsh(T @ T.conj().T / m)
    h, _ = np.histogram(ev, bins=edges, density=True)
    out[f"h{m}"] = h
    print(m, ev.min().round(4), ev.max().round(3), "mass below 0.1:", np.mean(ev < 0.1).round(4))
xs = np.linspace(0.02, 3.999, 400)
dens = np.sqrt((4 - xs) / xs) / (2 * np.pi)
np.savez("videos/data/v36.npz", edges=edges, xs=xs, dens=dens, **out)
