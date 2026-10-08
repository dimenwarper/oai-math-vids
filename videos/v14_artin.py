from pathlib import Path

import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(Path(__file__).parent / "data" / "v14.npz")
ART = float(D["A"])
HB = "[Heath-Brown](/hˈiθ bɹˈWn/)"
HOO = "[Hooley](/hˈuli/)"


class Video(NarratedScene):
    def residue_circle(self, p, center, radius):
        pts = {r: center + radius * np.array([np.sin(TAU * (r - 1) / (p - 1)), np.cos(TAU * (r - 1) / (p - 1)), 0])
               for r in range(1, p)}
        dots = VGroup(*[Dot(pts[r], radius=0.07, color=GREY_B) for r in range(1, p)])
        labs = VGroup(*[MathTex(str(r), font_size=28, color=GREY_A).move_to(
            center + (radius + 0.38) * normalize(pts[r] - center)) for r in range(1, p)])
        return pts, dots, labs

    def construct(self):
        card = title_card(self, "029", r"Primitive Roots for Every Base",
                          r"The infinitude part of Artin's 1927 conjecture, for every admissible integer")
        with self.say("Why does one seventh repeat every six digits?"):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ 1/7 and 1/13
        c7 = [int(v) for v in D["c7"]]
        dig7 = [10 * r // 7 for r in c7]
        dec = MathTex(r"\tfrac17=0.", *[str(d) for d in dig7], r"\,142857\ldots", font_size=48).to_edge(UP, buff=0.5)
        for m in dec[1:7]:
            m.set_opacity(0)
        dec[7].set_opacity(0)
        cen = LEFT * 2.6 + DOWN * 0.7
        pts, dots, labs = self.residue_circle(7, cen, 2.0)
        expl = VGroup(Tex(r"each step of long division:", font_size=32),
                      MathTex(r"\text{remainder}\ \mapsto\ 10\times\text{remainder}\pmod 7", font_size=34)
                      ).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.5 + UP * 1.2)
        per = Tex(r"all $6$ nonzero remainders\\ $\Rightarrow$ period $6=7-1$", font_size=34, color=YELLOW_3B
                  ).move_to(RIGHT * 3.5 + DOWN * 1.2)
        arrows7 = VGroup()
        for a, b in zip(c7, c7[1:] + c7[:1]):
            arrows7.add(CurvedArrow(pts[a], pts[b], angle=-0.5, color=YELLOW_3B, stroke_width=3, tip_length=0.18))
        with self.say("Divide one by seven. The digits one, four, two, eight, five, seven repeat forever: the "
                      "period is six. {why}Why six? In long division, each step multiplies the remainder by ten, "
                      "and reduces it mod seven. {cyc}Starting from one, the remainders run through three, two, six, "
                      "four, five, and back to one. {all}That is every possible nonzero remainder, so the period is "
                      "the longest it could be: seven minus one.") as s:
            self.play(FadeIn(dec[0]))
            self.play(*[m.animate.set_opacity(1) for m in dec[1:]], run_time=1.5)
            s.wait_until("why")
            self.play(FadeIn(dots), FadeIn(labs), FadeIn(expl))
            for m in dec[1:]:
                m.set_opacity(0.25)
            s.wait_until("cyc")
            self.play(Indicate(labs[0], color=YELLOW_3B), run_time=0.6)
            for i, arr in enumerate(arrows7):
                self.play(Create(arr), dec[1 + i].animate.set_opacity(1).set_color(YELLOW_3B), run_time=0.55)
            s.wait_until("all")
            self.play(FadeIn(per))
        self.play(FadeOut(VGroup(dec, dots, labs, arrows7, expl, per)))

        c13 = [int(v) for v in D["c13"]]
        dec13 = MathTex(r"\tfrac1{13}=0.\overline{076923}\ldots", font_size=48).to_edge(UP, buff=0.5)
        pts, dots, labs = self.residue_circle(13, cen, 2.0)
        arrows13 = VGroup()
        for a, b in zip(c13, c13[1:] + c13[:1]):
            arrows13.add(Arrow(pts[a], pts[b], buff=0.1, color=BLUE_3B, stroke_width=3,
                               max_tip_length_to_length_ratio=0.12))
        hit = VGroup(*[Dot(pts[r], radius=0.1, color=BLUE_3B) for r in c13])
        per13 = Tex(r"only $6$ of $12$ remainders\\ $\Rightarrow$ period $6$, not $12$", font_size=34,
                    color=BLUE_3B).move_to(RIGHT * 3.5 + UP * 1.0)
        defn = VGroup(Tex(r"$10$ is a \textbf{primitive root} mod $p$", font_size=36, color=YELLOW_3B),
                      Tex(r"$\iff$ powers of $10$ hit every nonzero remainder", font_size=32),
                      Tex(r"$\iff$ $1/p$ has period $p-1$", font_size=32)).arrange(DOWN, buff=0.22).move_to(
            RIGHT * 3.4 + DOWN * 1.5)
        with self.say("Now try thirteen. {c}The remainders cycle through only six of the twelve possibilities, so "
                      "one thirteenth repeats every six digits, not twelve. {pr}When the powers of ten do reach every "
                      "nonzero remainder mod a prime p, we say ten is a primitive root mod p, and one over p has the "
                      "longest possible period, p minus one.") as s:
            self.play(FadeIn(dec13), FadeIn(dots), FadeIn(labs))
            s.wait_until("c")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows13], lag_ratio=0.3), FadeIn(hit), run_time=2.5)
            self.play(FadeIn(per13))
            s.wait_until("pr")
            self.play(FadeIn(defn, shift=UP * 0.2))
        self.play(FadeOut(VGroup(dec13, dots, labs, arrows13, hit, per13, defn)))

        # ------------------------------------------------------------ Artin's conjecture + data
        full = ", ".join(str(int(v)) for v in D["full"][:10])
        lst = Tex(rf"$10$ is a primitive root mod $p$ for $p={full},\ldots$", font_size=30).to_edge(UP, buff=0.4)
        art = VGroup(
            Tex(r"\textbf{Artin (1927):} every integer $a\neq-1$ that is not a perfect square", font_size=32),
            Tex(r"is a primitive root mod infinitely many primes,", font_size=32),
            Tex(r"in fact for a predictable proportion of them", font_size=32),
        ).arrange(DOWN, buff=0.12).next_to(lst, DOWN, buff=0.3)
        xs, prop = D["xs"].astype(float), D["prop10"]
        keep = xs >= 100
        xs, prop = xs[keep], prop[keep]
        ax = Axes(x_range=[2, 6.7, 1], y_range=[0.25, 0.55, 0.1], x_length=9.5, y_length=3.0, tips=False,
                  axis_config={"color": GREY_B, "font_size": 22},
                  y_axis_config={"numbers_to_include": [0.3, 0.4, 0.5],
                                 "decimal_number_config": {"num_decimal_places": 1}}).to_edge(DOWN, buff=0.75)
        ax.x_axis.add_labels({k: MathTex(f"10^{k}", font_size=24) for k in range(2, 7)})
        curve = VMobject(color=BLUE_3B, stroke_width=3).set_points_as_corners(
            [ax.c2p(np.log10(x), y) for x, y in zip(xs, prop)])
        aline = DashedLine(ax.c2p(2, ART), ax.c2p(6.7, ART), color=YELLOW_3B)
        alab = Tex(rf"Artin's constant $\approx {ART:.4f}$", font_size=28, color=YELLOW_3B).next_to(
            ax.c2p(6.7, ART), UP, buff=0.3).shift(LEFT * 1.6)
        ylab = Tex(r"fraction of primes $p\le x$ with primitive root $10$", font_size=26).next_to(
            ax, UP, buff=0.12).align_to(ax, LEFT).shift(RIGHT * 0.3)
        xlab = MathTex("x", font_size=30).next_to(ax.x_axis, RIGHT, buff=0.15)
        endv = Tex(rf"{prop[-1]:.4f} at $x=4\times10^6$", font_size=26, color=BLUE_3B).next_to(
            ax.c2p(np.log10(xs[-1]), prop[-1]), DOWN, buff=0.25).shift(LEFT * 0.6)
        with self.say("Which primes behave like seven? {l}Seventeen, nineteen, twenty-three, and many more. {a}In 1927, Emil Artin conjectured that any integer, except minus one and the "
                      "perfect squares, is a primitive root for infinitely many primes, and in fact for a predictable "
                      "proportion of them. Squares and minus one have to be excluded, because their powers can never "
                      "reach every remainder. {d}For base ten, the predicted proportion is Artin's constant, about "
                      "thirty-seven point four percent. {e}Up to four million, the data agree.") as s:
            s.wait_until("l")
            self.play(FadeIn(lst))
            s.wait_until("a")
            self.play(FadeIn(art[0]))
            self.play(FadeIn(art[1]))
            s.wait_until("d")
            self.play(Create(ax), FadeIn(ylab), FadeIn(xlab), Create(aline), FadeIn(alab))
            s.wait_until("e")
            self.play(Create(curve), run_time=3, rate_func=linear)
            self.play(FadeIn(endv))
        self.play(FadeOut(VGroup(lst, art, ax, curve, aline, alab, ylab, xlab, endv)))

        # ------------------------------------------------------------ history
        hist = VGroup(
            Tex(r"1967, Hooley: the full conjecture, \emph{assuming} a generalized Riemann hypothesis", font_size=32),
            Tex(r"1984, Gupta--Murty: one of a set of 13 explicit bases works", font_size=32),
            Tex(r"1986, Heath-Brown: at most two \emph{prime} bases fail,", font_size=32),
            Tex(r"so at least one of $2,3,5$ works \textemdash{} but which one?", font_size=32, color=YELLOW_3B),
            Tex(r"Unconditionally, no single specific base was known to work: not $2$, not $10$.", font_size=32,
                color=RED_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        hist[3].shift(RIGHT * 0.6)
        with self.say(f"The conjecture has a strange history. {{h}}In 1967, Christopher {HOO} proved all of it, but "
                      "only by assuming a generalized Riemann hypothesis. {g}Without that assumption, Gupta and "
                      f"Murty found a set of thirteen bases, at least one of which works. {{hb}}Then {HB} showed that at "
                      "most two prime bases can fail, so at least one of two, three, and five is a primitive root for "
                      "infinitely many primes. {w}But which one? No one could prove it for any single, specific "
                      "base: not for two, not for ten.") as s:
            s.wait_until("h")
            self.play(FadeIn(hist[0]))
            s.wait_until("g")
            self.play(FadeIn(hist[1]))
            s.wait_until("hb")
            self.play(FadeIn(hist[2]))
            self.play(FadeIn(hist[3]))
            s.wait_until("w")
            self.play(FadeIn(hist[4]))
        self.play(FadeOut(hist))

        # ------------------------------------------------------------ theorem
        thm = VGroup(Tex(r"\textbf{Theorem.} For every integer $a\neq-1$ that is not a square,", font_size=38),
                     MathTex(r"\#\{p\in(x,2x):\ a\text{ is a primitive root mod }p\}\ \ge\ c_a\,\frac{x}{(\log x)^2}",
                             font_size=40),
                     Tex(r"for all large $x$, with some constant $c_a>0$.", font_size=34)).arrange(DOWN, buff=0.3)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3)).shift(UP * 1.2)
        cmp = VGroup(Tex(r"predicted count: $\approx$ constant $\times\ x/\log x$", font_size=32, color=GREY_A),
                     Tex(r"proved: a factor of $\log x$ smaller, but still infinitely many", font_size=32,
                         color=GREY_A),
                     Tex(r"$\Rightarrow$ $1/p$ has period $p-1$ for infinitely many primes $p$", font_size=34,
                         color=YELLOW_3B)).arrange(DOWN, buff=0.22).next_to(tb, DOWN, buff=0.5)
        with self.say("A manuscript in OpenAI's math catalogue claims the infinitude part of the conjecture for every "
                      "allowed base. {t}For each such a, at least a constant times x over log x squared primes "
                      "between x and two x have a as a primitive root. {c}That falls a log factor short of the "
                      "predicted count, so it does not give Artin's proportion. {i}But it does give infinitely many "
                      "primes, for two, for ten, for every allowed base. In particular, one over p has period p minus "
                      "one for infinitely many primes p.") as s:
            s.wait_until("t")
            self.play(Write(tb), run_time=3)
            s.wait_until("c")
            self.play(FadeIn(cmp[0]))
            self.play(FadeIn(cmp[1]))
            s.wait_until("i")
            self.play(FadeIn(cmp[2]))
        self.play(FadeOut(VGroup(tb, cmp)))

        # ------------------------------------------------------------ proof: the index
        hdr = Tex("The proof: build primes where nothing can go wrong", font_size=40, color=YELLOW_3B).to_edge(
            UP, buff=0.35)
        idx = VGroup(
            MathTex(r"a\text{ fails mod }p\iff\text{some prime }q\text{ divides the index }\frac{p-1}{\mathrm{ord}_p(a)}",
                    font_size=36),
            MathTex(r"q\mid\text{index}\iff p\equiv1\!\!\pmod q\ \text{ and }\ a^{(p-1)/q}\equiv1\!\!\pmod p", font_size=36),
            Tex(r"$\iff$ $p$ splits completely in the Kummer field $\mathbb{Q}(\zeta_q,\sqrt[q]{a})$", font_size=34,
                color=TEAL_3B),
        ).arrange(DOWN, buff=0.3).next_to(hdr, DOWN, buff=0.4)
        # p - 1 = c * r * Q bar
        W = 11.0
        segs = [("c", 1.0, GREY_B), ("r", 3.4, BLUE_3B), ("Q", 6.6, GREEN_3B)]
        bar = VGroup()
        xcur = -W / 2
        for lab, w, col in segs:
            rect = Rectangle(width=w, height=0.6, stroke_color=WHITE, stroke_width=2).set_fill(col, 0.55)
            rect.move_to([xcur + w / 2, -0.9, 0])
            bar.add(VGroup(rect, MathTex(lab, font_size=32).move_to(rect)))
            xcur += w
        pm1 = MathTex(r"p-1\ =", font_size=36).next_to(bar, LEFT, buff=0.2)
        barg = VGroup(pm1, bar).move_to(DOWN * 0.9)
        notes = VGroup(
            Tex(r"$c$: $2$ or $4$", font_size=28, color=GREY_A),
            Tex(r"$r$: all prime factors between $e^{(\log x)^{0.1}}$ and $e^{(\log x)^{0.3}}$", font_size=28,
                color=BLUE_3B),
            Tex(r"$Q$: a single prime larger than $x^{0.9}$", font_size=28, color=GREEN_3B),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(barg, DOWN, buff=0.3)
        chk = VGroup(
            Tex(r"$q=2$: choose $p$ with $a$ a non-square mod $p$ \checkmark", font_size=30),
            Tex(r"$q=Q$: forces $p\mid a^j-1$ for some $j<2x^{0.1}$; very few such $p$ \checkmark", font_size=30),
            Tex(r"$q\mid r$: Kummer splitting, which needs a new zero-free region", font_size=30, color=YELLOW_3B),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(DOWN, buff=0.6)
        with self.say("How do you force a to be a primitive root? {i}a fails mod p exactly when some prime q divides "
                      "the index: p minus one, divided by the order of a. {k}And q divides the index precisely when p "
                      "splits completely in a Kummer field, built from q-th roots of unity and a q-th root of a. "
                      "{b}So the manuscript builds primes for which p minus one has a rigid shape: two or four, "
                      "times a number r whose prime factors all lie in a medium range, times one huge prime Q, "
                      "bigger than x to the zero point nine.") as s:
            self.play(Write(hdr))
            s.wait_until("i")
            self.play(FadeIn(idx[0]))
            s.wait_until("k")
            self.play(FadeIn(idx[1]))
            self.play(FadeIn(idx[2]))
            s.wait_until("b")
            self.play(FadeIn(pm1), LaggedStart(*[FadeIn(b_, shift=UP * 0.2) for b_ in bar], lag_ratio=0.4),
                      run_time=2)
            self.play(FadeIn(notes))
        with self.say("Now rule out every possible q. {two}Two: choose p so that a is not a square mod p. "
                      "{big}The huge prime Q: if it divided the index, p would divide a to some small power, minus "
                      "one, and only a handful of primes do. {mid}The medium primes dividing r are the real fight. "
                      "Each needs p to split completely in a Kummer field, which should happen with probability "
                      "about one over q squared. Proving that, for all these fields at once, requires control of "
                      "the zeros of their L-functions.") as s:
            self.play(FadeOut(idx), barg.animate.next_to(hdr, DOWN, buff=0.6))
            self.play(notes.animate.next_to(barg, DOWN, buff=0.3))
            s.wait_until("two")
            self.play(FadeIn(chk[0]), Indicate(bar[0], color=WHITE))
            s.wait_until("big")
            self.play(FadeIn(chk[1]), Indicate(bar[2], color=GREEN_3B))
            s.wait_until("mid")
            self.play(FadeIn(chk[2]), Indicate(bar[1], color=BLUE_3B))
        self.play(FadeOut(VGroup(hdr, idx, barg, notes, chk)))

        # ------------------------------------------------------------ zero-free region
        hdr = Tex("The analytic engine: a uniform zero-free region", font_size=40, color=YELLOW_3B).to_edge(
            UP, buff=0.35)
        plane = Axes(x_range=[-0.2, 1.4, 0.5], y_range=[-3, 3, 1], x_length=5.0, y_length=5.0, tips=False,
                     axis_config={"color": GREY_B}).move_to(LEFT * 3.4 + DOWN * 0.5)
        strip = Rectangle(width=plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0], height=5.0, stroke_width=0).set_fill(
            GREY_B, 0.15).move_to(plane.c2p(0.5, 0))
        free = Rectangle(width=plane.c2p(1, 0)[0] - plane.c2p(0.93, 0)[0], height=5.0, stroke_width=0).set_fill(
            GREEN_3B, 0.55).move_to(plane.c2p(0.965, 0))
        crit = DashedLine(plane.c2p(0.5, -3), plane.c2p(0.5, 3), color=GREY_A)
        one = MathTex("1", font_size=28).next_to(plane.c2p(1, -3), DOWN, buff=0.12)
        half = MathTex(r"\tfrac12", font_size=28).next_to(plane.c2p(0.5, -3), DOWN, buff=0.12)
        rng = np.random.default_rng(5)
        zs = VGroup(*[Dot(plane.c2p(x, y), radius=0.045, color=RED_3B) for x, y in
                      zip(0.5 + rng.normal(0, 0.12, 30).clip(-0.38, 0.38), rng.uniform(-2.9, 2.9, 30))])
        arr = Arrow(plane.c2p(1.35, 2.3), plane.c2p(0.98, 1.6), color=GREEN_3B, buff=0.05, stroke_width=3)
        txt = VGroup(
            Tex(r"For every cyclotomic field $F\supseteq\mu_{12}$", font_size=32),
            Tex(r"and every finite-order Hecke character $\eta$:", font_size=32),
            MathTex(r"L_F(s,\eta)\neq0\quad\text{for }\ \mathrm{Re}\,s>1-10^{-6}", font_size=38, color=GREEN_3B),
            Tex(r"the same width for every field and character", font_size=30, color=GREY_A),
            Tex(r"(built from cubic theta series, adapting the method of\\ the companion quasi-Riemann hypothesis "
                r"manuscript)", font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 2.9 + UP * 0.2)
        exag = Tex("(width exaggerated)", font_size=24, color=GREEN_3B).next_to(plane, UP, buff=0.1).align_to(free, RIGHT)
        with self.say("The key new input is about where those zeros can live. {z}They lie in a critical strip. "
                      "{t}The manuscript proves that over cyclotomic fields containing the twelfth roots of unity, no "
                      "Hecke L-function has a zero with real part above one minus ten to the minus six, {u}with the "
                      "same width for every field and every character. Classical zero-free regions shrink as the "
                      "fields grow. {m}The argument uses cubic theta "
                      "series, adapting the method of the quasi-Riemann hypothesis manuscript in the same "
                      "catalogue.") as s:
            self.play(Write(hdr))
            s.wait_until("z")
            self.play(Create(plane), FadeIn(strip), Create(crit), FadeIn(one), FadeIn(half))
            self.play(LaggedStart(*[FadeIn(z, scale=2) for z in zs], lag_ratio=0.03), run_time=1.5)
            s.wait_until("t")
            self.play(FadeIn(txt[:3]), FadeIn(free), GrowArrow(arr), FadeIn(exag))
            s.wait_until("u")
            self.play(FadeIn(txt[3]))
            s.wait_until("m")
            self.play(FadeIn(txt[4]))
        self.play(FadeOut(VGroup(hdr, plane, strip, free, crit, one, half, zs, arr, txt, exag)))

        # ------------------------------------------------------------ assembly
        hdr = Tex("Putting it together", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.4)
        bars = VGroup()
        vals = [("primes in $(x,2x)$ with $p-1=c\\,r\\,Q$\\\\ and $a$ a non-square mod $p$", 5.0, BLUE_3B),
                ("lost to $q=Q$", 0.25, RED_3B), ("lost to $q\\mid r$", 0.5, RED_3B),
                ("left: $a$ is a primitive root", 4.25, GREEN_3B)]
        for i, (lab, h, col) in enumerate(vals):
            r_ = Rectangle(width=1.5, height=h * 0.85, stroke_width=0).set_fill(col, 0.8)
            r_.move_to([-4.5 + 3.0 * i, -2.6 + h * 0.85 / 2, 0])
            t_ = Tex(lab, font_size=26).next_to(r_, UP, buff=0.15)
            bars.add(VGroup(r_, t_))
        sv = Tex(r"sieve + Bombieri--Vinogradov:\\ $\gg x/(\log x)^2$ of them", font_size=26, color=BLUE_3B
                 ).next_to(bars[0], DOWN, buff=0.25).shift(UP * 0.0)
        sv.next_to(bars[0][0], DOWN, buff=0.2)
        sch = Tex("(schematic)", font_size=24, color=GREY_B).to_corner(DR, buff=0.4)
        with self.say("Finally, a sieve argument, which also uses an estimate from a companion manuscript on the "
                      "prime factors of p minus one, shows there are at least a constant times x over log x squared "
                      "primes of this shape between x and two x. {s}Subtract the few lost to the huge prime, {m}and the "
                      "few lost to the medium primes, which the zero-free region controls. {l}What's left, still of that "
                      "size, are primes for which a is a primitive root.") as s:
            self.play(FadeIn(hdr), FadeIn(sch))
            self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1]))
            self.play(FadeIn(sv))
            s.wait_until("s")
            self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1]))
            s.wait_until("m")
            self.play(GrowFromEdge(bars[2][0], DOWN), FadeIn(bars[2][1]))
            s.wait_until("l")
            self.play(GrowFromEdge(bars[3][0], DOWN), FadeIn(bars[3][1]))
        self.play(FadeOut(VGroup(hdr, bars, sv, sch)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Every integer $a\neq-1$, not a square, is a primitive root mod infinitely many $p$",
             r"At least $c_a\,x/(\log x)^2$ such primes in $(x,2x)$; Artin's density itself remains open",
             r"Manuscript: 92 pages, produced by an OpenAI model"],
            False, r"\emph{Primitive roots for every admissible integer base} (Oct.\ 2026)")
        with self.say("A caveat. This ninety-two page proof has not been formalized, and it relies on companion "
                      "manuscripts from the same catalogue, so it needs careful checking by experts. {c}If it holds, "
                      "then for two, for ten, and for every other allowed base, Artin's question, are there infinitely "
                      "many such primes, finally has an unconditional answer: yes.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("c")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
