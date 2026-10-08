from pathlib import Path

import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(Path(__file__).parent / "data" / "v34.npz")
SIN = "[Sinai](/sˈinˌI/)"
CHI = "[Chirikov](/ʧˈɪɹɪkˌɔf/)"
LYA = "[Lyapunov](/ljˈɑpʊnˌɔf/)"
PES = "[Pesin](/pˈɛsɪn/)"
ORB_COLS = [BLUE_3B, YELLOW_3B, TEAL_3B, RED_3B, GREEN_3B, ORANGE_3B, PURPLE_3B]


def px(base):
    return max(1, int(round(base * config.pixel_width / 1920)))


class Video(NarratedScene):
    def cloud(self, pts01, center, side, color=WHITE, size=None, cols=None):
        pm = PMobject(stroke_width=size or px(4))
        P = np.c_[center[0] + (pts01[:, 0] - 0.5) * side, center[1] + (pts01[:, 1] - 0.5) * side,
                  np.zeros(len(pts01))]
        pm.add_points(P, color=color)
        return pm

    def construct(self):
        card = title_card(self, "146", "Chaos With Positive Area",
                          r"The standard map has positive metric entropy for every large parameter")
        with self.say(f"The standard map, and a conjecture of Yakov {SIN}."):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.4)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ the map, a blob stretched
        side = 5.4
        c0 = np.array([-3.4, -0.3, 0])
        sq = Square(side, color=GREY_B, stroke_width=2).move_to(c0)
        eq = MathTex(r"y' = y + k\sin(2\pi x)", r"\\", r"x' = x + y'", font_size=42).to_corner(UR, buff=0.6)
        eqn = Tex(r"(both mod 1: a torus)", font_size=28, color=GREY_A).next_to(eq, DOWN, buff=0.2)
        blob = D["blob"]
        clouds = [self.cloud(blob[i], c0, side, YELLOW_3B) for i in range(len(blob))]
        steps_l = [Tex(rf"step {i}", font_size=30, color=YELLOW_3B).next_to(sq, DOWN, buff=0.15) for i in range(len(blob))]
        area = Tex(r"area is preserved,\\ but shapes are stretched\\ and folded", font_size=30).next_to(eqn, DOWN,
                                                                                                    buff=0.8)
        with self.say("Here is one of the simplest systems that shows chaos. A point moves on a square whose "
                      "opposite edges are glued together. {m}At each step its height gets a kick, k times the sine "
                      "of its horizontal position, and then it slides sideways by its new height. This is the "
                      f"standard map, studied by Boris {CHI} as a model of instability in physics. "
                      "{blob}Start with a small blob of points. {fold}Step by step, it keeps its area, but it is "
                      "stretched and folded into a long thin filament.") as s:
            self.play(Create(sq))
            s.wait_until("m")
            self.play(Write(eq), FadeIn(eqn))
            s.wait_until("blob")
            self.add(clouds[0])
            self.play(FadeIn(steps_l[0]))
            s.wait_until("fold")
            for i in range(1, len(blob)):
                self.play(FadeOut(clouds[i - 1]), FadeIn(clouds[i]), FadeOut(steps_l[i - 1]), FadeIn(steps_l[i]),
                          run_time=0.9)
                self.wait(0.3)
            self.play(FadeIn(area))
        self.play(FadeOut(Group(sq, eq, eqn, area, clouds[-1], steps_l[-1])))

        # ------------------------------------------------------------ phase portraits
        ks = D["ks"]
        ports = D["ports"]
        pside = 2.95
        cents = [np.array([-4.65 + i * 3.1, 0.1, 0]) for i in range(4)]
        frames = VGroup(*[Square(pside, color=GREY_D, stroke_width=1.5).move_to(c) for c in cents])
        panels = []
        for j in range(4):
            pm = PMobject(stroke_width=px(2))
            for o in range(ports.shape[1]):
                P = ports[j, o]
                pm.add_points(np.c_[cents[j][0] + (P[:, 0] - 0.5) * pside, cents[j][1] + (P[:, 1] - 0.5) * pside,
                                    np.zeros(len(P))], color=ORB_COLS[o % len(ORB_COLS)])
            panels.append(pm)
        klab = VGroup(*[MathTex(rf"k={k:g}", font_size=34).next_to(frames[j], DOWN, buff=0.2) for j, k in enumerate(ks)])
        desc = VGroup(Tex("regular", font_size=28, color=GREY_A), Tex("islands appear", font_size=28, color=GREY_A),
                      Tex("a chaotic sea", font_size=28, color=GREY_A), Tex(r"mostly sea", font_size=28, color=GREY_A))
        for j in range(4):
            desc[j].next_to(frames[j], UP, buff=0.2)
        with self.say("Now follow many starting points for a long time, each orbit in its own color. "
                      "{p}When the kick is weak, orbits trace smooth curves: the motion is regular. "
                      "{mid}As k grows, the curves break up, and a chaotic sea spreads between islands of regular "
                      "motion. {big}For large k, the sea seems to fill almost everything, although Pedro Duarte showed "
                      "in 1994 that islands of regular motion still turn up.") as s:
            self.play(Create(frames))
            s.wait_until("p")
            self.play(FadeIn(panels[0]), FadeIn(klab[0]), FadeIn(desc[0]))
            s.wait_until("mid")
            self.play(FadeIn(panels[1]), FadeIn(klab[1]), FadeIn(desc[1]))
            self.play(FadeIn(panels[2]), FadeIn(klab[2]), FadeIn(desc[2]))
            s.wait_until("big")
            self.play(FadeIn(panels[3]), FadeIn(klab[3]), FadeIn(desc[3]))
        self.play(FadeOut(Group(frames, klab, desc, *panels)))

        # ------------------------------------------------------------ the question; growth of derivatives
        ax = Axes(x_range=[0, 48, 8], y_range=[0, 48, 8], x_length=5.6, y_length=4.6, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": True, "font_size": 24}).shift(LEFT * 3.2 + DOWN * 0.5)
        xl = MathTex("n", font_size=32).next_to(ax.x_axis, RIGHT, buff=0.15)
        yl = MathTex(r"\log_M \|Df^n\|", font_size=30).next_to(ax.y_axis, UP, buff=0.15)
        maxl = ax.plot(lambda t: t, x_range=[0, 48], color=GREY_B, stroke_width=2)
        maxt = Tex(r"maximal rate", font_size=26, color=GREY_B).move_to(ax.c2p(31, 43))
        curves = D["curves"]
        cv = VGroup(*[VMobject(color=ORB_COLS[i], stroke_width=3).set_points_as_corners(
            [ax.c2p(0, 0)] + [ax.c2p(n + 1, curves[i, n]) for n in range(curves.shape[1])]) for i in range(curves.shape[0])])
        cvl = Tex(r"six orbits, $k=2$", font_size=26).next_to(ax, DOWN, buff=0.45)
        right = VGroup(
            Tex(r"Lyapunov exponent $\lambda$: nearby", font_size=30),
            Tex(r"points separate like $e^{\lambda n}$", font_size=30),
            Tex(r"metric entropy $=$ average of $\lambda$ over area", font_size=30, color=YELLOW_3B),
            Tex(r"(Pesin's formula)", font_size=26, color=GREY_A),
            Tex(r"\textbf{Sinai's conjecture:} positive metric", font_size=30),
            Tex(r"entropy for a set of $k$ of positive length", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.4).shift(UP * 0.9)
        right[3].shift(RIGHT * 0.3)
        hard = VGroup(*[Tex(t, font_size=28, color=GREY_A) for t in [
            r"already known: chaos on zero area,", r"full dimension, topological entropy,",
            r"noise-driven chaos. None of these settles it."]]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        hard.next_to(right, DOWN, buff=0.45).align_to(right, LEFT)
        with self.say(f"How do you measure chaos? {{ly}}Take two nearby starting points. If their distance grows like e "
                      f"to the lambda n, lambda is called the {LYA} exponent. {{ent}}The metric entropy, measured with "
                      f"area, is the average of that exponent over the square, by {PES}'s formula. {{sin}}{SIN} "
                      "conjectured that for a set of parameters k of positive length, this entropy is positive. "
                      "{cv}Computers make it look obvious: along these orbits, derivatives grow at a steady rate. "
                      "{hard}But a proof has to rule out that the chaos lives on a set of zero area. Invariant sets "
                      "of full dimension, positive topological entropy, and positive exponents after adding noise "
                      "had all been established, and none of them settles the question.") as s:
            s.wait_until("ly")
            self.play(FadeIn(right[0:2]))
            s.wait_until("ent")
            self.play(FadeIn(right[2:4]))
            s.wait_until("sin")
            self.play(FadeIn(right[4:6]))
            s.wait_until("cv")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(maxl), FadeIn(maxt))
            self.play(LaggedStart(*[Create(c) for c in cv], lag_ratio=0.2), FadeIn(cvl), run_time=3)
            s.wait_until("hard")
            self.play(FadeIn(hard))
        self.play(FadeOut(Group(ax, xl, yl, maxl, maxt, cv, cvl, right, hard)))

        # ------------------------------------------------------------ theorem
        thm = VGroup(Tex(r"\textbf{Theorem.} There is $k_0$ such that for \emph{every} $k\ge k_0$, the standard map",
                         font_size=34),
                     Tex(r"has positive metric entropy with respect to area.", font_size=34),
                     Tex(r"\mbox{Equivalently: the largest Lyapunov exponent is positive on a set of positive area.}",
                         font_size=30, color=GREY_A)).arrange(DOWN, buff=0.2)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3)).shift(UP * 1.4)
        cor = VGroup(Tex(r"Also: a positive-area ergodic component that is hyperbolic,", font_size=30, color=TEAL_3B),
                     Tex(r"split into finitely many Bernoulli pieces", font_size=30, color=TEAL_3B),
                     Tex(r"(no claim of ergodicity on the whole torus)", font_size=28, color=GREY_A)
                     ).arrange(DOWN, buff=0.15).shift(DOWN * 1.5)
        with self.say("A manuscript in OpenAI's math catalogue now proves the conjecture in a strong form. "
                      "{t}There is a threshold such that for every k beyond it, not just most k, the standard map has "
                      "positive metric entropy with respect to area. Equivalently, the largest exponent is positive on "
                      "a set of positive area. {c}It also gives a positive-area region where the map is hyperbolic and "
                      "ergodic. The paper makes no claim that the whole torus is chaotic.") as s:
            s.wait_until("t")
            self.play(Write(thm[:2]), Create(tb[1]), run_time=2.5)
            self.play(FadeIn(thm[2]))
            s.wait_until("c")
            self.play(FadeIn(cor))
        self.play(FadeOut(Group(tb, cor)))

        # ------------------------------------------------------------ proof: growth as a distance on time
        hdr = Tex("The proof: measuring lost growth", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.4)
        mats = VGroup(
            MathTex(r"Df^n \sim A_n\cdots A_2A_1,\qquad A_i=\begin{pmatrix} 2+2\pi k\cos 2\pi x_i & -1\\ 1 & 0\end{pmatrix}",
                    font_size=36),
            MathTex(r"g(i,j)=\log_M\|A_j\cdots A_{i+1}\|\ \in\ [0,\,|i-j|],\qquad M=2\pi k+4", font_size=36),
            Tex(r"$g$ behaves like a distance on time (triangle inequality)", font_size=30, color=GREY_A),
            MathTex(r"\text{shortfall } e_n = 1-\frac{\mathbb{E}\,g(0,n)}{n}", font_size=38, color=YELLOW_3B),
        ).arrange(DOWN, buff=0.25).next_to(hdr, DOWN, buff=0.35)
        with self.say("The proof works with the derivative directly. {m}Along an orbit, it is a product of two by two "
                      "matrices of determinant one, each stretching by at most M, about two pi k. {g}The logarithm of "
                      "the stretching between two times behaves like a distance on time. {e}The key quantity is the "
                      "shortfall: how far the average growth over n steps falls below the maximal rate.") as s:
            self.play(Write(hdr))
            s.wait_until("m")
            self.play(Write(mats[0]))
            s.wait_until("g")
            self.play(Write(mats[1]), FadeIn(mats[2]))
            s.wait_until("e")
            self.play(Write(mats[3]))
        self.play(FadeOut(mats))

        ax2 = Axes(x_range=[0, 6, 1], y_range=[0, 1.05, 0.25], x_length=6.0, y_length=4.0, tips=False,
                   axis_config={"color": GREY_B}, y_axis_config={"include_numbers": True, "font_size": 24,
                                                                 "decimal_number_config": {"num_decimal_places": 2}}
                   ).shift(LEFT * 2.9 + DOWN * 0.7)
        xt = VGroup(*[MathTex(str(2 ** j), font_size=24).next_to(ax2.c2p(j, 0), DOWN, buff=0.15) for j in range(7)])
        xl2 = Tex(r"$n$ (log scale)", font_size=26).next_to(ax2.x_axis, DOWN, buff=0.5)
        yl2 = MathTex("e_n", font_size=32).next_to(ax2.y_axis, UP, buff=0.15)
        nn = np.log2(np.arange(1, 65))
        c2 = VMobject(color=BLUE_3B, stroke_width=4).set_points_as_corners([ax2.c2p(a, b) for a, b in zip(nn, D["e2"])])
        c8 = VMobject(color=TEAL_3B, stroke_width=4).set_points_as_corners([ax2.c2p(a, b) for a, b in zip(nn, D["e8"])])
        l2 = MathTex("k=2", font_size=28, color=BLUE_3B).next_to(c2.get_end(), RIGHT, buff=0.1)
        l8 = MathTex("k=8", font_size=28, color=TEAL_3B).next_to(c8.get_end(), RIGHT, buff=0.1)
        hyp = ax2.plot(lambda t: 0.08 + 0.9 / (1 + np.exp(-2.2 * (t - 3.4))), x_range=[0, 6], color=RED_3B,
                       stroke_width=3)
        hyp = DashedVMobject(hyp, num_dashes=40)
        hl = Tex(r"if the exponent were zero:\\ $e_n\to 1$", font_size=26, color=RED_3B).next_to(ax2.c2p(4.4, 0.92), UP,
                                                                                               buff=0.15)
        num = Tex(r"computed from 20\,000\\ random starts", font_size=24, color=GREY_B).move_to(ax2.c2p(1.4, 0.8))
        ing = VGroup(
            Tex(r"\textbf{1. Cancellations are rare.}", font_size=30),
            Tex(r"Two long stretches that each grow", font_size=28),
            Tex(r"near the maximal rate almost never", font_size=28),
            Tex(r"cancel when joined: probability $\le Ce^{-\gamma n}$", font_size=28),
            Tex(r"\textbf{2. Bridges decouple.}", font_size=30),
            Tex(r"The two ends of a fast-growing stretch", font_size=28),
            Tex(r"obey a weighted product estimate,", font_size=28),
            Tex(r"with no mixing assumed", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.3)
        ing[4:].shift(DOWN * 0.4)
        tl = VGroup(Line(LEFT * 1.6, ORIGIN, color=GREEN_3B, stroke_width=7), Line(ORIGIN, RIGHT * 1.6, color=GREEN_3B,
                                                                                    stroke_width=7))
        tl.next_to(ing[3], DOWN, buff=0.15)
        with self.say("For a positive exponent, the shortfall should level off below one, as it does in these "
                      "computations. {hyp}If the exponent were zero, the shortfall would have to climb all the way to "
                      "one. {i1}The proof has two quantitative ingredients. First, cancellations are rare: two long "
                      "stretches that each grow at nearly the maximal rate almost never cancel when they are joined. "
                      "The probability is exponentially small in their length. {i2}Second, a bridge estimate: the two "
                      "ends of a fast-growing stretch obey a weighted product bound, as if nearly independent, without "
                      "assuming any mixing.") as s:
            self.play(Create(ax2), FadeIn(xt), FadeIn(xl2), FadeIn(yl2), FadeIn(num))
            self.play(Create(c2), Create(c8), FadeIn(l2), FadeIn(l8), run_time=2)
            s.wait_until("hyp")
            self.play(Create(hyp), FadeIn(hl), run_time=2)
            s.wait_until("i1")
            self.play(FadeIn(ing[0:4]), Create(tl))
            s.wait_until("i2")
            self.play(FadeIn(ing[4:]))
        self.play(FadeOut(Group(ax2, xt, xl2, yl2, c2, c8, l2, l8, hyp, hl, num, ing, tl)))

        # ------------------------------------------------------------ the contradiction
        steps = VGroup(
            Tex(r"Suppose arbitrarily large $k$ had zero exponent almost everywhere.", font_size=30),
            Tex(r"For those $k$: $e_n\to 1$ as $n$ grows; but for fixed $n$, $e_n\to0$ as $k$ grows.", font_size=30),
            Tex(r"Rare cancellations limit how much $e_n$ can jump when $n$ doubles:", font_size=30),
            Tex(r"zoom in on the dyadic range where it first rises, and rescale.", font_size=30),
            Tex(r"Limit shapes: one common rate, entirely slow, slow with one or two fast rays.", font_size=30),
            Tex(r"A telescoping balance of a capped shortfall rules them out: contradiction.", font_size=30, color=YELLOW_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(hdr, DOWN, buff=0.45)

        def shape(kind):
            g = VGroup()
            if kind == "affine":
                g.add(Line(LEFT * 1.0, RIGHT * 1.0, color=GREY_B, stroke_width=6))
            elif kind == "slow":
                g.add(Line(LEFT * 1.0, RIGHT * 1.0, color=RED_3B, stroke_width=6))
            elif kind == "one":
                g.add(Line(LEFT * 1.0, RIGHT * 0.2, color=RED_3B, stroke_width=6),
                      Arrow(RIGHT * 0.2, RIGHT * 1.2, buff=0, color=GREEN_3B, stroke_width=6))
            else:
                g.add(Arrow(LEFT * 0.4, LEFT * 1.3, buff=0, color=GREEN_3B, stroke_width=6),
                      Line(LEFT * 0.4, RIGHT * 0.4, color=RED_3B, stroke_width=6),
                      Arrow(RIGHT * 0.4, RIGHT * 1.3, buff=0, color=GREEN_3B, stroke_width=6))
            return g

        shapes = VGroup(*[shape(k) for k in ("affine", "slow", "one", "two")]).arrange(RIGHT, buff=1.0)
        shapes.next_to(steps, DOWN, buff=0.45)
        sl = VGroup(*[Tex(t, font_size=24, color=GREY_A).next_to(shapes[i], DOWN, buff=0.15)
                      for i, t in enumerate(["one common rate", "entirely slow", "one fast ray", "two fast rays"])])
        with self.say("Then comes the contradiction. {s0}Suppose arbitrarily large values of k had zero exponent. "
                      "{s1}For each of them, the shortfall climbs to one as n grows, while for any fixed n it tends to "
                      "zero as k grows. {s2}Because cancellations are rare, it cannot jump too much when n doubles. "
                      "So the proof zooms in on the range of scales where it first rises, and rescales. {s4}In the "
                      "limit, the growth patterns that matter are arrays with one common rate, entirely slow ones, and "
                      "slow intervals with one or two fast rays. {s5}A telescoping balance of a capped shortfall, using "
                      "both ingredients, shows that none of them can account for the rise. Contradiction.") as s:
            s.wait_until("s0")
            self.play(FadeIn(steps[0]))
            s.wait_until("s1")
            self.play(FadeIn(steps[1]))
            s.wait_until("s2")
            self.play(FadeIn(steps[2:4]))
            s.wait_until("s4")
            self.play(FadeIn(steps[4]), LaggedStart(*[FadeIn(sh) for sh in shapes], lag_ratio=0.3), FadeIn(sl),
                      run_time=2)
            s.wait_until("s5")
            self.play(FadeIn(steps[5]))
            self.play(*[Create(Cross(sh, stroke_color=RED_3B, stroke_width=5).scale(0.6)) for sh in shapes])
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"\mbox{For every sufficiently large $k$: positive metric entropy for area}",
             r"\mbox{Positive Lyapunov exponent on positive area; a hyperbolic Bernoulli component}",
             r"\mbox{Manuscript: 45 pages, produced by an OpenAI model, not yet peer reviewed}"],
            True, r"\mbox{\emph{Positive Metric Entropy for the Standard Map at Large Parameters} (Sept.\ 2026)}")
        with self.say("The manuscript is forty-five pages, written by an OpenAI model, and not yet peer reviewed. "
                      "{l}Its main theorem, positive entropy for every sufficiently large k, has been formalized in "
                      "the Lean proof assistant, together with the hyperbolic component. The paper gives no numerical "
                      "value for the threshold, and smaller values of k are not covered.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
