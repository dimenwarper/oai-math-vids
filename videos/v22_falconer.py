from pathlib import Path

import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(Path(__file__).parent / "data" / "v22.npz")
ERD = "[Erdős](/ˈɛɹdəʃ/)"
ERDO = "[Erdoğan](/ˈɛɹdəwɑn/)"
IOS = "[Iosevich](/joʊsˈAvɪʧ/)"
MAT = "[Mattila](/mˈɑtɪlə/)"
FROST = "[Frostman](/fɹˈɔstmən/)"


def dust_squares(stage, center, size, color=BLUE_3B, op=0.9):
    pts = np.zeros((1, 2))
    side = 1.0
    for _ in range(stage):
        side /= 3
        offs = np.array([[0, 0], [2, 0], [0, 2], [2, 2]]) * side
        pts = (pts[:, None, :] + offs[None]).reshape(-1, 2)
    g = VGroup()
    for x, y in pts + side / 2:
        g.add(Square(side * size, stroke_width=0).set_fill(color, op).move_to(
            center + size * np.array([x - 0.5, y - 0.5, 0])))
    return g


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "073", r"The Falconer Distance Conjecture",
                          r"Every dimension $d\ge2$: $\dim_H E>\tfrac d2\ \Rightarrow\ \Delta(E)$ has positive length")
        with self.say("How many distances does a fractal determine?"):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ the dust and its distances
        C = LEFT * 3.7 + UP * 0.1
        SZ = 4.6
        stages = [dust_squares(k, C, SZ) for k in range(5)]
        P = D["pts"]

        def to_scr(p):
            return C + SZ * np.array([p[0] - 0.5, p[1] - 0.5, 0])

        dlab = Tex(r"keep 4 corners, repeat:\\ dimension $\tfrac{\log 4}{\log 3}\approx1.26$", font_size=30
                   ).next_to(stages[0], DOWN, buff=0.3)
        nl = NumberLine(x_range=[0, 1.5, 0.5], length=6.0, include_numbers=False, color=GREY_B, include_tip=False
                        ).move_to(RIGHT * 3.6 + DOWN * 2.4)
        nlab = VGroup(*[MathTex(t, font_size=28).next_to(nl.n2p(v), DOWN, buff=0.15)
                        for v, t in [(0, "0"), (0.5, r"\tfrac12"), (1, "1"), (np.sqrt(2), r"\sqrt2")]])
        nll = Tex("distances", font_size=30, color=GREY_A).next_to(nl, UP, buff=2.9)
        pairs, pd = D["pairs"], D["pair_d"]
        segs = VGroup(*[Line(to_scr(P[i]), to_scr(P[j]), color=YELLOW_3B, stroke_width=1.5, stroke_opacity=0.6)
                        for i, j in pairs[:40]])
        ticks = VGroup(*[Line(nl.n2p(d) + UP * 0.12, nl.n2p(d) + DOWN * 0.12, color=YELLOW_3B, stroke_width=2)
                         for d in pd])
        bins, hist = D["bins"], D["hist"]
        hmax = np.percentile(hist[hist > 0], 97)
        bars = VGroup()
        for a, b, h in zip(bins[:-1], bins[1:], hist):
            if h == 0:
                continue
            hh = 2.3 * min(h / hmax, 1.0)
            bars.add(Rectangle(width=nl.n2p(b)[0] - nl.n2p(a)[0], height=hh, stroke_width=0).set_fill(
                BLUE_3B, 0.85).move_to(nl.n2p((a + b) / 2) + UP * (hh / 2 + 0.02)))
        hl = Tex(r"all 523{,}776 pairs of 1024 points:\\ 98\% of the 400 bins are hit", font_size=28).next_to(
            nl, UP, buff=2.45)
        rngf = np.random.default_rng(11)
        fp = [np.array([x, y, 0]) for x, y in rngf.uniform([-2.5, -1.8], [2.5, 1.8], size=(6, 2))]
        fdots = VGroup(*[Dot(p, radius=0.09, color=BLUE_3B) for p in fp])
        fsegs = VGroup(*[Line(fp[a], fp[b], color=YELLOW_3B, stroke_width=2, stroke_opacity=0.7)
                         for a in range(6) for b in range(a + 1, 6)])
        flab = Tex(r"6 points, 15 distances", font_size=32).to_edge(DOWN, buff=0.6)
        with self.say("Take a set of points, and look at every distance between two of them. That is its distance "
                      "set. {dust}Here is a fractal dust: keep the four corner squares, each a third the size, and "
                      "repeat forever. {pairs}Pick pairs of points, measure, and drop each distance onto a number "
                      "line. {hist}With all half a million pairs from this stage of the construction, the distances "
                      "spread over essentially the whole interval from zero to root two. {q}So when must the "
                      "distances of a set fill up a set of positive length?") as s:
            self.play(FadeIn(fdots))
            self.play(LaggedStart(*[Create(g) for g in fsegs], lag_ratio=0.1), FadeIn(flab), run_time=2)
            s.wait_until("dust")
            self.play(FadeOut(VGroup(fdots, fsegs, flab)), FadeIn(stages[0]))
            for k in range(1, 5):
                self.play(ReplacementTransform(stages[k - 1], stages[k]), run_time=0.8)
            self.play(FadeIn(dlab))
            s.wait_until("pairs")
            self.play(Create(nl), FadeIn(nlab))
            self.play(LaggedStart(*[Create(g) for g in segs], lag_ratio=0.08),
                      LaggedStart(*[FadeIn(t) for t in ticks[:40]], lag_ratio=0.08), run_time=3)
            self.play(FadeIn(ticks[40:], lag_ratio=0.02), run_time=1.5)
            s.wait_until("hist")
            self.play(FadeOut(segs), FadeOut(ticks), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                                                                  lag_ratio=0.003), run_time=2.5)
            self.play(FadeIn(hl))
        self.play(FadeOut(VGroup(stages[4], dlab, nl, nlab, bars, hl)))

        # ------------------------------------------------------------ Falconer's question and history
        l1 = Tex(r"Falconer (1985): in $\mathbb{R}^d$, compact $E$ with $\dim_H E>\tfrac{d+1}{2}$", font_size=34)
        l1b = Tex(r"$\Rightarrow$ the distance set $\Delta(E)=\{|x-y|:x,y\in E\}$ has positive length", font_size=34)
        l2 = Tex(r"lattice-like examples: dimension exactly $\tfrac d2$ is not enough", font_size=32, color=GREY_A)
        l3 = Tex(r"\textbf{Conjecture:} $\dim_H E>\tfrac d2$ suffices.", font_size=38, color=YELLOW_3B)
        top = VGroup(l1, l1b, l2, l3).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.5)
        l3.shift(DOWN * 0.15)
        nl = NumberLine(x_range=[1, 1.5, 0.05], length=10, include_numbers=False, color=GREY_B, include_tip=False,
                        tick_size=0.06).shift(DOWN * 2.3)
        nums = VGroup(*[MathTex(t, font_size=30).next_to(nl.n2p(v), DOWN, buff=0.18)
                        for v, t in [(1, "1"), (1.25, r"\tfrac54"), (4 / 3, r"\tfrac43"), (1.5, r"\tfrac32")]])
        pl = Tex(r"plane:", font_size=30).next_to(nl, LEFT, buff=0.3)
        mk = [(1.5, "Falconer 1985", BLUE_3B), (4 / 3, "Wolff 1999", TEAL_3B),
              (1.25, r"Guth--Iosevich--Ou--Wang", GREEN_3B)]
        marks = VGroup(*[VGroup(Dot(nl.n2p(v), color=c), Tex(t, font_size=24).next_to(nl.n2p(v), UP, buff=0.25))
                         for v, t, c in mk])
        marks[2][1].shift(LEFT * 0.6)
        goal = VGroup(Dot(nl.n2p(1), color=YELLOW_3B, radius=0.1),
                      Tex("conjecture", font_size=24, color=YELLOW_3B).next_to(nl.n2p(1), UP, buff=0.25))
        hd = Tex(r"higher $d$ (Erdo\u{g}an; Du, Zhang and coauthors; \dots): about $\tfrac d2+\tfrac14$",
                 font_size=30, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.say("Size here means Hausdorff dimension. This dust has dimension log four over log three, about "
                      "one point two six. {f}In 1985, Kenneth Falconer proved that a compact set in d dimensional "
                      "space with dimension above d plus one, over two, has distances of positive length. "
                      "{lat}His lattice-like examples show that dimension exactly d over two is not enough. "
                      "{c}He conjectured that anything above d over two suffices. "
                      f"{{nl}}In the plane, the threshold came down from three halves, {{w}}to four thirds by Wolff in "
                      f"1999, {{g}}then to five fourths by Guth, {IOS}, Ou and Wang. {{hd}}In higher dimensions, work "
                      f"of {ERDO}, Du, Zhang and others brought it to about d over two plus a quarter.") as s:
            s.wait_until("f")
            self.play(FadeIn(l1), FadeIn(l1b))
            s.wait_until("lat")
            self.play(FadeIn(l2))
            s.wait_until("c")
            self.play(Write(l3))
            s.wait_until("nl")
            self.play(Create(nl), FadeIn(nums), FadeIn(pl), FadeIn(marks[0]), FadeIn(goal))
            s.wait_until("w")
            self.play(FadeIn(marks[1]))
            s.wait_until("g")
            self.play(FadeIn(marks[2]))
            s.wait_until("hd")
            self.play(FadeIn(hd))
        self.play(FadeOut(VGroup(top, nl, nums, pl, marks, goal, hd)))

        # ------------------------------------------------------------ theorem
        thm = VGroup(Tex(r"\textbf{Theorem.} Let $d\ge2$ and $E\subset\mathbb{R}^d$ compact.", font_size=40),
                     Tex(r"If $\dim_H E>\tfrac d2$, then $\Delta(E)$ has positive Lebesgue measure.", font_size=40),
                     Tex(r"No regularity, no product structure, no Fourier decay assumed.", font_size=30,
                         color=GREY_A)).arrange(DOWN, buff=0.3)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.35))
        with self.say("A manuscript in OpenAI's math catalogue, produced by an OpenAI model and not yet peer reviewed, "
                      "claims the full conjecture, in every dimension: if a compact set has dimension greater than "
                      "half the ambient dimension, its distance set has positive length. No extra regularity is "
                      "assumed.") as s:
            self.play(Write(tb), run_time=2.5)
        self.play(FadeOut(tb))

        # ------------------------------------------------------------ proof: Frostman measure, distance measure, bands
        hdr = Tex("Step 1: turn the set into a measure, and the distances into a measure", font_size=34,
                  color=YELLOW_3B).to_edge(UP, buff=0.35)
        dust = dust_squares(4, LEFT * 4.3 + DOWN * 0.3, 3.6, BLUE_3B, 0.9)
        fr = MathTex(r"\mu(B(x,r))\le r^{s},\quad s>\tfrac d2", font_size=36).next_to(dust, DOWN, buff=0.35)
        arr = Arrow(LEFT * 2.0 + DOWN * 0.3, RIGHT * 0.0 + DOWN * 0.3, color=GREY_B)
        al = MathTex(r"(x,y)\mapsto|x-y|", font_size=30).next_to(arr, UP, buff=0.1)
        ax = Axes(x_range=[0, 1.45, 0.5], y_range=[0, 1, 1], x_length=5.6, y_length=2.4, tips=False,
                  axis_config={"color": GREY_B}).move_to(RIGHT * 3.6 + UP * 0.4)
        hist_n = hist / hist.max()
        dm = VMobject(color=TEAL_3B, stroke_width=3).set_points_smoothly(
            [ax.c2p((a + b) / 2, h) for a, b, h in zip(bins[:-1], bins[1:], np.convolve(hist_n, np.ones(5) / 5, "same"))])
        nul = MathTex(r"\nu=\text{distance measure on }\Delta(E)", font_size=30, color=TEAL_3B).next_to(ax, UP, 0.2)
        fax = NumberLine(x_range=[0, 6, 1], length=5.6, include_numbers=False, color=GREY_B, include_tip=False
                         ).move_to(RIGHT * 3.6 + DOWN * 2.0)
        bands = VGroup(*[Line(fax.n2p(k), fax.n2p(k + 1), color=c, stroke_width=10)
                         for k, c in zip(range(6), [BLUE_3B, TEAL_3B, GREEN_3B, YELLOW_3B, ORANGE_3B, RED_3B])])
        bl = MathTex(r"\int_{2^N}^{2^{N+1}}|\widehat{\nu}(r)|^2\,dr\ \lesssim\ 2^{-\gamma N}?", font_size=34
                     ).next_to(fax, DOWN, buff=0.3)
        fl = Tex("frequency bands", font_size=26, color=GREY_A).next_to(fax, UP, buff=0.15)
        with self.say(f"How does the proof go? {{fr}}First, by {FROST}'s lemma, spread a probability measure mu over "
                      "the set, so that no ball of radius r gets more than r to the s, with s bigger than d over two. "
                      "{nu}Push every pair forward by its distance: this gives a measure nu on the line, sitting on "
                      "the distance set. If nu has a density, the distance set has positive length. "
                      f"{{b}}Following {MAT}, one checks this one frequency band at a time: the Fourier energy of nu "
                      "between two to the N and two to the N plus one should decay geometrically.") as s:
            self.play(Write(hdr))
            s.wait_until("fr")
            self.play(FadeIn(dust), Write(fr))
            s.wait_until("nu")
            self.play(GrowArrow(arr), FadeIn(al))
            self.play(Create(ax), Create(dm), FadeIn(nul), run_time=2)
            s.wait_until("b")
            self.play(Create(fax), LaggedStart(*[Create(b) for b in bands], lag_ratio=0.2), FadeIn(fl), run_time=2)
            self.play(Write(bl))
        self.play(FadeOut(VGroup(hdr, dust, fr, arr, al, ax, dm, nul, fax, bands, bl, fl)))

        # ------------------------------------------------------------ step 2: directions and cap bounds
        hdr = Tex("Step 2: control the directions seen from each point", font_size=34, color=YELLOW_3B).to_edge(
            UP, buff=0.35)
        C2 = LEFT * 4.1 + DOWN * 0.4
        dust2 = dust_squares(4, C2, 4.2, BLUE_3B, 0.55)
        ix = int(np.argmin(np.hypot(P[:, 0] - 0.31, P[:, 1] - 0.31)))
        x0 = P[ix]
        xs = C2 + 4.2 * np.array([x0[0] - 0.5, x0[1] - 0.5, 0])
        rng = np.random.default_rng(1)
        others = rng.choice(len(P), 70, replace=False)
        rays = VGroup(*[Line(xs, C2 + 4.2 * np.array([P[j][0] - 0.5, P[j][1] - 0.5, 0]), stroke_width=1.2,
                             color=YELLOW_3B, stroke_opacity=0.5) for j in others if j != ix])
        xd = Dot(xs, color=RED_3B, radius=0.08)
        xl = MathTex("x", font_size=32, color=RED_3B).next_to(xd, DL, buff=0.05)
        cc = RIGHT * 1.9 + DOWN * 0.4
        circ = Circle(radius=1.7, color=GREY_B).move_to(cc)
        dirs = np.arctan2(P[:, 1] - x0[1], P[:, 0] - x0[0])
        dirs = np.delete(dirs, ix)
        dt = VGroup(*[Line(cc + 1.6 * np.array([np.cos(a), np.sin(a), 0]), cc + 1.8 * np.array([np.cos(a), np.sin(a), 0]),
                           stroke_width=1, color=YELLOW_3B, stroke_opacity=0.5) for a in dirs[::2]])
        a0 = np.median(dirs)
        cap = Arc(radius=1.7, start_angle=a0 - 0.25, angle=0.5, arc_center=cc, color=RED_3B, stroke_width=10)
        capl = Tex(r"cap of radius $r$:\\ mass $\lesssim r^{\,d/2-\varepsilon}$", font_size=30, color=RED_3B).next_to(
            circ, RIGHT, buff=0.2).shift(UP * 1.2)
        dl = Tex(r"directions $\frac{y-x}{|y-x|}$", font_size=30).next_to(circ, DOWN, buff=0.3)
        note = Tex(r"after deleting a power-small set of pairs", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.say("The first new ingredient is about directions. {x}Stand at a point x, and look in the "
                      "direction of every other point of the set. {c}Record those directions on a sphere, here a "
                      "circle. In high dimensions, these directions can't be spread out smoothly: a set of "
                      "dimension s casts a shadow of dimension at most s on the sphere. {cap}Instead, the paper "
                      "proves cap bounds: after deleting a tiny fraction of the pairs, no cap of radius r receives "
                      "more than about r to the d over two of the mass.") as s:
            self.play(Write(hdr))
            s.wait_until("x")
            self.play(FadeIn(dust2), FadeIn(xd), FadeIn(xl))
            self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.02), run_time=2)
            s.wait_until("c")
            self.play(Create(circ), FadeIn(dt, lag_ratio=0.01), FadeIn(dl), run_time=2)
            s.wait_until("cap")
            self.play(Create(cap), FadeIn(capl))
            self.play(FadeIn(note))
        self.play(FadeOut(VGroup(hdr, dust2, rays, xd, xl, circ, dt, cap, capl, dl, note)))

        # ------------------------------------------------------------ step 3: belts and the threshold
        hdr = Tex("Step 3: from directions to Fourier decay", font_size=34, color=YELLOW_3B).to_edge(UP, buff=0.35)
        sc = LEFT * 3.4 + DOWN * 0.5
        sph = Circle(radius=2.0, color=GREY_B).move_to(sc)
        belt = VGroup(Ellipse(width=4.0, height=0.9, color=TEAL_3B).move_to(sc + UP * 0.12),
                      Ellipse(width=4.0, height=0.9, color=TEAL_3B).move_to(sc + DOWN * 0.12))
        band = Polygon(*[sc + np.array([2 * np.cos(t), 0.45 * np.sin(t) + 0.12, 0]) for t in np.linspace(PI, 2 * PI, 40)],
                       *[sc + np.array([2 * np.cos(t), 0.45 * np.sin(t) - 0.12, 0]) for t in np.linspace(2 * PI, PI, 40)],
                       stroke_width=0).set_fill(TEAL_3B, 0.45)
        capd = Circle(radius=0.28, color=RED_3B).set_fill(RED_3B, 0.5).move_to(sc + UP * 1.2 + LEFT * 0.6)
        bl = Tex(r"belt of width $1/B$", font_size=28, color=TEAL_3B).next_to(sph, DOWN, buff=0.25)
        rows = VGroup(
            Tex(r"stationary phase: each frequency band of $\nu$", font_size=30),
            Tex(r"becomes an angular quantity on the sphere", font_size=30),
            Tex(r"belt estimate gives the factor", font_size=30),
            MathTex(r"B^{\,d-2S}", r"\;=\;1\quad\text{exactly when}\quad", r"S=\tfrac d2", font_size=42),
            Tex(r"$S$ = cap exponent from Step 2", font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.3).move_to(RIGHT * 2.75 + DOWN * 0.2)
        rows[3][2].set_color(YELLOW_3B)
        with self.say("The second ingredient turns these angular bounds into Fourier decay. {sp}By stationary phase, "
                      "each frequency band of the distance measure becomes an angular quantity on the sphere. "
                      "{belt}The key computation is over thin belts around the sphere, and it produces a factor B to "
                      "the power d minus two S, where S is the cap exponent. {one}That is exactly one when S equals "
                      "d over two. The threshold of the conjecture is precisely where this belt estimate balances.") as s:
            self.play(Write(hdr))
            s.wait_until("sp")
            self.play(Create(sph), FadeIn(capd), FadeIn(rows[:2]))
            s.wait_until("belt")
            self.play(FadeIn(band), Create(belt), FadeIn(bl), FadeIn(rows[2]))
            self.play(Write(rows[3][0]))
            s.wait_until("one")
            self.play(Write(rows[3][1:]), FadeIn(rows[4]))
        self.play(FadeOut(VGroup(hdr, sph, belt, band, capd, bl, rows)))

        # ------------------------------------------------------------ step 4: multiscale recursion and the limit
        hdr = Tex("Step 4: a multiscale recursion pays for every scale", font_size=34, color=YELLOW_3B).to_edge(
            UP, buff=0.35)
        ax = Axes(x_range=[0, 9, 1], y_range=[0, 1.1, 0.5], x_length=6.2, y_length=3.6, tips=False,
                  axis_config={"color": GREY_B}).move_to(LEFT * 2.8 + DOWN * 0.6)
        bars = VGroup(*[Rectangle(width=0.45, height=3.6 * 0.62 ** k / 1.1, stroke_width=0).set_fill(
            [BLUE_3B, TEAL_3B, GREEN_3B, YELLOW_3B, ORANGE_3B, RED_3B, PURPLE_3B, BLUE_3B, TEAL_3B][k], 0.85
        ).move_to(ax.c2p(k + 0.5, 0), aligned_edge=DOWN) for k in range(9)])
        xl = Tex("band $N$", font_size=28).next_to(ax.x_axis, DOWN, buff=0.2)
        yl = Tex(r"band energy (schematic)", font_size=28).next_to(ax, UP, buff=0.2)
        rr = VGroup(
            Tex(r"$\bullet$ split $\mu$ into pieces by \emph{profile}:", font_size=30),
            Tex(r"\quad how mass decays from scale to scale", font_size=30),
            Tex(r"$\bullet$ a potential built from two separated", font_size=30),
            Tex(r"\quad scales pays each step's cost", font_size=30),
            MathTex(r"\Rightarrow\ \text{band energy}\lesssim 2^{-\gamma N}", font_size=36, color=YELLOW_3B),
            Tex(r"$\Rightarrow$ $\nu_\infty\neq0$ has a density, lives on $\Delta(E)$", font_size=30),
            Tex(r"$\Rightarrow$ $|\Delta(E)|>0$", font_size=36, color=GREEN_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 3.6 + DOWN * 0.4)
        with self.say("Finally, the analysis runs across scales. {pr}The measure is split into pieces according to "
                      "their profile, which records how mass decays from one scale to the next, {pot}and a potential "
                      "built from two well separated scales pays the cost of every step of the recursion. "
                      "{dec}The upshot: the band energies decay geometrically. {lim}Adding up the bands gives a "
                      "nonzero limiting measure with a density, carried by the distance set. So the distance set has "
                      "positive length.") as s:
            self.play(Write(hdr))
            s.wait_until("pr")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(rr[:2]))
            s.wait_until("pot")
            self.play(FadeIn(rr[2:4]))
            s.wait_until("dec")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15), Write(rr[4]), run_time=2)
            s.wait_until("lim")
            self.play(FadeIn(rr[5]))
            self.play(FadeIn(rr[6], scale=1.2))
        self.play(FadeOut(VGroup(hdr, ax, bars, xl, yl, rr)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Compact $E\subset\mathbb{R}^d$, $d\ge2$, $\dim_H E>\tfrac d2$ $\Rightarrow$ $|\Delta(E)|>0$",
             r"Resolves Falconer's 1985 conjecture in every dimension",
             r"Manuscript: 64 pages, produced by an OpenAI model"],
            True, r"\emph{The Falconer distance conjecture in all dimensions} (Sept.\ 2026)")
        with self.say("The manuscript is sixty four pages, and it does not rely on decoupling, or on any earlier distance "
                      "theorem at an improved threshold. {l}Its main theorem, in every dimension, has been formalized and checked in the Lean "
                      "proof assistant. If it is right, Falconer's threshold of d over two was exactly the truth.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
