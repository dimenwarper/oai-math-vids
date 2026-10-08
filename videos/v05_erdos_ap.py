import numpy as np
from manim import *

from style import *
from vo import NarratedScene

ERDOS = "[Erdős](/ˈɛɹdəʃ/)"
SZEM = "[Szemerédi](/sˈɛməɹˌAdi/)"


def primes_upto(n):
    s = np.ones(n + 1, bool)
    s[:2] = False
    for i in range(2, int(n**0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.nonzero(s)[0]


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "159", r"Erd\H{o}s's Reciprocal-Sum Conjecture",
                          r"Divergent $\sum 1/a$ $\Rightarrow$ arithmetic progressions of every length")
        with self.say(f"{ERDOS}'s five thousand dollar problem."):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ APs
        nl = NumberLine(x_range=[0, 32, 1], length=12.5, include_numbers=False, tick_size=0.06,
                        color=GREY_B).shift(UP * 1.2)
        labs = VGroup(*[MathTex(str(k), font_size=22, color=GREY_B).next_to(nl.n2p(k), DOWN, buff=0.12)
                        for k in range(0, 33, 4)])
        ap = [3, 7, 11, 15]
        apd = VGroup(*[Dot(nl.n2p(a), radius=0.1, color=YELLOW_3B) for a in ap])
        apa = VGroup(*[ArcBetweenPoints(nl.n2p(a), nl.n2p(b), angle=-PI / 2, color=YELLOW_3B)
                       for a, b in zip(ap, ap[1:])])
        apl = MathTex(r"3,\ 7,\ 11,\ 15", r"\quad\text{(gap 4)}", font_size=40, color=YELLOW_3B).next_to(nl, UP,
                                                                                                    buff=1.0)
        nl2 = NumberLine(x_range=[0, 32, 1], length=12.5, include_numbers=False, tick_size=0.06,
                         color=GREY_B).shift(DOWN * 1.6)
        pr = [p for p in primes_upto(32)]
        prd = VGroup(*[Dot(nl2.n2p(p), radius=0.08, color=BLUE_3B) for p in pr])
        prl = VGroup(*[MathTex(str(p), font_size=22, color=BLUE_3B).next_to(nl2.n2p(p), DOWN, buff=0.12) for p in pr])
        pap = [5, 11, 17, 23, 29]
        papa = VGroup(*[ArcBetweenPoints(nl2.n2p(a), nl2.n2p(b), angle=-PI / 2, color=YELLOW_3B)
                        for a, b in zip(pap, pap[1:])])
        papl = MathTex(r"5,\ 11,\ 17,\ 23,\ 29", r"\quad\text{five primes, gap 6}", font_size=36,
                       color=YELLOW_3B).next_to(nl2, UP, buff=0.9)
        with self.say("An arithmetic progression is a list of numbers with equal gaps, {ap}like three, seven, "
                      "eleven, fifteen. {pr}They hide in surprising places. Among the primes, "
                      "{pp}five, eleven, seventeen, twenty-three, twenty-nine is a progression of five primes. "
                      "In 2004, Ben Green and Terence Tao proved that the primes contain progressions of every "
                      "finite length.") as s:
            self.play(Create(nl), FadeIn(labs))
            s.wait_until("ap")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in apd], lag_ratio=0.3),
                      LaggedStart(*[Create(a) for a in apa], lag_ratio=0.3), Write(apl), run_time=2)
            s.wait_until("pr")
            self.play(Create(nl2), LaggedStart(*[FadeIn(d) for d in prd], lag_ratio=0.1), FadeIn(prl), run_time=1.5)
            s.wait_until("pp")
            self.play(*[prd[pr.index(p)].animate.set_color(YELLOW_3B).scale(1.4) for p in pap],
                      LaggedStart(*[Create(a) for a in papa], lag_ratio=0.3), Write(papl), run_time=2.5)
        self.play(FadeOut(VGroup(nl, labs, apd, apa, apl, nl2, prd, prl, papa, papl)))

        # ------------------------------------------------------------ reciprocal sums
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 4, 1], x_length=7, y_length=4.6, tips=False,
                  axis_config={"color": GREY_B, "font_size": 24}).shift(LEFT * 2.3 + DOWN * 0.5)
        ax.x_axis.add_labels({k: MathTex(f"10^{k}", font_size=26) for k in range(1, 5)})
        ax.y_axis.add_numbers(font_size=24)
        xlab = MathTex("N", font_size=30).next_to(ax.x_axis, RIGHT, buff=0.15)
        N = 10_000
        n = np.arange(1, N + 1)
        p = primes_upto(N)
        Sh = np.cumsum(1 / n)
        Ss = np.cumsum(1 / n**2)
        Sp = np.cumsum(1 / p)

        def curve(xs, ys, col):
            m = VMobject(color=col, stroke_width=4)
            pts = [ax.c2p(np.log10(x), y) for x, y in zip(xs, ys)]
            m.set_points_smoothly(pts[:: max(1, len(pts) // 300)] + [pts[-1]])
            return m

        idx = np.unique(np.geomspace(1, N, 400).astype(int)) - 1
        hidx = idx[Sh[idx] <= 3.75]
        c_h = curve(n[hidx], Sh[hidx], GREY_A)
        c_h.add(Arrow(c_h.get_end() + DOWN * 0.3 + LEFT * 0.06, c_h.get_end() + UP * 0.35, buff=0, color=GREY_A,
                      stroke_width=4, max_tip_length_to_length_ratio=0.5))
        c_s = curve(n[idx], Ss[idx], GREEN_3B)
        pidx = np.unique(np.geomspace(1, len(p), 300).astype(int)) - 1
        c_p = curve(p[pidx], Sp[pidx], BLUE_3B)
        lh = MathTex(r"\sum \tfrac1n=\infty", font_size=34, color=GREY_A).next_to(c_h.get_end(), RIGHT, buff=0.25)
        ls = MathTex(r"\sum \tfrac1{n^2}=\tfrac{\pi^2}{6}", font_size=34, color=GREEN_3B).next_to(ax.c2p(4, 1.64),
                                                                                                RIGHT, buff=0.15)
        lp = MathTex(r"\sum \tfrac1p=\infty", font_size=34, color=BLUE_3B).next_to(ax.c2p(4, 2.48), RIGHT, buff=0.15)
        lp2 = Tex(r"(Euler, 1737; grows like $\log\log N$)", font_size=26, color=BLUE_3B).next_to(lp, UP,
                                                                                                buff=0.15)
        with self.say(f"Paul {ERDOS} guessed something much bigger. Measure how large a set of whole "
                      "numbers is by adding up the reciprocals of its members. {h}For all the whole numbers, "
                      "that sum diverges. {sq}For the perfect squares it converges, to pi squared over six. "
                      "{p}For the primes, it diverges, but agonizingly slowly. "
                      "{conj}{ERDOS}'s conjecture: any set whose reciprocal sum diverges contains arithmetic "
                      "progressions of every finite length. ".replace("{ERDOS}", ERDOS) +
                      "{prize}He eventually offered five thousand dollars for it, one of the largest prizes he ever posted. "
                      "And since the primes qualify, it would give Green and Tao's theorem for free.") as s:
            self.play(Create(ax), FadeIn(xlab))
            s.wait_until("h")
            self.play(Create(c_h), FadeIn(lh), run_time=1.5)
            s.wait_until("sq")
            self.play(Create(c_s), FadeIn(ls), run_time=1.5)
            s.wait_until("p")
            self.play(Create(c_p), FadeIn(lp), FadeIn(lp2), run_time=2)
            s.wait_until("conj")
            graph = VGroup(ax, xlab, c_h, c_s, c_p, lh, ls, lp, lp2)
            self.play(graph.animate.scale(0.55).to_corner(DL, buff=0.3))
            conj = VGroup(Tex(r"\textbf{Conjecture} (Erd\H{o}s)", font_size=40, color=YELLOW_3B),
                          MathTex(r"\sum_{a\in A}\frac1a=\infty\ \Longrightarrow\ A\ \text{contains }k\text{-term "
                                  r"progressions for every }k", font_size=38)).arrange(DOWN, buff=0.3).to_edge(UP,
                                                                                                         buff=0.6)
            self.play(Write(conj), run_time=3)
            s.wait_until("prize")
            prize = Tex(r"\$5000", font_size=72, color=GREEN_3B).move_to(RIGHT * 3.6 + DOWN * 1.5)
            self.play(FadeIn(prize, scale=1.5))
        self.play(FadeOut(VGroup(graph, prize)), conj.animate.scale(0.75).to_edge(UP, buff=0.25))

        # ------------------------------------------------------------ density bounds
        rk = MathTex(r"r_k(N)", "=", r"\text{size of the largest subset of }\{1,\dots,N\}\text{ with no }k\text{-term "
                                     r"progression}", font_size=34).next_to(conj, DOWN, buff=0.5)
        rows = VGroup(
            Tex(r"1975 \quad Szemer\'edi: $r_k(N)=o(N)$", font_size=34),
            Tex(r"2001 \quad Gowers: $r_k(N)\le N/(\log\log N)^{c}$", font_size=34),
            Tex(r"2024 \quad Leng--Sah--Sawhney: $r_k(N)\le N\exp\!\big(-(\log\log N)^{c}\big)$", font_size=34),
            Tex(r"2026 \quad OpenAI catalogue: $r_k(N)\le C\,N\exp\!\big(-c(\log N)^{\varepsilon}\big)$",
                font_size=34, color=YELLOW_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(rk, DOWN, buff=0.5)
        with self.say("The natural route is through density. {rk}Let r k of N be the largest number of integers "
                      "up to N you can pick without creating a k-term progression. "
                      f"{{sz}}In 1975, Endre {SZEM} proved this is a vanishing fraction of N. "
                      "{gw}Gowers made it quantitative in 2001, and in 2024 Leng, Sah, and Sawhney improved it "
                      "dramatically. {gap}But all of these savings are in log log N, "
                      "and that is too weak for the reciprocal sum. {new}The new manuscript proves a saving "
                      "in a power of log N, for every length k.") as s:
            s.wait_until("rk")
            self.play(Write(rk), run_time=2)
            s.wait_until("sz")
            self.play(FadeIn(rows[0]))
            s.wait_until("gw")
            self.play(FadeIn(rows[1]))
            self.play(FadeIn(rows[2]))
            s.wait_until("new")
            self.play(FadeIn(rows[3], shift=UP * 0.2), run_time=1.5)
        self.play(FadeOut(VGroup(rk, rows)))

        # ------------------------------------------------------------ dyadic summability
        blocks = VGroup()
        x0 = -6.3
        widths = [0.25 * 1.45**m for m in range(8)]
        for m, wd in enumerate(widths):
            r = Rectangle(width=wd, height=0.45, stroke_color=GREY_B, stroke_width=2).set_fill(
                [BLUE_3B, TEAL_3B][m % 2], 0.25)
            r.move_to(np.array([x0 + wd / 2, 1.3, 0]))
            x0 += wd
            blocks.add(r)
        blabs = VGroup(*[MathTex(f"[2^{{{m}}},2^{{{m + 1}}})", font_size=20).next_to(b, DOWN, buff=0.08)
                         for m, b in enumerate(blocks) if m >= 4])
        expl = MathTex(r"\sum_{a\in A\cap[2^m,2^{m+1})}\frac1a\ \le\ \frac{r_k(2^m)}{2^m}", font_size=38).next_to(
            blocks, DOWN, buff=0.6)
        ax2 = Axes(x_range=[0, 60, 10], y_range=[0, 1, 0.5], x_length=5.6, y_length=2.4, tips=False,
                   axis_config={"color": GREY_B, "font_size": 20}).to_corner(DL, buff=0.5).shift(RIGHT * 0.3)
        ax3 = Axes(x_range=[0, 60, 10], y_range=[0, 20, 10], x_length=5.6, y_length=2.4, tips=False,
                   axis_config={"color": GREY_B, "font_size": 20}).to_corner(DR, buff=0.5)
        ax3.y_axis.add_numbers([10, 20], font_size=20)
        ms = np.arange(1, 61)
        old = np.exp(-np.log(ms * np.log(2) + 1.0) ** 0.6)
        new = np.exp(-1.1 * (ms * np.log(2)) ** 0.5)
        bars_old = VGroup(*[Line(ax2.c2p(m, 0), ax2.c2p(m, v), color=RED_3B, stroke_width=3) for m, v in zip(ms, old)])
        bars_new = VGroup(*[Line(ax2.c2p(m, 0), ax2.c2p(m, v), color=GREEN_3B, stroke_width=3) for m, v in
                            zip(ms, new)])
        t2 = Tex(r"max contribution of block $m$", font_size=26).next_to(ax2, UP, buff=0.1)
        t3 = Tex(r"running total", font_size=26).next_to(ax3, UP, buff=0.1)
        so = ax3.plot_line_graph(ms, np.cumsum(old), add_vertex_dots=False, line_color=RED_3B, stroke_width=4)
        sn = ax3.plot_line_graph(ms, np.cumsum(new), add_vertex_dots=False, line_color=GREEN_3B, stroke_width=4)
        lo = Tex(r"$\log\log$ savings: $\infty$", font_size=26, color=RED_3B).next_to(ax3.c2p(60, 19), LEFT,
                                                                                       buff=0.05).shift(DOWN * 0.1)
        ln = Tex(r"new bound: finite", font_size=26, color=GREEN_3B).next_to(ax3.c2p(60, np.cumsum(new)[-1]), UP,
                                                                             buff=0.15).shift(LEFT * 0.6)
        m_l = MathTex("m", font_size=26).next_to(ax2.x_axis, RIGHT, buff=0.1)
        m_l3 = MathTex("m", font_size=26).next_to(ax3.x_axis, RIGHT, buff=0.1)
        with self.say("Here is why the strength of the saving matters. {b}Chop the integers into blocks that "
                      "double in length: one to two, two to four, four to eight, and so on. "
                      "{c}A set with no k-term progression has at most r k of two to the m elements in block m, "
                      "each at least two to the m, so that block adds at most r k of two to the m, "
                      "over two to the m, to its reciprocal sum. "
                      "{old}With log-log savings, those per-block caps shrink so slowly that they add up to infinity, "
                      "and nothing is proved. {new}With the new bound, they shrink fast enough to have a finite total. "
                      "{fin}So every progression-free set has a convergent reciprocal sum. Turn that around, and "
                      "you have {ERDOS}'s conjecture.".replace("{ERDOS}", ERDOS)) as s:
            s.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in blocks], lag_ratio=0.15), FadeIn(blabs), run_time=2)
            s.wait_until("c")
            self.play(Write(expl), run_time=2.5)
            s.wait_until("old")
            self.play(Create(ax2), Create(ax3), FadeIn(t2, t3, m_l, m_l3), run_time=1)
            self.play(LaggedStart(*[Create(b) for b in bars_old], lag_ratio=0.02), Create(so), FadeIn(lo), run_time=2.5)
            s.wait_until("new")
            self.play(bars_old.animate.set_stroke(opacity=0.35),
                      LaggedStart(*[Create(b) for b in bars_new], lag_ratio=0.02), Create(sn), FadeIn(ln),
                      run_time=2.5)
            s.wait_until("fin")
            self.play(Indicate(conj, color=YELLOW_3B, scale_factor=1.05), run_time=1.5)
        self.play(FadeOut(Group(*self.mobjects)))

        # ------------------------------------------------------------ the theorem
        thm = VGroup(
            Tex(r"\textbf{Theorem.} For each $k\ge3$ there are $C_k,c_k,\varepsilon_k>0$ with", font_size=38),
            MathTex(r"r_k(N)\ \le\ C_k\,N\,\exp\!\big(-c_k(\log N)^{\varepsilon_k}\big).", font_size=44),
            Tex(r"\textbf{Corollary.} Erd\H{o}s's reciprocal-sum conjecture is true.", font_size=38,
                color=YELLOW_3B),
        ).arrange(DOWN, buff=0.35)
        with self.say("That is the theorem in the new manuscript: for every k, r k of N is at most N times "
                      "e to the minus a power of log N. {c}The corollary is the conjecture itself.") as s:
            self.play(Write(thm[:2]), run_time=3)
            s.wait_until("c")
            self.play(FadeIn(thm[2], shift=UP * 0.2))
        self.play(FadeOut(thm))

        # ------------------------------------------------------------ proof idea: density increment
        hdr = Tex("The engine: density increments", font_size=42, color=YELLOW_3B).to_edge(UP, buff=0.35)
        rng = np.random.default_rng(11)
        bar = Rectangle(width=11, height=0.5, stroke_color=GREY_B).shift(UP * 1.2)
        pts = VGroup(*[Line(UP * 0.22, DOWN * 0.22, color=BLUE_3B, stroke_width=2).move_to(
            bar.get_left() + RIGHT * x + UP * 1.2 * 0) for x in np.sort(rng.uniform(0.1, 10.9, 70))])
        for l in pts:
            l.set_y(1.2)
        dens = ValueTracker(0.12)
        meter = Rectangle(width=0.5, height=3.2, stroke_color=GREY_B).move_to(RIGHT * 5.8 + DOWN * 1.6)
        fill = always_redraw(lambda: Rectangle(width=0.5, height=3.2 * dens.get_value(), stroke_width=0)
                             .set_fill(YELLOW_3B, 0.8).align_to(meter, DOWN).set_x(meter.get_x()))
        mlab = Tex("density", font_size=28).next_to(meter, UP, buff=0.15)
        one = MathTex("1", font_size=28).next_to(meter, LEFT, buff=0.1).align_to(meter, UP)
        zooms = VGroup()
        cur = bar
        for i, (wd, op) in enumerate([(6.5, 0.9), (3.6, 0.9), (1.9, 0.9)]):
            z = Rectangle(width=wd, height=0.5, stroke_color=YELLOW_3B, stroke_width=3).move_to(
                bar.get_center() + DOWN * (1.0 + 0.9 * i) + LEFT * (2.2 - 0.5 * i))
            zooms.add(z)
        steps = VGroup(
            Tex(r"no $k$-term progression $\Rightarrow$ a structured piece where the set is denser", font_size=30),
            Tex(r"density can't pass 1 $\Rightarrow$ only $O(\log\frac1\alpha)$ steps", font_size=30),
            Tex(r"the real cost: how much room each step eats", font_size=30, color=RED_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DL, buff=0.5)
        with self.say("How do you prove such a bound? The classic engine, going back to Klaus Roth, "
                      "is the density increment. {s1}If a set has no progressions, it must be unusually dense on some "
                      "structured piece of the interval. {z}Zoom into that piece, and repeat. "
                      "{s2}Density can never pass one, so this can only happen a limited number of times. "
                      "{s3}The real enemy is cost: each zoom shrinks the room you have, and with every past "
                      "constraint to respect, the losses pile up.") as s:
            self.play(Write(hdr), Create(bar), FadeIn(pts), Create(meter), FadeIn(mlab, one), FadeIn(fill))
            s.wait_until("s1")
            self.play(FadeIn(steps[0]))
            s.wait_until("z")
            for z, d in zip(zooms, [0.25, 0.45, 0.75]):
                self.play(TransformFromCopy(bar if z is zooms[0] else zooms[list(zooms).index(z) - 1], z),
                          dens.animate.set_value(d), run_time=1.1)
            s.wait_until("s2")
            self.play(FadeIn(steps[1]))
            s.wait_until("s3")
            self.play(FadeIn(steps[2]))
        self.play(FadeOut(VGroup(bar, pts, meter, mlab, one, zooms, steps)), FadeOut(fill))

        new_ideas = VGroup(
            Tex(r"\textbf{Triangular polynomial cells}: each zoom adds constraints", font_size=32),
            MathTex(r"\|b_h - C_h(u,b_1,\dots,b_{h-1}) - l_h\|_\infty \le w_h", font_size=34, color=BLUE_3B),
            Tex(r"old constraints kept \emph{exactly}; precision budgeted weight by weight", font_size=30,
                color=GREY_A),
            Tex(r"\textbf{Inputs}: Leng--Sah--Sawhney inverse theorem (nilsequences),", font_size=30),
            Tex(r"Kelley--Meka style sifting, Schoen--Sisask almost-periodicity", font_size=30),
            Tex(r"total loss stays polynomial in $\log\frac1\alpha$ $\Rightarrow$ a quasipolynomial bound",
                font_size=32, color=YELLOW_3B),
        ).arrange(DOWN, buff=0.28).next_to(hdr, DOWN, buff=0.5)
        with self.say("The new proof's contribution is cost control. {cells}Each zoom lands in a triangular "
                      "polynomial cell, where integer blocks are pinned down one after another by polynomial "
                      "constraints. {exact}Old constraints are kept exactly, never approximately, and the precision "
                      "lost at each layer is bounded only in terms of the layers above it. "
                      "{inp}The heavy machinery comes from recent breakthroughs: the Leng, Sah, Sawhney inverse "
                      "theorem, and ideas from Kelley and Meka's work on three-term progressions. "
                      "{tot}The upshot: the total loss stays polynomial in log one over the density, "
                      "which is exactly what the bound needs.") as s:
            s.wait_until("cells")
            self.play(FadeIn(new_ideas[0]), Write(new_ideas[1]), run_time=2)
            s.wait_until("exact")
            self.play(FadeIn(new_ideas[2]))
            s.wait_until("inp")
            self.play(FadeIn(new_ideas[3:5]))
            s.wait_until("tot")
            self.play(Write(new_ideas[5]), run_time=2)
        self.play(FadeOut(VGroup(hdr, new_ideas)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Every set with $\sum 1/a=\infty$ has progressions of every length",
             r"$r_k(N)\le C_kN\exp(-c_k(\log N)^{\varepsilon_k})$ for every $k\ge3$",
             r"Also: quasipolynomial van der Waerden bounds",
             r"Manuscript: 198 pages, produced by an OpenAI model"],
            True, r"\emph{Quasipolynomial Bounds for Arithmetic Progressions} (Sept.\ 2026)")
        with self.say("Bonus consequences include quasipolynomial bounds for van der Waerden numbers, "
                      "and a new proof of the Green Tao theorem. {c}The manuscript is a hundred and ninety-eight "
                      "pages, written by an OpenAI model, {l}and the reciprocal-sum statement itself has been "
                      "formalized in the Lean proof assistant. If it stands, {ERDOS}'s prize problem is solved.".replace(
                          "{ERDOS}", ERDOS)) as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
