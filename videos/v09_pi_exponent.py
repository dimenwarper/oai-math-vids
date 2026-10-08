from pathlib import Path

import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(Path(__file__).parent / "data" / "v09.npz")
PI = np.pi


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "017", r"The Irrationality Exponent of $\pi$ Is 2",
                          r"$\pi$ is as hard to approximate as a ``typical'' number")
        with self.say("How well can fractions approximate pi?"):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ approximations
        nl = NumberLine(x_range=[3.13, 3.15, 0.005], length=12, include_numbers=True, font_size=24,
                        decimal_number_config={"num_decimal_places": 3}).shift(UP * 1.2)
        pid = Line(nl.n2p(PI) + UP * 0.3, nl.n2p(PI) + DOWN * 0.3, color=YELLOW_3B, stroke_width=5)
        pil = MathTex(r"\pi", color=YELLOW_3B, font_size=44).next_to(pid, UP, buff=0.1)
        approx = [("22/7", 22 / 7, BLUE_3B), ("333/106", 333 / 106, TEAL_3B), ("355/113", 355 / 113, GREEN_3B)]
        table = VGroup()
        for i, (s_, v, c) in enumerate(approx):
            num, den = s_.split("/")
            r = VGroup(MathTex(rf"\tfrac{{{num}}}{{{den}}}", font_size=40, color=c),
                       MathTex(rf"= {v:.10f}", font_size=34),
                       MathTex(rf"\text{{error}}\approx {abs(v - PI):.1e}".replace("e-0", r"\times10^{-").replace(
                           "e-", r"\times10^{-") + "}", font_size=32, color=GREY_A))
            r.arrange(RIGHT, buff=0.5)
            table.add(r)
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.35).shift(DOWN * 1.4)
        pis = MathTex(r"\pi=3.1415926535\ldots", font_size=36, color=YELLOW_3B).next_to(table, UP, buff=0.4)
        with self.say("Pi is irrational, so no fraction equals it. But some come remarkably close. "
                      "{a}Twenty-two sevenths is right to two decimal places. {b}Three hundred fifty-five over "
                      "one hundred thirteen is right to six, with a denominator of only three digits. "
                      "How much better than expected can such approximations get?") as s:
            self.play(Create(nl), Create(pid), FadeIn(pil), FadeIn(pis))
            s.wait_until("a")
            d = Dot(nl.n2p(22 / 7), color=BLUE_3B, radius=0.09)
            self.play(FadeIn(d, scale=2), FadeIn(table[0]))
            s.wait_until("b")
            d2 = Dot(nl.n2p(333 / 106), color=TEAL_3B, radius=0.09)
            d3 = Dot(nl.n2p(355 / 113), color=GREEN_3B, radius=0.09)
            self.play(FadeIn(d2, scale=2), FadeIn(table[1]))
            self.play(FadeIn(d3, scale=2), FadeIn(table[2]))
        self.play(FadeOut(VGroup(nl, pid, pil, table, pis, d, d2, d3)))

        # ------------------------------------------------------------ irrationality exponent
        defn = VGroup(
            MathTex(r"\left|\,x-\frac pq\,\right|<\frac{1}{q^{\nu}}", r"\quad\text{for infinitely many }p/q", font_size=44),
            Tex(r"\textbf{irrationality exponent} $\mu(x)$ = the largest such $\nu$", font_size=36, color=YELLOW_3B),
        ).arrange(DOWN, buff=0.4).to_edge(UP, buff=0.5)
        facts = VGroup(
            Tex(r"every irrational: $\mu\ge 2$ \quad (Dirichlet's pigeonhole argument)", font_size=32),
            Tex(r"$\sqrt2$, any algebraic number: $\mu=2$ \quad (Roth, 1955; Fields Medal)", font_size=32),
            Tex(r"almost every real number: $\mu=2$", font_size=32),
            Tex(r"Liouville numbers: $\mu=\infty$", font_size=32, color=GREY_A),
            Tex(r"$\pi$: conjectured $\mu=2$; proved only $\mu\le 7.10$", font_size=34, color=RED_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(defn, DOWN, buff=0.6)
        with self.say("The precise measure is the irrationality exponent. {d}It is the largest power nu such that "
                      "infinitely many fractions land within one over q to the nu. Bigger means more approximable. "
                      "{f}Every irrational number scores at least two, by a pigeonhole argument. "
                      "{r}Square root of two, and every algebraic number, scores exactly two: that is Roth's theorem, "
                      "which won a Fields Medal. {ae}So does almost every real number. "
                      "{lv}At the other extreme, Liouville's numbers score infinity. "
                      "{pi}And pi? Everyone expected two, but the best proven bound was about seven.") as s:
            s.wait_until("d")
            self.play(Write(defn[0]), run_time=2)
            self.play(FadeIn(defn[1]))
            s.wait_until("f")
            self.play(FadeIn(facts[0]))
            s.wait_until("r")
            self.play(FadeIn(facts[1]))
            s.wait_until("ae")
            self.play(FadeIn(facts[2]))
            s.wait_until("lv")
            self.play(FadeIn(facts[3]))
            s.wait_until("pi")
            self.play(FadeIn(facts[4]))
        self.play(FadeOut(VGroup(defn, facts)))

        # ------------------------------------------------------------ history of bounds
        ax = Axes(x_range=[1950, 2030, 10], y_range=[0, 45, 10], x_length=10, y_length=5, tips=False,
                  axis_config={"color": GREY_B, "font_size": 24},
                  x_axis_config={"numbers_to_include": [1960, 1980, 2000, 2020],
                                 "decimal_number_config": {"group_with_commas": False, "num_decimal_places": 0}},
                  y_axis_config={"numbers_to_include": [10, 20, 30, 40]}).shift(DOWN * 0.3)
        yl = MathTex(r"\mu(\pi)\le", font_size=34).next_to(ax.y_axis, UP, buff=0.15)
        hist = [(1953, 42, "Mahler"), (1974, 20, "Mignotte"), (1993, 8.016, "Hata"), (2008, 7.606, "Salikhov"),
                (2020, 7.103, "Zeilberger--Zudilin")]
        dots = VGroup(*[Dot(ax.c2p(y, v), color=BLUE_3B, radius=0.08) for y, v, _ in hist])
        labs = VGroup(*[Tex(f"{n} {v:g}", font_size=24, color=BLUE_3B).next_to(ax.c2p(y, v), UR if i < 2 else UP,
                                                                               buff=0.1)
                        for i, (y, v, n) in enumerate(hist)])
        labs[2].next_to(dots[2], DL, buff=0.08)
        labs[3].next_to(dots[3], UP, buff=0.35)
        labs[4].next_to(dots[4], UR, buff=0.08)
        two = DashedLine(ax.c2p(1950, 2), ax.c2p(2030, 2), color=GREEN_3B)
        two_l = Tex("the conjectured truth: 2", font_size=28, color=GREEN_3B).next_to(ax.c2p(1975, 2), UP, buff=0.1)
        new = Dot(ax.c2p(2026, 2), color=YELLOW_3B, radius=0.12)
        with self.say("Here is the history. {m}Kurt Mahler first proved a finite bound in 1953: forty-two. "
                      "{h}Decades of ingenious integrals brought it down to about eight, "
                      "{z}and then to seven point one, by Zeilberger and Zudilin in 2020. {t}The truth was "
                      "believed to be two. {n}A manuscript in OpenAI's math catalogue claims to prove exactly that.") as s:
            self.play(Create(ax), FadeIn(yl))
            s.wait_until("m")
            self.play(FadeIn(dots[0], scale=2), FadeIn(labs[0]))
            self.play(FadeIn(dots[1], scale=2), FadeIn(labs[1]))
            s.wait_until("h")
            self.play(FadeIn(dots[2:4]), FadeIn(labs[2:4]))
            s.wait_until("z")
            self.play(FadeIn(dots[4], scale=2), FadeIn(labs[4]))
            s.wait_until("t")
            self.play(Create(two), FadeIn(two_l))
            s.wait_until("n")
            self.play(FadeIn(new, scale=3), Flash(new, color=YELLOW_3B))
        self.play(FadeOut(VGroup(ax, yl, dots, labs, two, two_l, new)))

        thm = VGroup(Tex(r"\textbf{Theorem.} The irrationality exponent of $\pi$ is 2:", font_size=40),
                     MathTex(r"\text{for every }\nu>2:\quad \left|\,\pi-\frac pq\,\right|\ \ge\ \frac1{q^{\nu}}"
                             r"\quad\text{for all large }q", font_size=40)).arrange(DOWN, buff=0.35)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3)).shift(UP * 1.6)
        ax2 = Axes(x_range=[0, 30, 5], y_range=[1.8, 3.6, 0.5], x_length=9, y_length=3.2, tips=False,
                   axis_config={"color": GREY_B, "font_size": 22},
                   x_axis_config={"numbers_to_include": [5, 10, 15, 20, 25, 30]},
                   y_axis_config={"numbers_to_include": [2, 2.5, 3, 3.5],
                                  "decimal_number_config": {"num_decimal_places": 1}}).shift(DOWN * 1.9)
        cf = D["cf"]
        cf = cf[cf[:, 0] <= 30]
        pts = VGroup(*[Dot(ax2.c2p(x, y), radius=0.05, color=TEAL_3B) for x, y in cf])
        l2 = DashedLine(ax2.c2p(0, 2), ax2.c2p(30, 2), color=GREEN_3B)
        xl = Tex(r"digits of $q$", font_size=26).next_to(ax2.x_axis, DOWN, buff=0.35)
        yl2 = Tex(r"how good is $p/q$: exponent", font_size=26).next_to(ax2, UP, buff=0.05).align_to(ax2, LEFT)
        lab22 = MathTex(r"\tfrac{22}7", font_size=26, color=TEAL_3B).next_to(pts[0], RIGHT, buff=0.1)
        lab355 = MathTex(r"\tfrac{355}{113}", font_size=26, color=TEAL_3B).next_to(pts[2], RIGHT, buff=0.1)
        with self.say("The theorem: for any nu above two, once the denominator is large enough, "
                      "every fraction stays at least one over q to the nu away from pi. "
                      "{data}You can see the spirit of it in the best approximations, the continued fraction "
                      "convergents. Twenty-two sevenths and three fifty-five over one thirteen are lucky outliers, "
                      "{flat}but as denominators grow to thirty digits, the quality hugs two. "
                      "The theorem says it can never drift above two, in the long run.") as s:
            self.play(Write(tb), run_time=3)
            s.wait_until("data")
            self.play(Create(ax2), FadeIn(xl, yl2), Create(l2))
            self.play(FadeIn(pts[:3]), FadeIn(lab22), FadeIn(lab355))
            s.wait_until("flat")
            self.play(LaggedStart(*[FadeIn(p, scale=2) for p in pts[3:]], lag_ratio=0.05), run_time=3)
        self.play(FadeOut(VGroup(tb, ax2, pts, l2, xl, yl2, lab22, lab355)))

        # ------------------------------------------------------------ Flint–Hills
        fh = MathTex(r"\sum_{n=1}^{\infty}\frac{1}{n^3\,\sin^2 n}", font_size=54).to_edge(UP, buff=0.4).shift(LEFT * 3.5)
        q = Tex(r"Flint--Hills series:\\ does it converge?", font_size=36, color=YELLOW_3B).next_to(fh, RIGHT, buff=1)
        ax3 = Axes(x_range=[0, 5.3, 1], y_range=[0, 32, 10], x_length=9.5, y_length=4.4, tips=False,
                   axis_config={"color": GREY_B, "font_size": 22},
                   y_axis_config={"numbers_to_include": [10, 20, 30]}).shift(DOWN * 1.3)
        ax3.x_axis.add_labels({k: MathTex(f"10^{k}", font_size=24) for k in range(0, 6)})
        Sx, Sy = D["Sx"], D["Sy"]
        pts3 = [ax3.c2p(np.log10(x), y) for x, y in zip(Sx, Sy)]
        corners = [pts3[0]]
        for p in pts3[1:]:
            corners += [np.array([p[0], corners[-1][1], 0]), p]
        stair = VMobject(color=BLUE_3B, stroke_width=4).set_points_as_corners(corners)
        nl3 = Tex(r"partial sums up to $n$", font_size=26).next_to(ax3, UP, buff=0.05).align_to(ax3, LEFT)
        jump = Tex(r"$n=355$: $\sin 355\approx -0.00003$\\ because $355\approx 113\pi$", font_size=28,
                   color=RED_3B).next_to(ax3.c2p(np.log10(355), 29.4), LEFT, buff=0.3)
        conv = Tex(r"converges: $\mu(\pi)<\tfrac52$ suffices\\ (Alekseyev; Meiburg)", font_size=28,
                   color=GREEN_3B).next_to(ax3.c2p(5.3, 30.3), DOWN, buff=0.5).shift(LEFT * 1.0)
        with self.say("A bonus. {fh}This innocent-looking series, the Flint Hills series, has been a famous puzzle. "
                      "{plot}Its terms explode whenever n is very close to a multiple of pi, because then sine of n is "
                      "almost zero. {j}At n equals three hundred fifty-five, the sum leaps from about five to "
                      "about twenty-nine. Do such leaps keep coming, forever? "
                      "{c}That depends exactly on how well pi can be approximated by fractions. "
                      "Convergence was known to follow from an exponent below five halves. "
                      "With exponent two, the series converges.") as s:
            s.wait_until("fh")
            self.play(Write(fh), FadeIn(q), run_time=2)
            s.wait_until("plot")
            self.play(Create(ax3), FadeIn(nl3))
            self.play(Create(stair), run_time=4, rate_func=linear)
            s.wait_until("j")
            self.play(FadeIn(jump), Flash(ax3.c2p(np.log10(355), 29.4), color=RED_3B))
            s.wait_until("c")
            self.play(FadeIn(conv))
        self.play(FadeOut(VGroup(fh, q, ax3, stair, nl3, jump, conv)))

        # ------------------------------------------------------------ proof idea
        hdr = Tex("The proof: a determinant squeezed from both sides", font_size=40, color=YELLOW_3B).to_edge(
            UP, buff=0.35)
        step1 = VGroup(
            Tex(r"Suppose infinitely many fractions beat exponent $\nu>2$.", font_size=32),
            Tex(r"Pick several, $p_1/q_1,\ p_2/q_2,\dots$, with widely separated sizes.", font_size=32),
            MathTex(r"e^{2\pi i}=1:\quad \frac{2\pi i\,p_j}{q_j}\ \text{ is extremely close to a period of }e^{z}",
                    font_size=34, color=BLUE_3B),
        ).arrange(DOWN, buff=0.25).next_to(hdr, DOWN, buff=0.45)
        step2 = Tex(r"Build polynomials with prescribed Taylor coefficients along logarithmic curves\\"
                    r"(a new multivariable interpolation theorem), then a nonzero determinant $\Delta$.",
                    font_size=30).next_to(step1, DOWN, buff=0.45)
        nl = NumberLine(x_range=[0, 10, 1], length=10, include_tip=False, include_ticks=False, color=GREY_B).shift(
            DOWN * 2.3)
        zero = MathTex("0", font_size=30).next_to(nl.n2p(0), DOWN)
        lo = Line(nl.n2p(6.5) + UP * 0.35, nl.n2p(6.5) + DOWN * 0.35, color=GREEN_3B, stroke_width=5)
        lol = Tex(r"arithmetic: $|\Delta|\ge 1/\text{denominator}$", font_size=28, color=GREEN_3B).next_to(lo, UP,
                                                                                                          buff=0.2)
        hi = Line(nl.n2p(2.0) + UP * 0.35, nl.n2p(2.0) + DOWN * 0.35, color=RED_3B, stroke_width=5)
        hil = Tex(r"analytic: $|\Delta|\le$ tiny,\\ since the approximations\\ are so good", font_size=28,
                  color=RED_3B).next_to(hi, UP, buff=0.2)
        x = Tex(r"$\Delta$ can't be in both places: contradiction", font_size=32, color=YELLOW_3B).next_to(nl, DOWN,
                                                                                                          buff=0.4)
        with self.say("How does the proof go? {s1}Suppose infinitely many fractions beat some exponent bigger than two. "
                      "Pick several of them, with wildly different sizes. Each one makes two pi i times p over q "
                      "almost exactly a period of the exponential function. "
                      "{s2}Using a new interpolation theorem in many variables, the proof builds polynomials with "
                      "prescribed behavior along logarithmic curves, and from them a determinant that cannot be zero. "
                      "{lo}Being a nonzero number with a controlled denominator, it cannot be too small. "
                      "{hi}But because the approximations are so good, analysis shows it must be extremely small. "
                      "{x}Both cannot hold. In the spirit of Roth's theorem, the contradiction proves the exponent "
                      "is two.") as s:
            self.play(Write(hdr))
            s.wait_until("s1")
            self.play(FadeIn(step1[:2]), run_time=1.5)
            self.play(Write(step1[2]), run_time=2)
            s.wait_until("s2")
            self.play(FadeIn(step2))
            s.wait_until("lo")
            self.play(Create(nl), FadeIn(zero), Create(lo), FadeIn(lol))
            s.wait_until("hi")
            self.play(Create(hi), FadeIn(hil))
            s.wait_until("x")
            self.play(FadeIn(x))
        self.play(FadeOut(Group(*self.mobjects)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"$\mu(\pi)=2$: for every $\nu>2$, $|\pi-p/q|\ge q^{-\nu}$ for all large $q$",
             r"Corollary: the Flint--Hills series $\sum 1/(n^3\sin^2 n)$ converges",
             r"Manuscript: 23 pages, produced by an OpenAI model"],
            True, r"\emph{The irrationality exponent of pi is 2} (Sept.\ 2026)")
        with self.say("The manuscript is twenty-three pages, written by an OpenAI model, {l}and its main statement, "
                      "that the irrationality exponent of pi is two, has been formalized in the Lean proof assistant. "
                      "Pi, it turns out, is no easier to approximate than a typical number.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
