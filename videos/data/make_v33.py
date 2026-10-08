"""Billiard trajectories in an irrational triangle (angles 1, 0.8, pi-1.8 rad) and a nearby rational one
(pi/3, pi/4, 5pi/12). Exact specular reflection, event driven. Output: videos/data/v33.npz"""
import numpy as np


def triangle(alpha, beta):
    """A=(0,0), B=(1,0), angle alpha at A, beta at B."""
    gamma = np.pi - alpha - beta
    ac = np.sin(beta) / np.sin(gamma)
    return np.array([[0.0, 0.0], [1.0, 0.0], [ac * np.cos(alpha), ac * np.sin(alpha)]])


def next_hit(T, p, v, skip):
    best, bi = np.inf, -1
    for i in range(3):
        if i == skip:
            continue
        a, b = T[i], T[(i + 1) % 3]
        e = b - a
        den = v[0] * (-e[1]) - v[1] * (-e[0])
        if abs(den) < 1e-14:
            continue
        w = a - p
        t = (w[0] * (-e[1]) - w[1] * (-e[0])) / den
        s = (v[0] * w[1] - v[1] * w[0]) / den
        if t > 1e-12 and -1e-12 <= s <= 1 + 1e-12 and t < best:
            best, bi = t, i
    return best, bi


def reflect(v, T, i):
    e = T[(i + 1) % 3] - T[i]
    e = e / np.linalg.norm(e)
    return 2 * np.dot(v, e) * e - v


def trajectory(T, p0, th0, nb):
    p, v, skip = np.array(p0, float), np.array([np.cos(th0), np.sin(th0)]), -1
    pts, dirs = [p.copy()], []
    for _ in range(nb):
        t, i = next_hit(T, p, v, skip)
        dirs.append(np.arctan2(v[1], v[0]))
        p = p + t * v
        pts.append(p.copy())
        v = reflect(v, T, i)
        skip = i
    return np.array(pts), np.array(dirs)


def positions_at(T, p0, th0, times):
    """Position and direction at each requested (sorted) time."""
    p, v, skip = np.array(p0, float), np.array([np.cos(th0), np.sin(th0)]), -1
    out, dout = np.zeros((len(times), 2)), np.zeros(len(times))
    tnow, k = 0.0, 0
    while k < len(times):
        t, i = next_hit(T, p, v, skip)
        while k < len(times) and times[k] <= tnow + t:
            out[k] = p + (times[k] - tnow) * v
            dout[k] = np.arctan2(v[1], v[0])
            k += 1
        p, tnow = p + t * v, tnow + t
        v = reflect(v, T, i)
        skip = i
    return out, dout


def unfold(T, p0, th0, nb):
    """Straight line through successive reflected copies of the table."""
    v = np.array([np.cos(th0), np.sin(th0)])
    P, skip = np.array(p0, float), -1
    copies = [T.copy()]
    cur = T.copy()
    for _ in range(nb):
        t, i = next_hit(cur, P, v, skip)
        P = P + t * v
        a, b = cur[i], cur[(i + 1) % 3]
        e = (b - a) / np.linalg.norm(b - a)
        new = np.array([a + 2 * np.dot(q - a, e) * e - (q - a) for q in cur])
        cur = new
        copies.append(cur.copy())
        skip = i  # same vertex order is kept, so side i is shared
    return np.array(copies), P


Ti = triangle(1.0, 0.8)
Tr = triangle(np.pi / 3, np.pi / 4)
cen = lambda T: T.mean(axis=0)

# long single trajectories
p0 = cen(Ti) + np.array([-0.12, -0.05])
th0 = 0.37
traj_i, dirs_i = trajectory(Ti, p0, th0, 3000)
traj_r, dirs_r = trajectory(Tr, cen(Tr) + np.array([-0.12, -0.05]), th0, 3000)
print("distinct rational directions:", len(np.unique(np.round(np.mod(dirs_r, 2 * np.pi), 6))))

# unfolding
copies, endP = unfold(Ti, p0, th0, 6)
fold_pts, _ = trajectory(Ti, p0, th0, 6)

# clouds
rng = np.random.default_rng(1)
NB = 1200
times = np.linspace(0, 24, 241)
q0 = np.array([0.32, 0.12])
r = 0.025 * np.sqrt(rng.uniform(0, 1, NB))
a = rng.uniform(0, 2 * np.pi, NB)
starts = q0 + np.c_[r * np.cos(a), r * np.sin(a)]
ths = 0.9 + rng.uniform(-0.04, 0.04, NB)
cloud_i = np.zeros((len(times), NB, 2), np.float32)
cloud_r = np.zeros((len(times), NB, 2), np.float32)
cdir_i = np.zeros((len(times), NB), np.float32)
cdir_r = np.zeros((len(times), NB), np.float32)
qr0 = q0 * np.array([1, 1])
for b in range(NB):
    P, D = positions_at(Ti, starts[b], ths[b], times)
    cloud_i[:, b], cdir_i[:, b] = P, D
    P, D = positions_at(Tr, starts[b], ths[b], times)
    cloud_r[:, b], cdir_r[:, b] = P, D

np.savez_compressed("videos/data/v33.npz", Ti=Ti, Tr=Tr, traj_i=traj_i, traj_r=traj_r, dirs_i=dirs_i, dirs_r=dirs_r,
                    copies=copies, endP=endP, fold_pts=fold_pts, times=times, cloud_i=cloud_i, cloud_r=cloud_r,
                    cdir_i=cdir_i, cdir_r=cdir_r)
print(Ti, Tr)
print("cloud range", cloud_i.min(), cloud_i.max(), cloud_r.min(), cloud_r.max())
print("rational cloud distinct dirs at end (rounded 2dp):", len(np.unique(np.round(np.mod(cdir_r[-1], 2 * np.pi), 1))))
