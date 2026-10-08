"""Data for v20 (Barnette): Tutte embeddings and Hamiltonian cycles of cubic bipartite polyhedra."""
import numpy as np
from itertools import permutations, product


def tutte(nv, edges, outer, radius=1.0, rot=0.0):
    k = len(outer)
    pos = np.zeros((nv, 2))
    for t, v in enumerate(outer):
        a = rot + 2 * np.pi * t / k
        pos[v] = radius * np.array([np.cos(a), np.sin(a)])
    nb = [[] for _ in range(nv)]
    for a, b in edges:
        nb[a].append(b)
        nb[b].append(a)
    inner = [v for v in range(nv) if v not in outer]
    idx = {v: i for i, v in enumerate(inner)}
    M = np.zeros((len(inner), len(inner)))
    rhs = np.zeros((len(inner), 2))
    for v in inner:
        M[idx[v], idx[v]] = len(nb[v])
        for w in nb[v]:
            if w in idx:
                M[idx[v], idx[w]] -= 1
            else:
                rhs[idx[v]] += pos[w]
    sol = np.linalg.solve(M, rhs)
    for v in inner:
        pos[v] = sol[idx[v]]
    return pos, nb


def ham_cycle(nv, nb, start=0):
    path, used = [start], {start}

    def rec():
        if len(path) == nv:
            return start in nb[path[-1]]
        for w in sorted(nb[path[-1]]):
            if w not in used:
                path.append(w)
                used.add(w)
                if rec():
                    return True
                path.pop()
                used.discard(w)
        return False

    assert rec()
    return list(path)


def bipartite(nv, nb):
    col = [-1] * nv
    col[0] = 0
    st = [0]
    while st:
        v = st.pop()
        for w in nb[v]:
            if col[w] < 0:
                col[w] = 1 - col[v]
                st.append(w)
            assert col[w] != col[v]
    return col


out = {}
# ---- truncated octahedron: permutations of (0, +-1, +-2)
V = sorted(set(p for s in product([1, -1], repeat=2) for p in permutations((0, s[0] * 1, s[1] * 2))))
V = [np.array(v, float) for v in V]
nv = len(V)
E = [(i, j) for i in range(nv) for j in range(i + 1, nv) if abs(np.linalg.norm(V[i] - V[j]) - np.sqrt(2)) < 1e-9]
assert nv == 24 and len(E) == 36
# outer face: a hexagon = vertices with x+y+z = 3 (a hexagonal face), ordered by angle
hexf = [i for i, v in enumerate(V) if abs(v.sum() - 3) < 1e-9]
c = np.mean([V[i] for i in hexf], axis=0)
u1 = V[hexf[0]] - c
u2 = np.cross(np.ones(3) / np.sqrt(3), u1)
hexf.sort(key=lambda i: np.arctan2((V[i] - c) @ u2, (V[i] - c) @ u1))
pos, nb = tutte(nv, E, hexf, radius=3.4, rot=np.pi / 6)
# spread the inner rings radially (r -> R (r/R)^0.6) for legibility, then check the drawing is still plane
rr = np.linalg.norm(pos, axis=1, keepdims=True)
pos = pos / rr * 3.4 * (rr / 3.4) ** 0.6


def cross(p1, p2, p3, p4):
    def o(a, b, c):
        return np.sign((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))
    return o(p1, p2, p3) * o(p1, p2, p4) < 0 and o(p3, p4, p1) * o(p3, p4, p2) < 0


for x in range(len(E)):
    for y in range(x + 1, len(E)):
        (a, b), (c, d) = E[x], E[y]
        if len({a, b, c, d}) == 4:
            assert not cross(pos[a], pos[b], pos[c], pos[d]), (E[x], E[y])
print("rescaled embedding is still plane; min vertex distance",
      min(np.linalg.norm(pos[i] - pos[j]) for i in range(nv) for j in range(i + 1, nv)))
col = bipartite(nv, nb)
H = ham_cycle(nv, nb)
print("truncated octahedron: Hamiltonian cycle", H)
out.update(to_pos=pos, to_E=np.array(E), to_H=np.array(H), to_col=np.array(col))

# ---- cube (planar: outer square 0-3, inner square 4-7)
cpos = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]], float)
cpos = np.vstack([cpos * 2.2, cpos * 0.9])
cE = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
cnb = [[] for _ in range(8)]
for a, b in cE:
    cnb[a].append(b)
    cnb[b].append(a)
cH = [0, 1, 5, 6, 2, 3, 7, 4]  # a Hamiltonian cycle
assert all(cH[(i + 1) % 8] in cnb[cH[i]] for i in range(8))
faces = {"in": [4, 5, 6, 7], "S": [0, 1, 5, 4], "E": [1, 2, 6, 5], "N": [2, 3, 7, 6], "W": [3, 0, 4, 7],
         "out": [0, 1, 2, 3]}


def inside(pt, poly):
    x, y = pt
    res = False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            res = not res
    return res


poly = [cpos[v] for v in cH]
side = {}
for f, vs in faces.items():
    side[f] = (f != "out") and inside(cpos[vs].mean(0), poly)
print("faces inside the cycle:", [f for f in faces if side[f]], "outside:", [f for f in faces if not side[f]])
cbip = bipartite(8, cnb)
out.update(c_pos=cpos, c_E=np.array(cE), c_H=np.array(cH), c_col=np.array(cbip),
           c_in=np.array([f for f in faces if side[f]]), c_out=np.array([f for f in faces if not side[f]]))
np.savez("videos/data/v20.npz", **out)
