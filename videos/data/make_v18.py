"""Data for v18 (crossing numbers): Zarankiewicz drawings and the two-page drawing of K_n, with crossings."""
import numpy as np
from itertools import combinations


def Zb(m, n):
    return (m // 2) * ((m - 1) // 2) * (n // 2) * ((n - 1) // 2)


def Zc(n):
    return (n // 2) * ((n - 1) // 2) * ((n - 2) // 2) * ((n - 3) // 2) // 4


def seg_x(p1, p2, p3, p4):
    d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
    if abs(d) < 1e-12:
        return None
    t = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d
    u = ((p3[0] - p1[0]) * (p2[1] - p1[1]) - (p3[1] - p1[1]) * (p2[0] - p1[0])) / d
    if 1e-9 < t < 1 - 1e-9 and 1e-9 < u < 1 - 1e-9:
        return p1 + t * (p2 - p1)
    return None


def zarankiewicz(m, n, xs, ys):
    """m vertices on the x-axis, n on the y-axis, split as evenly as possible; straight edges."""
    A = np.array([[x, 0.0] for x in xs])
    B = np.array([[0.0, y] for y in ys])
    E = [(i, j) for i in range(m) for j in range(n)]
    X = []
    for (a, b), (c, d) in combinations(E, 2):
        if a == c or b == d:
            continue
        p = seg_x(A[a], B[b], A[c], B[d])
        if p is not None:
            X.append(p)
    X = np.array(X)
    # no triple crossings
    if len(X):
        dd = np.linalg.norm(X[:, None] - X[None], axis=2) + np.eye(len(X)) * 9
        assert dd.min() > 1e-6
    return A, B, X


out = {}
# K_{4,6}: positions chosen generically (no three edges through a point)
xs = [-2.1, -1.0, 1.15, 2.3]
ys = [-2.6, -1.55, -0.6, 0.65, 1.6, 2.7]
A, B, X = zarankiewicz(4, 6, xs, ys)
print("K_{4,6} crossings", len(X), "formula", Zb(4, 6))
assert len(X) == Zb(4, 6)
out.update(zA=A, zB=B, zX=X)

# K_{3,3} drawn the same way
A3, B3, X3 = zarankiewicz(3, 3, [-1.3, 1.0, 2.0], [-1.5, 1.0, 2.1])
print("K_{3,3} crossings", len(X3))
assert len(X3) == 1
out.update(z3A=A3, z3B=B3, z3X=X3)


# two-page drawing of K_n (de Klerk-Pasechnik-Salazar endpoint-sum rule, as in the paper):
# edge ij above the spine iff (i+j) mod n < floor(n/2); semicircles on the spine
def two_page(n, pos):
    m = n // 2
    E = [(i, j) for i in range(n) for j in range(i + 1, n)]
    side = np.array([1 if (i + j) % n < m else -1 for i, j in E])
    X = []
    for (e1, s1), (e2, s2) in combinations(zip(E, side), 2):
        if s1 != s2:
            continue
        (a, b), (c, d) = e1, e2
        if len({a, b, c, d}) < 4:
            continue
        if a < c < b < d or c < a < d < b:
            pa, pb, pc, pd = pos[a], pos[b], pos[c], pos[d]
            # circles centered on spine: (x-h1)^2+y^2=r1^2, (x-h2)^2+y^2=r2^2
            h1, r1 = (pa + pb) / 2, (pb - pa) / 2
            h2, r2 = (pc + pd) / 2, (pd - pc) / 2
            x = (r1 ** 2 - r2 ** 2 - h1 ** 2 + h2 ** 2) / (2 * (h2 - h1))
            y = np.sqrt(r1 ** 2 - (x - h1) ** 2)
            X.append((x, s1 * y))
    return np.array(E), side, np.array(X)


for n in (5, 6, 7, 8, 9, 10, 11):
    E, side, X = two_page(n, np.arange(n, dtype=float))
    print("two-page K_%d: crossings %d, Z(n) = %d" % (n, len(X), Zc(n)))
    assert len(X) == Zc(n)
pos7 = np.linspace(-5.4, 5.4, 7)
E7, S7, X7 = two_page(7, pos7)
pos8 = np.linspace(-5.6, 5.6, 8)
E8, S8, X8 = two_page(8, pos8)
out.update(pos7=pos7, E7=E7, S7=S7, X7=X7, pos8=pos8, E8=E8, S8=S8, X8=X8)
print("K7 above/below crossings", (X7[:, 1] > 0).sum(), (X7[:, 1] < 0).sum())

# signed crossing matrix of the K7 drawing: edges oriented from lower to higher label (left to right);
# sign of a crossing = orientation of the ordered pair of tangent vectors
def signed_matrix(n, pos):
    m = n // 2
    E = [(i, j) for i in range(n) for j in range(i + 1, n)]
    side = [1 if (i + j) % n < m else -1 for i, j in E]
    M = np.zeros((len(E), len(E)), int)
    for x, (e1, s1) in enumerate(zip(E, side)):
        for y, (e2, s2) in enumerate(zip(E, side)):
            if x >= y or s1 != s2:
                continue
            (a, b), (c, d) = e1, e2
            if not (a < c < b < d or c < a < d < b):
                continue
            pa, pb, pc, pd = pos[a], pos[b], pos[c], pos[d]
            h1, r1 = (pa + pb) / 2, (pb - pa) / 2
            h2, r2 = (pc + pd) / 2, (pd - pc) / 2
            X = (r1 ** 2 - r2 ** 2 - h1 ** 2 + h2 ** 2) / (2 * (h2 - h1))
            Y = s1 * np.sqrt(r1 ** 2 - (X - h1) ** 2)
            # tangent of a semicircle traversed left to right: (Y, -(X-h)) up to positive scaling, for the upper page
            t1 = np.array([s1 * Y, -s1 * (X - h1)])
            t2 = np.array([s2 * Y, -s2 * (X - h2)])
            sg = int(np.sign(t1[0] * t2[1] - t1[1] * t2[0]))
            M[x, y], M[y, x] = sg, -sg
    return M


M7 = signed_matrix(7, pos7)
print("K7 signed matrix: nonzero entries", (M7 != 0).sum(), "(= 2 x 9 crossing pairs)")
assert (M7 != 0).sum() == 18
out["M7"] = M7

# table of values and the dimension count C(s,2)^2 for n = 2s+1
tab = np.array([(n, Zc(n)) for n in range(5, 16)])
out["tab"] = tab
for s in range(2, 8):
    assert Zc(2 * s + 1) == (s * (s - 1) // 2) ** 2
np.savez("videos/data/v18.npz", **out)
print(tab)
