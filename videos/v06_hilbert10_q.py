import numpy as np
from manim import *
from sympy import Rational as Q

from style import *
from vo import NarratedScene

MATI = "[Matiyasevich](/mˌætijəsˈAvɪʧ/)"


def ec_add(P, R_):
    if P is None:
        return R_
    x1, y1 = P
    x2, y2 = R_
    lam = (3 * x1 * x1) / (2 * y1) if P == R_ else (y2 - y1) / (x2 - x1)
    x3 = lam * lam - x1 - x2
    return (x3, lam * (x1 - x3) - y1)


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "004", r"Hilbert's Tenth Problem over $\mathbb{Q}$",
                          "No algorithm decides whether a polynomial has a rational solution")
        with self.say("Hilbert's tenth problem, over the rational numbers."):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ Hilbert's question
        h = Tex(r"Hilbert, 1900, problem 10:", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.5)
        hq = Tex(r"find a procedure that decides whether a polynomial equation\\ with integer coefficients "
                 r"has a solution in integers", font_size=36).next_to(h, DOWN, buff=0.3)
        eqs = VGroup(
            VGroup(MathTex(r"x^2+y^2=z^2", font_size=44), MathTex(r"(3,4,5)\ \checkmark", font_size=40,
                                                                    color=GREEN_3B)),
            VGroup(MathTex(r"x^3+y^3=z^3", font_size=44), Tex(r"only trivial ones (Euler)", font_size=34,
                                                               color=RED_3B)),
            VGroup(MathTex(r"x^2-61y^2=1", font_size=44),
                   MathTex(r"(1766319049,\ 226153980)\ \checkmark", font_size=38, color=GREEN_3B)),
        )
        for e in eqs:
            e.arrange(RIGHT, buff=0.8)
        eqs.arrange(DOWN, buff=0.5, aligned_edge=LEFT).next_to(hq, DOWN, buff=0.7)
        with self.say("In 1900, David Hilbert asked for a procedure that takes any polynomial equation with "
                      "integer coefficients and decides whether it has a solution in whole numbers. "
                      "{e1}Some equations have easy solutions. {e2}Some have none. "
                      "{e3}And some hide their smallest solution behind ten-digit numbers.") as s:
            self.play(Write(h), FadeIn(hq), run_time=2)
            s.wait_until("e1")
            self.play(FadeIn(eqs[0]))
            s.wait_until("e2")
            self.play(FadeIn(eqs[1]))
            s.wait_until("e3")
            self.play(FadeIn(eqs[2][0]))
            self.play(Write(eqs[2][1]), run_time=1.5)
        self.play(FadeOut(VGroup(h, hq, eqs)))

        # ------------------------------------------------------------ DPRM
        prog = VGroup(RoundedRectangle(width=3.6, height=2, corner_radius=0.2, color=BLUE_3B),
                      Tex(r"any computer\\ program", font_size=36, color=BLUE_3B))
        prog[1].move_to(prog[0])
        poly = VGroup(RoundedRectangle(width=3.6, height=2, corner_radius=0.2, color=YELLOW_3B),
                      Tex(r"a polynomial\\ equation", font_size=36, color=YELLOW_3B))
        poly[1].move_to(poly[0])
        pair = VGroup(prog, poly).arrange(RIGHT, buff=2.6).shift(UP * 0.4)
        iff = MathTex(r"\Longleftrightarrow", font_size=60).move_to(pair)
        lbl = VGroup(Tex("halts", font_size=32).next_to(prog, DOWN, buff=0.2),
                     Tex("has an integer solution", font_size=32).next_to(poly, DOWN, buff=0.2))
        names = Tex(r"Davis, Putnam, Robinson (1961) $+$ Matiyasevich (1970)", font_size=34,
                    color=GREY_A).to_edge(DOWN, buff=1.3)
        verdict = Tex(r"$\Rightarrow$ no algorithm can decide integer solvability", font_size=38,
                      color=RED_3B).next_to(names, DOWN, buff=0.3)
        with self.say(f"The answer, completed by Yuri {MATI} in 1970 on the work of Martin Davis, Hilary Putnam, "
                      "and Julia Robinson, was no. {enc}Polynomial equations turn out to be a programming language: "
                      "for any computer program, there is an equation that has an integer solution exactly when "
                      "the program halts. {no}Since no algorithm can predict halting, none can decide "
                      "integer equations.") as s:
            s.wait_until("enc")
            self.play(FadeIn(prog), FadeIn(poly), Write(iff), FadeIn(lbl), run_time=2)
            self.play(FadeIn(names))
            s.wait_until("no")
            self.play(Write(verdict))
        self.play(FadeOut(VGroup(pair, iff, lbl, names, verdict)))

        # ------------------------------------------------------------ rationals
        ax = Axes(x_range=[-1.6, 1.6, 1], y_range=[-1.6, 1.6, 1], x_length=5.4, y_length=5.4, tips=False,
                  axis_config={"color": GREY_D}).shift(LEFT * 3.3 + DOWN * 0.3)
        circ = Circle(radius=ax.x_axis.unit_size, color=BLUE_3B).move_to(ax.c2p(0, 0))
        base = Dot(ax.c2p(-1, 0), color=YELLOW_3B)
        slopes = [Q(1, 2), Q(1, 3), Q(2, 3), Q(3, 4), Q(-1, 2), Q(1, 5), Q(-2, 3), Q(4, 5), Q(-1, 4)]
        rdots, rlines = VGroup(), VGroup()
        for t in slopes:
            x, y = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
            rdots.add(Dot(ax.c2p(float(x), float(y)), radius=0.07, color=YELLOW_3B))
            rlines.add(Line(ax.c2p(-1, 0), ax.c2p(float(x), float(y)), color=YELLOW_3B, stroke_width=1.5,
                            stroke_opacity=0.5))
        clab = MathTex(r"x^2+y^2=1", font_size=36, color=BLUE_3B).next_to(ax, UP, buff=0.1)
        ex = MathTex(r"\left(\tfrac{3}{5},\tfrac{4}{5}\right),\ \left(\tfrac{5}{13},\tfrac{12}{13}\right),\dots",
                     font_size=34, color=YELLOW_3B).next_to(ax, DOWN, buff=0.15)
        right = VGroup(
            Tex(r"Now ask for \emph{rational} solutions.", font_size=36),
            MathTex(r"x^2+y^2=3:\ \text{none at all}", font_size=36, color=RED_3B),
            Tex(r"Searching finds solutions if they exist,\\ but never certifies that none do.", font_size=30,
                color=GREY_A),
        ).arrange(DOWN, buff=0.4).move_to(RIGHT * 3.2 + UP * 0.6)
        with self.say("But what if we allow fractions? {q}Ask instead whether an equation has a rational solution. "
                      "{c}The unit circle has infinitely many rational points: draw lines with rational slope "
                      "through one of them. {n}The circle of radius root three has none at all. "
                      "{s}You can always search for a rational solution, but searching never proves that none exists. "
                      "Is there an algorithm? That question stayed open for more than fifty years.") as s:
            s.wait_until("q")
            self.play(FadeIn(right[0]))
            s.wait_until("c")
            self.play(Create(ax), Create(circ), FadeIn(clab), FadeIn(base), run_time=1.5)
            self.play(LaggedStart(*[AnimationGroup(Create(l), FadeIn(d)) for l, d in zip(rlines, rdots)],
                                  lag_ratio=0.2), FadeIn(ex), run_time=3)
            s.wait_until("n")
            self.play(FadeIn(right[1]))
            s.wait_until("s")
            self.play(FadeIn(right[2]))
        self.play(FadeOut(VGroup(ax, circ, base, rdots, rlines, clab, ex, right)))

        # ------------------------------------------------------------ the obvious route and its obstacle
        route = VGroup(
            Tex(r"\textbf{The obvious route:} describe $\mathbb{Z}$ inside $\mathbb{Q}$ by an equation", font_size=36),
            MathTex(r"t\in\mathbb{Z}\iff \exists\, u_1,\dots,u_m\in\mathbb{Q}:\ P(t,u_1,\dots,u_m)=0", font_size=40,
                    color=BLUE_3B),
            Tex(r"Robinson (1949), Poonen (2009), Koenigsmann (2016): definitions needing $\forall$",
                font_size=30, color=GREY_A),
            Tex(r"Mazur's conjecture would rule out the purely existential one", font_size=32, color=RED_3B),
        ).arrange(DOWN, buff=0.4)
        with self.say("The natural plan is to describe the integers inside the rationals using a polynomial "
                      "equation. {f}If some equation had rational solutions exactly when t is an integer, "
                      f"you could translate {MATI}'s theorem directly. ".replace("{f}", "{f}") +
                      "{r}Julia Robinson, Bjorn Poonen, and Jochen Koenigsmann found definitions, but they "
                      "all need for-all quantifiers. {m}And a well-known conjecture of Barry Mazur would forbid "
                      "the purely existential kind. The obvious route looked blocked.") as s:
            self.play(FadeIn(route[0]))
            s.wait_until("f")
            self.play(Write(route[1]), run_time=2)
            s.wait_until("r")
            self.play(FadeIn(route[2]))
            s.wait_until("m")
            self.play(FadeIn(route[3]))
        self.play(FadeOut(route))

        # ------------------------------------------------------------ theorem
        thm = VGroup(Tex(r"\textbf{Theorem.} There is no algorithm which, given $f\in\mathbb{Z}[X_1,\dots,X_n]$,",
                         font_size=38),
                     Tex(r"decides whether $f$ has a zero in $\mathbb{Q}^n$.", font_size=38),
                     Tex(r"(even for total degree $\le 4$; exactly as hard as the halting problem)", font_size=30,
                         color=GREY_A)).arrange(DOWN, buff=0.25)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3))
        with self.say("A manuscript in OpenAI's math catalogue claims to settle it anyway. "
                      "{t}No algorithm decides whether a polynomial with integer coefficients has a rational zero. "
                      "{d}It even stays undecidable for equations of degree four, and it is exactly as hard as "
                      "the halting problem.") as s:
            s.wait_until("t")
            self.play(Write(thm[:2]), Create(tb[1]), run_time=3)
            s.wait_until("d")
            self.play(FadeIn(thm[2]))
        self.play(FadeOut(tb))

        # ------------------------------------------------------------ the race
        hdr = Tex(r"The trick: don't \emph{define} the integers, \emph{test} for them", font_size=40,
                  color=YELLOW_3B).to_edge(UP, buff=0.4)
        tests = Tex(r"for each $f$: tests $T_1,T_2,T_3,\dots$, each answered by finitely many\\"
                    r"``does this have a rational solution?'' questions", font_size=32).next_to(hdr, DOWN, buff=0.35)
        iff2 = MathTex(r"f\ \text{has an integer zero}\iff\text{every test passes}", font_size=40,
                       color=BLUE_3B).next_to(tests, DOWN, buff=0.35)
        track1 = Line(LEFT * 5.5, RIGHT * 5.5, color=GREY_B).shift(DOWN * 1.2)
        track2 = Line(LEFT * 5.5, RIGHT * 5.5, color=GREY_B).shift(DOWN * 2.4)
        l1 = Tex("search integer tuples", font_size=28, color=GREEN_3B).next_to(track1, UP, buff=0.1).align_to(
            track1, LEFT)
        l2 = Tex("run tests until one fails", font_size=28, color=RED_3B).next_to(track2, UP, buff=0.1).align_to(
            track2, LEFT)
        r1 = Dot(track1.get_start(), color=GREEN_3B, radius=0.12)
        r2 = Dot(track2.get_start(), color=RED_3B, radius=0.12)
        stop = Tex(r"one of them must stop $\Rightarrow$ integer solvability decided: impossible!", font_size=32,
                   color=YELLOW_3B).to_edge(DOWN, buff=0.3)
        with self.say("The proof sidesteps the obstacle. {t}For each polynomial f, it builds an infinite list of "
                      "finite tests. Each test asks finitely many questions of the form: does this equation have "
                      "a rational solution? {i}And f has an integer zero exactly when every test passes. "
                      "{race}Now suppose a rational-solvability algorithm existed. Run two searches side by side: "
                      "one hunting for an integer solution, the other running tests until one fails. "
                      "{st}One of them must stop. That would decide integer equations, which "
                      f"{MATI} showed is impossible.") as s:
            self.play(Write(hdr))
            s.wait_until("t")
            self.play(FadeIn(tests))
            s.wait_until("i")
            self.play(Write(iff2), run_time=2)
            s.wait_until("race")
            self.play(Create(track1), Create(track2), FadeIn(l1, l2, r1, r2))
            self.play(r1.animate.move_to(track1.point_from_proportion(0.8)),
                      r2.animate.move_to(track2.point_from_proportion(0.65)), run_time=4, rate_func=linear)
            s.wait_until("st")
            self.play(Write(stop))
        self.play(FadeOut(VGroup(hdr, tests, iff2, track1, track2, l1, l2, r1, r2, stop)))

        # ------------------------------------------------------------ elliptic encoding
        ax2 = Axes(x_range=[0, 6.5, 1], y_range=[-16, 16, 8], x_length=5.6, y_length=6.2, tips=False,
                   axis_config={"color": GREY_D}).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        ec = ParametricFunction(lambda t: ax2.c2p(np.cbrt(t * t + 2), t), t_range=[-15.5, 15.5], color=BLUE_3B)
        ecl = MathTex(r"y^2=x^3-2", font_size=34, color=BLUE_3B).next_to(ax2.c2p(5.5, 15), LEFT)
        P = (Q(3), Q(5))
        pts, cur = [], None
        for n in range(1, 9):
            cur = ec_add(cur, P)
            pts.append(cur)
        P2 = pts[1]
        dP = Dot(ax2.c2p(3, 5), color=YELLOW_3B, radius=0.09)
        dPl = MathTex("P", font_size=34, color=YELLOW_3B).next_to(dP, RIGHT, buff=0.1)
        tan = Line(ax2.c2p(0.8, 5 - 2.7 * 2.2), ax2.c2p(4.4, 5 + 2.7 * 1.4), color=GREY_A, stroke_width=2)
        m2 = Dot(ax2.c2p(float(P2[0]), -float(P2[1])), color=GREY_A, radius=0.07)
        d2 = Dot(ax2.c2p(float(P2[0]), float(P2[1])), color=YELLOW_3B, radius=0.09)
        d2l = MathTex("2P", font_size=32, color=YELLOW_3B).next_to(d2, LEFT, buff=0.1)
        refl = DashedLine(m2.get_center(), d2.get_center(), color=GREY_A)
        d3 = Dot(ax2.c2p(float(pts[2][0]), float(pts[2][1])), color=YELLOW_3B, radius=0.09)
        d3l = MathTex("3P", font_size=32, color=YELLOW_3B).next_to(d3, RIGHT, buff=0.1)
        rows = VGroup(*[MathTex(f"{n}P:\\ x=" + (str(p[0]) if len(str(p[0])) < 26 else str(p[0])[:22] + r"\dots"),
                                font_size=26) for n, p in zip(range(1, 7), pts)]).arrange(DOWN, aligned_edge=LEFT,
                                                                                          buff=0.18)
        rows.to_edge(RIGHT, buff=0.4).shift(UP * 1.0)
        digs = VGroup(*[MathTex(str(len(str(p[0].p))), font_size=28, color=ORANGE_3B).next_to(r, LEFT, buff=0.35)
                        .align_to(rows, LEFT).shift(LEFT * 0.7) for r, p in zip(rows, pts)])
        dl = Tex("digits", font_size=26, color=ORANGE_3B).next_to(digs, UP, buff=0.15)
        quad = Tex(r"digits grow like $n^2$: \emph{height} $h(nP)\approx c\,n^2$", font_size=32,
                   color=ORANGE_3B).next_to(rows, DOWN, buff=0.45).to_edge(RIGHT, buff=0.4)
        with self.say("To build the tests, integers are encoded as points on an elliptic curve. "
                      "{p}Start with a rational point P. {d}The chord and tangent construction produces "
                      "two P, {t3}three P, and so on: the integer n becomes the point n P. "
                      "The paper uses a curve over the field with square root of two whose points essentially form "
                      "a single infinite cyclic family. {h}The key arithmetic fact: the number of digits in the "
                      "coordinates of n P grows like n squared. This is the point's height.") as s:
            self.play(Create(ax2), Create(ec), FadeIn(ecl), run_time=1.5)
            s.wait_until("p")
            self.play(FadeIn(dP, scale=2), FadeIn(dPl))
            s.wait_until("d")
            self.play(Create(tan), run_time=1)
            self.play(FadeIn(m2), Create(refl), FadeIn(d2, scale=2), FadeIn(d2l))
            s.wait_until("t3")
            self.play(FadeIn(d3, scale=2), FadeIn(d3l), FadeOut(tan), FadeOut(refl), FadeOut(m2))
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.25), run_time=2.5)
            s.wait_until("h")
            self.play(FadeIn(dl), LaggedStart(*[FadeIn(d) for d in digs], lag_ratio=0.2), run_time=1.5)
            self.play(Write(quad))
        self.play(FadeOut(VGroup(ax2, ec, ecl, dP, dPl, d2, d2l, d3, d3l, rows, digs, dl, quad)))

        # ------------------------------------------------------------ the squeeze
        ax3 = Axes(x_range=[0, 10, 2], y_range=[0, 40, 10], x_length=5, y_length=4.4, tips=False,
                   axis_config={"color": GREY_B}).shift(LEFT * 4.0 + DOWN * 0.6)
        bl = MathTex("B", font_size=32).next_to(ax3.x_axis, RIGHT, buff=0.1)
        hl = Tex("height", font_size=28).next_to(ax3.y_axis, UP, buff=0.1)
        sq = ax3.plot(lambda b: 0.5 * b * b, x_range=[0, 8.9], color=ORANGE_3B)
        lin = ax3.plot(lambda b: 3.2 * b, x_range=[0, 10], color=TEAL_3B)
        sql = MathTex(r"\gtrsim B^2", font_size=32, color=ORANGE_3B).next_to(ax3.c2p(8.9, 39.6), RIGHT, buff=0.1)
        linl = MathTex(r"\lesssim B", font_size=32, color=TEAL_3B).next_to(ax3.c2p(10, 32), RIGHT, buff=0.1)
        cross = DashedLine(ax3.c2p(6.4, 0), ax3.c2p(6.4, 20.5), color=YELLOW_3B)
        txt = VGroup(
            Tex(r"If every test passes but $f$ has no integer zero,", font_size=30),
            Tex(r"compactness gives a `fake' solution with\\ infinitely large indices, of size $B$.", font_size=30),
            Tex(r"Elliptic curve: heights $\gtrsim B^2$", font_size=30, color=ORANGE_3B),
            Tex(r"New bound, from abelian surfaces\\ and modularity: heights $\lesssim B$", font_size=30,
                color=TEAL_3B),
            Tex(r"$\Rightarrow B$ is bounded $\Rightarrow$ a real integer zero.", font_size=30, color=YELLOW_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        with self.say("The hard part is showing that some test must fail when there is no integer solution. "
                      "{c}Suppose every test passed anyway. A compactness argument from logic produces a fake "
                      "solution, whose integer indices are infinitely large, of size B. "
                      "{e}The elliptic curve says the heights involved grow like B squared. "
                      "{n}But a new height bound, proved using families of abelian surfaces and a modularity theorem, "
                      "says they grow at most like B. {x}B squared below a constant times B forces B to be finite, "
                      "so the fake solution is a real integer solution after all.") as s:
            self.play(FadeIn(txt[0]))
            s.wait_until("c")
            self.play(FadeIn(txt[1]))
            s.wait_until("e")
            self.play(Create(ax3), FadeIn(bl, hl), Create(sq), FadeIn(sql), FadeIn(txt[2]), run_time=2)
            s.wait_until("n")
            self.play(Create(lin), FadeIn(linl), FadeIn(txt[3]), run_time=2)
            s.wait_until("x")
            self.play(Create(cross), FadeIn(txt[4]))
        self.play(FadeOut(Group(*self.mobjects)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"No algorithm decides rational solvability of integer polynomials",
             r"Built on two companion results in the same catalogue",
             r"Manuscript: 62 pages, produced by an OpenAI model"],
            False, r"\emph{Hilbert's tenth problem over the rational numbers} (Sept.\ 2026)")
        with self.say("A caveat. This proof has not been formalized, and it leans on two other results from the same "
                      "catalogue: a converse theorem for elliptic curves, and a modularity theorem at the prime two. "
                      "{c}So it needs careful checking by experts. If it holds, one of the most famous questions "
                      "left over from Hilbert's list has been answered.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("c")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
