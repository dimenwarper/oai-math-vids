import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(__file__.replace("v29_coloring.py", "data/v29.npz"))
POS, COL, EDGES = D["pos"], D["col"], D["edges"]
XS, CEDGES, ARC = D["xs"], D["cedges"], D["arc"]
PAL = [BLUE_3B, YELLOW_3B, RED_3B]

KLS = "[Khanna](/kˈɑnə/), [Linial](/lˈɪniəl/) and [Safra](/sˈɑfɹə/)"
GK = "[Guruswami](/ɡˌʊɹuswˈɑmi/) and [Khanna](/kˈɑnə/)"
BBKO = "[Barto](/bˈɑɹtO/), [Bulín](/bˈulin/), [Krokhin](/kɹˈOkɪn/) and [Opršal](/ˈɔpɹʃɑl/)"
FMW = "[Fei](/fˈA/), [Minzer](/mˈɪnzəɹ/) and Wang"
FRIED = "[Friedgut](/fɹˈidɡʊt/)"


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "106", r"Hardness of Coloring Three-Colorable Graphs",
                          r"Even an independent set of size $\delta n$ is NP-hard to find")
        with self.say("Can you color a three-colorable graph, if you are allowed a few extra colors?"):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ hook: a 3-colorable graph
        pts = [np.array([x, y - 0.3, 0]) for x, y in POS]
        verts = VGroup(*[Dot(p, radius=0.16, color=GREY_B) for p in pts])
        eds = VGroup(*[Line(pts[a], pts[b], color=GREY_C, stroke_width=3) for a, b in EDGES])
        prom = Tex(r"Promise: 3 colors suffice", font_size=38, color=YELLOW_3B).to_edge(UP, buff=0.4)
        qq = Tex(r"Can you find a coloring with 4 colors? 5? 100?", font_size=36).to_edge(DOWN, buff=0.45)
        with self.say("Here is a graph. {p}Someone promises you that it can be colored with three colors, "
                      "so that no edge joins two vertices of the same color. {r}Here is such a coloring. "
                      "{h}Finding a three-coloring is a classic NP-hard problem. {q}But with the promise in hand, "
                      "could you at least find a coloring with four colors? Or five? Or a hundred?") as s:
            self.play(Create(eds), FadeIn(verts), run_time=2)
            s.wait_until("p")
            self.play(FadeIn(prom))
            s.wait_until("r")
            self.play(*[v.animate.set_color(PAL[int(c)]) for v, c in zip(verts, COL)], run_time=1.5)
            s.wait_until("q")
            self.play(FadeIn(qq))
        self.play(FadeOut(VGroup(verts, eds, prom, qq)))

        # ------------------------------------------------------------ history: the palette gap
        ax = NumberLine(x_range=[0, 10, 1], length=11, include_ticks=False, color=GREY_B).shift(UP * 0.2)
        marks = [(0.4, "3", "promised", GREEN_3B), (1.9, "4", "NP-hard", RED_3B),
                 (3.4, "5", "NP-hard", RED_3B), (9.4, r"n^{0.195}", "achievable", BLUE_3B)]
        mk = VGroup()
        for x, lab, sub, c in marks:
            d = Dot(ax.n2p(x), color=c, radius=0.1)
            t1 = MathTex(lab, font_size=40, color=c).next_to(d, UP, buff=0.2)
            t2 = Tex(sub, font_size=26, color=c).next_to(d, DOWN, buff=0.2)
            mk.add(VGroup(d, t1, t2))
        cap = Tex("number of colors", font_size=30, color=GREY_A).next_to(ax, DOWN, buff=1.0)
        gap = Brace(Line(ax.n2p(3.8), ax.n2p(8.7)), UP, color=YELLOW_3B).shift(UP * 0.3)
        gap_t = Tex(r"conjectured: NP-hard for \emph{every} fixed number", font_size=30, color=YELLOW_3B).next_to(
            gap, UP, buff=0.15)
        who = VGroup(Tex(r"4: Khanna--Linial--Safra; Guruswami--Khanna", font_size=28, color=GREY_A),
                     Tex(r"5: Barto--Bul\'in--Krokhin--Opr\v{s}al", font_size=28, color=GREY_A),
                     Tex(r"$n^{0.19539}$: Bansal--Huang--Lee (2026); newer preprints: slightly fewer", font_size=28, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.4)
        with self.say(f"{KLS} showed that four colors is already NP-hard, and {GK} gave another proof. "
                      f"{{b}}The algebraic theory of {BBKO} pushed this to five colors. "
                      "{a}Meanwhile, efficient algorithms still need a growing number of colors: about n to the zero point one "
                      "nine five in a 2026 algorithm, and slightly fewer in even newer preprints. "
                      "{g}In between lies a huge gap, and the conjecture was that every fixed number of colors is hard. "
                      "{r}In recent weeks, that statement has also been reached by another route, through results on "
                      f"so-called d-to-1 games: by {FMW}, and via a companion manuscript in this same catalogue.") as s:
            self.play(Create(ax))
            self.play(FadeIn(mk[0]), FadeIn(mk[1]), FadeIn(cap), FadeIn(who[0]))
            s.wait_until("b")
            self.play(FadeIn(mk[2]), FadeIn(who[1]))
            s.wait_until("a")
            self.play(FadeIn(mk[3]), FadeIn(who[2]))
            s.wait_until("g")
            self.play(GrowFromCenter(gap), FadeIn(gap_t))
        self.play(FadeOut(VGroup(ax, mk, cap, gap, gap_t, who)))

        # ------------------------------------------------------------ the theorem
        ind = Tex(r"3-colorable $\Rightarrow$ some color class has $\ge n/3$ vertices:\\ an \textbf{independent set}"
                  r" (no edges inside)", font_size=34).to_edge(UP, buff=0.5)
        yes = VGroup(Tex(r"\textbf{YES}", font_size=34, color=GREEN_3B), Tex(r"3-colorable", font_size=32),
                     Tex(r"(independent set $\ge n/3$)", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.15)
        no = VGroup(Tex(r"\textbf{NO}", font_size=34, color=RED_3B),
                    Tex(r"every independent set", font_size=32), Tex(r"has $<\delta n$ vertices", font_size=32)
                    ).arrange(DOWN, buff=0.15)
        yb = VGroup(yes, caption_box(yes, GREEN_3B, 0.25))
        nb = VGroup(no, caption_box(no, RED_3B, 0.25))
        VGroup(yb, nb).arrange(RIGHT, buff=1.6).shift(UP * 0.1)
        vs = Tex(r"NP-hard to tell apart, for every fixed $0<\delta<\tfrac13$", font_size=34,
                 color=YELLOW_3B).next_to(VGroup(yb, nb), DOWN, buff=0.45)
        cor = VGroup(Tex(r"$c$-colorable $\Rightarrow$ independent set $\ge n/c$.", font_size=32),
                     Tex(r"Take $\delta<1/c$: finding a $c$-coloring of a 3-colorable graph is NP-hard.",
                         font_size=32, color=GREEN_3B)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.say("A new manuscript proves a stronger form. {i}Every three-colorable graph has an independent set, "
                      "a set of vertices with no edges among them, containing at least a third of the vertices: "
                      "just take the largest color class. {t}The theorem says: for every fixed delta below one third, "
                      "it is NP-hard to tell three-colorable graphs apart from graphs in which every independent set "
                      "has fewer than delta n vertices. {c}Coloring follows in one line. A c-coloring has a color class "
                      "of at least n over c vertices, so taking delta below one over c shows that finding a c-coloring "
                      "is NP-hard, for every fixed c.") as s:
            s.wait_until("i")
            self.play(FadeIn(ind))
            s.wait_until("t")
            self.play(FadeIn(yb), run_time=1)
            self.play(FadeIn(nb), run_time=1)
            self.play(Write(vs))
            s.wait_until("c")
            self.play(FadeIn(cor[0]))
            self.play(FadeIn(cor[1]))
        self.play(FadeOut(VGroup(ind, yb, nb, vs, cor)))

        # ------------------------------------------------------------ Label Cover
        hdr = Tex("Starting point: Label Cover", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.4)
        Lp = [np.array([-4.9, y, 0]) for y in (1.2, -0.2, -1.6)]
        Rp = [np.array([-1.9, y, 0]) for y in (1.2, -0.2, -1.6)]
        Ln = VGroup(*[Circle(radius=0.3, color=BLUE_3B, fill_opacity=0.2).move_to(p) for p in Lp])
        Rn = VGroup(*[Circle(radius=0.3, color=TEAL_3B, fill_opacity=0.2).move_to(p) for p in Rp])
        lc_e = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 0), (2, 2)]
        lce = VGroup(*[Line(Lp[a] + RIGHT * 0.3, Rp[b] + LEFT * 0.3, color=GREY_B) for a, b in lc_e])
        lab_l = VGroup(*[MathTex(t, font_size=30).move_to(p) for t, p in zip(["7", "2", "5"], Lp)])
        lab_r = VGroup(*[MathTex(t, font_size=30).move_to(p) for t, p in zip(["b", "a", "b"], Rp)])
        ul = Tex(r"answers from $\Sigma_L$", font_size=28, color=BLUE_3B).next_to(Ln, UP, buff=0.3)
        ur = Tex(r"answers from $\Sigma_R$", font_size=28, color=TEAL_3B).next_to(Rn, UP, buff=0.3)
        rules = VGroup(
            Tex(r"each edge: a projection $\pi:\Sigma_L\to\Sigma_R$", font_size=30),
            Tex(r"passes if $\pi(\text{left answer})=\text{right answer}$", font_size=30),
            Tex(r"satisfiable: \emph{all} tests pass", font_size=30, color=GREEN_3B),
            Tex(r"unsatisfiable: at most a fraction $\sigma$ pass", font_size=30, color=RED_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.2)
        with self.say("The reduction starts from Label Cover, the standard output of the PCP theorem with parallel "
                      "repetition. {q}There are questions on two sides, each answered from a fixed alphabet, "
                      "{t}and tests along the edges, which demand that the left answer projects to the right answer. "
                      "{g}From a satisfiable formula, every test can be passed. From an unsatisfiable one, any answers "
                      "pass at most a tiny fraction, sigma. The construction then strings questions together into "
                      "layered chains.") as s:
            self.play(Write(hdr))
            s.wait_until("q")
            self.play(FadeIn(Ln), FadeIn(Rn), FadeIn(ul), FadeIn(ur))
            s.wait_until("t")
            self.play(Create(lce), FadeIn(lab_l), FadeIn(lab_r), FadeIn(rules[:2]))
            s.wait_until("g")
            self.play(FadeIn(rules[2:]))
        self.play(FadeOut(VGroup(hdr, Ln, Rn, lce, lab_l, lab_r, ul, ur, rules)))

        # ------------------------------------------------------------ the phase graph and completeness
        hdr = Tex(r"Vertices are phase assignments", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.35)
        rule = VGroup(Tex(r"vertex $x$: a phase in $\mathbb{R}/\mathbb{Z}$ for each possible answer", font_size=30),
                      MathTex(r"x\sim y\iff \mathrm{dist}\big(x,\ y+\tfrac12\big)\le\tfrac18", font_size=36)).arrange(
            DOWN, buff=0.2).next_to(hdr, DOWN, buff=0.3)
        cen = np.array([-3.0, -1.2, 0])
        R = 2.0
        circ = Circle(radius=R, color=GREY_B).move_to(cen)

        def cp(x):
            return cen + R * np.array([np.cos(TAU * x + PI / 2), np.sin(TAU * x + PI / 2), 0])

        cd_ = VGroup(*[Dot(cp(x), radius=0.08, color=WHITE) for x in XS])
        ce = VGroup(*[Line(cp(XS[a]), cp(XS[b]), color=GREY_C, stroke_width=1.6) for a, b in CEDGES])
        arcs = VGroup(*[Arc(radius=R + 0.18, start_angle=PI / 2 + TAU * k / 3, angle=TAU / 3 - 0.04, color=PAL[k],
                            stroke_width=10).shift(cen) for k in range(3)])
        side = VGroup(
            Tex(r"one coordinate: join nearly opposite points", font_size=28),
            Tex(r"joined points are $\ge\tfrac38>\tfrac13$ apart", font_size=28),
            Tex(r"$\Rightarrow$ three arcs give a proper 3-coloring", font_size=28, color=GREEN_3B),
            Tex(r"satisfying labeling: read off the phase", font_size=28),
            Tex(r"of the chosen answer (never stretches", font_size=28),
            Tex(r"distances) and color by arc", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.3, -1.3, 0])
        with self.say("Now the new graph. {v}Each vertex is a point that assigns a phase, a position on a circle, "
                      "to every possible answer of a tuple of questions. {e}Two vertices are joined when one is "
                      "within one eighth of the other, shifted by half a turn. {c}With a single coordinate, that is "
                      "this graph: points on a circle, joined when nearly opposite. "
                      "{a}Cut the circle into three equal arcs. Joined points are at least three eighths apart, "
                      "more than a third, so they never share an arc. "
                      "{s}When the formula is satisfiable, a correct labeling picks one answer for each tuple. "
                      "Reading off that answer's phase maps the whole graph onto this circle without stretching "
                      "distances, and the three arcs color every vertex.") as s:
            self.play(Write(hdr))
            s.wait_until("v")
            self.play(FadeIn(rule[0]))
            s.wait_until("e")
            self.play(Write(rule[1]))
            s.wait_until("c")
            self.play(Create(circ), FadeIn(cd_), FadeIn(side[0]))
            self.play(Create(ce), run_time=2.5)
            s.wait_until("a")
            self.play(Create(arcs), FadeIn(side[1]), run_time=1.5)
            self.play(*[d.animate.set_color(PAL[int(k)]) for d, k in zip(cd_, ARC)], FadeIn(side[2]))
            s.wait_until("s")
            self.play(FadeIn(side[3:]), run_time=1.5)
        self.play(FadeOut(VGroup(hdr, rule, circ, cd_, ce, arcs, side)))

        # ------------------------------------------------------------ soundness
        hdr = Tex(r"Unsatisfiable $\Rightarrow$ every independent set is tiny", font_size=40,
                  color=YELLOW_3B).to_edge(UP, buff=0.35)
        S = 3.6
        sq0 = np.array([-4.3, -0.6, 0])

        def tp(u, v):
            return sq0 + S * np.array([u - 0.5, v - 0.5, 0])

        sq = Square(S, color=GREY_B).move_to(sq0)
        band = Rectangle(width=S / 3, height=S, stroke_width=0, fill_color=BLUE_3B, fill_opacity=0.35).move_to(
            tp(1 / 6, 0.5))
        k1 = MathTex(r"\text{phase of answer }k", font_size=26).next_to(sq, DOWN, buff=0.15)
        k2 = MathTex(r"\text{answer }k'", font_size=26).rotate(PI / 2).next_to(sq, LEFT, buff=0.15)
        x0 = (0.2, 0.2)
        xd = Dot(tp(*x0), color=WHITE)
        xl = MathTex("x", font_size=30).next_to(xd, LEFT, buff=0.08)
        tx = (x0[0] + 0.5, x0[1] + 0.5)
        txd = Dot(tp(*tx), color=RED_3B)
        nb_ = Square(S / 4, color=RED_3B, stroke_width=2).move_to(tp(*tx))
        txl = MathTex(r"x+\tfrac12", font_size=28, color=RED_3B).next_to(nb_, UP, buff=0.08)
        harr = Arrow(tp(*x0), tp(*tx), buff=0.1, color=RED_3B, stroke_width=3)
        bl = Tex(r"a large independent set\\ that names answer $k$", font_size=26, color=BLUE_3B).next_to(
            sq, UP, buff=0.15)
        steps = VGroup(
            Tex(r"independent set $\Rightarrow$ a bounded, Lipschitz function", font_size=28),
            Tex(r"that flips sign under the half-turn", font_size=28),
            Tex(r"Austin's dimension-free junta theorem:", font_size=28, color=TEAL_3B),
            Tex(r"close to a function of boundedly many answers", font_size=28, color=TEAL_3B),
            Tex(r"short answer lists along chains must agree", font_size=28),
            Tex(r"$\Rightarrow$ answers passing many Label Cover tests", font_size=28),
            Tex(r"value $\le\sigma$ $\Rightarrow$ density $<\delta$", font_size=30, color=GREEN_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([2.6, -0.5, 0])
        with self.say("The hard part is the other direction: if the formula is unsatisfiable, every independent "
                      "set must be tiny. {d}With many answers, there are natural large independent sets: "
                      "all points whose phase at one answer, k, lies in a fixed arc. {n}Half a turn moves every such "
                      "point out of the band, so no edges stay inside. This set names the answer k. "
                      "{j}The proof shows that every large independent set behaves somewhat like this. "
                      "It yields a bounded, Lipschitz function that flips sign under the half turn. "
                      "{au}By Tim Austin's dimension-free junta theorem, a continuous cousin of "
                      f"{FRIED}'s, such a function is close to one that depends on only boundedly many answers. "
                      "{dec}Short answer lists along a chain must then agree, which yields answers passing many "
                      "Label Cover tests. {fin}A Ramsey-style alignment lemma makes this quantitative: "
                      "if the Label Cover value is tiny, the independent set has density below delta.") as s:
            self.play(Write(hdr))
            s.wait_until("d")
            self.play(Create(sq), FadeIn(k1), FadeIn(k2))
            self.play(FadeIn(band), FadeIn(bl))
            s.wait_until("n")
            self.play(FadeIn(xd), FadeIn(xl))
            self.play(GrowArrow(harr), FadeIn(txd), Create(nb_), FadeIn(txl))
            extra = VGroup()
            for (u, v) in [(0.08, 0.68), (0.28, 0.9)]:
                d0 = Dot(tp(u, v), color=WHITE, radius=0.06)
                tu, tv = (u + 0.5) % 1, (v + 0.5) % 1
                extra.add(d0, Dot(tp(tu, tv), color=RED_3B, radius=0.06),
                          Square(S / 4, color=RED_3B, stroke_width=1.5).move_to(tp(tu, tv)))
            self.play(FadeIn(extra), run_time=1)
            s.wait_until("j")
            self.play(FadeIn(steps[0:2]))
            s.wait_until("au")
            self.play(FadeIn(steps[2:4]))
            s.wait_until("dec")
            self.play(FadeIn(steps[4:6]))
            s.wait_until("fin")
            self.play(FadeIn(steps[6]))
        self.play(FadeOut(VGroup(hdr, sq, band, k1, k2, xd, xl, txd, nb_, txl, harr, bl, steps, extra)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"For every fixed $0<\delta<1/3$: NP-hard to distinguish 3-colorable graphs",
             r"\qquad from graphs with no independent set of size $\delta n$",
             r"$\Rightarrow$ $c$-coloring a 3-colorable graph is NP-hard for every fixed $c\ge 3$",
             r"Manuscript: 21 pages, produced by an OpenAI model"],
            True, r"\emph{Hardness of finding large independent sets}\\ \emph{in three-colorable graphs} (Sept.\ 2026)")
        with self.say("The graph is built from finite rational data, so the reduction is deterministic and runs in "
                      "polynomial time. {l}The main theorem, the reduction from three SAT with its three-colorable "
                      "completeness, its independent-set soundness and its polynomial running time, has been "
                      "formalized in the Lean proof assistant.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
