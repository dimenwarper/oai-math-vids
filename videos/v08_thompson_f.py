import numpy as np
from manim import *

from style import *
from vo import NarratedScene

GEO = "[Geoghegan](/ɡˈAɡən/)"
FOL = "[Følner](/fˈɜlnəɹ/)"
BRO = "[Brouwer](/bɹˈWəɹ/)"

A_PTS = [(0, 0), (0.5, 0.25), (0.75, 0.5), (1, 1)]
B_PTS = [(0, 0), (0.5, 0.5), (0.75, 0.625), (0.875, 0.75), (1, 1)]


class Video(NarratedScene):
    def pl_graph(self, ax, pts, color):
        return VMobject(color=color, stroke_width=5).set_points_as_corners([ax.c2p(x, y) for x, y in pts])

    def bar(self, cuts, colors, width=5.0, height=0.45):
        g = VGroup()
        for (a, b), c in zip(zip(cuts, cuts[1:]), colors):
            g.add(Rectangle(width=(b - a) * width, height=height, stroke_color=BLACK, stroke_width=2)
                  .set_fill(c, 0.85).move_to(RIGHT * ((a + b) / 2 - 0.5) * width))
        return g

    def construct(self):
        card = title_card(self, "248", r"Thompson's Group $F$ Is Nonamenable",
                          r"Settling a 1979 conjecture of Geoghegan")
        with self.say("Thompson's group F is not amenable."):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ the group F
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 1, 0.25], x_length=4.2, y_length=4.2, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": False}).shift(LEFT * 4.2 + DOWN * 0.4)
        sq = Square(4.2, color=GREY_D).move_to(ax.c2p(0.5, 0.5))
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_D)
        gA = self.pl_graph(ax, A_PTS, BLUE_3B)
        gB = self.pl_graph(ax, B_PTS, YELLOW_3B)
        brk = VGroup(*[Dot(ax.c2p(x, y), radius=0.06, color=BLUE_3B) for x, y in A_PTS[1:-1]])
        ticks = VGroup(*[MathTex(t, font_size=26).next_to(ax.c2p(v, 0), DOWN, buff=0.12)
                         for t, v in [("0", 0), (r"\tfrac12", 0.5), (r"\tfrac34", 0.75), ("1", 1)]])
        rules = VGroup(
            Tex(r"$F$ = maps $[0,1]\to[0,1]$ that are", font_size=34),
            Tex(r"$\bullet$ increasing and piecewise linear", font_size=32),
            Tex(r"$\bullet$ with breakpoints at dyadic rationals $\tfrac{k}{2^n}$", font_size=32),
            Tex(r"$\bullet$ with slopes that are powers of 2", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
        b0 = self.bar([0, 0.5, 0.75, 1], [RED_3B, GREEN_3B, PURPLE_3B]).move_to(RIGHT * 3.2 + DOWN * 1.2)
        b1 = self.bar([0, 0.25, 0.5, 1], [RED_3B, GREEN_3B, PURPLE_3B]).move_to(RIGHT * 3.2 + DOWN * 2.4)
        arr = Arrow(b0.get_bottom(), b1.get_top(), buff=0.1, color=BLUE_3B)
        al = MathTex("A", font_size=34, color=BLUE_3B).next_to(arr, RIGHT, buff=0.1)
        with self.say("Here is a strange and beautiful group. {r}Its elements are maps from the interval zero to one "
                      "to itself, that are increasing and piecewise linear, with breakpoints at fractions like "
                      "a half, three quarters, five eighths, and slopes that are powers of two. "
                      "{a}This one, called A, squeezes the left half into the first quarter, and stretches the last "
                      "quarter onto the right half. {b}This one, B, does the same trick, but only on the right half. "
                      "{gr}Compose such maps, invert them, and you get Thompson's group F, introduced by Richard "
                      "Thompson in 1965.") as s:
            self.play(Create(ax), Create(sq), Create(diag), FadeIn(ticks))
            s.wait_until("r")
            self.play(LaggedStart(*[FadeIn(r) for r in rules], lag_ratio=0.4), run_time=3)
            s.wait_until("a")
            self.play(Create(gA), FadeIn(brk), run_time=1.5)
            self.play(FadeIn(b0))
            self.play(GrowArrow(arr), FadeIn(al), TransformFromCopy(b0, b1), run_time=1.5)
            s.wait_until("b")
            self.play(Create(gB), run_time=1.5)
            s.wait_until("gr")
            Fl = MathTex(r"F=\langle A,B\rangle", font_size=48, color=YELLOW_3B).next_to(ax, UP, buff=0.3)
            self.play(Write(Fl))
        self.play(FadeOut(VGroup(ax, sq, diag, gA, gB, brk, ticks, rules, b0, b1, arr, al, Fl)))

        # ------------------------------------------------------------ amenability: Z vs free group
        hdr = Tex(r"\textbf{Amenable}: has finite chunks that barely move when shifted", font_size=36,
                  color=YELLOW_3B).to_edge(UP, buff=0.4)
        line = VGroup(*[Dot(LEFT * 6 + RIGHT * 0.4 * k + UP * 1.2, radius=0.05, color=GREY_B) for k in range(16)])
        chunk = VGroup(*[line[k] for k in range(3, 13)])
        brA = SurroundingRectangle(chunk, color=BLUE_3B, buff=0.12)
        shifted = brA.copy().shift(RIGHT * 0.4).set_color(TEAL_3B)
        zl = Tex(r"$\mathbb{Z}$: a long interval shifted by 1\\ changes only 2 of its $N$ points", font_size=28).next_to(
            line, DOWN, buff=0.45)
        # free group tree
        def tree():
            g = VGroup()
            pts = {(): np.array([3.3, 0.6, 0])}
            dirs = [RIGHT, UP, LEFT, DOWN]
            frontier = [((), None)]
            for depth in range(4):
                new = []
                L = 1.25 * 0.52**depth
                for node, back in frontier:
                    for k, d in enumerate(dirs):
                        if back is not None and k == (back + 2) % 4:
                            continue
                        child = node + (k,)
                        pts[child] = pts[node] + d * L
                        g.add(Line(pts[node], pts[child], color=GREY_B, stroke_width=2.5 - 0.4 * depth))
                        new.append((child, k))
                frontier = new
            return g, pts
        tg, tp = tree()
        ball = VGroup(*[Dot(p, radius=0.06, color=BLUE_3B) for k, p in tp.items() if len(k) <= 2])
        bnd = VGroup(*[Dot(p, radius=0.06, color=RED_3B) for k, p in tp.items() if len(k) == 3])
        fl = Tex(r"free group: any finite chunk has a\\ boundary as big as itself", font_size=28).next_to(
            tg, DOWN, buff=0.3)
        with self.say("Now, a group is called amenable if it has finite chunks that barely change when you shift them. "
                      "{z}The integers are amenable: shift a long interval by one, and only two of its points change. "
                      "{fr}A free group, whose picture is an infinitely branching tree, is not: "
                      "any finite chunk has a boundary as large as the chunk itself. "
                      "{bt}This dichotomy, studied by von Neumann, is what lies behind the Banach Tarski paradox.") as s:
            self.play(Write(hdr))
            s.wait_until("z")
            self.play(FadeIn(line), Create(brA))
            self.play(TransformFromCopy(brA, shifted), FadeIn(zl), run_time=1.5)
            s.wait_until("fr")
            self.play(Create(tg), run_time=2)
            self.play(FadeIn(ball), FadeIn(bnd), FadeIn(fl))
        self.play(FadeOut(VGroup(hdr, line, brA, shifted, zl, tg, ball, bnd, fl)))

        # ------------------------------------------------------------ the question
        facts = VGroup(
            Tex(r"1979: Ross Geoghegan conjectures $F$ is \emph{not} amenable", font_size=34),
            Tex(r"$F$ contains no free subgroups (Brin--Squier, 1985)", font_size=32, color=GREY_A),
            Tex(r"$\Rightarrow$ the usual way to prove nonamenability is unavailable", font_size=32, color=GREY_A),
            Tex(r"claimed solutions in \emph{both} directions; several found flawed", font_size=32, color=RED_3B),
        ).arrange(DOWN, buff=0.4)
        with self.say(f"So is Thompson's group amenable? In 1979, Ross {GEO} conjectured that it is not. "
                      "{nf}The standard way to prove a group is not amenable is to find a free group inside it. "
                      "But Brin and Squier showed F has no free subgroups. "
                      "{cl}The problem became famous, with claimed proofs of both answers over the years, "
                      "several of which were found to contain errors.") as s:
            self.play(FadeIn(facts[0]))
            s.wait_until("nf")
            self.play(FadeIn(facts[1]))
            self.play(FadeIn(facts[2]))
            s.wait_until("cl")
            self.play(FadeIn(facts[3]))
        self.play(FadeOut(facts))

        thm = VGroup(Tex(r"\textbf{Theorem.} Thompson's group $F$ is not amenable.", font_size=44),
                     Tex(r"13 pages", font_size=30, color=GREY_A)).arrange(DOWN, buff=0.3)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.35))
        with self.say("A manuscript in OpenAI's math catalogue claims to settle it, in thirteen pages: "
                      "{t}F is not amenable. And the main theorem has been formalized in the Lean proof assistant.") as s:
            s.wait_until("t")
            self.play(Write(tb), run_time=2.5)
        self.play(FadeOut(tb))

        # ------------------------------------------------------------ Brouwer vs Benyamini–Sternfeld
        disk = Circle(radius=1.9, color=GREY_B).shift(LEFT * 3.4 + DOWN * 0.5)
        c = disk.get_center()
        fp = c + np.array([0.6, 0.3, 0])
        arrows = VGroup()
        for r in [0.6, 1.2, 1.7]:
            for t in np.linspace(0, TAU, int(8 * r), endpoint=False):
                p = c + r * np.array([np.cos(t), np.sin(t), 0])
                v = 0.45 * rotate_vector(p - fp, 0.9)
                q = p + v
                if np.linalg.norm(q - c) > 1.9:
                    q = c + (q - c) / np.linalg.norm(q - c) * 1.9
                arrows.add(Arrow(p, q, buff=0, stroke_width=2, color=BLUE_3B, max_tip_length_to_length_ratio=0.25))
        fpd = Dot(fp, color=YELLOW_3B, radius=0.09)
        bl = Tex(r"finite dimensions (Brouwer):\\ every continuous map of the ball\\ has a fixed point", font_size=28
                 ).next_to(disk, DOWN, buff=0.3)
        ball2 = Circle(radius=1.9, color=GREY_B).shift(RIGHT * 3.4 + DOWN * 0.5)
        c2 = ball2.get_center()
        rings = VGroup(*[Ellipse(width=3.8, height=3.8 * k, color=GREY_D, stroke_width=1.5).move_to(c2)
                         for k in (0.25, 0.55, 0.85)])
        arrows2 = VGroup()
        rng = np.random.default_rng(2)
        for _ in range(26):
            r = 1.7 * np.sqrt(rng.uniform(0.05, 1))
            t = rng.uniform(0, TAU)
            p = c2 + r * np.array([np.cos(t), np.sin(t), 0])
            d = rng.normal(size=2)
            d = d / np.linalg.norm(d) * 0.5
            arrows2.add(Arrow(p, p + np.array([d[0], d[1], 0]), buff=0, stroke_width=2, color=RED_3B,
                              max_tip_length_to_length_ratio=0.25))
        bsl = Tex(r"infinite-dimensional ball (Benyamini--Sternfeld):\\ a Lipschitz map moving \emph{every} point\\"
                  r" by at least $\delta$", font_size=28).next_to(ball2, DOWN, buff=0.3)
        hdr = Tex("The key tool: a map with no almost-fixed points", font_size=38, color=YELLOW_3B).to_edge(UP,
                                                                                                         buff=0.35)
        with self.say(f"The proof's key tool comes from geometry. {{br}}In finite dimensions, {BRO}'s theorem says "
                      "every continuous map from a ball to itself has a fixed point: some point that does not move. "
                      "{bs}In infinite dimensions that fails, badly. Benyamini and Sternfeld showed that the unit "
                      "ball of a Hilbert space has a well-behaved, Lipschitz map that moves every single point by at "
                      "least some fixed distance delta. There are not even approximately fixed points.") as s:
            self.play(Write(hdr))
            s.wait_until("br")
            self.play(Create(disk), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.02), run_time=2)
            self.play(FadeIn(fpd, scale=2), FadeIn(bl))
            s.wait_until("bs")
            self.play(Create(ball2), Create(rings), LaggedStart(*[GrowArrow(a) for a in arrows2], lag_ratio=0.03),
                      run_time=2)
            self.play(FadeIn(bsl))
        self.play(FadeOut(VGroup(disk, arrows, fpd, bl, ball2, rings, arrows2, bsl, hdr)))

        # ------------------------------------------------------------ recursive coloring
        hdr = Tex("Coloring dyadic partitions with points of the ball", font_size=38, color=YELLOW_3B).to_edge(
            UP, buff=0.35)
        W = 11
        base = Line(LEFT * W / 2, RIGHT * W / 2, color=GREY_B).shift(UP * 1.6)
        cuts = [0, 1 / 8, 1 / 4, 5 / 16, 3 / 8, 1 / 2, 9 / 16, 5 / 8, 3 / 4, 13 / 16, 7 / 8, 1]
        tk = VGroup(*[Line(UP * 0.15, DOWN * 0.15, color=WHITE).move_to(base.point_from_proportion(c)) for c in cuts])
        Tl = MathTex("T", font_size=36).next_to(base, LEFT, buff=0.2)
        parents = [(1 / 8, 1 / 4), (3 / 8, 1 / 2), (5 / 8, 3 / 4), (13 / 16, 7 / 8)]
        pcol = [BLUE_3B, TEAL_3B, GREEN_3B, ORANGE_3B]
        par = VGroup(*[Line(base.point_from_proportion(a), base.point_from_proportion(b), color=c, stroke_width=10)
                       for (a, b), c in zip(parents, pcol)])
        pl = Tex(r"$D$ fixed ``parent'' intervals", font_size=28).next_to(par, UP, buff=0.3)
        zooms = VGroup()
        for k, ((a, b), c) in enumerate(zip(parents, pcol)):
            zb = Line(LEFT * 1.1, RIGHT * 1.1, color=c, stroke_width=4).move_to(LEFT * 4.2 + RIGHT * 2.8 * k + UP * 0.1)
            inner = [x for x in cuts if a <= x <= b]
            zt = VGroup(*[Line(UP * 0.1, DOWN * 0.1).move_to(zb.point_from_proportion((x - a) / (b - a)))
                          for x in inner])
            col = Dot(zb.get_center() + DOWN * 0.7, radius=0.12, color=c)
            pt = MathTex(f"p(T_{{I_{k + 1}}})", font_size=26, color=c).next_to(col, DOWN, buff=0.12)
            zooms.add(VGroup(zb, zt, col, pt))
        avg = MathTex(r"p(T)", "=", r"f\Big(", r"\tfrac1D\sum_{j} p(T_{I_j})", r"\Big)", font_size=44).to_edge(
            DOWN, buff=0.5)
        avg[2].set_color(RED_3B)
        avg[4].set_color(RED_3B)
        with self.say("Here is how the proof uses it. {p}Take a partition of the interval into dyadic pieces. "
                      "{par}Fix a handful of parent intervals. {z}Zoom into each one, stretch it back to full size, "
                      "and you see a smaller partition, which by recursion already has a color: a point in the "
                      "Hilbert ball. {f}Average those colors, apply the Benyamini Sternfeld map f, and that is the "
                      "color of the original partition.") as s:
            self.play(Write(hdr))
            s.wait_until("p")
            self.play(Create(base), FadeIn(tk), FadeIn(Tl))
            s.wait_until("par")
            self.play(Create(par), FadeIn(pl))
            s.wait_until("z")
            self.play(LaggedStart(*[TransformFromCopy(p, z[0]) for p, z in zip(par, zooms)], lag_ratio=0.2),
                      run_time=1.5)
            self.play(*[FadeIn(z[1]) for z in zooms])
            self.play(*[FadeIn(z[2:]) for z in zooms])
            s.wait_until("f")
            self.play(Write(avg), run_time=2)
        self.play(FadeOut(VGroup(base, tk, Tl, par, pl, zooms)), avg.animate.next_to(hdr, DOWN, buff=0.4))

        # ------------------------------------------------------------ the contradiction
        chain = VGroup(
            Tex(r"Suppose $F$ were amenable: average over a nearly invariant chunk $A$.", font_size=32),
            Tex(r"$F$ can carry any pair of separated dyadic intervals onto any other pair,", font_size=32),
            Tex(r"so all averaged correlations between colors become nearly equal.", font_size=32),
            MathTex(r"\Rightarrow\quad z_i\approx m\ \ \text{for each parent}\quad\Rightarrow\quad f(m)\approx m",
                    font_size=40, color=YELLOW_3B),
            Tex(r"an almost-fixed point of $f$: impossible!", font_size=36, color=RED_3B),
        ).arrange(DOWN, buff=0.32).next_to(avg, DOWN, buff=0.6)
        with self.say("Now suppose F were amenable. {a}Average these colors over a chunk of the group that barely moves "
                      "when shifted. {c}Elements of F can carry any pair of separated dyadic intervals onto any other "
                      "pair, so after averaging, all the correlations between colors become nearly equal. "
                      "{z}That forces each parent's average color to sit near the overall mean m, and then f of m "
                      "is nearly m. {x}An almost-fixed point, which Benyamini and Sternfeld say cannot exist. "
                      "So F is not amenable.") as s:
            s.wait_until("a")
            self.play(FadeIn(chain[0]))
            s.wait_until("c")
            self.play(FadeIn(chain[1:3]), run_time=1.5)
            s.wait_until("z")
            self.play(Write(chain[3]), run_time=2)
            s.wait_until("x")
            self.play(FadeIn(chain[4], scale=1.1))
        self.play(FadeOut(VGroup(hdr, avg, chain)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Thompson's group $F$ admits no invariant mean: it is nonamenable",
             r"Confirms Geoghegan's 1979 conjecture",
             r"Manuscript: 13 pages, produced by an OpenAI model"],
            True, r"\emph{Thompson's group F is nonamenable} (Sept.\ 2026)")
        with self.say("After nearly fifty years and several false starts, the argument is short: thirteen pages, "
                      "written by an OpenAI model. {l}And because this problem has a history of flawed proofs, "
                      "the most reassuring part is this: the theorem has been formalized and checked in the Lean "
                      "proof assistant.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
