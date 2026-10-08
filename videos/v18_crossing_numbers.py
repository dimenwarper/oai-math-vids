from pathlib import Path

import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(Path(__file__).parent / "data" / "v18.npz")

TUR = "[Turán](/tˈʊɹɑn/)"
ZAR = "[Zarankiewicz](/zˌɑɹɑnkjˈɛvɪʧ/)"
HAR = "[Harary](/həɹˈɛɹi/)"
AICH = "[Aichholzer](/ˈIkhˌOlʦəɹ/)"
KLEIT = "[Kleitman](/klˈItmən/)"


def semicircle(a, b, up, color, width=2.5):
    h, r = (a + b) / 2, (b - a) / 2
    return Arc(radius=r, start_angle=PI if up else -PI, angle=-PI if up else PI, arc_center=np.array([h, 0, 0]),
               color=color, stroke_width=width)


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "165", "Crossing Numbers of Complete Graphs",
                          r"The Harary--Hill and Zarankiewicz formulas")
        with self.say("How few crossings does it take to draw a complete graph?"):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.4)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ the brickyard
        s = 0.95
        A, B, X = D["zA"] * s, D["zB"] * s, D["zX"] * s
        org = LEFT * 2.6 + DOWN * 0.3

        def p2(v):
            return org + np.array([v[0], v[1], 0])

        kil = VGroup(*[Square(0.28, color=RED_3B, fill_opacity=1).move_to(p2(a)) for a in A])
        yar = VGroup(*[Dot(p2(b), radius=0.13, color=BLUE_3B) for b in B])
        edges = VGroup(*[Line(p2(a), p2(b), color=GREY_B, stroke_width=2.5) for a in A for b in B])
        xs = VGroup(*[Dot(p2(x), radius=0.075, color=YELLOW_3B) for x in X])
        leg = VGroup(VGroup(Square(0.25, color=RED_3B, fill_opacity=1), Tex("kilns", font_size=30)).arrange(RIGHT),
                     VGroup(Dot(radius=0.12, color=BLUE_3B), Tex("storage yards", font_size=30)).arrange(RIGHT)
                     ).arrange(DOWN, aligned_edge=LEFT).move_to(RIGHT * 4.3 + UP * 2.6)
        cnt = Tex(r"12 crossings", font_size=40, color=YELLOW_3B).move_to(RIGHT * 4.3 + UP * 1.1)
        zf = MathTex(r"Z(m,n)=\left\lfloor\tfrac m2\right\rfloor\left\lfloor\tfrac{m-1}2\right\rfloor"
                     r"\left\lfloor\tfrac n2\right\rfloor\left\lfloor\tfrac{n-1}2\right\rfloor", font_size=36
                     ).move_to(RIGHT * 3.6 + DOWN * 0.5)
        zx = MathTex(r"Z(4,6)=2\cdot1\cdot3\cdot2=12", font_size=34, color=GREY_A).next_to(zf, DOWN, buff=0.3)
        gap = VGroup(Tex(r"claimed optimal; the proof had a gap", font_size=28, color=RED_3B),
                     Tex(r"1970, Kleitman: true if one side has $\le 6$", font_size=28),
                     Tex(r"1993, Woodall: $K_{7,7}$, $K_{7,9}$ by computer", font_size=28)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(zx, DOWN, buff=0.4)
        with self.say(f"In 1944, Paul {TUR} was doing forced labor at a brick factory near Budapest. Rail tracks led "
                      "from the kilns to the storage yards, and where tracks crossed, the carts tended to jump the "
                      "rails. {q}So he asked: if every kiln is joined to every yard, how few crossings can there be? "
                      f"{{z}}{ZAR} proposed this drawing: kilns on a horizontal line, yards on a vertical line, each "
                      "split evenly between the two sides, joined by straight tracks. {c}Four kilns and six yards "
                      "give twelve crossings, and in general this product of four floors. {g}He claimed it was best "
                      f"possible, but the proof had a gap. {KLEIT} proved the formula when one side has at most six "
                      "vertices, and Woodall checked a few more cases by computer.") as s_:
            self.play(FadeIn(kil), FadeIn(yar), FadeIn(leg))
            s_.wait_until("q")
            self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.04), run_time=2.5)
            self.bring_to_front(kil, yar)
            s_.wait_until("c")
            self.play(LaggedStart(*[GrowFromCenter(x) for x in xs], lag_ratio=0.1), FadeIn(cnt), run_time=1.5)
            self.play(Write(zf))
            self.play(FadeIn(zx))
            s_.wait_until("g")
            self.play(FadeIn(gap[0]))
            self.play(FadeIn(gap[1:]))
        self.play(FadeOut(VGroup(kil, yar, edges, xs, leg, cnt, zf, zx, gap)))

        # ------------------------------------------------------------ complete graphs, two-page drawing
        pos = D["pos7"]
        E7, S7, X7 = D["E7"], D["S7"], D["X7"]
        base = DOWN * 0.45
        ys = 0.5  # squash the semicircles vertically (an affine map: same crossings)
        spine = Line(LEFT * 6.3, RIGHT * 6.3, color=GREY_D).shift(base)
        vd = VGroup(*[Dot(np.array([x, 0, 0]) + base, radius=0.1, color=WHITE) for x in pos])
        vl = VGroup(*[MathTex(str(k), font_size=26).next_to(vd[k], DOWN + RIGHT * 0.3, buff=0.08)
                      for k in range(7)])
        arcs = VGroup(*[semicircle(pos[i], pos[j], sd > 0, BLUE_3B if sd > 0 else ORANGE_3B)
                        .stretch(ys, 1, about_point=ORIGIN).shift(base) for (i, j), sd in zip(E7, S7)])
        xd = VGroup(*[Dot(np.array([x, ys * y, 0]) + base, radius=0.08, color=YELLOW_3B) for x, y in X7])
        hh = MathTex(r"\mathrm{cr}(K_n)\overset{?}{=}\tfrac14\left\lfloor\tfrac n2\right\rfloor"
                     r"\left\lfloor\tfrac{n-1}2\right\rfloor\left\lfloor\tfrac{n-2}2\right\rfloor"
                     r"\left\lfloor\tfrac{n-3}2\right\rfloor", font_size=40).to_edge(UP, buff=0.25)
        vals = Tex(r"$K_5$: 1 \quad $K_6$: 3 \quad $K_7$: 9 \quad $K_8$: 18 \quad $K_9$: 36", font_size=32,
                   color=GREY_A).next_to(hh, DOWN, buff=0.2)
        rule = Tex(r"edge $ij$ above if $i+j \bmod 7\in\{0,1,2\}$, else below", font_size=28).next_to(
            vals, DOWN, buff=0.15)
        c7 = Tex(r"$K_7$: 2 crossings above + 7 below = 9", font_size=32, color=YELLOW_3B).move_to(vals)
        with self.say(f"The same question for the complete graph K n, every vertex joined to every other. {{hh}}In 1963, "
                      f"{HAR} and Hill conjectured the answer: a quarter of a product of four "
                      "floors. One crossing for K five, three for K six, nine for K seven. "
                      "{tp}Here is one drawing that achieves it. Put the vertices on a line, and draw each edge as a "
                      "semicircle, above or below, depending on the sum of its endpoints modulo n. {k7}For K seven, "
                      "that gives two crossings above and seven below: nine.") as s_:
            self.play(Create(spine), FadeIn(vd), FadeIn(vl))
            s_.wait_until("hh")
            self.play(Write(hh), run_time=2)
            self.play(FadeIn(vals))
            s_.wait_until("tp")
            self.play(FadeIn(rule))
            self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.08), run_time=3)
            s_.wait_until("k7")
            self.play(LaggedStart(*[GrowFromCenter(x) for x in xd], lag_ratio=0.1), FadeOut(vals), FadeIn(c7),
                      run_time=1.5)
        self.play(FadeOut(VGroup(spine, vd, vl, arcs, xd, rule, c7)), hh.animate.scale(0.85).to_edge(UP, 0.3))

        hist = VGroup(
            Tex(r"2007, Pan--Richter (computer): $\mathrm{cr}(K_{11})=100$, so $\mathrm{cr}(K_{12})=150$", font_size=32),
            Tex(r"Aichholzer (computer): $\mathrm{cr}(K_{13})=225$, so $\mathrm{cr}(K_{14})=315$", font_size=32),
            Tex(r"semidefinite programming: at least $0.83\times$ the formula, for large $n$", font_size=32),
            Tex(r"flag algebras (Balogh--Lidick\'y--Salazar): $> 0.9855\times$", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(UP * 0.4)
        bar0 = Rectangle(width=10, height=0.35, color=GREY_B).to_edge(DOWN, buff=0.9)
        b1 = Rectangle(width=8.3, height=0.35, stroke_width=0).set_fill(BLUE_3B, 0.8).align_to(bar0, LEFT).align_to(
            bar0, DOWN)
        b2 = Rectangle(width=9.855, height=0.35, stroke_width=0).set_fill(TEAL_3B, 0.8).align_to(bar0, LEFT).align_to(
            bar0, DOWN)
        bl = Tex(r"proved lower bound as a fraction of the conjectured value", font_size=26, color=GREY_A).next_to(
            bar0, DOWN, buff=0.15)
        with self.say(f"Lower bounds came slowly. Exact values were proved by computer: up to K twelve by Pan and "
                      f"Richter, then K thirteen and fourteen by {AICH}. {{a}}For large n, semidefinite programming "
                      "proved at least eighty-three percent of the formula, {b}and flag algebras pushed that past "
                      "ninety-eight and a half percent. But never all the way.") as s_:
            self.play(FadeIn(hist[0]))
            self.play(FadeIn(hist[1]))
            s_.wait_until("a")
            self.play(FadeIn(hist[2]), Create(bar0), FadeIn(bl), GrowFromEdge(b1, LEFT))
            s_.wait_until("b")
            self.play(FadeIn(hist[3]), ReplacementTransform(b1, b2))
        self.play(FadeOut(VGroup(hist, bar0, b2, bl, hh)))

        thm = VGroup(Tex(r"\textbf{Theorems.} For all $n$, and all $m,n$:", font_size=40),
                     MathTex(r"\mathrm{cr}(K_n)=\tfrac14\left\lfloor\tfrac n2\right\rfloor"
                             r"\left\lfloor\tfrac{n-1}2\right\rfloor\left\lfloor\tfrac{n-2}2\right\rfloor"
                             r"\left\lfloor\tfrac{n-3}2\right\rfloor", font_size=42),
                     MathTex(r"\mathrm{cr}(K_{m,n})=\left\lfloor\tfrac m2\right\rfloor\left\lfloor\tfrac{m-1}2\right"
                             r"\rfloor\left\lfloor\tfrac n2\right\rfloor\left\lfloor\tfrac{n-1}2\right\rfloor",
                             font_size=42),
                     Tex(r"the classical drawings are optimal among \emph{all} drawings with curved edges",
                         font_size=32, color=GREY_A)).arrange(DOWN, buff=0.3)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3))
        with self.say("Two manuscripts in OpenAI's math catalogue claim to finish the job. {t}The crossing number of "
                      "K n is exactly the Harary Hill formula, for every n, {b}and the crossing number of K m n is "
                      f"exactly {ZAR}'s formula, for all m and n. {{c}}No drawing, however curvy, beats the classical "
                      "ones.") as s_:
            s_.wait_until("t")
            self.play(FadeIn(tb[1]), FadeIn(thm[0]), Write(thm[1]), run_time=2)
            s_.wait_until("b")
            self.play(Write(thm[2]), run_time=2)
            s_.wait_until("c")
            self.play(FadeIn(thm[3]))
        self.play(FadeOut(tb))

        # ------------------------------------------------------------ signed crossings and the cycle identity
        hdr = Tex(r"Step 1: turn any drawing into linear algebra", font_size=38, color=YELLOW_3B).to_edge(UP, buff=0.3)
        cA, cB = LEFT * 4.6 + DOWN * 0.4, LEFT * 3.4 + DOWN * 0.4

        def fA(t):
            return cA + np.array([1.25 * np.cos(t), 1.25 * np.sin(t), 0])

        def fB(t):
            return cB + np.array([1.7 * np.cos(t), 0.75 * np.sin(t) + 0.25 * np.sin(3 * t), 0])

        crvA = ParametricFunction(fA, t_range=[0, TAU], color=BLUE_3B, stroke_width=4)
        crvB = ParametricFunction(fB, t_range=[0, TAU], color=ORANGE_3B, stroke_width=4)
        tt = np.linspace(0, TAU, 4000, endpoint=False)
        PA = np.array([fA(t) for t in tt])
        PB = np.array([fB(t) for t in tt])
        signs = VGroup()
        for i in range(len(tt)):
            a0, a1 = PA[i], PA[(i + 1) % len(tt)]
            dd = np.linalg.norm(PB - a0, axis=1)
            j = int(np.argmin(dd))
            if dd[j] < 0.004:
                ta, tb_ = a1 - a0, PB[(j + 1) % len(tt)] - PB[j]
                sg = np.sign(ta[0] * tb_[1] - ta[1] * tb_[0])
                if all(np.linalg.norm(a0 - m.get_center()) > 0.3 for m in signs):
                    signs.add(MathTex("+" if sg > 0 else "-", font_size=40, color=GREEN_3B if sg > 0 else RED_3B)
                              .move_to(a0 + 0.32 * normalize(a0 - (cA + cB) / 2)))
        tipA = Arrow(fA(0.8), fA(0.95), buff=0, color=BLUE_3B, max_tip_length_to_length_ratio=1)
        tipB = Arrow(fB(1.9), fB(2.05), buff=0, color=ORANGE_3B, max_tip_length_to_length_ratio=1)
        zl = Tex(r"two closed curves:\\ signed crossings sum to 0", font_size=30).next_to(VGroup(crvA, crvB), DOWN,
                                                                                         buff=0.3)
        M = D["M7"]
        cell = 0.17
        mat = VGroup()
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                c = {1: GREEN_3B, -1: RED_3B, 0: "#1c1c22"}[int(M[i, j])]
                mat.add(Square(cell, stroke_width=0.4, stroke_color=GREY_D).set_fill(c, 1).move_to(
                    np.array([j * cell, -i * cell, 0])))
        mat.move_to(RIGHT * 3.4 + UP * 0.35)
        ml = Tex(r"signed crossings $I(e,f)$ of the $K_7$ drawing\\ (21 edges $\times$ 21 edges)", font_size=28
                 ).next_to(mat, DOWN, buff=0.2)
        jf = MathTex(r"J(e,f)=I(e,f)+\tfrac12\!\!\sum_{\text{shared }w}\!\!\pm\,T_w(e,f)", font_size=34
                     ).next_to(ml, DOWN, buff=0.25)
        jz = Tex(r"$J(z,z')=0$ for every pair of cycles $z,z'$", font_size=30, color=YELLOW_3B).next_to(jf, DOWN,
                                                                                                      buff=0.2)
        with self.say("Lower bounds are hard because a drawing can be anything at all. The proof turns any drawing "
                      "into linear algebra. {s}Orient the edges, and give each crossing a sign, plus or minus, from "
                      "the orientations of the two strands. {z}Two closed curves in the plane always have signed "
                      "crossings summing to zero. {m}Record the signed crossings of every pair of edges in a matrix. "
                      "{j}Add a small correction at shared endpoints, recording the order in which edges leave each "
                      "vertex. The resulting form vanishes on every pair of cycles of the graph: a huge family of "
                      "linear identities that every drawing must obey.") as s_:
            self.play(Write(hdr))
            s_.wait_until("s")
            self.play(Create(crvA), Create(crvB), FadeIn(tipA), FadeIn(tipB), run_time=2)
            self.play(LaggedStart(*[FadeIn(x, scale=1.5) for x in signs], lag_ratio=0.3))
            s_.wait_until("z")
            self.play(FadeIn(zl))
            s_.wait_until("m")
            self.play(FadeIn(mat, lag_ratio=0.002), FadeIn(ml), run_time=2)
            s_.wait_until("j")
            self.play(Write(jf))
            self.play(FadeIn(jz))
        self.play(FadeOut(VGroup(hdr, crvA, crvB, tipA, tipB, signs, zl, mat, ml, jf, jz)))

        # ------------------------------------------------------------ dimension count
        hdr = Tex(r"Step 2: count crossings by counting dimensions ($n=2s+1$)", font_size=38, color=YELLOW_3B
                  ).to_edge(UP, buff=0.3)
        sp = VGroup(Tex(r"$S$ = polynomials $P(u_1,u_2;\,v_1,v_2)$ in the endpoints of two edges,", font_size=30),
                    Tex(r"symmetric within each edge, degree $\le s-2$ in each variable", font_size=30),
                    MathTex(r"\dim S=\binom{s}{2}^{2}", font_size=38)).arrange(DOWN, buff=0.18).next_to(hdr, DOWN,
                                                                                                    buff=0.3)
        rows = [("s", "n", r"\dim S", r"\text{formula}")] + [(str(k), str(2 * k + 1), str((k * (k - 1) // 2) ** 2),
                                                               str((k * (k - 1) // 2) ** 2)) for k in range(2, 6)]
        tab = VGroup(*[VGroup(*[MathTex(c, font_size=32) for c in r]).arrange(RIGHT, buff=0.1) for r in rows])
        for r in tab:
            for k, c in enumerate(r):
                c.move_to(np.array([1.25 * k, 0, 0]))
        tab.arrange(DOWN, buff=0.18).move_to(LEFT * 4.3 + DOWN * 1.5)
        for r in tab:
            for k, c in enumerate(r):
                c.set_x(-5.9 + 1.2 * k)
        tab[0].set_color(GREY_A)
        hl = Line(tab[0].get_corner(DL) + DOWN * 0.08 + LEFT * 0.2, tab[0].get_corner(DR) + DOWN * 0.08 + RIGHT * 0.2,
                  color=GREY_D)
        steps = VGroup(
            Tex(r"evaluate $P\in S$ at the pairs of edges that cross", font_size=30),
            Tex(r"cycle identity + Lagrange interpolation $\Rightarrow$ injective", font_size=30),
            Tex(r"image is totally isotropic $\Rightarrow$ dim $\le\frac12\#$coordinates", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 2.3 + DOWN * 0.75)
        chain = MathTex(r"\#\text{crossings}\ \ge\ \#\text{crossing pairs}\ \ge\ \dim S=\binom s2^{2}", font_size=38,
                        color=YELLOW_3B).to_edge(DOWN, buff=0.4).shift(RIGHT * 1.6)
        with self.say("Then comes a dimension count. For n equals two s plus one, take polynomials in four variables, "
                      "standing for the endpoints of two edges, symmetric within each edge, with degree at most s "
                      "minus two in each variable. {d}That space has dimension s choose two, squared, which is exactly "
                      "the conjectured crossing number. {e}Evaluate these polynomials at the pairs of edges that "
                      "cross. {i}Using the cycle identity and Lagrange interpolation, the paper shows this loses "
                      "nothing: the evaluation map is injective. {iso}A second use of the identity shows the image is "
                      "isotropic for a nondegenerate form, so its dimension is at most half the number of "
                      "coordinates, and each crossing pair supplies two. {c}So there must be at least as many crossing "
                      "pairs as the dimension. The even case follows by deleting a vertex, and for K m n, a "
                      "companion inequality about intersecting subspaces plays the same role.") as s_:
            self.play(Write(hdr))
            self.play(FadeIn(sp[:2]))
            s_.wait_until("d")
            self.play(Write(sp[2]))
            self.play(FadeIn(tab), Create(hl))
            s_.wait_until("e")
            self.play(FadeIn(steps[0]))
            s_.wait_until("i")
            self.play(FadeIn(steps[1]))
            s_.wait_until("iso")
            self.play(FadeIn(steps[2]))
            s_.wait_until("c")
            self.play(Write(chain), run_time=2)
        self.play(FadeOut(VGroup(hdr, sp, tab, hl, steps, chain)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Harary--Hill: $\mathrm{cr}(K_n)=\frac14\lfloor\frac n2\rfloor\lfloor\frac{n-1}2\rfloor"
             r"\lfloor\frac{n-2}2\rfloor\lfloor\frac{n-3}2\rfloor$ for every $n$",
             r"Zarankiewicz / Tur\'an's brickyard: $\mathrm{cr}(K_{m,n})=\lfloor\frac m2\rfloor"
             r"\lfloor\frac{m-1}2\rfloor\lfloor\frac n2\rfloor\lfloor\frac{n-1}2\rfloor$",
             r"Manuscripts: 13 and 16 pages, produced by an OpenAI model"],
            True, r"\emph{The crossing number of complete (bipartite) graphs} (Sept.\ 2026)")
        with self.say("Both manuscripts are short, thirteen and sixteen pages, written by an OpenAI model and not yet "
                      "peer reviewed. {l}Both formulas, lower bounds and matching drawings, counting every crossing "
                      "point, have been formalized in the Lean proof assistant.") as s_:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s_.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
