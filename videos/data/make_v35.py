"""1-D cartoon of a one-species collisionless plasma: N charged sheets, exact 1-D electrostatic field
E_i = (charge to the left - charge to the right)/2, relativistic motion dx/dt = v/sqrt(1+v^2), dv/dt = E.
(One space dimension, electric field only: a cartoon, not the 3-D Vlasov-Maxwell system.)
Output: videos/data/v35.npz with phase-space snapshots (x, v)."""
import numpy as np

N = 2500
Q = 3.0  # total charge (sets the strength of repulsion)
rng = np.random.default_rng(2)
x = np.sort(rng.uniform(-1, 1, N))
v = -2.2 * np.sin(np.pi * x / 2) * 1.0 + 0.25 * rng.standard_normal(N)


def field(x):
    order = np.argsort(x)
    rank = np.empty(N)
    rank[order] = np.arange(N)
    left = rank * (Q / N)
    right = (N - 1 - rank) * (Q / N)
    return 0.5 * (left - right)


dt = 0.002
T = 4.0
snaps_t = np.linspace(0, T, 181)
snaps = []
t, k = 0.0, 0
while k < len(snaps_t):
    if t >= snaps_t[k] - 1e-9:
        snaps.append(np.c_[x, v].copy())
        k += 1
    # velocity Verlet-like (leapfrog) step
    E = field(x)
    v = v + 0.5 * dt * E
    x = x + dt * v / np.sqrt(1 + v * v)
    E = field(x)
    v = v + 0.5 * dt * E
    t += dt
snaps = np.array(snaps, np.float32)
np.savez_compressed("videos/data/v35.npz", snaps=snaps, t=snaps_t)
print(snaps.shape, "x range", snaps[..., 0].min(), snaps[..., 0].max(), "v range", snaps[..., 1].min(),
      snaps[..., 1].max())
