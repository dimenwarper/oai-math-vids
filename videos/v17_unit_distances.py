from pathlib import Path

import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(Path(__file__).parent / "data" / "v17.npz")

ERD = "[Erdős](/ˈɛɹdəʃ/)"
SOL = "[Solymosi](/ʃˈOjmOʃi/)"
TOTH = "[Tóth](/tˈOt/)"
TAR = "[Tardos](/tˈɑɹdOʃ/)"
SZEM = "[Szemerédi](/sˈɛməɹˌAdi/)"
SZEK = "[Székely](/sˈAkAj/)"
MOB = "[Möbius](/mˈObiəs/)"


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "167", "Distinct and Unit Distances",
                          r"The weak pinned Erd\H{o}s conjecture, and a power saving below $n^{4/3}$")
        with self.say("Put n points in the plane. How many different distances must they determine? "
                      "And how often can one distance repeat?"):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.4)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ grid and a pin
        g = 0.62
        org = LEFT * 3.2 + DOWN * 0.25
        pts = VGroup(*[Dot(org + g * np.array([i - 3, j - 3, 0]), radius=0.07, color=GREY_A)
                       for i in range(7) for j in range(7)])
        pin = Dot(org, radius=0.11, color=YELLOW_3B)
        circs = VGroup(*[Circle(radius=g * np.sqrt(d), color=BLUE_3B, stroke_width=2.5).move_to(org)
                         for d in D["d2_center"]])
        cnt = VGroup(Tex(r"48 other points", font_size=36),
                     Tex(rf"only {len(D['d2_center'])} distinct distances", font_size=36, color=BLUE_3B),
                     Tex(rf"(from a corner: {len(D['d2_corner'])})", font_size=32, color=GREY_A)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.6 + UP * 0.6)
        why = MathTex(r"5=1^2+2^2,\quad 25=0^2+5^2=3^2+4^2", font_size=34, color=GREY_A).next_to(cnt, DOWN, buff=0.6)
        with self.say("Take a seven by seven grid, and stand at its center. {c}Draw a circle through every other "
                      "point. {n}There are forty-eight other points, but only nine circles: the center sees just "
                      "nine distinct distances. {w}Grids are good at repeating distances, because many whole-number "
                      "vectors have the same length. {co}From a corner, the same grid shows twenty-six.") as s:
            self.play(LaggedStart(*[GrowFromCenter(p) for p in pts], lag_ratio=0.02), run_time=1.5)
            self.play(FadeIn(pin, scale=2))
            s.wait_until("c")
            self.play(LaggedStart(*[Create(c) for c in circs], lag_ratio=0.25), run_time=3)
            s.wait_until("n")
            self.play(FadeIn(cnt[:2]))
            s.wait_until("w")
            self.play(FadeIn(why))
            s.wait_until("co")
            self.play(FadeIn(cnt[2]))
        self.play(FadeOut(VGroup(pts, pin, circs, cnt, why)))

        # ------------------------------------------------------------ history of pinned distances
        hist = VGroup(
            Tex(r"1946, Erd\H{o}s: a grid of $n$ points has only $\approx n/\sqrt{\log n}$ distances", font_size=32),
            Tex(r"Guth--Katz: every $n$ points determine $\ge c\,n/\log n$ distances", font_size=32),
            Tex(r"1957, Erd\H{o}s: is there one \emph{pin} that sees almost $n$ distances?", font_size=32,
                color=YELLOW_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(UP, buff=0.5)
        nl = NumberLine(x_range=[0.8, 1.0, 0.05], length=9, include_numbers=False, color=GREY_B).shift(
            DOWN * 1.4 + RIGHT * 0.9)
        nlab = VGroup(*[MathTex(t, font_size=28).next_to(nl.n2p(v), DOWN, buff=0.2)
                        for t, v in [("0.80", 0.8), ("0.85", 0.85), ("0.90", 0.9), ("0.95", 0.95), ("1", 1.0)]])
        ex = Tex(r"pinned exponent", font_size=28, color=GREY_A).next_to(nl, LEFT, buff=0.2).shift(UP * 0.0)
        m1 = VGroup(Dot(nl.n2p(6 / 7), color=BLUE_3B),
                    Tex(r"Solymosi--T\'oth: $6/7$", font_size=28, color=BLUE_3B).next_to(nl.n2p(6 / 7), UP, buff=0.8)
                    .shift(LEFT * 0.9))
        m2 = VGroup(Dot(nl.n2p(0.8641), color=TEAL_3B),
                    Tex(r"Katz--Tardos: $0.864$", font_size=28, color=TEAL_3B).next_to(nl.n2p(0.8641), UP, buff=0.3)
                    .shift(RIGHT * 0.9))
        m3 = VGroup(Dot(nl.n2p(1.0), color=YELLOW_3B),
                    Tex(r"conjecture: $1-\varepsilon$", font_size=28, color=YELLOW_3B).next_to(nl.n2p(1.0), UP,
                                                                                            buff=0.3))
        with self.say(f"Paul {ERD} raised these questions in 1946. {{gr}}A square grid of n points has only about n "
                      "over the square root of log n distances in total, {gk}and Guth and Katz proved that every set "
                      f"has at least a constant times n over log n. {{pin}}In 1957, {ERD} asked a pinned version: is "
                      "there always a single point that sees almost n distances by itself? "
                      f"{{st}}{SOL} and {TOTH} found a point seeing n to the six sevenths. {{kt}}{TAR}, and then Katz "
                      f"and {TAR}, pushed the exponent to about point eight six four. {{c}}The conjecture asks for one "
                      "minus epsilon.") as s:
            s.wait_until("gr")
            self.play(FadeIn(hist[0]))
            s.wait_until("gk")
            self.play(FadeIn(hist[1]))
            s.wait_until("pin")
            self.play(FadeIn(hist[2]), Create(nl), FadeIn(nlab), FadeIn(ex))
            s.wait_until("st")
            self.play(FadeIn(m1))
            s.wait_until("kt")
            self.play(FadeIn(m2))
            s.wait_until("c")
            self.play(FadeIn(m3))
        self.play(FadeOut(VGroup(hist, nl, nlab, ex, m1, m2, m3)))

        thm = VGroup(Tex(r"\textbf{Theorem 1} (weak pinned conjecture). For every $\varepsilon>0$,", font_size=38),
                     Tex(r"all but $o(n)$ of any $n$ points in the plane each see", font_size=38),
                     Tex(r"at least $n^{1-\varepsilon}$ distinct distances.", font_size=38)).arrange(DOWN, buff=0.22)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3)).shift(UP * 1.3)
        cc = DOWN * 2.0 + LEFT * 2.0
        ring = VGroup(*[Dot(cc + 1.1 * np.array([np.cos(t), np.sin(t), 0]), radius=0.06, color=GREY_A)
                        for t in np.linspace(0, TAU, 14, endpoint=False)])
        cen = Dot(cc, radius=0.08, color=RED_3B)
        spokes = VGroup(*[Line(cc, d.get_center(), color=RED_3B, stroke_width=1.5) for d in ring])
        exl = Tex(r"exceptions are unavoidable:\\ the center sees one distance", font_size=30).next_to(ring, RIGHT,
                                                                                                    buff=0.6)
        with self.say("The first manuscript claims the weak pinned conjecture. {t}For every epsilon, all but a "
                      "vanishing fraction of the points each see at least n to the one minus epsilon distinct "
                      "distances. {e}Some exceptions are unavoidable: the center of a circle of points sees only "
                      "one distance.") as s:
            s.wait_until("t")
            self.play(Write(tb), run_time=2.5)
            s.wait_until("e")
            self.play(FadeIn(ring), FadeIn(cen), Create(spokes), FadeIn(exl))
        self.play(FadeOut(VGroup(tb, ring, cen, spokes, exl)))

        # ------------------------------------------------------------ unit distances
        g = 0.5
        korg = LEFT * 3.4 + DOWN * 0.3
        kP = D["kn_P"]
        kd = VGroup(*[Dot(korg + g * np.array([i - 3.5, j - 3.5, 0]), radius=0.06, color=GREY_A) for i, j in kP])
        ke = VGroup(*[Line(kd[a].get_center(), kd[b].get_center(), color=BLUE_3B, stroke_width=1.6)
                      for a, b in D["kn_E"]])
        kt = VGroup(Tex(r"knight's move: length $\sqrt5$", font_size=32),
                    Tex(r"rescale it to 1:", font_size=32),
                    Tex(rf"64 points, {len(D['kn_E'])} unit distances", font_size=32, color=BLUE_3B)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 3.3 + UP * 2.2)
        uh = VGroup(
            Tex(r"lattices: $u(n)\ge n^{1+c/\log\log n}$ (Erd\H{o}s, 1946)", font_size=30),
            Tex(r"$u(n)=O(n^{4/3})$ (Spencer--Szemer\'edi--Trotter, 1984)", font_size=30),
            Tex(r"Sz\'ekely: proof via crossing numbers,\\ using only that two unit circles\\ meet in at most two points",
                font_size=30, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.3 + DOWN * 1.2)
        with self.say("Now the other question: how often can one distance repeat? Rescale it, and call it one. "
                      "{kn}In this eight by eight grid, a knight's move has length root five. Rescale that to one, "
                      "and sixty-four points give a hundred and sixty-eight unit distances. "
                      f"{{lat}}{ERD} showed that lattices give a bit more than linear growth. {{sst}}The upper bound, "
                      f"n to the four thirds, is due to Spencer, {SZEM} and Trotter in 1984, {{sz}}and {SZEK} later "
                      "gave a slick proof using crossing numbers. Since then, only the constant in front had "
                      "improved.") as s:
            self.play(FadeIn(kd))
            s.wait_until("kn")
            self.play(FadeIn(kt[0]), LaggedStart(*[Create(e) for e in ke], lag_ratio=0.01), run_time=2.5)
            self.play(FadeIn(kt[1:]))
            s.wait_until("lat")
            self.play(FadeIn(uh[0]))
            s.wait_until("sst")
            self.play(FadeIn(uh[1]))
            s.wait_until("sz")
            self.play(FadeIn(uh[2]))
        self.play(FadeOut(VGroup(kd, ke, kt, uh)))

        thm2 = VGroup(Tex(r"\textbf{Theorem 2.} There is an absolute $\beta<4/3$ such that", font_size=38),
                      Tex(r"$n$ points in the plane determine $O(n^{\beta})$ unit distances.", font_size=38)
                      ).arrange(DOWN, buff=0.22)
        tb2 = VGroup(thm2, caption_box(thm2, YELLOW_3B, 0.3)).shift(UP * 1.5)
        nl = NumberLine(x_range=[1, 4 / 3 + 0.001, 1 / 12], length=9, include_numbers=False, color=GREY_B).shift(
            DOWN * 1.3)
        l1 = MathTex("1", font_size=32).next_to(nl.n2p(1), DOWN, buff=0.2)
        l2 = MathTex(r"\tfrac43", font_size=32).next_to(nl.n2p(4 / 3), DOWN, buff=0.2)
        lo = Line(nl.n2p(1), nl.n2p(1.03), color=GREY_D, stroke_width=12)
        hi = Line(nl.n2p(1.29), nl.n2p(4 / 3), color=GREY_D, stroke_width=12)
        mid = Line(nl.n2p(1.03), nl.n2p(1.29), color=YELLOW_3B, stroke_width=6)
        lol = Tex(r"$1+\varepsilon$: earlier OpenAI\\ construction (cited)", font_size=26).next_to(lo, UP, buff=0.3)
        hil = Tex(r"$\beta$: this paper", font_size=26).next_to(hi, UP, buff=0.3)
        tl = Tex(r"the true exponent lies in here", font_size=28, color=YELLOW_3B).next_to(mid, DOWN, buff=0.35)
        with self.say("The second manuscript claims a power saving. {t}There is an absolute exponent beta, below four "
                      f"thirds, such that n points always determine at most a constant times n to the beta unit "
                      f"distances. The value of beta is not made explicit. {{c}}The paper also cites an earlier OpenAI "
                      f"construction with more than n to the one plus epsilon unit distances, which refuted {ERD}'s "
                      "guess of n to the one plus little o of one. {b}So the true exponent is now trapped strictly "
                      "between one and four thirds.") as s:
            s.wait_until("t")
            self.play(Write(tb2), run_time=2.5)
            s.wait_until("c")
            self.play(Create(nl), FadeIn(l1), FadeIn(l2), FadeIn(lo), FadeIn(lol))
            s.wait_until("b")
            self.play(FadeIn(hi), FadeIn(hil), Create(mid), FadeIn(tl))
        self.play(FadeOut(VGroup(tb2, nl, l1, l2, lo, hi, mid, lol, hil, tl)))

        # ------------------------------------------------------------ the shared engine
        hdr = Tex(r"The shared engine: arithmetic", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.35)
        f1 = Tex(r"1. Nudge the points to algebraic coordinates,\\ keeping every distance coincidence.",
                 font_size=30).to_edge(LEFT, buff=0.5).shift(UP * 1.9)
        f2 = VGroup(MathTex(r"z=x+iy,\qquad w=x-iy", font_size=36),
                    MathTex(r"|p-q|^2=(z_p-z_q)(w_p-w_q)", font_size=36),
                    MathTex(r"|p-q|=1:\quad w_p-w_q=\frac{1}{z_p-z_q}", font_size=36)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(f1, DOWN, buff=0.45).align_to(f1, LEFT)
        ax = Axes(x_range=[0, 4, 1], y_range=[-1.6, 2.2, 1], x_length=4.6, y_length=3.6, tips=False,
                  axis_config={"color": GREY_B, "include_ticks": False}).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.7)
        names = [r"|\cdot|_\infty", r"|\cdot|_2", r"|\cdot|_3", r"|\cdot|_7"]
        vals = D["pf"]
        cols = [BLUE_3B, RED_3B, RED_3B, BLUE_3B]
        bars = VGroup(*[Rectangle(width=0.7, height=abs(v) * ax.y_length / 3.8, stroke_width=0).set_fill(c, 0.85)
                        .move_to(ax.c2p(k + 0.5, 0), aligned_edge=DOWN if v > 0 else UP)
                        for k, (v, c) in enumerate(zip(vals, cols))])
        bl = VGroup(*[MathTex(nm, font_size=26).next_to(ax.c2p(k + 0.5, 0), DOWN if vals[k] > 0 else UP, buff=0.15)
                      for k, nm in enumerate(names)])
        bv = VGroup(*[MathTex(t, font_size=28).next_to(b, UP if v > 0 else DOWN, buff=0.1)
                      for t, b, v in zip([r"\tfrac{12}{7}", r"\tfrac14", r"\tfrac13", "7"], bars, vals)])
        pft = MathTex(r"\tfrac{12}{7}\cdot\tfrac14\cdot\tfrac13\cdot 7=1", font_size=34).next_to(ax, UP, buff=0.25)
        pfl = Tex(r"product formula: $\sum_v \log|\alpha|_v=0$", font_size=28, color=GREY_A).next_to(pft, UP,
                                                                                                    buff=0.15)
        with self.say("Both proofs run on the same unusual engine: arithmetic. {a}First, nudge the points so that "
                      "every coordinate is an algebraic number, keeping every distance coincidence. {z}Then give each "
                      "point two complex coordinates, z equals x plus i y, and w equals x minus i y. Squared distance "
                      "factors as the jump in z times the jump in w, so for a unit pair, the two jumps are d and one "
                      "over d. {pf}Now, algebraic numbers obey the product formula. Measure a number's size in every "
                      "possible way, the ordinary way and one way for each prime, and the sizes multiply to one. For "
                      "twelve sevenths: twelve sevenths, times a quarter, times a third, times seven, is one. "
                      "{b}So a jump that is tiny in one measurement must be large in another, for every "
                      "configuration whatsoever.") as s:
            self.play(Write(hdr))
            s.wait_until("a")
            self.play(FadeIn(f1))
            s.wait_until("z")
            self.play(FadeIn(f2[0]))
            self.play(FadeIn(f2[1]))
            self.play(FadeIn(f2[2]))
            s.wait_until("pf")
            self.play(Create(ax), FadeIn(pfl))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if v > 0 else UP) for b, v in zip(bars, vals)],
                                  lag_ratio=0.3), FadeIn(bl), FadeIn(bv), run_time=2)
            self.play(Write(pft))
            s.wait_until("b")
            self.play(Indicate(bars[1]), Indicate(bars[3]))
        self.play(FadeOut(VGroup(hdr, f1, f2, ax, bars, bl, bv, pft, pfl)))

        # ------------------------------------------------------------ how each proof uses it
        hdr = Tex(r"How each proof uses the balance", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.35)
        rng = np.random.default_rng(4)
        box = Square(3.2, color=GREY_B).move_to(LEFT * 4.3 + DOWN * 0.5)
        P2 = rng.uniform(-1.5, 1.5, (40, 2))
        pd = VGroup(*[Dot(box.get_center() + np.array([x, y, 0]), radius=0.04, color=GREY_A) for x, y in P2])
        shift = {RIGHT.tobytes(): 0.37, UP.tobytes(): -0.29}  # one random shift shared by all levels (nested)
        grids = VGroup()
        for lev, (k, col) in enumerate([(2, BLUE_3B), (4, TEAL_3B), (8, GREEN_3B)]):
            h = 3.2 / k
            for d_ in (RIGHT, UP):
                for t in range(-1, k + 1):
                    off = -1.6 + t * h + shift[d_.tobytes()] % h
                    if not -1.55 < off < 1.55:
                        continue
                    a = box.get_center() + off * d_
                    ln = Line(a - 1.6 * rotate_vector(d_, PI / 2), a + 1.6 * rotate_vector(d_, PI / 2), color=col,
                              stroke_width=3.5 - lev)
                    grids.add(ln)
        gl = Tex(r"nested grids at every scale,\\ in every measurement", font_size=26).next_to(box, DOWN, buff=0.2)
        pin_t = VGroup(
            Tex(r"\textbf{Pinned:} group points by closeness at every level", font_size=30),
            Tex(r"and place. The product formula makes the total", font_size=30),
            Tex(r"overlap of two points split as $f(x)+g(y)$.", font_size=30),
            Tex(r"$\Rightarrow$ a variance bound: points on a rich circle", font_size=30),
            Tex(r"must be spread like the whole set, at every scale.", font_size=30),
            Tex(r"Limits then contradict this (trees / M\"obius maps).", font_size=30, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to(RIGHT * 1.55 + UP * 1.35)
        unit_t = VGroup(
            Tex(r"\textbf{Unit:} points vs.\ unit circles (as in Sz\'ekely),", font_size=30),
            Tex(r"plus information: two random neighbors of a center", font_size=30),
            Tex(r"share little information. With heights, this forces", font_size=30),
            Tex(r"ratios that the final step, flipping signs of square", font_size=30),
            Tex(r"roots via valuations, shows cannot exist.", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(pin_t, DOWN, buff=0.45).align_to(pin_t, LEFT)
        with self.say("For the pinned theorem, the paper groups points by closeness, at every scale and in every one "
                      "of these measurements, using randomly shifted grids. {o}The product formula makes the total "
                      "overlap of two points split into a function of the first plus a function of the second. "
                      "{v}That identity gives a variance bound: the points on a heavily repeated circle must be "
                      "spread out like the whole set, at every scale, and a limiting argument turns this into a "
                      "contradiction. {u}The unit-distance proof starts from points and unit circles, and adds "
                      "information theory: two random neighbors of a random center share little information. "
                      "{h}Combined with heights from the product formula, this forces a family of ratios which a "
                      "final algebraic argument, flipping signs of square roots, rules out.") as s:
            self.play(Write(hdr), Create(box), FadeIn(pd))
            self.play(LaggedStart(*[Create(l) for l in grids], lag_ratio=0.03), FadeIn(gl), run_time=2)
            self.play(FadeIn(pin_t[0]))
            s.wait_until("o")
            self.play(FadeIn(pin_t[1:3]))
            s.wait_until("v")
            self.play(FadeIn(pin_t[3:]))
            s.wait_until("u")
            self.play(FadeIn(unit_t[:3]))
            s.wait_until("h")
            self.play(FadeIn(unit_t[3:]))
        self.play(FadeOut(VGroup(hdr, box, pd, grids, gl, pin_t, unit_t)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Weak pinned Erd\H{o}s conjecture: all but $o(n)$ points see $\ge n^{1-\varepsilon}$ distances",
             r"Unit distances: at most $Cn^{\beta}$ for an absolute $\beta<4/3$ (not explicit)",
             r"Manuscripts: 27 and 53 pages, produced by an OpenAI model"],
            True, r"\emph{The weak pinned planar distance theorem} and\\ \emph{A power saving for planar unit distances}"
                  r" (Sept.\ 2026)")
        with self.say("Both manuscripts, twenty-seven and fifty-three pages, were written by an OpenAI model and are "
                      "not yet peer reviewed. {l}Both main theorems, the weak pinned statement and the unit-distance "
                      "power saving, have been formalized in the Lean proof assistant.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
