import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(__file__.replace("v27_fft.py", "data/v27.npz"))
PH = D["ph"]
CRT = D["crt"]
MLAM = float(D["mlam"])

CT = "Cooley and [Tukey](/tˈuki/)"
MORG = "[Morgenstern](/mˈɔɹɡənstɜɹn/)"
AILON = "[Ailon](/ˈAlɑn/)"
ALMAN = "[Alman](/ˈɔlmən/)"
BLUE = "[Bluestein](/blˈustIn/)"


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "130", r"The Fourier Transform Below $n\log n$",
                          r"An exact DFT at every length in $O\big(n(\log n)^{1-10^{-13}}\big)$ operations")
        with self.say("Can the Fourier transform be computed with fewer than n log n operations?"):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ the DFT
        form = MathTex(r"X_k=\sum_{j=0}^{n-1}\zeta^{jk}x_j", r",\qquad \zeta=e^{2\pi i/n}", font_size=44).to_edge(
            UP, buff=0.5)
        n = 8
        cs = 0.62
        grid = VGroup()
        for j in range(n):
            for k in range(n):
                c = np.array([(k - 3.5) * cs, (3.5 - j) * cs, 0])
                circ = Circle(radius=0.25, color=GREY_D, stroke_width=1.5).move_to(c)
                ang = TAU * PH[j, k]
                col = interpolate_color(ManimColor(BLUE_3B), ManimColor(YELLOW_3B), PH[j, k])
                arr = Line(c, c + 0.24 * np.array([np.cos(ang), np.sin(ang), 0]), color=col, stroke_width=3)
                grid.add(VGroup(circ, arr))
        grid.shift(DOWN * 0.7 + LEFT * 2.3)
        Fl = MathTex(r"F_8", font_size=40).next_to(grid, LEFT, buff=0.3)
        cost = Tex(r"direct: about $n^2$ operations", font_size=34, color=RED_3B).move_to([4.0, -0.7, 0])
        with self.say("The discrete Fourier transform takes n numbers and returns n new ones. "
                      "{f}Output number k is a sum of the inputs, each turned by a power of the root of unity zeta. "
                      "{m}As a matrix, every entry is a point on the unit circle, spinning faster and faster from row to "
                      "row. {c}Multiplying by this matrix directly costs about n squared operations.") as s:
            s.wait_until("f")
            self.play(Write(form), run_time=2)
            s.wait_until("m")
            self.play(LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.01), FadeIn(Fl), run_time=2.5)
            s.wait_until("c")
            self.play(FadeIn(cost))
        self.play(FadeOut(VGroup(form, grid, Fl, cost)))

        # ------------------------------------------------------------ the FFT butterfly
        order = [0, 4, 2, 6, 1, 5, 3, 7]
        ys = [2.45 - 0.7 * r for r in range(8)]
        xs = [-5.0, -2.6, -0.2, 2.2]
        nodes = VGroup(*[VGroup(*[Dot([x, y, 0], radius=0.06, color=GREY_B) for y in ys]) for x in xs])
        lines = VGroup()
        stage_groups = []
        for s_ in range(3):
            g = VGroup()
            half = 2 ** s_
            for r in range(8):
                blk = r // (2 * half)
                pos = r % (2 * half)
                partner = r + half if pos < half else r - half
                for tgt in (r, partner):
                    g.add(Line([xs[s_], ys[r], 0], [xs[s_ + 1], ys[tgt], 0], color=BLUE_3B if tgt == r else TEAL_3B,
                               stroke_width=2.2))
            stage_groups.append(g)
            lines.add(g)
        inl = VGroup(*[MathTex(f"x_{order[r]}", font_size=28).next_to([xs[0], ys[r], 0], LEFT, buff=0.15)
                       for r in range(8)])
        outl = VGroup(*[MathTex(f"X_{r}", font_size=28).next_to([xs[3], ys[r], 0], RIGHT, buff=0.15)
                        for r in range(8)])
        stl = VGroup(*[Tex(f"stage {k + 1}", font_size=26, color=GREY_A).move_to([(xs[k] + xs[k + 1]) / 2, -3.05, 0])
                       for k in range(3)])
        side = VGroup(Tex(r"Cooley--Tukey (1965)", font_size=32, color=YELLOW_3B),
                      Tex(r"$\log_2 n$ stages,", font_size=30), Tex(r"each touching all $n$ numbers", font_size=30),
                      MathTex(r"\approx n\log n", font_size=44, color=YELLOW_3B),
                      Tex(r"every $n$: Bluestein's chirp", font_size=28, color=GREY_A)).arrange(
            DOWN, buff=0.25).move_to([4.75, 0.2, 0])
        with self.say(f"In 1965, {CT} published the fast Fourier transform. {{b}}For n a power of two, it splits "
                      "the work into log n stages of simple butterflies, each stage touching every number a constant "
                      f"number of times. {{c}}That is about n log n operations, and with {BLUE}'s chirp trick, "
                      "the same bound holds for every length. It is one of the most used algorithms there is.") as s:
            self.play(FadeIn(nodes), FadeIn(inl), FadeIn(side[0]))
            s.wait_until("b")
            for k in range(3):
                self.play(Create(stage_groups[k]), FadeIn(stl[k]), run_time=1.0)
            self.play(FadeIn(outl), FadeIn(side[1:3]))
            s.wait_until("c")
            self.play(Write(side[3]))
            self.play(FadeIn(side[4]))
        self.play(FadeOut(VGroup(nodes, lines, inl, outl, stl, side)))

        # ------------------------------------------------------------ lower bounds
        rows = VGroup(
            Tex(r"Morgenstern: $\Omega(n\log n)$ if constants are \emph{bounded}", font_size=34),
            Tex(r"Ailon: lower bounds for unitary $2\times2$ gates", font_size=34),
            Tex(r"Alman--Rao: better leading constant for $n=2^k$", font_size=34, color=GREY_A),
            Tex(r"unrestricted complex constants: is $n\log n$ necessary?", font_size=36, color=YELLOW_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        with self.say(f"Is n log n the end? It depends on the rules. {{mo}}{MORG} proved an n log n lower bound "
                      f"if the algorithm may only use constants of bounded size. {{ai}}{AILON} proved lower bounds for "
                      f"circuits built from unitary two by two gates. {{ar}}{ALMAN} and Rao improved the leading "
                      "constant for powers of two. {op}But with arbitrary complex constants, whether order n log n "
                      "operations are really needed was an open question.") as s:
            s.wait_until("mo")
            self.play(FadeIn(rows[0]))
            s.wait_until("ai")
            self.play(FadeIn(rows[1]))
            s.wait_until("ar")
            self.play(FadeIn(rows[2]))
            s.wait_until("op")
            self.play(FadeIn(rows[3]))
        self.play(FadeOut(rows))

        # ------------------------------------------------------------ theorem + model
        thm = VGroup(Tex(r"\textbf{Theorem.} One deterministic algorithm computes $F_nx$ exactly,", font_size=34),
                     Tex(r"for every $n$, in $O\big(n(\log n)^{1-10^{-13}}\big)$ operations.", font_size=34)).arrange(
            DOWN, buff=0.2)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3)).to_edge(UP, buff=0.4)
        model = VGroup(
            Tex(r"\textbf{The model}", font_size=32, color=TEAL_3B),
            Tex(r"exact complex arithmetic; each $+$, $-$, $\times$ constant costs 1", font_size=30),
            Tex(r"constants of any size; one root of unity supplied", font_size=30),
            Tex(r"integer indexing on $O(\log n)$-bit words costs 1", font_size=30),
            Tex(r"preparing constants and organizing arrays is counted", font_size=30),
            Tex(r"no claim about floating point, stability, or bit complexity", font_size=30, color=RED_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(tb, DOWN, buff=0.4)
        tiny = MathTex(r"\frac{n\log n}{n(\log n)^{1-10^{-13}}}=(\log n)^{10^{-13}}", r"\ \approx\ 1+4\cdot10^{-13}",
                       r"\ \text{ at } n=2^{64}", font_size=34).to_edge(DOWN, buff=0.35)
        tiny[1].set_color(YELLOW_3B)
        with self.say("A manuscript in OpenAI's math catalogue claims: {t}one deterministic algorithm computes the "
                      "exact transform at every length n, with order n times log n to the power one minus ten to the "
                      "minus thirteen operations. {mod}The model matters. Arithmetic is exact, and each addition, "
                      "subtraction, or multiplication by a prepared constant costs one. {c}Constants can be any size, "
                      "and one root of unity is supplied. {ix}Integer index operations on logarithmic-size words cost "
                      "one, {pr}and the work of preparing constants and organizing arrays is counted too. {no}It says "
                      "nothing about floating point, numerical stability, or bit complexity. {ti}And the saving is a "
                      "factor of log n to the ten to the minus thirteen: it grows without bound, but at n equal to two "
                      "to the sixty-four, it is about one plus four times ten to the minus thirteen.") as s:
            s.wait_until("t")
            self.play(Write(thm), Create(tb[1]), run_time=2.5)
            s.wait_until("mod")
            self.play(FadeIn(model[0:2]))
            s.wait_until("c")
            self.play(FadeIn(model[2]))
            s.wait_until("ix")
            self.play(FadeIn(model[3]))
            s.wait_until("pr")
            self.play(FadeIn(model[4]))
            s.wait_until("no")
            self.play(FadeIn(model[5]))
            s.wait_until("ti")
            self.play(Write(tiny), run_time=2)
        self.play(FadeOut(VGroup(tb, model, tiny)))

        # ------------------------------------------------------------ Good-Thomas
        hdr = Tex(r"Coprime lengths are tensor products", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.35)
        row = VGroup(*[VGroup(Square(0.55, stroke_color=GREY_B, stroke_width=2),
                              MathTex(str(j), font_size=26)) for j in range(15)])
        for sq in row:
            sq[1].move_to(sq[0])
        row.arrange(RIGHT, buff=0.08).next_to(hdr, DOWN, buff=0.4)
        gs = 0.85
        g0 = np.array([-2.0, -0.9, 0])

        def gpos(a, b):
            return g0 + np.array([(b - 2) * gs, (1 - a) * gs, 0])

        targets = VGroup(*[row[j].copy().move_to(gpos(int(CRT[j][0]), int(CRT[j][1]))) for j in range(15)])
        rl = VGroup(*[MathTex(rf"j\equiv{a}\ (3)", font_size=24, color=BLUE_3B).next_to(gpos(a, 0), LEFT, buff=0.5)
                      for a in range(3)])
        cl = VGroup(*[MathTex(rf"{b}\ (5)", font_size=24, color=TEAL_3B).next_to(gpos(2, b), DOWN, buff=0.45)
                      for b in range(5)])
        colbox = VGroup(*[SurroundingRectangle(VGroup(*[targets[j] for j in range(15) if CRT[j][1] == b]),
                                               color=BLUE_3B, buff=0.05) for b in range(5)])
        rowbox = VGroup(*[SurroundingRectangle(VGroup(*[targets[j] for j in range(15) if CRT[j][0] == a]),
                                               color=TEAL_3B, buff=0.05) for a in range(3)])
        eqn = MathTex(r"F_{15}\ \cong\ F_3\otimes F_5", font_size=44, color=YELLOW_3B).move_to([4.2, -0.4, 0])
        eqn2 = MathTex(r"n=r_1r_2\cdots r_k:\quad F_n\cong F_{r_1}\otimes\cdots\otimes F_{r_k}", font_size=36
                       ).to_edge(DOWN, buff=0.4)
        with self.say("The proof starts from a classical observation, due to Good and to Thomas. "
                      "{g}When n is three times five, the Chinese remainder theorem places the fifteen inputs on a three "
                      "by five grid. {t}Then the fifteen-point transform becomes three-point transforms down the columns, "
                      "and five-point transforms along the rows, with no extra twiddle factors in between. "
                      "{k}With many coprime factors, the transform is a tensor product of many small transforms, "
                      "and the standard method processes one axis at a time. {q}So the real question is: can a tensor "
                      "product be computed faster than one axis at a time?") as s:
            self.play(Write(hdr))
            self.play(FadeIn(row))
            s.wait_until("g")
            self.play(LaggedStart(*[Transform(row[j], targets[j]) for j in range(15)], lag_ratio=0.08), run_time=2.5)
            self.play(FadeIn(rl), FadeIn(cl))
            s.wait_until("t")
            self.play(LaggedStart(*[Create(b) for b in colbox], lag_ratio=0.15), run_time=1.2)
            self.play(FadeOut(colbox), LaggedStart(*[Create(b) for b in rowbox], lag_ratio=0.2), run_time=1.2)
            self.play(Write(eqn))
            s.wait_until("k")
            self.play(FadeOut(rowbox), Write(eqn2))
        self.play(FadeOut(VGroup(hdr, row, rl, cl, eqn, eqn2)))

        # ------------------------------------------------------------ the finite tensor saving
        hdr = Tex(r"A finite tensor saving", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.35)
        Cm = MathTex(r"C=\frac12\begin{pmatrix}1+i&1-i\\1-i&1+i\end{pmatrix}", font_size=40)
        C2 = MathTex(r"C^2=\begin{pmatrix}0&1\\1&0\end{pmatrix}", font_size=40, color=TEAL_3B)
        top = VGroup(Cm, C2).arrange(RIGHT, buff=1.2).next_to(hdr, DOWN, buff=0.35)
        std = MathTex(r"C^{\otimes k}\text{ on }2^k\text{ numbers: axis by axis}\ \approx k\cdot 2^k", font_size=36
                      ).next_to(top, DOWN, buff=0.4)
        # bars: m axes vs lambda
        bw = 8.0
        b1 = Rectangle(width=bw, height=0.45, stroke_width=0, fill_color=GREY_B, fill_opacity=0.6)
        b2 = Rectangle(width=bw, height=0.45, stroke_width=0, fill_color=YELLOW_3B, fill_opacity=0.7)
        bars = VGroup(b1, b2).arrange(DOWN, buff=0.35).next_to(std, DOWN, buff=0.45).shift(RIGHT * 1.2)
        b1l = Tex(r"$m=10^6$ axes, standard", font_size=26).next_to(b1, LEFT, buff=0.2)
        b2l = Tex(r"new network", font_size=26, color=YELLOW_3B).next_to(b2, LEFT, buff=0.2)
        b1v = MathTex(r"1{,}000{,}000", font_size=28).move_to(b1)
        b2v = MathTex(r"999{,}999.999997\ldots", font_size=28, color=BLACK).move_to(b2)
        diff = Tex(r"saves about $%.1f\times10^{-6}$ of one pass" % (MLAM * 1e6), font_size=28,
                   color=YELLOW_3B).next_to(bars, DOWN, buff=0.2)
        amp = MathTex(r"m^j\text{ axes}\ \to\ \lambda^j=(m^j)^{\theta},\qquad \theta=\log_m\lambda\approx 1-2.1\cdot10^{-13}",
                      font_size=34, color=GREEN_3B).to_edge(DOWN, buff=0.35)
        with self.say("The paper says yes, for one special matrix. {c}This two by two matrix C is a square root of the "
                      "swap: C squared exchanges the two coordinates. {k}Its k-th tensor power acts on two to the k "
                      "numbers, and axis by axis it costs about k times two to the k. "
                      "{n}Using a fixed network from the companion integer-multiplication paper, which exchanges two "
                      "banks of arrays while restoring its scratch values, the paper processes a million axes at once, "
                      "for the cost of slightly fewer than a million axis passes: about three millionths of a pass fewer. "
                      "{a}Tiny, but it compounds. Applied recursively, m to the j axes cost lambda to the j, which is "
                      "m to the j, raised to a power theta just below one.") as s:
            self.play(Write(hdr))
            s.wait_until("c")
            self.play(Write(Cm))
            self.play(Write(C2))
            s.wait_until("k")
            self.play(FadeIn(std))
            s.wait_until("n")
            self.play(GrowFromEdge(b1, LEFT), FadeIn(b1l), FadeIn(b1v))
            self.play(GrowFromEdge(b2, LEFT), FadeIn(b2l), FadeIn(b2v))
            self.play(FadeIn(diff))
            s.wait_until("a")
            self.play(Write(amp), run_time=2)
        self.play(FadeOut(VGroup(hdr, top, std, bars, b1l, b2l, b1v, b2v, diff, amp)))

        # ------------------------------------------------------------ transfer to Fourier
        hdr = Tex(r"From $C$ to every Fourier matrix", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.35)
        steps = VGroup(
            Tex(r"\textbf{1.} Newton interpolation factors each small $F_r$ into diagonal", font_size=31),
            Tex(r"\quad and triangular Toeplitz pieces: $O(\log^4 r)$ layers of", font_size=31),
            Tex(r"\quad two-coordinate steps on \emph{exactly} $r$ coordinates", font_size=31),
            Tex(r"\textbf{2.} Run the layers in sync on many coprime axes: each layer", font_size=31),
            Tex(r"\quad splits into sectors carrying tensor powers of $C$", font_size=31),
            Tex(r"\textbf{3.} Chirp convolution: from convenient lengths to every $n$", font_size=31),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(hdr, DOWN, buff=0.45)
        # sector picture
        sec = VGroup()
        widths = [3.2, 2.0, 1.4, 0.9, 0.5]
        cols = [BLUE_3B, TEAL_3B, GREEN_3B, YELLOW_3B, ORANGE_3B]
        x = -4.0
        for w, c in zip(widths, cols):
            r = Rectangle(width=w, height=0.6, stroke_color=c, fill_color=c, fill_opacity=0.35).move_to(
                [x + w / 2, -2.6, 0])
            sec.add(r)
            x += w + 0.1
        secl = VGroup(*[MathTex(rf"C^{{\otimes {k}}}", font_size=26).move_to(r) for k, r in zip([7, 6, 5, 4, 3], sec)])
        sect = Tex(r"one synchronized layer (schematic)", font_size=26, color=GREY_A).next_to(sec, DOWN, buff=0.15)
        with self.say("Then every Fourier transform has to be made to look like tensor powers of C. "
                      "{nw}Each small transform of size r is factored, through Newton interpolation, into diagonal and "
                      "triangular Toeplitz pieces, and compiled into order log to the fourth r layers of two-coordinate "
                      "steps, on exactly r coordinates, with no extra workspace. {sy}Running those layers in sync across "
                      "many coprime axes, each simultaneous layer splits into sectors carrying tensor powers of C, "
                      "where the saving applies. {ch}Finally, a chirp convolution carries the bound from convenient "
                      "lengths to every n.") as s:
            self.play(Write(hdr))
            s.wait_until("nw")
            self.play(FadeIn(steps[0:3]), run_time=1.5)
            s.wait_until("sy")
            self.play(FadeIn(steps[3:5]))
            self.play(LaggedStart(*[FadeIn(r) for r in sec], lag_ratio=0.2), FadeIn(secl), FadeIn(sect), run_time=1.5)
            s.wait_until("ch")
            self.play(FadeIn(steps[5]))
        self.play(FadeOut(VGroup(hdr, steps, sec, secl, sect)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Exact DFT at every length in $O\big(n(\log n)^{1-10^{-13}}\big)$ operations",
             r"model: exact complex arithmetic, unbounded constants, one supplied root",
             r"Lean: only the companion statement, $<c\,n\log_2 n$ gates for some",
             r"\qquad arbitrarily large $n$ (unrestricted complex circuits)",
             r"Manuscripts: 31 + 49 pages, produced by an OpenAI model"],
            False, r"\emph{An explicit power saving for the exact discrete Fourier transform} (Sept.\ 2026)")
        with self.say("What has been checked by machine? The companion paper's statement, that for every c, some "
                      "arbitrarily large n have exact circuits with fewer than c times n log n gates, using arbitrary "
                      "complex constants, has been formalized in the Lean proof assistant. "
                      "{c}The all-length algorithm with its explicit exponent has not, and it needs careful checking "
                      "by experts.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("c")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
