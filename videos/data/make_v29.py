"""Data for v29 (3-colorable graphs): planted 3-colorable graph, circle 'half-shift' graph."""
from pathlib import Path

import numpy as np

rng = np.random.default_rng(11)

# planted 3-colorable graph on a jittered grid
pos, col = [], []
for i in range(7):
    for j in range(3):
        pos.append([-5.4 + 1.8 * i + rng.uniform(-0.35, 0.35), -1.9 + 1.7 * j + rng.uniform(-0.3, 0.3)])
pos = np.array(pos)
n = len(pos)
col = rng.integers(0, 3, size=n)
edges = []
for a in range(n):
    for b in range(a + 1, n):
        d = np.linalg.norm(pos[a] - pos[b])
        if col[a] != col[b] and d < 2.75 and rng.random() < 0.95:
            edges.append((a, b))
deg = np.zeros(n, int)
for a, b in edges:
    deg[a] += 1
    deg[b] += 1
for a in range(n):
    if deg[a] < 2:
        cand = sorted((np.linalg.norm(pos[a] - pos[b]), b) for b in range(n) if col[b] != col[a])
        for _, b in cand:
            e = (min(a, b), max(a, b))
            if e not in edges:
                edges.append(e)
                deg[a] += 1
                deg[b] += 1
            if deg[a] >= 2:
                break
edges = np.array(edges)


def is_k_colorable(n, edges, k):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    c = [-1] * n

    def go(v):
        if v == n:
            return True
        for x in range(k):
            if all(c[u] != x for u in adj[v]):
                c[v] = x
                if go(v + 1):
                    return True
        c[v] = -1
        return False

    return go(0)


print("vertices", n, "edges", len(edges), "2-colorable", is_k_colorable(n, edges, 2), "3-col",
      is_k_colorable(n, edges, 3))

# circle graph: x ~ y iff circle distance between x and y + 1/2 is <= 1/8
N = 20
xs = np.sort((np.arange(N) + rng.uniform(-0.3, 0.3, N)) / N % 1.0)


def cd(a, b):
    d = abs(a - b) % 1.0
    return min(d, 1 - d)


cedges = np.array([(a, b) for a in range(N) for b in range(a + 1, N) if cd(xs[a], xs[b] + 0.5) <= 1 / 8])
arc = np.floor(xs * 3).astype(int)
bad = [(a, b) for a, b in cedges if arc[a] == arc[b]]
print("circle edges", len(cedges), "monochromatic", len(bad))
assert not bad

np.savez(Path(__file__).with_name("v29.npz"), pos=pos, col=col, edges=edges, xs=xs, cedges=cedges, arc=arc)
