"""Data for v28 (integer multiplication): binary product, XOR swap, triple-intersection matrix, constants."""
import itertools
from fractions import Fraction
from pathlib import Path

import mpmath as mp
import numpy as np

x, y = 0b10110101, 0b11010011
prod = x * y
print(x, y, prod, bin(prod))
xb = [int(c) for c in format(x, "08b")]
yb = [int(c) for c in format(y, "08b")]
pb = [int(c) for c in format(prod, "016b")]

# XOR swap on two 8-bit registers: y ^= x; x ^= y; y ^= x
X0 = np.array([1, 0, 1, 1, 0, 0, 1, 0])
Y0 = np.array([0, 1, 1, 0, 1, 0, 0, 1])
s1 = (X0, Y0 ^ X0)
s2 = (s1[0] ^ s1[1], s1[1])
s3 = (s2[0], s2[1] ^ s2[0])
assert (s3[0] == Y0).all() and (s3[1] == X0).all()
xsteps = np.array([[X0, Y0], [s1[0], s1[1]], [s2[0], s2[1]], [s3[0], s3[1]]])

# triples of {1..h}: gather/scatter coefficient |S cap T| mod 2, side wires cancel |S cap T| = 1
h = 6
tr = list(itertools.combinations(range(h), 3))
inter = np.array([[len(set(S) & set(T)) for T in tr] for S in tr])
par = inter % 2
N1 = (inter == 1).astype(int)
assert ((par - N1) == np.eye(len(tr), dtype=int)).all()
print("triples", len(tr), "N1 count per row", N1.sum(1)[0])

# constants from the paper (h = 100)
from math import comb
v = comb(100, 3)
print("v =", v, " m =", 100 ** 3)
eta_b = Fraction(339, 22587335000000)
mp.mp.dps = 30
kappa = mp.mpf(2) ** -182
print("eta_b ~", float(eta_b), " tau = 1 - 2^-50 =", 1 - 2.0 ** -50, " kappa =", kappa)
np.savez(Path(__file__).with_name("v28.npz"), xb=xb, yb=yb, pb=pb, xsteps=xsteps, inter=inter, par=par, N1=N1,
         eta_b=float(eta_b), v=v)
