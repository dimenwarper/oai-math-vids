from pathlib import Path

import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(Path(__file__).parent / "data" / "v12.npz")

GOLD = "[Goldfeld](/ɡˈOldfɛld/)"
TUN = "[Tunnell](/tənˈɛl/)"
SELM = "[Selmer](/sˈɛlməɹ/)"
CHEV = "[Chevalley](/ʃəvˈæli/)"
HEEG = "[Heegner](/hˈAɡnəɹ/)"

CLS_COL = [BLUE_3B, YELLOW_3B, RED_3B]


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "006", r"Goldfeld's Conjecture",
                          r"For every elliptic curve: half its twists have rank 0, half have rank 1")
        with self.say("Twist one elliptic curve in every possible way. How often is the rank zero, and how often "
                      "is it one?"):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ congruent numbers
        def tri(a, b, labs, area, pos, sc):
            A, B, C = pos, pos + RIGHT * a * sc, pos + UP * b * sc
            poly = Polygon(A, B, C, color=BLUE_3B, stroke_width=4).set_fill(BLUE_3B, 0.2)
            ra = Square(0.18, color=GREY_B, stroke_width=2).move_to(A + np.array([0.09, 0.09, 0]))
            la = MathTex(labs[0], font_size=30).next_to(Line(A, B), DOWN, buff=0.12)
            lb = MathTex(labs[1], font_size=30).next_to(Line(A, C), LEFT, buff=0.12)
            lc = MathTex(labs[2], font_size=30).move_to((B + C) / 2 + 0.38 * normalize(np.array([b, a, 0])))
            ar = MathTex(rf"\text{{area}}={area}", font_size=34, color=YELLOW_3B).move_to(
                A + (B - A) / 3 + (C - A) / 3 + RIGHT * 0.15)
            return VGroup(poly, ra, la, lb, lc, ar)

        t6 = tri(4, 3, ["4", "3", "5"], "6", LEFT * 6.0 + UP * 0.2, 0.62)
        t5 = tri(20 / 3, 1.5, [r"\tfrac{20}{3}", r"\tfrac32", r"\tfrac{41}{6}"], "5", LEFT * 1.6 + UP * 0.6, 0.55)
        t5[5].next_to(t5[0], RIGHT, buff=0.3).shift(DOWN * 0.2)
        no = Tex(r"areas $1,2,3$: impossible", font_size=32, color=RED_3B).move_to(RIGHT * 4.6 + UP * 2.6)
        q = Tex(r"Which whole numbers $n$ are the area of a right triangle with rational sides?", font_size=34
                ).to_edge(UP, buff=0.4)
        crv = VGroup(
            Tex(r"$n$ is such an area $\iff$ the curve", font_size=32),
            MathTex(r"E_n:\ y^2=x^3-n^2x", font_size=42, color=TEAL_3B),
            Tex(r"has infinitely many rational points (positive rank)", font_size=32),
            Tex(r"Every $E_n$ is a \emph{quadratic twist} of $y^2=x^3-x$", font_size=32, color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.say("Which whole numbers are the area of a right triangle with rational sides? {six}Six is: three, "
                      "four, five. {five}Five is too, with sides three halves, twenty thirds, and forty-one sixths. "
                      "{one}But one, two and three are not. {c}This old puzzle hides an elliptic curve. A number n is "
                      "such an area exactly when the curve y squared equals x cubed minus n squared x has infinitely "
                      "many rational points, that is, positive rank. {tw}And all these curves are quadratic twists of a "
                      "single curve, y squared equals x cubed minus x.") as s:
            self.play(FadeIn(q))
            s.wait_until("six")
            self.play(DrawBorderThenFill(t6[0]), FadeIn(t6[1:]))
            s.wait_until("five")
            self.play(DrawBorderThenFill(t5[0]), FadeIn(t5[1:]))
            s.wait_until("one")
            self.play(FadeIn(no))
            s.wait_until("c")
            self.play(FadeIn(crv[:3]), run_time=1.5)
            s.wait_until("tw")
            self.play(FadeIn(crv[3]))
        self.play(FadeOut(VGroup(q, t6, t5, no, crv)))

        # ------------------------------------------------------------ the grid of twists
        ns, cls = D["ns"][:120], D["cls"][:120]
        cells = VGroup()
        for n, c in zip(ns, cls):
            sq = Square(0.5, stroke_width=1.5, stroke_color=BLACK).set_fill(CLS_COL[c], 0.85)
            lab = Text(str(n), font_size=15, color=BLACK).move_to(sq)
            cells.add(VGroup(sq, lab))
        cells.arrange_in_grid(rows=8, cols=15, buff=0.04).move_to(LEFT * 2.5 + DOWN * 0.3)
        hdr = Tex(r"squarefree $n$, colored by what the $L$-function of $E_n$ says", font_size=32).to_edge(UP, buff=0.35)
        leg = VGroup(
            Tex(r"\textbf{sign $-1$}:\\ odd analytic rank ($\ge1$)", font_size=28, color=YELLOW_3B),
            Tex(r"\textbf{sign $+1$}, $L(E_n,1)\neq0$:\\ analytic rank $0$", font_size=28, color=BLUE_3B),
            Tex(r"\textbf{sign $+1$}, $L(E_n,1)=0$:\\ analytic rank $\ge2$", font_size=28, color=RED_3B),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).next_to(cells, RIGHT, buff=0.5)
        ycells = VGroup(*[c for c, k in zip(cells, cls) if k == 1])
        bcells = VGroup(*[c for c, k in zip(cells, cls) if k == 0])
        rcells = VGroup(*[c for c, k in zip(cells, cls) if k == 2])
        tn = Tex(r"(Tunnell's criterion decides $L(E_n,1)=0$ exactly,\\ by counting solutions of $x^2+2y^2+8z^2=n$ "
                 r"and similar equations)", font_size=24, color=GREY_B).to_edge(DOWN, buff=0.3)
        if tn.width > 12.5:
            tn.scale_to_fit_width(12.5)
        with self.say("Here are the first hundred and twenty squarefree numbers n, colored by what the L-function of "
                      "the twisted curve says. {y}For the yellow ones, the sign in the functional equation is minus "
                      "one, which forces the analytic rank to be odd, so at least one. {b}For the blue ones, the sign "
                      "is plus one, and the L-value at the center is not zero, which can be checked exactly using "
                      f"{TUN}'s criterion: analytic rank zero. {{r}}The few red ones have sign plus one, but a "
                      "vanishing L-value: analytic rank at least two, like thirty-four, forty-one and sixty-five.") as s:
            self.play(FadeIn(hdr))
            self.play(LaggedStart(*[FadeIn(c[0].copy().set_fill(GREY_D, 0.8)) for c in cells], lag_ratio=0.005),
                      run_time=1)
            s.wait_until("y")
            self.play(FadeIn(leg[0]), LaggedStart(*[FadeIn(c) for c in ycells], lag_ratio=0.01), run_time=1.5)
            s.wait_until("b")
            self.play(FadeIn(leg[1]), LaggedStart(*[FadeIn(c) for c in bcells], lag_ratio=0.01), FadeIn(tn),
                      run_time=1.5)
            s.wait_until("r")
            self.play(FadeIn(leg[2]), LaggedStart(*[FadeIn(c) for c in rcells], lag_ratio=0.05), run_time=1.5)
            self.play(*[Indicate(c, scale_factor=1.3, color=WHITE) for c in rcells[:3]])
        self.play(FadeOut(Group(*self.mobjects)))

        # ------------------------------------------------------------ Goldfeld's conjecture + data
        conj = VGroup(
            Tex(r"\textbf{Goldfeld (1979):} among the quadratic twists of any elliptic curve,", font_size=32),
            Tex(r"the average analytic rank is $\tfrac12$.", font_size=32),
            Tex(r"Density form: rank $0$ half the time, rank $1$ half the time, rank $\ge2$ density zero.",
                font_size=30, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        xs, fr = D["xs"].astype(float), D["fr"]
        keep = xs >= 100
        xs, fr = xs[keep], fr[:, keep]
        ax = Axes(x_range=[2, 6.3, 1], y_range=[0, 0.6, 0.1], x_length=9.5, y_length=3.8, tips=False,
                  axis_config={"color": GREY_B, "font_size": 22},
                  y_axis_config={"numbers_to_include": [0.1, 0.2, 0.3, 0.4, 0.5],
                                 "decimal_number_config": {"num_decimal_places": 1}}).to_edge(DOWN, buff=0.7).shift(
            LEFT * 0.7)
        ax.x_axis.add_labels({k: MathTex(f"10^{k}", font_size=24) for k in range(2, 7)})
        xl = Tex(r"$X$", font_size=28).next_to(ax.x_axis, RIGHT, buff=0.15)
        half = DashedLine(ax.c2p(2, 0.5), ax.c2p(6.3, 0.5), color=GREY_B)
        curves = VGroup(*[VMobject(color=CLS_COL[j], stroke_width=3.5).set_points_as_corners(
            [ax.c2p(np.log10(x), y) for x, y in zip(xs, fr[j])]) for j in range(3)])
        labs = VGroup(
            Tex(rf"rank $0$: {fr[0][-1]:.3f}", font_size=26, color=BLUE_3B),
            Tex(rf"odd: {fr[1][-1]:.3f}", font_size=26, color=YELLOW_3B),
            Tex(rf"rank $\ge2$: {fr[2][-1]:.3f}", font_size=26, color=RED_3B))
        for l_, c_ in zip(labs, curves):
            l_.next_to(c_.get_end(), RIGHT, buff=0.12)
        labs[0].shift(DOWN * 0.12)
        labs[1].shift(UP * 0.12)
        yl = Tex(r"fraction of squarefree $n\le X$ ($y^2=x^3-n^2x$)", font_size=26).next_to(ax, UP, buff=0.2).align_to(
            ax, LEFT).shift(RIGHT * 0.3)
        with self.say(f"In 1979, Dorian {GOLD} conjectured that, for any elliptic curve, the average analytic rank of "
                      "its quadratic twists is one half. The sharper density form says: rank zero half the time, "
                      "rank one half the time, and higher ranks almost never. {d}Here is the data for our family, "
                      "out to two million. The odd-sign twists sit at exactly one half. The rank zero twists climb "
                      "toward one half, and the higher-rank twists shrink, slowly.") as s:
            self.play(FadeIn(conj[:2]))
            self.play(FadeIn(conj[2]))
            s.wait_until("d")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(half))
            self.play(*[Create(c) for c in curves], run_time=3.5, rate_func=linear)
            self.play(FadeIn(labs))
        self.play(FadeOut(VGroup(conj, ax, xl, yl, half, curves, labs)))

        # ------------------------------------------------------------ history
        hist = VGroup(
            Tex(r"Positive proportions of ranks $0$ and $1$: known only for special families", font_size=32),
            Tex(r"(e.g.\ Vatsal for $X_0(19)$; Kriz--Li for curves with a rational 3-isogeny)", font_size=28,
                color=GREY_A),
            Tex(r"Smith: the \emph{Selmer corank}, an algebraic stand-in for the rank, is", font_size=32),
            Tex(r"$0$ half the time and $1$ half the time, for every curve", font_size=32),
            Tex(r"(and so Birch--Swinnerton-Dyer would imply Goldfeld's conjecture)", font_size=28, color=GREY_A),
            Tex(r"Missing link: from Selmer corank to \emph{analytic} rank", font_size=34, color=YELLOW_3B),
        ).arrange(DOWN, buff=0.2)
        hist[2].shift(DOWN * 0.25)
        hist[3:5].shift(DOWN * 0.25)
        hist[5].shift(DOWN * 0.5)
        with self.say("For decades, positive proportions of rank zero and rank one twists were proved only in special "
                      "families. {s}Then Alexander Smith proved that an algebraic stand-in for the rank, the two-power "
                      f"{SELM} corank, is zero half the time and one half the time, for every elliptic curve. So the "
                      "Birch and Swinnerton-Dyer conjecture would imply Goldfeld's conjecture. {m}The missing link was "
                      "unconditional: getting from the Selmer corank to the analytic rank.") as s:
            self.play(FadeIn(hist[:2]))
            s.wait_until("s")
            self.play(FadeIn(hist[2:4]))
            self.play(FadeIn(hist[4]))
            s.wait_until("m")
            self.play(FadeIn(hist[5]))
        self.play(FadeOut(hist))

        # ------------------------------------------------------------ theorem
        thm = VGroup(Tex(r"\textbf{Theorem.} For every elliptic curve $E/\mathbb{Q}$ and $j\in\{0,1\}$:", font_size=36),
                     MathTex(r"\lim_{X\to\infty}\frac{\#\{d\ \text{squarefree},\ |d|\le X:\ \mathrm{ord}_{s=1}"
                             r"L(E^{(d)},s)=j\}}{\#\{d\ \text{squarefree},\ |d|\le X\}}=\frac12", font_size=36),
                     ).arrange(DOWN, buff=0.35)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3)).shift(UP * 1.2)
        extra = VGroup(
            Tex(r"Companion manuscript: the mean analytic rank of the twists tends to $\tfrac12$", font_size=30),
            Tex(r"For almost all twists: analytic rank $=$ Mordell--Weil rank, and Sha is finite", font_size=30),
        ).arrange(DOWN, buff=0.25).next_to(tb, DOWN, buff=0.5)
        with self.say("A manuscript in OpenAI's math catalogue claims to supply that link, and with it, Goldfeld's "
                      "conjecture. {t}For every elliptic curve over the rationals, twists of analytic rank zero, and "
                      "twists of analytic rank one, each make up exactly half, counting signed squarefree twists by "
                      "size. {m}A companion manuscript adds the tail estimate needed for the average: the mean analytic "
                      "rank tends to one half.") as s:
            s.wait_until("t")
            self.play(Write(tb), run_time=3)
            s.wait_until("m")
            self.play(FadeIn(extra))
        self.play(FadeOut(VGroup(tb, extra)))

        # ------------------------------------------------------------ the 2-converse and the cube
        conv = VGroup(
            MathTex(r"\text{Smith: } \mathrm{corank}\,\mathrm{Sel}_{2^\infty}\in\{0,1\}\text{, half each}", font_size=34),
            MathTex(r"+\quad\textbf{2-converse: }\ \mathrm{corank}\,\mathrm{Sel}_{2^\infty}(E)=r\in\{0,1\}"
                    r"\ \Rightarrow\ \mathrm{ord}_{s=1}L(E,s)=r", font_size=34, color=YELLOW_3B),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(UP, buff=0.3)
        org = LEFT * 5.9 + DOWN * 1.7
        e1, e2, e3 = RIGHT * 2.5, UP * 2.0, np.array([1.05, 0.8, 0])
        verts = {}
        for x1 in (0, 1):
            for x2 in (0, 1):
                for x3 in (0, 1):
                    verts[(x1, x2, x3)] = org + x1 * e1 + x2 * e2 + x3 * e3
        edges = VGroup()
        for v in verts:
            for i in range(3):
                if v[i] == 0:
                    w = list(v)
                    w[i] = 1
                    edges.add(Line(verts[v], verts[tuple(w)], color=GREY_B, stroke_width=2.5))
        vd = {v: Dot(p, radius=0.11, color=GREY_B) for v, p in verts.items()}
        names = {}
        for v, p in verts.items():
            if v == (0, 0, 0):
                t_ = MathTex(r"E", font_size=32, color=YELLOW_3B)
            else:
                qs = "".join(rf"q_{i + 1}^*" for i in range(3) if v[i])
                t_ = MathTex(rf"E^{{({qs})}}", font_size=26)
            t_.next_to(p, DL if v[0] == 0 else DR, buff=0.08)
            names[v] = t_
        cube = VGroup(edges, *vd.values(), *names.values())
        info = VGroup(
            Tex(r"vertex $x\in\{0,1\}^b$: twist $E$ by $\prod_i (q_i^*)^{x_i}$", font_size=27),
            Tex(r"$u_x$: a 2-adic number detecting the central\\ $L$-value (Kato class) or $L'$ (Heegner point)",
                font_size=27),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        good = Tex(r"$x\neq0$: $u_x\neq0$, with $2$-adic valuation $\le B$", font_size=27, color=GREEN_3B)
        cw = Tex(r"Chevalley--Warning: low-degree equations over\\ $\mathbb{F}_2$ on a big cube have an "
                 r"\emph{even} number\\ of solutions", font_size=27, color=BLUE_3B)
        fin = Tex(r"$\Rightarrow$ some $x\neq0$ has $u_x\equiv u_0$ to high 2-adic\\ precision, so $u_0\neq0$: "
                  r"$E$ has the\\ predicted analytic rank", font_size=27, color=YELLOW_3B)
        txtblk = VGroup(info, good, cw, fin).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        txtblk.move_to(RIGHT * 2.9 + DOWN * 0.55)
        if txtblk.width > 7.4:
            txtblk.scale_to_fit_width(7.4)
        with self.say("The proof combines Smith's statistics with a pointwise theorem, the two-converse: if the "
                      "two-power Selmer corank of any elliptic curve is zero or one, then so is its analytic rank, "
                      "and they agree. {cube}To prove it, the manuscript surrounds the curve with a cube of twists. "
                      "Pick auxiliary primes; each vertex of a binary cube twists the curve by a product of them. The "
                      "base vertex is the curve itself. {u}At each vertex sits a two-adic number that detects the "
                      f"central L-value, through a Kato class, or its derivative, through a {HEEG} point. "
                      "{g}Using modular forms and carefully chosen prime configurations, every other vertex is shown to "
                      f"have a nonzero number, not too divisible by two. {{cw}}Then a counting trick of {CHEV} and "
                      "Warning: the conditions for a vertex to match the base to high two-adic precision are "
                      "low-degree equations over the field with two elements, and on a large enough cube their "
                      "solutions come in even number. {f}The base is one solution, so another vertex matches it. "
                      "That vertex is not too divisible by two, so neither is the base. Its number is nonzero, and the "
                      "curve has exactly the predicted rank.") as s:
            self.play(FadeIn(conv[0]))
            self.play(FadeIn(conv[1]))
            s.wait_until("cube")
            self.play(Create(edges), *[FadeIn(d) for d in vd.values()], run_time=1.5)
            self.play(*[FadeIn(t_) for t_ in names.values()])
            self.play(Indicate(names[(0, 0, 0)], color=YELLOW_3B), vd[(0, 0, 0)].animate.set_color(YELLOW_3B))
            s.wait_until("u")
            self.play(FadeIn(info))
            s.wait_until("g")
            self.play(*[vd[v].animate.set_color(GREEN_3B).scale(1.3) for v in vd if v != (0, 0, 0)], FadeIn(good))
            s.wait_until("cw")
            self.play(FadeIn(cw))
            s.wait_until("f")
            link = DashedLine(verts[(0, 0, 0)], verts[(1, 1, 0)], color=YELLOW_3B, stroke_width=4)
            self.play(Create(link))
            self.play(vd[(0, 0, 0)].animate.set_color(GREEN_3B).scale(1.5), FadeIn(fin))
        self.play(FadeOut(Group(*self.mobjects)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"For every $E/\mathbb{Q}$: twists of analytic rank $0$ and of rank $1$ each have density $\tfrac12$",
             r"Companion: mean analytic rank of twists $\to\tfrac12$",
             r"Key step: the 2-converse; combined with Smith's Selmer distribution theorem",
             r"Manuscript: 130 pages, produced by an OpenAI model"],
            False, r"\emph{Goldfeld's analytic density conjecture and the 2-converse} (Sept.\ 2026)")
        with self.say("A caveat. The hundred-and-thirty page proof has not been formalized, and it uses Smith's Selmer "
                      "distribution theorem as an input, so it needs careful checking by experts. {c}If it holds, "
                      "Goldfeld's prediction is now a theorem for every elliptic curve over the rationals: half rank "
                      "zero, half rank one, and the rest, a vanishing fraction.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("c")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
