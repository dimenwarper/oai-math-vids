import numpy as np
from manim import *

from style import *
from vo import NarratedScene

K = 5
LCOL = [BLUE_3B, YELLOW_3B, RED_3B, GREEN_3B, PURPLE_3B]
POS = {"A": (-4.6, 0.9), "B": (-2.6, 2.1), "C": (-0.2, 1.6), "D": (2.2, 2.3), "E": (4.5, 1.0),
       "F": (-3.5, -1.6), "G": (-0.4, -1.1), "H": (2.9, -1.5)}
EDGES = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("A", "F"), ("F", "G"), ("G", "H"), ("H", "E"),
         ("B", "G"), ("C", "G"), ("D", "H")]
TRUE = {"A": 0, "B": 3, "C": 1, "D": 4, "E": 2, "F": 2, "G": 0, "H": 3}
BFS = [("A", "B"), ("A", "F"), ("B", "C"), ("B", "G"), ("C", "D"), ("G", "H"), ("D", "E")]


def pos(v, shift=DOWN * 0.4):
    x, y = POS[v]
    return np.array([x, y, 0]) + shift


class Video(NarratedScene):
    def make_graph(self, consts):
        edges, tags = {}, {}
        for u, v in EDGES:
            ln = Line(pos(u), pos(v), color=GREY_B, stroke_width=3)
            mid = (pos(u) + pos(v)) / 2
            normal = rotate_vector(normalize(pos(v) - pos(u)), PI / 2) * 0.28
            tag = MathTex(f"+{consts[(u, v)]}", font_size=28, color=GREY_A).move_to(mid + normal)
            edges[(u, v)], tags[(u, v)] = ln, tag
        verts = {v: Circle(radius=0.32, color=WHITE, stroke_width=3).set_fill(BLACK, 1).move_to(pos(v))
                 for v in POS}
        return edges, tags, verts

    def label(self, v, val):
        c = Circle(radius=0.32, color=LCOL[val], stroke_width=4).set_fill(LCOL[val], 0.35).move_to(pos(v))
        return VGroup(c, MathTex(str(val), font_size=34).move_to(pos(v)))

    def construct(self):
        card = title_card(self, "102", "The Unique Games Conjecture",
                          r"Proved: a 3SAT-to-Unique-Games reduction with completeness $1-\varepsilon$")
        with self.say("The Unique Games Conjecture."):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ the game
        consts = {(u, v): (TRUE[v] - TRUE[u]) % K for u, v in EDGES}
        edges, tags, verts = self.make_graph(consts)
        rule = MathTex(r"\text{label}(v)", r"=", r"\text{label}(u)", r"+", r"c", r"\pmod 5",
                       font_size=40).to_edge(UP, buff=0.35)
        rule[4].set_color(YELLOW_3B)
        with self.say("Here is a puzzle. Every dot gets a label, one of five values. "
                      "{e}Each edge carries a rule: the label on one end must equal the label on the other end, "
                      "plus some shift, counted modulo five. "
                      "{u}The rules are unique: once you know the label at one end of an edge, "
                      "there is exactly one label that works at the other end.") as s:
            self.play(LaggedStart(*[GrowFromCenter(c) for c in verts.values()], lag_ratio=0.1), run_time=1.5)
            s.wait_until("e")
            self.play(LaggedStart(*[Create(e) for e in edges.values()], lag_ratio=0.08),
                      LaggedStart(*[FadeIn(t) for t in tags.values()], lag_ratio=0.08), Write(rule), run_time=3)
            s.wait_until("u")
            e0 = edges[("A", "B")]
            self.play(e0.animate.set_color(YELLOW_3B).set_stroke(width=6), run_time=0.6)
            la = self.label("A", 0)
            self.play(FadeIn(la), run_time=0.8)
            lb = self.label("B", 3)
            self.play(TransformFromCopy(la, lb), run_time=1.2)
            self.play(e0.animate.set_color(GREY_B).set_stroke(width=3), FadeOut(la), FadeOut(lb), run_time=0.6)

        # ------------------------------------------------------------ easy case: propagate
        labs = {}
        with self.say("If every rule can be satisfied at once, the puzzle is easy. "
                      "{g}Guess a label for one dot, and let the rules propagate it along the edges. "
                      "{c}Either everything checks out, or you try the next guess. "
                      "Five guesses, and you are done.") as s:
            s.wait_until("g")
            labs["A"] = self.label("A", 0)
            self.play(FadeIn(labs["A"], scale=1.3))
            for u, v in BFS:
                labs[v] = self.label(v, TRUE[v])
                self.play(edges[(u, v)].animate.set_color(GREEN_3B), TransformFromCopy(labs[u], labs[v]),
                          run_time=0.55)
            s.wait_until("c")
            rest = [e for e in EDGES if e not in BFS]
            self.play(*[edges[e].animate.set_color(GREEN_3B) for e in rest], run_time=1)
            chk = Tex(r"all 11 rules satisfied \checkmark", color=GREEN_3B, font_size=36).to_edge(DOWN, buff=0.35)
            self.play(Write(chk))
        self.play(FadeOut(chk), *[FadeOut(l) for l in labs.values()],
                  *[e.animate.set_color(GREY_B) for e in edges.values()])

        # ------------------------------------------------------------ hard case
        bad = ("C", "G")
        new_tag = MathTex("+2", font_size=28, color=RED_3B).move_to(tags[bad])
        with self.say("Now corrupt just a few of the rules, so that only ninety-nine percent of them "
                      "can be satisfied together. {p}Propagation breaks: a single bad edge sends a wrong label "
                      "down a whole branch, and you cannot tell which edges to distrust. "
                      "{ugc}In 2002, Subhash [Khot](/kˈOt/) conjectured that this is not a failure of cleverness, "
                      "but a wall. For any small error you like, with enough labels, it is NP-hard "
                      "to tell a puzzle where ninety-nine percent of the rules can be satisfied "
                      "from one where barely one percent can.") as s:
            self.play(Transform(tags[bad], new_tag))
            s.wait_until("p")
            order = [("A", "B"), ("A", "F"), ("B", "C"), ("C", "G"), ("C", "D"), ("G", "H"), ("D", "E")]
            wrong = dict(TRUE)
            wrong["G"] = (TRUE["C"] + 2) % K
            wrong["H"] = (wrong["G"] + consts[("G", "H")]) % K
            labs = {"A": self.label("A", 0)}
            self.play(FadeIn(labs["A"]), run_time=0.5)
            for u, v in order:
                labs[v] = self.label(v, wrong[v])
                col = RED_3B if (u, v) == bad else GREEN_3B
                self.play(edges[(u, v)].animate.set_color(col), TransformFromCopy(labs[u], labs[v]), run_time=0.45)
            fails = [e for e in EDGES if (wrong[e[1]] - wrong[e[0]]) % K != (consts[e] if e != bad else 2)]
            oks = [e for e in EDGES if e not in fails and e not in order]
            self.play(*[edges[e].animate.set_color(RED_3B) for e in fails],
                      *[edges[e].animate.set_color(GREEN_3B) for e in oks], run_time=1)
            s.wait_until("ugc")
            graph = VGroup(*edges.values(), *tags.values(), *verts.values(), *labs.values())
            self.play(FadeOut(rule), graph.animate.scale(0.5).to_corner(UL, buff=0.3), run_time=1.2)
            yes = VGroup(Tex(r"\textbf{YES}", color=GREEN_3B), Tex(r"$\ge 99\%$ of rules\\satisfiable",
                                                                    font_size=34)).arrange(DOWN)
            no = VGroup(Tex(r"\textbf{NO}", color=RED_3B), Tex(r"$\le 1\%$ of rules\\satisfiable",
                                                              font_size=34)).arrange(DOWN)
            yb = VGroup(yes, caption_box(yes, GREEN_3B, 0.35)).move_to(LEFT * 2.8 + DOWN * 0.6)
            nb = VGroup(no, caption_box(no, RED_3B, 0.35)).move_to(RIGHT * 2.8 + DOWN * 0.6)
            vs = Tex(r"NP-hard to\\tell apart", font_size=34, color=YELLOW_3B).move_to(DOWN * 0.6)
            hdr = Tex(r"\textbf{Unique Games Conjecture} (Khot, 2002)", font_size=40).to_corner(UR, buff=0.5)
            self.play(Write(hdr), FadeIn(yb, shift=RIGHT), FadeIn(nb, shift=LEFT), run_time=2)
            self.play(Write(vs))
        self.play(FadeOut(VGroup(graph, yb, nb, vs, hdr)))

        # ------------------------------------------------------------ why it matters: max-cut
        rng = np.random.default_rng(3)
        angs = np.sort(rng.uniform(0, TAU, 9))
        circ = Circle(radius=2.0, color=GREY_B, stroke_width=2).shift(LEFT * 3.3 + DOWN * 0.4)
        vecs = VGroup(*[Arrow(circ.get_center(), circ.get_center() + 2.0 * np.array([np.cos(a), np.sin(a), 0]),
                              buff=0, stroke_width=3, color=BLUE_3B, max_tip_length_to_length_ratio=0.12)
                        for a in angs])
        cut_line = DashedLine(circ.get_center() + 2.6 * np.array([np.cos(1.1), np.sin(1.1), 0]),
                              circ.get_center() - 2.6 * np.array([np.cos(1.1), np.sin(1.1), 0]), color=YELLOW_3B)
        mc_title = Tex(r"\textbf{Max-Cut}: split the vertices to cut as many edges as possible", font_size=34)
        mc_title.to_edge(UP, buff=0.35)
        gw = VGroup(Tex("Goemans--Williamson (1995):", font_size=34),
                    MathTex(r"\alpha_{GW}\approx 0.878", font_size=44, color=BLUE_3B),
                    Tex(r"vectors on a sphere,\\ cut by a random hyperplane", font_size=30, color=GREY_A)
                    ).arrange(DOWN, buff=0.25).move_to(RIGHT * 3 + UP * 0.8)
        ugc_mc = Tex(r"UGC $\Rightarrow$ beating $0.878$ is NP-hard", font_size=36, color=YELLOW_3B).next_to(
            gw, DOWN, buff=0.6)
        with self.say("Why care? Because a huge number of optimization problems hinge on it. "
                      "{mc}Take Max-Cut: split a network in two, cutting as many links as possible. "
                      "{gw}In 1995, [Goemans](/ɡˈOmənz/) and Williamson found a beautiful algorithm: "
                      "place the vertices as vectors on a sphere, then slice with a random plane. "
                      "It always gets within eighty-seven point eight percent of the best cut. "
                      "{opt}If the Unique Games Conjecture is true, that strange constant is exactly optimal: "
                      "doing any better is NP-hard.") as s:
            s.wait_until("mc")
            self.play(Write(mc_title), run_time=1.5)
            s.wait_until("gw")
            self.play(Create(circ), LaggedStart(*[GrowArrow(v) for v in vecs], lag_ratio=0.1), FadeIn(gw[0]),
                      run_time=2)
            self.play(Create(cut_line))
            n = np.array([np.cos(1.1 + PI / 2), np.sin(1.1 + PI / 2), 0])
            self.play(*[v.animate.set_color(RED_3B if np.dot(v.get_end() - circ.get_center(), n) > 0 else BLUE_3B)
                        for v in vecs], Write(gw[1]), FadeIn(gw[2]), run_time=1.5)
            s.wait_until("opt")
            self.play(Write(ugc_mc))
        self.play(FadeOut(VGroup(circ, vecs, cut_line, mc_title, gw, ugc_mc)))

        rows = [("Max-Cut", r"$0.878$", "Goemans--Williamson"),
                ("Vertex Cover", r"factor $2$", "take both ends of any edge"),
                ("Max 2-SAT, Min-UnCut, \\dots", "fixed thresholds", "semidefinite rounding"),
                ("every constraint problem", "Raghavendra's SDP", "one algorithm for all")]
        table = VGroup()
        for i, (a, b, c) in enumerate(rows):
            r = VGroup(Tex(a, font_size=32), Tex(b, font_size=32, color=BLUE_3B),
                       Tex(c, font_size=28, color=GREY_A))
            r[0].move_to(LEFT * 3.9 + DOWN * i * 0.8)
            r[1].move_to(RIGHT * 0.2 + DOWN * i * 0.8)
            r[2].move_to(RIGHT * 4.0 + DOWN * i * 0.8)
            table.add(r)
        hdrs = VGroup(Tex(r"\textbf{problem}", font_size=30), Tex(r"\textbf{simple algorithm}", font_size=30),
                      Tex(r"\textbf{how}", font_size=30))
        for h, x in zip(hdrs, [-3.9, 0.2, 4.0]):
            h.move_to(RIGHT * x + UP * 0.9)
        tbl = VGroup(hdrs, table).move_to(UP * 0.3)
        verdict = Tex(r"UGC true $\Rightarrow$ all of these are \emph{exactly optimal}", font_size=38,
                      color=YELLOW_3B).to_edge(DOWN, buff=0.6)
        with self.say("The same story repeats across the field. "
                      "{vc}Vertex cover, where the naive factor two is best possible. "
                      "{csp}And for every constraint satisfaction problem at once, Prasad [Raghavendra](/ɹɑɡəvˈɛndɹə/) "
                      "showed that one semidefinite program would be the optimal algorithm. "
                      "{v}For twenty years these were theorems with an asterisk: true, if the conjecture is true.") as s:
            self.play(FadeIn(hdrs), FadeIn(table[0]))
            s.wait_until("vc")
            self.play(FadeIn(table[1]))
            self.play(FadeIn(table[2]))
            s.wait_until("csp")
            self.play(FadeIn(table[3]))
            s.wait_until("v")
            self.play(Write(verdict))
        self.play(FadeOut(VGroup(tbl, verdict)))

        # ------------------------------------------------------------ halfway: 2-to-2
        nl = NumberLine(x_range=[0, 1, 0.25], length=10, include_numbers=True, font_size=28,
                        decimal_number_config={"num_decimal_places": 2}).shift(DOWN * 0.3)
        nl_lab = Tex("completeness: fraction of rules satisfiable in YES instances", font_size=32).next_to(
            nl, UP, buff=1.2)
        m18 = Triangle(color=BLUE_3B, fill_opacity=1).scale(0.15).rotate(PI).next_to(nl.n2p(0.5), UP, buff=0.05)
        l18 = Tex(r"2018: Khot--Minzer--Safra\\ (2-to-2 Games Theorem)", font_size=28, color=BLUE_3B).next_to(
            m18, UP, buff=0.15)
        goal = Triangle(color=YELLOW_3B, fill_opacity=1).scale(0.15).rotate(PI).next_to(nl.n2p(0.99), UP, buff=0.05)
        lgoal = Tex(r"the conjecture:\\ $1-\varepsilon$", font_size=28, color=YELLOW_3B).next_to(goal, UP, buff=0.15)
        with self.say("Then, in 2018, came a breakthrough. "
                      "{kms}[Khot](/kˈOt/), [Minzer](/mˈɪnzəɹ/), and [Safra](/sˈɑfɹə/) proved the 2-to-2 games theorem. "
                      "As a consequence, they got the Unique Games hardness gap, but only for puzzles where "
                      "about half the rules can be satisfied. "
                      "{g}The conjecture needs puzzles where almost all of them can. "
                      "Closing that gap, from one half to one, has been the open problem since.") as s:
            self.play(Create(nl), FadeIn(nl_lab))
            s.wait_until("kms")
            self.play(FadeIn(m18, shift=DOWN * 0.3), Write(l18), run_time=2)
            s.wait_until("g")
            self.play(FadeIn(goal, shift=DOWN * 0.3), Write(lgoal))
            gap = Line(nl.n2p(0.5), nl.n2p(0.99), color=RED_3B, stroke_width=8)
            self.play(Create(gap), run_time=1.5)
        self.play(FadeOut(VGroup(nl, nl_lab, m18, l18, goal, lgoal, gap)))

        # ------------------------------------------------------------ the theorem
        thm = VGroup(
            Tex(r"\textbf{Theorem.} For all fixed $\varepsilon,\delta\in(0,\tfrac12)$ there is a", font_size=36),
            Tex(r"deterministic polynomial-time reduction from 3SAT to Unique Games:", font_size=36),
            MathTex(r"\varphi\ \text{satisfiable}\ \Rightarrow\ \mathrm{val}\ge 1-\varepsilon, \qquad"
                    r"\varphi\ \text{unsatisfiable}\ \Rightarrow\ \mathrm{val}\le\delta", font_size=38),
        ).arrange(DOWN, buff=0.3)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3))
        with self.say("A new manuscript in OpenAI's math catalogue claims to close it. "
                      "{t}It gives an explicit, deterministic, polynomial-time reduction from 3SAT to Unique Games, "
                      "where satisfiable formulas become puzzles with value at least one minus epsilon, "
                      "and unsatisfiable ones, at most delta. That is the Unique Games Conjecture, proved.") as s:
            s.wait_until("t")
            self.play(Write(tb), run_time=4)
        self.play(tb.animate.scale(0.6).to_edge(UP, buff=0.2))

        # ------------------------------------------------------------ the 1/2 barrier: rank-one kicks
        rng = np.random.default_rng(7)
        Mv = rng.integers(0, 2, (4, 5))
        a = np.array([1, 0, 1, 1])
        lv = np.array([0, 1, 1, 0, 1])
        z = np.array([1, 1, 0, 1, 0])

        def grid(Mat, hl=None, cs=0.42):
            g = VGroup()
            for i in range(Mat.shape[0]):
                for j in range(Mat.shape[1]):
                    sq = Square(cs, stroke_width=1.5, stroke_color=GREY_B)
                    sq.set_fill(BLUE_3B if Mat[i, j] else BLACK, 0.8 if Mat[i, j] else 1)
                    if hl is not None and hl[i, j]:
                        sq.set_stroke(YELLOW_3B, 3)
                    sq.move_to(np.array([j * cs, -i * cs, 0]))
                    g.add(sq)
            return g

        def colvec(v, cs=0.42, color=TEAL_3B):
            return VGroup(*[Square(cs, stroke_width=1.5, stroke_color=GREY_B).set_fill(color if b else BLACK, 0.85)
                            .move_to(np.array([0, -i * cs, 0])) for i, b in enumerate(v)])

        G0 = grid(Mv).move_to(LEFT * 4.2 + DOWN * 0.6)
        Ml = MathTex("M", font_size=40).next_to(G0, UP)
        zrow = VGroup(*[MathTex(str(b), font_size=28, color=YELLOW_3B if b else GREY_B).next_to(G0[15 + j], DOWN, buff=0.12)
                        for j, b in enumerate(z)])
        zl = MathTex("z=", font_size=30, color=YELLOW_3B).next_to(zrow, LEFT, buff=0.15)
        ans = colvec(Mv @ z % 2).next_to(G0, RIGHT, buff=0.9)
        al = MathTex("Mz", font_size=36).next_to(ans, UP)
        arr1 = Arrow(G0.get_right(), ans.get_left(), buff=0.1, color=GREY_B)
        with self.say("To see where the difficulty lies, look at the test at the heart of the 2018 approach. "
                      "{m}A prover's honest answer is encoded by a binary matrix M, and a question z reads off "
                      "the answer M times z: add up the chosen columns, mod two. "
                      "{k}The test kicks the matrix by a random rank-one matrix, a times l transpose, "
                      "and checks that the answer did not change.") as s:
            s.wait_until("m")
            self.play(FadeIn(G0), Write(Ml), FadeIn(zrow), Write(zl), run_time=1.5)
            self.play(GrowArrow(arr1), FadeIn(ans), Write(al), run_time=1.5)
            s.wait_until("k")
            kick = np.outer(a, lv)
            G1 = grid((Mv + kick) % 2, hl=kick).move_to(RIGHT * 1.6 + DOWN * 0.6)
            M1l = MathTex(r"M+a\,l^{\top}", font_size=40).next_to(G1, UP)
            arr2 = Arrow(G0.get_right() + RIGHT * 2.6 + DOWN * 1.5, G1.get_left() + DOWN * 0.3, buff=0.1,
                         color=YELLOW_3B)
            self.play(TransformFromCopy(G0, G1), Write(M1l), run_time=2)
        ans1 = colvec((Mv + np.outer(a, lv)) @ z % 2).next_to(G1, RIGHT, buff=0.9)
        a1l = MathTex("(M+al^{\\top})z", font_size=34).next_to(ans1, UP)
        arr3 = Arrow(G1.get_right(), ans1.get_left(), buff=0.1, color=GREY_B)
        eq = MathTex(r"(M+a\,l^{\top})z", r"=", r"Mz", r"+", r"a\,(l^{\top}z)", font_size=40).to_edge(DOWN, buff=0.4)
        eq[4].set_color(RED_3B)
        coin = Tex(r"$l^{\top}z$ is a fair coin $\Rightarrow$ the honest answer survives only half the time",
                   font_size=32, color=RED_3B).next_to(eq, UP, buff=0.25)
        with self.say("But the honest answer moves. {eq}It shifts by a, times l dot z, "
                      "{coin}and l dot z is a fair coin flip. So even a perfectly honest prover fails half the time. "
                      "That is the one-half barrier, in miniature.") as s:
            self.play(GrowArrow(arr3), FadeIn(ans1), Write(a1l), run_time=1.5)
            s.wait_until("eq")
            self.play(Write(eq), run_time=2)
            s.wait_until("coin")
            self.play(FadeIn(coin, shift=UP * 0.2))
        self.play(FadeOut(VGroup(G0, Ml, zrow, zl, ans, al, arr1, G1, M1l, ans1, a1l, arr3, eq, coin)))

        # ------------------------------------------------------------ the fix: latent noise + nonlinear map
        box = RoundedRectangle(width=2.6, height=1.6, corner_radius=0.2, color=TEAL_3B).shift(UP * 0.2)
        cl = MathTex("C", font_size=60, color=TEAL_3B).move_to(box)
        inp = MathTex(r"x+a", font_size=44).next_to(box, LEFT, buff=1.4)
        out = MathTex(r"C(x)", font_size=44, color=GREEN_3B).next_to(box, RIGHT, buff=1.4)
        a1 = Arrow(inp.get_right(), box.get_left(), buff=0.15)
        a2 = Arrow(box.get_right(), out.get_left(), buff=0.15)
        p1 = MathTex(r"\Pr\big[C(x+a)\neq C(x)\big]\le p", font_size=38, color=GREEN_3B)
        p1n = Tex("honest answers barely notice the noise", font_size=30, color=GREEN_3B)
        p2 = Tex(r"but any cheater using many independent \emph{linear} observations\\"
                 r"still detects the noise at least $1/8$ of the time", font_size=30, color=RED_3B)
        props = VGroup(VGroup(p1, p1n).arrange(DOWN, buff=0.15), p2).arrange(DOWN, buff=0.45).to_edge(DOWN, buff=0.4)
        with self.say("The new proof keeps the same matrix test, but changes the noise. "
                      "{c}It builds a special nonlinear map, C, out of quadratic blocks over a finite field, "
                      "together with a carefully designed noise distribution. "
                      "{p1}Honest answers, passed through C, survive the kick almost always. "
                      "{p2}But any cheating strategy built from enough linear structure still sees the noise, "
                      "at least one time in eight. Completeness goes up to one minus epsilon, "
                      "without opening the door to cheaters.") as s:
            s.wait_until("c")
            self.play(Create(box), Write(cl), FadeIn(inp), GrowArrow(a1), run_time=1.5)
            self.play(GrowArrow(a2), FadeIn(out), run_time=1)
            s.wait_until("p1")
            self.play(Write(p1), FadeIn(p1n), run_time=2)
            s.wait_until("p2")
            self.play(FadeIn(p2, shift=UP * 0.2), run_time=1.5)
        self.play(FadeOut(VGroup(box, cl, inp, out, a1, a2, props)))

        # ------------------------------------------------------------ soundness: two incompatible bounds
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 1, 0.5], x_length=6, y_length=3.6, tips=False,
                  axis_config={"color": GREY_B}).shift(RIGHT * 3.2 + DOWN * 1.0)
        xl = MathTex("k", font_size=32).next_to(ax.x_axis, RIGHT, buff=0.1)
        gam = ax.plot(lambda k: 0.3, color=GREEN_3B)
        dec = ax.plot(lambda k: np.exp(-0.9 * k ** (1 / 1.4)), x_range=[0.01, 10], color=RED_3B)
        gl = MathTex(r"\ge\gamma", font_size=32, color=GREEN_3B).next_to(ax.c2p(10, 0.3), UP, buff=0.1)
        dl = MathTex(r"\le e^{-c k^{1/3}}", font_size=32, color=RED_3B).next_to(ax.c2p(2.2, 0.35), UR, buff=0.05)
        left = VGroup(
            Tex(r"Suppose a cheater passes $99\%$ of tests", font_size=30),
            Tex(r"on a \emph{false} formula. Then:", font_size=30),
            Tex(r"\textbf{1.} Grassmann expansion (KMS 2018) $+$", font_size=28, color=GREEN_3B),
            Tex(r"Fourier decoding $\Rightarrow$ strategies agreeing $\ge\gamma$", font_size=28, color=GREEN_3B),
            Tex(r"\textbf{2.} parallel repetition (Dinur--Steurer) $\Rightarrow$", font_size=28, color=RED_3B),
            Tex(r"every strategy agrees $\le e^{-ck^{1/3}}$", font_size=28, color=RED_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(LEFT, buff=0.5).shift(DOWN * 0.7)
        with self.say("Soundness is a squeeze. Suppose some labeling passes ninety-nine percent of the tests, "
                      "even though the original formula is unsatisfiable. "
                      "{one}Using the Grassmann expansion theorem from 2018, plus Fourier decoding, "
                      "the proof extracts strategies that agree a fixed fraction of the time. "
                      "{two}But a parallel repetition bound says every strategy for a false formula "
                      "agrees exponentially rarely, as the tuple length k grows. "
                      "{x}For large k, both cannot hold. So cheaters cannot pass.") as s:
            self.play(FadeIn(left[:2]), run_time=1.5)
            s.wait_until("one")
            self.play(FadeIn(left[2:4]), Create(ax), FadeIn(xl), Create(gam), FadeIn(gl), run_time=2)
            s.wait_until("two")
            self.play(FadeIn(left[4:]), Create(dec), FadeIn(dl), run_time=2)
            s.wait_until("x")
            xm = Cross(scale_factor=0.25, stroke_color=YELLOW_3B).move_to(ax.c2p(2.1, 0.3))
            self.play(Create(xm), Flash(ax.c2p(2.1, 0.3), color=YELLOW_3B))
        self.play(FadeOut(Group(*self.mobjects)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Unique Games Conjecture: true (deterministic reduction from 3SAT)",
             r"Max-Cut beyond $0.878$, Vertex Cover below $2$: NP-hard",
             r"Manuscript: 58 pages, produced by an OpenAI model"],
            True, r"\emph{The Unique Games Theorem} (Sept.\ 2026)")
        with self.say("If it holds up, two decades of conditional theorems lose their asterisk at once. "
                      "{c}The manuscript is fifty-eight pages, written by an OpenAI model, "
                      "and its main reduction theorem has been formalized in the Lean proof assistant, "
                      "using only the standard axioms. "
                      "Companion papers give direct proofs of the Max-Cut and Vertex Cover thresholds.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("c")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
