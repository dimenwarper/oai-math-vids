import numpy as np
from manim import *

from style import *
from vo import NarratedScene

U = 1.6  # screen length of one unit
PAL = [RED_3B, BLUE_3B, YELLOW_3B, GREEN_3B, PURPLE_3B, ORANGE_3B, TEAL_3B]


def spindle_points(center, unit=U):
    phi = 2 * np.arcsin(1 / (2 * np.sqrt(3)))
    pts = {"A": 0j}
    for side, rot in (("", -phi / 2), ("'", phi / 2)):
        r = np.exp(1j * (rot + PI / 2))
        pts["B" + side] = np.exp(-1j * PI / 6) * r
        pts["C" + side] = np.exp(1j * PI / 6) * r
        pts["D" + side] = np.sqrt(3) * r
    return {k: center + unit * np.array([v.real, v.imag, 0]) for k, v in pts.items()}


SP_EDGES = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D"),
            ("A", "B'"), ("A", "C'"), ("B'", "C'"), ("B'", "D'"), ("C'", "D'"), ("D", "D'")]


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "158", "The Plane Is Not 5-Colorable",
                          r"The Hadwiger--Nelson problem: now $\chi(\mathbb{R}^2)\in\{6,7\}$")
        with self.say("How many colors does the plane need?"):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ the rule
        plane = NumberPlane(background_line_style={"stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.5},
                            axis_config={"stroke_opacity": 0})
        p0 = np.array([-0.8, -0.3, 0])
        ang = ValueTracker(0.3)
        stick = always_redraw(lambda: Line(p0, p0 + U * np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0]),
                                           color=WHITE, stroke_width=5))
        e1 = Dot(p0, radius=0.12, color=RED_3B)
        e2 = always_redraw(lambda: Dot(stick.get_end(), radius=0.12, color=BLUE_3B))
        one = always_redraw(lambda: MathTex("1", font_size=36).move_to(
            stick.get_center() + 0.3 * rotate_vector(normalize(stick.get_end() - p0), PI / 2)))
        rule = Tex(r"Color every point of the plane so that\\ points at distance exactly 1 get different colors.",
                   font_size=38).to_edge(UP, buff=0.4)
        rule.add_background_rectangle(opacity=0.85, buff=0.15)
        with self.say("Here is a deceptively simple question from 1950. You want to paint every single point of "
                      "the plane, using as few colors as possible. {r}The one rule: any two points at distance "
                      "exactly one must get different colors. {s}Think of a stick of length one. "
                      "Wherever you drop it, however you turn it, its two ends must land on different colors. "
                      "{q}The smallest number of colors that works is called the chromatic number of the plane.") as s:
            self.play(FadeIn(plane), run_time=1)
            s.wait_until("r")
            self.play(FadeIn(rule))
            s.wait_until("s")
            self.play(Create(stick), FadeIn(e1), FadeIn(e2), FadeIn(one))
            self.play(ang.animate.set_value(0.3 + 2 * PI), run_time=4, rate_func=smooth)
            s.wait_until("q")
            chi = MathTex(r"\chi(\mathbb{R}^2)", "=", "?", font_size=56, color=YELLOW_3B).to_edge(DOWN, buff=0.5)
            chi.add_background_rectangle(opacity=0.85, buff=0.1)
            self.play(Write(chi))
        self.play(FadeOut(VGroup(rule, stick, e1, e2, one, chi)))

        # ------------------------------------------------------------ triangle & Moser spindle
        tri_c = LEFT * 4.3 + DOWN * 0.6
        tri = [tri_c + U * np.array([np.cos(a), np.sin(a), 0]) / np.sqrt(3) for a in (PI / 2, PI / 2 + TAU / 3,
                                                                                  PI / 2 + 2 * TAU / 3)]
        tri_e = VGroup(*[Line(tri[i], tri[(i + 1) % 3], color=GREY_B, stroke_width=3) for i in range(3)])
        tri_d = VGroup(*[Dot(p, radius=0.13, color=c) for p, c in zip(tri, PAL)])
        tri_l = Tex(r"$\Rightarrow$ at least 3", font_size=34).next_to(tri_e, DOWN, buff=0.5)
        with self.say("Three colors are certainly needed: {t}the corners of an equilateral triangle of side one "
                      "are all at distance one from each other.") as s:
            s.wait_until("t")
            self.play(Create(tri_e), LaggedStart(*[GrowFromCenter(d) for d in tri_d], lag_ratio=0.3), run_time=2)
            self.play(FadeIn(tri_l))

        P = spindle_points(RIGHT * 1.6 + DOWN * 2.9)
        sp_e = {e: Line(P[e[0]], P[e[1]], color=GREY_B, stroke_width=3) for e in SP_EDGES}
        sp_d = {k: Dot(v, radius=0.13, color=WHITE) for k, v in P.items()}
        sp_title = Tex(r"Moser spindle (1961): 7 points, 11 unit edges", font_size=32).next_to(
            VGroup(*sp_d.values()), UP, buff=0.35).shift(RIGHT * 0.8)
        cols = {"A": RED_3B, "B": BLUE_3B, "C": YELLOW_3B, "D": RED_3B, "B'": YELLOW_3B, "C'": BLUE_3B, "D'": RED_3B}
        with self.say("Three are not enough. {sp}This little graph, the Moser spindle, is made of four equilateral "
                      "triangles, glued into two diamonds, with their far tips exactly one apart. "
                      "{a}Try three colors. Color the bottom point red. {bc}Its two diamond neighbors must take "
                      "the other two colors, {d}which forces the far tip of the diamond back to red. "
                      "{d2}The same happens in the other diamond. {x}But the two red tips are at distance one. "
                      "So the plane needs at least four colors.") as s:
            s.wait_until("sp")
            self.play(Write(sp_title), *[Create(e) for e in sp_e.values()],
                      *[GrowFromCenter(d) for d in sp_d.values()], run_time=2.5)
            s.wait_until("a")
            self.play(sp_d["A"].animate.set_color(cols["A"]).scale(1.2))
            s.wait_until("bc")
            self.play(sp_d["B"].animate.set_color(cols["B"]), sp_d["C"].animate.set_color(cols["C"]))
            s.wait_until("d")
            self.play(sp_d["D"].animate.set_color(cols["D"]).scale(1.2), Indicate(sp_e[("B", "D")]),
                      Indicate(sp_e[("C", "D")]))
            s.wait_until("d2")
            self.play(sp_d["B'"].animate.set_color(cols["B'"]), sp_d["C'"].animate.set_color(cols["C'"]))
            self.play(sp_d["D'"].animate.set_color(cols["D'"]).scale(1.2))
            s.wait_until("x")
            self.play(sp_e[("D", "D'")].animate.set_color(RED_3B).set_stroke(width=8), Flash(sp_e[("D", "D'")],
                                                                                          color=RED_3B))
        spindle = VGroup(*sp_e.values(), *sp_d.values(), sp_title)
        self.play(FadeOut(VGroup(tri_e, tri_d, tri_l, spindle, plane)))

        # ------------------------------------------------------------ hexagonal 7-coloring
        r = 0.4 * U
        w = np.exp(2j * PI / 3)
        hexes, centers = VGroup(), []
        for a in range(-12, 13):
            for b in range(-12, 13):
                z = (a + b * w) * np.sqrt(3) * r
                if abs(z.real) > 8 or abs(z.imag) > 4.8:
                    continue
                c = np.array([z.real, z.imag, 0])
                centers.append((c, (a + 2 * b) % 7))
                hexes.add(RegularPolygon(6, start_angle=PI / 6, color=BLACK, stroke_width=1.5)
                          .scale(r).move_to(c).set_fill(PAL[(a + 2 * b) % 7], 0.75))
        cpos = np.array([c for c, _ in centers])

        def color_at(p):
            return PAL[centers[int(np.argmin(np.linalg.norm(cpos - p, axis=1)))][1]]

        q0 = ValueTracker(0)
        def stick_pts():
            t = q0.get_value()
            a = np.array([-1.5 + 2.2 * np.cos(0.7 * t), 0.4 * np.sin(1.3 * t), 0])
            return a, a + U * np.array([np.cos(1.1 * t + 0.4), np.sin(1.1 * t + 0.4), 0])
        st2 = always_redraw(lambda: Line(*stick_pts(), color=WHITE, stroke_width=6))
        d1 = always_redraw(lambda: Dot(stick_pts()[0], radius=0.13, color=color_at(stick_pts()[0]),
                                       stroke_color=WHITE, stroke_width=3).set_stroke(WHITE, 3, background=False))
        d2 = always_redraw(lambda: Dot(stick_pts()[1], radius=0.13, color=color_at(stick_pts()[1])).set_stroke(
            WHITE, 3))
        seven = Tex(r"7 colors suffice (Isbell, 1950)", font_size=40).to_edge(UP, buff=0.3)
        seven.add_background_rectangle(opacity=0.9, buff=0.15)
        with self.say("And seven are always enough. {h}Tile the plane with hexagons just under one unit across, "
                      "and color them in this repeating seven-color pattern. "
                      "{st}Two points in the same hexagon are closer than one, and same-colored hexagons are "
                      "farther than one apart. So the stick's ends never match.") as s:
            s.wait_until("h")
            self.play(LaggedStart(*[FadeIn(h) for h in hexes], lag_ratio=0.004), FadeIn(seven), run_time=2.5)
            s.wait_until("st")
            self.add(st2, d1, d2)
            self.play(q0.animate.set_value(9), run_time=7, rate_func=linear)
        self.play(FadeOut(VGroup(hexes, seven, st2, d1, d2)))

        # ------------------------------------------------------------ history line
        nums = VGroup(*[MathTex(str(k), font_size=64) for k in range(1, 8)]).arrange(RIGHT, buff=0.9).shift(UP * 0.4)
        chi_l = MathTex(r"\chi(\mathbb{R}^2)\in", font_size=50).next_to(nums, LEFT, buff=0.5)
        VGroup(chi_l, nums).move_to(UP * 0.4)

        def strike(k):
            return Line(nums[k - 1].get_corner(DL) + DL * 0.1, nums[k - 1].get_corner(UR) + UR * 0.1, color=RED_3B,
                        stroke_width=6)

        notes = VGroup(Tex(r"1950s: Nelson, Isbell, Hadwiger, Moser: $4\le\chi\le7$", font_size=32),
                       Tex(r"2018: de Grey, a 1581-point graph needing 5 colors (later 509 points)", font_size=32),
                       Tex(r"2026: OpenAI catalogue: $\chi\ge 6$", font_size=32, color=YELLOW_3B)
                       ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(DOWN, buff=0.6)
        with self.say("So the answer was somewhere from four to seven, and it stayed that way for almost seventy years. "
                      "{dg}In 2018, Aubrey de Grey, an amateur mathematician, found a graph of fifteen hundred and "
                      "eighty-one points that cannot be four-colored. The lower bound became five. "
                      "{now}Now, a manuscript in OpenAI's math catalogue claims the next step: {five}the plane cannot be "
                      "colored with five colors, no matter how wild the coloring is. "
                      "Only six and seven remain.") as s:
            self.play(FadeIn(chi_l), FadeIn(nums))
            self.play(*[Create(strike(k)) for k in (1, 2, 3)], FadeIn(notes[0]), run_time=1.5)
            s.wait_until("dg")
            self.play(Create(strike(4)), FadeIn(notes[1]), run_time=1.5)
            s.wait_until("five")
            self.play(Create(strike(5)), FadeIn(notes[2]), run_time=1.5)
            self.play(*[Circumscribe(nums[k], color=YELLOW_3B, shape=Circle) for k in (5, 6)])
        self.play(FadeOut(Group(*self.mobjects)))

        # ------------------------------------------------------------ no finite graph; transfer
        hdr = Tex("The twist: no graph is ever drawn", font_size=42, color=YELLOW_3B).to_edge(UP, buff=0.4)
        db = Tex(r"de Bruijn--Erd\H{o}s: if no 5-coloring exists,\\ some \emph{finite} unit-distance graph "
                 r"already needs 6 colors", font_size=32).next_to(hdr, DOWN, buff=0.4)
        rng = np.random.default_rng(5)
        n = 34
        noise = VGroup()
        for i in range(n):
            for j in range(n):
                noise.add(Square(0.13, stroke_width=0).set_fill(PAL[rng.integers(0, 5)], 0.9).move_to(
                    np.array([j * 0.13, -i * 0.13, 0])))
        noise.move_to(LEFT * 3.6 + DOWN * 1.3)
        # smooth version: 5 blobs
        xs = np.linspace(-1, 1, n)
        seeds = rng.uniform(-1, 1, (9, 2))
        sc = rng.integers(0, 5, 9)
        smooth_g = VGroup()
        for i in range(n):
            for j in range(n):
                p = np.array([xs[j], -xs[i]])
                k = int(np.argmin(np.linalg.norm(seeds - p, axis=1)))
                smooth_g.add(Square(0.13, stroke_width=0).set_fill(PAL[sc[k]], 0.9).move_to(
                    np.array([j * 0.13, -i * 0.13, 0])))
        smooth_g.move_to(RIGHT * 3.6 + DOWN * 1.3)
        arr = Arrow(noise.get_right(), smooth_g.get_left(), buff=0.3, color=WHITE)
        arr_l = Tex(r"average over algebraic\\ rotations \& translations;\\ Fourier rigidity", font_size=26).next_to(
            arr, UP, buff=0.15)
        nl = Tex("any coloring, however wild", font_size=28, color=GREY_A).next_to(noise, DOWN, buff=0.2)
        sl = Tex(r"a measurable coloring:\\ same-color unit pairs have measure zero", font_size=28,
                 color=GREY_A).next_to(smooth_g, DOWN, buff=0.2)
        with self.say("What is striking is how. {db}By a classic compactness theorem, if five colors fail, "
                      "some finite graph of points must already need six. But this proof never finds one. "
                      "{tr}Instead, it starts from any coloring at all, even one too wild to measure, "
                      "{avg}and averages it over algebraic rotations and translations. "
                      "A rigidity theorem in Fourier analysis, built on the [Furstenberg](/fˈɜɹstənbɜɹɡ/) Zimmer "
                      "structure theory, shows the wild part averages away. {m}What survives is an honest "
                      "measurable coloring in which same-colored unit pairs are vanishingly rare.") as s:
            self.play(Write(hdr))
            s.wait_until("db")
            self.play(FadeIn(db), run_time=1.5)
            s.wait_until("tr")
            self.play(FadeIn(noise), FadeIn(nl), run_time=1.5)
            s.wait_until("avg")
            self.play(GrowArrow(arr), FadeIn(arr_l))
            s.wait_until("m")
            self.play(TransformFromCopy(noise, smooth_g), FadeIn(sl), run_time=2.5)
        self.play(FadeOut(VGroup(hdr, db, noise, smooth_g, arr, arr_l, nl, sl)))

        # ------------------------------------------------------------ palettes and cycles
        hdr2 = Tex("Then: geometry around each point", font_size=42, color=YELLOW_3B).to_edge(UP, buff=0.4)
        cx = LEFT * 3.5 + DOWN * 0.5
        xd = Dot(cx, radius=0.1, color=WHITE)
        xl = MathTex("x", font_size=34).next_to(xd, DL, buff=0.1)
        arcs = VGroup(*[Arc(radius=U * 1.2, start_angle=a0, angle=TAU / 6, arc_center=cx,
                            color=[RED_3B, BLUE_3B][k % 2], stroke_width=10) for k, a0 in
                        enumerate(np.arange(0, TAU, TAU / 6) + 0.2)])
        pal_l = Tex(r"the \emph{palette} at $x$:\\ colors seen near the unit circle", font_size=30).next_to(
            arcs, DOWN, buff=0.3)
        two = Tex(r"almost every palette\\ has at most 2 colors", font_size=32, color=TEAL_3B).next_to(arcs, UP,
                                                                                                    buff=0.25)
        # K5 label graph
        k5c = RIGHT * 3.4 + DOWN * 0.2
        kp = [k5c + 1.7 * np.array([np.cos(PI / 2 + k * TAU / 5), np.sin(PI / 2 + k * TAU / 5), 0]) for k in range(5)]
        kd = VGroup(*[Dot(p, radius=0.17, color=PAL[k]) for k, p in enumerate(kp)])
        ke = VGroup(*[Line(kp[i], kp[j], color=GREY_D, stroke_width=2) for i in range(5) for j in range(i + 1, 5)])
        cyc = VGroup(*[Line(kp[i], kp[j], color=WHITE, stroke_width=6) for i, j in [(0, 1), (1, 3), (3, 0)]])
        kl = Tex(r"interfaces between colors\\ form a graph on the 5 labels", font_size=28).next_to(kd, DOWN, buff=0.35)
        with self.say("Now comes the geometry. {pal}Around each point x, look at which colors show up near the unit "
                      "circle, direction by direction. Call that the palette. {two}Because of the distance rule, "
                      "the proof shows that almost every palette uses at most two colors. "
                      "{k}So colors meet along interfaces, and those interfaces form a graph on the five labels. "
                      "{cyc}A topological argument forces a cycle of labels winding around some point.") as s:
            self.play(Write(hdr2))
            s.wait_until("pal")
            self.play(FadeIn(xd), FadeIn(xl), Create(arcs), FadeIn(pal_l), run_time=2.5)
            s.wait_until("two")
            self.play(FadeIn(two))
            s.wait_until("k")
            self.play(Create(ke), FadeIn(kd), FadeIn(kl), run_time=2)
            s.wait_until("cyc")
            self.play(Create(cyc), run_time=1.5)
        self.play(FadeOut(VGroup(xd, xl, arcs, pal_l, two, ke, kd, kl, cyc)))

        cases = VGroup()
        for L, txt, col in [(5, r"5-cycle: incompatible\\ angular patterns", RED_3B),
                            (4, r"4-cycle: an impossible\\ parity rule", RED_3B),
                            (3, r"3-cycle: a region with\\ only 3 colors\dots", YELLOW_3B)]:
            pts = [np.array([np.cos(PI / 2 + k * TAU / L), np.sin(PI / 2 + k * TAU / L), 0]) * 0.8 for k in range(L)]
            poly = Polygon(*pts, color=WHITE, stroke_width=4)
            dts = VGroup(*[Dot(p, radius=0.12, color=PAL[k]) for k, p in enumerate(pts)])
            t = Tex(txt, font_size=28, color=col).next_to(poly, DOWN, buff=0.35)
            cases.add(VGroup(poly, dts, t))
        cases.arrange(RIGHT, buff=0.9).shift(DOWN * 0.2 + LEFT * 1.3)
        xs_ = VGroup(*[Cross(c[0], stroke_color=RED_3B, stroke_width=6).scale(0.8) for c in cases[:2]])
        P2 = spindle_points(cases[2][0].get_center() + RIGHT * 2.6 + DOWN * 0.75, unit=0.62)
        mini = VGroup(*[Line(P2[a], P2[b], color=GREY_B, stroke_width=2) for a, b in SP_EDGES],
                      *[Dot(v, radius=0.06, color=WHITE) for v in P2.values()])
        with self.say("A cycle on five labels has length three, four, or five, and each case is ruled out. "
                      "{c5}A five-cycle produces angular color patterns that cannot fit together. "
                      "{c4}A four-cycle forces an impossible parity rule. "
                      "{c3}And a three-cycle leaves an open region using only three colors. "
                      "{ms}Inside that region, the proof places a Moser spindle, the same seven-point graph from 1961, "
                      "which needs four. Contradiction. Five colors are impossible.") as s:
            self.play(FadeIn(cases[0][:2]), FadeIn(cases[1][:2]), FadeIn(cases[2][:2]))
            s.wait_until("c5")
            self.play(FadeIn(cases[0][2]), Create(xs_[0]))
            s.wait_until("c4")
            self.play(FadeIn(cases[1][2]), Create(xs_[1]))
            s.wait_until("c3")
            self.play(FadeIn(cases[2][2]))
            s.wait_until("ms")
            self.play(Create(mini), run_time=2)
            x3 = Cross(cases[2][0], stroke_color=RED_3B, stroke_width=6).scale(0.8)
            self.play(Create(x3), Flash(mini, color=RED_3B))
        self.play(FadeOut(Group(*self.mobjects)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Every 5-coloring of the plane has two points at distance 1 with the same color",
             r"No regularity assumed on the colors; so $\chi(\mathbb{R}^2)\in\{6,7\}$",
             r"Manuscript: 62 pages, produced by an OpenAI model"],
            True, r"\emph{The Euclidean plane is not five-colorable} (Sept.\ 2026)")
        with self.say("Six or seven? That is still open. {c}The manuscript is sixty-two pages, written by an "
                      "OpenAI model, and its main theorem, that no five-coloring of the plane avoids "
                      "monochromatic unit pairs, {l}has been formalized in the Lean proof assistant.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
