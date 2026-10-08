import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(__file__.replace("v28_integer_mult.py", "data/v28.npz"))
XB, YB, PB = [int(b) for b in D["xb"]], [int(b) for b in D["yb"]], [int(b) for b in D["pb"]]
XSTEPS = D["xsteps"]
PAR, N1 = D["par"], D["N1"]

KO = "[Karatsuba](/kˌɑɹətsˈubə/) and [Ofman](/ˈɔfmən/)"
TOOM = "[Toom](/tˈOm/)"
SS = "[Schönhage](/ʃˈɜnhɑɡə/) and [Strassen](/ʃtɹˈɑsən/)"
SCH = "[Schönhage](/ʃˈɜnhɑɡə/)"
FUR = "[Fürer](/fjˈʊɹəɹ/)"
HVDH = "Harvey and [van der Hoeven](/vˌæn dəɹ hˈuvən/)"


def bitrow(bits, color, cs=0.42, fs=28):
    g = VGroup(*[VGroup(Square(cs, stroke_color=color, stroke_width=2),
                        MathTex(str(b), font_size=fs, color=color)) for b in bits]).arrange(RIGHT, buff=0)
    for c in g:
        c[1].move_to(c[0])
    return g


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "109", r"Integer Multiplication Below $n\log n$",
                          r"Multitape Turing machines: $O\big(n(\log n)^{1-\kappa}\big)$ with $\kappa=2^{-182}$")
        with self.say("Multiplying whole numbers, faster than n log n."):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ schoolbook
        cs = 0.38
        xr = bitrow(XB, BLUE_3B, cs, 26)
        yr = bitrow(YB, YELLOW_3B, cs, 26)
        x_right = np.array([2.6, 2.3, 0])
        xr.move_to(x_right - np.array([xr.width / 2, 0, 0]))
        yr.next_to(xr, DOWN, buff=0.08).align_to(xr, RIGHT)
        times = MathTex(r"\times", font_size=36).next_to(yr, LEFT, buff=0.2)
        rows = VGroup()
        for i in range(8):
            yi = YB[7 - i]
            bits = [b & yi for b in XB]
            r = bitrow(bits, GREY_A if yi else GREY_D, cs, 24)
            r.next_to(yr, DOWN, buff=0.12 + i * cs).align_to(xr, RIGHT).shift(LEFT * cs * i)
            rows.add(r)
        line = Line(rows.get_corner(DL) + DOWN * 0.08 + LEFT * 0.1, xr.get_right() * RIGHT + rows.get_bottom() * UP
                    + DOWN * 0.08 + RIGHT * 0.1, color=GREY_B)
        pr = bitrow(PB, GREEN_3B, cs, 26).next_to(line, DOWN, buff=0.1).align_to(xr, RIGHT)
        n2 = Tex(r"$n\times n$ bit products:\\ about $n^2$ steps", font_size=34, color=RED_3B).move_to([4.8, 0.2, 0])
        kar = VGroup(Tex(r"1962: Karatsuba--Ofman, $n^{1.585}$", font_size=30),
                     Tex(r"Toom: $n^{1+\varepsilon}$ for any $\varepsilon>0$", font_size=30)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.5)
        with self.say("To multiply two n-digit numbers the way we learn in school, multiply every digit of one by "
                      "every digit of the other, then add. {g}In binary, that is an n by n grid of bit products: "
                      f"about n squared steps. {{k}}In 1962, {KO} showed how to do better, about n to the one point "
                      f"five eight, {{t}}and {TOOM}'s method pushed the exponent as close to one as you like.") as s:
            self.play(FadeIn(xr), FadeIn(yr), FadeIn(times))
            s.wait_until("g")
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in rows], lag_ratio=0.15), run_time=2.5)
            self.play(Create(line), FadeIn(pr), FadeIn(n2))
            s.wait_until("k")
            self.play(FadeIn(kar[0]))
            s.wait_until("t")
            self.play(FadeIn(kar[1]))
        self.play(FadeOut(VGroup(xr, yr, times, rows, line, pr, n2, kar)))

        # ------------------------------------------------------------ the FFT era
        tl = VGroup(
            Tex(r"1971 \quad Sch\"onhage--Strassen: $O(n\log n\log\log n)$", font_size=34),
            Tex(r"\qquad\quad conjecture: $n\log n$ is optimal", font_size=34, color=YELLOW_3B),
            Tex(r"2007 \quad F\"urer: $n\log n\cdot 2^{O(\log^* n)}$", font_size=34),
            Tex(r"2019 \quad Harvey--van der Hoeven: $O(n\log n)$", font_size=34, color=GREEN_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        with self.say(f"In 1971, {SS} used the fast Fourier transform to multiply in n log n log log n steps, "
                      f"{{c}}and proposed that n log n is the true order of growth. {{f}}{FUR} improved the bound in 2007, "
                      f"{{h}}and in 2019, {HVDH} reached n log n, matching the conjecture. "
                      "It looked like the end of the story.") as s:
            self.play(FadeIn(tl[0]))
            s.wait_until("c")
            self.play(FadeIn(tl[1]))
            s.wait_until("f")
            self.play(FadeIn(tl[2]))
            s.wait_until("h")
            self.play(FadeIn(tl[3]))
        self.play(FadeOut(tl))

        # ------------------------------------------------------------ the model
        tapes = VGroup()
        heads = VGroup()
        rng = np.random.default_rng(4)
        for k in range(3):
            t = bitrow(list(rng.integers(0, 2, 22)), GREY_B, 0.4, 24).move_to([0, 1.6 - 1.2 * k, 0])
            hd = Triangle(color=YELLOW_3B, fill_opacity=1).scale(0.12).next_to(t[5 + 4 * k], DOWN, buff=0.04)
            tapes.add(t)
            heads.add(hd)
        tl_ = VGroup(*[Tex(f"tape {k + 1}", font_size=26, color=GREY_A).next_to(tapes[k], LEFT, buff=0.25)
                       for k in range(3)])
        rules = VGroup(Tex(r"fixed finite alphabet, fixed number of tapes", font_size=32),
                       Tex(r"each head moves one cell per step: moving data costs time", font_size=32, color=YELLOW_3B)
                       ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.say("These bounds live in one precise model: the multitape Turing machine. {t}It has a fixed finite "
                      "alphabet, a fixed number of one-dimensional tapes, {h}and heads that move one cell per step. "
                      "There is no random access, so moving data around costs time. "
                      f"{{o}}Other models give other answers: {SCH} found a linear-time method on storage modification "
                      "machines. The question here is about tapes.") as s:
            self.play(FadeIn(tapes), FadeIn(tl_), FadeIn(heads))
            s.wait_until("t")
            self.play(FadeIn(rules[0]))
            s.wait_until("h")
            self.play(FadeIn(rules[1]), *[hd.animate.shift(RIGHT * 0.4 * (3 - k)) for k, hd in enumerate(heads)],
                      run_time=1.5)
            self.play(*[hd.animate.shift(LEFT * 0.4 * (k + 1)) for k, hd in enumerate(heads)], run_time=1.2)
        self.play(FadeOut(VGroup(tapes, tl_, heads, rules)))

        # ------------------------------------------------------------ the theorem
        thm = VGroup(Tex(r"\textbf{Theorem.} One fixed multitape Turing machine multiplies two", font_size=34),
                     Tex(r"$n$-bit integers exactly, for every $n$, in worst-case time", font_size=34),
                     MathTex(r"O\big(n(\log n)^{1-\kappa}\big),\qquad \kappa=2^{-182}", font_size=40)).arrange(
            DOWN, buff=0.22)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3)).to_edge(UP, buff=0.4)
        dis = Tex(r"$\Rightarrow$ $n\log n$ is \emph{not} optimal on multitape machines", font_size=34,
                  color=GREEN_3B).next_to(tb, DOWN, buff=0.35)
        tiny = VGroup(MathTex(r"\text{saving factor }(\log n)^{\kappa}=2", r"\iff \log_2 n=2^{2^{182}}", font_size=34),
                      MathTex(r"\iff n=2^{2^{2^{182}}}\text{ bits}", font_size=34, color=RED_3B)).arrange(
            DOWN, buff=0.2).next_to(dis, DOWN, buff=0.45)
        cor = Tex(r"also: division, square roots, binary matrix transposition", font_size=30,
                  color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.say("A manuscript in OpenAI's math catalogue claims: {t}one fixed multitape Turing machine "
                      "multiplies two n-bit integers exactly, for every n, in worst-case time of order n times log n "
                      "to the power one minus kappa, where kappa is two to the minus one hundred eighty-two. "
                      "{d}That would disprove the optimality of n log n in this model. {ti}How small is the saving? "
                      "It is a factor of log n to the kappa. For that factor to reach two, the numbers would need two "
                      "to the two to the two to the one hundred eighty-two bits. This is a statement about growth rates, "
                      "not a practical algorithm. {c}The same bound carries over to division, square roots, and "
                      "transposing binary matrices.") as s:
            s.wait_until("t")
            self.play(Write(thm), Create(tb[1]), run_time=3)
            s.wait_until("d")
            self.play(FadeIn(dis))
            s.wait_until("ti")
            self.play(Write(tiny[0]), run_time=2)
            self.play(Write(tiny[1]))
            s.wait_until("c")
            self.play(FadeIn(cor))
        self.play(FadeOut(VGroup(tb, dis, tiny, cor)))

        # ------------------------------------------------------------ where n log n comes from
        pipe = VGroup(Tex(r"digits", font_size=30), MathTex(r"\to", font_size=30), Tex(r"convolution", font_size=30),
                      MathTex(r"\to", font_size=30), Tex(r"multidimensional transforms", font_size=30),
                      MathTex(r"\to", font_size=30), Tex(r"over $\mathbb{C}[y]/(y^r+1)$", font_size=30)).arrange(
            RIGHT, buff=0.2).to_edge(UP, buff=0.45)
        shift_t = Tex(r"roots of unity are powers of $y$: multiplying by one is a signed shift", font_size=28,
                      color=GREY_A).next_to(pipe, DOWN, buff=0.25)
        lv = VGroup()
        for k in range(6):
            r = Rectangle(width=9.0, height=0.36, stroke_color=GREY_B, stroke_width=1.5, fill_color=BLUE_3B,
                          fill_opacity=0.12).move_to([-0.6, 0.6 - 0.5 * k, 0])
            lv.add(r)
        sweeps = VGroup(*[Arrow(r.get_left() + RIGHT * 0.1, r.get_right() + LEFT * 0.1, buff=0, color=YELLOW_3B,
                                stroke_width=3, max_tip_length_to_length_ratio=0.03) for r in lv])
        brn = Brace(lv[0], UP, color=GREY_B, buff=0.05)
        brn_t = MathTex(r"n\text{ bits}", font_size=28).next_to(brn, UP, buff=0.05)
        brl = Brace(lv, RIGHT, color=GREY_B)
        brl_t = MathTex(r"\sim\log n\text{ levels}", font_size=28).next_to(brl, RIGHT, buff=0.1)
        need = Tex(r"to go below $n\log n$: save on \emph{both} data movement and butterflies", font_size=30,
                   color=YELLOW_3B).to_edge(DOWN, buff=0.4)
        with self.say(f"Why is n log n so hard to beat? Following {HVDH}, the best algorithms turn multiplication into "
                      "multidimensional Fourier transforms, over polynomial rings where roots of unity are cheap: "
                      "multiplying by one is just a signed shift. {lv}What remains is rearranging data, shifting, and "
                      "simple butterflies. On a tape, each of about log n transform levels sweeps across all n bits. "
                      "That is n log n. {nd}To beat it, you must save on both data movement and arithmetic.") as s:
            self.play(FadeIn(pipe), run_time=1.5)
            self.play(FadeIn(shift_t))
            s.wait_until("lv")
            self.play(FadeIn(lv), GrowFromCenter(brn), FadeIn(brn_t))
            self.play(LaggedStart(*[GrowArrow(a) for a in sweeps], lag_ratio=0.3), GrowFromCenter(brl),
                      FadeIn(brl_t), run_time=3)
            s.wait_until("nd")
            self.play(FadeIn(need))
        self.play(FadeOut(VGroup(pipe, shift_t, lv, sweeps, brn, brn_t, brl, brl_t, need)))

        # ------------------------------------------------------------ XOR swap and the network
        hdr = Tex(r"Swapping with XORs", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.35)
        labs = [r"\text{start}", r"y\leftarrow y\oplus x", r"x\leftarrow x\oplus y", r"y\leftarrow y\oplus x"]

        def regs(k):
            a = bitrow(list(XSTEPS[k][0]), BLUE_3B, 0.42, 26)
            b = bitrow(list(XSTEPS[k][1]), YELLOW_3B, 0.42, 26)
            g = VGroup(a, b).arrange(DOWN, buff=0.18)
            return g

        rg = regs(0).move_to([-3.2, 1.0, 0])
        xl = MathTex("x", font_size=32, color=BLUE_3B).next_to(rg[0], LEFT, buff=0.25)
        yl = MathTex("y", font_size=32, color=YELLOW_3B).next_to(rg[1], LEFT, buff=0.25)
        stl = MathTex(labs[0], font_size=32).next_to(rg, DOWN, buff=0.3)
        with self.say("The new idea starts from a familiar trick. {x}You can swap two registers with three exclusive "
                      "ors, and no temporary storage: {a}y becomes y x-or x, {b}then x becomes x x-or y, {c}then y "
                      "becomes y x-or x. The final effect is a pure exchange, but the steps in between are "
                      "combinations of the data.") as s:
            self.play(Write(hdr))
            s.wait_until("x")
            self.play(FadeIn(rg), FadeIn(xl), FadeIn(yl), FadeIn(stl))
            for k, mk in zip([1, 2, 3], ["a", "b", "c"]):
                s.wait_until(mk)
                new = regs(k).move_to(rg)
                self.play(Transform(rg, new), Transform(stl, MathTex(labs[k], font_size=32).move_to(stl)), run_time=0.9)
        # intersection matrix
        nT = PAR.shape[0]
        cz = 0.16
        cells = VGroup()
        for i in range(nT):
            for j in range(nT):
                v = int(PAR[i, j])
                sq = Square(cz, stroke_width=0.5, stroke_color=GREY_D).set_fill(
                    YELLOW_3B if (v and i == j) else (RED_3B if v else BLACK), 0.85 if v else 0.0)
                sq.move_to([j * cz, -i * cz, 0])
                cells.add(sq)
        cells.move_to([3.3, -0.4, 0])
        mt = Tex(r"triples of $\{1,\dots,6\}$: $|S\cap T|\bmod 2$", font_size=28).next_to(cells, UP, buff=0.2)
        net = VGroup(
            Tex(r"the paper's network: values $x_T$, $y_S$ indexed", font_size=28),
            Tex(r"by triples from $\{1,\dots,100\}$", font_size=28),
            Tex(r"gather through 100 central wires,", font_size=28),
            Tex(r"scatter back: $|S\cap T|\bmod 2$", font_size=28),
            Tex(r"side wires cancel $|S\cap T|=1$", font_size=28, color=RED_3B),
            Tex(r"net effect: $y\leftarrow y+x$; scratch restored", font_size=28, color=GREEN_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([-3.3, -1.9, 0])
        with self.say("The paper builds a fixed, enormous network of this kind. It exchanges two banks of values, "
                      "and each 'add x to y' step goes through auxiliary wires whose arbitrary contents are restored "
                      "at the end. {tr}The values are indexed by triples from a hundred symbols. {g}Gathering through a "
                      "hundred central wires and scattering back adds, from each source triple to each target triple, "
                      "the parity of their intersection. {sd}Side wires cancel the pairs that meet in exactly one "
                      "point, {n}leaving exactly y plus x.") as s:
            s.wait_until("tr")
            self.play(FadeIn(net[0:2]))
            s.wait_until("g")
            self.play(FadeIn(net[2:4]), FadeIn(mt), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.002),
                      run_time=2)
            s.wait_until("sd")
            red = [cells[i * nT + j] for i in range(nT) for j in range(nT) if N1[i, j]]
            self.play(FadeIn(net[4]), *[Indicate(c, color=RED_3B, scale_factor=1.3) for c in red[:40]], run_time=1)
            s.wait_until("n")
            self.play(*[c.animate.set_fill(opacity=0) for c in red], FadeIn(net[5]), run_time=1.5)
        self.play(FadeOut(VGroup(hdr, rg, xl, yl, stl, cells, mt, net)))

        # ------------------------------------------------------------ frames and the recursion
        hdr = Tex(r"From wires to arrays: the recursive saving", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.35)
        w1 = VGroup(*[Square(0.3, stroke_color=BLUE_3B, stroke_width=1.5).set_fill(BLUE_3B, 0.2) for _ in range(10)]
                    ).arrange(RIGHT, buff=0)
        w2 = w1.copy().set_color(TEAL_3B)
        gate = RoundedRectangle(width=1.0, height=1.4, corner_radius=0.1, color=YELLOW_3B)
        diag = VGroup(w1, gate, w2).arrange(RIGHT, buff=0.5).next_to(hdr, DOWN, buff=0.5)
        gl = MathTex("G", font_size=34, color=YELLOW_3B).move_to(gate)
        fu = MathTex(r"D_u g", font_size=30, color=BLUE_3B).next_to(w1, DOWN, buff=0.15)
        fv = MathTex(r"D_v g", font_size=30, color=TEAL_3B).next_to(w2, DOWN, buff=0.15)
        fr = VGroup(Tex(r"each array is stored in a changing \emph{frame} $D$;", font_size=30),
                    Tex(r"gates act pointwise and commute with frames", font_size=30)).arrange(
            DOWN, buff=0.12).next_to(diag, DOWN, buff=0.5)
        eqs = VGroup(
            Tex(r"changing frames along all edges costs $s$ smaller calls of the same procedure", font_size=30),
            MathTex(r"s<W\cdot m\qquad(W=\#\text{wires},\ m=10^6)", font_size=36, color=GREEN_3B),
            MathTex(r"\text{parameter}\times m\ \Rightarrow\ \text{cost per bit}\times\frac{s}{W}<m", font_size=36),
            MathTex(r"\Rightarrow\ \text{cost per bit}\ \propto f^{\tau},\quad \tau<1", font_size=36, color=YELLOW_3B),
        ).arrange(DOWN, buff=0.28).next_to(fr, DOWN, buff=0.4)
        with self.say("Now replace every wire by a whole array of data. {f}Each array is stored in a changing frame: "
                      "a change of representation. Gates act pointwise, so they commute with frames, the frames cancel, "
                      "and the network exchanges entire arrays. {s}Changing frames along the edges costs smaller calls "
                      "of the same procedure, and the network is designed so that the total number of those calls, s, "
                      "is less than the number of wires times m, a million. {r}So each time the problem parameter grows "
                      "by a factor of m, the cost per bit grows by s over W, which is less than m. {p}That is a power "
                      "saving, and it speeds up both the data rearrangements and the butterfly layers.") as s:
            self.play(Write(hdr))
            self.play(FadeIn(w1), FadeIn(gate), FadeIn(gl), FadeIn(w2))
            s.wait_until("f")
            self.play(FadeIn(fu), FadeIn(fv), FadeIn(fr))
            s.wait_until("s")
            self.play(FadeIn(eqs[0]))
            self.play(Write(eqs[1]))
            s.wait_until("r")
            self.play(Write(eqs[2]))
            s.wait_until("p")
            self.play(Write(eqs[3]))
        self.play(FadeOut(VGroup(hdr, w1, gate, gl, w2, fu, fv, fr, eqs)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Exact $n$-bit multiplication in $O\big(n(\log n)^{1-\kappa}\big)$ time, $\kappa=2^{-182}$",
             r"on one fixed multitape Turing machine: $n\log n$ is not optimal there",
             r"also: division, square root, binary matrix transposition",
             r"Manuscript: 73 pages, produced by an OpenAI model"],
            False, r"\emph{Integer multiplication below n log n} (Sept.\ 2026)")
        with self.say("This seventy-three page manuscript, produced by an OpenAI model, has not been formalized or peer "
                      "reviewed, and it needs careful checking by experts. {c}If it holds, n log n, long conjectured "
                      "to be the final answer for multiplication on multitape machines, is not.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("c")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
