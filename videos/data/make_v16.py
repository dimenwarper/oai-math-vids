"""Data for v16 (Gaussian moat): Gaussian primes, bounded-step components, a finite sieve."""
import numpy as np
from collections import deque
from sympy import isprime

R = 120  # search box for components (the D=2 component from 1+i stays inside radius 46)


def is_gp(a, b):
    if a == 0 or b == 0:
        m = abs(a + b)
        return isprime(m) and m % 4 == 3
    return isprime(a * a + b * b)


P = sorted((a, b) for a in range(-R, R + 1) for b in range(-R, R + 1) if is_gp(a, b))
Pset = set(P)


def offsets(D):
    r = int(np.floor(D))
    return [(dx, dy) for dx in range(-r, r + 1) for dy in range(-r, r + 1) if 0 < dx * dx + dy * dy <= D * D + 1e-9]


def component(start, D):
    off = offsets(D)
    par = {start: None}
    q = deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in off:
            r = (x + dx, y + dy)
            if r in Pset and r not in par:
                par[r] = (x, y)
                q.append(r)
    return par


out = {}
box = 52
out["primes"] = np.array([p for p in P if abs(p[0]) <= box and abs(p[1]) <= box])
for name, D in (("c2", 2.0), ("cs2", 2 ** 0.5)):
    par = component((1, 1), D)
    mem = np.array(list(par.keys()))
    out[name] = mem
    far = max(par, key=lambda p: p[0] ** 2 + p[1] ** 2)
    path = [far]
    while par[path[-1]] is not None:
        path.append(par[path[-1]])
    out[name + "_path"] = np.array(path[::-1])
    print(name, len(mem), "max radius", np.sqrt((mem ** 2).sum(1)).max(), "path len", len(path), "far", far)
    assert np.sqrt((mem ** 2).sum(1)).max() < R - 5


# ---- a finite sieve for step length 1: remove multiples of both Gaussian factors of 5, 13, 17
def sqrtm1(p):
    return next(a for a in range(2, p) if (a * a + 1) % p == 0)


def allowed(primes, xs, ys):
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    ok = np.ones(X.shape, bool)
    for p in primes:
        a = sqrtm1(p)
        ok &= ((X + a * Y) % p != 0) & ((X - a * Y) % p != 0)
    return ok


def torus_check(primes, D=1):
    """Exact test on the period torus: are all components in Z^2 finite? returns (finite?, max size)."""
    Q = int(np.prod(primes))
    ok = allowed(primes, np.arange(Q), np.arange(Q))
    off = offsets(D)
    seen = np.zeros((Q, Q), bool)
    best = 0
    for sx in range(Q):
        for sy in range(Q):
            if not ok[sx, sy] or seen[sx, sy]:
                continue
            lift = {(sx, sy): (sx, sy)}
            seen[sx, sy] = True
            q = deque([(sx, sy)])
            while q:
                x, y = q.popleft()
                X, Y = lift[(x, y)]
                for dx, dy in off:
                    nx, ny = (x + dx) % Q, (y + dy) % Q
                    if not ok[nx, ny]:
                        continue
                    if not seen[nx, ny]:
                        seen[nx, ny] = True
                        lift[(nx, ny)] = (X + dx, Y + dy)
                        q.append((nx, ny))
                    elif lift[(nx, ny)] != (X + dx, Y + dy):
                        return False, None
            best = max(best, len(lift))
    return True, best


fin5, _ = torus_check((5,))
fin, best = torus_check((5, 13, 17))
print("sieve {5}: finite?", fin5, " sieve {5,13,17}: finite?", fin, "largest island", best)
assert (not fin5) and fin

# window for display
x0, y0, W, H = 300, 200, 56, 30
xs, ys = np.arange(x0, x0 + W), np.arange(y0, y0 + H)
for name, prs in (("w5", (5,)), ("w3", (5, 13, 17))):
    ok = allowed(prs, xs, ys)
    lab = -np.ones(ok.shape, int)
    k = 0
    for i in range(W):
        for j in range(H):
            if ok[i, j] and lab[i, j] < 0:
                lab[i, j] = k
                q = deque([(i, j)])
                while q:
                    a, b = q.popleft()
                    for da, db in offsets(1):
                        c, d = a + da, b + db
                        if 0 <= c < W and 0 <= d < H and ok[c, d] and lab[c, d] < 0:
                            lab[c, d] = k
                            q.append((c, d))
                k += 1
    out[name] = lab
    print(name, "allowed", ok.sum(), "components in window", k)
gpw = np.array([(i, j) for i in range(W) for j in range(H) if is_gp(x0 + i, y0 + j)])
out["wprimes"] = gpw
ok3 = allowed((5, 13, 17), xs, ys)
assert all(ok3[i, j] for i, j in gpw)
out["window"] = np.array([x0, y0, W, H])
out["best"] = np.array([best])
np.savez("videos/data/v16.npz", **out)
print("primes in box", len(out["primes"]), "primes in window", len(gpw))
