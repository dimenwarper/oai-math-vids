import numpy as np
from manim import *

from style import *
from vo import NarratedScene

BOR = "[Borsuk](/bˈɔɹsʊk/)"
PAL3 = [BLUE_3B, YELLOW_3B, RED_3B]

# record dimensions of Borsuk counterexamples (year, dimension), as listed in the paper's history
RECORDS = [(1993, 1325), (1994, 946), (1997, 561), (2000, 560), (2002, 323), (2002, 321), (2003, 298),
           (2014, 65), (2014, 64), (2026, 63)]


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "156", r"Borsuk's Conjecture Fails in Dimension 9",
                          r"Lines in $\mathbb{R}^4$ that cannot be cut into ten smaller pieces")
        with self.say(f"Cutting shapes into smaller pieces: {BOR}'s conjecture."):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.4)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ diameter, disk, halves, thirds
        R = 1.6
        cL, cR = LEFT * 3.3 + DOWN * 0.5, RIGHT * 3.3 + DOWN * 0.5
        disk = Circle(R, color=BLUE_3B, fill_opacity=0.35).move_to(cL)
        dia = Line(cL + R * LEFT, cL + R * RIGHT, color=YELLOW_3B, stroke_width=5)
        dlab = Tex(r"diameter: the largest distance\\ between two points", font_size=30).next_to(disk, UP, buff=0.35)
        halves = VGroup(Sector(radius=R, start_angle=PI / 2, angle=PI, color=BLUE_3B, fill_opacity=0.45),
                        Sector(radius=R, start_angle=-PI / 2, angle=PI, color=GREEN_3B, fill_opacity=0.45))
        for h in halves:
            h.move_to(cR, aligned_edge=ORIGIN).shift(cR - h.get_arc_center())
        halves[0].shift(LEFT * 0.15)
        halves[1].shift(RIGHT * 0.15)
        bad = Line(cR + R * UP + LEFT * 0.15, cR + R * DOWN + LEFT * 0.15, color=RED_3B, stroke_width=5)
        bl = Tex(r"2 pieces: a piece still\\ has the full diameter", font_size=28, color=RED_3B).next_to(halves, DOWN,
                                                                                                      buff=0.3)
        thirds = VGroup(*[Sector(radius=R, start_angle=PI / 2 + k * TAU / 3, angle=TAU / 3, color=PAL3[k],
                                 fill_opacity=0.5, stroke_width=2) for k in range(3)])
        for k, t in enumerate(thirds):
            t.shift(cR - t.get_arc_center() + 0.15 * np.array([np.cos(PI / 2 + (k + 0.5) * TAU / 3),
                                                              np.sin(PI / 2 + (k + 0.5) * TAU / 3), 0]))
        a0, a1 = PI / 2, PI / 2 + TAU / 3
        sh = 0.15 * np.array([np.cos(a0 + TAU / 6), np.sin(a0 + TAU / 6), 0])
        chord = Line(cR + sh + R * np.array([np.cos(a0), np.sin(a0), 0]), cR + sh + R * np.array([np.cos(a1), np.sin(a1), 0]),
                     color=WHITE, stroke_width=4)
        tl = Tex(r"3 pieces: each strictly smaller\\ ($\sqrt3\,r < 2r$)", font_size=28, color=GREEN_3B).next_to(
            thirds, DOWN, buff=0.3)
        with self.say("The diameter of a shape is the largest distance between two of its points. "
                      "{cut}Suppose you want to cut a shape into pieces that are all strictly smaller, in this "
                      "sense. {two}For a disk, two pieces never suffice: one of them always contains two opposite "
                      "points, so it keeps the full diameter. {three}Three pieces do work.") as s:
            self.play(FadeIn(disk), Create(dia), FadeIn(dlab))
            s.wait_until("two")
            self.play(FadeIn(halves))
            self.play(Create(bad), FadeIn(bl))
            s.wait_until("three")
            self.play(FadeOut(VGroup(halves, bad, bl)), FadeIn(thirds))
            self.play(Create(chord), FadeIn(tl))
        self.play(FadeOut(VGroup(disk, dia, dlab, thirds, chord, tl)))

        # ------------------------------------------------------------ the conjecture
        tri_pts = [cL + 1.7 * np.array([np.cos(PI / 2 + k * TAU / 3), np.sin(PI / 2 + k * TAU / 3), 0]) for k in range(3)]
        tri = Polygon(*tri_pts, color=GREY_B, stroke_width=3)
        tri_d = VGroup(*[Dot(p, radius=0.12, color=c) for p, c in zip(tri_pts, PAL3)])
        trl = Tex(r"corners all at maximal distance:\\ at least 3 pieces", font_size=28).next_to(tri, DOWN, buff=0.35)
        conj = VGroup(Tex(rf"\textbf{{Borsuk, 1933:}}", font_size=34, color=YELLOW_3B),
                      Tex(r"can every bounded set in $\mathbb{R}^d$ be cut", font_size=32),
                      Tex(r"into $d+1$ pieces of smaller diameter?", font_size=32),
                      Tex(r"($d+1$ are needed for a regular simplex)", font_size=28, color=GREY_A),
                      Tex(r"true for $d=2$ and $d=3$", font_size=30, color=GREEN_3B)).arrange(DOWN, buff=0.2)
        conj.move_to(RIGHT * 2.7 + DOWN * 0.3)
        with self.say("A triangle with equal sides needs three as well: its corners are all at the maximal distance "
                      "from each other. In d dimensions, a regular simplex has d plus one such corners. "
                      f"{{q}}In 1933, Karol {BOR} asked whether d plus one pieces are always enough, for every bounded "
                      "set in d dimensions. {t}The answer is yes in the plane and in three-dimensional space.") as s:
            self.play(Create(tri), FadeIn(tri_d), FadeIn(trl))
            s.wait_until("q")
            self.play(FadeIn(conj[:4]), run_time=1.5)
            s.wait_until("t")
            self.play(FadeIn(conj[4]))
        self.play(FadeOut(VGroup(tri, tri_d, trl, conj)))

        # ------------------------------------------------------------ records
        ax = Axes(x_range=[1990, 2028, 5], y_range=[0.6, 3.6, 1], x_length=9.5, y_length=5.2, tips=False,
                  axis_config={"color": GREY_B}, x_axis_config={"include_numbers": True, "font_size": 24,
                                                                "decimal_number_config": {"group_with_commas": False,
                                                                                          "num_decimal_places": 0}}
                  ).shift(DOWN * 0.3 + RIGHT * 0.4)
        yt = VGroup(*[MathTex(str(v), font_size=26).next_to(ax.c2p(1990, np.log10(v)), LEFT, buff=0.15)
                      for v in (10, 100, 1000)])
        ytk = VGroup(*[Line(ax.c2p(1990, np.log10(v)) + LEFT * 0.08, ax.c2p(1990, np.log10(v)) + RIGHT * 0.08,
                            color=GREY_B) for v in (10, 100, 1000)])
        ylab = Tex("dimension of the smallest known counterexample (log scale)", font_size=26).next_to(
            ax, UP, buff=0.25).align_to(ax, LEFT)
        dots = VGroup(*[Dot(ax.c2p(y, np.log10(d)), radius=0.07, color=BLUE_3B) for y, d in RECORDS])
        steps = []
        for (y0, d0), (y1, d1) in zip(RECORDS, RECORDS[1:]):
            steps += [ax.c2p(y0, np.log10(d0)), ax.c2p(y1, np.log10(d0)), ax.c2p(y1, np.log10(d1))]
        stair = VMobject(color=BLUE_3B, stroke_width=3).set_points_as_corners(steps)
        kk = Tex(r"1993: Kahn--Kalai, 1325", font_size=26).next_to(dots[0], UP, buff=0.12).align_to(dots[0], LEFT)
        mid = Tex(r"spherical codes:\\ 323, 321, 298", font_size=26).next_to(dots[6], DR, buff=0.1)
        srg = Tex(r"2014: 65, 64", font_size=26).next_to(dots[7], LEFT, buff=0.2)
        g63 = Tex(r"May 2026: 63", font_size=26).next_to(dots[9], UP, buff=0.15).shift(LEFT * 0.4)
        new = Dot(ax.c2p(2026.4, np.log10(9)), radius=0.11, color=YELLOW_3B)
        newl = Tex(r"now: \textbf{9}", font_size=32, color=YELLOW_3B).next_to(new, LEFT, buff=0.2)
        drop = DashedLine(dots[9].get_center(), new.get_center(), color=YELLOW_3B)
        with self.say("For sixty years, no counterexample was found. {kk}Then, in 1993, Jeff Kahn and Gil "
                      "Kalai showed it fails in dimension thirteen hundred and twenty-five, and in all large dimensions. "
                      "{down}A race began to lower the dimension: below six hundred, then about three hundred using "
                      "spherical codes, {srg}then sixty-five and sixty-four in 2014, using strongly regular graphs, "
                      "{g}and sixty-three this May. {new}A manuscript in OpenAI's math catalogue now claims a "
                      "counterexample in dimension nine.") as s:
            self.play(Create(ax), FadeIn(yt), FadeIn(ytk), FadeIn(ylab), run_time=1.5)
            s.wait_until("kk")
            self.play(FadeIn(dots[0], scale=2), FadeIn(kk))
            s.wait_until("down")
            self.play(Create(stair), LaggedStart(*[FadeIn(d) for d in dots[1:]], lag_ratio=0.3), run_time=4)
            self.play(FadeIn(mid))
            s.wait_until("srg")
            self.play(FadeIn(srg))
            s.wait_until("g")
            self.play(FadeIn(g63))
            s.wait_until("new")
            self.play(Create(drop), FadeIn(new, scale=3), FadeIn(newl))
        self.play(FadeOut(VGroup(ax, yt, ytk, ylab, dots, stair, kk, mid, srg, g63, new, newl, drop)))

        # ------------------------------------------------------------ the theorem
        thm = VGroup(Tex(r"\textbf{Theorem.} Let $X=\{\,uu^{\mathsf T} : u\in\mathbb{R}^4,\ |u|=1\,\}$, inside the",
                         font_size=34),
                     Tex(r"9-dimensional space of trace-one symmetric $4\times4$ matrices.", font_size=34),
                     Tex(r"Then $\operatorname{diam} X=\sqrt2$, and $X$ cannot be covered by $10$ sets", font_size=34),
                     Tex(r"of diameter less than $\sqrt2$.", font_size=34)).arrange(DOWN, buff=0.2)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3)).to_edge(UP, buff=0.5)
        ex = MathTex(r"u=\tfrac15(1,2,2,4)\ \Rightarrow\ uu^{\mathsf T}=\frac1{25}\begin{pmatrix}1&2&2&4\\2&4&4&8\\"
                     r"2&4&4&8\\4&8&8&16\end{pmatrix}", font_size=36).shift(DOWN * 1.7 + LEFT * 2.2)
        exl = Tex(r"10 entries, trace $=1$:\\ 9 free dimensions", font_size=30, color=GREY_A).next_to(ex, RIGHT, buff=0.6)
        with self.say("Here is the claim. {t}Take every unit vector u in four dimensions, and form the four by four "
                      "matrix u times u transpose. {ex}Symmetric four by four matrices have ten independent entries; "
                      "these all have trace one, which leaves nine dimensions. {d}Measured with the ordinary "
                      "Euclidean distance on matrix entries, this set has diameter root two, and it cannot be cut into "
                      "ten pieces of smaller diameter. Nine plus one is ten, so Borsuk's bound fails.") as s:
            s.wait_until("t")
            self.play(Write(thm[0]), Create(tb[1]), run_time=2)
            s.wait_until("ex")
            self.play(Write(thm[1]), FadeIn(ex), run_time=1.5)
            self.play(FadeIn(exl))
            s.wait_until("d")
            self.play(Write(thm[2:]), run_time=2)
        self.play(FadeOut(VGroup(tb, ex, exl)))

        # ------------------------------------------------------------ lines <-> projectors, the 2-D picture
        oL = LEFT * 3.4 + DOWN * 0.7
        oR = RIGHT * 3.0 + DOWN * 0.7
        SC = 2.6  # screen units per matrix unit
        rc = SC / np.sqrt(2)
        th = ValueTracker(0.35)
        dirv = lambda a: np.array([np.cos(a), np.sin(a), 0])
        l1 = always_redraw(lambda: Line(oL - 2.0 * dirv(th.get_value()), oL + 2.0 * dirv(th.get_value()),
                                        color=BLUE_3B, stroke_width=5))
        l2 = always_redraw(lambda: Line(oL - 2.0 * dirv(th.get_value() + PI / 2), oL + 2.0 * dirv(th.get_value() + PI / 2),
                                        color=ORANGE_3B, stroke_width=5))
        circ = Circle(rc, color=GREY_B, stroke_width=2).move_to(oR)
        p1 = always_redraw(lambda: Dot(oR + rc * dirv(2 * th.get_value()), radius=0.1, color=BLUE_3B))
        p2 = always_redraw(lambda: Dot(oR + rc * dirv(2 * th.get_value() + PI), radius=0.1, color=ORANGE_3B))
        dd = always_redraw(lambda: DashedLine(oR + rc * dirv(2 * th.get_value()), oR + rc * dirv(2 * th.get_value() + PI),
                                              color=WHITE, stroke_width=2))
        dist = MathTex(r"\|uu^{\mathsf T}-vv^{\mathsf T}\|^2 = 2-2\cos^2\angle(u,v)", font_size=36).to_edge(UP, buff=0.45)
        far = Tex(r"farthest ($\sqrt2$) $\iff$ perpendicular lines", font_size=32, color=YELLOW_3B).next_to(dist, DOWN,
                                                                                                      buff=0.2)
        cl = Tex(r"lines in $\mathbb{R}^2$", font_size=30).next_to(oL + DOWN * 2.1, DOWN, buff=0.05)
        cr = Tex(r"their matrices: a circle", font_size=30).next_to(oR + DOWN * 2.1, DOWN, buff=0.05)
        with self.say("Why should this set be hard to cut? {l}A unit vector u spans a line through the origin, and u u "
                      "transpose is the matrix that projects onto that line. {d}The squared distance between two such "
                      "matrices is two, minus two times the squared cosine of the angle between the lines. "
                      "{far}So the farthest pairs, at distance root two, are exactly perpendicular lines. "
                      "{c}For lines in the plane, the matrices form a circle. As the line makes a half turn, its point "
                      "goes once around, {perp}and perpendicular lines land at opposite points.") as s:
            self.add(l1)
            self.play(Create(circ), FadeIn(cl), FadeIn(cr))
            s.wait_until("d")
            self.play(Write(dist))
            s.wait_until("far")
            self.play(FadeIn(far))
            s.wait_until("c")
            self.add(p1)
            self.play(th.animate.set_value(0.35 + PI), run_time=4, rate_func=linear)
            s.wait_until("perp")
            self.add(l2, p2, dd)
            self.play(th.animate.set_value(0.35 + PI + 0.9), run_time=2.5)
        # three arcs <-> three classes of lines
        th_final = 0.35 + PI + 0.9
        self.remove(l1, l2, p1, p2, dd)
        arcs = VGroup(*[Arc(radius=rc, start_angle=k * TAU / 3 + 0.04, angle=TAU / 3 - 0.08, arc_center=oR,
                            color=PAL3[k], stroke_width=10) for k in range(3)])
        fan = VGroup(*[Line(oL - 2.0 * dirv(a), oL + 2.0 * dirv(a), color=PAL3[int(a // (PI / 3)) % 3], stroke_width=3)
                       for a in np.arange(0, PI, PI / 30) + PI / 60])
        three = Tex(r"3 arcs, 3 classes of lines:\\ perpendicular lines never share a class", font_size=30).to_edge(
            DOWN, buff=0.25)
        three.add_background_rectangle(opacity=0.85, buff=0.1)
        up = Tex(r"lines in $\mathbb{R}^4$: a curved 3-dimensional set in $\mathbb{R}^9$", font_size=32,
                 color=TEAL_3B).move_to(three)
        up.add_background_rectangle(opacity=0.85, buff=0.1)
        with self.say("Three arcs, each less than half the circle, cover it. {three}That is three pieces, exactly "
                      "what Borsuk allows in two dimensions. Equivalently, three classes of lines, where "
                      "perpendicular lines never share a class. {up}For lines in four dimensions, the same matrices "
                      "fill a curved three-dimensional set sitting in nine dimensions.") as s:
            self.play(FadeOut(VGroup(cl, cr)), Create(arcs), FadeIn(fan), run_time=2)
            s.wait_until("three")
            self.play(FadeIn(three))
            s.wait_until("up")
            self.play(FadeOut(three), FadeIn(up))
        self.play(FadeOut(VGroup(arcs, fan, circ, dist, far, up)))

        # ------------------------------------------------------------ proof
        hdr = Tex("Why ten pieces cannot work", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.4)
        steps = VGroup(
            Tex(r"\textbf{1.} 10 smaller pieces $\Rightarrow$ a smooth ``fuzzy coloring'' of the lines of", font_size=30),
            Tex(r"\quad $\mathbb{R}^4$ by 10 colors; perpendicular lines never share a color", font_size=30),
            Tex(r"\textbf{2.} Extend to symmetric matrices: $F(A)=E(A_+)-E(A_-)$.", font_size=30),
            Tex(r"\quad $A_\pm$ live on perpendicular subspaces, so nothing cancels:", font_size=30),
            Tex(r"\quad an odd map from a 9-sphere to a 9-sphere", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(hdr, DOWN, buff=0.4)
        for k_ in (1, 3, 4):
            steps[k_].shift(RIGHT * 0.4)
        tbl = VGroup(
            VGroup(MathTex("k", font_size=34), MathTex("2", font_size=34), MathTex("3", font_size=34),
                   MathTex("4", font_size=34)),
            VGroup(Tex(r"colors forced", font_size=28), MathTex("3", font_size=34), MathTex("6", font_size=34),
                   MathTex("10", font_size=34, color=YELLOW_3B)),
            VGroup(Tex(r"Borsuk's $d+1$", font_size=28), MathTex("3", font_size=34), MathTex("6", font_size=34),
                   MathTex("10", font_size=34, color=YELLOW_3B)),
        )
        for r_, row in enumerate(tbl):
            for c_, m in enumerate(row):
                m.move_to(np.array([-1.8 + 1.5 * c_ + (0 if c_ else -0.6), -1.4 - 0.62 * r_, 0]))
        tlab = Tex(r"\textbf{3.} Borsuk--Ulam type count: lines in $\mathbb{R}^k$ need $\ge \tfrac{k(k+1)}{2}$ colors",
                   font_size=30).next_to(tbl, UP, buff=0.3)
        tlab.align_to(steps, LEFT)
        with self.say("So why can't ten pieces work? {fz}If they did, smoothing the pieces would give a fuzzy coloring "
                      "of all the lines in four dimensions, with ten colors, in which perpendicular lines never share a "
                      "color. {ext}The proof extends this coloring from lines to every symmetric matrix: split a "
                      "matrix into its positive and negative parts, which live on perpendicular subspaces, and "
                      "subtract their colors. Nothing cancels, {odd}and the result is an odd map from a nine-dimensional "
                      "sphere to a nine-dimensional sphere. {bu}A count in the spirit of the Borsuk Ulam theorem then "
                      "says that lines in k dimensions need at least k times k plus one, over two, colors: three in the "
                      "plane, six in three dimensions, {ten}and ten in four. Ten is exactly the threshold.") as s:
            self.play(Write(hdr))
            s.wait_until("fz")
            self.play(FadeIn(steps[0:2]))
            s.wait_until("ext")
            self.play(FadeIn(steps[2:4]))
            s.wait_until("odd")
            self.play(FadeIn(steps[4]))
            s.wait_until("bu")
            self.play(FadeIn(tlab), FadeIn(tbl[0]), FadeIn(tbl[1][:3]), FadeIn(tbl[2][:3]))
            s.wait_until("ten")
            self.play(FadeIn(tbl[1][3]), FadeIn(tbl[2][3]))
            self.play(Circumscribe(VGroup(tbl[1][3], tbl[2][3]), color=YELLOW_3B))
        self.play(FadeOut(VGroup(steps, tbl, tlab)))

        # rigidity at the threshold: six-label triangle systems
        rig = VGroup(Tex(r"\textbf{4.} At the threshold the odd map has odd degree. This forces:", font_size=30),
                     Tex(r"\quad every maximal set of colors on one line has exactly 4 colors,", font_size=30),
                     Tex(r"\quad and the 6 colors left out carry a rigid triangle system:", font_size=30)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(hdr, DOWN, buff=0.4)
        rig[1:].shift(RIGHT * 0.4)
        cen = [np.array([0.0, 0.0, 0])] + [0.6 * np.array([np.cos(PI / 2 + k * TAU / 5), np.sin(PI / 2 + k * TAU / 5), 0])
                                          for k in range(5)]
        lab_cols = [WHITE, BLUE_3B, TEAL_3B, GREEN_3B, YELLOW_3B, RED_3B]
        tris = [(0, i, (i % 5) + 1) for i in range(1, 6)]
        tris += [(i, ((i + 1) % 5) + 1, ((i + 2) % 5) + 1) for i in range(1, 6)]
        thumbs = VGroup()
        for T in tris:
            pts = [cen[t] for t in T]
            g = VGroup(Polygon(*pts, stroke_width=1.5, color=WHITE).set_fill(PURPLE_3B, 0.6),
                       *[Dot(cen[t], radius=0.07, color=lab_cols[t]) for t in range(6)])
            thumbs.add(g)
        thumbs.arrange_in_grid(rows=2, cols=5, buff=(0.7, 0.4)).shift(DOWN * 0.95)
        tri_note = Tex(r"10 triangles on 6 colors: one from each complementary pair,\\ every pair of colors in "
                       r"exactly two of them", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.3)
        fin = Tex(r"\textbf{5.} These patterns cannot fit together (a finite combinatorial argument).", font_size=30,
                  color=YELLOW_3B).next_to(thumbs, DOWN, buff=0.3)
        with self.say("At the threshold the odd map has odd degree, and that forces a rigid structure. {r1}Every "
                      "maximal set of colors used together on one line has exactly four colors. {r2}And the six colors "
                      "left out of each such set must form a rigid pattern: ten triangles, one from each complementary "
                      "pair, with every pair of colors in exactly two of them. {fin}Following these patterns from one "
                      "four-color set to its neighbors, a finite combinatorial argument reaches a contradiction. "
                      "So ten pieces are impossible.") as s:
            self.play(FadeIn(rig[0]))
            s.wait_until("r1")
            self.play(FadeIn(rig[1]))
            s.wait_until("r2")
            self.play(FadeIn(rig[2]), LaggedStart(*[FadeIn(t) for t in thumbs], lag_ratio=0.15), run_time=2.5)
            self.play(FadeIn(tri_note))
            s.wait_until("fin")
            self.play(FadeOut(tri_note), FadeIn(fin))
        self.play(FadeOut(VGroup(hdr, rig, thumbs, fin)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"The projectors $uu^{\mathsf T}$, $u\in\mathbb{R}^4$, form a set of diameter $\sqrt2$ in $\mathbb{R}^9$",
             r"It cannot be covered by 10 smaller sets; counterexamples in every $d\ge 9$",
             r"Manuscript: 18 pages, produced by an OpenAI model, not yet peer reviewed"],
            True, r"\mbox{\emph{A nine-dimensional counterexample to Borsuk's covering assertion} (Sept.\ 2026)}")
        with self.say("The manuscript is eighteen pages, written by an OpenAI model, and not yet peer reviewed. "
                      "Adding points gives counterexamples in every dimension from nine up. "
                      "{l}The main theorem has been formalized in the Lean proof assistant. The smallest dimension "
                      "where Borsuk's conjecture fails is still unknown: somewhere from four to nine.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
