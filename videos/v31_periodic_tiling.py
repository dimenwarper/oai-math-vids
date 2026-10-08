import numpy as np
from manim import *

from style import *
from vo import NarratedScene

BHAT = "[Bhattacharya](/bˌɑtəʧˈɑɹjə/)"
PAL5 = [BLUE_3B, YELLOW_3B, GREEN_3B, RED_3B, PURPLE_3B]
PLUS = {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (0, -1), 4: (-1, 0)}  # indexed by (x + 2y) mod 5


def plus_anchor(cx, cy):
    f = PLUS[(cx + 2 * cy) % 5]
    return cx - f[0], cy - f[1]


def lnz_digit(t, p):
    """Last nonzero base-p digit of t (f(0) = 1), the paper's model array."""
    if t == 0:
        return 1
    t = abs(t)
    while t % p == 0:
        t //= p
    return t % p


def iso(x, y, z, s=0.42):
    return np.array([(x - y) * np.cos(PI / 6) * s, (z - (x + y) * np.sin(PI / 6)) * s, 0])


def iso_cube(x, y, z, color, s=0.42):
    P = lambda a, b, c: iso(x + a, y + b, z + c, s)
    top = Polygon(P(0, 0, 1), P(1, 0, 1), P(1, 1, 1), P(0, 1, 1))
    left = Polygon(P(0, 1, 0), P(1, 1, 0), P(1, 1, 1), P(0, 1, 1))
    right = Polygon(P(1, 0, 0), P(1, 1, 0), P(1, 1, 1), P(1, 0, 1))
    g = VGroup(top, left, right)
    for face, op in zip(g, (0.95, 0.6, 0.35)):
        face.set_fill(color, op).set_stroke(BLACK, 1.2)
    return g


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "155", "A Tile That Never Repeats",
                          r"A counterexample to the periodic tiling conjecture in dimension three")
        with self.say("A shape that tiles space, but never periodically."):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.4)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ the plus tile and a periodic tiling
        S = 0.5
        cells = {}
        for cx in range(-17, 17):
            for cy in range(-11, 11):
                a = plus_anchor(cx, cy)
                i, j = (a[0] + 2 * a[1]) // 5, (2 * a[0] - a[1]) // 5
                sq = Square(S, stroke_width=1, stroke_color=BLACK).move_to(np.array([(cx + 0.5) * S, (cy + 0.5) * S, 0]))
                sq.set_fill(PAL5[(i + 2 * j) % 5], 0.8)
                cells[(cx, cy)] = (sq, a)
        grid = VGroup(*[Square(S, stroke_width=1, stroke_color=GREY_D).move_to(np.array([(cx + 0.5) * S, (cy + 0.5) * S, 0]))
                        for cx in range(-14, 14) for cy in range(-8, 8)])
        tiling = VGroup(*[sq for sq, _ in cells.values()])
        one = VGroup(*[cells[(c[0], c[1])][0].copy() for c in PLUS.values()]).set_fill(YELLOW_3B, 1)
        # a few individual copies, popping in
        anchors = sorted({a for _, a in cells.values() if abs(a[0]) <= 5 and abs(a[1]) <= 3},
                         key=lambda a: a[0] ** 2 + a[1] ** 2)
        groups = {}
        for (cx, cy), (sq, a) in cells.items():
            groups.setdefault(a, []).append(sq)
        first = VGroup(*[VGroup(*groups[a]) for a in anchors[1:9]])
        rest = VGroup(*[sq for a, sqs in groups.items() if a not in anchors[1:9] and a != (0, 0) for sq in sqs])
        def per_arrow(v):
            a = Arrow(ORIGIN, v * S, buff=0, color=WHITE, stroke_width=10, max_tip_length_to_length_ratio=0.35,
                      max_stroke_width_to_length_ratio=12).shift(np.array([0.5, 0.5, 0]) * S)
            return VGroup(a.copy().set_color(BLACK).set_stroke(width=16), a)
        b1 = per_arrow(np.array([1, 2, 0]))
        b2 = per_arrow(np.array([2, -1, 0]))
        lab = Tex(r"translates of one tile,\\ each cell covered once", font_size=32)
        lab.add_background_rectangle(opacity=0.85, buff=0.15).to_corner(UL, buff=0.3)
        with self.say("Here is a shape made of five grid squares: a plus sign. {t}Make copies of it, "
                      "and slide them around, with no rotating and no flipping, only shifting. "
                      "{f}These copies cover every square of the grid exactly once, so the plus sign is a "
                      "translational tile. {p}This tiling is also periodic: {s}shift the whole picture along "
                      "either of these two arrows, and it lands exactly on itself.") as s:
            self.play(FadeIn(grid), run_time=1)
            self.play(FadeIn(one, scale=1.3))
            s.wait_until("t")
            self.play(LaggedStart(*[FadeIn(g, shift=0.2 * DOWN) for g in first], lag_ratio=0.25), run_time=2.5)
            s.wait_until("f")
            self.play(FadeIn(rest), FadeIn(VGroup(*groups[(0, 0)])), FadeOut(one), FadeIn(lab), run_time=1.5)
            s.wait_until("s")
            self.remove(*tiling.submobjects)
            self.add(tiling, lab)
            self.play(FadeIn(b1[0]), FadeIn(b2[0]), GrowArrow(b1[1]), GrowArrow(b2[1]))
            self.play(tiling.animate.shift(np.array([1, 2, 0]) * S), run_time=1.5)
            self.play(tiling.animate.shift(np.array([2, -1, 0]) * S), run_time=1.5)
        self.play(FadeOut(VGroup(tiling, grid, b1, b2, lab)))

        # ------------------------------------------------------------ tile vs tiling: dominoes
        rng = np.random.default_rng(3)
        dom = VGroup()
        for r in range(-7, 7):
            off = int(rng.integers(0, 2))
            for k in range(-9, 9):
                x0 = (2 * k + off) * S
                dom.add(Rectangle(width=2 * S, height=S, stroke_color=BLACK, stroke_width=1.5)
                        .set_fill([BLUE_3B, TEAL_3B][(k + r) % 2], 0.75).move_to(np.array([x0 + S, (r + 0.5) * S, 0])))
        q = VGroup(Tex(r"\textbf{Periodic tiling conjecture}", font_size=38, color=YELLOW_3B),
                   Tex(r"If a finite set of cells tiles by translations,\\ does it have a \emph{periodic} tiling?",
                       font_size=34)).arrange(DOWN, buff=0.25)
        qb = VGroup(BackgroundRectangle(q, fill_opacity=0.92, buff=0.3), q)
        with self.say("One tile can have many tilings. {d}Rows of dominoes can each slide on their own, giving "
                      "tilings that never repeat, although the domino also tiles periodically. "
                      "{q}The periodic tiling conjecture asks: if a finite shape tiles by translations at all, must "
                      "at least one of its tilings be periodic? The shape may be any finite set of cells, even a "
                      "disconnected one, in any dimension. Lagarias and Wang stated a version explicitly in 1996.") as s:
            s.wait_until("d")
            self.play(LaggedStart(*[FadeIn(d) for d in dom], lag_ratio=0.002), run_time=2)
            for r in (3, 8, 10):
                row = VGroup(*dom[r * 18:(r + 1) * 18])
                self.play(row.animate.shift(RIGHT * S), run_time=0.6)
            s.wait_until("q")
            self.play(FadeIn(qb))
        self.play(FadeOut(VGroup(dom, qb)))

        # ------------------------------------------------------------ history
        hdr = Tex("What was known", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.4)
        # 1-D picture: tile {0,2}, copies at 0,1 + 4Z
        line_cells = VGroup()
        for kk in range(12):
            a = kk - 2 if (kk % 4) >= 2 else kk
            line_cells.add(Square(0.36, stroke_width=1.5, stroke_color=BLACK)
                           .set_fill(PAL5[(a // 4 * 2 + a % 4) % 5], 0.85).move_to(RIGHT * 0.36 * kk))
        tile1d = MathTex(r"\{0,2\}", font_size=30)
        rows = VGroup(
            Tex(r"\textbf{1 dimension:} always periodic (Newman, 1977)", font_size=32),
            Tex(rf"\textbf{{2 dimensions:}} always a periodic tiling (Bhattacharya, 2016/2020)", font_size=32),
            Tex(r"\textbf{2022:} Greenfeld and Tao: false in some very high dimension", font_size=32, color=RED_3B),
            Tex(r"\textbf{3, 4, 5, \dots:} unknown", font_size=32, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).shift(DOWN * 0.3 + LEFT * 1.2)
        line_cells.next_to(rows[0], RIGHT, buff=0.5)
        tile1d.next_to(line_cells, UP, buff=0.12)
        with self.say("On the line, the answer is yes. {n}Donald Newman showed in 1977 that every tiling of the "
                      f"integers by a finite tile repeats. {{b}}In the plane, Siddhartha {BHAT} proved that every "
                      "finite tile of the square grid has a periodic tiling. {gt}Then, in 2022, Rachel Greenfeld and "
                      "Terence Tao found a counterexample, in some very high dimension. {gap}That left every "
                      "dimension in between.") as s:
            self.play(Write(hdr))
            s.wait_until("n")
            self.play(FadeIn(rows[0]), FadeIn(tile1d), LaggedStart(*[FadeIn(c) for c in line_cells], lag_ratio=0.1),
                      run_time=2)
            s.wait_until("b")
            self.play(FadeIn(rows[1]))
            s.wait_until("gt")
            self.play(FadeIn(rows[2]))
            s.wait_until("gap")
            self.play(FadeIn(rows[3]))
        self.play(FadeOut(VGroup(hdr, rows, line_cells, tile1d)))

        # ------------------------------------------------------------ theorem
        thm = VGroup(Tex(r"\textbf{Theorem.} There is a finite set $T\subset\mathbb{Z}^3$ that tiles $\mathbb{Z}^3$",
                         font_size=34),
                     Tex(r"by translations, but no tiling by $T$ is periodic.", font_size=34),
                     Tex(r"The cubes $T+[0,1]^3$ tile $\mathbb{R}^3$, never periodically, even with real shifts.",
                         font_size=30, color=GREY_A)).arrange(DOWN, buff=0.22)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3)).to_edge(UP, buff=0.5)
        cubes = VGroup()
        spots = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (3, 0, 0), (3, 1, 0), (0, 3, 0), (2, 2, 1), (1, 3, 0),
                 (3, 3, 0), (3, 3, 1)]
        for (x, y, z) in sorted(spots, key=lambda p: (p[0] + p[1], p[2])):
            cubes.add(iso_cube(x, y, z, TEAL_3B))
        cubes.scale(1.35).move_to(DOWN * 1.5 + LEFT * 3)
        cl = Tex(r"(a cartoon: the real tile is\\ finite, but far too large to draw)", font_size=28, color=GREY_A)
        cl.next_to(cubes, RIGHT, buff=0.7)
        least = Tex(r"for grid tiles, three is the\\ smallest possible dimension", font_size=32, color=TEAL_3B).next_to(cl, DOWN, buff=0.4)
        with self.say("A manuscript in OpenAI's math catalogue closes the gap at its lowest rung. "
                      "{t}It constructs a finite set of cells, T, in three dimensions, that tiles by translations, "
                      "{np}but no tiling by it is periodic: none is unchanged by shifts in three independent "
                      "directions. {r}Thickening each cell into a solid cube gives the same result in ordinary space, "
                      "even when copies may be shifted by arbitrary real amounts. "
                      "{m}And since finite tiles on the integer line and on the square grid always have periodic "
                      "tilings, three is the smallest possible dimension for tiles on a grid.") as s:
            s.wait_until("t")
            self.play(Write(thm[0]), Create(tb[1]), run_time=2)
            self.play(LaggedStart(*[FadeIn(c, shift=0.2 * DOWN) for c in cubes], lag_ratio=0.1), FadeIn(cl),
                      run_time=2)
            s.wait_until("np")
            self.play(Write(thm[1]))
            s.wait_until("r")
            self.play(FadeIn(thm[2]))
            s.wait_until("m")
            self.play(FadeIn(least))
        self.play(FadeOut(VGroup(tb, cubes, cl, least)))

        # ------------------------------------------------------------ the Sudoku and its line rule
        p, N = 3, 9
        H = 0.4
        rows_shown = list(range(1, 15))
        strip = VGroup()
        cellmap = {}
        for n in range(N):
            for k, m in enumerate(rows_shown):
                d = lnz_digit(m, p)
                c = Square(H, stroke_width=1.5, stroke_color=BLACK).set_fill([BLUE_3B, YELLOW_3B][d - 1], 0.75)
                c.move_to(np.array([n * H, -k * H, 0]))
                t = MathTex(str(d), font_size=24, color=BLACK).move_to(c)
                strip.add(VGroup(c, t))
                cellmap[(n, m)] = c
        strip.move_to(LEFT * 4.2 + DOWN * 0.35)
        dots_top = MathTex(r"\vdots", font_size=30).next_to(strip, UP, buff=0.08)
        dots_bot = MathTex(r"\vdots", font_size=30).next_to(strip, DOWN, buff=0.08)
        cols = Tex(r"$N=p^2$ columns", font_size=28).next_to(dots_top, UP, buff=0.05)
        hdr = Tex(r"Step 1: a Sudoku that cannot repeat", font_size=38, color=YELLOW_3B).to_corner(UR, buff=0.45)
        rule = VGroup(
            Tex(r"Each cell: a nonzero digit mod a prime $p$", font_size=30),
            Tex(r"Along every line of integer slope, the digits", font_size=30),
            Tex(r"read like the last nonzero base-$p$ digit of $an+b$", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(hdr, DOWN, buff=0.4).align_to(hdr, RIGHT)
        e0 = 3
        line_cells_ = [cellmap[(n, e0 + n)] for n in range(N) if (e0 + n) in rows_shown]
        hl = VGroup(*[SurroundingRectangle(c, color=WHITE, buff=0, stroke_width=4) for c in line_cells_])
        word = MathTex(*[str(lnz_digit(e0 + n, p)) for n in range(N)], font_size=36).arrange(RIGHT, buff=0.22)
        word.next_to(rule, DOWN, buff=0.45)
        wl = Tex(r"$=$ last nonzero base-3 digit of $n+3$", font_size=28, color=GREY_A).next_to(word, DOWN, buff=0.2)
        ill = Tex(r"illustration: $p=3$ (the proof takes $p>200$)", font_size=26, color=GREY_B).to_corner(DR, buff=0.4)
        with self.say("How can a tile be forced never to repeat? {gt}The proof follows the strategy of Greenfeld and "
                      "Tao: build a kind of Sudoku puzzle whose solutions exist, but can never repeat, and then encode "
                      "the puzzle in a tile. {st}Take a strip, a fixed number of columns wide and infinitely tall, "
                      "and write a nonzero digit, mod a prime p, in every cell. {rule}The rule: along every straight "
                      "line of integer slope, the digits you read must look like the last nonzero digit, in base p, "
                      "of a linear function, a n plus b.") as s:
            self.play(Write(hdr))
            s.wait_until("st")
            self.play(LaggedStart(*[FadeIn(c) for c in strip], lag_ratio=0.004), FadeIn(dots_top), FadeIn(dots_bot),
                      FadeIn(cols), FadeIn(ill), FadeIn(rule[0]), run_time=2)
            s.wait_until("rule")
            self.play(FadeIn(rule[1:]))
            self.play(Create(hl), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(w, shift=0.2 * UP) for w in word], lag_ratio=0.15), FadeIn(wl), run_time=1.5)

        # one column, self-similar
        colH = 0.215
        col = VGroup()
        for m in range(1, 28):
            d = lnz_digit(m, p)
            c = Rectangle(width=0.5, height=colH, stroke_width=1, stroke_color=BLACK).set_fill(
                [BLUE_3B, YELLOW_3B][d - 1], 0.85)
            c.move_to(DOWN * (m - 1) * colH)
            col.add(c)
        col.move_to(RIGHT * 0.2 + DOWN * 0.35)
        col_l = Tex(r"one column,\\ rows $1$--$27$", font_size=26).next_to(col, LEFT, buff=0.3).align_to(col, UP)
        picks = VGroup(*[col[m - 1] for m in range(3, 28, 3)])
        marks = VGroup(*[SurroundingRectangle(c, color=WHITE, buff=0.0, stroke_width=3) for c in picks])
        sub = VGroup(*[c.copy() for c in picks])
        sub_target = VGroup(*[col[m - 1].copy() for m in range(1, 10)]).next_to(col, RIGHT, buff=1.4).align_to(col, UP)
        top9 = VGroup(SurroundingRectangle(VGroup(*col[:9]), color=TEAL_3B, buff=0.04, stroke_width=3),
                      SurroundingRectangle(sub_target, color=TEAL_3B, buff=0.04, stroke_width=3))
        same = Tex(r"every 3rd row\\ $=$ the column itself", font_size=28, color=TEAL_3B).next_to(sub_target, RIGHT,
                                                                                                  buff=0.3)
        with self.say("A solution exists: {sol}in every column, write the last nonzero base p digit of the row "
                      "number. {np}But this column never settles into a repeating cycle. {self}Keep only every p-th "
                      "row, and you get the whole column back. That self-similarity is the engine of the proof.") as s:
            self.play(FadeOut(VGroup(hl, word, wl, rule)))
            s.wait_until("sol")
            self.play(FadeIn(col), FadeIn(col_l), run_time=1.5)
            s.wait_until("self")
            self.play(Create(marks), run_time=1)
            self.play(Transform(sub, sub_target), run_time=1.5)
            self.play(Create(top9), FadeIn(same))

        desc = VGroup(
            Tex(r"Suppose a solution with no constant column", font_size=30),
            Tex(r"repeats vertically; take its smallest period $M$.", font_size=30),
            Tex(r"The rule forces $p \mid M$.", font_size=30),
            Tex(r"Keep every $p$-th row (after a normalization):", font_size=30),
            Tex(r"still a solution, period $M/p<M$.", font_size=30),
            Tex(r"Contradiction: \textbf{no solution repeats.}", font_size=32, color=YELLOW_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        with self.say("Now suppose some solution, with no constant column, did repeat vertically, and take its "
                      "smallest period, M. {div}The rule forces M to be a multiple of p. {keep}Keep only every p-th "
                      "row. After a normalization, what remains still obeys the rule, still has no constant column, "
                      "{per}but it repeats with period M over p. That's smaller than the smallest period. "
                      "{c}So no solution can ever repeat.") as s:
            self.play(FadeOut(VGroup(sub, same, top9, marks, strip, dots_top, dots_bot, cols)))
            self.play(VGroup(col, col_l).animate.shift(LEFT * 3.2))
            desc.next_to(col, RIGHT, buff=1.0).shift(UP * 0.2)
            self.play(FadeIn(desc[0:2]))
            s.wait_until("div")
            self.play(FadeIn(desc[2]))
            s.wait_until("keep")
            self.play(FadeIn(desc[3]))
            s.wait_until("per")
            self.play(FadeIn(desc[4]))
            s.wait_until("c")
            self.play(FadeIn(desc[5]))
        self.play(FadeOut(VGroup(desc, col, col_l, ill, hdr)))

        # ------------------------------------------------------------ from puzzle to one tile
        hdr = Tex(r"Step 2: from the puzzle to one tile", font_size=38, color=YELLOW_3B).to_edge(UP, buff=0.4)
        labels = [r"Sudoku\\ (never repeats)", r"tiling equations\\ in $\mathbb{Z}^2\times$ cyclic",
                  r"one tile in\\ $\mathbb{Z}^2\times\mathbb{Z}/Q\mathbb{Z}$", r"one tile $T\subset\mathbb{Z}^3$\\ and its cubes"]
        boxes = VGroup()
        for L, c in zip(labels, [BLUE_3B, TEAL_3B, GREEN_3B, YELLOW_3B]):
            t = Tex(L, font_size=28)
            b = RoundedRectangle(width=2.75, height=1.35, corner_radius=0.15, color=c, stroke_width=3)
            boxes.add(VGroup(b, t))
        boxes.arrange(RIGHT, buff=0.55).shift(UP * 1.4)
        fwd = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.06, color=WHITE, stroke_width=4)
                       for i in range(3)])
        back = CurvedArrow(boxes[3].get_bottom() + DOWN * 0.1, boxes[0].get_bottom() + DOWN * 0.1, angle=-PI / 5,
                           color=RED_3B)
        back_l = Tex(r"a periodic tiling would decode into a repeating Sudoku", font_size=28, color=RED_3B).next_to(
            back, DOWN, buff=0.1)
        # quotient picture: layers of Z^2 with the third coordinate wrapped mod Q
        Q = 5
        layers = VGroup()
        for z in range(Q):
            pts = [np.array([-1.3, -0.35, 0]), np.array([0.7, -0.35, 0]), np.array([1.3, 0.35, 0]), np.array([-0.7, 0.35, 0])]
            lay = Polygon(*pts, stroke_color=[BLUE_3B, TEAL_3B, GREEN_3B, YELLOW_3B, ORANGE_3B][z], stroke_width=2.5)
            lay.set_fill([BLUE_3B, TEAL_3B, GREEN_3B, YELLOW_3B, ORANGE_3B][z], 0.18).shift(UP * 0.38 * z)
            layers.add(lay)
        layers.move_to(LEFT * 2.6 + DOWN * 2.4)
        wrap = CurvedArrow(layers[-1].get_left() + LEFT * 0.1, layers[0].get_left() + LEFT * 0.1, angle=PI * 0.8,
                           color=WHITE)
        qmap = MathTex(r"\mathbb{Z}^3 \to \mathbb{Z}^2\times\mathbb{Z}/Q\mathbb{Z}", font_size=36).next_to(layers, RIGHT,
                                                                                                     buff=1.0).shift(UP * 0.35)
        eqs = VGroup(MathTex(r"A\oplus F_1 = A\oplus F_2 = \cdots = A\oplus F_s = \mathbb{Z}^2\times V", font_size=38),
                     Tex(r"the same unknown set of shifts $A$; \ $V$ a finite group, kept \emph{cyclic}", font_size=30,
                         color=GREY_A)).arrange(DOWN, buff=0.2).move_to(DOWN * 0.2)
        qmap2 = MathTex(r"(x,y,z)\mapsto (x,\,y,\,z \bmod Q)", font_size=32, color=GREY_A).next_to(qmap, DOWN, buff=0.2)
        with self.say("Next, the puzzle becomes geometry. {eq}Each rule turns into a tiling equation: some shapes "
                      "must tile, all using the same unknown set of shifts. These shapes live in the plane times a "
                      "finite group. {cyc}The new step is keeping that finite group cyclic, by building it from "
                      "factors of pairwise coprime prime orders. {why}That matters because the plane times a cyclic "
                      "group is a quotient of the three-dimensional grid: just wrap the third direction around. "
                      "{st}The equations are then stacked into a single tile, {lift}and lifted to one tile in three "
                      "dimensions, with a rigidity argument that also handles solid cubes shifted by real amounts. "
                      "{back}Run backwards, any periodic tiling would decode into a repeating Sudoku solution, "
                      "which cannot exist.") as s:
            self.play(Write(hdr), FadeIn(boxes[0]))
            s.wait_until("eq")
            self.play(GrowArrow(fwd[0]), FadeIn(boxes[1]))
            self.play(Write(eqs[0]))
            s.wait_until("cyc")
            self.play(FadeIn(eqs[1]))
            s.wait_until("why")
            self.play(Create(layers), run_time=1.5)
            self.play(Create(wrap), Write(qmap), FadeIn(qmap2))
            s.wait_until("st")
            self.play(GrowArrow(fwd[1]), FadeIn(boxes[2]))
            s.wait_until("lift")
            self.play(GrowArrow(fwd[2]), FadeIn(boxes[3]))
            s.wait_until("back")
            self.play(FadeOut(VGroup(layers, wrap, qmap, qmap2, eqs)))
            self.play(Create(back), FadeIn(back_l), run_time=1.5)
        self.play(FadeOut(VGroup(hdr, boxes, fwd, back, back_l)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"A finite tile $T\subset\mathbb{Z}^3$ tiles by translations, but never periodically",
             r"Same for the cubes $T+[0,1]^3$ in $\mathbb{R}^3$; three is the least lattice dimension",
             r"Manuscript: 26 pages, produced by an OpenAI model, not yet peer reviewed"],
            True, r"\emph{A translational tile with no fully periodic tiling in dimension three} (Sept.\ 2026)")
        with self.say("The manuscript is twenty-six pages, written by an OpenAI model, and not yet peer reviewed. "
                      "{l}Its main theorem, a three-dimensional tile with no periodic tiling, has been formalized in "
                      "the Lean proof assistant. So the periodic tiling conjecture fails in dimension three, which, "
                      "for tiles on a grid, is the lowest dimension where it could fail.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
