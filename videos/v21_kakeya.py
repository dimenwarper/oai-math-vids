from pathlib import Path

import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(Path(__file__).parent / "data" / "v21.npz")
KAK = "[Kakeya](/kɑkˈAjɑ/)"
BES = "[Besicovitch](/bəzˈɪkəvɪʧ/)"
LABA = "[Łaba](/wˈɑbə/)"
ZAHL = "[Zahl](/zˈɑl/)"


def tube(p, q, w, color, op):
    d = normalize(q - p)
    n = rotate_vector(d, PI / 2) * w / 2
    return Polygon(p + n, q + n, q - n, p - n, stroke_width=0).set_fill(color, op)


class Video(NarratedScene):
    def number_line(self, lo, hi, step, width, labels):
        nl = NumberLine(x_range=[lo, hi, step], length=width, include_numbers=False, color=GREY_B,
                        include_tip=False, tick_size=0.08)
        nums = VGroup(*[MathTex(t, font_size=30).next_to(nl.n2p(v), DOWN, buff=0.18) for v, t in labels])
        return nl, nums

    def construct(self):
        card = title_card(self, "074", r"Kakeya in Three and Four Dimensions",
                          r"The maximal conjecture in $\mathbb{R}^3$, full dimension in $\mathbb{R}^4$")
        with self.say("How small can a set be, if it points in every direction?"):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ the needle problem
        S = 2.6
        cL = LEFT * 3.4 + DOWN * 0.2
        cR = RIGHT * 3.0 + DOWN * 0.45
        disk = Circle(radius=S / 2, color=BLUE_3B, stroke_width=3).set_fill(BLUE_3B, 0.15).move_to(cL)
        ang = ValueTracker(0)
        ndl1 = always_redraw(lambda: Line(cL - S / 2 * np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0]),
                                          cL + S / 2 * np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0]),
                                          color=WHITE, stroke_width=6))
        dl = D["deltoid"]
        delt = VMobject(color=YELLOW_3B, stroke_width=3).set_points_as_corners(
            [cR + S * np.array([x, y, 0]) for x, y in dl]).set_fill(YELLOW_3B, 0.15)
        nd = D["needles"]
        k = ValueTracker(0)

        def ndl_pos():
            i = k.get_value() * (len(nd) - 1)
            a = int(np.clip(np.floor(i), 0, len(nd) - 2))
            f = i - a
            v = nd[a] * (1 - f) + nd[a + 1] * f
            return Line(cR + S * np.array([v[0], v[1], 0]), cR + S * np.array([v[2], v[3], 0]), color=WHITE,
                        stroke_width=6)

        ndl2 = always_redraw(ndl_pos)
        end_dot = always_redraw(lambda: Dot(ndl2.get_start(), radius=0.07, color=RED_3B))
        lab1 = Tex(r"disk: area $\pi/4\approx0.785$", font_size=32).move_to(cL[0] * RIGHT + DOWN * 2.6)
        lab2 = Tex(r"deltoid: area $\pi/8\approx0.393$", font_size=32).move_to(cR[0] * RIGHT + DOWN * 2.6)
        ndl0 = Line(LEFT * S / 2, RIGHT * S / 2, color=WHITE, stroke_width=6).shift(DOWN * 0.3)
        q = Tex("Turn a needle of length 1 all the way around. How little area is needed?", font_size=36
                ).to_edge(UP, buff=0.4)
        bes = Tex(r"Besicovitch: the area can be made as small as you like", font_size=36, color=YELLOW_3B
                  ).to_edge(DOWN, buff=0.35)
        with self.say(f"Here is a puzzle {KAK} posed over a century ago. {{n}}A needle of length one lies in the plane. "
                      "What is the smallest area in which you can turn it all the way around? "
                      "{disk}Spinning it about its middle sweeps out a disk. "
                      "{del}Sliding while turning, inside this three cornered curve called a deltoid, "
                      "takes only half the area. "
                      f"{{bes}}Then {BES} found something shocking: the area can be made as small as you like.") as s:
            self.play(FadeIn(q))
            s.wait_until("n")
            self.play(Create(ndl0))
            self.play(Rotate(ndl0, PI / 3), run_time=1.5)
            s.wait_until("disk")
            self.play(Create(disk), FadeOut(ndl0), FadeIn(ndl1))
            self.play(ang.animate.set_value(PI), FadeIn(lab1), run_time=2.5)
            s.wait_until("del")
            self.play(Create(delt), FadeIn(ndl2), FadeIn(end_dot))
            self.play(k.animate.set_value(1), FadeIn(lab2), run_time=6, rate_func=linear)
            s.wait_until("bes")
            self.play(FadeIn(bes))
        self.play(FadeOut(VGroup(disk, ndl1, delt, ndl2, end_dot, lab1, lab2, q, bes)))
        self.remove(ndl1, ndl2, end_dot)

        # ------------------------------------------------------------ a Kakeya-type family, computed
        n = 6
        ab = D[f"fam{n}"]
        xs01 = np.linspace(0, 1, 3)
        ymin = min((ab[:, 0] * x + ab[:, 1]).min() for x in xs01)
        ymax = max((ab[:, 0] * x + ab[:, 1]).max() for x in xs01)
        ymin, ymax = min(ymin, 0), max(ymax, 1)
        box_w, box_h = 4.6, 5.2
        org = LEFT * 6.2 + DOWN * 2.9

        def P(x, y):
            return org + RIGHT * x * box_w + UP * (y - ymin) / (ymax - ymin) * box_h

        fan = VGroup(*[Line(P(0, 0), P(1, a), stroke_width=1.6, color=BLUE_3B) for a, b in ab])
        slid = VGroup(*[Line(P(0, b), P(1, a + b), stroke_width=1.6, color=BLUE_3B) for a, b in ab])
        hdr = Tex(r"$N=64$ needles, one for each slope $\tfrac{j}{N}$", font_size=32).next_to(
            VGroup(fan, slid), UP, buff=0.25)
        ns, areas = D["ns"], D["areas"]
        ax = Axes(x_range=[0, 14, 2], y_range=[0, 0.5, 0.1], x_length=5.6, y_length=4.0, tips=False,
                  axis_config={"color": GREY_B, "font_size": 24},
                  x_axis_config={"numbers_to_include": [2, 4, 6, 8, 10, 12, 14]},
                  y_axis_config={"numbers_to_include": [0.1, 0.2, 0.3, 0.4, 0.5],
                                 "decimal_number_config": {"num_decimal_places": 1}}).shift(RIGHT * 3.3 + DOWN * 0.4)
        xl = MathTex(r"\log_2 N", font_size=30).next_to(ax.x_axis, DOWN, buff=0.45)
        yl = Tex(r"area of union of the width-$\tfrac1N$ needles", font_size=28).next_to(ax, UP, buff=0.25)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=YELLOW_3B) for a, b in zip(ns, areas)])
        crv = VMobject(color=YELLOW_3B, stroke_width=3).set_points_smoothly([ax.c2p(a, b) for a, b in zip(ns, areas)])
        ref = Tex(r"$\approx 1.3/\log_2 N \to 0$", font_size=30, color=YELLOW_3B).move_to(ax.c2p(9.5, 0.33))
        with self.say("Now drop the motion, and just ask for a set containing a unit segment in every direction. "
                      "Here is one explicit recipe: N thin needles, one for each slope, {slide}slid along so "
                      "that they pile up on top of each other. {plot}I computed the area of the union for longer "
                      "and longer lists. It keeps shrinking, roughly like one over log N, so in the limit the area "
                      "is zero.") as s:
            self.play(LaggedStart(*[Create(l) for l in fan], lag_ratio=0.02), FadeIn(hdr), run_time=2)
            s.wait_until("slide")
            self.play(Transform(fan, slid), run_time=3)
            s.wait_until("plot")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.15), Create(crv), run_time=3)
            self.play(FadeIn(ref))
        self.play(FadeOut(VGroup(fan, hdr, ax, xl, yl, dots, crv, ref)))

        conj = VGroup(
            Tex(r"Plane: Kakeya sets can have area zero, but must have", font_size=36),
            Tex(r"Hausdorff dimension 2 (Davies)", font_size=36),
            Tex(r"\textbf{Kakeya conjecture:} a set in $\mathbb{R}^n$ containing a unit segment", font_size=36,
                color=YELLOW_3B),
            Tex(r"in every direction has Hausdorff dimension $n$.", font_size=36, color=YELLOW_3B),
        ).arrange(DOWN, buff=0.25)
        conj[2:].shift(DOWN * 0.4)
        conj.move_to(UP * 1.6)
        fef = Tex(r"Fefferman (1971): Kakeya sets break the ball multiplier in Fourier analysis", font_size=30,
                  color=GREY_A).next_to(conj, DOWN, buff=0.6)
        nl, nums = self.number_line(2, 3, 0.1, 9, [(2, "2"), (2.5, r"\tfrac52"), (3, "3")])
        nl.shift(DOWN * 2.3)
        nums = VGroup(*[MathTex(t, font_size=30).next_to(nl.n2p(v), DOWN, buff=0.18)
                        for v, t in [(2, "2"), (2.5, r"\tfrac52"), (3, "3")]])
        nlab = Tex(r"$\mathbb{R}^3$:", font_size=32).next_to(nl, LEFT, buff=0.3)
        m1 = VGroup(Dot(nl.n2p(2.5), color=BLUE_3B),
                    Tex("Wolff 1995", font_size=26).next_to(nl.n2p(2.5), UP, 0.25).shift(LEFT * 0.8))
        m2 = VGroup(Dot(nl.n2p(2.52), color=TEAL_3B),
                    Tex(r"Katz--{\L}aba--Tao, Katz--Zahl: $>\tfrac52$", font_size=24).next_to(nl.n2p(2.52), DOWN, 0.25
                                                                                          ).shift(RIGHT * 1.9))
        m3 = VGroup(Dot(nl.n2p(3), color=GREEN_3B, radius=0.1),
                    Tex(r"Wang--Zahl 2025", font_size=26, color=GREEN_3B).next_to(nl.n2p(3), UP, 0.25))
        with self.say("But a Kakeya set can't be small in every sense. In the plane, Davies proved it must "
                      "have full Hausdorff dimension, two. {conj}The Kakeya conjecture says the same in every "
                      "dimension: a set in n dimensional space with a unit segment in every direction has "
                      "dimension n. {fef}This is far more than a puzzle. Fefferman showed in 1971 that Kakeya sets "
                      "break a basic question about Fourier series in several variables, and the same overlapping "
                      "tubes sit at the heart of problems like Fourier restriction. "
                      f"{{w}}In three dimensions, Wolff proved dimension at least five halves in 1995. "
                      f"{{kz}}Katz, {LABA} and Tao, and then Katz and {ZAHL}, pushed past it. "
                      f"{{wz}}And in 2025, Hong Wang and Joshua {ZAHL} announced a proof of the three dimensional "
                      "set conjecture: dimension exactly three.") as s:
            self.play(FadeIn(conj[:2]))
            s.wait_until("conj")
            self.play(Write(conj[2:]), run_time=2)
            s.wait_until("fef")
            self.play(FadeIn(fef))
            s.wait_until("w")
            self.play(Create(nl), FadeIn(nums), FadeIn(nlab), FadeIn(m1))
            s.wait_until("kz")
            self.play(FadeIn(m2))
            s.wait_until("wz")
            self.play(FadeIn(m3, scale=1.3))
        self.play(FadeOut(VGroup(conj, fef, nl, nums, nlab, m1, m2, m3)))

        # ------------------------------------------------------------ set vs maximal
        rng = np.random.default_rng(4)
        tubes, lits = VGroup(), VGroup()
        cen = LEFT * 3.3 + DOWN * 0.3
        for i in range(11):
            th = PI * i / 11 + 0.1
            d = np.array([np.cos(th), np.sin(th), 0])
            off = rotate_vector(d, PI / 2) * rng.uniform(-0.5, 0.5) + d * rng.uniform(-0.3, 0.3)
            p, q2 = cen + off - 2.2 * d, cen + off + 2.2 * d
            tubes.add(tube(p, q2, 0.2, BLUE_3B, 0.28))
            s0 = rng.uniform(0, 0.6)
            lits.add(tube(p + (s0 * 4.4) * d, p + (s0 + 0.35) * 4.4 * d, 0.2, YELLOW_3B, 0.9))
        lt = VGroup(
            Tex(r"tubes of radius $\delta$, about $\delta^{-2}$ directions", font_size=30),
            Tex(r"set conjecture: $\big|\bigcup T\big|\gtrsim_\varepsilon \delta^{\varepsilon}$", font_size=34),
            Tex(r"light up a fraction $\lambda$ of each tube:", font_size=30, color=YELLOW_3B),
            MathTex(r"\Big|\bigcup_T Y(T)\Big|\ \gtrsim_\varepsilon\ \delta^{\varepsilon}\,\lambda^{3}\sum_T |T|",
                    font_size=40, color=YELLOW_3B),
            Tex(r"Wang--Zahl: $\lambda^{K(\varepsilon)}$ in place of $\lambda^3$", font_size=30, color=GREY_A),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 2.9 + UP * 0.4)
        lt[3].shift(RIGHT * 0.2)
        mx = MathTex(r"\|K_\delta f\|_{L^3(S^2)}\le C_\varepsilon\,\delta^{-\varepsilon}\|f\|_{L^3(\mathbb{R}^3)}",
                     font_size=40).to_edge(DOWN, buff=0.45)
        mxb = VGroup(mx, caption_box(mx, YELLOW_3B))
        with self.say("So what was left in three dimensions? A stronger, quantitative version. "
                      "Thicken each segment into a tube of radius delta, one for each of about one over delta "
                      "squared separated directions. {set}The set conjecture says the tubes' union has nearly full "
                      "volume, losing at most delta to the epsilon. {lit}The maximal conjecture asks for more. "
                      "Light up only a fraction lambda of each tube, anywhere along it. The lit pieces must still "
                      "fill a volume of about lambda cubed times the total. {wz}Wang and Zahl's theorem gives a much "
                      "worse power of lambda, and they pointed out that exactly lambda cubed is what the maximal "
                      "conjecture needs. {mx}In the language of functions, this says the Kakeya maximal operator is "
                      "bounded on L three, up to delta to the minus epsilon.") as s:
            self.play(LaggedStart(*[FadeIn(t) for t in tubes], lag_ratio=0.1), FadeIn(lt[0]), run_time=2)
            s.wait_until("set")
            self.play(FadeIn(lt[1]))
            s.wait_until("lit")
            self.play(tubes.animate.set_fill(opacity=0.12), LaggedStart(*[FadeIn(l) for l in lits], lag_ratio=0.1),
                      FadeIn(lt[2]), run_time=2)
            self.play(Write(lt[3]))
            s.wait_until("wz")
            self.play(FadeIn(lt[4]))
            s.wait_until("mx")
            self.play(Write(mxb))
        self.play(FadeOut(VGroup(tubes, lits, lt, mxb)))

        # ------------------------------------------------------------ the two theorems
        th3 = Tex(r"\textbf{Theorem 1} ($\mathbb{R}^3$). The Kakeya maximal conjecture holds:", font_size=34)
        th3b = MathTex(r"\|K_\delta f\|_{L^3(S^2)}\le C_\varepsilon\,\delta^{-\varepsilon}\|f\|_{L^3(\mathbb{R}^3)}",
                       font_size=40)
        th4 = Tex(r"\textbf{Theorem 2} ($\mathbb{R}^4$). Every Kakeya set in $\mathbb{R}^4$ has", font_size=34)
        th4b = Tex(r"Hausdorff dimension 4 (no compactness or regularity assumed).", font_size=34)
        thm = VGroup(th3, th3b, th4, th4b).arrange(DOWN, buff=0.28)
        thm[2].shift(DOWN * 0.3)
        thm[3].shift(DOWN * 0.3)
        thm.move_to(UP * 1.5)
        tb = caption_box(thm, YELLOW_3B, 0.3)
        nl4 = NumberLine(x_range=[3, 4, 0.1], length=9, include_numbers=False, color=GREY_B, include_tip=False,
                         tick_size=0.08).shift(DOWN * 2.5)
        n4 = VGroup(*[MathTex(t, font_size=30).next_to(nl4.n2p(v), DOWN, buff=0.18) for v, t in [(3.5, "3.5"), (4, "4")]])
        l4 = Tex(r"$\mathbb{R}^4$:", font_size=32).next_to(nl4, LEFT, buff=0.3)
        w4 = VGroup(Dot(nl4.n2p(3), color=BLUE_3B), Tex("Wolff: 3", font_size=26).next_to(nl4.n2p(3), DOWN, 0.22))
        g4 = VGroup(Dot(nl4.n2p(3.025), color=TEAL_3B),
                    Tex(r"$3+\tfrac1{40}$", font_size=26).next_to(nl4.n2p(3.025), UP, 0.25).shift(RIGHT * 0.3))
        k4 = VGroup(Dot(nl4.n2p(3.059), color=TEAL_3B),
                    Tex(r"Katz--Zahl: $3.059$", font_size=26).next_to(nl4.n2p(3.059), UP, 0.25).shift(RIGHT * 1.7))
        o4 = VGroup(Dot(nl4.n2p(4), color=YELLOW_3B, radius=0.1),
                    Tex(r"claimed: 4", font_size=26, color=YELLOW_3B).next_to(nl4.n2p(4), UP, 0.25))
        with self.say("Two manuscripts in OpenAI's math catalogue, produced by an OpenAI model and not yet peer "
                      "reviewed, claim two new results. {t1}First: the Kakeya maximal conjecture in three "
                      "dimensions. {t2}Second: in four dimensions, every Kakeya set has Hausdorff dimension four. "
                      "{nl}There, Wolff's argument gives three, and the best previous Hausdorff bound cited in the "
                      "paper is about three point oh six, due to Katz and Zahl.") as s:
            self.play(Create(tb), FadeIn(th3))
            s.wait_until("t1")
            self.play(Write(th3b), run_time=1.5)
            s.wait_until("t2")
            self.play(FadeIn(th4), FadeIn(th4b))
            s.wait_until("nl")
            self.play(Create(nl4), FadeIn(n4), FadeIn(l4), FadeIn(w4))
            self.play(FadeIn(g4), FadeIn(k4))
            self.play(FadeIn(o4, scale=1.3))
        self.play(FadeOut(VGroup(thm, tb, nl4, n4, l4, w4, g4, k4, o4)))

        # ------------------------------------------------------------ proof idea (3D)
        hdr = Tex("Three dimensions: study the configurations that would be extremal", font_size=36,
                  color=YELLOW_3B).to_edge(UP, buff=0.35)
        crit = MathTex(r"\Big|\bigcup Y(T)\Big|\ \ge\ \delta^{\,e}\,\lambda^3\sum|T|", r"\qquad e=\text{critical exponent}",
                       font_size=36).next_to(hdr, DOWN, buff=0.35)
        crit[1].set_color(GREY_A)
        # (a) packet zoom
        pa = LEFT * 5.2 + UP * 1.1
        bg = VGroup(*[tube(pa + rotate_vector(RIGHT, a) * -1.0 + UP * dy, pa + rotate_vector(RIGHT, a) * 1.0 + UP * dy,
                           0.05, GREY_B, 0.35) for a, dy in zip([0.9, -0.7, 1.4, -1.2], [0.45, -0.5, -0.3, 0.55])])
        pk = VGroup(*[tube(pa + rotate_vector(RIGHT, a) * -0.3 + UP * dy, pa + rotate_vector(RIGHT, a) * 0.3 + UP * dy,
                           0.035, BLUE_3B, 0.8) for a, dy in zip(np.linspace(-0.3, 0.3, 7), np.linspace(-0.08, 0.08, 7))])
        pbox = Square(0.7, color=RED_3B, stroke_width=3).move_to(pa)
        zc = LEFT * 2.2 + UP * 1.1
        zoom = Square(1.75, color=RED_3B, stroke_width=3).move_to(zc)
        zarr = Arrow(pbox.get_right(), zoom.get_left(), buff=0.1, color=RED_3B, stroke_width=3)
        pl = Tex(r"too much mass in a small packet?\\ rescale it: a better exponent", font_size=26).move_to(
            LEFT * 3.6 + DOWN * 0.25)
        # (b) planiness
        pc = RIGHT * 3.4 + UP * 1.1
        plate = Polygon(pc + LEFT * 1.6 + DOWN * 0.7, pc + RIGHT * 1.2 + DOWN * 0.7, pc + RIGHT * 1.6 + UP * 0.7,
                        pc + LEFT * 1.2 + UP * 0.7, color=TEAL_3B, stroke_width=2).set_fill(TEAL_3B, 0.15)
        through = VGroup(*[tube(pc + rotate_vector(RIGHT, a) * -1.25 * np.array([1, 0.45, 0]),
                                pc + rotate_vector(RIGHT, a) * 1.25 * np.array([1, 0.45, 0]), 0.07, BLUE_3B, 0.8)
                           for a in np.linspace(-1.2, 1.2, 6)])
        bl = Tex(r"multilinear Kakeya $\Rightarrow$ tubes through\\ a point lie near a plane: thin plates", font_size=26
                 ).move_to(RIGHT * 3.4 + DOWN * 0.25)
        # (c) stationary profile
        pax = Axes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], x_length=3.4, y_length=1.3, tips=False,
                   axis_config={"color": GREY_B}).move_to(LEFT * 3.6 + DOWN * 1.85)
        prof = pax.plot(lambda x: max(0.0, 1.3 * (x - 0.35)), x_range=[0, 1, 0.005], color=YELLOW_3B, stroke_width=4)
        tau = MathTex(r"\tau", font_size=26).next_to(pax.c2p(0.35, 0), DOWN, buff=0.1)
        sx = Tex("scale", font_size=22, color=GREY_A).next_to(pax.x_axis, RIGHT, buff=0.1)
        prl = Tex(r"stationary profile $F(s)=\beta\,(s-\tau)_+$", font_size=26).next_to(pax, DOWN, buff=0.3)
        # (d) two frames
        fc = RIGHT * 3.4 + DOWN * 1.75
        mat = MathTex(r"\begin{pmatrix}X'\\ U'\end{pmatrix}=\begin{pmatrix}1&\Delta t\\0&1\end{pmatrix}"
                      r"\begin{pmatrix}X\\ U\end{pmatrix}", font_size=36).move_to(fc)
        ml = Tex(r"one tube seen from two lit points:\\ position $X$ shifts by $\Delta t\cdot$ velocity $U$",
                 font_size=26).next_to(mat, DOWN, buff=0.3)
        with self.say("How does the three dimensional proof work? {crit}Define the critical exponent: the smallest "
                      "extra power of one over delta needed to make the lit tube inequality hold for every "
                      "configuration. Suppose it were positive. Then some configurations nearly attain it, and the "
                      "proof studies their shape. {pk}First, such a configuration can't hide a small packet carrying "
                      "too much mass: {zoom}rescaling that packet would give a better exponent. "
                      "{pl}Combined with multilinear Kakeya, which controls tubes in three independent directions, "
                      "this forces the tubes through a point to be nearly coplanar, and organizes them into thin "
                      "plates. {st}Comparing two ways of cutting the configuration across scales then forces a "
                      "self similar, stationary profile. {fr}Finally, the same tube seen from two of its lit points "
                      "gives two coordinate frames, related by a simple shear. Entropy bookkeeping, with the planar "
                      "Furstenberg estimate of Ren and Wang, shows these frames can't carry all the information the "
                      "stationary pieces demand. {end}So the critical exponent is zero.") as s:
            self.play(Write(hdr))
            s.wait_until("crit")
            self.play(Write(crit), run_time=2)
            s.wait_until("pk")
            self.play(FadeIn(bg), FadeIn(pk), Create(pbox))
            s.wait_until("zoom")
            self.play(GrowArrow(zarr), TransformFromCopy(pbox, zoom), pk.copy().animate.scale(2.4).move_to(zc),
                      run_time=1.5)
            self.play(FadeIn(pl))
            s.wait_until("pl")
            self.play(FadeIn(plate), LaggedStart(*[FadeIn(t) for t in through], lag_ratio=0.15), run_time=2)
            self.play(FadeIn(bl))
            s.wait_until("st")
            self.play(Create(pax), FadeIn(tau), FadeIn(sx))
            self.play(Create(prof), FadeIn(prl))
            s.wait_until("fr")
            self.play(Write(mat), run_time=1.5)
            self.play(FadeIn(ml))
            s.wait_until("end")
            ez = MathTex(r"e=0", font_size=44, color=GREEN_3B).next_to(crit, RIGHT, buff=0.4)
            self.play(Transform(crit[1], ez))
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ------------------------------------------------------------ four dimensions
        hdr = Tex(r"Four dimensions: nested quadratic charts (175 pages)", font_size=36, color=YELLOW_3B).to_edge(
            UP, buff=0.35)
        bx = Rectangle(width=5.2, height=3.4, color=GREY_B).shift(LEFT * 3.2 + DOWN * 0.5)
        par = FunctionGraph(lambda x: 0.28 * x ** 2 - 1.0, x_range=[-2.3, 2.3], color=TEAL_3B, stroke_width=3
                            ).shift(LEFT * 3.2 + DOWN * 0.5)
        segs = VGroup()
        rng4 = np.random.default_rng(8)
        for x0 in np.linspace(-2.0, 2.0, 9):
            y0 = 0.28 * x0 ** 2 - 1.0
            sl = 0.56 * x0
            d = normalize(np.array([1, sl, 0]))
            c0 = LEFT * 3.2 + DOWN * 0.5 + np.array([x0, y0, 0]) + rotate_vector(d, PI / 2) * rng4.uniform(0.07, 0.16)
            d = rotate_vector(d, rng4.uniform(-0.12, 0.12))
            segs.add(Line(c0 - 0.45 * d, c0 + 0.45 * d, color=WHITE, stroke_width=3))
        inner = Rectangle(width=1.6, height=1.0, color=ORANGE_3B).move_to(LEFT * 3.2 + DOWN * 1.4)
        bl = Tex(r"a \emph{chart}: line pieces in a box\\ nearly obeying one quadratic relation", font_size=28
                 ).next_to(bx, DOWN, buff=0.25)
        steps = VGroup(
            Tex(r"$\bullet$ uses the 3D estimate as an input", font_size=30),
            Tex(r"$\bullet$ a Kakeya set of dimension $<4$ would force", font_size=30),
            Tex(r"\quad every good chart system to pay a fixed cost", font_size=30),
            Tex(r"$\bullet$ three geometric regimes: each yields an", font_size=30),
            Tex(r"\quad impossible improvement $\Rightarrow$ contradiction", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 3.3 + DOWN * 0.3)
        with self.say("The four dimensional proof is much longer, a hundred and seventy five pages, and it uses the "
                      "three dimensional estimate as one of its inputs. {ch}Its basic object is a chart: a box in "
                      "which pieces of lines nearly obey a single quadratic relation. Charts can be nested inside "
                      "charts. {cost}A Kakeya set of dimension below four would force every good system of charts "
                      "to pay a definite cost. {reg}The proof splits into three geometric regimes, and in each one "
                      "produces an improvement that cannot exist, a contradiction.") as s:
            self.play(Write(hdr), FadeIn(steps[0]))
            s.wait_until("ch")
            self.play(Create(bx), Create(par), LaggedStart(*[Create(g) for g in segs], lag_ratio=0.1), run_time=2)
            self.play(FadeIn(bl))
            self.play(Create(inner))
            s.wait_until("cost")
            self.play(FadeIn(steps[1:3]))
            s.wait_until("reg")
            self.play(FadeIn(steps[3:]))
        self.play(FadeOut(VGroup(hdr, bx, par, segs, inner, bl, steps)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"$\mathbb{R}^3$: Kakeya maximal conjecture, $\|K_\delta f\|_{L^3(S^2)}\le C_\varepsilon\delta^{-\varepsilon}"
             r"\|f\|_{L^3}$",
             r"$\mathbb{R}^4$: every Kakeya set has Hausdorff dimension 4",
             r"Manuscripts: 97 and 175 pages, produced by an OpenAI model"],
            False, r"\emph{The Kakeya maximal conjecture in three dimensions} (Sept.\ 2026)")
        with self.say("Neither proof has been formalized in Lean, and together they run to over two hundred and "
                      "seventy pages, with the four dimensional result resting on the three dimensional one. "
                      "{c}So they need careful checking by experts. If they hold, Kakeya is settled in its strong "
                      "maximal form in three dimensions, and for sets in four.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("c")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
