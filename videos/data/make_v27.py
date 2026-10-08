"""Data for v27 (DFT below n log n): constants of the explicit saving, DFT phases, CRT grid, C matrix checks."""
from pathlib import Path

import mpmath as mp
import numpy as np

mp.mp.dps = 40
m = mp.mpf(10) ** 6
Delta = mp.mpf(6871402692000000)
Wstar = mp.mpf(2) ** 71
lam = m - Delta / Wstar
theta = mp.log(lam) / mp.log(m)
print("lambda =", lam, " m - lambda =", m - lam, " theta =", theta, " 1-theta =", 1 - theta)
ratio64 = mp.mpf(64) ** mp.mpf("1e-13") - 1
print("(log2 n)^(1e-13) - 1 at n = 2^64:", ratio64)

# 8x8 DFT phases (fraction of a turn)
n = 8
ph = np.array([[(j * k) % n / n for k in range(n)] for j in range(n)])

# Good-Thomas: 15 = 3 x 5, index j -> (j mod 3, j mod 5)
crt = np.array([(j % 3, j % 5) for j in range(15)])
# check: F15 = P_out (F3 kron F5) P_in for CRT input map and Ruritanian/CRT output map
F = lambda r: np.exp(2j * np.pi * np.outer(np.arange(r), np.arange(r)) / r)
F15 = F(15)
# input map j -> (j mod 3, j mod 5); output map k -> (k*5^{-1}*... ) use CRT idempotents: k = 10 a + 6 b mod 15
# with omega_15^{jk}: choose output index k(a,b) = (10a + 6b) % 15 -> exponent jk/15 = j(10a+6b)/15 = 2ja/3 + 2jb/5
# so F15 restricted equals (F3^2 kron F5^2) up to the CRT map; F_r^2 is F_r with permuted rows: still a tensor product.
P_in = np.array([3 * (j % 3) + 0 for j in range(15)])
M = np.zeros((15, 15), complex)
for j in range(15):
    for a in range(3):
        for b in range(5):
            k = (10 * a + 6 * b) % 15
            M[3 * 0 + a * 5 + b, j] = F15[k, j]
T = np.kron(F(3)[[0, 2, 1]], F(5)[[0, 2, 4, 1, 3]])
cols = [(j % 3) * 5 + (j % 5) for j in range(15)]
ok = np.allclose(M, T[:, cols])
print("Good-Thomas tensor identity holds:", ok)

a, b = (1 + 1j) / 2, (1 - 1j) / 2
C = np.array([[a, b], [b, a]])
print("C^2 =", np.round(C @ C, 12).tolist())
np.savez(Path(__file__).with_name("v27.npz"), ph=ph, crt=crt, theta=float(theta), lam=float(lam),
         mlam=float(m - lam), ratio64=float(ratio64), gt_ok=ok)
