import numpy as np
from manim import *

from style import *
from vo import NarratedScene

DEL = "[Deligne](/dəlˈinjə/)"
AND = "[André](/ɑndɹˈA/)"
POHL = "[Pohlmann](/pˈOlmən/)"
MARK = "[Markman](/mˈɑɹkmən/)"
LEF = "[Lefschetz](/lˈɛfʃɛts/)"


def sign_tile(sign, size=0.62):
    col = BLUE_3B if sign > 0 else ORANGE_3B
    sq = RoundedRectangle(width=size, height=size, corner_radius=0.08, stroke_width=2, stroke_color=WHITE).set_fill(
        col, 0.75)
    t = MathTex("+" if sign > 0 else "-", font_size=36, color=BLACK).move_to(sq)
    return VGroup(sq, t)


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "032", r"The Hodge Conjecture for CM Abelian Varieties",
                          r"Every rational Hodge class on a CM abelian variety is algebraic")
        with self.say("The Hodge conjecture, claimed for every abelian variety with complex multiplication."):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ what the conjecture asks
        cen = LEFT * 3.6 + UP * 0.3
        outer = Ellipse(width=5.4, height=2.9, color=BLUE_3B, stroke_width=4).move_to(cen)
        hole_top = ArcBetweenPoints(cen + LEFT * 1.1 + UP * 0.05, cen + RIGHT * 1.1 + UP * 0.05, angle=-PI / 2.2,
                                    color=BLUE_3B, stroke_width=4)
        hole_bot = ArcBetweenPoints(cen + LEFT * 1.35 + UP * 0.2, cen + RIGHT * 1.35 + UP * 0.2, angle=PI / 2.6,
                                    color=BLUE_3B, stroke_width=4)
        torus = VGroup(outer, hole_top, hole_bot)
        loop_a = Ellipse(width=3.8, height=1.65, color=YELLOW_3B, stroke_width=3).move_to(cen + UP * 0.05)
        loop_b = Ellipse(width=0.55, height=1.15, color=RED_3B, stroke_width=3).move_to(cen + DOWN * 0.85)
        tl = Tex(r"cohomology: the holes and cycles\\ of every dimension", font_size=28).next_to(outer, DOWN, buff=0.3)
        # Hodge diamond of an abelian surface
        dc = RIGHT * 3.4 + UP * 0.6
        hd = {(0, 0): 1, (1, 0): 2, (0, 1): 2, (2, 0): 1, (1, 1): 4, (0, 2): 1, (2, 1): 2, (1, 2): 2, (2, 2): 1}
        diamond = VGroup()
        for (p, q_), h in hd.items():
            pos = dc + RIGHT * 0.85 * (q_ - p) + UP * 0.75 * (2 - p - q_) + DOWN * 0.0
            col = YELLOW_3B if p == q_ else GREY_A
            diamond.add(MathTex(rf"h^{{{p},{q_}}}", font_size=28, color=col).move_to(pos))
        dl = Tex(r"Hodge decomposition $H^k=\bigoplus_{p+q=k}H^{p,q}$", font_size=28).next_to(diamond, DOWN, buff=0.35)
        pp = Tex(r"subvarieties give rational classes\\ of type $(p,p)$: the middle column", font_size=28,
                 color=YELLOW_3B).next_to(dl, DOWN, buff=0.3)
        conj = VGroup(
            Tex(r"\textbf{Hodge conjecture} (Hodge, ICM 1950): every rational class of type $(p,p)$", font_size=32),
            Tex(r"is a rational combination of classes of algebraic subvarieties.", font_size=32),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)
        with self.say("A complex algebraic variety is a shape cut out by polynomial equations. Its topology is "
                      "recorded by cohomology, which measures holes and cycles of every dimension. {sub}Each "
                      "subvariety, a smaller shape cut out by polynomials, defines a cohomology class. {hd}Cohomology splits into pieces of type p comma q, and classes of "
                      "subvarieties are rational and always land in the middle column, type p comma p. {q}At the "
                      "International Congress in 1950, Hodge asked about the converse: is every rational class of "
                      "type p comma p a rational combination of classes of subvarieties? {cl}That is the Hodge "
                      f"conjecture, one of the Clay Millennium Prize problems. For divisors, it is a classical "
                      f"theorem of {LEF}. Beyond that, it is open in general.") as s:
            self.play(Create(torus), run_time=2)
            self.play(FadeIn(tl))
            s.wait_until("sub")
            self.play(Create(loop_a), Create(loop_b))
            s.wait_until("hd")
            self.play(LaggedStart(*[FadeIn(d) for d in diamond], lag_ratio=0.1), FadeIn(dl))
            self.play(FadeIn(pp))
            s.wait_until("q")
            self.play(FadeIn(conj))
            s.wait_until("cl")
            self.play(Indicate(conj, color=YELLOW_3B, scale_factor=1.03))
        self.play(FadeOut(VGroup(torus, loop_a, loop_b, tl, diamond, dl, pp, conj)))

        # ------------------------------------------------------------ abelian varieties and CM
        def lattice(c, b1, b2, color, rng_=4, clip=2.1):
            pts = VGroup()
            for i in range(-rng_, rng_ + 1):
                for j in range(-rng_, rng_ + 1):
                    v = i * np.array(b1) + j * np.array(b2)
                    if abs(v[0]) <= clip and abs(v[1]) <= clip:
                        pts.add(Dot(c + np.array([v[0], v[1], 0]), radius=0.07, color=color))
            return pts

        cl_, cr_ = LEFT * 3.4 + DOWN * 0.5, RIGHT * 3.4 + DOWN * 0.5
        frameL = Square(4.6, color=GREY_D).move_to(cl_)
        frameR = Square(4.6, color=GREY_D).move_to(cr_)
        gen = lattice(cl_, (0.95, 0), (0.35, 1.2), GREY_A)
        sqr = lattice(cr_, (1.0, 0), (0, 1.0), GREY_A)
        genr = gen.copy().set_color(RED_3B)
        sqrr = sqr.copy().set_color(GREEN_3B)
        lg = Tex(r"a generic lattice", font_size=30).next_to(frameL, UP, buff=0.2)
        lr = Tex(r"the Gaussian integers $\mathbb{Z}[i]$", font_size=30).next_to(frameR, UP, buff=0.2)
        mg = Tex(r"rotated by $90^\circ$: no match", font_size=28, color=RED_3B).next_to(frameL, DOWN, buff=0.2)
        mr = Tex(r"$\times i$ maps it to itself: \textbf{CM}", font_size=28, color=GREEN_3B).next_to(frameR, DOWN,
                                                                                                    buff=0.2)
        top = Tex(r"Abelian variety: a complex torus $\mathbb{C}^g/\Lambda$ that is also algebraic", font_size=32
                  ).to_edge(UP, buff=0.3)
        with self.say("Abelian varieties are complex tori that are also algebraic: complex space, modulo a lattice. "
                      "{e}In dimension one they are elliptic curves: the plane, modulo a lattice of points. "
                      "{g}Rotate a typical lattice by ninety degrees, and it does not match itself. {sq}But the square lattice of Gaussian integers is preserved by multiplication by i. "
                      "{cm}This is complex multiplication, CM for short. In higher dimensions, CM abelian varieties "
                      "are the ones with the largest possible commutative algebra of symmetries.") as s:
            self.play(FadeIn(top))
            s.wait_until("e")
            self.play(Create(frameL), Create(frameR), FadeIn(gen), FadeIn(sqr), FadeIn(lg), FadeIn(lr))
            s.wait_until("g")
            self.play(Rotate(genr, PI / 2, about_point=cl_), run_time=2)
            self.play(FadeIn(mg))
            s.wait_until("sq")
            self.play(Rotate(sqrr, PI / 2, about_point=cr_), run_time=2)
            self.play(FadeIn(mr))
        self.play(FadeOut(VGroup(top, frameL, frameR, gen, sqr, genr, sqrr, lg, lr, mg, mr)))

        # ------------------------------------------------------------ history
        hist = VGroup(
            Tex(r"Products of divisor classes give many algebraic Hodge classes, but not all:", font_size=32),
            Tex(r"exotic \emph{Weil classes} appear already on abelian fourfolds", font_size=32, color=GREY_A),
            Tex(r"1982, Deligne: Hodge classes on abelian varieties are \emph{absolute Hodge}", font_size=32),
            Tex(r"(an arithmetic shadow of algebraicity; it produces no cycles)", font_size=28, color=GREY_A),
            Tex(r"Deligne, Andr\'e: CM Hodge classes reduce to Weil-type classes on auxiliary CM", font_size=32),
            Tex(r"varieties, whose algebraicity was unknown in general", font_size=32),
            Tex(r"Recently, Markman: the conjecture for all abelian fourfolds", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        for k in (2, 4, 6):
            hist[k:].shift(DOWN * 0.2)
        hist[1].shift(RIGHT * 0.4)
        hist[3].shift(RIGHT * 0.4)
        hist[5].shift(RIGHT * 0.4)
        with self.say("For abelian varieties, products of divisor classes give many "
                      "algebraic Hodge classes, but not all of them: exotic classes, called Weil classes, already "
                      f"appear on abelian fourfolds. {{d}}In 1982, {DEL} proved that Hodge classes on abelian varieties "
                      "are absolute Hodge, an arithmetic shadow of being algebraic, but this produces no cycles. "
                      f"{{a}}For CM varieties, work of {DEL} and {AND} reduced every Hodge class to Weil-type classes "
                      "on auxiliary CM varieties, whose algebraicity was not known in general. {m}And recently, "
                      f"{MARK} proved the conjecture for all abelian fourfolds.") as s:
            self.play(FadeIn(hist[:2]))
            s.wait_until("d")
            self.play(FadeIn(hist[2:4]))
            s.wait_until("a")
            self.play(FadeIn(hist[4:6]))
            s.wait_until("m")
            self.play(FadeIn(hist[6]))
        self.play(FadeOut(hist))

        # ------------------------------------------------------------ theorem
        thm = VGroup(Tex(r"\textbf{Theorem.} Let $A$ be a complex abelian variety with CM.", font_size=38),
                     Tex(r"Then for every $p$, every rational Hodge class of type $(p,p)$ on $A$", font_size=34),
                     Tex(r"is a rational linear combination of algebraic cycle classes.", font_size=34),
                     ).arrange(DOWN, buff=0.2)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3)).shift(UP * 1.4)
        cons = VGroup(
            Tex(r"$\Rightarrow$ the generalized Hodge conjecture for CM abelian varieties", font_size=30),
            Tex(r"$\Rightarrow$ via Milne: the Tate conjecture for abelian varieties over finite fields",
                font_size=30),
            Tex(r"$\Rightarrow$ via Milne: the Hodge standard conjecture for abelian varieties,", font_size=30),
            Tex(r"in every characteristic", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(tb, DOWN, buff=0.5)
        cons[3].shift(RIGHT * 0.45)
        with self.say("A manuscript in OpenAI's math catalogue claims the conjecture for every CM abelian variety: "
                      "{t}in every dimension and every codimension, each rational Hodge class is a rational "
                      "combination of algebraic cycles. {c}Through theorems of Milne, this would also give the Tate "
                      "conjecture for abelian varieties over finite fields, and the Hodge standard conjecture for "
                      "abelian varieties in every characteristic.") as s:
            s.wait_until("t")
            self.play(Write(tb), run_time=3)
            s.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c) for c in cons], lag_ratio=0.5), run_time=2.5)
        self.play(FadeOut(VGroup(tb, cons)))

        # ------------------------------------------------------------ proof 1: signs
        hdr = Tex(r"Step 1: bookkeeping with signs", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.35)
        expl = VGroup(
            Tex(r"$H^1$ of a CM abelian variety splits into lines, one per embedding:", font_size=30),
            Tex(r"each line is holomorphic ($+$) or antiholomorphic ($-$)", font_size=30),
        ).arrange(DOWN, buff=0.12).next_to(hdr, DOWN, buff=0.3)
        types = [[1, 1, -1, -1], [1, -1, -1, 1], [1, -1, 1, -1]]
        grid = VGroup(*[sign_tile(v) for row in types for v in row]).arrange_in_grid(3, 4, buff=0.12)
        grid.move_to(LEFT * 1.6 + DOWN * 1.1)
        rl = VGroup(*[Tex(f"conjugate {i + 1}", font_size=26, color=GREY_A).next_to(grid[4 * i], LEFT, buff=0.3)
                      for i in range(3)])
        cl = VGroup(*[MathTex(str(j + 1), font_size=26, color=GREY_A).next_to(grid[j], UP, buff=0.15)
                      for j in range(4)])
        cl.add(Tex("tensor factors", font_size=24, color=GREY_A).next_to(cl, UP, buff=0.12))
        chk = VGroup(*[Tex(r"$2+,\ 2-$ \checkmark", font_size=28, color=GREEN_3B).next_to(grid[4 * i + 3], RIGHT,
                                                                                           buff=0.35)
                       for i in range(3)])
        rule = Tex(r"a product of lines is a Hodge class $\iff$ balanced in \emph{every}\\ Galois conjugate "
                   r"(Pohlmann's criterion)", font_size=30, color=YELLOW_3B).to_edge(DOWN, buff=0.35)
        with self.say("How does the proof go? {e}The first cohomology of a CM abelian variety splits into lines, one "
                      "for each embedding of its CM field, and each line is either holomorphic, plus, or "
                      "antiholomorphic, minus. {g}A product of such lines has a type that you can read off by counting "
                      "signs. {b}It is a Hodge class exactly when it is balanced, equally many plusses and minuses, "
                      "and this must hold in every Galois conjugate, which reshuffles the signs. That is "
                      f"{POHL}'s criterion.") as s:
            self.play(Write(hdr))
            s.wait_until("e")
            self.play(FadeIn(expl))
            s.wait_until("g")
            self.play(LaggedStart(*[FadeIn(t_, scale=0.7) for t_ in grid], lag_ratio=0.05), FadeIn(rl), FadeIn(cl),
                      run_time=2)
            s.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in chk], lag_ratio=0.3), run_time=1.5)
            self.play(FadeIn(rule))
        self.play(FadeOut(VGroup(hdr, expl, grid, rl, cl, chk, rule)))

        # ------------------------------------------------------------ proof 2: four-factor switch
        hdr = Tex(r"Step 2: reduce everything to four-factor switches", font_size=40, color=YELLOW_3B).to_edge(
            UP, buff=0.35)
        V = [[1, 1, 1], [1, -1, -1], [1, 1, -1], [1, -1, 1]]
        cols = VGroup()
        for j, v in enumerate(V):
            col = VGroup(*[sign_tile(x, 0.55) for x in v]).arrange(DOWN, buff=0.1)
            cols.add(col)
        cols.arrange(RIGHT, buff=0.25)
        plus = MathTex("+", font_size=40).move_to((cols[0].get_center() + cols[1].get_center()) / 2)
        cols[1].shift(RIGHT * 0.35)
        cols[2].shift(RIGHT * 1.6)
        cols[3].shift(RIGHT * 1.95)
        plus.move_to((cols[0].get_right() + cols[1].get_left()) / 2)
        eqs = MathTex("=", font_size=44).move_to((cols[1].get_right() + cols[2].get_left()) / 2)
        plus2 = MathTex("+", font_size=40).move_to((cols[2].get_right() + cols[3].get_left()) / 2)
        sw = VGroup(cols, plus, eqs, plus2).move_to(LEFT * 3.2 + DOWN * 0.3)
        names = VGroup(*[MathTex(f"v_{j + 1}", font_size=32).next_to(cols[j], UP, buff=0.2) for j in range(4)])
        rel = MathTex(r"v_1+v_2=v_3+v_4", font_size=38, color=TEAL_3B).next_to(sw, DOWN, buff=0.5)
        line = MathTex(r"U(v_1)\otimes U(v_2)\otimes \overline{U(v_3)}\otimes\overline{U(v_4)}", font_size=34
                       ).move_to(RIGHT * 3.0 + UP * 1.4)
        lt = Tex(r"type $(2,2)$ in every conjugate:\\ a Hodge class on a product\\ of four CM abelian varieties",
                 font_size=28).next_to(line, DOWN, buff=0.3)
        red = Tex(r"Any balanced class is reached by a chain\\ of such switches, glued together by\\ "
                  r"polarization pairings (all algebraic)", font_size=28, color=GREY_A).next_to(lt, DOWN, buff=0.45)
        goal = Tex(r"So it suffices: every four-factor switch class is algebraic", font_size=32, color=YELLOW_3B
                   ).to_edge(DOWN, buff=0.35)
        with self.say("The manuscript then reduces everything to one kind of building block. {v}Take four sign "
                      "patterns, v one through v four, with v one plus v two equal to v three plus v four, position "
                      "by position. {l}Pair the first two lines with the conjugates of the other two, and you get a "
                      "balanced class of type two comma two on a product of four CM abelian varieties: a four-factor "
                      "switch. {r}Any balanced class can be reached by a chain of such switches, glued together with "
                      "polarization pairings, which are algebraic. {g}So it "
                      "suffices to show that every four-factor switch class is algebraic.") as s:
            self.play(Write(hdr))
            s.wait_until("v")
            self.play(FadeIn(cols), FadeIn(names), FadeIn(plus), FadeIn(eqs), FadeIn(plus2))
            self.play(Write(rel))
            s.wait_until("l")
            self.play(Write(line), run_time=2)
            self.play(FadeIn(lt))
            s.wait_until("r")
            self.play(FadeIn(red))
            s.wait_until("g")
            self.play(FadeIn(goal))
        self.play(FadeOut(VGroup(hdr, sw, names, rel, line, lt, red, goal)))

        # ------------------------------------------------------------ proof 3: surface criterion + ball quotient
        hdr = Tex(r"Step 3: find the right surface", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.35)
        S = VMobject(color=TEAL_3B, stroke_width=4).set_points_smoothly(
            [np.array([np.cos(a) * (1.6 + 0.12 * np.sin(2 * a + 0.5)), np.sin(a) * (1.0 + 0.1 * np.cos(3 * a)), 0])
             for a in np.linspace(0, TAU, 41)[:-1]] + [np.array([1.6 + 0.12 * np.sin(0.5), 0, 0])]
        ).set_fill(TEAL_3B, 0.2).move_to(LEFT * 3.8 + UP * 0.3)
        Sl = MathTex("S", font_size=40, color=TEAL_3B).move_to(S)
        targets = VGroup(*[MathTex(rf"B(v_{j + 1})", font_size=32).move_to(RIGHT * 0.5 + UP * (2.1 - 1.1 * j))
                           for j in range(4)])
        arrows = VGroup(*[Arrow(S.get_right(), t_.get_left(), buff=0.15, color=GREY_B, stroke_width=3) for t_ in targets])
        integ = MathTex(r"\int_S \eta_1\wedge\eta_2\wedge\eta_3\wedge\eta_4\ \neq\ 0", font_size=38,
                        color=YELLOW_3B).move_to(RIGHT * 4.3 + UP * 1.5)
        il = Tex(r"$\eta_i$: one-forms pulled back\\ from $B(v_i)$", font_size=26, color=GREY_A).next_to(integ, DOWN,
                                                                                                    buff=0.2)
        img = Tex(r"$\Rightarrow$ the image of $S$ in $\prod_i B(v_i)$\\ is an algebraic cycle detecting\\ the "
                  r"switch class", font_size=28, color=GREEN_3B).next_to(il, DOWN, buff=0.35)
        # ball quotient picture
        disk = Circle(radius=1.45, color=PURPLE_3B, stroke_width=3).move_to(LEFT * 3.8 + UP * 0.3)
        geos = VGroup()
        for k in range(9):
            th = TAU * k / 9
            d_ = 1.45 * 1.55
            r_ = np.sqrt(d_**2 - 1.45**2)
            c_ = disk.get_center() + d_ * np.array([np.cos(th), np.sin(th), 0])
            a0 = np.arctan2(*(disk.get_center() - c_)[[1, 0]])
            half = np.arctan2(1.45, r_)
            geos.add(Arc(radius=r_, start_angle=a0 - half, angle=2 * half, arc_center=c_, color=PURPLE_3B,
                         stroke_width=2))
        ball = VGroup(disk, geos)
        bl = Tex(r"compact complex 2-ball quotient (schematic)", font_size=26,
                 color=PURPLE_3B).next_to(disk, DOWN, buff=0.25)
        how = VGroup(
            Tex(r"theta series $\rightarrow$ holomorphic one-forms", font_size=28),
            Tex(r"continuity + weak approximation $\rightarrow$ a nonzero mixed integral", font_size=28),
            Tex(r"Hecke operators and Frobenius $\rightarrow$ the forms come from the right CM types", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.say("Here is how a switch class becomes algebraic. {s}Suppose a surface S maps to the four abelian "
                      "varieties, and the four one-forms pulled back from them have a nonzero integral over S. "
                      "{i}Then the image of S in the product is an algebraic cycle that detects the switch class, "
                      "and that is enough to make the class algebraic. {b}The manuscript "
                      "finds S as a compact quotient of the complex two-dimensional ball by an arithmetic unitary "
                      "group. {h}Theta series supply holomorphic one-forms on it. A continuity argument, moving local "
                      "data by weak approximation, makes the mixed integral nonzero. And a computation with Hecke "
                      "operators and Frobenius shows that those one-forms come from exactly the right CM abelian "
                      "varieties.") as s:
            self.play(Write(hdr))
            s.wait_until("s")
            self.play(DrawBorderThenFill(S), FadeIn(Sl))
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), FadeIn(targets))
            self.play(Write(integ), FadeIn(il))
            s.wait_until("i")
            self.play(FadeIn(img))
            s.wait_until("b")
            self.play(FadeOut(S), FadeOut(Sl), FadeIn(ball), FadeIn(bl))
            s.wait_until("h")
            self.play(LaggedStart(*[FadeIn(h_) for h_ in how], lag_ratio=0.6), run_time=4)
        self.play(FadeOut(VGroup(hdr, ball, bl, targets, arrows, integ, il, img, how)))

        # ------------------------------------------------------------ closing
        fam = VGroup(Tex(r"Companion manuscripts in the same family:", font_size=32),
                     Tex(r"the rational Hodge conjecture for every product of K3 surfaces,", font_size=32),
                     Tex(r"and algebraicity of Kuga--Satake correspondences", font_size=32)).arrange(DOWN, buff=0.18)
        with self.say("Companion manuscripts in the same family go further, claiming the rational Hodge conjecture "
                      "for every product of K3 surfaces.") as s:
            self.play(FadeIn(fam))
        self.play(FadeOut(fam))
        card = status_card(
            [r"Rational Hodge conjecture for every complex CM abelian variety,",
             r"in every dimension and codimension (and all products and powers)",
             r"Consequences: Tate conjecture over finite fields; Hodge standard conjecture",
             r"Manuscript: 53 pages, produced by an OpenAI model"],
            False, r"\emph{The rational Hodge conjecture for CM abelian varieties} (Sept.\ 2026)")
        with self.say("A caveat. This fifty-three page proof has not been formalized, and it needs careful checking "
                      "by experts. {c}If it holds, the Hodge conjecture is now settled for every abelian variety with "
                      "complex multiplication, in every dimension.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("c")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
