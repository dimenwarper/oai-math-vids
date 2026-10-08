"""(2,3,7) triangle tiling of the Poincare disk, a group element used to magnify a boundary arc,
and a min-cost 'height function' on a grid (illustrating the blocking-weight construction)."""
import heapq

import numpy as np

p, q, r = 7, 2, 3  # angles pi/7 at A=0, pi/2 at B (real axis), pi/3 at C
al, be, ga = np.pi / p, np.pi / q, np.pi / r
c_len = np.arccosh((np.cos(ga) + np.cos(al) * np.cos(be)) / (np.sin(al) * np.sin(be)))  # AB
b_len = np.arccosh((np.cos(be) + np.cos(al) * np.cos(ga)) / (np.sin(al) * np.sin(ga)))  # AC
A = 0j
B = np.tanh(c_len / 2) + 0j
C = np.tanh(b_len / 2) * np.exp(1j * al)
# circle through B, C orthogonal to unit circle: center c with |c|^2 = R^2 + 1
# solve |B-c|^2 = |c|^2 - 1, |C-c|^2 = |c|^2 - 1  ->  2 Re(conj(z) c) = |z|^2 + 1
M2 = np.array([[2 * B.real, 2 * B.imag], [2 * C.real, 2 * C.imag]])
rhs = np.array([abs(B) ** 2 + 1, abs(C) ** 2 + 1])
cx, cy = np.linalg.solve(M2, rhs)
cc = cx + 1j * cy
R = np.sqrt(abs(cc) ** 2 - 1)

refl = [
    (np.eye(2, dtype=complex), True),  # real axis (AB)
    (np.array([[np.exp(1j * al), 0], [0, np.exp(-1j * al)]]), True),  # line AC
    (np.array([[cc, -1], [1, -np.conj(cc)]]), True),  # circle BC
]


def compose(f, g):
    Mf, af = f
    Mg, ag = g
    M = Mf @ (np.conj(Mg) if af else Mg)
    return (M / np.sqrt(np.linalg.det(M)), af ^ ag)


def apply(f, z):
    M, a = f
    w = np.conj(z) if a else z
    return (M[0, 0] * w + M[0, 1]) / (M[1, 0] * w + M[1, 1])


def sample_boundary(n=14):
    t = np.linspace(0, 1, n, endpoint=False)
    ab = A + (B - A) * t
    # arc B -> C on circle centered cc
    thB, thC = np.angle(B - cc), np.angle(C - cc)
    d = (thC - thB + np.pi) % (2 * np.pi) - np.pi
    bc = cc + R * np.exp(1j * (thB + d * t))
    ca = C + (A - C) * t
    return np.concatenate([ab, bc, ca])


F = sample_boundary()
verts = np.array([A, B, C])
ident = (np.eye(2, dtype=complex), False)
key = lambda z: (round(z.real, 5), round(z.imag, 5))
cent0 = verts.mean()
seen = {key(cent0)}
tiles = [ident]
frontier = [ident]
LIM = 0.968
while frontier:
    nf = []
    for f in frontier:
        for rf in refl:
            g = compose(f, rf)
            v = apply(g, verts)
            if np.max(np.abs(v)) > LIM:
                continue
            k = key(apply(g, cent0))
            if k in seen:
                continue
            seen.add(k)
            tiles.append(g)
            nf.append(g)
    frontier = nf
polys = np.array([apply(g, F) for g in tiles])
par = np.array([g[1] for g in tiles])
cents = np.array([apply(g, cent0) for g in tiles])
print("tiles", len(tiles), "B", B, "C", C, "R", R)

# pick an orientation-preserving tile far out, towards the left, and the element mapping it to F
hd = 2 * np.arctanh(np.abs(cents))
cand = [i for i in range(len(tiles)) if not par[i] and 2.6 < hd[i] < 3.0 and np.cos(np.angle(cents[i]) - 3.6) > 0.97]
best = None
for i in cand:
    M, a = tiles[i]
    Minv = np.linalg.inv(M)
    Minv = Minv / np.sqrt(np.linalg.det(Minv))
    tr = np.trace(Minv)
    if abs(tr.imag) < 1e-6 and abs(tr.real) > 2.05:
        best = (i, Minv)
        break
i0, G = best
if np.trace(G).real < 0:
    G = -G
w, V = np.linalg.eig(G)
L = V @ np.diag(np.log(w.astype(complex))) @ np.linalg.inv(V)
print("tile", i0, "dist", hd[i0], "angle", np.angle(cents[i0]), "trace", np.trace(G))
# second pass: keep every tile that is visible either before or after applying G
Gf = (G, False)
seen = {key(cent0)}
tiles = [ident]
frontier = [ident]
while frontier:
    nf = []
    for f in frontier:
        for rf in refl:
            g = compose(f, rf)
            v = apply(g, verts)
            if np.max(np.abs(v)) > LIM and np.max(np.abs(apply(Gf, v))) > LIM:
                continue
            k = key(apply(g, cent0))
            if k in seen:
                continue
            seen.add(k)
            tiles.append(g)
            nf.append(g)
    frontier = nf
polys = np.array([apply(g, F) for g in tiles])
par = np.array([g[1] for g in tiles])
print("tiles (union)", len(tiles))
# boundary arc around the tile's direction, and its image
th0 = np.angle(cents[i0])
arc = np.exp(1j * np.linspace(th0 - 0.09, th0 + 0.09, 60))
img = (G[0, 0] * arc + G[0, 1]) / (G[1, 0] * arc + G[1, 1])
ang = np.unwrap(np.angle(img))
print("arc image span (deg)", np.degrees(ang.max() - ang.min()))
# check: G maps the tiling onto itself (centroids of images are centroids of tiles)
allc = {key(apply(g, cent0)) for g in tiles}
imgc = [key(apply(compose(Gf, g), cent0)) for g in tiles if np.max(np.abs(apply(compose(Gf, g), verts))) < 0.9]
print("G-invariance check:", sum(k in allc for k in imgc), "/", len(imgc))

# min-cost height function on a grid (blocking weights -> separating level sets)
rng = np.random.default_rng(11)
H, W = 36, 54
raw = rng.normal(size=(H + 8, W + 8))
k = np.ones((5, 5)) / 25
sm = np.zeros((H, W))
for dy in range(5):
    for dx in range(5):
        sm += raw[dy:dy + H, dx:dx + W] / 25
rho = np.exp(0.55 * sm / sm.std())
dist = np.full((H, W), np.inf)
pq = [(rho[0, j], 0, j) for j in range(W)]
for d0, i, j in pq:
    dist[i, j] = d0
heapq.heapify(pq)
while pq:
    d0, i, j = heapq.heappop(pq)
    if d0 > dist[i, j]:
        continue
    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        a, b = i + di, j + dj
        if 0 <= a < H and 0 <= b < W:
            nd = d0 + rho[a, b]
            if nd < dist[a, b]:
                dist[a, b] = nd
                heapq.heappush(pq, (nd, a, b))
height = dist / np.median(dist[-1])
print("height range", height.min(), height.max())
np.savez("videos/data/v37.npz", polys=polys, par=par, i0=i0, G=G, L=L, arc=arc, img=img,
         height=np.minimum(height, 1.0), rho=rho)
