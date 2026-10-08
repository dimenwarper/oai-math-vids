from pathlib import Path

import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(Path(__file__).parent / "data" / "v11.npz")

MORD = "[Mordell](/mɔɹdˈɛl/)"
SHA = "[Tate-Shafarevich](/tˈAt ʃˌæfəɹˈAvɪʧ/)"
KOLY = "[Kolyvagin](/kˌOlɪvˈɑɡɪn/)"
ZAG = "[Zagier](/zˈɑɡjA/)"
HEEG = "[Heegner](/hˈAɡnəɹ/)"
SELM = "[Selmer](/sˈɛlməɹ/)"


def curve_branches(ax, xmax=2.45, n=160):
    """Real locus of y^2 + y = x^3 - x, i.e. y = (-1 +- sqrt(4x^3-4x+1))/2."""
    r1, r2, r3 = sorted(np.roots([4, 0, -4, 1]).real)
    f = lambda x: np.sqrt(np.maximum(4 * x**3 - 4 * x + 1, 0))
    # oval on [r1, r2], parametrize densely near the ends
    t = np.linspace(0, np.pi, n)
    xo = r1 + (r2 - r1) * (1 - np.cos(t)) / 2
    up = [ax.c2p(x, (-1 + f(x)) / 2) for x in xo]
    dn = [ax.c2p(x, (-1 - f(x)) / 2) for x in xo[::-1]]
    oval = VMobject(color=BLUE_3B, stroke_width=4).set_points_smoothly(up + dn[1:] + [up[0]])
    s = np.linspace(0, np.sqrt(xmax - r3), n)
    xb = r3 + s**2
    upb = [ax.c2p(x, (-1 + f(x)) / 2) for x in xb]
    dnb = [ax.c2p(x, (-1 - f(x)) / 2) for x in xb]
    branch = VMobject(color=BLUE_3B, stroke_width=4).set_points_smoothly(dnb[::-1] + upb[1:])
    return VGroup(oval, branch)


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "002", r"The Full Birch--Swinnerton-Dyer Formula",
                          r"Exact, for every elliptic curve over $\mathbb{Q}$ with Selmer corank zero or one")
        with self.say("The Birch and Swinnerton-Dyer formula, claimed in full, for curves of rank zero and one."):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ the curve and its points
        ax = Axes(x_range=[-1.5, 2.5, 1], y_range=[-4, 3, 1], x_length=4.8, y_length=6.4, tips=False,
                  axis_config={"color": GREY_D, "include_numbers": False}).move_to(LEFT * 3.9 + DOWN * 0.2)
        cv = curve_branches(ax)
        eq = MathTex(r"y^2+y=x^3-x", font_size=40, color=BLUE_3B).next_to(ax, UP, buff=0.05).shift(RIGHT * 0.3)
        P = [(0, 0), (1, 0), (-1, -1), (2, -3), (0.25, -0.625)]
        pd = [Dot(ax.c2p(*p), radius=0.08, color=YELLOW_3B) for p in P]
        pl = [MathTex(t, font_size=28, color=YELLOW_3B) for t in ["P", "2P", "3P", "4P", "5P"]]
        dirs = [UL, UR, DL, RIGHT, DR]
        for d_, l_, dd in zip(pd, pl, dirs):
            l_.next_to(d_, dd, buff=0.08)
        line = Line(ax.c2p(-1.5, 0), ax.c2p(2.5, 0), color=WHITE, stroke_width=2.5)
        third = Dot(ax.c2p(-1, 0), radius=0.08, color=WHITE)
        refl = DashedLine(ax.c2p(-1, 0), ax.c2p(-1, -1), color=WHITE)
        axis_sym = DashedLine(ax.c2p(-1.5, -0.5), ax.c2p(2.5, -0.5), color=GREY_D, stroke_width=1.5)
        mstr = [str(v) for v in D["mstr"]]

        def frac(s_):
            s_ = s_.strip()
            if "/" in s_:
                a, b = s_.split("/")
                return (r"-" if a.startswith("-") else "") + rf"\tfrac{{{a.lstrip('-')}}}{{{b}}}"
            return s_

        rows = VGroup()
        for n, s_ in enumerate(mstr[:12]):
            x_, y_ = s_.split("|")
            rows.add(MathTex(rf"{n + 1}P", r"=", rf"\left({frac(x_)},\ {frac(y_)}\right)", font_size=30))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(RIGHT * 3.0 + UP * 0.35)
        for r in rows:
            r[0].set_color(YELLOW_3B)
        mord = Tex(r"Mordell (1922): finitely many points generate all of them.\\ Here one point $P$ suffices: "
                   r"\textbf{rank 1}", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.25).shift(RIGHT * 2.6)
        with self.say("Here is a cubic curve: y squared plus y equals x cubed minus x. {p}The point zero, zero lies "
                      "on it, and so does one, zero. {l}Draw the line through them. It meets the curve in exactly one "
                      "more point, minus one, zero, {r}and flipping that across the curve's axis of symmetry gives a "
                      "new rational point, minus one, minus one. {m}Repeating with chords and tangents produces "
                      "infinitely many rational points, with numerators and denominators that keep growing. "
                      f"{{mo}}{MORD} proved in 1922 that finitely many points generate them all. The number of "
                      "independent points needed is the rank. Here, a single point does it: rank one.") as s:
            self.play(Create(ax), Create(cv), FadeIn(eq), run_time=2)
            s.wait_until("p")
            self.play(FadeIn(pd[0], scale=2), FadeIn(pl[0]))
            self.play(FadeIn(pd[1], scale=2), FadeIn(pl[1]))
            s.wait_until("l")
            self.play(Create(line))
            self.play(FadeIn(third, scale=2))
            s.wait_until("r")
            self.play(Create(axis_sym), Create(refl))
            self.play(FadeIn(pd[2], scale=2), FadeIn(pl[2]))
            s.wait_until("m")
            self.play(FadeOut(line), FadeOut(third), FadeOut(refl))
            self.play(*[FadeIn(d_, scale=2) for d_ in pd[3:]], *[FadeIn(l_) for l_ in pl[3:]])
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in rows], lag_ratio=0.25), run_time=4)
            s.wait_until("mo")
            self.play(FadeIn(mord))
        self.play(FadeOut(VGroup(ax, cv, eq, *pd, *pl, axis_sym, rows, mord)))

        # ------------------------------------------------------------ BSD's experiment
        hdr = MathTex(r"N_p=\#\{\text{points of }E\text{ mod }p\},\qquad \prod_{p\le x}\frac{N_p}{p}\ \approx\ "
                      r"C\,(\log x)^{\text{rank}}", font_size=40).to_edge(UP, buff=0.4)
        ax2 = Axes(x_range=[0.4, 2.6, 0.5], y_range=[0, 10, 2], x_length=8.6, y_length=4.9, tips=False,
                   axis_config={"color": GREY_B, "font_size": 22},
                   y_axis_config={"numbers_to_include": [2, 4, 6, 8, 10]}).shift(DOWN * 0.7 + LEFT * 0.8)
        ax2.x_axis.add_labels({np.log(np.log(10.0**k)): MathTex(f"10^{k}", font_size=24) for k in range(1, 6)})
        xl = MathTex("x", font_size=30).next_to(ax2.x_axis, RIGHT, buff=0.15)
        yl = Tex(r"$\log\prod_{p\le x} N_p/p$", font_size=28).next_to(ax2, UP, buff=0.0).align_to(ax2, LEFT)
        px = D["px"]
        m = px >= 5
        cols = [GREY_A, BLUE_3B, TEAL_3B, YELLOW_3B]
        names = [("11a1", 0), ("37a1", 1), ("389a1", 2), ("5077a1", 3)]
        graphs, labs = VGroup(), VGroup()
        for (nm, rk), c in zip(names, cols):
            v = D[f"lp_{nm}"][m]
            g = VMobject(color=c, stroke_width=3).set_points_as_corners(
                [ax2.c2p(np.log(np.log(x)), y) for x, y in zip(px[m], v)])
            graphs.add(g)
            labs.add(Tex(f"rank {rk}", font_size=28, color=c).next_to(g.get_end(), RIGHT, buff=0.15))
        cap = Tex(r"four curves, primes up to $2\times10^5$;\\ horizontal axis: $\log\log x$", font_size=24,
                  color=GREY_B).move_to(ax2.c2p(0.5, 9.0), aligned_edge=UL)
        with self.say("How can you know the rank without finding the points? {e}In the early 1960s, Bryan Birch and "
                      "Peter Swinnerton-Dyer used early computers at Cambridge to count points modulo primes. {n}For "
                      "each prime p, count the solutions mod p, call it N p, and multiply together the ratios N p "
                      "over p. {g}Here are four real curves. For rank zero, the product levels off. For ranks one, "
                      "two and three, it grows roughly like log x to the power of the rank: more rational points, more "
                      "solutions mod p, on average.") as s:
            s.wait_until("e")
            self.play(Create(ax2), FadeIn(xl), FadeIn(yl), FadeIn(cap))
            s.wait_until("n")
            self.play(Write(hdr), run_time=2)
            s.wait_until("g")
            self.play(*[Create(g) for g in graphs], run_time=4, rate_func=linear)
            self.play(LaggedStart(*[FadeIn(l_) for l_ in labs], lag_ratio=0.3))
        self.play(FadeOut(VGroup(hdr, ax2, xl, yl, graphs, labs, cap)))

        # ------------------------------------------------------------ the conjecture and the formula
        c1 = MathTex(r"\text{rank }E(\mathbb{Q})\ =\ \mathrm{ord}_{s=1}L(E,s)", font_size=44).to_edge(UP, buff=0.6)
        F = MathTex(r"\frac{L^{(r)}(E,1)}{r!}", "=", r"\Omega_E", r"\cdot", r"\mathrm{Reg}_E", r"\cdot",
                    r"\#\mathrm{Sha}(E)", r"\cdot", r"\prod_{\ell}c_\ell", r"\Big/", r"\#E(\mathbb{Q})_{\mathrm{tors}}^{2}",
                    font_size=46).shift(UP * 0.5)
        tcol = {2: BLUE_3B, 4: TEAL_3B, 6: RED_3B, 8: GREEN_3B, 10: ORANGE_3B}
        tlab = {2: "real period", 4: r"regulator:\\ size of points", 6: "Tate--Shafarevich\\\\ group",
                8: r"local factors\\ at bad primes", 10: "torsion"}
        braces = VGroup()
        for k, c in tcol.items():
            F[k].set_color(c)
            b = Brace(F[k], DOWN, color=c, buff=0.12)
            lab_ = Tex(tlab[k], font_size=26, color=c).next_to(b, DOWN, buff=0.1)
            if k in (4, 8):
                lab_.shift(DOWN * 0.75)
                braces.add(VGroup(b, Line(b.get_bottom(), lab_.get_top(), color=c, stroke_width=1.5), lab_))
            else:
                braces.add(VGroup(b, lab_))
        lead = Tex(r"leading Taylor coefficient at $s=1$", font_size=26, color=GREY_A).next_to(F[0], UP, buff=0.3)
        clay = Tex(r"One of the Clay Millennium Prize Problems", font_size=30, color=YELLOW_3B).to_edge(DOWN, buff=0.5)
        with self.say("This led to their conjecture: the rank equals the order of vanishing of the curve's "
                      "L-function at s equals one. {f}And they went further, predicting the exact value of the first "
                      "nonzero Taylor coefficient. {t}It should equal the real period, times the regulator, which "
                      f"measures the size of the rational points, times the order of the mysterious {SHA} group, "
                      "times local factors at the bad primes, divided by the square of the number of torsion points. "
                      "{c}Proving all of this is one of the Clay Millennium Prize problems.") as s:
            self.play(Write(c1), run_time=2)
            s.wait_until("f")
            self.play(Write(F), FadeIn(lead), run_time=2.5)
            s.wait_until("t")
            for b in braces:
                self.play(FadeIn(b), run_time=0.8)
            s.wait_until("c")
            self.play(FadeIn(clay))
        self.play(FadeOut(VGroup(c1, lead, braces, clay)), F.animate.scale(0.8).to_edge(UP, buff=0.4))

        # ------------------------------------------------------------ what was known
        known = VGroup(
            Tex(r"1980s, Gross--Zagier and Kolyvagin (with modularity): if $\mathrm{ord}_{s=1}L(E,s)\le1$,", font_size=32),
            Tex(r"then the rank matches, and $\mathrm{Sha}(E)$ is finite.", font_size=32),
            Tex(r"The exact formula, prime by prime: only under extra hypotheses", font_size=32, color=ORANGE_3B),
            Tex(r"on the curve, its reduction, and the primes involved.", font_size=32, color=ORANGE_3B),
        ).arrange(DOWN, buff=0.22).shift(UP * 0.4)
        known[2].shift(DOWN * 0.25)
        known[3].shift(DOWN * 0.25)
        with self.say(f"Work of Gross and {ZAG}, and of {KOLY}, in the 1980s, together with the later proof of "
                      "modularity, shows that when the L-function vanishes to order at most one, the rank matches, and the Tate-Shafarevich group is finite. {x}But the "
                      "exact formula, every prime factor of it, was known only under extra hypotheses on the curve and "
                      "the primes involved.") as s:
            self.play(FadeIn(known[:2]))
            s.wait_until("x")
            self.play(FadeIn(known[2:]))
        self.play(FadeOut(known))

        # ------------------------------------------------------------ Selmer + theorem
        sel = VGroup(
            Tex(r"$q^\infty$-\textbf{Selmer group}: defined by local conditions, it packages", font_size=32),
            Tex(r"the rational points together with the $q$-part of $\mathrm{Sha}$", font_size=32),
            MathTex(r"\mathrm{corank}\,\mathrm{Sel}_{q^\infty}(E)\ =\ \mathrm{rank}\,E(\mathbb{Q})\ +\ "
                    r"\mathrm{corank}\,\mathrm{Sha}(E)[q^\infty]", font_size=36, color=TEAL_3B),
        ).arrange(DOWN, buff=0.22).next_to(F, DOWN, buff=0.6)
        thm = VGroup(
            Tex(r"\textbf{Theorem.} If for some prime $q$ the $q^\infty$-Selmer corank of $E/\mathbb{Q}$ is $0$ or "
                r"$1$,", font_size=32),
            Tex(r"then rank $=$ analytic rank $=$ that corank, $\mathrm{Sha}(E)$ is finite,", font_size=32),
            Tex(r"and the formula above holds exactly, at every prime,", font_size=32),
            Tex(r"with no extra hypotheses on reduction, torsion, isogenies, or CM.", font_size=32),
        ).arrange(DOWN, buff=0.15)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.25)).next_to(sel, DOWN, buff=0.45)
        with self.say(f"A manuscript in OpenAI's math catalogue claims the full formula whenever a {SELM} group is "
                      "small. {s}A Selmer group, defined by local conditions, packages the rational points together "
                      "with part of the Tate-Shafarevich group, one prime q at a time. {t}The theorem: if, for some "
                      "prime q, this Selmer group has corank zero or one, then the rank and the analytic rank both "
                      "equal that corank, Sha is finite, and the formula holds exactly, with no further hypotheses "
                      "on the curve.") as s:
            s.wait_until("s")
            self.play(FadeIn(sel[:2]))
            self.play(Write(sel[2]), run_time=2)
            s.wait_until("t")
            self.play(FadeIn(tb), run_time=2)
        self.play(FadeOut(VGroup(sel, tb, F)))

        # ------------------------------------------------------------ proof idea: discrepancies
        hdr = Tex("The proof: kill the discrepancy at every prime", font_size=40, color=YELLOW_3B).to_edge(
            UP, buff=0.35)
        ratio = MathTex(r"\frac{L^{(r)}(E,1)/r!}{\text{right-hand side}}", "=", r"2^{X_2}", r"\,3^{X_3}",
                        r"\,5^{X_5}", r"\,7^{X_7}", r"\cdots", font_size=42).next_to(hdr, DOWN, buff=0.45)
        goal = Tex(r"goal: every discrepancy $X_p=0$", font_size=32, color=GREY_A).next_to(ratio, DOWN, buff=0.25)
        inputs = VGroup(
            Tex(r"rank and finiteness: companion manuscript (the Selmer converse)", font_size=28, color=GREY_A),
            Tex(r"$X_2=0$: companion manuscript (the two-primary formula)", font_size=28, color=GREY_A),
            Tex(r"new here: $X_p=0$ for every odd prime $p$", font_size=30, color=YELLOW_3B),
        ).arrange(DOWN, buff=0.18).next_to(goal, DOWN, buff=0.4)
        with self.say("Here is the shape of the argument. {q}Given what the companion results already show, both "
                      "sides of the formula are positive and their ratio is a rational number. So it factors into "
                      "prime powers: two to some exponent, times three to some exponent, and so on. {x}Call the "
                      "exponent at p the discrepancy at p. The goal is to show every discrepancy is zero. {c}The rank "
                      "and finiteness statements, and the prime two, come from companion manuscripts in the same "
                      "catalogue. {o}What is new is every odd prime.") as s:
            self.play(Write(hdr))
            s.wait_until("q")
            self.play(Write(ratio), run_time=2.5)
            s.wait_until("x")
            self.play(FadeIn(goal))
            s.wait_until("c")
            self.play(FadeIn(inputs[:2]), ratio[2].animate.set_color(GREEN_3B))
            s.wait_until("o")
            self.play(FadeIn(inputs[2]), *[ratio[k].animate.set_color(YELLOW_3B) for k in (3, 4, 5)])
        self.play(FadeOut(VGroup(goal, inputs)), ratio.animate.scale(0.75).next_to(hdr, DOWN, buff=0.3))

        steps = VGroup(
            Tex(r"\textbf{1.} One-sided: $X_p(E)\ge0$", font_size=32, color=BLUE_3B),
            Tex(r"Kato's construction from modular symbols, made integral", font_size=26, color=GREY_A),
            Tex(r"\textbf{2.} Pair identity: $X_p(E)+X_p(E^D)=0$", font_size=32, color=TEAL_3B),
            Tex(r"a twist $E^D$ with ranks adding to $1$, over $K=\mathbb{Q}(\sqrt D)$ where $p$ splits;", font_size=26,
                color=GREY_A),
            Tex(r"Heegner points, Gross--Zagier, multivariable Iwasawa theory, theta series", font_size=26,
                color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(LEFT, buff=0.6).shift(UP * 0.2)
        steps[2].shift(DOWN * 0.15)
        steps[3:].shift(DOWN * 0.15)
        nl = NumberLine(x_range=[-2, 2, 1], length=5.2, include_numbers=True, font_size=24, color=GREY_B).move_to(
            RIGHT * 3.6 + DOWN * 2.2)
        bad = Rectangle(width=nl.n2p(0)[0] - nl.n2p(-2)[0], height=0.35, stroke_width=0).set_fill(RED_3B, 0.3).move_to(
            nl.n2p(-1))
        badl = Tex(r"forbidden by 1", font_size=24, color=RED_3B).next_to(bad, DOWN, buff=0.45)
        t = ValueTracker(1.4)
        dA = always_redraw(lambda: Dot(nl.n2p(t.get_value()) + UP * 0.35, radius=0.1, color=BLUE_3B))
        dB = always_redraw(lambda: Dot(nl.n2p(-t.get_value()) + UP * 0.7, radius=0.1,
                                       color=RED_3B if t.get_value() > 0.02 else TEAL_3B))
        lA = always_redraw(lambda: MathTex(r"X_p(E)", font_size=26, color=BLUE_3B).next_to(dA, RIGHT, buff=0.1))
        lB = always_redraw(lambda: MathTex(r"X_p(E^D)", font_size=26, color=TEAL_3B).next_to(dB, LEFT, buff=0.1))
        concl = Tex(r"both $\ge0$, sum $=0$ $\Rightarrow$ both $=0$", font_size=32, color=YELLOW_3B).next_to(
            nl, DOWN, buff=0.7)
        cm = Tex(r"(CM curves: the pair identity plus\\ a rank-zero theorem of Burungale--Flach)", font_size=24,
                 color=GREY_B).next_to(steps, DOWN, buff=0.6).align_to(steps, LEFT)
        with self.say("Fix an odd prime p. The manuscript proves two things. {one}First, a one-sided inequality: the "
                      "discrepancy of the curve is at least zero. This comes from making Kato's construction, built "
                      "from modular symbols, integral. {two}Second, a pair identity. Choose an imaginary quadratic "
                      "field where p splits, and a twisted curve whose rank complements the original, so that the "
                      f"two ranks add up to one. Over that field, {HEEG} points and the Gross {ZAG} formula tie the "
                      "two curves together, and the hard part, using Iwasawa theory in several variables and theta series, "
                      "shows that their discrepancies add up to exactly zero. {sq}Now, two numbers that are each at "
                      "least zero, and add up to zero, must both be zero. {cm}Curves with complex multiplication use "
                      "the same identity, plus one known rank-zero theorem. And that is the formula, at every odd "
                      "prime.") as s:
            s.wait_until("one")
            self.play(FadeIn(steps[:2]))
            self.play(Create(nl), FadeIn(bad), FadeIn(badl))
            self.add(dA, lA)
            s.wait_until("two")
            self.play(FadeIn(steps[2:]), run_time=1.5)
            self.add(dB, lB)
            s.wait_until("sq")
            self.play(t.animate.set_value(0), run_time=2.5)
            self.play(FadeIn(concl))
            s.wait_until("cm")
            self.play(FadeIn(cm))
        dA.clear_updaters()
        dB.clear_updaters()
        lA.clear_updaters()
        lB.clear_updaters()
        self.play(FadeOut(Group(*self.mobjects)))

        # ------------------------------------------------------------ closing
        cons = Tex(r"With result 006 (Goldfeld's conjecture): the full formula holds for\\ a density-one set of "
                   r"quadratic twists of every elliptic curve over $\mathbb{Q}$", font_size=32).shift(UP * 0.2)
        with self.say("Combined with the proof of Goldfeld's conjecture in the same catalogue, this would give the "
                      "full formula for almost all quadratic twists of every elliptic curve over the rationals.") as s:
            self.play(FadeIn(cons))
        self.play(FadeOut(cons))
        card = status_card(
            [r"Selmer corank $0$ or $1$ at some prime $\Rightarrow$ rank $=$ analytic rank, $\mathrm{Sha}$ finite,",
             r"and the exact Birch--Swinnerton-Dyer leading-term formula holds",
             r"Builds on companion manuscripts (Selmer converse; two-primary formula)",
             r"Manuscript: 94 pages, produced by an OpenAI model"],
            False, r"\emph{Exact Birch--Swinnerton-Dyer Formula from Low Selmer Corank} (Oct.\ 2026)")
        with self.say("A caveat. None of this has been formalized, and the ninety-four page proof builds on several "
                      "companion manuscripts in the same catalogue, none yet peer reviewed. {c}If they hold, the Birch "
                      "and Swinnerton-Dyer formula is known exactly for every curve whose Selmer group certifies rank "
                      "zero or one.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("c")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
