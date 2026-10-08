import numpy as np
from manim import *

from style import *
from vo import NarratedScene

TUK = "[Tukia](/tˈukiə/)"
GAB = "[Gabai](/ɡəbˈI/)"
JUN = "[Jungreis](/jˈʌŋɡɹIs/)"
KLE = "[Kleiner](/klˈInəɹ/)"
GRO = "[Gromov](/ɡɹˈOmɑf/)"
HOL = "[Hölder](/hˈɜldəɹ/)"

D = np.load("videos/data/v37.npz")
POLYS, PAR = D["polys"], D["par"]
G, LOGG = D["G"], D["L"]
_w, _V = np.linalg.eig(LOGG)
_Vi = np.linalg.inv(_V)


def mob_t(t):
    """G^t = exp(t log G), an element of the one-parameter group through G."""
    return _V @ np.diag(np.exp(t * _w)) @ _Vi


def to_pts(z, center, rad):
    return np.stack([center[0] + rad * z.real, center[1] + rad * z.imag, np.zeros(len(z))], axis=1)


VIS = 0.97  # tiles reaching beyond this radius are drawn invisible (keeps a uniform rim)


def tile_op(a, zmax):
    return 0.0 if zmax > VIS else (0.75 if a else 0.9)


def tiling(center, rad, polys=POLYS, par=PAR, stroke=0.0, keep_hidden=False):
    g = VGroup()
    for z, a in zip(polys, par):
        zmax = np.max(np.abs(z))
        if zmax > VIS and not keep_hidden:
            continue
        m = VMobject(stroke_color=GREY_A, stroke_width=stroke, stroke_opacity=0.5)
        m.set_points_as_corners(to_pts(np.append(z, z[0]), center, rad))
        m.set_fill(BLUE_3B if a else "#123540", opacity=tile_op(a, zmax))
        m.zorig = np.append(z, z[0])
        m.par = a
        g.add(m)
    return g


def sphere(center, rad, color=TEAL_3B):
    c = np.array(center)
    g = VGroup(Circle(radius=rad, color=color, stroke_width=3).move_to(c))
    for k in (0.3, 0.65):
        g.add(Ellipse(width=2 * rad, height=2 * rad * k, color=color, stroke_width=1.5, stroke_opacity=0.6).move_to(c))
        g.add(Ellipse(width=2 * rad * k, height=2 * rad, color=color, stroke_width=1.5, stroke_opacity=0.6).move_to(c))
    return g


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "246", r"Cannon's Conjecture",
                          r"Groups with a 2-sphere at infinity act on hyperbolic 3-space")
        with self.say("Cannon's conjecture."):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ hook: the tiled hyperbolic plane
        C0, RD = np.array([0, -0.15, 0]), 3.45
        til = tiling(C0, RD)
        rim = Circle(radius=RD, color=YELLOW_3B, stroke_width=5).move_to(C0)
        tri = Tex(r"angles $\tfrac{\pi}{2},\ \tfrac{\pi}{3},\ \tfrac{\pi}{7}$", font_size=32).to_corner(UL, buff=0.5)
        grp = Tex(r"reflections in the sides\\ generate a group", font_size=32).next_to(tri, DOWN, buff=0.3,
                                                                                       aligned_edge=LEFT)
        bl = Tex(r"boundary at\\ infinity: a circle", font_size=32, color=YELLOW_3B).to_corner(UR, buff=0.5)
        with self.say("This is the hyperbolic plane, drawn as a disk and tiled by copies of a single triangle, with "
                      "angles a half, a third and a seventh of pi. {g}Reflections in the triangle's sides generate a "
                      "group, which shuffles the tiles among themselves. Every tile is the same size; they only look "
                      "smaller near the edge. {b}Seen from far away, this group looks like the plane itself, and "
                      "what lies at infinity is this circle: the group's boundary.") as s:
            self.play(FadeIn(til), run_time=2.5)
            self.play(FadeIn(tri))
            s.wait_until("g")
            self.play(FadeIn(grp))
            s.wait_until("b")
            self.play(Create(rim), FadeIn(bl), run_time=1.5)
        self.play(FadeOut(VGroup(til, rim, tri, grp, bl)))

        # ------------------------------------------------------------ hyperbolic groups and their boundaries
        hdr = Tex(r"Hyperbolic groups (Gromov): Cayley graphs with uniformly thin triangles", font_size=36,
                  color=YELLOW_3B).to_edge(UP, buff=0.4)
        # panel 1: tree with Cantor-set boundary
        c1 = np.array([-4.6, 0.2, 0])
        tr = VGroup()
        ends = []
        pts = {(): c1}
        frontier = [((), None)]
        dirs = [RIGHT, UP, LEFT, DOWN]
        for d in range(4):
            Lh = 0.95 * 0.5**d
            nf = []
            for node, back in frontier:
                for k, dv in enumerate(dirs):
                    if back is not None and k == (back + 2) % 4:
                        continue
                    ch = node + (k,)
                    pts[ch] = pts[node] + dv * Lh
                    tr.add(Line(pts[node], pts[ch], color=GREY_B, stroke_width=2.2 - 0.4 * d))
                    nf.append((ch, k))
                    if d == 3:
                        ends.append(pts[ch])
            frontier = nf
        cant = VGroup(*[Dot(e, radius=0.035, color=RED_3B) for e in ends])
        t1 = Tex(r"free group\\ boundary: Cantor set", font_size=28).next_to(tr, DOWN, buff=0.35)
        # panel 2: small tiled disk
        c2 = np.array([0, 0.2, 0])
        small = tiling(c2, 1.75)
        rim2 = Circle(radius=1.75, color=YELLOW_3B, stroke_width=3).move_to(c2)
        t2 = Tex(r"surface group\\ boundary: circle", font_size=28).next_to(rim2, DOWN, buff=0.35)
        # panel 3: sphere
        c3 = np.array([4.6, 0.2, 0])
        sph = sphere(c3, 1.75)
        t3 = Tex(r"hyperbolic 3-manifold\\ boundary: 2-sphere", font_size=28).next_to(sph, DOWN, buff=0.35)
        VGroup(t1, t2, t3).set_y(min(t1.get_y(), t2.get_y(), t3.get_y()))
        def geo_arc(t1, t2, center, rad, n=80):
            """Geodesic between ideal points e^{i t1}, e^{i t2} of the disk: arc of the orthogonal circle."""
            dt = (t2 - t1 + PI) % TAU - PI
            m = t1 + dt / 2
            h = abs(dt) / 2
            cc_ = np.exp(1j * m) / np.cos(h)
            rr = np.tan(h)
            a0, a1 = np.angle(np.exp(1j * t1) - cc_), np.angle(np.exp(1j * t2) - cc_)
            dd = (a1 - a0 + np.pi) % TAU - np.pi
            z = cc_ + rr * np.exp(1j * (a0 + dd * np.linspace(0, 1, n)))
            return VMobject(color=ORANGE_3B, stroke_width=4).set_points_smoothly(to_pts(z, center, rad))

        ideal_rim = Circle(radius=1.75, color=GREY_B, stroke_width=2).move_to(c2)
        angs = [PI / 2, PI / 2 + TAU / 3, PI / 2 + 2 * TAU / 3]
        ideal = VGroup(*[geo_arc(angs[i], angs[(i + 1) % 3], c2, 1.75) for i in range(3)])
        thin = Tex(r"a geodesic triangle:\\ every side stays close\\ to the other two", font_size=28,
                   color=ORANGE_3B).next_to(ideal_rim, RIGHT, buff=0.5)
        with self.say(f"In the nineteen-eighties, {GRO} singled out the groups that look negatively curved like "
                      "this: in their Cayley graphs, geodesic triangles are uniformly thin. Every such hyperbolic "
                      "group has a boundary at infinity. {f}For a free group, whose picture is a tree, the boundary "
                      "is a Cantor set. {s}For the group of a closed surface, it is a circle. {m}And for the group "
                      "of a closed hyperbolic three-manifold, it is a two-dimensional sphere.") as s:
            self.play(Write(hdr), run_time=1.5)
            self.play(Create(ideal_rim), Create(ideal), FadeIn(thin), run_time=2)
            s.wait_until("f")
            self.play(FadeOut(thin))
            self.play(Create(tr), run_time=1.5)
            self.play(FadeIn(cant), FadeIn(t1))
            s.wait_until("s")
            self.play(FadeOut(ideal), FadeOut(ideal_rim), FadeIn(small), Create(rim2), FadeIn(t2), run_time=1.5)
            s.wait_until("m")
            self.play(Create(sph), FadeIn(t3), run_time=1.5)
        self.play(FadeOut(VGroup(tr, cant, t1, small, rim2, t2)), FadeOut(hdr),
                  VGroup(sph, t3).animate.move_to(LEFT * 4.3 + DOWN * 0.3))

        # ------------------------------------------------------------ the conjecture and its history
        conj = VGroup(
            Tex(r"\textbf{Cannon's conjecture}", font_size=40, color=YELLOW_3B),
            Tex(r"$G$ hyperbolic, $\partial G\cong S^2$", font_size=36),
            Tex(r"$\Longrightarrow$ $G$ acts properly and cocompactly", font_size=36),
            Tex(r"by isometries on hyperbolic 3-space $\mathbb{H}^3$", font_size=36),
        ).arrange(DOWN, buff=0.22).move_to(RIGHT * 2.3 + UP * 2.0)
        hist = VGroup(
            Tex(r"circle case $\partial G\cong S^1$: Tukia, Gabai, Casson--Jungreis", font_size=30),
            Tex(r"Cannon: combinatorial Riemann mapping theorem (1994)", font_size=30),
            Tex(r"Cannon--Swenson (1998): the conjecture stated", font_size=30),
            Tex(r"Cannon--Floyd--Parry (1999): reduction to discrete moduli", font_size=30),
            Tex(r"Bonk--Kleiner: proof when the conformal dimension is attained", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 2.3 + DOWN * 1.5)
        for h in hist:
            h.set_color(GREY_A)
        if hist.width > 8.4:
            hist.scale_to_fit_width(8.4).move_to(RIGHT * 2.3 + DOWN * 1.5)
        with self.say("Cannon's conjecture says the sphere is a fingerprint. {c}If a hyperbolic group has a "
                      "two-sphere as its boundary, it should act properly and co-compactly by isometries on "
                      "hyperbolic three-space. For a torsion-free group, that means it is the fundamental group of "
                      "a closed hyperbolic three-manifold: geometry recognized from the group alone. "
                      f"{{h}}The circle version was settled by the early nineteen-nineties, by {TUK}, {GAB}, and Casson and "
                      f"{JUN}. {{cf}}For the sphere, Cannon's combinatorial Riemann mapping theorem, and his work "
                      f"with Swenson, Floyd and Parry, turned the problem into analysis. {{bk}}Bonk and {KLE} proved "
                      "it under an extra hypothesis. The general case stayed open.") as s:
            s.wait_until("c")
            self.play(FadeIn(conj[0]), FadeIn(conj[1]))
            self.play(FadeIn(conj[2:]))
            s.wait_until("h")
            self.play(FadeIn(hist[0]))
            s.wait_until("cf")
            self.play(FadeIn(hist[1:4]), run_time=1.5)
            s.wait_until("bk")
            self.play(FadeIn(hist[4]))
        self.play(FadeOut(VGroup(sph, t3, conj, hist)))

        thm = VGroup(Tex(r"\textbf{Theorem.} Every hyperbolic group $G$ with $\partial G\cong S^2$ admits", font_size=38),
                     Tex(r"a proper, cocompact, isometric action on $\mathbb{H}^3$ with finite kernel.", font_size=38)
                     ).arrange(DOWN, buff=0.2)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3)).shift(UP * 0.8)
        cor = Tex(r"Torsion-free $\Rightarrow$ $G=\pi_1$ of a closed hyperbolic 3-manifold", font_size=34,
                  color=TEAL_3B).next_to(tb, DOWN, buff=0.5)
        with self.say("A thirty-one page manuscript in OpenAI's math catalogue, not yet peer reviewed, claims to "
                      "prove it. {t}Every hyperbolic group whose boundary is a two-sphere acts properly and "
                      "co-compactly by isometries on hyperbolic three-space, with finite kernel. {c}In particular, "
                      "every torsion-free one is the fundamental group of a closed hyperbolic three-manifold.") as s:
            s.wait_until("t")
            self.play(Write(tb), run_time=2.5)
            s.wait_until("c")
            self.play(FadeIn(cor))
        self.play(FadeOut(VGroup(tb, cor)))

        # ------------------------------------------------------------ the modulus criterion
        hdr = Tex(r"The criterion: bounded combinatorial modulus", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.35)
        S = 4.2
        sq_c = np.array([-3.4, -0.5, 0])

        def grid_panel(n):
            g = VGroup()
            curve_f = lambda x: 0.18 * np.sin(2.2 * np.pi * x + 0.6) + 0.08 * np.sin(5.1 * x) + 0.47
            hit = set()
            for x in np.linspace(0, 0.9999, 600):
                hit.add((int(x * n), int(curve_f(x) * n)))
            for i in range(n):
                for j in range(n):
                    r = Square(S / n, stroke_width=1, stroke_color=GREY_D).move_to(
                        sq_c + np.array([(i + 0.5) * S / n - S / 2, (j + 0.5) * S / n - S / 2, 0]))
                    if (i, j) in hit:
                        r.set_fill(ORANGE_3B, 0.55)
                    g.add(r)
            xs = np.linspace(0, 1, 120)
            cur = VMobject(color=YELLOW_3B, stroke_width=4).set_points_smoothly(
                [sq_c + np.array([x * S - S / 2, curve_f(x) * S - S / 2, 0]) for x in xs])
            return VGroup(g, cur)

        defs = VGroup(
            Tex(r"cover the sphere by $\sim$ balls of size $a^{-n}$", font_size=30),
            Tex(r"weights $w\ge0$: every curve of diameter $\ge d_0$", font_size=30),
            Tex(r"meets total weight $\ge1$", font_size=30),
            MathTex(r"M(n)=\min\sum w^2", font_size=40, color=YELLOW_3B),
        ).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.3 + UP * 1.6)
        flat = MathTex(r"\text{flat square: } w=\tfrac1n,\ \ \sum w^2=n^2\cdot\tfrac{1}{n^2}=1", font_size=34
                       ).move_to(RIGHT * 3.3 + DOWN * 0.3)
        nlab = MathTex("n=4", font_size=34).next_to(VGroup(Square(S).move_to(sq_c)), UP, buff=0.15)
        crit = VGroup(
            Tex(r"$\sup_n M(n)<\infty$ $\Rightarrow$ boundary $\approx$ round sphere", font_size=30, color=TEAL_3B),
            Tex(r"(Bonk--Kleiner, Bourdon--Kleiner)", font_size=26, color=GREY_A),
            Tex(r"$\Rightarrow$ Sullivan--Tukia straightening: action on $\mathbb{H}^3$", font_size=30, color=TEAL_3B),
        ).arrange(DOWN, buff=0.15).move_to(RIGHT * 3.3 + DOWN * 2.1)
        panel = grid_panel(4)
        with self.say("The proof follows the analytic route. {cov}Cover the boundary sphere by small balls at "
                      "scale a to the minus n. {w}Give each ball a weight, so that every curve of a fixed size "
                      "crosses total weight at least one, and let M of n be the least possible sum of squared "
                      "weights. {fl}For curves crossing a flat square, weights one over n work at every scale, and the sum stays one. "
                      "{cr}The classical criterion: if M of n stays bounded as the scale shrinks, the boundary is "
                      f"a round sphere up to controlled distortion, and Sullivan and {TUK}'s straightening then builds "
                      "the action on hyperbolic three-space.") as s:
            self.play(Write(hdr))
            s.wait_until("cov")
            self.play(FadeIn(panel[0]), FadeIn(nlab), FadeIn(defs[0]))
            s.wait_until("w")
            self.play(Create(panel[1]), FadeIn(defs[1:3]))
            self.play(Write(defs[3]))
            s.wait_until("fl")
            self.play(FadeIn(flat))
            for n in (8, 16):
                newp = grid_panel(n)
                self.play(FadeOut(panel), FadeIn(newp), Transform(nlab, MathTex(f"n={n}", font_size=34).move_to(nlab)),
                          run_time=1.0)
                panel = newp
            s.wait_until("cr")
            self.play(FadeIn(crit), run_time=1.5)
        self.play(FadeOut(VGroup(hdr, panel, nlab, defs, flat, crit)))

        # ------------------------------------------------------------ duality and the limit function
        H = D["height"]
        nh, nw = H.shape
        RW, RH = 6.3, 4.2
        rc = np.array([-3.0, -0.6, 0])
        cols = [BLUE_E, BLUE_D, BLUE_C, TEAL_D, TEAL_C, GREEN_C, YELLOW_D, YELLOW_C, ORANGE]
        cells = VGroup()
        for i in range(nh):
            for j in range(nw):
                v = H[i, j]
                band = min(len(cols) - 1, int(v * len(cols)))
                r = Rectangle(width=RW / nw, height=RH / nh, stroke_width=0).set_fill(cols[band], 0.9)
                r.move_to(rc + np.array([(j + 0.5) * RW / nw - RW / 2, RH / 2 - (i + 0.5) * RH / nh, 0]))
                cells.add(r)
        frame = Rectangle(width=RW, height=RH, color=WHITE, stroke_width=2).move_to(rc)
        top = Tex(r"top edge: height $0$", font_size=26).next_to(frame, UP, buff=0.12)
        bot = Tex(r"bottom: height $\ge 1$", font_size=26).next_to(frame, DOWN, buff=0.12)
        side = VGroup(
            Tex(r"If $M(n)\to\infty$:", font_size=32, color=YELLOW_3B),
            Tex(r"left--right crossings are\\ expensive to block, so", font_size=30),
            Tex(r"top--bottom crossings are\\ cheap: energy $\lesssim 1/M(n)$", font_size=30),
            Tex(r"height $b(x)$ = cheapest\\ weighted path from the top", font_size=30, color=TEAL_3B),
            Tex(r"level sets cut across", font_size=30, color=TEAL_3B),
            Tex(r"limit: nonconstant $u$, small-scale\\ oscillation controlled by a measure", font_size=30, color=ORANGE_3B),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.6 + DOWN * 0.3)
        note = Tex(r"illustration with random weights", font_size=22, color=GREY_B).next_to(bot, DOWN, buff=0.1)
        with self.say("So suppose, for contradiction, that M of n is unbounded. {d}A duality for crossings kicks in: "
                      "if curves crossing a rectangle from left to right are expensive to block, then curves from "
                      "top to bottom are cheap to block, with energy about one over M. {h}Turn these cheap weights "
                      "into a height: the cost of the cheapest path from the top edge to each point. {l}Its level "
                      "sets are continua that cut across the rectangle. {u}As the scale shrinks, these heights "
                      "converge to a nonconstant function u, whose oscillation on small balls is controlled by a "
                      "finite measure.") as s:
            self.play(FadeIn(side[0]))
            s.wait_until("d")
            self.play(FadeIn(side[1:3]), Create(frame))
            s.wait_until("h")
            self.play(FadeIn(cells), FadeIn(top), FadeIn(bot), FadeIn(note), FadeIn(side[3]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(side[4]))
            s.wait_until("u")
            self.play(FadeIn(side[5]))
        self.play(FadeOut(VGroup(cells, frame, top, bot, side, note)))

        # ------------------------------------------------------------ magnification by the group
        C1, R1 = np.array([-3.4, -0.05, 0]), 3.2
        til = tiling(C1, R1, keep_hidden=True)
        rim = Circle(radius=R1, color=GREY_B, stroke_width=2).move_to(C1)
        arcz = D["arc"]
        arc = VMobject(color=YELLOW_3B, stroke_width=9).set_points_smoothly(to_pts(arcz, C1, R1))
        cap = Tex(r"(shown one dimension down)", font_size=24, color=GREY_B).next_to(rim, DOWN, buff=0.08)
        txt = VGroup(
            Tex(r"group elements magnify\\ tiny balls of the boundary", font_size=32, color=YELLOW_3B),
            Tex(r"\textbf{fast growth} of $M$: $u$ is H\"older;\\ magnified limits on punctured\\ spheres "
                r"contradict each other", font_size=28),
            Tex(r"\textbf{slow growth}: a probability flow\\ on a tree of balls; overlapping\\ magnifications "
                r"overcharge small balls", font_size=28),
            Tex(r"either way: contradiction,\\ so $M(n)$ stays bounded", font_size=32, color=TEAL_3B),
        ).arrange(DOWN, buff=0.38).move_to(RIGHT * 3.7 + DOWN * 0.1)

        def mag(mob, alpha):
            M = mob_t(alpha)
            for m in mob[0]:
                z = m.zorig
                w = (M[0, 0] * z + M[0, 1]) / (M[1, 0] * z + M[1, 1])
                m.set_points_as_corners(to_pts(w, C1, R1))
                m.set_fill(opacity=tile_op(m.par, np.max(np.abs(w))))
            za = (M[0, 0] * arcz + M[0, 1]) / (M[1, 0] * arcz + M[1, 1])
            mob[1].set_points_smoothly(to_pts(za, C1, R1))

        pair = VGroup(til, arc)
        with self.say("Now the group itself enters. {m}Its elements act on the boundary, and they can magnify any "
                      "tiny ball to a macroscopic size. Here a single group element blows up a small arc of the "
                      "circle, and the tiling lands back on itself. {f}The paper splits into two cases. If the "
                      "moduli grow exponentially, u is HOLDER continuous, and magnified copies of it converge to "
                      "functions on punctured spheres; comparing magnifications at different punctures gives a "
                      "contradiction. {sl}If they grow more slowly, the "
                      "paper spreads u's variation over a tree of balls carrying a probability flow, and shows that "
                      "many overlapping magnifications would charge more mass to small balls than they can hold. "
                      "{x}Either way, a contradiction. So M of n stays bounded, the boundary is a round sphere, and "
                      "the group acts on hyperbolic three-space.".replace("HOLDER", HOL)) as s:
            self.play(FadeIn(til), Create(rim), FadeIn(cap), run_time=1.5)
            self.play(Create(arc))
            s.wait_until("m")
            self.play(FadeIn(txt[0]))
            self.play(UpdateFromAlphaFunc(pair, mag), run_time=4, rate_func=smooth)
            s.wait_until("f")
            self.play(FadeIn(txt[1]))
            s.wait_until("sl")
            self.play(FadeIn(txt[2]))
            s.wait_until("x")
            self.play(FadeIn(txt[3]))
        self.play(FadeOut(VGroup(til, arc, rim, cap, txt)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Every hyperbolic group with $\partial G\cong S^2$ acts properly, cocompactly,",
             r"\quad and isometrically on $\mathbb{H}^3$, with finite kernel",
             r"Torsion-free case: fundamental group of a closed hyperbolic 3-manifold",
             r"Manuscript: 31 pages, produced by an OpenAI model"],
            True, r"\emph{A Modulus Proof of Cannon's Conjecture} (Sept.\ 2026)")
        with self.say("The manuscript was written by an OpenAI model, {l}and its main theorem, the geometric action "
                      "on hyperbolic three-space, has been formalized in the Lean proof assistant. If it holds, a "
                      "sphere at infinity is all it takes to recognize three-dimensional hyperbolic geometry.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
