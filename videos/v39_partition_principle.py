import numpy as np
from manim import *

from style import *
from vo import NarratedScene

GODEL = "[Gödel](/ɡˈɜdəl/)"
LEVI = "[Beppo Levi](/bˈɛpO lˈɛvi/)"
ZF = "[ZF](/zˈi ˈɛf/)"
ZFC = "[ZFC](/zˈi ˈɛf sˈi/)"

FIB = [BLUE_3B, TEAL_3B, GREEN_3B, ORANGE_3B, PURPLE_3B]


def shoe(color, letter):
    body = RoundedRectangle(width=0.42, height=0.75, corner_radius=0.18, stroke_color=color, stroke_width=3)
    body.set_fill(color, 0.25)
    t = Tex(letter, font_size=24, color=color).move_to(body)
    return VGroup(body, t)


def sock(color):
    leg = Rectangle(width=0.3, height=0.55, stroke_color=color, stroke_width=3).set_fill(color, 0.25)
    foot = RoundedRectangle(width=0.5, height=0.26, corner_radius=0.12, stroke_color=color, stroke_width=3)
    foot.set_fill(color, 0.25).next_to(leg, DOWN, buff=-0.05).align_to(leg, LEFT)
    return VGroup(leg, foot)


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "244", r"The Partition Principle Does Not Imply Choice",
                          r"Comparing sizes is weaker than choosing representatives")
        with self.say("Can you compare the sizes of sets without making choices?"):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ hook: a surjection and its fibers
        rng = np.random.default_rng(4)
        sizes = [4, 3, 5, 2, 4]
        fibers = VGroup()
        ycen = np.linspace(2.0, -2.2, 5)
        for k, (n, yc) in enumerate(zip(sizes, ycen)):
            g = VGroup(*[Dot([-4.6 + 0.5 * i + rng.uniform(-0.08, 0.08), yc + rng.uniform(-0.15, 0.15), 0],
                             radius=0.09, color=FIB[k]) for i in range(n)])
            fibers.add(g)
        boxes = VGroup(*[SurroundingRectangle(f, buff=0.15, corner_radius=0.12, color=FIB[k], stroke_width=2)
                         for k, f in enumerate(fibers)])
        ys = VGroup(*[Dot([3.2, yc, 0], radius=0.12, color=FIB[k]) for k, yc in enumerate(ycen)])
        arr = VGroup(*[Arrow(boxes[k].get_right(), ys[k].get_left(), buff=0.15, color=FIB[k], stroke_width=3)
                       for k in range(5)])
        Xl = MathTex("X", font_size=48).next_to(boxes, UP, buff=0.3)
        Yl = MathTex("Y", font_size=48).next_to(ys, UP, buff=0.3).match_y(Xl)
        fl = MathTex(r"f:X\twoheadrightarrow Y", font_size=40).move_to(UP * 3.3)
        reps = VGroup(*[Circle(radius=0.17, color=YELLOW_3B, stroke_width=4).move_to(f[-1]) for f in fibers])
        back = VGroup(*[CurvedArrow(ys[k].get_left() + LEFT * 0.05, fibers[k][-1].get_center() + RIGHT * 0.2,
                                    angle=0.6, color=YELLOW_3B, stroke_width=3, tip_length=0.15) for k in range(5)])
        inj = MathTex(r"j:Y\hookrightarrow X", font_size=40, color=YELLOW_3B).next_to(ys, RIGHT, buff=0.5)
        with self.say("Suppose a set X maps onto a set Y. {fib}The map splits X into pieces, one for each point of "
                      "Y. {inv}Then surely Y is no bigger than X. Just pick one point from each piece, {rep}and "
                      "you get a one-to-one map from Y back into X. {c}But picking, for infinitely many pieces at "
                      "once, is exactly what the Axiom of Choice is needed for.") as s:
            self.play(FadeIn(fl), FadeIn(fibers), FadeIn(ys), FadeIn(Xl), FadeIn(Yl))
            self.play(LaggedStart(*[GrowArrow(a) for a in arr], lag_ratio=0.15), run_time=1.5)
            s.wait_until("fib")
            self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.15), run_time=1.5)
            s.wait_until("rep")
            self.play(LaggedStart(*[Create(r) for r in reps], lag_ratio=0.15), run_time=1.2)
            self.play(arr.animate.set_opacity(0.25), LaggedStart(*[Create(b) for b in back], lag_ratio=0.15),
                      FadeIn(inj), run_time=1.5)
            s.wait_until("c")
            self.play(Indicate(reps, color=RED_3B, scale_factor=1.3), run_time=1.5)
        self.play(FadeOut(VGroup(fibers, boxes, ys, arr, Xl, Yl, fl, reps, back, inj)))

        # ------------------------------------------------------------ the axiom of choice: shoes and socks
        ac = Tex(r"\textbf{Axiom of Choice}: from any family of nonempty sets,\\ one can choose an element of each",
                 font_size=38, color=YELLOW_3B).to_edge(UP, buff=0.45)
        shoes = VGroup(*[VGroup(shoe(BLUE_3B, "L"), shoe(BLUE_3B, "R")).arrange(RIGHT, buff=0.12) for _ in range(6)]
                       ).arrange(RIGHT, buff=0.5).shift(UP * 0.4)
        socks = VGroup(*[VGroup(sock(TEAL_3B), sock(TEAL_3B)).arrange(RIGHT, buff=0.15) for _ in range(6)]
                       ).arrange(RIGHT, buff=0.42).shift(DOWN * 1.7)
        sh_l = Tex(r"shoes: ``take the left one''", font_size=30).next_to(shoes, UP, buff=0.25)
        so_l = Tex(r"socks: no rule tells the two apart", font_size=30).next_to(socks, UP, buff=0.25)
        dots1 = MathTex(r"\cdots", font_size=40).next_to(shoes, RIGHT, buff=0.3)
        dots2 = MathTex(r"\cdots", font_size=40).next_to(socks, RIGHT, buff=0.3)
        picks = VGroup(*[SurroundingRectangle(p[0], color=YELLOW_3B, buff=0.06) for p in shoes])
        ind = Tex(r"G\"odel (1938), Cohen (1963): Choice is independent of the axioms ZF", font_size=32,
                  color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.say("The Axiom of Choice says that from any family of nonempty sets, you can choose one element "
                      "of each. {sh}Bertrand Russell's illustration: from infinitely many pairs of shoes, you can "
                      "choose without the axiom. Take the left shoe every time. {so}From infinitely many pairs of "
                      "socks, you can't: nothing distinguishes one sock in a pair from the other. "
                      f"{{z}}{GODEL} and Cohen showed that Choice can be neither proved nor refuted from the other "
                      f"axioms of set theory, called {ZF}.") as s:
            self.play(Write(ac), run_time=2)
            s.wait_until("sh")
            self.play(FadeIn(shoes), FadeIn(sh_l), FadeIn(dots1))
            self.play(LaggedStart(*[Create(p) for p in picks], lag_ratio=0.1))
            s.wait_until("so")
            self.play(FadeIn(socks), FadeIn(so_l), FadeIn(dots2))
            s.wait_until("z")
            self.play(FadeIn(ind))
        self.play(FadeOut(VGroup(ac, shoes, socks, sh_l, so_l, dots1, dots2, picks, ind)))

        # ------------------------------------------------------------ the partition principle
        pp = VGroup(
            Tex(r"\textbf{Partition Principle (PP)}", font_size=42, color=YELLOW_3B),
            MathTex(r"X\twoheadrightarrow Y\ \Longrightarrow\ Y\hookrightarrow X", font_size=48),
            Tex(r"every partition of a set is no bigger than the set", font_size=32, color=GREY_A),
        ).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.8)
        imp = VGroup(
            MathTex(r"\text{AC}\ \Longrightarrow\ \text{PP}", font_size=44, color=GREEN_3B),
            MathTex(r"\text{PP}\ \overset{?}{\Longrightarrow}\ \text{AC}", font_size=44, color=ORANGE_3B),
        ).arrange(RIGHT, buff=2.0).next_to(pp, DOWN, buff=0.7)
        note = Tex(r"the injection need not pick a point from each part", font_size=32).next_to(imp, DOWN, buff=0.5)
        hist = VGroup(
            Tex(r"traced back to Beppo Levi, 1902", font_size=30, color=GREY_A),
            Tex(r"classical: PP $\Rightarrow$ Choice for wellorderable families (Pincus)", font_size=30, color=GREY_A),
        ).arrange(DOWN, buff=0.2).next_to(note, DOWN, buff=0.5)
        with self.say("The Partition Principle drops the picking and keeps only the comparison of sizes. Whenever X "
                      "maps onto Y, there is a one-to-one map from Y into X. {ac}Choice implies it. {conv}But the "
                      "map it promises doesn't have to land in the right pieces; it can send points anywhere. "
                      f"{{q}}So does the Partition Principle imply Choice? {{h}}The principle goes back to "
                      f"{LEVI} in 1902, and it already gives choice for wellorderable families. But whether it "
                      "gives full Choice has been a well-known open problem in set theory.") as s:
            self.play(FadeIn(pp[0]), Write(pp[1]), run_time=2)
            self.play(FadeIn(pp[2]))
            s.wait_until("ac")
            self.play(FadeIn(imp[0]))
            s.wait_until("conv")
            self.play(FadeIn(note))
            s.wait_until("q")
            self.play(FadeIn(imp[1]))
            s.wait_until("h")
            self.play(FadeIn(hist), run_time=1.5)
        self.play(FadeOut(VGroup(pp, imp, note, hist)))

        thm = VGroup(Tex(r"\textbf{Theorem.} If ZF is consistent, then so is", font_size=40),
                     MathTex(r"\mathrm{ZF}+\mathrm{PP}+\mathrm{AC}_{\mathrm{WO}}+\neg\mathrm{AC}", font_size=50)
                     ).arrange(DOWN, buff=0.3)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.35)).shift(UP * 0.9)
        sub = Tex(r"$\mathrm{AC}_{\mathrm{WO}}$: choice for ordinal-indexed families", font_size=30,
                  color=GREY_A).next_to(tb, DOWN, buff=0.35)
        t2 = Tex(r"also: a transitive symmetric model over any countable transitive model of ZFC,\\ with the same "
                 r"ordinals and no new countable sequences of ground elements", font_size=30).next_to(sub, DOWN,
                                                                                                    buff=0.5)
        with self.say("A forty-four page manuscript in OpenAI's math catalogue, not yet peer reviewed, claims the "
                      f"answer is no. {{t}}If {ZF} is consistent, then so is {ZF} together with the Partition "
                      "Principle, choice for wellorderable families, and the failure of the Axiom of Choice. "
                      f"{{t2}}A second version builds such a model directly on top of any countable transitive "
                      f"model of {ZFC}.") as s:
            s.wait_until("t")
            self.play(Write(tb), run_time=2.5)
            self.play(FadeIn(sub))
            s.wait_until("t2")
            self.play(FadeIn(t2))
        self.play(FadeOut(VGroup(tb, sub, t2)))

        # ------------------------------------------------------------ symmetric models
        hdr = Tex(r"A symmetric model", font_size=42, color=YELLOW_3B).to_edge(UP, buff=0.35)
        N = 12
        lab_pts = [np.array([-5.5 + k * 1.0, 1.2, 0]) for k in range(N)]
        labels = VGroup(*[Dot(p, radius=0.15, color=BLUE_3B) for p in lab_pts])
        Al = MathTex(r"A=\{\text{generic subsets of }\omega_1\}", font_size=36).next_to(labels, UP, buff=0.35)
        supp = SurroundingRectangle(VGroup(*labels[1:4]), color=TEAL_3B, buff=0.15, corner_radius=0.1)
        sl = Tex("support", font_size=28, color=TEAL_3B).next_to(supp, DOWN, buff=0.15)
        swap = CurvedDoubleArrow(lab_pts[7] + DOWN * 0.22, lab_pts[10] + DOWN * 0.22, angle=0.9, color=ORANGE_3B,
                                 tip_length=0.18)
        rule = VGroup(
            Tex(r"a set survives if some small support fixes it:", font_size=32),
            Tex(r"unchanged by every permutation of the other labels", font_size=32),
        ).arrange(DOWN, buff=0.15).move_to(DOWN * 0.7)
        wo = MathTex(r"a_1<a_2<a_3<\cdots", font_size=40).move_to(DOWN * 2.2 + LEFT * 2.6)
        wo2 = Tex(r"a wellordering of $A$: moved by swapping\\ two labels outside its support", font_size=30,
                  color=RED_3B).next_to(wo, RIGHT, buff=0.6)
        nac = Tex(r"$\Rightarrow$ $A$ cannot be wellordered, so Choice fails", font_size=34, color=YELLOW_3B
                  ).to_edge(DOWN, buff=0.35)
        with self.say("The tool is a symmetric model, the method Cohen used to break Choice. {a}Force new generic "
                      "objects into the universe; here, a set A of labels, which are generic subsets of omega one. "
                      "{s}Then keep only the sets whose descriptions are pinned down by a small support of labels: "
                      "left unchanged by every permutation that fixes the support. {w}No wellordering of A survives this test. "
                      "Swapping two labels outside its support would change it. {n}So in this model, A cannot be "
                      "wellordered, and Choice fails.") as s:
            self.play(Write(hdr))
            s.wait_until("a")
            self.play(FadeIn(labels), FadeIn(Al))
            s.wait_until("s")
            self.play(Create(supp), FadeIn(sl), FadeIn(rule))
            self.play(Create(swap), Swap(labels[7], labels[10]), run_time=1.5)
            s.wait_until("w")
            self.play(FadeIn(wo), FadeIn(wo2))
            s.wait_until("n")
            self.play(FadeIn(nac))
        self.play(FadeOut(VGroup(labels, Al, supp, sl, swap, rule, wo, wo2, nac)))

        # ------------------------------------------------------------ the key property
        A_pts = [np.array([-5.8 + 0.42 * k, 1.5, 0]) for k in range(28)]
        cls = [k % 7 for k in range(28)]
        cls = [0, 0, 1, 2, 1, 3, 3, 4, 2, 5, 6, 5, 0, 4, 6, 1, 2, 3, 6, 5, 4, 0, 1, 2, 3, 4, 5, 6]
        ccol = [BLUE_3B, TEAL_3B, GREEN_3B, ORANGE_3B, PURPLE_3B, RED_3B, YELLOW_3B]
        Ad = VGroup(*[Dot(p, radius=0.1, color=GREY_A) for p in A_pts])
        Adots = MathTex(r"\cdots", font_size=36).next_to(Ad, RIGHT, buff=0.2)
        Alab = MathTex("A", font_size=40).next_to(Ad, LEFT, buff=0.3)
        Q = VGroup(*[Dot([-2.5 + 0.8 * k, -0.6, 0], radius=0.16, color=ccol[k]) for k in range(7)])
        Qdots = MathTex(r"\cdots", font_size=36).next_to(Q, RIGHT, buff=0.2)
        Qlab = MathTex("A/E", font_size=40).next_to(Q, LEFT, buff=0.3)
        lines_ = VGroup(*[Line(A_pts[k] + DOWN * 0.1, Q[cls[k]].get_center() + UP * 0.16, color=ccol[cls[k]],
                               stroke_width=1.5, stroke_opacity=0.6) for k in range(28)])
        key = VGroup(
            Tex(r"\textbf{Key property:} every surjective image of $A$", font_size=34),
            Tex(r"that cannot be wellordered is in bijection with $A$", font_size=34),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=1.3)
        bij = MathTex(r"A/E\ \cong\ A", font_size=44, color=YELLOW_3B).next_to(key, DOWN, buff=0.3)
        pres = Tex(r"and every set in the model is an image of $A\times\eta$, $\eta$ an ordinal", font_size=30,
                   color=GREY_A).to_edge(UP, buff=0.9)
        with self.say("Everything in this model is an image of A times an ordinal. {k}And the paper's central "
                      "property is this. {c}Collapse A by any equivalence relation. {b}If what remains cannot be "
                      "wellordered, it is in bijection with A itself: collapsing never makes A smaller, unless it "
                      "makes it wellorderable.") as s:
            self.play(FadeIn(pres))
            s.wait_until("k")
            self.play(FadeIn(Ad), FadeIn(Adots), FadeIn(Alab))
            s.wait_until("c")
            self.play(*[Ad[k].animate.set_color(ccol[cls[k]]) for k in range(28)])
            self.play(Create(lines_), FadeIn(Q), FadeIn(Qdots), FadeIn(Qlab), run_time=1.5)
            s.wait_until("b")
            self.play(FadeIn(key))
            self.play(Write(bij))
        self.play(FadeOut(VGroup(Ad, Adots, Alab, Q, Qdots, Qlab, lines_, key, bij, pres)))

        # ------------------------------------------------------------ from the property to PP: slicing
        hdr2 = Tex(r"From the key property to PP", font_size=42, color=YELLOW_3B).to_edge(UP, buff=0.35)
        ncol = 4
        cols = VGroup()
        tags = VGroup()
        kinds = ["wo", "A", "A", "wo"]
        for i in range(ncol):
            x = -4.5 + 3.0 * i
            Si = RoundedRectangle(width=1.6, height=1.3, corner_radius=0.15, color=FIB[i], stroke_width=3
                                  ).set_fill(FIB[i], 0.2).move_to([x, 1.0, 0])
            Yi = RoundedRectangle(width=1.2, height=0.9, corner_radius=0.15, color=FIB[i], stroke_width=3
                                  ).set_fill(FIB[i], 0.2).move_to([x, -1.2, 0])
            ar = Arrow(Si.get_bottom(), Yi.get_top(), buff=0.08, color=FIB[i], stroke_width=3)
            ls = MathTex(f"S_{i}", font_size=32).move_to(Si)
            ly = MathTex(f"Y_{i}", font_size=32).move_to(Yi)
            cols.add(VGroup(Si, Yi, ar, ls, ly))
            if kinds[i] == "wo":
                t = Tex(r"wellorderable:\\ choose", font_size=26, color=GREEN_3B)
            else:
                t = Tex(r"both $\cong A$:\\ inject", font_size=26, color=TEAL_3B)
            tags.add(t.next_to(Yi, DOWN, buff=0.25))
        Xb = MathTex(r"X", font_size=40).move_to([-6.3, 1.0, 0])
        Yb = MathTex(r"Y", font_size=40).move_to([-6.3, -1.2, 0])
        dots = MathTex(r"\cdots", font_size=40).move_to([6.3, 0, 0])
        glue = Tex(r"glue the pieces, choosing once more over an ordinal-indexed family", font_size=32,
                   color=YELLOW_3B).to_edge(DOWN, buff=0.45)
        with self.say("From there, the Partition Principle follows by slicing. {sl}Given a map from X onto Y, "
                      "cut X into pieces, each an image of A, that map onto disjoint pieces of Y. {w}Where a piece "
                      "of Y can be wellordered, choose directly, using choice for wellorderable families. {a}Where "
                      "it can't, both pieces are in bijection with A, so one injects into the other. {g}Then glue "
                      "all the pieces together.") as s:
            self.play(FadeOut(hdr), FadeIn(hdr2))
            s.wait_until("sl")
            self.play(FadeIn(Xb), FadeIn(Yb), LaggedStart(*[FadeIn(c) for c in cols], lag_ratio=0.25), FadeIn(dots),
                      run_time=2)
            s.wait_until("w")
            self.play(FadeIn(tags[0]), FadeIn(tags[3]))
            s.wait_until("a")
            self.play(FadeIn(tags[1]), FadeIn(tags[2]))
            s.wait_until("g")
            self.play(FadeIn(glue))
        self.play(FadeOut(VGroup(hdr2, cols, tags, Xb, Yb, dots, glue)))

        # ------------------------------------------------------------ the hard part
        hdr3 = Tex(r"The hard part: symmetric bijections", font_size=42, color=YELLOW_3B).to_edge(UP, buff=0.35)
        rects = VGroup(
            Rectangle(width=2.8, height=1.8, color=BLUE_3B).set_fill(BLUE_3B, 0.15).move_to([-4.7, 0.7, 0]),
            Rectangle(width=2.8, height=1.8, color=TEAL_3B).set_fill(TEAL_3B, 0.15).move_to([-3.4, -0.3, 0]),
            Rectangle(width=2.6, height=1.5, color=PURPLE_3B).set_fill(PURPLE_3B, 0.15).move_to([-5.0, -1.2, 0]),
        )
        for r_, nm, cr in zip(rects, ["J_1", "J_2", "J_3"], [UL, DR, DL]):
            rects.add(MathTex(nm, font_size=30, color=r_.get_color()).move_to(r_.get_corner(cr) + (-cr) * 0.3))
        rl = Tex(r"overlapping supports must agree", font_size=28, color=GREY_A).next_to(rects, DOWN, buff=0.3)
        steps = VGroup(
            Tex(r"\textbf{1.} a monoid of \emph{diagrams}\\ controls how supports overlap", font_size=30),
            Tex(r"\textbf{2.} exact counts: \emph{availability fibers}\\ of labels and of quotient elements\\ "
                r"have matching sizes", font_size=30),
            Tex(r"\textbf{3.} countable chains and Cohen\\ generic sets make the choices coherent", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(RIGHT * 2.9 + DOWN * 0.1)
        with self.say("The real difficulty is that these bijections must themselves belong to the symmetric model. "
                      "{ov}Bijections chosen on different supports have to agree where the supports overlap, and "
                      "respect every permutation in sight. {s1}The paper builds a special monoid of diagrams that "
                      "controls exactly how supports can overlap. {s2}It shows that, pattern by pattern, the "
                      "available labels and quotient elements come in fibers of exactly the same size. {s3}And it "
                      "uses countable chains and the Cohen generic sets to make all the choices fit together.") as s:
            self.play(Write(hdr3))
            s.wait_until("ov")
            self.play(LaggedStart(*[FadeIn(r) for r in rects], lag_ratio=0.3), FadeIn(rl), run_time=1.5)
            s.wait_until("s1")
            self.play(FadeIn(steps[0]))
            s.wait_until("s2")
            self.play(FadeIn(steps[1]))
            s.wait_until("s3")
            self.play(FadeIn(steps[2]))
        self.play(FadeOut(VGroup(hdr3, rects, rl, steps)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Con(ZF) $\Rightarrow$ Con(ZF $+$ PP $+$ AC$_{\mathrm{WO}}$ $+$ $\neg$AC)",
             r"So the Partition Principle does not imply the Axiom of Choice",
             r"Also a transitive symmetric model over countable transitive models of ZFC",
             r"Manuscript: 44 pages, produced by an OpenAI model"],
            True, r"\emph{The Partition Principle does not imply Choice} (Sept.\ 2026)")
        with self.say("The manuscript was written by an OpenAI model, {l}and the relative consistency theorem has "
                      "been formalized in the Lean proof assistant. The paper's stronger claims about transitive "
                      "models go beyond the formalized statements. If it holds, comparing sizes really is weaker "
                      "than choosing.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
