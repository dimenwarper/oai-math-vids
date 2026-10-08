import numpy as np
from manim import *

from style import *
from vo import NarratedScene

HIST = [(1969, 2.8074, "Strassen"), (1978, 2.796, ""), (1979, 2.780, ""), (1981, 2.522, ""),
        (1981.5, 2.496, ""), (1986, 2.479, ""), (1990, 2.3755, "Coppersmith--Winograd"), (2010, 2.3737, ""),
        (2012, 2.3729, ""), (2014, 2.37286, ""), (2020, 2.37286, ""), (2022, 2.37187, ""), (2023, 2.37155, ""),
        (2024, 2.37134, ""), (2026, 2.37118, "")]


def mat(entries, color=WHITE, fs=36):
    return Matrix(entries, element_to_mobject=lambda e: MathTex(e, font_size=fs, color=color),
                  h_buff=0.9, v_buff=0.7)


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "107", r"Matrix Multiplication: $\omega \le 9/4$",
                          r"Two $n\times n$ matrices in $O(n^{2.25+\varepsilon})$ operations")
        with self.say("Multiplying matrices, faster."):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ naive n^3
        A = mat([["a_{11}", "a_{12}", "a_{13}"], ["a_{21}", "a_{22}", "a_{23}"], ["a_{31}", "a_{32}", "a_{33}"]],
                BLUE_3B)
        B = mat([["b_{11}", "b_{12}", "b_{13}"], ["b_{21}", "b_{22}", "b_{23}"], ["b_{31}", "b_{32}", "b_{33}"]],
                YELLOW_3B)
        C = mat([["c_{11}", "\\cdot", "\\cdot"], ["\\cdot", "\\cdot", "\\cdot"], ["\\cdot", "\\cdot", "\\cdot"]])
        times, eq = MathTex(r"\times"), MathTex("=")
        prod = VGroup(A, times, B, eq, C).arrange(RIGHT, buff=0.3).shift(UP * 0.8)
        row = SurroundingRectangle(A.get_rows()[0], color=BLUE_3B, buff=0.1)
        col = SurroundingRectangle(B.get_columns()[0], color=YELLOW_3B, buff=0.1)
        form = MathTex(r"c_{11}", "=", r"a_{11}b_{11}", "+", r"a_{12}b_{21}", "+", r"a_{13}b_{31}",
                       font_size=40).next_to(prod, DOWN, buff=0.6)
        count = MathTex(r"n \text{ multiplications per entry} \times n^2 \text{ entries} = n^3",
                        font_size=40, color=RED_3B).next_to(form, DOWN, buff=0.4)
        with self.say("To multiply two matrices the way we learn in school, each entry of the answer "
                      "is a row times a column: {rc}n multiplications, added up. "
                      "{n3}There are n squared entries, so that is n cubed multiplications in all. "
                      "{gpu}Every neural network and every physics simulation runs on this operation, "
                      "so the exponent, that three, matters enormously.") as s:
            self.play(FadeIn(prod), run_time=1.5)
            s.wait_until("rc")
            self.play(Create(row), Create(col))
            self.play(Write(form), run_time=2)
            s.wait_until("n3")
            self.play(Write(count))
            s.wait_until("gpu")
            self.play(Indicate(count[0][-2:], color=RED_3B, scale_factor=1.6))
        self.play(FadeOut(VGroup(prod, row, col, form, count)))

        # ------------------------------------------------------------ Strassen
        naive = VGroup(*[MathTex(t, font_size=32) for t in [
            r"A_{11}B_{11}", r"A_{12}B_{21}", r"A_{11}B_{12}", r"A_{12}B_{22}",
            r"A_{21}B_{11}", r"A_{22}B_{21}", r"A_{21}B_{12}", r"A_{22}B_{22}"]]).arrange_in_grid(4, 2, buff=(0.6, 0.3))
        naive_t = Tex(r"block formula: \textbf{8} products", font_size=34).next_to(naive, UP, buff=0.4)
        nv = VGroup(naive_t, naive).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        st = VGroup(*[MathTex(t, font_size=28) for t in [
            r"M_1=(A_{11}+A_{22})(B_{11}+B_{22})", r"M_2=(A_{21}+A_{22})B_{11}", r"M_3=A_{11}(B_{12}-B_{22})",
            r"M_4=A_{22}(B_{21}-B_{11})", r"M_5=(A_{11}+A_{12})B_{22}", r"M_6=(A_{21}-A_{11})(B_{11}+B_{12})",
            r"M_7=(A_{12}-A_{22})(B_{21}+B_{22})"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.17)
        st_t = Tex(r"Strassen (1969): \textbf{7} products", font_size=34, color=YELLOW_3B).next_to(st, UP, buff=0.4)
        sv = VGroup(st_t, st).to_edge(RIGHT, buff=0.7).shift(DOWN * 0.2)
        rec = MathTex(r"7^{\log_2 n} = n^{\log_2 7}\approx n^{2.807}", font_size=42, color=YELLOW_3B).to_edge(
            DOWN, buff=0.35)
        with self.say("In 1969, Volker [Strassen](/ʃtɹˈɑsən/) shocked everyone. Split each matrix into four blocks. "
                      "{n8}The obvious formula needs eight block products. "
                      "{s7}Strassen found a way with only seven, at the cost of some extra additions. "
                      "{rec}Apply the trick recursively, and the cost drops from n cubed "
                      "to n to the two point eight one.") as s:
            s.wait_until("n8")
            self.play(FadeIn(naive_t), LaggedStart(*[FadeIn(m) for m in naive], lag_ratio=0.1), run_time=1.5)
            s.wait_until("s7")
            self.play(FadeIn(st_t), LaggedStart(*[Write(m) for m in st], lag_ratio=0.15), run_time=3)
            s.wait_until("rec")
            self.play(Write(rec))
        self.play(FadeOut(VGroup(nv, sv, rec)))

        # ------------------------------------------------------------ history plot
        ax = Axes(x_range=[1965, 2030, 10], y_range=[2.0, 3.0, 0.2], x_length=10.5, y_length=5.4, tips=False,
                  axis_config={"color": GREY_B, "font_size": 24},
                  x_axis_config={"numbers_to_include": [1970, 1980, 1990, 2000, 2010, 2020],
                                 "decimal_number_config": {"group_with_commas": False, "num_decimal_places": 0}},
                  y_axis_config={"numbers_to_include": [2.0, 2.2, 2.4, 2.6, 2.8, 3.0],
                                 "decimal_number_config": {"num_decimal_places": 1}}).shift(DOWN * 0.3)
        omega_l = MathTex(r"\omega", font_size=44).next_to(ax.y_axis, UP, buff=0.15)
        two = DashedLine(ax.c2p(1965, 2), ax.c2p(2030, 2), color=GREEN_3B)
        two_l = Tex(r"$\omega\ge 2$: you must at least read the input", font_size=28, color=GREEN_3B).next_to(
            ax.c2p(1995, 2), UP, buff=0.1)
        pts = [ax.c2p(1965, 3.0)] + [ax.c2p(y, w) for y, w, _ in HIST]
        stair = VMobject(color=BLUE_3B, stroke_width=4)
        corners = [pts[0]]
        for p in pts[1:]:
            corners += [np.array([p[0], corners[-1][1], 0]), p]
        corners.append(np.array([ax.c2p(2026.4, 0)[0], corners[-1][1], 0]))
        stair.set_points_as_corners(corners)
        dots = VGroup(*[Dot(p, radius=0.05, color=BLUE_3B) for p in pts[1:]])
        cw = Tex("1990: 2.3755", font_size=28, color=BLUE_3B).next_to(ax.c2p(1990, 2.3755), DR, buff=0.12)
        sl = Tex("1969: 2.807", font_size=28, color=BLUE_3B).next_to(ax.c2p(1969, 2.8074), UR, buff=0.1)
        zoom = VGroup(Tex(r"1990--2026:", font_size=28),
                      MathTex(r"2.3755\ \to\ 2.37118", font_size=34, color=BLUE_3B)).arrange(DOWN, buff=0.12)
        zoom.next_to(ax.c2p(2008, 2.6), UP, buff=0)
        with self.say("The best exponent is called omega. {plot}The bound fell quickly at first, "
                      "through the nineteen seventies and eighties. "
                      "{cw}In 1990, [Coppersmith](/kˈɑpəɹsmɪθ/) and Winograd reached two point three seven five five. "
                      "{crawl}Then it crawled. Over the next thirty-five years, a string of papers moved it only in the third decimal place, "
                      "to two point three seven one one eight in 2026. "
                      "{two}The only lower bound is two, because you have to at least look at all the entries.") as s:
            s.wait_until("plot")
            self.play(Create(ax), FadeIn(omega_l), run_time=1.2)
            self.play(Create(stair), FadeIn(dots), FadeIn(sl), run_time=4, rate_func=linear)
            s.wait_until("cw")
            self.play(FadeIn(cw), Flash(dots[6], color=BLUE_3B))
            s.wait_until("crawl")
            self.play(FadeIn(zoom, shift=DOWN * 0.2), run_time=1.5)
            s.wait_until("two")
            self.play(Create(two), FadeIn(two_l), run_time=1.5)

        drop = Line(ax.c2p(2026.4, 2.37118), ax.c2p(2026.4, 2.25), color=YELLOW_3B, stroke_width=5)
        new = Dot(ax.c2p(2026.4, 2.25), radius=0.09, color=YELLOW_3B)
        new_l = MathTex(r"\omega\le\tfrac94=2.25", font_size=42, color=YELLOW_3B).next_to(new, LEFT, buff=0.3)
        with self.say("A new manuscript in OpenAI's math catalogue claims a jump not in the third decimal, "
                      "but the first: {nine}omega is at most nine fourths. "
                      "{alg}For every epsilon, two n by n matrices can be multiplied with about "
                      "n to the two point two five plus epsilon operations. "
                      "{gal}This is an asymptotic statement. The algorithm only wins for astronomically large matrices, "
                      "so do not expect it in your graphics card.") as s:
            s.wait_until("nine")
            self.play(Create(drop), FadeIn(new, scale=2), run_time=1.5)
            self.play(Write(new_l))
            s.wait_until("alg")
            alg = MathTex(r"O_\varepsilon\!\left(n^{9/4+\varepsilon}\right)\ \text{operations}", font_size=40,
                          color=YELLOW_3B).to_corner(UR, buff=0.4)
            self.play(Write(alg))
            s.wait_until("gal")
            gal = Tex(r"asymptotic: a ``galactic'' algorithm", font_size=30, color=GREY_A).next_to(alg, DOWN)
            self.play(FadeIn(gal))
        self.play(FadeOut(Group(*self.mobjects)))

        # ------------------------------------------------------------ tensors and measuring sticks
        tn = MathTex(r"T_n", "=", r"\sum_{i,j,k}", r"x_{ij}", r"y_{jk}", r"z_{ki}", font_size=50).to_edge(UP, buff=0.5)
        legs = VGroup(Tex(r"$x$-leg", color=BLUE_3B, font_size=32), Tex(r"$y$-leg", color=YELLOW_3B, font_size=32),
                      Tex(r"$z$-leg", color=TEAL_3B, font_size=32)).arrange(RIGHT, buff=1.2).next_to(tn, DOWN,
                                                                                                 buff=0.3)
        rules = VGroup(
            Tex(r"A \textbf{character} $\lambda$ is a measuring stick for tensors:", font_size=34),
            MathTex(r"\lambda(A\oplus B)=\lambda(A)+\lambda(B)", font_size=36),
            MathTex(r"\lambda(A\otimes B)=\lambda(A)\,\lambda(B)", font_size=36),
            Tex(r"never grows when you specialize a tensor", font_size=32),
        ).arrange(DOWN, buff=0.25).shift(DOWN * 0.5)
        key = MathTex(r"\lambda(T_n)=n^{3t}", r"\qquad\Rightarrow\qquad", r"\text{show } t\le\tfrac34",
                      r"\text{ for every }\lambda", font_size=40, color=YELLOW_3B).to_edge(DOWN, buff=0.5)
        with self.say("How could a thirteen-page argument do this? It works in Strassen's own language. "
                      "{t}Matrix multiplication is a tensor: a sum of products of three groups of variables, "
                      "called its legs. {ch}Strassen showed that the exponent is governed by measuring sticks "
                      "for tensors, called characters. They add over direct sums, multiply over tensor products, "
                      "and never grow when you specialize. "
                      "{k}On n by n matrix multiplication, every character reads n to the three t, for some t. "
                      "So it is enough to show that t is at most three quarters, for every character.") as s:
            s.wait_until("t")
            self.play(Write(tn), run_time=2)
            self.play(FadeIn(legs))
            self.play(tn[3].animate.set_color(BLUE_3B), tn[4].animate.set_color(YELLOW_3B),
                      tn[5].animate.set_color(TEAL_3B))
            s.wait_until("ch")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.15) for r in rules], lag_ratio=0.5), run_time=4)
            s.wait_until("k")
            self.play(Write(key), run_time=2.5)
        self.play(FadeOut(VGroup(tn, legs, rules, key)))

        # ------------------------------------------------------------ polynomial multiplication
        a_n, b_n = 3, 4
        cs = 0.7
        cells = VGroup()
        ccol = [BLUE_3B, TEAL_3B, GREEN_3B, YELLOW_3B, ORANGE_3B, RED_3B]
        for i in range(a_n):
            for j in range(b_n):
                sq = Square(cs, stroke_color=GREY_B, stroke_width=2).set_fill(ccol[i + j], 0.45)
                sq.move_to(np.array([j * cs, -i * cs, 0]))
                lab = MathTex(f"p_{i}q_{j}", font_size=24).move_to(sq)
                cells.add(VGroup(sq, lab))
        cells.move_to(LEFT * 2.6 + DOWN * 0.2)
        pl = MathTex(r"(p_0+p_1x+p_2x^2)", font_size=34, color=BLUE_3B)
        ql = MathTex(r"(q_0+q_1x+q_2x^2+q_3x^3)", font_size=34, color=YELLOW_3B)
        pq = VGroup(pl, MathTex(r"\times", font_size=34), ql).arrange(RIGHT, buff=0.2).to_edge(UP, buff=0.5)
        outs = VGroup(*[MathTex(f"c_{k}", font_size=34, color=ccol[k]) for k in range(6)]).arrange(DOWN, buff=0.22)
        outs.next_to(cells, RIGHT, buff=1.4)
        brace_t = Tex(r"$a$ and $b$ coefficients in,\\ $a+b-1$ out", font_size=30).next_to(outs, RIGHT, buff=0.6)
        with self.say("The surprise is that the proof barely looks at matrices. It studies a humbler operation: "
                      "{pm}multiplying polynomials. A polynomial with a coefficients times one with b coefficients "
                      "gives one with a plus b minus one coefficients, {diag}each a sum along a diagonal "
                      "of this table of products. "
                      "{prof}For each character, the proof defines a profile, P of a and b, "
                      "measuring how big this polynomial multiplication looks.") as s:
            s.wait_until("pm")
            self.play(Write(pq), run_time=2)
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.05), run_time=1.5)
            s.wait_until("diag")
            for k in range(6):
                grp = VGroup(*[cells[i * b_n + j] for i in range(a_n) for j in range(b_n) if i + j == k])
                self.play(Indicate(grp, color=ccol[k], scale_factor=1.08), FadeIn(outs[k]), run_time=0.45)
            self.play(FadeIn(brace_t))
            s.wait_until("prof")
            prof = MathTex(r"P(a,b)", font_size=48, color=YELLOW_3B).to_edge(DOWN, buff=0.5)
            self.play(Write(prof))
        self.play(FadeOut(VGroup(pq, cells, outs, brace_t, prof)))

        # ------------------------------------------------------------ ceiling & floor
        ceil_t = Tex(r"\textbf{Ceiling} (interpolation)", font_size=36, color=RED_3B)
        ceil_f = MathTex(r"P(a,b)\le(a+b-1)^{1/t}", font_size=40, color=RED_3B)
        ceil_n = Tex(r"evaluate at $a+b-1$ points, multiply, interpolate back", font_size=28, color=GREY_A)
        ceil = VGroup(ceil_t, ceil_f, ceil_n).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.4)
        floor_t = Tex(r"\textbf{Floor} (two new constructions)", font_size=36, color=GREEN_3B)
        f1 = MathTex(r"2P(a,b)\ \ge\ P(a,b+1)+P(a,b-1)", font_size=36, color=GREEN_3B)
        f1n = Tex(r"a determinant filtration", font_size=26, color=GREY_A)
        f2 = MathTex(r"P(a,\,3h+a-1)\ \ge\ 3\,P(a,h)", font_size=36, color=GREEN_3B)
        f2n = Tex(r"three sectors, pulled apart", font_size=26, color=GREY_A)
        f3 = MathTex(r"\Longrightarrow\quad P(a,a)\ \ge\ a^{4/3}", font_size=42, color=GREEN_3B)
        floor = VGroup(floor_t, VGroup(f1, f1n).arrange(DOWN, buff=0.08), VGroup(f2, f2n).arrange(DOWN, buff=0.08),
                       f3).arrange(DOWN, buff=0.3).next_to(ceil, DOWN, buff=0.6)
        with self.say("Now the profile gets squeezed. {c}From above, by an old idea: evaluate both polynomials "
                      "at enough points, multiply the values, and interpolate back. "
                      "That caps P at a plus b minus one, to the power one over t. "
                      "{f}From below, by two new constructions. The key one takes pieces of a tensor that share "
                      "one of their three legs, and pulls them fully apart. "
                      "{ff}Together they show the profile is concave, and that it at least triples when you "
                      "roughly triple an input. {g}Those two facts force the diagonal values to grow "
                      "at least like a to the four thirds.") as s:
            s.wait_until("c")
            self.play(FadeIn(ceil_t), Write(ceil_f), run_time=2)
            self.play(FadeIn(ceil_n))
            s.wait_until("f")
            self.play(FadeIn(floor_t))
            s.wait_until("ff")
            self.play(FadeIn(floor[1]), run_time=1.2)
            self.play(FadeIn(floor[2]), run_time=1.2)
            s.wait_until("g")
            self.play(Write(f3), run_time=2)
        self.play(FadeOut(VGroup(ceil, floor)))

        # ------------------------------------------------------------ the separation trick
        hdr = Tex("The separation trick", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.4)
        shared = Rectangle(width=6, height=0.5, color=BLUE_3B, fill_opacity=0.3).shift(UP * 1.3 + LEFT * 2.6)
        sh_l = Tex(r"shared $x$-leg", font_size=28, color=BLUE_3B).next_to(shared, UP, buff=0.1)
        blocks = VGroup(*[RoundedRectangle(width=1.5, height=1.1, corner_radius=0.1, color=c, fill_opacity=0.3)
                          for c in [YELLOW_3B, TEAL_3B, RED_3B]]).arrange(RIGHT, buff=0.5).next_to(shared, DOWN,
                                                                                                    buff=0.6)
        blabs = VGroup(*[MathTex(f"A_{h}", font_size=34).move_to(b) for h, b in zip([1, 2, 3], blocks)])
        links = VGroup(*[Line(shared.get_bottom() + RIGHT * (b.get_x() - shared.get_x()), b.get_top(),
                              color=BLUE_3B) for b in blocks])
        ax2 = Axes(x_range=[-3, 3, 1], y_range=[0, 9, 3], x_length=4, y_length=2.8, tips=False,
                   axis_config={"color": GREY_B}).shift(RIGHT * 3.8 + UP * 0.6)
        par = ax2.plot(lambda u: u * u, x_range=[-3, 3], color=YELLOW_3B)
        par_l = MathTex(r"\text{weight}=(g-h)^2", font_size=32, color=YELLOW_3B).next_to(ax2, UP, buff=0.15)
        g_l = MathTex(r"g-h", font_size=28).next_to(ax2.x_axis, DOWN, buff=0.1)
        zero = Dot(ax2.c2p(0, 0), color=GREEN_3B, radius=0.09)
        sep = VGroup(*[VGroup(Rectangle(width=1.5, height=0.35, color=BLUE_3B, fill_opacity=0.3),
                              RoundedRectangle(width=1.5, height=1.1, corner_radius=0.1, color=c, fill_opacity=0.3))
                       .arrange(DOWN, buff=0.3) for c in [YELLOW_3B, TEAL_3B, RED_3B]]).arrange(RIGHT, buff=0.5)
        sep.move_to(LEFT * 2.6 + DOWN * 2.0)
        seplabs = VGroup(*[MathTex(f"A_{h}\\otimes\\langle\\cdot,\\cdot\\rangle", font_size=26).move_to(b[1])
                           for h, b in zip([1, 2, 3], sep)])
        with self.say("Here is the flavor of that separation trick. {sh}Several blocks share one leg, "
                      "so they are not independent. {f}The construction takes many copies, "
                      "and uses a finite Fourier transform to give every piece a tentative block label, g. "
                      "{w}Then it weights each term by the square of the mismatch between the guessed label "
                      "and the true one, and keeps only the terms of weight zero. "
                      "{sep}Only correct labels survive. The blocks come out fully separated, each with its own copy "
                      "of the shared leg, and each carrying a bonus dot product, which is where the extra growth "
                      "comes from.") as s:
            self.play(Write(hdr))
            s.wait_until("sh")
            self.play(FadeIn(shared), FadeIn(sh_l), *[Create(l) for l in links], *[FadeIn(b) for b in blocks],
                      FadeIn(blabs), run_time=2)
            s.wait_until("w")
            self.play(Create(ax2), Create(par), FadeIn(par_l), FadeIn(g_l), run_time=2)
            self.play(FadeIn(zero, scale=2), Flash(zero, color=GREEN_3B))
            s.wait_until("sep")
            self.play(TransformFromCopy(VGroup(shared, blocks), sep), FadeIn(seplabs), run_time=2.5)
        self.play(FadeOut(VGroup(hdr, shared, sh_l, blocks, blabs, links, ax2, par, par_l, g_l, zero, sep, seplabs)))

        # ------------------------------------------------------------ the squeeze
        ax3 = Axes(x_range=[0, 8, 2], y_range=[0, 12, 4], x_length=7.5, y_length=5, tips=False,
                   axis_config={"color": GREY_B}).shift(LEFT * 2 + DOWN * 0.3)
        xl = MathTex(r"\log a", font_size=30).next_to(ax3.x_axis, DOWN, buff=0.15).align_to(ax3.x_axis, RIGHT)
        yl = MathTex(r"\log P(a,a)", font_size=30).next_to(ax3.y_axis, UP, buff=0.15)
        t = ValueTracker(0.95)
        floor_c = ax3.plot(lambda x: 4 / 3 * x, x_range=[0, 8], color=GREEN_3B, stroke_width=4)
        def end_dir():
            return UP if np.log(2 * np.exp(8) - 1) / t.get_value() > 4 / 3 * 8 else DOWN

        floor_l = always_redraw(lambda: MathTex(r"\text{floor: } a^{4/3}", font_size=32, color=GREEN_3B).next_to(
            ax3.c2p(8, 10.67), RIGHT).shift(-0.3 * end_dir()))
        ceil_c = always_redraw(lambda: ax3.plot(
            lambda x: np.log(2 * np.exp(x) - 1) / t.get_value(), x_range=[0, 8], color=RED_3B, stroke_width=4))
        ceil_l = always_redraw(lambda: MathTex(r"\text{ceiling: }(2a-1)^{1/t}", font_size=32, color=RED_3B).next_to(
            ax3.c2p(8, min(11.6, np.log(2 * np.exp(8) - 1) / t.get_value())), RIGHT).shift(0.3 * end_dir()))
        tl = always_redraw(lambda: MathTex(f"t={t.get_value():.3f}", font_size=40, color=YELLOW_3B).to_corner(
            UR, buff=0.6))

        def bad_region():
            tv = t.get_value()
            xs = np.linspace(0, 8, 200)
            cv = np.log(2 * np.exp(xs) - 1) / tv
            fv = 4 / 3 * xs
            m = cv < fv
            if not m.any():
                return VMobject()
            xb = xs[m]
            pts = [ax3.c2p(x, 4 / 3 * x) for x in xb] + [ax3.c2p(x, np.log(2 * np.exp(x) - 1) / tv) for x in xb[::-1]]
            return Polygon(*pts, stroke_width=0, fill_color=RED_3B, fill_opacity=0.35)

        bad = always_redraw(bad_region)
        contra = Tex(r"ceiling below floor:\\ contradiction", font_size=30, color=RED_3B).move_to(RIGHT * 4.3 + DOWN * 1)
        with self.say("Now put the two bounds together. On a log-log plot, the floor is a line of slope four thirds. "
                      "{c}The ceiling has slope one over t. {big}If t were bigger than three quarters, "
                      "the ceiling would be shallower than the floor, and for large a it would dip below it. "
                      "Impossible. {sh}So t is at most three quarters, for every character. "
                      "{fin}And three times three quarters is nine fourths.") as s:
            self.play(Create(ax3), FadeIn(xl, yl), Create(floor_c), FadeIn(floor_l), run_time=2)
            s.wait_until("c")
            self.add(ceil_c, ceil_l, tl)
            self.play(FadeIn(ceil_c), run_time=0.8)
            s.wait_until("big")
            self.add(bad)
            self.play(FadeIn(contra))
            self.wait(1)
            s.wait_until("sh")
            self.play(t.animate.set_value(0.75), FadeOut(contra), run_time=3)
            s.wait_until("fin")
            fin = MathTex(r"\omega\ \le\ 3t\ \le\ 3\cdot\tfrac34=\tfrac94", font_size=46, color=YELLOW_3B).move_to(
                RIGHT * 4.2 + DOWN * 1.2)
            self.play(Write(fin), run_time=2)
        self.play(FadeOut(Group(*self.mobjects)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"$\omega\le 9/4$ over $\mathbb{C}$: $n\times n$ products in $O_\varepsilon(n^{9/4+\varepsilon})$ operations",
             r"companions: $\omega<2.258$ in all but finitely many characteristics,",
             r"\qquad and $\omega<2.37106$ over every field",
             r"Manuscript: 13 pages, produced by an OpenAI model"],
            True, r"\emph{An Upper Bound of 9/4 for the Matrix Multiplication Exponent} (Oct.\ 2026)")
        with self.say("Is two the true answer? Nobody knows, and nine fourths leaves plenty of room. "
                      "{c}But after thirty-five years of creeping in the third decimal place, "
                      "a thirteen-page argument from an OpenAI model claims to cut the distance to two by a third, "
                      "{l}and its statement that omega is at most nine fourths has been formalized in the "
                      "Lean proof assistant.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
