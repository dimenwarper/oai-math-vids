from pathlib import Path

import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(Path(__file__).parent / "data" / "v23.npz")
VIAZ = "[Viazovska](/vjɑzˈɔfskə/)"
SAND = "[Sandier](/sɑndjˈA/)"
SERF = "[Serfaty](/sɛɹfɑtˈi/)"
BRAU = "[Brauchart](/bɹˈWkɑɹt/)"
BET = "[Bétermin](/bAtɛɹmˈæn/)"
ENN = "[Ennola](/ˈɛnoʊlə/)"
DIAN = "[Diananda](/diənˈɑndə/)"
B = np.sqrt(3) / 2


def tri_points(R, scale, center):
    pts = []
    for j in range(-12, 13):
        for k in range(-12, 13):
            p = np.array([j + k / 2, k * B]) / np.sqrt(B)
            if np.hypot(*p) <= R:
                pts.append(center + scale * np.array([p[0], p[1], 0]))
    return pts


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "090", r"Universal Optimality of the Triangular Lattice",
                          r"Optimal for every completely monotone energy in the plane")
        with self.say("What is the best way to arrange repelling particles in the plane?"):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ simulation
        F = D["frames"]
        W, H = D["box"]
        sc = 0.44
        corner = LEFT * 6.3 + DOWN * 2.85
        box = Rectangle(width=W * sc, height=H * sc, color=GREY_B).move_to(corner + np.array([W * sc / 2, H * sc / 2, 0]))
        # unwrap the trajectory so interpolation never jumps across the periodic box
        U = F.copy()
        for t in range(1, len(U)):
            d = U[t] - U[t - 1]
            U[t, :, 0] -= W * np.round(d[:, 0] / W)
            U[t, :, 1] -= H * np.round(d[:, 1] / H)
        tt = ValueTracker(0)

        def pos(i):
            x = tt.get_value() * (len(U) - 1)
            a = int(min(np.floor(x), len(U) - 2))
            f = x - a
            p = U[a, i] * (1 - f) + U[a + 1, i] * f
            return corner + sc * np.array([p[0] % W, p[1] % H, 0])

        dots = VGroup(*[Dot(pos(i), radius=0.065, color=BLUE_3B) for i in range(F.shape[1])])
        for i, d in enumerate(dots):
            d.add_updater(lambda m, i=i: m.move_to(pos(i)))
        en = D["energies"]
        elab = Tex(r"energy per particle:", font_size=30).next_to(box, UP, buff=0.2).align_to(box, LEFT)
        eval_ = DecimalNumber(en[0], num_decimal_places=4, font_size=30).next_to(elab, RIGHT, buff=0.15)
        eval_.add_updater(lambda m: m.set_value(en[int(round(tt.get_value() * (len(en) - 1)))]))
        tc = RIGHT * 3.6 + DOWN * 0.3
        tri = VGroup(*[Dot(p, radius=0.065, color=YELLOW_3B) for p in tri_points(5.6, sc, tc)])
        hexa = RegularPolygon(6, color=TEAL_3B, stroke_width=3).scale(sc / np.sqrt(B)).move_to(tc)
        tlab = Tex(r"triangular lattice: $0.1596$", font_size=30, color=YELLOW_3B).next_to(tri, UP, buff=0.25)
        glab = Tex(r"Gaussian repulsion $g(r^2)=e^{-\pi r^2}$, density one", font_size=28, color=GREY_A).to_edge(
            DOWN, buff=0.25).shift(RIGHT * 2.9)
        with self.say("Scatter a hundred and twenty particles in a box that wraps around at the edges, and let them "
                      "push each other apart with a Gaussian force. {go}As they settle, a pattern emerges: mostly "
                      "hexagonal, with a few defects. {tri}The perfect version is the triangular lattice, where every "
                      "particle has six nearest neighbours. Its energy per particle is a little lower than what our "
                      "simulation reached.") as s:
            self.play(Create(box), FadeIn(dots), FadeIn(elab), FadeIn(eval_), FadeIn(glab))
            s.wait_until("go")
            self.play(tt.animate.set_value(1), run_time=8, rate_func=linear)
            s.wait_until("tri")
            self.play(FadeIn(tri, lag_ratio=0.01), FadeIn(tlab), run_time=1.5)
            self.play(Create(hexa))
        for d in dots:
            d.clear_updaters()
        eval_.clear_updaters()
        self.play(FadeOut(VGroup(box, dots, elab, eval_, tri, hexa, tlab, glab)))

        # ------------------------------------------------------------ energy definition and comparison
        edef = MathTex(r"E_g(C)=\liminf_{R\to\infty}\frac1{N_R}\sum_{\substack{x\neq y\\ x,y\in C\cap B_R}} g(|x-y|^2)",
                       font_size=40).to_edge(UP, buff=0.4)
        al = D["alphas"]
        i1 = int(np.argmin(np.abs(al - 1.0)))
        vals = [D["Et"][i1], D["Es"][i1], D["Eh"][i1], float(D["E_final"])]
        names = ["triangular", "square", "honeycomb", "simulation"]
        cols = [YELLOW_3B, BLUE_3B, PURPLE_3B, TEAL_3B]
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 0.3, 0.05], x_length=6.5, y_length=4.0, tips=False,
                  axis_config={"color": GREY_B, "font_size": 24},
                  y_axis_config={"numbers_to_include": [0.05, 0.1, 0.15, 0.2, 0.25, 0.3],
                                 "decimal_number_config": {"num_decimal_places": 2}}).shift(LEFT * 2.6 + DOWN * 1.0)
        bars = VGroup(*[Rectangle(width=0.9, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0).set_fill(c, 0.85)
                        .move_to(ax.c2p(k + 0.5, 0), aligned_edge=DOWN) for k, (v, c) in enumerate(zip(vals, cols))])
        bl = VGroup(*[Tex(n, font_size=24).next_to(ax.c2p(k + 0.5, 0), DOWN, buff=0.15) for k, n in enumerate(names)])
        bv = VGroup(*[DecimalNumber(v, num_decimal_places=4, font_size=24).next_to(b, UP, buff=0.1)
                      for v, b in zip(vals, bars)])
        ax2 = Axes(x_range=[0.3, 3, 0.5], y_range=[1, 2.6, 0.5], x_length=5.0, y_length=3.6, tips=False,
                   axis_config={"color": GREY_B, "font_size": 24},
                   x_axis_config={"numbers_to_include": [0.5, 1, 1.5, 2, 2.5, 3],
                                  "decimal_number_config": {"num_decimal_places": 1}},
                   y_axis_config={"numbers_to_include": [1, 1.5, 2, 2.5],
                                  "decimal_number_config": {"num_decimal_places": 1}}).shift(RIGHT * 3.9 + DOWN * 0.8)
        r_sq = VMobject(color=BLUE_3B, stroke_width=4).set_points_smoothly(
            [ax2.c2p(a, v) for a, v in zip(al, D["Es"] / D["Et"])])
        hm = D["Eh"] / D["Et"]
        keep = hm < 2.6
        r_hc = VMobject(color=PURPLE_3B, stroke_width=4).set_points_smoothly(
            [ax2.c2p(a, v) for a, v in zip(al[keep], hm[keep])])
        one = DashedLine(ax2.c2p(0.3, 1), ax2.c2p(3, 1), color=YELLOW_3B)
        x2 = MathTex(r"\alpha", font_size=30).next_to(ax2.x_axis, DOWN, buff=0.4)
        y2 = Tex(r"energy relative to triangular, $g=e^{-\pi\alpha r^2}$", font_size=26).next_to(ax2, UP, buff=0.2)
        l_sq = Tex("square", font_size=24, color=BLUE_3B).move_to(ax2.c2p(2.6, 2.1))
        l_hc = Tex("honeycomb", font_size=24, color=PURPLE_3B).move_to(ax2.c2p(1.05, 2.3))
        with self.say("Energy per particle means: add up g of the squared distance over all pairs, and divide by the "
                      "number of particles. {bar}At the same density, the triangular lattice beats the square "
                      "lattice, the honeycomb, and our simulation. {cur}And for every Gaussian width alpha we tried, "
                      "the triangular lattice wins. {q}Universal optimality asks for much more: is the triangular "
                      "lattice the minimizer for every reasonable repulsive interaction, against every "
                      "configuration, periodic or not?") as s:
            self.play(Write(edef), run_time=2)
            s.wait_until("bar")
            self.play(Create(ax), FadeIn(bl))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), FadeIn(bv), run_time=2)
            s.wait_until("cur")
            self.play(Create(ax2), FadeIn(x2), FadeIn(y2), Create(one))
            self.play(Create(r_sq), Create(r_hc), FadeIn(l_sq), FadeIn(l_hc), run_time=2)
        self.play(FadeOut(VGroup(edef, ax, bars, bl, bv, ax2, r_sq, r_hc, one, x2, y2, l_sq, l_hc)))

        # ------------------------------------------------------------ history
        hist = VGroup(
            Tex(r"\textbf{Among lattices:} Rankin (1953), Cassels, Ennola, Diananda: inverse powers", font_size=32),
            Tex(r"Montgomery (1988): every Gaussian", font_size=32),
            Tex(r"\textbf{Against everything:} Cohn--Kumar conjecture (2007):", font_size=32, color=YELLOW_3B),
            Tex(r"triangular lattice, $E_8$, Leech lattice are universally optimal", font_size=32, color=YELLOW_3B),
            Tex(r"$E_8$ and Leech: Cohn, Kumar, Miller, Radchenko, Viazovska (2022)", font_size=32),
            Tex(r"plane: only restricted competitor classes so far", font_size=32, color=GREY_A),
        ).arrange(DOWN, buff=0.3)
        hist[2:].shift(DOWN * 0.3)
        hist[4:].shift(DOWN * 0.2)
        with self.say(f"Among lattices alone, the answer has long been known: Rankin in 1953, then Cassels, {ENN} and "
                      f"{DIAN} for inverse power laws, {{mo}}and Montgomery in 1988 for every Gaussian. "
                      "{ck}Beating every non lattice configuration is far harder. In 2007, Cohn and Kumar conjectured "
                      "universal optimality for three special arrangements: the triangular lattice, the E8 lattice "
                      f"in eight dimensions, and the Leech lattice in twenty four. {{e8}}Cohn, Kumar, Miller, "
                      f"Radchenko and {VIAZ} proved the E8 and Leech cases. {{pl}}In the plane, only restricted "
                      "versions were known.") as s:
            self.play(FadeIn(hist[0]))
            s.wait_until("mo")
            self.play(FadeIn(hist[1]))
            s.wait_until("ck")
            self.play(FadeIn(hist[2:4]))
            s.wait_until("e8")
            self.play(FadeIn(hist[4]))
            s.wait_until("pl")
            self.play(FadeIn(hist[5]))
        self.play(FadeOut(hist))

        # ------------------------------------------------------------ theorem
        thm = VGroup(
            Tex(r"\textbf{Theorem.} Let $g\ge0$ be completely monotone: $(-1)^k g^{(k)}\ge 0$ for all $k$.",
                font_size=36),
            Tex(r"For every locally finite planar configuration $C$ of density one,", font_size=36),
            MathTex(r"E_g(C)\ \ge\ \sum_{a\in A\setminus\{0\}} g(|a|^2)\ =\ E_g(A),", font_size=42),
            Tex(r"$A$ = triangular lattice. Includes $e^{-\pi\alpha r^2}$ and $r^{-2p}$, even infinite energies.",
                font_size=30, color=GREY_A),
        ).arrange(DOWN, buff=0.3)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3))
        with self.say("Manuscripts in OpenAI's math catalogue, produced by an OpenAI model and not yet peer "
                      "reviewed, claim the planar case. Take any interaction g of squared distance that is "
                      "completely monotone, meaning its derivatives alternate in sign forever. Then every "
                      "configuration of density one has energy at least that of the triangular lattice. This covers "
                      "every Gaussian and every inverse power law, even when the energies are infinite.") as s:
            self.play(FadeIn(tb), run_time=2.5)
        self.play(FadeOut(tb))

        # ------------------------------------------------------------ step 1: mixtures of Gaussians
        hdr = Tex("Step 1: every completely monotone $g$ is a positive mixture of Gaussians", font_size=34,
                  color=YELLOW_3B).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 3, 1], x_length=7.5, y_length=4.4, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": True, "font_size": 24}).shift(LEFT * 1.6 + DOWN * 0.7)
        target = ax.plot(lambda t: 1 / t, x_range=[1 / 3, 4], color=YELLOW_3B, stroke_width=5)
        us = np.geomspace(0.05, 40, 14)
        du = np.gradient(us)
        comps = VGroup(*[ax.plot(lambda t, u=u, w=w: w * np.exp(-u * t),
                                 x_range=[max(0.02, np.log(w / 2.95) / u) if w > 2.95 else 0.0, 4, 0.01],
                                 color=BLUE_3B, stroke_width=2, stroke_opacity=0.7, use_smoothing=False)
                         for u, w in zip(us, du)])
        summ = ax.plot(lambda t: sum(w * np.exp(-u * t) for u, w in zip(us, du)), x_range=[0.36, 4, 0.01],
                       color=TEAL_3B, stroke_width=4, use_smoothing=False)
        tl = MathTex(r"g(t)=\frac1t=\int_0^\infty e^{-ut}\,du", font_size=36, color=YELLOW_3B).move_to(RIGHT * 4.3 + UP * 1.2)
        cl = Tex(r"weighted Gaussians\\ $e^{-u|x|^2}$ (blue), their sum (teal)", font_size=28).move_to(RIGHT * 4.3 + DOWN * 0.6)
        xl = MathTex(r"t=|x|^2", font_size=28).next_to(ax.x_axis, DOWN, buff=0.4)
        with self.say("How does the proof go? {mix}Step one is classical. By a theorem of Bernstein, every completely "
                      "monotone function is a positive mixture of decaying exponentials, which, in the squared "
                      "distance, are Gaussians. {sum}So if the triangular lattice wins for every single Gaussian, it "
                      "wins for every mixture.") as s:
            self.play(Write(hdr))
            s.wait_until("mix")
            self.play(Create(ax), FadeIn(xl), Create(target), FadeIn(tl))
            self.play(LaggedStart(*[Create(c) for c in comps], lag_ratio=0.1), FadeIn(cl), run_time=2)
            s.wait_until("sum")
            self.play(Create(summ), run_time=1.5)
        self.play(FadeOut(VGroup(hdr, ax, target, comps, summ, tl, cl, xl)))

        # ------------------------------------------------------------ step 2: magic auxiliary function
        hdr = Tex(r"Step 2: for each Gaussian $G$, an auxiliary function $f$", font_size=34, color=YELLOW_3B).to_edge(
            UP, buff=0.35)
        conds = VGroup(
            MathTex(r"f\le G", font_size=36), MathTex(r"\widehat f\ge0", font_size=36),
            MathTex(r"f(a)=G(a),\ a\in A\setminus\{0\}", font_size=36),
            MathTex(r"\widehat f(w)=0,\ w\in A^*\setminus\{0\}", font_size=36),
        ).arrange_in_grid(2, 2, buff=(0.8, 0.25)).next_to(hdr, DOWN, buff=0.3)
        chain = MathTex(r"E_G(C)\ \ge\ \tfrac1N\sum_{x\neq y}f(x-y)\ \ge\ \widehat f(0)-f(0)", r"\ =\ E_G(A)",
                        font_size=40).next_to(conds, DOWN, buff=0.35)
        why = VGroup(
            Tex(r"$\sum_{x,y}f(x-y)=\int\widehat f(\xi)\,\big|\sum_x e^{2\pi i x\cdot\xi}\big|^2d\xi$: keep only $\xi\approx0$",
                font_size=28, color=GREY_A),
            Tex(r"equality for $A$: Poisson summation", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.15).next_to(
            chain, DOWN, buff=0.25)
        nodes = [1, 3, 4, 7, 9, 12, 13, 15]
        shells = set(int(round(v)) for v in D["shells"])

        def prod0(s):
            return np.prod([np.sin(np.pi * (s - l) / 12) ** 2 for l in (0, 1, 3, 4, 7, 9)], axis=0)

        pmax = prod0(np.linspace(0, 12, 2401)).max()

        def prod(s):
            return prod0(s) / pmax

        axl = Axes(x_range=[0, 15.5, 1], y_range=[0, 1.15, 0.5], x_length=5.8, y_length=2.4, tips=False,
                   axis_config={"color": GREY_B}).move_to(LEFT * 3.4 + DOWN * 1.9)
        axr = axl.copy().move_to(RIGHT * 3.4 + DOWN * 1.9)
        ratio = axl.plot(lambda s: 1 - 0.6 * prod(s) * np.exp(-0.04 * s), x_range=[0.4, 15.5, 0.02], color=TEAL_3B,
                         stroke_width=3)
        lvl = DashedLine(axl.c2p(0, 1), axl.c2p(15.5, 1), color=YELLOW_3B, stroke_width=2)
        fh = axr.plot(lambda s: 0.9 * prod(s) * np.exp(-0.06 * s), x_range=[0.4, 15.5, 0.02], color=ORANGE_3B,
                      stroke_width=3)
        nd_l = VGroup(*[Dot(axl.c2p(n, 1), radius=0.05, color=YELLOW_3B if n in shells else GREY_A) for n in nodes])
        nd_r = VGroup(*[Dot(axr.c2p(n, 0), radius=0.05, color=YELLOW_3B if n in shells else GREY_A) for n in nodes])
        ll = Tex(r"$f/G\le1$, touching $1$ at the nodes (schematic)", font_size=28).next_to(axl, UP, buff=0.15)
        lr = Tex(r"$\widehat f\ge0$, double zeros at the nodes (schematic)", font_size=28).next_to(axr, UP, buff=0.15)
        sl = Tex(r"squared radius $s=\tfrac{\sqrt3}{2}|x|^2$; yellow: lattice shells, grey: extra node", font_size=26,
                 color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.say("Step two is the heart of the matter. For each Gaussian G, find an auxiliary function f, "
                      "following the linear programming method of Cohn and Elkies, and Cohn and Kumar. "
                      "{c}It must stay below G, its Fourier transform must never be negative, it must touch G at every "
                      "lattice point, and its transform must vanish at every point of the dual lattice. "
                      "{ch}Given such an f, a short Fourier argument shows that any configuration at all has energy "
                      "at least f hat of zero minus f of zero. {eq}And Poisson summation shows the triangular lattice "
                      "attains exactly that. {pl}So everything hinges on constructing f, with infinitely many exact "
                      "contacts and signs holding everywhere in between.") as s:
            self.play(Write(hdr))
            s.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c) for c in conds], lag_ratio=0.5), run_time=3)
            s.wait_until("ch")
            self.play(Write(chain[0]), FadeIn(why[0]), run_time=2)
            s.wait_until("eq")
            self.play(Write(chain[1]), FadeIn(why[1]))
            s.wait_until("pl")
            self.play(FadeOut(VGroup(chain, why)))
            self.play(Create(axl), Create(axr), Create(lvl), FadeIn(ll), FadeIn(lr), FadeIn(sl))
            self.play(Create(ratio), Create(fh), FadeIn(nd_l), FadeIn(nd_r), run_time=2)
        self.play(FadeOut(VGroup(hdr, conds, axl, axr, ratio, lvl, fh, nd_l, nd_r, ll, lr, sl)))

        # ------------------------------------------------------------ step 3: the shells and the construction
        hdr = Tex("Step 3: building $f$ by interpolation at the lattice shells", font_size=34, color=YELLOW_3B).to_edge(
            UP, buff=0.35)
        lc = LEFT * 3.6 + DOWN * 0.5
        lsc = 0.62
        latt = VGroup(*[Dot(p, radius=0.06, color=YELLOW_3B) for p in tri_points(4.2, lsc, lc)])
        rings = VGroup()
        for sv in [1, 3, 4, 7]:
            r = np.sqrt(sv / B) * lsc
            rings.add(Circle(radius=r, color=TEAL_3B, stroke_width=2, stroke_opacity=0.7).move_to(lc))
        rlab = VGroup(*[MathTex(str(sv), font_size=24, color=TEAL_3B).move_to(
            lc + np.sqrt(sv / B) * lsc * np.array([np.cos(0.95), np.sin(0.95), 0]) + np.array([0.12, 0.12, 0]))
            for sv in [1, 3, 4, 7]])
        dual = latt.copy().set_color(RED_3B).set_opacity(0.8)
        dl = Tex(r"dual lattice $A^*$ = $A$ turned $90^\circ$", font_size=28, color=RED_3B).move_to(lc + DOWN * 2.95)
        rows = VGroup(
            MathTex(r"s=j^2+j\ell+\ell^2=1,3,4,7,9,12,13,\dots", font_size=34),
            Tex(r"mod 3: $\equiv(j-\ell)^2\in\{0,1\}$; even only if $j,\ell$ even", font_size=28),
            Tex(r"$\Rightarrow$ every shell lies in $12\mathbb{Z}+\{0,1,3,4,7,9\}$", font_size=30, color=YELLOW_3B),
            Tex(r"$\bullet$ squared-sine product: double zero at every node", font_size=28),
            Tex(r"$\bullet$ pole terms prescribe value and slope at each node", font_size=28),
            Tex(r"$\bullet$ finite blocks certified by interval arithmetic,", font_size=28),
            Tex(r"\quad infinite tail by a convergent series", font_size=28),
            Tex(r"$\bullet$ signs between nodes: Bernstein-polynomial bounds", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT * 3.0 + DOWN * 0.4)
        with self.say("Here is how the manuscripts build it. {sh}Measure squared distance in units where the lattice "
                      "shells are the numbers j squared plus j l plus l squared: one, three, four, seven, nine, and "
                      "so on. {du}The dual lattice is just the lattice turned by a right angle, so both sides of the "
                      "Fourier transform see the same shells. {m}Looking mod three and mod two shows that every shell "
                      "falls into six residue classes mod twelve. {sin}A product of squared sines then has a double "
                      "zero at every one of them, and extra pole terms prescribe the value and the slope at each "
                      "node. {cert}A finite block of these equations is solved and certified with rigorous interval "
                      "arithmetic, the infinite tail is handled by a convergent series, and the signs between nodes "
                      "are checked on whole intervals. The formalized companion manuscript does this with a mod "
                      "thirty six version and two twenty by twenty blocks.") as s:
            self.play(Write(hdr))
            s.wait_until("sh")
            self.play(FadeIn(latt, lag_ratio=0.01), run_time=1.5)
            self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.3), FadeIn(rlab), FadeIn(rows[0]), run_time=2)
            s.wait_until("du")
            self.play(Rotate(dual, PI / 2, about_point=lc), FadeIn(dl), run_time=2)
            s.wait_until("m")
            self.play(FadeIn(rows[1]))
            self.play(FadeIn(rows[2]))
            s.wait_until("sin")
            self.play(FadeIn(rows[3:5]))
            s.wait_until("cert")
            self.play(FadeIn(rows[5:]))
        self.play(FadeOut(VGroup(hdr, latt, rings, rlab, dual, dl, rows)))

        # ------------------------------------------------------------ corollaries
        cor = VGroup(
            Tex(r"Heat-kernel comparison (after Petrache--Serfaty) gives long-range energies:", font_size=32),
            Tex(r"$\bullet$ Riesz $|x|^{-s}$, $0<s<2$: renormalized and jellium minima are triangular", font_size=32),
            Tex(r"$\bullet$ Coulomb $-\log|x|$: the Sandier--Serfaty conjecture", font_size=32),
            Tex(r"$\bullet$ with B\'etermin--Sandier: the Brauchart--Hardin--Saff conjecture", font_size=32),
            Tex(r"\quad (linear term of the optimal log energy of $n$ points on $S^2$)", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        with self.say("Gaussians also unlock the long range interactions, through heat kernel identities, following "
                      f"Petrache and {SERF}. {{r}}The manuscripts deduce that the triangular lattice minimizes "
                      "renormalized Riesz energies for exponents between zero and two, {c}and the Coulomb energy of "
                      f"the plane, settling a conjecture of {SAND} and {SERF}. {{s}}Combined with a formula of "
                      f"{BET} and {SAND}, this settles the {BRAU}, Hardin, Saff conjecture for the linear term in the "
                      "optimal logarithmic energy of many points on a sphere.") as s:
            self.play(FadeIn(cor[0]))
            s.wait_until("r")
            self.play(FadeIn(cor[1]))
            s.wait_until("c")
            self.play(FadeIn(cor[2]))
            s.wait_until("s")
            self.play(FadeIn(cor[3:]))
        self.play(FadeOut(cor))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Triangular lattice minimizes every completely monotone energy in the plane",
             r"Riesz ($0<s<2$) and Coulomb corollaries: \emph{not} formalized",
             r"Manuscripts produced by an OpenAI model (31, 70 and 49 pages)"],
            True, r"\emph{An atomic certificate for triangular-lattice universal optimality} (Sept.\ 2026)")
        with self.say("The universal optimality theorem, with its Gaussian auxiliary functions, has been formalized "
                      "in the Lean proof assistant, as has a companion result: the Cohn Elkies bound is sharp for "
                      "circle packing in the plane. {c}The Riesz and Coulomb corollaries have not been formalized, "
                      "and still await expert checking.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("c")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
