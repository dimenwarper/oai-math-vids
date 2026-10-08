"""Data for v12 (Goldfeld's conjecture), using the congruent-number family E_n: y^2 = x^3 - n^2 x,
the quadratic twists of y^2 = x^3 - x.

Root number of E_n (n squarefree): +1 if n = 1,2,3 mod 8, -1 if n = 5,6,7 mod 8.
Tunnell (1983, unconditional for the L-value via Waldspurger): for odd squarefree n,
    L(E_n,1) = 0  <=>  #{x^2+2y^2+8z^2=n} = 2 #{x^2+2y^2+32z^2=n};
for even squarefree n,
    L(E_n,1) = 0  <=>  #{x^2+4y^2+8z^2=n/2} = 2 #{x^2+4y^2+32z^2=n/2}.
Classes: 0 = even sign & L(E_n,1) != 0 (analytic rank 0); 1 = odd sign (odd analytic rank);
         2 = even sign & L(E_n,1) = 0 (analytic rank >= 2).
"""
import numpy as np

N = 2_000_000


def theta(k, n):
    t = np.zeros(n + 1)
    x = 0
    while k * x * x <= n:
        t[k * x * x] += 1 if x == 0 else 2
        x += 1
    return t


def conv(a, b, n):
    L = 1 << int(np.ceil(np.log2(2 * n + 2)))
    c = np.fft.irfft(np.fft.rfft(a, L) * np.fft.rfft(b, L), L)[: n + 1]
    return np.rint(c).astype(np.int64)


def ternary(k1, k2, k3, n):
    return conv(conv(theta(k1, n), theta(k2, n), n), theta(k3, n), n)


A = ternary(1, 2, 8, N)
B = ternary(1, 2, 32, N)
C = ternary(1, 4, 8, N // 2)
D = ternary(1, 4, 32, N // 2)

sqf = np.ones(N + 1, bool)
sqf[0] = False
for p in range(2, int(N**0.5) + 1):
    sqf[p * p :: p * p] = False
ns = np.nonzero(sqf)[0]
cls = np.zeros(len(ns), np.int8)
r8 = ns % 8
odd_sign = np.isin(r8, [5, 6, 7])
cls[odd_sign] = 1
for i in np.nonzero(~odd_sign)[0]:
    n = ns[i]
    if n % 2:
        zero = A[n] == 2 * B[n]
    else:
        zero = C[n // 2] == 2 * D[n // 2]
    if zero:
        cls[i] = 2

print("first rank>=2 (even sign, L=0):", ns[cls == 2][:20])
print("first odd:", ns[cls == 1][:20])
xs = np.unique(np.geomspace(10, N, 300).astype(np.int64))
k = np.searchsorted(ns, xs, side="right")
c = np.cumsum(np.stack([cls == 0, cls == 1, cls == 2]), axis=1)
fr = np.stack([c[j][k - 1] / k for j in range(3)])
for X in (100, 1000, 10**4, 10**5, 10**6, 2 * 10**6):
    kk = np.searchsorted(ns, X, side="right")
    print(X, [round(c[j][kk - 1] / kk, 4) for j in range(3)])
np.savez("videos/data/v12.npz", ns=ns[:400], cls=cls[:400], xs=xs, fr=fr)
