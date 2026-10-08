import numpy as np
from manim import *

from style import *
from vo import NarratedScene

KAP = "[Kaplansky](/kəplˈænski/)"
ELEK = "[Elek](/ˈɛlɛk/)"
SZA = "[Szabó](/sˈɑbO/)"
GOT = "[Gottschalk](/ɡˈɑtʃɔk/)"
FANO = "[Fano](/fˈɑnO/)"
OMEARA = "[O'Meara](/Omˈɑɹə/)"


def mat(rows, color):
    return Matrix(rows, element_alignment_corner=ORIGIN, h_buff=0.7, v_buff=0.6).set_color(color).scale(0.75)


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "197", r"Kaplansky's Direct-Finiteness Conjecture Is False",
                          r"A torsion-free group algebra in which $ab=1$ but $ba\neq1$")
        with self.say("One-sided inverses, in group algebras."):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ hook: rectangles and shifts
        sq = MathTex(r"\text{square matrices:}\quad AB=I\ \Longrightarrow\ BA=I", font_size=40).to_edge(UP, buff=0.5)
        A = mat([[1, 0, 0], [0, 1, 0]], BLUE_3B)
        B = mat([[1, 0], [0, 1], [0, 0]], YELLOW_3B)
        I2 = mat([[1, 0], [0, 1]], WHITE)
        BA = mat([[1, 0, 0], [0, 1, 0], [0, 0, 0]], WHITE)
        row1 = VGroup(A, B, MathTex("=", font_size=44), I2).arrange(RIGHT, buff=0.3)
        row2 = VGroup(B.copy(), A.copy(), MathTex("=", font_size=44), BA, MathTex(r"\neq I_3", font_size=40,
                                                                                    color=RED_3B)).arrange(RIGHT,
                                                                                                           buff=0.3)
        rows = VGroup(row1, row2).arrange(RIGHT, buff=1.2).next_to(sq, DOWN, buff=0.6)
        if rows.width > 12.8:
            rows.scale_to_fit_width(12.8)

        def tape(vals, y, x0=-5.2, col=GREY_A):
            g = VGroup()
            for k, v in enumerate(vals):
                b = Square(0.62, stroke_color=GREY_B, stroke_width=2).move_to([x0 + 0.66 * k, y, 0])
                t = MathTex(v, font_size=28, color=col if v != "0" else RED_3B).move_to(b)
                g.add(VGroup(b, t))
            g.add(MathTex(r"\cdots", font_size=32).next_to(g, RIGHT, buff=0.15))
            return g

        xs = ["x_1", "x_2", "x_3", "x_4", "x_5"]
        tA = tape(xs, -1.0)
        tR = tape(["0"] + xs[:4], -1.8)
        tL = tape(xs, -2.6)
        lab = VGroup(Tex(r"shift right $R$", font_size=28).next_to(tR, RIGHT, buff=0.4),
                     Tex(r"then left $L$: back to start", font_size=28, color=GREEN_3B).next_to(tL, RIGHT, buff=0.4))
        uA = tape(xs, -1.0, x0=1.4)
        uL = tape(xs[1:] + ["x_6"], -1.8, x0=1.4)
        uR = tape(["0"] + xs[1:4] + ["x_5"], -2.6, x0=1.4)
        ct1 = Tex(r"right, then left", font_size=30, color=GREEN_3B).next_to(tA, UP, buff=0.2)
        ct2 = Tex(r"left, then right: $x_1$ is lost", font_size=30, color=RED_3B).next_to(uA, UP, buff=0.2)
        with self.say("For square matrices, a left inverse is automatically a right inverse: if A B is the "
                      "identity, so is B A. {r}Not for rectangles. This two by three matrix times this three by two "
                      "matrix is the identity, {o}but in the other order you get a three by three matrix that has "
                      "lost a dimension. {s}Infinite objects behave like rectangles. Shift a sequence right, then "
                      "left, and you get it back. {l}Shift left first, and the first entry is gone for good.") as s:
            self.play(Write(sq))
            s.wait_until("r")
            self.play(FadeIn(row1))
            s.wait_until("o")
            self.play(FadeIn(row2))
            s.wait_until("s")
            self.play(FadeIn(tA), FadeIn(ct1))
            self.play(TransformFromCopy(tA, tR), FadeIn(lab[0]))
            self.play(TransformFromCopy(tR, tL), FadeIn(lab[1]))
            s.wait_until("l")
            self.play(FadeOut(lab), FadeIn(uA), FadeIn(ct2))
            self.play(TransformFromCopy(uA, uL))
            self.play(TransformFromCopy(uL, uR))
        lr = MathTex(r"LR=1,\qquad RL\neq1", font_size=44, color=YELLOW_3B).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(lr))
        self.wait(0.8)
        self.play(FadeOut(VGroup(sq, rows, tA, tR, tL, uA, uL, uR, lr, ct1, ct2)))

        # ------------------------------------------------------------ group algebras
        defn = VGroup(
            Tex(r"Group algebra $K[G]$: finite sums $\sum c_g\,g$, multiplied by the group law", font_size=36),
            Tex(r"over $\mathbb{F}_2=\{0,1\}$: a finite set of group elements; terms cancel in pairs", font_size=32,
                color=GREY_A),
        ).arrange(DOWN, buff=0.25).to_edge(UP, buff=0.5)
        ex = MathTex(r"(1+t)(1+t+t^2)", r"=1+", r"t", r"+", r"t^2", r"+", r"t", r"+", r"t^2", r"+t^3", r"=1+t^3",
                     font_size=44).next_to(defn, DOWN, buff=0.7)
        exl = Tex(r"in $\mathbb{F}_2[\mathbb{Z}]$, \ $\mathbb{Z}=\langle t\rangle$", font_size=28, color=GREY_A).next_to(
            ex, DOWN, buff=0.25)
        both = VGroup(
            Tex(r"infinite-dimensional, like the shifts", font_size=34, color=BLUE_3B),
            Tex(r"but every element is finite, like a matrix", font_size=34, color=BLUE_3B),
        ).arrange(DOWN, buff=0.2).next_to(exl, DOWN, buff=0.6)
        q = Tex(r"Kaplansky: in every $K[G]$, does $ab=1$ force $ba=1$?", font_size=42, color=YELLOW_3B).next_to(
            both, DOWN, buff=0.55)
        with self.say("A group algebra sits in between. Its elements are finite sums of group elements with "
                      "coefficients in a field, multiplied using the group law. {f}Over the field with two "
                      "elements, an element is just a finite set of group elements, and when you multiply, "
                      "matching terms cancel in pairs, since one plus one is zero. {e}For example, one plus t, "
                      "times one plus t plus t squared, is one plus t cubed. {inf}Infinite-dimensional, like the "
                      "shifts, but every element finite, like a matrix. "
                      f"{{k}}{KAP} asked whether that is enough: in every group algebra, does a b equals one force "
                      "b a equals one?") as s:
            self.play(FadeIn(defn[0]))
            s.wait_until("f")
            self.play(FadeIn(defn[1]))
            s.wait_until("e")
            self.play(Write(ex[0:10]), FadeIn(exl), run_time=2)
            self.play(*[ex[i].animate.set_color(RED_3B) for i in (2, 4, 6, 8)])
            self.play(Write(ex[10]))
            s.wait_until("inf")
            self.play(FadeIn(both))
            s.wait_until("k")
            self.play(Write(q))
        self.play(FadeOut(VGroup(defn, ex, exl, both, q)))

        # ------------------------------------------------------------ history: soficity
        hist = VGroup(
            Tex(r"characteristic 0: \textbf{yes} for every group (Kaplansky; a trace argument)", font_size=34),
            Tex(r"characteristic $p$: free-by-amenable groups (Ara--O'Meara--Perera)", font_size=34),
            Tex(r"\phantom{characteristic $p$:} then all \emph{sofic} groups (Elek--Szab\'o)", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(UP, buff=0.5)
        # a permutation picture for soficity
        n = 12
        circ_c = np.array([-3.2, -1.6, 0])
        pts = [circ_c + 1.5 * np.array([np.cos(TAU * k / n), np.sin(TAU * k / n), 0]) for k in range(n)]
        dots = VGroup(*[Dot(p, radius=0.07, color=GREY_A) for p in pts])
        perm = [(k + 5) % n for k in range(n)]
        arrows = VGroup(*[CurvedArrow(pts[k], pts[perm[k]], angle=-0.5, color=TEAL_3B, stroke_width=2,
                                      tip_length=0.12) for k in range(n)])
        sofl = VGroup(
            Tex(r"\textbf{sofic}: the group law can be imitated", font_size=32, color=TEAL_3B),
            Tex(r"by permutations of finite sets,", font_size=32, color=TEAL_3B),
            Tex(r"each $g\neq e$ moving almost every point", font_size=32, color=TEAL_3B),
            Tex(r"no non-sofic group was known", font_size=32, color=ORANGE_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(RIGHT * 2.6 + DOWN * 1.5)
        with self.say(f"In characteristic zero the answer is yes, for every group: {KAP} proved it with operator "
                      "algebras, using a trace. {p}In positive characteristic, it was proved for larger and larger "
                      f"classes of groups: free-by-amenable groups, by Ara, {OMEARA} and Perera, and then all sofic "
                      f"groups, by {ELEK} and {SZA}. {{s}}A group is sofic if its multiplication can be imitated by "
                      "permutations of finite sets, with every non-identity element moving almost every point. "
                      "{n}No group was known to be non-sofic. So any counterexample would have to be a group of a "
                      "kind nobody had ever seen.") as s:
            self.play(FadeIn(hist[0]))
            s.wait_until("p")
            self.play(FadeIn(hist[1]))
            self.play(FadeIn(hist[2]))
            s.wait_until("s")
            self.play(FadeIn(dots), FadeIn(sofl[0:3]))
            self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.08), run_time=2)
            s.wait_until("n")
            self.play(FadeIn(sofl[3]))
        self.play(FadeOut(VGroup(hist, dots, arrows, sofl)))

        # ------------------------------------------------------------ theorem
        thm = VGroup(
            Tex(r"\textbf{Theorem.} There is a finitely presented, torsion-free group $G$", font_size=38),
            Tex(r"and $a,b,c\in\mathbb{F}_2[G]$ with \quad $ab=1,\quad ac=0,\quad c\neq0.$", font_size=38),
        ).arrange(DOWN, buff=0.2)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3)).to_edge(UP, buff=0.5)
        cert = MathTex(r"ba=1\ \Rightarrow\ c=(ba)c=b(ac)=0", font_size=44).next_to(tb, DOWN, buff=0.6)
        cx = Tex(r"contradiction, so $ba\neq1$", font_size=36, color=RED_3B).next_to(cert, DOWN, buff=0.3)
        ns = Tex(r"by Elek--Szab\'o, $G$ is \textbf{not sofic}", font_size=36, color=ORANGE_3B).next_to(cx, DOWN,
                                                                                                    buff=0.5)
        comp = Tex(r"earlier manuscript: characteristic two, with a group that has odd-order torsion;\\ "
                   r"its elements also give an injective, non-surjective cellular automaton,\\ "
                   r"refuting Gottschalk's surjunctivity conjecture", font_size=28, color=GREY_A).next_to(ns, DOWN, buff=0.5)
        with self.say("Manuscripts in OpenAI's math catalogue, not yet peer reviewed, claim that the answer is no. "
                      "{t}The strongest: a finitely presented, torsion-free group G, and elements a, b and c of its "
                      "group algebra over the field with two elements, with a b equal to one, a c equal to zero, "
                      "and c not zero. {c}That settles it: if b a were one, then c would equal b a c, which is b "
                      "times zero. {ns}And by Elek and Szabó's theorem, this G cannot be sofic. "
                      f"{{e}}An earlier manuscript did it in characteristic two, with a group that has torsion, "
                      f"and also refuted {GOT}'s surjunctivity conjecture.".replace("Elek and Szabó", f"{ELEK} and {SZA}")) as s:
            s.wait_until("t")
            self.play(Write(tb), run_time=2.5)
            s.wait_until("c")
            self.play(Write(cert))
            self.play(FadeIn(cx))
            s.wait_until("ns")
            self.play(FadeIn(ns))
            s.wait_until("e")
            self.play(FadeIn(comp))
        self.play(FadeOut(VGroup(tb, cert, cx, ns, comp)))

        # ------------------------------------------------------------ graphs and cones
        hdr = Tex(r"Building $G$ from labeled graphs", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.35)
        gc = np.array([-4.3, -0.4, 0])
        V = {0: (0, 0), 1: (1.4, 0.9), 2: (1.5, -0.9), 3: (-1.4, 1.0), 4: (-1.5, -0.9), 5: (0.1, 1.9),
             6: (2.8, 0.1)}
        V = {k: gc + np.array([x, y, 0]) for k, (x, y) in V.items()}
        E = [(0, 1, BLUE_3B), (0, 2, GREEN_3B), (0, 3, PURPLE_3B), (0, 4, ORANGE_3B), (1, 5, GREEN_3B),
             (3, 5, BLUE_3B), (1, 6, PURPLE_3B), (2, 6, ORANGE_3B), (2, 4, PURPLE_3B)]
        edges = VGroup(*[Line(V[a], V[b], color=c, stroke_width=5) for a, b, c in E])
        verts = VGroup(*[Dot(V[k], radius=0.11, color=YELLOW_3B if k == 0 else GREY_A) for k in V])
        rl = Tex("root", font_size=26, color=YELLOW_3B).next_to(V[0], DOWN, buff=0.18)
        path = VGroup(Line(V[0], V[1], color=WHITE, stroke_width=10, stroke_opacity=0.5),
                      Line(V[1], V[6], color=WHITE, stroke_width=10, stroke_opacity=0.5))
        xl = MathTex("x", font_size=32).next_to(V[6], RIGHT, buff=0.15)
        legend = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.5, color=c, stroke_width=5), MathTex(l, font_size=30))
                          .arrange(RIGHT, buff=0.15) for l, c in [("s", BLUE_3B), ("t", GREEN_3B), ("u", PURPLE_3B),
                                                                  ("v", ORANGE_3B)]]).arrange(RIGHT, buff=0.45)
        legend.next_to(VGroup(*verts), DOWN, buff=0.45)
        side = VGroup(
            Tex(r"each edge carries a letter", font_size=32),
            Tex(r"glue a cone onto the graph:", font_size=32),
            Tex(r"every closed path becomes $1$ in $G$", font_size=32),
            MathTex(r"g_x=\text{letters read from the root to }x", font_size=32, color=TEAL_3B),
            MathTex(r"a=\sum_x g_x,\qquad b=\sum_x g_x^{-1}", font_size=40, color=YELLOW_3B),
        ).arrange(DOWN, buff=0.28).move_to(RIGHT * 3.55 + DOWN * 0.2)
        gxl = MathTex(r"g_x=s\,u", font_size=34, color=WHITE).next_to(V[6], RIGHT, buff=0.45).shift(UP * 0.35)
        with self.say("How do you build such a group? {e}Start with finite graphs whose edges carry letters. "
                      "{c}Glue a cone onto each graph, so that every closed path in it becomes trivial in the "
                      "group. {g}Then every vertex x gets a well-defined group element, g x: read the letters along "
                      "any path from the root. {a}Let a be the sum of all the g x, and b the sum of their "
                      "inverses.") as s:
            self.play(Write(hdr))
            s.wait_until("e")
            self.play(Create(edges), FadeIn(verts), FadeIn(rl), FadeIn(legend), FadeIn(side[0]), run_time=2)
            s.wait_until("c")
            self.play(FadeIn(side[1:3]))
            s.wait_until("g")
            self.play(Create(path), FadeIn(xl), FadeIn(side[3]))
            self.play(FadeIn(gxl))
            s.wait_until("a")
            self.play(Write(side[4]))
        self.play(FadeOut(VGroup(edges, verts, rl, path, xl, legend, side[:4], gxl)),
                  side[4].animate.next_to(hdr, DOWN, buff=0.3))
        aform = side[4]

        # ------------------------------------------------------------ parity
        ab = MathTex(r"ab=\sum_{x,x'} g_x\,g_{x'}^{-1}", font_size=40).next_to(aform, DOWN, buff=0.35)
        step = MathTex(r"g_{x\cdot t}\,g_{x'\cdot t}^{-1}=g_x\,t\,t^{-1}g_{x'}^{-1}=g_x\,g_{x'}^{-1}", font_size=38,
                       color=TEAL_3B).next_to(ab, DOWN, buff=0.3)
        steptxt = Tex(r"step $x$ and $x'$ along a shared letter $t$: the term doesn't change", font_size=30,
                      color=GREY_A).next_to(step, DOWN, buff=0.2)

        def comp_graph(pos, edges_, center, label, deg_even=None, scale=0.75):
            P = [center + scale * np.array([x, y, 0]) for x, y in pos]
            g = VGroup(*[Line(P[a], P[b], color=GREY_B, stroke_width=3) for a, b in edges_])
            ds = VGroup(*[Dot(p, radius=0.1, color=(YELLOW_3B if i == deg_even else BLUE_3B)) for i, p in enumerate(P)])
            lab_ = MathTex(label, font_size=32).next_to(VGroup(g, ds), DOWN, buff=0.25)
            return VGroup(g, ds, lab_)

        y0 = -1.5
        k4 = comp_graph([(-0.7, -0.7), (0.7, -0.7), (0.7, 0.7), (-0.7, 0.7)],
                        [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3)], np.array([-4.2, y0, 0]),
                        r"4\times g = 0")
        k2 = comp_graph([(-0.7, 0), (0.7, 0)], [(0, 1)], np.array([-1.4, y0, 0]), r"2\times h = 0")
        k6 = comp_graph([(np.cos(TAU * k / 6), np.sin(TAU * k / 6)) for k in range(6)],
                        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 3), (1, 4), (2, 5)],
                        np.array([1.4, y0, 0]), r"6\times k = 0")
        root = comp_graph([(-0.9, 0), (0, 0), (0.9, 0)], [(0, 1), (1, 2)], np.array([4.4, y0, 0]),
                          r"3\times 1 = 1", deg_even=1)
        rlab = Tex(r"(root, root)", font_size=24, color=YELLOW_3B).next_to(root[1][1], UP, buff=0.15)
        hs = Tex(r"handshake lemma: a finite graph has an \emph{even} number of odd-degree vertices",
                 font_size=30, color=YELLOW_3B).to_edge(DOWN, buff=0.35)
        with self.say("Multiply them: a b is a sum of terms g x times g x prime inverse, one for each pair of "
                      "vertices. {st}Now the key trick. If x and x prime both have an edge with the same letter t, "
                      "stepping both along it leaves the term unchanged, because t times t inverse cancels. "
                      "{cp}Join pairs by these simultaneous steps. Each connected component of this pair graph "
                      "contributes a single group element, once for each of its vertices, and over the field with "
                      "two elements only components with an odd number of vertices survive. {hs}Here the handshake "
                      "lemma enters: every finite graph has an even number of vertices of odd degree. The degree of "
                      "a pair is the number of letters the two vertices share. {od}Arrange for every pair to share "
                      "an odd number of letters, except the root paired with itself. {r}Then every component "
                      "cancels, except the root's, which has odd size and contributes exactly one. So a b equals "
                      "one. The same count with a second graph, with no exception at all, gives a c equals "
                      "zero.") as s:
            self.play(Write(ab))
            s.wait_until("st")
            self.play(Write(step), FadeIn(steptxt), run_time=2)
            s.wait_until("cp")
            self.play(FadeOut(steptxt), FadeIn(k4[:2]), FadeIn(k2[:2]), FadeIn(k6[:2]), FadeIn(root[:2]))
            s.wait_until("hs")
            self.play(FadeIn(hs))
            s.wait_until("od")
            self.play(FadeIn(rlab), Indicate(root[1][1], color=YELLOW_3B))
            s.wait_until("r")
            self.play(LaggedStart(FadeIn(k4[2]), FadeIn(k2[2]), FadeIn(k6[2]), FadeIn(root[2]), lag_ratio=0.4),
                      run_time=2)
            res = MathTex(r"ab=1", font_size=44, color=YELLOW_3B).next_to(step, RIGHT, buff=0.6)
            self.play(Write(res))
        self.play(FadeOut(VGroup(hdr, aform, ab, step, k4, k2, k6, root, rlab, hs, res)))

        # ------------------------------------------------------------ projective planes, and the hard part
        fc = np.array([-3.6, -0.3, 0])
        R0 = 2.0
        P = [fc + R0 * np.array([np.cos(PI / 2 + TAU * k / 3), np.sin(PI / 2 + TAU * k / 3), 0]) for k in range(3)]
        M = [(P[(k + 1) % 3] + P[(k + 2) % 3]) / 2 for k in range(3)]
        Cn = fc
        pts7 = P + M + [Cn]
        lines7 = [Line(P[0], P[1]), Line(P[1], P[2]), Line(P[2], P[0]),
                  Line(P[0], M[0]), Line(P[1], M[1]), Line(P[2], M[2])]
        fano = VGroup(*[l.set_color(GREY_B).set_stroke(width=3) for l in lines7],
                      Circle(radius=R0 / 2, color=GREY_B, stroke_width=3).move_to(fc))
        fd = VGroup(*[Dot(p, radius=0.12, color=WHITE) for p in pts7])
        hl1 = Line(P[1], P[2], color=BLUE_3B, stroke_width=8)
        hl2 = Line(P[0], M[0], color=GREEN_3B, stroke_width=8)
        meet = Dot(M[0], radius=0.17, color=YELLOW_3B)
        flab = Tex(r"the Fano plane (over $\mathbb{F}_2$)", font_size=28, color=GREY_A).next_to(fano, DOWN, buff=0.3)
        hdr2 = Tex(r"Where the odd overlaps come from", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.35)
        txt = VGroup(
            Tex(r"projective plane over $\mathbb{F}_{128}$:", font_size=32),
            Tex(r"vertex $\mapsto$ the points of a line", font_size=32),
            Tex(r"two lines meet in exactly $1$ point;\\ a line has $129$ points: both odd", font_size=32,
                color=TEAL_3B),
            Tex(r"7 extra letters, from the Fano plane,\\ give the root its one even exception", font_size=32),
            Tex(r"the hard part: random graphs of huge girth\\ $\Rightarrow$ $G$ torsion-free, and $c\neq0$",
                font_size=32, color=ORANGE_3B),
        ).arrange(DOWN, buff=0.32).move_to(RIGHT * 2.9 + DOWN * 0.1)
        with self.say("Where do odd overlaps come from? From projective geometry. {pp}The letters at each vertex "
                      "are the points of a line in the projective plane over the field with a hundred and "
                      "twenty-eight elements. {m}Two different lines always meet in exactly one point, and each "
                      f"line has a hundred and twenty-nine points: odd, either way. The {FANO} plane shows the same "
                      f"thing in miniature. {{x}}Seven extra letters, arranged by the {FANO} "
                      "plane, give the root its single even exception. {h}The hard part, most of the thirty-one "
                      "pages, is geometry: choosing the graphs at random, with enormous girth, so that the group is "
                      "torsion-free, and proving that no path from the root to another vertex becomes trivial, so "
                      "that c is not zero.") as s:
            self.play(Write(hdr2))
            s.wait_until("pp")
            self.play(FadeIn(txt[0:2]))
            s.wait_until("m")
            self.play(FadeIn(txt[2]))
            self.play(Create(fano), FadeIn(fd), FadeIn(flab))
            self.play(Create(hl1), Create(hl2))
            self.play(FadeIn(meet, scale=2))
            s.wait_until("x")
            self.play(FadeIn(txt[3]))
            s.wait_until("h")
            self.play(FadeIn(txt[4]))
        self.play(FadeOut(VGroup(hdr2, fano, fd, hl1, hl2, meet, flab, txt)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Finitely presented torsion-free $G$, and $a,b\in\mathbb{F}_2[G]$ with $ab=1\neq ba$",
             r"$G$ is not sofic; companions refute Gottschalk's surjunctivity conjecture",
             r"\quad and the group-ring Determinant Conjecture",
             r"Lean: the earlier characteristic-two counterexample (a group with torsion)",
             r"Manuscripts produced by an OpenAI model"],
            False, r"\emph{A Torsion-Free Group Algebra That Is Not Directly Finite} (Oct.\ 2026)")
        with self.say("On verification: Lean formalizations cover the earlier counterexamples: "
                      "characteristic two with a finitely presented group that has torsion, an odd characteristic "
                      "version, and the Determinant Conjecture. {l}The torsion-free construction, and the "
                      "conclusion that the group is not sofic, have not been formalized, and await expert checking. "
                      "If they hold, a question about one-sided inverses has also shown that not every group is "
                      "sofic.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
