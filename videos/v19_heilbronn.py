from pathlib import Path

import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(Path(__file__).parent / "data" / "v19.npz")

HEIL = "[Heilbronn](/hˈIlbɹɑn/)"
ERD = "[Erdős](/ˈɛɹdəʃ/)"
KOM = "[Komlós](/kˈOmlOʃ/)"
PINTZ = "[Pintz](/pˈɪnts/)"
SZEM = "[Szemerédi](/sˈɛməɹˌAdi/)"
POHO = "[Pohoata](/pˌOhOˈɑtə/)"
ZAKH = "[Zakharov](/zˈɑkəɹˌɔf/)"


class Video(NarratedScene):
    def square_pts(self, P, center, side, color=WHITE, r=0.06):
        sq = Square(side, color=GREY_B, stroke_width=2).move_to(center)
        dots = VGroup(*[Dot(center + side * np.array([x - 0.5, y - 0.5, 0]), radius=r, color=color) for x, y in P])
        return sq, dots

    def construct(self):
        card = title_card(self, "191", "The Heilbronn Triangle Problem",
                          r"A power improvement in the lower bound")
        with self.say("Scatter n points in a square. How large can you make the smallest triangle they form?"):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.4)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ random points vs Erdos parabola
        side = 4.6
        cL, cR = LEFT * 3.4 + DOWN * 0.45, RIGHT * 3.4 + DOWN * 0.45
        R = D["rand"]
        sqL, dL = self.square_pts(R, cL, side)
        t = D["rand_tri"]
        triL = Polygon(*[dL[i].get_center() for i in t], color=RED_3B, stroke_width=3, fill_opacity=0.5)
        zoomL = Circle(radius=0.45, color=RED_3B).move_to(triL.get_center())
        labL = VGroup(Tex(r"17 random points", font_size=32),
                      MathTex(r"\text{smallest of } 680 \text{ triangles} \approx 0.00014", font_size=32, color=RED_3B)
                      ).arrange(DOWN, buff=0.15).next_to(sqL, UP, buff=0.25)
        p = int(D["p"][0])
        E = D["erd"]
        sqR, dR = self.square_pts(E, cR, side, color=YELLOW_3B)
        grid = VGroup(*[Line(cR + side * np.array([(k + 0.5) / p - 0.5, -0.5, 0]),
                             cR + side * np.array([(k + 0.5) / p - 0.5, 0.5, 0]), color=GREY_D, stroke_width=1)
                        for k in range(p)],
                      *[Line(cR + side * np.array([-0.5, (k + 0.5) / p - 0.5, 0]),
                             cR + side * np.array([0.5, (k + 0.5) / p - 0.5, 0]), color=GREY_D, stroke_width=1)
                        for k in range(p)])
        te = D["erd_tri"]
        triR = Polygon(*[dR[i].get_center() for i in te], color=YELLOW_3B, stroke_width=3, fill_opacity=0.35)
        labR = VGroup(MathTex(r"(x,\ x^2 \bmod 17)", font_size=34),
                      MathTex(r"\text{smallest triangle}=\tfrac{1}{2\cdot17^2}\approx0.0017", font_size=32,
                              color=YELLOW_3B)).arrange(DOWN, buff=0.15).next_to(sqR, UP, buff=0.25)
        why = Tex(r"no three on a line; lattice triangles have area $\ge\frac12$", font_size=28, color=GREY_A
                  ).next_to(sqR, DOWN, buff=0.15)
        with self.say("Random points do badly. {r}Among these seventeen, some three nearly line up: the smallest of "
                      f"the six hundred and eighty triangles has area barely more than one ten-thousandth. {{e}}{ERD} found a "
                      "cleverer arrangement. On a seventeen by seventeen grid, take the points x, x squared, reduced "
                      "modulo seventeen. {c}No three lie on a line, because a line meets a parabola at most twice, "
                      "even modulo a prime. And three grid points not on a line always span area at least one half. "
                      "{s}Shrink into the unit square, and every triangle has area at least one over two p squared: "
                      "order one over n squared.") as s:
            self.play(Create(sqL), LaggedStart(*[GrowFromCenter(d) for d in dL], lag_ratio=0.05), run_time=1.5)
            s.wait_until("r")
            self.play(FadeIn(labL), FadeIn(triL), Create(zoomL))
            s.wait_until("e")
            self.play(Create(sqR), Create(grid), LaggedStart(*[GrowFromCenter(d) for d in dR], lag_ratio=0.05),
                      FadeIn(labR[0]), run_time=2)
            s.wait_until("c")
            self.play(FadeIn(why))
            s.wait_until("s")
            self.play(FadeIn(triR), FadeIn(labR[1]))
        self.play(FadeOut(VGroup(sqL, dL, triL, zoomL, labL, sqR, dR, grid, triR, labR, why)))

        # ------------------------------------------------------------ the problem and its history
        dd = MathTex(r"\Delta(n)=\max_{n\text{ points}}\ \min_{\text{triangles}}\ \text{area}", font_size=44
                     ).to_edge(UP, buff=0.4)
        nl = NumberLine(x_range=[-2, -1, 0.25], length=11.5, include_numbers=False, color=GREY_B).shift(DOWN * 0.5)
        ends = VGroup(MathTex(r"n^{-2}", font_size=34).next_to(nl.n2p(-2), DOWN, buff=0.25),
                      MathTex(r"n^{-1}", font_size=34).next_to(nl.n2p(-1), DOWN, buff=0.25))
        lab_lo = Tex(r"lower bounds (constructions)", font_size=28, color=BLUE_3B).next_to(nl.n2p(-2), UP,
                                                                                       buff=2.4).shift(RIGHT * 1.9)
        lab_up = Tex(r"upper bounds (impossibility)", font_size=28, color=ORANGE_3B).next_to(nl.n2p(-1), UP,
                                                                                         buff=2.4).shift(LEFT * 1.9)
        lo1 = VGroup(Dot(nl.n2p(-2), color=BLUE_3B),
                     Tex(r"Erd\H{o}s: $n^{-2}$;\\ 1982, KPS: $\frac{\log n}{n^2}$", font_size=28, color=BLUE_3B
                         ).next_to(nl.n2p(-2), UP, buff=0.3).shift(RIGHT * 0.5))
        ups = VGroup()
        for v, txt in [(-1.0, r"1951, Roth:\\ $o(n^{-1})$"), (-8 / 7, r"KPS:\\ $n^{-8/7+\varepsilon}$"),
                       (-7 / 6, r"Cohen--Pohoata--\\Zakharov: $n^{-7/6+\varepsilon}$")]:
            ups.add(VGroup(Dot(nl.n2p(v), color=ORANGE_3B),
                           Tex(txt, font_size=26, color=ORANGE_3B).next_to(nl.n2p(v), UP, buff=0.3)))
        ups[0][1].shift(LEFT * 0.3)
        ups[1][1].next_to(nl.n2p(-8 / 7), UP, buff=1.35)
        ups[2][1].shift(LEFT * 1.5)
        conj = Tex(r"conjecture: $\Delta(n)\le C_\varepsilon\, n^{-2+\varepsilon}$ for every $\varepsilon>0$",
                   font_size=34, color=RED_3B).to_edge(DOWN, buff=0.45)
        with self.say(f"This is {HEIL}'s triangle problem: delta of n is the best possible smallest area. {{c}}The "
                      f"original conjecture was that delta of n is at most a constant over n squared, matching "
                      f"{ERD}'s parabola. {{k}}In 1982, {KOM}, {PINTZ} and {SZEM} disproved it, gaining a factor of "
                      f"log n with a random construction. {{u}}From above, Roth proved the first bound better than one "
                      f"over n, in 1951. Later work reached n to the minus eight sevenths, and Cohen, {POHO} and "
                      f"{ZAKH} pushed it to n to the minus seven sixths. {{a}}But the lower bound stayed stuck at "
                      "exponent minus two, and it was conjectured that the truth is n to the minus two, up to factors "
                      "smaller than any power of n.") as s:
            self.play(Write(dd), Create(nl), FadeIn(ends))
            s.wait_until("c")
            self.play(FadeIn(lo1[0]), FadeIn(lab_lo))
            s.wait_until("k")
            self.play(FadeIn(lo1[1]))
            s.wait_until("u")
            self.play(FadeIn(lab_up), FadeIn(ups[0]))
            self.play(FadeIn(ups[1]))
            self.play(FadeIn(ups[2]))
            s.wait_until("a")
            self.play(FadeIn(conj))
        new_arr = Arrow(nl.n2p(-1.82) + DOWN * 1.15, nl.n2p(-1.94) + DOWN * 0.12, buff=0, color=YELLOW_3B)
        new = VGroup(new_arr, MathTex(r"n^{-2+\eta}\ \text{(not to scale)}", font_size=34, color=YELLOW_3B)
                     .next_to(new_arr.get_start(), RIGHT, buff=0.15))

        thm = VGroup(Tex(r"\textbf{Theorem.} There are absolute constants $\eta, c>0$ such that for", font_size=38),
                     Tex(r"every large $n$, some $n$ points in the unit square have", font_size=38),
                     Tex(r"every triangle of area at least $c\,n^{-2+\eta}$.", font_size=38)).arrange(DOWN, buff=0.2)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3)).to_edge(UP, buff=0.3)
        eta = Tex(r"$\eta$ is fixed but tiny: the paper's explicit value is about $10^{-235}$", font_size=30,
                  color=GREY_A).next_to(conj, UP, buff=0.25)
        with self.say("A manuscript in OpenAI's math catalogue claims that this conjecture is false. "
                      "{t}There are absolute constants eta and c such that, for every large n, you can place n points "
                      "with every triangle of area at least c times n to the minus two plus eta. {x}A power of n "
                      "better than the old constructions. {e}The exponent eta is fixed but extremely small: the "
                      "explicit value in the paper is around ten to the minus two hundred thirty-five.") as s:
            self.play(FadeOut(dd), FadeOut(lab_up), FadeOut(ups), FadeOut(lab_lo))
            s.wait_until("t")
            self.play(Write(tb), run_time=2.5)
            s.wait_until("x")
            self.play(GrowArrow(new[0]), FadeIn(new[1]), conj.animate.set_opacity(0.4))
            self.play(Create(Line(conj.get_left(), conj.get_right(), color=RED_3B, stroke_width=4)))
            s.wait_until("e")
            self.play(FadeIn(eta))
        self.play(FadeOut(Group(*self.mobjects)))

        # ------------------------------------------------------------ points as columns: area = det
        hdr = Tex(r"Points as integer columns: area is a determinant", font_size=38, color=YELLOW_3B).to_edge(
            UP, buff=0.35)
        col = MathTex(r"u=\begin{pmatrix}u_1\\u_2\\u_3\end{pmatrix}\ \mapsto\ \Big(\frac{u_1}{u_3},\frac{u_2}{u_3}\Big)",
                      r",\quad N\le u_3<2N", font_size=40).next_to(hdr, DOWN, buff=0.45)
        area = MathTex(r"\text{Area}=\frac{|\det A|}{2\,A_{31}A_{32}A_{33}}", r"\ \ge\ \frac{|\det A|}{16N^3}",
                       font_size=46).next_to(col, DOWN, buff=0.5)
        area[1].set_color(TEAL_3B)
        goal = Tex(r"Goal: many columns whose $3\times3$ determinants are never small", font_size=34).next_to(
            area, DOWN, buff=0.55)
        with self.say("How does the construction work? {c}Represent each point by a column of three integers, u one, "
                      "u two, u three, where u three is between N and two N: the point is u one over u three, u two "
                      "over u three. {a}Then the area of a triangle is the determinant of the three columns, divided "
                      "by twice the product of their third coordinates, which is at most eight N cubed. {g}So the "
                      "goal is a large set of columns whose three by three determinants are never small.") as s:
            self.play(Write(hdr))
            s.wait_until("c")
            self.play(Write(col), run_time=2)
            s.wait_until("a")
            self.play(Write(area[0]), run_time=2)
            self.play(FadeIn(area[1]))
            s.wait_until("g")
            self.play(FadeIn(goal))
        self.play(FadeOut(VGroup(hdr, col, area, goal)))

        # ------------------------------------------------------------ two congruence conditions
        hdr = Tex(r"Two congruence conditions", font_size=38, color=YELLOW_3B).to_edge(UP, buff=0.35)
        vd = MathTex(r"\det\begin{pmatrix}1&1&1\\ \xi_1&\xi_2&\xi_3\\ \xi_1^2&\xi_2^2&\xi_3^2\end{pmatrix}"
                     r"=(\xi_2-\xi_1)(\xi_3-\xi_1)(\xi_3-\xi_2)", font_size=38).next_to(hdr, DOWN, buff=0.35)
        vdl = Tex(r"labels $\xi$ in a finite field: nonzero when the labels are distinct", font_size=30,
                  color=GREY_A).next_to(vd, DOWN, buff=0.2)
        B = 0.55
        digits = VGroup(*[Square(B, color=GREY_B, stroke_width=2) for _ in range(9)]).arrange(LEFT, buff=0)
        digits.next_to(vdl, DOWN, buff=0.55).shift(LEFT * 2.2)
        dl = VGroup(*[MathTex(s_, font_size=26).move_to(sq) for s_, sq in
                      zip([r"d_0", r"d_1", r"\cdots", r"d_j", r"\cdots", "", "", "", ""], digits)])
        digits[3].set_fill(YELLOW_3B, 0.5)
        dlab = Tex(r"the field norm of that determinant\\ is planted in one base-$B$ digit", font_size=28
                   ).next_to(digits, RIGHT, buff=0.4)
        c1 = Tex(r"$\bmod\ h=B^k$: distinct labels $\Rightarrow$ $\det A$ has no small representative", font_size=30
                 ).next_to(digits, DOWN, buff=0.4).set_x(0)
        c2 = Tex(r"$\bmod\ q$: points on a quadric with no three on a line $\Rightarrow$ controls $\det A=0$",
                 font_size=30).next_to(c1, DOWN, buff=0.25)
        c3 = Tex(r"glued by the Chinese remainder theorem; mixed by a random det-1 matrix", font_size=30,
                 color=GREY_A).next_to(c2, DOWN, buff=0.25)
        with self.say(f"The key idea revives {ERD}'s parabola. {{v}}Give each column a random label, [xi](/ksˈI/), from a large "
                      "finite field. The columns one, [xi](/ksˈI/), [xi](/ksˈI/) squared have a [Vandermonde](/vˈændəɹmˌɑnd/) determinant, which is nonzero "
                      "whenever the three labels are distinct. {d}The paper takes the field norm of this determinant, "
                      "writes it as a sum of simpler determinants, and plants it in one designated digit of a "
                      "base B expansion. {m}Then, modulo B to the k, three distinct labels force the determinant to "
                      "have no small integer representative. {z}A second condition, modulo another prime, uses points "
                      "on a quadratic surface with no three on a line, to control triples with determinant exactly "
                      "zero. {cr}The Chinese remainder theorem glues the two conditions together, and a random matrix "
                      "of determinant one mixes things up without changing any determinant.") as s:
            self.play(Write(hdr))
            s.wait_until("v")
            self.play(Write(vd), run_time=2)
            self.play(FadeIn(vdl))
            s.wait_until("d")
            self.play(FadeIn(digits), FadeIn(dl), FadeIn(dlab))
            s.wait_until("m")
            self.play(FadeIn(c1))
            s.wait_until("z")
            self.play(FadeIn(c2))
            s.wait_until("cr")
            self.play(FadeIn(c3))
        self.play(FadeOut(VGroup(hdr, vd, vdl, digits, dl, dlab, c1, c2, c3)))

        # ------------------------------------------------------------ deletion
        hdr = Tex(r"Then delete: one point from each bad triple", font_size=38, color=YELLOW_3B).to_edge(UP, buff=0.35)
        S = D["del_S"]
        c0 = LEFT * 3.3 + DOWN * 0.45
        sqD, dD = self.square_pts(S, c0, 5.2, color=GREY_A, r=0.07)
        bad = VGroup(*[Polygon(*[dD[i].get_center() for i in t], color=RED_3B, stroke_width=2, fill_opacity=0.35)
                       for t in D["del_bad"]])
        rm = [int(i) for i in D["del_rm"]]
        txt = VGroup(
            Tex(r"Classical: random points, delete one\\ point from each small triangle $\Rightarrow n^{-2}$",
                font_size=30),
            Tex(r"New: in the arithmetic construction,\\ a small determinant needs a\\ \emph{repeated label}",
                font_size=30),
            Tex(r"repeated labels are rare, so few\\ deletions leave $n$ points with", font_size=30),
            MathTex(r"\text{every triangle}\ \ge\ c\,n^{-2+\eta}", font_size=36, color=YELLOW_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.3 + DOWN * 0.3)
        with self.say(f"The last step is an old trick. {{c}}With purely random points, you can delete one point from "
                      "each small triangle, and what is left has smallest area of order one over n squared. "
                      "{n}In the new construction, a small determinant can only come from columns whose labels "
                      "repeat. {r}Repeated labels are rare, so only a few deletions are needed, and the surviving n "
                      "points have every triangle of area at least c n to the minus two plus eta.") as s:
            self.play(Write(hdr), Create(sqD), FadeIn(dD))
            s.wait_until("c")
            self.play(FadeIn(txt[0]), LaggedStart(*[FadeIn(b) for b in bad], lag_ratio=0.05), run_time=2)
            self.play(*[dD[i].animate.set_color(RED_3B).scale(1.4) for i in rm])
            self.play(FadeOut(bad), *[FadeOut(dD[i]) for i in rm])
            s.wait_until("n")
            self.play(FadeIn(txt[1]))
            s.wait_until("r")
            self.play(FadeIn(txt[2]), FadeIn(txt[3]))
        self.play(FadeOut(Group(*self.mobjects)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"$\Delta(n)\ge c\,n^{-2+\eta}$ for all large $n$: the almost-$n^{-2}$ bound is false",
             r"Lean: verified for infinitely many $n$, which refutes the almost-$n^{-2}$ bound",
             r"Manuscript: 24 pages, produced by an OpenAI model"],
            False, r"\emph{A power improvement in the Heilbronn triangle lower bound} (Sept.\ 2026)")
        with self.say("The manuscript is twenty-four pages, written by an OpenAI model and not yet peer reviewed. "
                      "{l}The Lean formalization verifies the construction for infinitely many values of n, which "
                      "already refutes the n to the minus two plus epsilon conjecture. The paper's full statement, "
                      "for every sufficiently large n, is broader than what has been formalized.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
