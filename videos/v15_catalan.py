from pathlib import Path

import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(Path(__file__).parent / "data" / "v15.npz")
GV = float(D["G"])

KAST = "[Kasteleyn](/kˈæstəlˌIn/)"
APERY = "[Apéry](/ˌɑpAɹˈi/)"
ZUD = "[Zudilin](/zudˈilɪn/)"
RIV = "[Rivoal](/ɹivwˈɑl/)"
AGOL = "[Agol](/ˈAɡɔl/)"
SUN = "[Zhi-Wei](/ʤˈɜ wˈA/) Sun"


def domino_tiling(n=8, flips=4000, seed=3):
    """Random domino tiling of an n x n board by 2x2 flips, starting from all-horizontal."""
    rng = np.random.default_rng(seed)
    partner = {}
    for r in range(n):
        for c in range(0, n, 2):
            partner[(r, c)] = (r, c + 1)
            partner[(r, c + 1)] = (r, c)
    for _ in range(flips):
        r, c = rng.integers(0, n - 1, size=2)
        a, b, cc, d = (r, c), (r, c + 1), (r + 1, c), (r + 1, c + 1)
        if partner[a] == b and partner[cc] == d:
            partner[a], partner[cc], partner[b], partner[d] = cc, a, d, b
        elif partner[a] == cc and partner[b] == d:
            partner[a], partner[b], partner[cc], partner[d] = b, a, d, cc
    doms = set()
    for k, v in partner.items():
        doms.add(tuple(sorted([k, v])))
    return sorted(doms)


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "005", r"Catalan's Constant Is Irrational",
                          r"$G=1-\tfrac19+\tfrac1{25}-\tfrac1{49}+\cdots$ is not a fraction")
        with self.say("Is Catalan's constant a fraction?"):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ three sibling series
        r1 = MathTex(r"1+\frac14+\frac19+\frac1{16}+\cdots", "=", r"\frac{\pi^2}{6}", font_size=42)
        r2 = MathTex(r"1-\frac13+\frac15-\frac17+\cdots", "=", r"\frac{\pi}{4}", font_size=42)
        r3 = MathTex(r"1-\frac19+\frac1{25}-\frac1{49}+\cdots", "=", r"G", font_size=42)
        rows = VGroup(r1, r2, r3).arrange(DOWN, buff=0.55, aligned_edge=LEFT).shift(UP * 0.6 + LEFT * 1.0)
        for r in rows:
            r[1].align_to(rows[0][1], LEFT)
            r[2].next_to(r[1], RIGHT, buff=0.25)
        r1[2].set_color(BLUE_3B)
        r2[2].set_color(TEAL_3B)
        r3[2].set_color(YELLOW_3B)
        n1 = Tex("Euler", font_size=28, color=GREY_A).next_to(r1, RIGHT, buff=0.6)
        n2 = Tex("Leibniz", font_size=28, color=GREY_A).next_to(r2, RIGHT, buff=0.6).align_to(n1, LEFT)
        n3 = Tex(r"$\approx 0.9159655941\ldots$", font_size=32, color=YELLOW_3B).next_to(r3, RIGHT, buff=0.6).align_to(
            n1, LEFT)
        ps = D["ps"][:24]
        ax = Axes(x_range=[0, 24, 4], y_range=[0.86, 1.0, 0.04], x_length=10, y_length=3.0, tips=False,
                  axis_config={"color": GREY_B, "font_size": 22},
                  x_axis_config={"numbers_to_include": [4, 8, 12, 16, 20, 24]},
                  y_axis_config={"numbers_to_include": [0.88, 0.92, 0.96, 1.0],
                                 "decimal_number_config": {"num_decimal_places": 2}}).to_edge(DOWN, buff=0.9)
        gl = DashedLine(ax.c2p(0, GV), ax.c2p(24, GV), color=YELLOW_3B)
        gll = MathTex("G", font_size=32, color=YELLOW_3B).next_to(gl, RIGHT, buff=0.1)
        dots = VGroup(*[Dot(ax.c2p(j + 1, v), radius=0.06, color=BLUE_3B) for j, v in enumerate(ps)])
        zig = VMobject(color=BLUE_3B, stroke_width=2, stroke_opacity=0.6).set_points_as_corners(
            [ax.c2p(j + 1, v) for j, v in enumerate(ps)])
        xl = Tex("number of terms", font_size=26).next_to(ax.x_axis, DOWN, buff=0.45)
        with self.say("Add up the reciprocals of the squares, one plus a quarter plus a ninth, and so on, and Euler "
                      "showed that you get pi squared over six. {b}Take the odd numbers instead, with alternating "
                      "signs, and you get pi over four. {c}Now combine the two ideas: odd squares, with alternating "
                      "signs. One, minus a ninth, plus a twenty-fifth, minus a forty-ninth. {g}The sum is Catalan's "
                      "constant, G, about zero point nine one six. {p}Unlike its siblings, no one has found a "
                      "closed form for it in terms of pi, or any other classical constant.") as s:
            self.play(Write(r1), run_time=2)
            self.play(FadeIn(n1))
            s.wait_until("b")
            self.play(Write(r2), run_time=2)
            self.play(FadeIn(n2))
            s.wait_until("c")
            self.play(Write(r3), run_time=2.5)
            s.wait_until("g")
            self.play(FadeIn(n3))
            self.play(VGroup(rows, n1, n2, n3).animate.to_edge(UP, buff=0.4))
            s.wait_until("p")
            self.play(Create(ax), Create(gl), FadeIn(gll), FadeIn(xl))
            self.play(Create(zig), LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.08), run_time=3)
        self.play(FadeOut(VGroup(rows, n1, n2, n3, ax, gl, gll, dots, zig, xl)))

        # ------------------------------------------------------------ dominoes
        n, cs = 8, 0.5
        origin = np.array([-6.0, 2.0, 0])
        board = VGroup()
        cols = [BLUE_3B, TEAL_3B, YELLOW_3B, ORANGE_3B]
        for (r0, c0), (r1_, c1_) in domino_tiling(n):
            horiz = r0 == r1_
            w, h = (2 * cs, cs) if horiz else (cs, 2 * cs)
            cx = origin[0] + (c0 + c1_ + 1) / 2 * cs
            cy = origin[1] - (r0 + r1_ + 1) / 2 * cs
            k = (0 if horiz else 2) + ((c0 if horiz else r0) % 2)
            board.add(RoundedRectangle(width=w - 0.06, height=h - 0.06, corner_radius=0.06, stroke_width=1.5,
                                       stroke_color=WHITE).set_fill(cols[k], 0.75).move_to([cx, cy, 0]))
        cnt = Tex(r"$12{,}988{,}816$ tilings", font_size=34, color=YELLOW_3B).next_to(board, DOWN, buff=0.3)
        dom = D["dom"]
        ax2 = Axes(x_range=[0, 80, 20], y_range=[0.2, 0.3, 0.02], x_length=5.6, y_length=3.6, tips=False,
                   axis_config={"color": GREY_B, "font_size": 22},
                   x_axis_config={"numbers_to_include": [20, 40, 60, 80]},
                   y_axis_config={"numbers_to_include": [0.22, 0.26, 0.30],
                                  "decimal_number_config": {"num_decimal_places": 2}}).move_to(RIGHT * 3.2 + UP * 0.4)
        sel = dom[dom[:, 0] >= 4]
        dpts = VGroup(*[Dot(ax2.c2p(a, b), radius=0.045, color=TEAL_3B) for a, b in sel[:, :2]])
        lim = DashedLine(ax2.c2p(0, GV / np.pi), ax2.c2p(80, GV / np.pi), color=YELLOW_3B)
        liml = MathTex(r"G/\pi", font_size=30, color=YELLOW_3B).next_to(lim, UP, buff=0.08).align_to(lim, RIGHT)
        ylab = MathTex(r"\frac{\log(\#\text{tilings})}{\text{area}}", font_size=30).next_to(ax2, UP, buff=0.15)
        xlab = Tex(r"side of the square board", font_size=26).next_to(ax2.x_axis, DOWN, buff=0.35)
        hyp = Tex(r"Hyperbolic geometry: the Whitehead link complement has volume\\ $4G\approx 3.6639$, "
                  r"the least for orientable two-cusped manifolds (Agol)", font_size=30).to_edge(DOWN, buff=0.35).shift(RIGHT * 1.0)
        with self.say("Catalan's constant turns up all over mathematics. {d}A chessboard can be tiled by dominoes in "
                      "exactly twelve million, nine hundred eighty-eight thousand, eight hundred sixteen ways. "
                      f"{{e}}For larger boards, the count grows like e to the power G over pi times the area, a "
                      f"classical result of {KAST}, and of Temperley and Fisher. {{h}}And in hyperbolic geometry, "
                      "four times G is the volume of the Whitehead link complement, which by a theorem of "
                      f"Ian {AGOL} is the smallest volume of any orientable hyperbolic three-manifold with two cusps.") as s:
            s.wait_until("d")
            self.play(LaggedStart(*[FadeIn(b, scale=0.6) for b in board], lag_ratio=0.03), run_time=2.5)
            self.play(FadeIn(cnt))
            s.wait_until("e")
            self.play(Create(ax2), FadeIn(ylab), FadeIn(xlab), Create(lim), FadeIn(liml))
            self.play(LaggedStart(*[FadeIn(p) for p in dpts], lag_ratio=0.05), run_time=2.5)
            s.wait_until("h")
            self.play(FadeIn(hyp, shift=UP * 0.2))
        self.play(FadeOut(VGroup(board, cnt, ax2, dpts, lim, liml, ylab, xlab, hyp)))

        # ------------------------------------------------------------ beta values
        beta = MathTex(r"\beta(s)=\sum_{j\ge0}\frac{(-1)^j}{(2j+1)^s}", font_size=42).to_edge(UP, buff=0.5)
        odd = MathTex(r"\beta(1)=\frac{\pi}{4},\qquad \beta(3)=\frac{\pi^3}{32},\qquad\ldots", font_size=38,
                      color=TEAL_3B).next_to(beta, DOWN, buff=0.5)
        oddl = Tex("odd values: rational multiples of powers of $\\pi$", font_size=28, color=GREY_A).next_to(
            odd, DOWN, buff=0.2)
        boxes = VGroup()
        for k in range(1, 8):
            t = MathTex(rf"\beta({2 * k})", font_size=34)
            b = RoundedRectangle(width=1.35, height=0.8, corner_radius=0.1, color=GREY_B)
            boxes.add(VGroup(b, t))
        boxes.arrange(RIGHT, buff=0.22).shift(DOWN * 1.0)
        boxes[0][1].set_color(YELLOW_3B)
        gname = MathTex("G", font_size=32, color=YELLOW_3B).next_to(boxes[0], UP, buff=0.15)
        br7 = Brace(boxes, DOWN, color=BLUE_3B)
        t7 = Tex(r"Rivoal--Zudilin (2003): at least one of these is irrational", font_size=28,
                 color=BLUE_3B).next_to(br7, DOWN, buff=0.15)
        br5 = Brace(boxes[:5], DOWN, color=BLUE_3B)
        t5 = Tex(r"later narrowed to these five (Zudilin; Lai--Zhou)", font_size=28, color=BLUE_3B).next_to(
            br5, DOWN, buff=0.15)
        with self.say("Why was this so hard? G is the simplest even value of the Dirichlet beta function. "
                      "{o}The odd values are rational multiples of powers of pi. {e}The even values are a mystery. "
                      f"{{rz}}In 2003, {RIV} and {ZUD} proved that infinitely many even values are irrational, and "
                      "that at least one of the first seven is. {f}Later work narrowed that to one of the first "
                      "five. {w}But which one? Nobody could say.") as s:
            self.play(Write(beta))
            s.wait_until("o")
            self.play(FadeIn(odd), FadeIn(oddl))
            s.wait_until("e")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.1), FadeIn(gname))
            s.wait_until("rz")
            self.play(GrowFromCenter(br7), FadeIn(t7))
            s.wait_until("f")
            self.play(ReplacementTransform(br7, br5), ReplacementTransform(t7, t5), boxes[5:].animate.set_opacity(0.3))
            s.wait_until("w")
            self.play(Indicate(boxes[0], color=YELLOW_3B))
        self.play(FadeOut(VGroup(beta, odd, oddl, boxes, gname, br5, t5)))

        # ------------------------------------------------------------ irrationality criterion
        hdr = Tex(r"If $G=\dfrac ab$, then $A\,G-B\in\dfrac1b\mathbb{Z}$ for all integers $A,B$", font_size=38
                  ).to_edge(UP, buff=0.5)
        nl = NumberLine(x_range=[-3.5, 3.5, 1], length=12, include_tip=False, color=GREY_B).shift(UP * 0.4)
        lbls = VGroup(*[MathTex(s_, font_size=30).next_to(nl.n2p(k), DOWN, buff=0.2) for k, s_ in
                        [(-3, r"-\tfrac3b"), (-2, r"-\tfrac2b"), (-1, r"-\tfrac1b"), (0, "0"), (1, r"\tfrac1b"),
                         (2, r"\tfrac2b"), (3, r"\tfrac3b")]])
        allowed = VGroup(*[Dot(nl.n2p(k), radius=0.09, color=TEAL_3B) for k in range(-3, 4)])
        gap = Rectangle(width=nl.n2p(1)[0] - nl.n2p(-1)[0] - 0.25, height=0.5, stroke_width=0).set_fill(
            RED_3B, 0.25).move_to(nl.n2p(0))
        gap_l = Tex(r"no nonzero value can land here", font_size=28, color=RED_3B).next_to(gap, UP, buff=0.55)
        seq_x = [3.0, 2.0, 1.0, 0.5]
        seq = VGroup(*[Dot(nl.n2p(x) + UP * 0.4, radius=0.11, color=YELLOW_3B) for x in seq_x])
        crit = Tex(r"So: nonzero integer combinations $A_mG-B_m\to0$ $\Rightarrow$ $G$ is irrational", font_size=32
                   ).shift(DOWN * 1.6)
        ap = Tex(r"Ap\'ery (1979): this works for $\zeta(3)$. For $G$, fast approximations exist,\\"
                 r"but after clearing denominators the combinations do not shrink (Zudilin).", font_size=30,
                 color=GREY_A).shift(DOWN * 2.7)
        with self.say("Here is the classic way to prove a number is irrational. {a}Suppose G equals a over b. "
                      "Then any combination A times G minus B, with whole numbers A and B, is a multiple of one "
                      "over b. {gap}So if it isn't zero, it is at least one over b in size. {s}If you can build "
                      "such combinations that are nonzero but shrink toward zero, you get a contradiction. "
                      f"{{ap}}This is how {APERY} proved that zeta of three is irrational, in 1979. For Catalan's "
                      f"constant, {ZUD} found fast approximations, but after clearing denominators, the "
                      "combinations refuse to shrink.") as s:
            s.wait_until("a")
            self.play(Write(hdr), run_time=2)
            self.play(Create(nl), FadeIn(lbls), FadeIn(allowed))
            s.wait_until("gap")
            self.play(FadeIn(gap), FadeIn(gap_l))
            s.wait_until("s")
            self.play(FadeIn(seq[0], scale=2))
            for d in seq[1:]:
                self.play(FadeIn(d, scale=2), run_time=0.6)
            self.play(seq[-1].animate.set_color(RED_3B), Flash(seq[-1], color=RED_3B))
            self.play(FadeIn(crit))
            s.wait_until("ap")
            self.play(FadeIn(ap))
        self.play(FadeOut(VGroup(hdr, nl, lbls, allowed, gap, gap_l, seq, crit, ap)))

        # ------------------------------------------------------------ theorem
        thm = VGroup(Tex(r"\textbf{Theorem.} Catalan's constant $G$ is irrational.", font_size=46),
                     Tex(r"Corollary: $4G$, the least volume of an orientable hyperbolic\\ 3-manifold with two "
                         r"cusps, is irrational.", font_size=32, color=GREY_A)).arrange(DOWN, buff=0.4)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.35))
        with self.say("A manuscript in OpenAI's math catalogue claims to settle it: {t}Catalan's constant is "
                      "irrational. {c}As a corollary, that hyperbolic volume, four G, is irrational too. {l}And the "
                      "main statement has been formalized in the Lean proof assistant.") as s:
            s.wait_until("t")
            self.play(Write(thm[0]), Create(tb[1]), run_time=2)
            s.wait_until("c")
            self.play(FadeIn(thm[1]))
            s.wait_until("l")
            lean = Tex(r"Lean: formalized \checkmark", font_size=32, color=GREEN_3B).next_to(tb, DOWN, buff=0.4)
            self.play(FadeIn(lean))
        self.play(FadeOut(VGroup(tb, lean)))

        # ------------------------------------------------------------ the determinant
        hdr = Tex("The proof: one giant determinant instead of one small number", font_size=38,
                  color=YELLOW_3B).to_edge(UP, buff=0.35)
        k = 10
        grid = VGroup(*[Square(0.28, stroke_width=1, stroke_color=GREY_B).set_fill(BLUE_3B, 0.15 + 0.5 * ((i * 7 + j * 3) % 5) / 5)
                        for i in range(k) for j in range(k)]).arrange_in_grid(k, k, buff=0.04)
        bars = VGroup(Line(UP, DOWN).set_height(grid.height + 0.2).next_to(grid, LEFT, buff=0.1),
                      Line(UP, DOWN).set_height(grid.height + 0.2).next_to(grid, RIGHT, buff=0.1))
        det = VGroup(grid, bars).move_to(LEFT * 4.3 + DOWN * 0.4)
        dl = MathTex(r"\Delta_N", font_size=40, color=BLUE_3B).next_to(det, UP, buff=0.2)
        size = Tex(r"size $48N\times48N$", font_size=28).next_to(det, DOWN, buff=0.2)
        hl = SurroundingRectangle(grid[23], color=YELLOW_3B, buff=0.02)
        entry = MathTex(r"\text{entry}", "=", r"\iint(\cdots)", "=", r"r_1", "+", r"r_2\,G", "+", r"r_3\,\zeta(2)",
                        font_size=38).move_to(RIGHT * 2.0 + UP * 1.7)
        entry[6].set_color(YELLOW_3B)
        entry[8].set_color(RED_3B)
        rat = Tex(r"$r_1,r_2,r_3$ rational", font_size=28, color=GREY_A).next_to(entry, DOWN, buff=0.2)
        cross = Cross(entry[7:], stroke_color=RED_3B, stroke_width=5)
        tay = Tex(r"rows: polynomials with matching Taylor coefficients\\ to very high order $\Rightarrow$ the "
                  r"$\zeta(2)$ parts cancel", font_size=30).next_to(rat, DOWN, buff=0.45)
        ifq = Tex(r"$G=\tfrac ab\ \Longrightarrow\ \Delta_N\in\mathbb{Q}$,\\ with denominators controlled prime by prime",
                  font_size=32, color=TEAL_3B).next_to(tay, DOWN, buff=0.4)
        nz = Tex(r"$N=p$ prime: Frobenius reduces $\Delta_p$ to 3 fixed rational matrices;\\ an exact finite "
                 r"certificate shows $\Delta_p\neq0$", font_size=30, color=GREEN_3B).to_edge(DOWN, buff=0.35).shift(
            RIGHT * 1.6)
        with self.say("The proof replaces single combinations with huge determinants. {d}For each N, it builds a "
                      "determinant of size forty-eight N, whose entries are explicit double integrals. "
                      "{e}Each entry works out to a rational combination of one, G, and zeta of two, which is pi "
                      "squared over six. {c}The rows are polynomials chosen to agree to very high order in their "
                      "Taylor expansions, and that agreement makes the zeta of two parts cancel in every entry. "
                      "{r}So if G were a fraction, every determinant would be a rational number, with denominators "
                      "that can be controlled prime by prime. {nz}It also has to be nonzero. When N is a large "
                      "prime, a Frobenius argument reduces the giant matrix to three fixed rational matrices, whose "
                      "nonvanishing is checked by an exact finite certificate.") as s:
            self.play(Write(hdr))
            s.wait_until("d")
            self.play(FadeIn(grid, lag_ratio=0.01), Create(bars), FadeIn(dl), FadeIn(size), run_time=2)
            s.wait_until("e")
            self.play(Create(hl))
            self.play(TransformFromCopy(grid[23], entry), run_time=1.5)
            self.play(FadeIn(rat))
            s.wait_until("c")
            self.play(FadeIn(tay))
            self.play(Create(cross))
            s.wait_until("r")
            self.play(FadeIn(ifq))
            s.wait_until("nz")
            self.play(FadeIn(nz))
        self.play(FadeOut(VGroup(hdr, grid, bars, dl, size, hl, entry, rat, cross, tay, ifq, nz)))

        # ------------------------------------------------------------ the squeeze
        Lf = MathTex(r"L_N=\frac{\log|\Delta_N|}{(48N)^2}-\frac12\log 2", font_size=42).to_edge(UP, buff=0.45)
        LO, HI = -2.29084, -2.290939875
        nl = NumberLine(x_range=[-2.40, -2.20, 0.05], length=11, include_numbers=True, font_size=24,
                        decimal_number_config={"num_decimal_places": 2}).shift(DOWN * 0.3)

        def marks(line, lo_lab_dir=UP):
            lo = Line(line.n2p(LO) + UP * 0.4, line.n2p(LO) + DOWN * 0.4, color=GREEN_3B, stroke_width=6)
            hi = Line(line.n2p(HI) + UP * 0.4, line.n2p(HI) + DOWN * 0.4, color=RED_3B, stroke_width=6)
            right = Rectangle(width=line.get_right()[0] - line.n2p(LO)[0], height=0.3, stroke_width=0).set_fill(
                GREEN_3B, 0.35)
            right.move_to(line.n2p(LO), aligned_edge=LEFT).shift(UP * 0.0)
            left = Rectangle(width=line.n2p(HI)[0] - line.get_left()[0], height=0.3, stroke_width=0).set_fill(
                RED_3B, 0.35)
            left.move_to(line.n2p(HI), aligned_edge=RIGHT)
            return lo, hi, right, left

        lo, hi, right, left = marks(nl)
        lot = Tex(r"arithmetic (if $G\in\mathbb{Q}$):\\ $\liminf L_p>-2.29084$", font_size=30, color=GREEN_3B
                  ).next_to(nl, UP, buff=0.7).shift(RIGHT * 3.2)
        hit = Tex(r"analysis:\\ $\limsup L_N\le-2.290939875$", font_size=30, color=RED_3B).next_to(
            nl, DOWN, buff=0.9).shift(LEFT * 3.2)
        nl2 = NumberLine(x_range=[-2.2912, -2.2906, 0.0001], length=11, include_numbers=True, font_size=22,
                         decimal_number_config={"num_decimal_places": 4}).move_to(nl)
        lo2, hi2, right2, left2 = marks(nl2)
        gapb = BraceBetweenPoints(nl2.n2p(HI) + DOWN * 0.45, nl2.n2p(LO) + DOWN * 0.45, DOWN, color=YELLOW_3B)
        gapt = Tex(r"$\approx 10^{-4}$: no room for $L_p$", font_size=30, color=YELLOW_3B).next_to(gapb, DOWN,
                                                                                                buff=0.1)
        with self.say("Now measure the determinant on a logarithmic scale, normalized by the square of its size. "
                      "{lo}Arithmetic says that a nonzero fraction with those denominators can't be too small: "
                      "along primes, the normalized size stays above minus two point two nine zero eight four. "
                      "{hi}Analysis, using an integral formula, logarithmic potential theory, and bounds certified "
                      "in exact rational arithmetic, says it must end up at most about minus two point two nine zero "
                      "nine four. {z}Zoom in. The two bounds miss each other by about one ten-thousandth. {x}That sliver "
                      "is enough. No number can satisfy both, so G cannot be a fraction.") as s:
            self.play(Write(Lf), Create(nl))
            s.wait_until("lo")
            self.play(Create(lo), FadeIn(right), FadeIn(lot))
            s.wait_until("hi")
            self.play(Create(hi), FadeIn(left), FadeIn(hit))
            s.wait_until("z")
            self.play(ReplacementTransform(nl, nl2), ReplacementTransform(lo, lo2), ReplacementTransform(hi, hi2),
                      ReplacementTransform(right, right2), ReplacementTransform(left, left2), run_time=2.5)
            self.play(GrowFromCenter(gapb), FadeIn(gapt))
            s.wait_until("x")
            self.play(Indicate(gapt, color=YELLOW_3B))
        self.play(FadeOut(Group(*self.mobjects)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Catalan's constant $G=\sum_{j\ge0}(-1)^j/(2j+1)^2$ is irrational",
             r"Corollary: the hyperbolic volume $4G$ (Whitehead link) is irrational",
             r"Manuscript: 44 pages, produced by an OpenAI model"],
            True, r"\emph{Catalan's constant is irrational} (Sept.\ 2026)")
        with self.say("The manuscript is forty-four pages, produced by an OpenAI model. {l}Its main theorem, that "
                      "Catalan's constant is irrational, has been formalized and checked in the Lean proof "
                      "assistant. The manuscript notes that a separate preprint, by {SUN}, has also announced a proof. "
                      "Catalan's constant, it seems, is finally known not to be a fraction.".replace("{SUN}", SUN)) as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
