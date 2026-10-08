from pathlib import Path

import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(Path(__file__).parent / "data" / "v20.npz")

BAR = "[Barnette](/bɑɹnˈɛt/)"
TUT = "[Tutte](/tˈʌt/)"
GRU = "[Grünbaum](/ɡɹˈunbWm/)"
SCHN = "[Schnieders](/ʃnˈidəɹz/)"
GOOD = "[Goodey](/ɡˈʊdi/)"

# dual of the planar cube drawing = octahedron; vertices are the cube's faces
OCT = {"out": np.array([0, 3.0, 0]), "S": np.array([-2.75, -1.6, 0]), "W": np.array([2.75, -1.6, 0]),
       "in": np.array([0, -0.75, 0]), "E": np.array([-0.68, 0.4, 0]), "N": np.array([0.68, 0.4, 0])}
OCT_E = [("out", "S"), ("S", "W"), ("W", "out"), ("in", "E"), ("E", "N"), ("N", "in"),
         ("out", "E"), ("out", "N"), ("S", "E"), ("S", "in"), ("W", "N"), ("W", "in")]
BLACK = [("out", "E", "N"), ("S", "in", "E"), ("N", "in", "W")]  # blue triangles besides the outer face
WHITE_T = [("out", "S", "E"), ("out", "N", "W"), ("S", "in", "W"), ("in", "E", "N")]
STATE_S = {0: "N", 1: "E", 2: "in"}
STATE_R = {0: "E", 1: "in", 2: "N"}


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "180", r"Barnette's Conjecture",
                          r"Hamiltonian cycles in cubic bipartite polyhedra")
        with self.say(f"{BAR}'s conjecture: can you always tour every corner of a polyhedron like this, and come "
                      "back to the start?"):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.4)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ truncated octahedron
        off = LEFT * 3.0 + DOWN * 0.2
        pos = D["to_pos"]
        P = [off + np.array([x, y, 0]) for x, y in pos]
        E = D["to_E"]
        col = D["to_col"]
        edges = VGroup(*[Line(P[a], P[b], color=GREY_B, stroke_width=3) for a, b in E])
        verts = VGroup(*[Dot(P[v], radius=0.09, color=WHITE) for v in range(len(P))])
        H = list(D["to_H"]) + [D["to_H"][0]]
        cyc = VMobject(color=YELLOW_3B, stroke_width=7).set_points_as_corners([P[v] for v in H])
        txt = VGroup(Tex(r"truncated octahedron, flattened", font_size=32),
                     Tex(r"every corner: 3 edges (\emph{cubic})", font_size=32),
                     Tex(r"faces: squares and hexagons", font_size=32),
                     Tex(r"even faces $\Rightarrow$ two colors of corners,\\ every edge joins different colors"
                         r" (\emph{bipartite})", font_size=30, color=GREY_A),
                     Tex(r"a \emph{Hamiltonian cycle}: every corner once", font_size=32, color=YELLOW_3B),
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(RIGHT * 3.4 + UP * 0.3)
        with self.say("This is the skeleton of a truncated octahedron, flattened into the plane. {c}Every corner "
                      "meets exactly three edges, and every face is a square or a hexagon. {b}Because all faces have "
                      "an even number of sides, the corners split into two colors, with every edge joining different "
                      "colors. {h}Can you walk along the edges, visit every corner exactly once, and return to the "
                      "start? Here is one way: a Hamiltonian cycle.") as s:
            self.play(Create(edges), FadeIn(verts), FadeIn(txt[0]), run_time=2)
            s.wait_until("c")
            self.play(FadeIn(txt[1]), FadeIn(txt[2]))
            s.wait_until("b")
            self.play(*[verts[v].animate.set_color(BLUE_3B if col[v] else ORANGE_3B) for v in range(len(P))],
                      FadeIn(txt[3]))
            s.wait_until("h")
            self.play(Create(cyc), run_time=4, rate_func=linear)
            self.play(FadeIn(txt[4]))
        self.play(FadeOut(VGroup(edges, verts, cyc, txt)))

        # ------------------------------------------------------------ history
        hist = VGroup(
            Tex(r"1884, Tait: every cubic polyhedron has a Hamiltonian cycle?", font_size=34),
            Tex(r"(this would have proved the four color theorem)", font_size=30, color=GREY_A),
            Tex(r"1946, Tutte: a counterexample with 46 vertices", font_size=34, color=RED_3B),
            Tex(r"Barnette: true if the graph is also \emph{bipartite}?", font_size=34, color=YELLOW_3B),
            Tex(r"(recorded by Gr\"unbaum, 1969)", font_size=30, color=GREY_A),
            Tex(r"proved for faces of sizes 4 and 6 only (Goodey); faces $\le 8$ (Schnieders)", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        with self.say("In 1884, Peter Guthrie Tait conjectured that every polyhedron with three edges at each corner "
                      f"has such a tour. That would have proved the four color theorem. {{t}}But in 1946, {TUT} found "
                      f"a counterexample with forty-six vertices. {{b}}David {BAR} then proposed that the bipartite "
                      f"ones always have a tour: the conjecture was recorded by {GRU} in 1969. {{p}}It was proved when "
                      f"every face is a square or a hexagon, by {GOOD}, and more recently for faces of at most eight "
                      f"sides, by {SCHN}. But not in general.") as s:
            self.play(FadeIn(hist[0]))
            self.play(FadeIn(hist[1]))
            s.wait_until("t")
            self.play(FadeIn(hist[2]))
            s.wait_until("b")
            self.play(FadeIn(hist[3]), FadeIn(hist[4]))
            s.wait_until("p")
            self.play(FadeIn(hist[5]))
        self.play(FadeOut(hist))

        thm = VGroup(Tex(r"\textbf{Theorem.} Every finite simple graph that is", font_size=40),
                     Tex(r"cubic, bipartite, planar and 3-connected", font_size=40, color=YELLOW_3B),
                     Tex(r"has a Hamiltonian cycle.", font_size=40),
                     Tex(r"(Stronger: the cycle can avoid any one prescribed edge.)", font_size=32, color=GREY_A)
                     ).arrange(DOWN, buff=0.25)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3))
        with self.say("A manuscript in OpenAI's math catalogue claims a proof, in eleven pages. {t}Every finite simple "
                      "graph that is cubic, bipartite, planar and three-connected has a Hamiltonian cycle. {s}In fact, "
                      "the paper proves that the cycle can be chosen to avoid any one prescribed edge.") as s:
            s.wait_until("t")
            self.play(FadeIn(tb[1]), Write(thm[:3]), run_time=2.5)
            s.wait_until("s")
            self.play(FadeIn(thm[3]))
        self.play(FadeOut(tb))

        # ------------------------------------------------------------ the dual picture on the cube
        hdr = Tex(r"A Hamiltonian cycle splits the faces into two trees", font_size=38, color=YELLOW_3B).to_edge(
            UP, buff=0.3)
        co = LEFT * 3.3 + DOWN * 0.45
        cp = [co + np.array([x, y, 0]) * 0.95 for x, y in D["c_pos"]]
        cE = VGroup(*[Line(cp[a], cp[b], color=GREY_B, stroke_width=3) for a, b in D["c_E"]])
        cV = VGroup(*[Dot(p, radius=0.1, color=WHITE) for p in cp])
        cH = list(D["c_H"]) + [D["c_H"][0]]
        ccyc = VMobject(color=YELLOW_3B, stroke_width=7).set_points_as_corners([cp[v] for v in cH])
        faces = {"in": [4, 5, 6, 7], "S": [0, 1, 5, 4], "E": [1, 2, 6, 5], "N": [2, 3, 7, 6], "W": [3, 0, 4, 7]}
        inside = [str(f) for f in D["c_in"]]
        fill = VGroup(*[Polygon(*[cp[v] for v in vs], stroke_width=0).set_fill(TEAL_3B if f in inside else PURPLE_3B,
                                                                                0.45)
                        for f, vs in faces.items()])
        outer_band = Square(2.2 * 2 * 0.95 + 0.7, stroke_width=0).set_fill(PURPLE_3B, 0.25).move_to(co)
        cen = {f: np.mean([cp[v] for v in vs], axis=0) for f, vs in faces.items()}
        cen["out"] = co + UP * 2.55
        tdots = VGroup(*[Dot(cen[f], radius=0.11, color=TEAL_3B if f in inside else PURPLE_3B)
                         .set_stroke(WHITE, 2) for f in cen])
        t1 = VGroup(Line(cen["S"], cen["in"], color=TEAL_3B, stroke_width=6),
                    Line(cen["in"], cen["N"], color=TEAL_3B, stroke_width=6))
        t2 = VGroup(ArcBetweenPoints(cen["W"], cen["out"], angle=-PI / 2.2, color=PURPLE_3B, stroke_width=6),
                    ArcBetweenPoints(cen["out"], cen["E"], angle=-PI / 2.2, color=PURPLE_3B, stroke_width=6))
        side = VGroup(
            Tex(r"Dual: one vertex per face (outer face too).", font_size=30),
            Tex(r"For the cube: an octahedron, whose faces are", font_size=30),
            Tex(r"triangles in two colors (cube is bipartite).", font_size=30),
            Tex(r"Inside faces: a tree.\ \ Outside faces: a tree.", font_size=30, color=YELLOW_3B),
            Tex(r"Goal: split the vertices of a 2-colored", font_size=30),
            Tex(r"triangulation into two \emph{induced trees}.", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT * 3.25 + DOWN * 0.3)
        side[4:].shift(DOWN * 0.3)
        with self.say("The proof moves to the dual picture. {c}Here is the cube with a Hamiltonian cycle. {f}The cycle "
                      "cuts the faces into two sides: inside and outside. {d}Put a vertex in every face, the outer one "
                      "included, and join neighboring faces. For the cube, that gives an octahedron, whose faces are "
                      "triangles, and because the cube is bipartite, those triangles come in two colors. "
                      "{t}On each side of the cycle, the faces form a tree in the dual: connected, with no loops. "
                      "{g}This works in reverse too, so the goal becomes: split the vertices of a two-colored "
                      "triangulation into two sets, each forming a tree.") as s:
            self.play(Write(hdr), Create(cE), FadeIn(cV))
            s.wait_until("c")
            self.play(Create(ccyc), run_time=2)
            s.wait_until("f")
            self.play(FadeIn(outer_band), FadeIn(fill))
            self.bring_to_front(cE, ccyc, cV)
            s.wait_until("d")
            self.play(FadeIn(tdots), FadeIn(side[:3]))
            s.wait_until("t")
            self.play(Create(t1), Create(t2), FadeIn(side[3]), run_time=2)
            s.wait_until("g")
            self.play(FadeIn(side[4:]))
        self.play(FadeOut(VGroup(hdr, cE, cV, ccyc, fill, outer_band, tdots, t1, t2, side)))

        # ------------------------------------------------------------ states on the octahedron
        hdr = Tex(r"Tutte states on the triangulation", font_size=38, color=YELLOW_3B).to_edge(UP, buff=0.3)
        oo = LEFT * 3.0 + DOWN * 0.55
        O = {k: oo + v * 0.95 for k, v in OCT.items()}
        tris_b = VGroup(*[Polygon(*[O[v] for v in t], stroke_width=0).set_fill(BLUE_3B, 0.45) for t in BLACK])
        tris_w = VGroup(*[Polygon(*[O[v] for v in t], stroke_width=0).set_fill(YELLOW_3B, 0.3) for t in WHITE_T])
        oE = VGroup(*[Line(O[a], O[b], color=GREY_B, stroke_width=3) for a, b in OCT_E])
        oV = {k: Dot(O[k], radius=0.11, color=WHITE) for k in O}
        roots = VGroup(*[oV[k] for k in ("out", "S", "W")])
        rl = Tex(r"roots", font_size=28, color=RED_3B).next_to(O["out"], RIGHT, buff=0.2)
        outer_note = Tex(r"(the outside is the\\ outer blue triangle)", font_size=24, color=GREY_A).next_to(
            O["S"], DOWN, buff=0.2).shift(RIGHT * 0.6)

        def arrows(state, color):
            g = VGroup()
            for k, t in enumerate(BLACK):
                c = np.mean([O[v] for v in t], axis=0)
                tgt = O[state[k]]
                g.add(Arrow(c, c + 0.62 * (tgt - c), buff=0, color=color, stroke_width=5,
                            max_tip_length_to_length_ratio=0.3))
            return g

        aS = arrows(STATE_S, WHITE)
        aR = arrows(STATE_R, RED_3B)
        Q = VGroup()
        for k, t in enumerate(BLACK):
            a, b = [v for v in t if v != STATE_S[k]]
            Q.add(Line(O[a], O[b], color=GREEN_3B, stroke_width=9))
        side = VGroup(
            Tex(r"A \emph{state}: each other blue triangle points", font_size=30),
            Tex(r"at one corner; each non-root used once.", font_size=30),
            Tex(r"A \emph{pair} $(r,s)$: states that disagree", font_size=30),
            Tex(r"at every triangle.", font_size=30),
            Tex(r"$Q_s$: in each blue triangle, the edge", font_size=30, color=GREEN_3B),
            Tex(r"opposite the corner chosen by $s$.", font_size=30, color=GREEN_3B),
            Tex(r"If $Q_s$ is a forest, duality builds", font_size=30, color=YELLOW_3B),
            Tex(r"the two trees $\Rightarrow$ Hamiltonian cycle.", font_size=30, color=YELLOW_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to(RIGHT * 3.5 + DOWN * 0.3)
        for k in (2, 4, 6):
            side[k:].shift(DOWN * 0.2)
        with self.say("Now the tool. {o}Here is the octahedron, with its triangles in two colors. Choose one blue "
                      "triangle as the outer face; its three corners are the roots. {st}A state lets every other blue "
                      "triangle point at one of its corners, so that each non-root corner is chosen exactly once. "
                      f"These are states from {TUT}'s theory of trinity. {{pr}}A pair is two states, r and s, that "
                      "disagree at every triangle. {q}From s, mark in each blue triangle the edge opposite the corner "
                      "it chose. {f}Here these marked edges form a forest, with no cycles. The paper shows that "
                      "whenever that happens, a duality argument builds the two trees, and so a Hamiltonian "
                      "cycle.") as s:
            self.play(Write(hdr), FadeIn(tris_b), FadeIn(tris_w), Create(oE), *[FadeIn(d) for d in oV.values()])
            s.wait_until("o")
            self.play(roots.animate.set_color(RED_3B), FadeIn(rl), FadeIn(outer_note))
            s.wait_until("st")
            self.play(LaggedStart(*[GrowArrow(a) for a in aS], lag_ratio=0.3), FadeIn(side[:2]))
            s.wait_until("pr")
            self.play(LaggedStart(*[GrowArrow(a) for a in aR], lag_ratio=0.3), FadeIn(side[2:4]))
            s.wait_until("q")
            self.play(Create(Q), FadeIn(side[4:6]), run_time=1.5)
            s.wait_until("f")
            self.play(FadeIn(side[6:]), Indicate(Q, color=GREEN_3B))
        self.play(FadeOut(VGroup(hdr, tris_b, tris_w, oE, *oV.values(), rl, outer_note, aS, aR, Q, side)))

        # ------------------------------------------------------------ cancellation
        hdr = Tex(r"Why a good pair must exist: a sum where the bad terms cancel", font_size=38,
                  color=YELLOW_3B).to_edge(UP, buff=0.3)
        Z = MathTex(r"Z(x)=\sum_{(r,s)\ \text{pairs}} i^{\,J(r,s)}\,e^{\,x\,\omega(s)}", font_size=44).next_to(
            hdr, DOWN, buff=0.35)
        kinds = ["b", "b", "g", "b", "b", "b", "g", "b"]
        phase = [0, 2, 1, 1, 3, 0, 1, 2]
        partner = {0: 1, 1: 0, 3: 4, 4: 3, 5: 7, 7: 5}
        toks = VGroup()
        for k, (kd, ph) in enumerate(zip(kinds, phase)):
            c = RED_3B if kd == "b" else GREEN_3B
            circ = Circle(radius=0.42, color=c, stroke_width=3)
            ar = Arrow(ORIGIN, 0.36 * np.array([np.cos(ph * PI / 2), np.sin(ph * PI / 2), 0]), buff=0, color=c,
                       stroke_width=5, max_tip_length_to_length_ratio=0.35)
            toks.add(VGroup(circ, ar))
        toks.arrange(RIGHT, buff=0.45).shift(DOWN * 0.35)
        arcs = VGroup(*[ArcBetweenPoints(toks[a].get_bottom() + DOWN * 0.08, toks[b].get_bottom() + DOWN * 0.08,
                                         angle=PI / 2.5, color=RED_3B, stroke_width=2.5)
                        for a, b in partner.items() if a < b])
        leg = VGroup(Tex(r"red: $Q_s$ has a cycle \quad green: $Q_s$ is a forest \quad arrow: phase $i^{J}$",
                         font_size=28), Tex(r"(schematic)", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.1
                                                                                                ).next_to(toks, UP,
                                                                                                          buff=0.4)
        bullets = VGroup(
            Tex(r"Bad pair: reverse $r$ along a cycle of $Q_s$; a disk identity shifts $J$ by $\pm2$", font_size=30),
            Tex(r"phase flips ($i^{\pm2}=-1$), weight unchanged (it depends only on $s$): they cancel",
                font_size=30),
            Tex(r"Regroup by the cycles where $r,s$ differ; well-chosen positive weights give $Z\not\equiv0$",
                font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.say("Why must such a good pair exist? {z}The paper adds up all pairs in one weighted sum, where each "
                      "term carries a phase, a power of i. {bad}Suppose the marked edges of s contain a cycle. Reverse "
                      "the choices of r around that cycle. A counting identity for disks shows that this shifts the "
                      "exponent by two, so the phase flips sign, while the weight, which depends only on s, stays the "
                      "same. {c}So all the bad pairs cancel in couples. {nz}Grouping the terms differently, and "
                      "choosing the weights carefully, the paper shows the total sum is not zero. {g}A nonzero sum "
                      "whose bad terms all cancel must contain a good term. {sep}Graphs whose triangulation has "
                      "separating triangles are cut into smaller pieces, solved, and glued back together.") as s:
            self.play(Write(hdr))
            s.wait_until("z")
            self.play(Write(Z), run_time=2)
            self.play(LaggedStart(*[FadeIn(t) for t in toks], lag_ratio=0.1), FadeIn(leg))
            s.wait_until("bad")
            self.play(Create(arcs), FadeIn(bullets[0]))
            self.play(FadeIn(bullets[1]))
            s.wait_until("c")
            self.play(*[FadeOut(toks[k], shift=DOWN * 0.3) for k in partner], FadeOut(arcs), run_time=1.5)
            s.wait_until("nz")
            self.play(FadeIn(bullets[2]))
            s.wait_until("g")
            self.play(*[Indicate(toks[k], color=GREEN_3B, scale_factor=1.4) for k in (2, 6)])
        self.play(FadeOut(VGroup(hdr, Z, toks[2], toks[6], leg, bullets)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Every cubic bipartite planar 3-connected graph has a Hamiltonian cycle",
             r"Paper also: the cycle can avoid any prescribed edge",
             r"Manuscript: 11 pages, produced by an OpenAI model"],
            True, r"\emph{Paired states and Hamiltonian cycles}\\ \emph{in cubic bipartite planar graphs} (Sept.\ 2026)")
        with self.say("The manuscript is eleven pages, written by an OpenAI model and not yet peer reviewed. {l}Its main "
                      f"theorem, that every such graph has a Hamiltonian cycle, has been formalized in the Lean proof "
                      f"assistant. If it holds up, {BAR}'s conjecture is "
                      "settled.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
