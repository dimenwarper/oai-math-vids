import numpy as np, mpmath as mp, time
mp.mp.dps = 20
t = time.time()
N = 100
gam = [float(mp.im(mp.zetazero(k))) for k in range(1, N + 1)]
xs = np.linspace(1.6, 50, 900)
R = np.array([float(mp.riemannr(x)) for x in xs])
corr = -1 / np.log(xs) + np.arctan(np.pi / np.log(xs)) / np.pi
terms = np.zeros((N, len(xs)))
for k, g in enumerate(gam):
    rho = mp.mpc(0.5, g)
    terms[k] = [-2 * float(mp.re(mp.ei(rho * mp.log(x)))) for x in xs]
li = np.array([float(mp.li(x)) for x in xs])
np.savez("videos/data/v01.npz", gam=np.array(gam), xs=xs, R=R + corr, terms=terms, li=li)
print("done", time.time() - t, gam[:5])
