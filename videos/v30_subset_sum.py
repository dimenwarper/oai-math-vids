import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(__file__.replace("v30_subset_sum.py", "data/v30.npz"))
A = [int(v) for v in D["A"]]
TGT = int(D["T"])
LV = [int(v) for v in D["Lv"]]
RV = [int(v) for v in D["Rv"]]
TRACE = D["trace"]
PR = int(D["P"])
PH = D["ph"]
IS_AL = D["is_alias"]
SV = [int(v) for v in D["Sv"]]
STRUCT = [int(v) for v in D["STRUCT"]]

HS = "[Horowitz](/hˈɔɹəwɪts/)"
SAHNI = "[Sahni](/sˈɑni/)"
SCHR = "[Schroeppel](/ʃɹˈɛpəl/)"
SHAMIR = "[Shamir](/ʃəmˈiɹ/)"
SERV = "[Servedio](/səɹvˈAdiˌO/)"
MVV = "[Mulmuley](/mʊlmˈuli/), [Vazirani](/vˌɑzɪɹˈɑni/) and [Vazirani](/vˌɑzɪɹˈɑni/)"


def num_box(v, color, fs=30, w=0.78, h=0.56):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=color, stroke_width=2.5)
    r.set_fill(color, 0.12)
    return VGroup(r, MathTex(str(v), font_size=fs).move_to(r))


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "138", r"Subset Sum in $O(2^{0.49n})$",
                          r"Beating meet-in-the-middle's $2^{n/2}$ on every input")
        with self.say("Subset Sum, faster than meet in the middle."):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ the problem
        boxes = VGroup(*[num_box(v, GREY_B, fs=36, w=0.95, h=0.7) for v in A]).arrange(RIGHT, buff=0.25)
        boxes.shift(UP * 1.6)
        tl = MathTex(r"t = %d" % TGT, font_size=48, color=YELLOW_3B).next_to(boxes, DOWN, buff=0.7)
        q = Tex(r"Is there a subset that adds up to exactly $t$?", font_size=36).next_to(tl, DOWN, buff=0.5)
        tries = [(0, 2, 5), (1, 3, 4, 6), (2, 4, 5, 7)]
        sol = [i for i in range(8) if i in (0, 1, 4, 7)]
        cnt = MathTex(r"2^8=256\text{ subsets}\qquad 2^{n}\text{ in general}", font_size=38, color=GREY_A).to_edge(
            DOWN, buff=0.6)
        with self.say("Here are eight numbers, and a target, one hundred and three. "
                      "{q}Is there a subset of the numbers that adds up to exactly the target? "
                      "{try}You could simply try them all. {s}This one works: twenty-eight, nine, fifty-nine and seven. "
                      "{c}But n numbers have two to the n subsets, so brute force doubles with every number you add. "
                      "{np}This is Subset Sum, a form of the knapsack problem from Karp's original list of "
                      "NP-complete problems. Nobody expects a polynomial-time algorithm. "
                      "The real question is how far below two to the n we can go.") as s:
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in boxes], lag_ratio=0.08), run_time=1.5)
            self.play(Write(tl))
            s.wait_until("q")
            self.play(FadeIn(q))
            s.wait_until("try")
            for tr in tries:
                tot = sum(A[i] for i in tr)
                lab = MathTex(r"= %d" % tot, font_size=40, color=RED_3B).next_to(tl, RIGHT, buff=0.6)
                self.play(*[boxes[i][0].animate.set_fill(RED_3B, 0.5) for i in tr], FadeIn(lab), run_time=0.5)
                self.wait(0.3)
                self.play(*[boxes[i][0].animate.set_fill(GREY_B, 0.12) for i in tr], FadeOut(lab), run_time=0.3)
            s.wait_until("s")
            lab = MathTex(r"28+9+59+7=103", font_size=40, color=GREEN_3B).next_to(tl, RIGHT, buff=0.6)
            self.play(*[boxes[i][0].animate.set_fill(GREEN_3B, 0.55) for i in sol], FadeIn(lab), run_time=0.8)
            s.wait_until("c")
            self.play(FadeIn(cnt))
        self.play(FadeOut(VGroup(q, cnt, lab, tl)), *[boxes[i][0].animate.set_fill(GREY_B, 0.12) for i in sol])

        # ------------------------------------------------------------ meet in the middle
        left_b, right_b = boxes[:4], boxes[4:]
        self.play(boxes.animate.scale(0.8).to_edge(UP, buff=0.3))
        self.play(left_b.animate.shift(LEFT * 0.5), right_b.animate.shift(RIGHT * 0.5))
        self.play(*[b[0].animate.set_stroke(BLUE_3B).set_fill(BLUE_3B, 0.15) for b in left_b],
                  *[b[0].animate.set_stroke(YELLOW_3B).set_fill(YELLOW_3B, 0.15) for b in right_b])
        sp = 0.37
        y0 = 2.35
        lcol = VGroup(*[MathTex(str(v), font_size=28, color=BLUE_3B).move_to([-4.6, y0 - k * sp, 0])
                        for k, v in enumerate(LV)])
        rv_desc = RV[::-1]
        rcol = VGroup(*[MathTex(str(v), font_size=28, color=YELLOW_3B).move_to([-2.2, y0 - k * sp, 0])
                        for k, v in enumerate(rv_desc)])
        lh = Tex(r"left sums", font_size=26, color=BLUE_3B).next_to(lcol, LEFT, buff=0.35).shift(UP * 2.4)
        rh = Tex(r"right sums", font_size=26, color=YELLOW_3B).next_to(rcol, RIGHT, buff=0.35).shift(UP * 2.4)
        lsz = MathTex(r"2^{n/2}", font_size=30, color=BLUE_3B).next_to(lh, DOWN, buff=0.15)
        rsz = MathTex(r"2^{n/2}", font_size=30, color=YELLOW_3B).next_to(rh, DOWN, buff=0.15)
        hdr = Tex(r"Meet in the middle\\(Horowitz--Sahni, 1974)", font_size=34, color=YELLOW_3B).move_to(
            [3.4, 2.1, 0])
        with self.say(f"In 1974, {HS} and {SAHNI} found the classic shortcut: meet in the middle. "
                      "{split}Split the numbers into two halves. "
                      "{lists}List all sixteen subset sums of the left half, and all sixteen of the right half: "
                      "two to the n over two each, in sorted order.") as s:
            self.play(FadeIn(hdr))
            s.wait_until("lists")
            self.play(FadeIn(lh), FadeIn(lsz), LaggedStart(*[FadeIn(m) for m in lcol], lag_ratio=0.06), run_time=2)
            self.play(FadeIn(rh), FadeIn(rsz), LaggedStart(*[FadeIn(m) for m in rcol], lag_ratio=0.06), run_time=2)

        lp = Triangle(color=BLUE_3B, fill_opacity=1).scale(0.1).rotate(-PI / 2)
        rp = Triangle(color=YELLOW_3B, fill_opacity=1).scale(0.1).rotate(PI / 2)
        rule = VGroup(Tex(r"sum $<t$: move left pointer down", font_size=28),
                      Tex(r"sum $>t$: move right pointer down", font_size=28)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.4, 0.7, 0])
        with self.say("Now look for a left sum and a right sum that add to the target. "
                      "{p}Start at the smallest left sum and the largest right sum. "
                      "{r}If the total is too small, step down the left list. If it is too big, step down the right list. "
                      "{f}Each step discards one candidate for good, so a single pass "
                      "through both lists finds the pair: thirty-seven plus sixty-six.") as s:
            s.wait_until("p")
            lp.next_to(lcol[0], LEFT, buff=0.15)
            rp.next_to(rcol[0], RIGHT, buff=0.15)
            self.play(FadeIn(lp), FadeIn(rp), FadeIn(rule))
            s.wait_until("r")
            cur = None
            for i, j, sm in TRACE:
                i, j, sm = int(i), int(j), int(sm)
                jj = 15 - j
                col = GREEN_3B if sm == TGT else (BLUE_3B if sm < TGT else YELLOW_3B)
                rel = "=" if sm == TGT else ("<" if sm < TGT else ">")
                new = MathTex(r"%d+%d=%d\ %s\ t" % (LV[i], RV[j], sm, rel), font_size=38, color=col).move_to(
                    [3.4, -0.9, 0])
                anims = [lp.animate.next_to(lcol[i], LEFT, buff=0.15), rp.animate.next_to(rcol[jj], RIGHT, buff=0.15)]
                anims.append(Transform(cur, new) if cur is not None else FadeIn(new))
                if cur is None:
                    cur = new
                self.play(*anims, run_time=0.55)
                self.wait(0.15)
            hl = VGroup(SurroundingRectangle(lcol[4], color=GREEN_3B, buff=0.06),
                        SurroundingRectangle(rcol[15 - 10], color=GREEN_3B, buff=0.06))
            self.play(Create(hl))
        cost = VGroup(Tex(r"time $\approx 2^{n/2}$", font_size=40, color=GREEN_3B),
                      Tex(r"the square root of brute force", font_size=30, color=GREY_A)).arrange(
            DOWN, buff=0.15).move_to([3.4, -2.4, 0])
        with self.say("The cost is about two to the n over two: the square root of brute force. "
                      "{s}With a hundred numbers, that is the difference between two to the hundred "
                      "and two to the fifty.") as s:
            self.play(FadeIn(cost))
        self.play(FadeOut(VGroup(boxes, lcol, rcol, lh, rh, lsz, rsz, hdr, lp, rp, rule, cur, hl, cost)))

        # ------------------------------------------------------------ history
        rows = VGroup(
            Tex(r"1974 \quad Horowitz--Sahni: time $2^{n/2}$", font_size=34),
            Tex(r"1981 \quad Schroeppel--Shamir: same time, memory $2^{n/4}$", font_size=34),
            Tex(r"random inputs: faster ``representation'' methods (not worst case)", font_size=34, color=GREY_A),
            Tex(r"recent: Chen--Jin--Randolph--Servedio, $2^{n/2}/n^{0.5023}$", font_size=34, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(UP * 0.6)
        goal = Tex(r"Lowering the exponent $\tfrac12$ itself, on \emph{every} input?", font_size=38,
                   color=YELLOW_3B).next_to(rows, DOWN, buff=0.7)
        with self.say(f"In 1981, {SCHR} and {SHAMIR} kept the same running time, but cut the memory to two to "
                      "the n over four. {rep}Later methods ran faster on random inputs, but without a guarantee "
                      f"for every input. {{cj}}Recently, Chen, Jin, Randolph and {SERV} shaved a polynomial factor "
                      "off the worst case. {g}Reducing the exponent one half itself, for every input, is a "
                      "different goal, and that is what a new manuscript claims.") as s:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), run_time=1.2)
            s.wait_until("rep")
            self.play(FadeIn(rows[2]))
            s.wait_until("cj")
            self.play(FadeIn(rows[3]))
            s.wait_until("g")
            self.play(Write(goal))
        self.play(FadeOut(VGroup(rows, goal)))

        # ------------------------------------------------------------ the theorem
        thm = VGroup(
            Tex(r"\textbf{Theorem.} A randomized algorithm decides every Subset Sum instance", font_size=34),
            Tex(r"of $n$ integers in $O(2^{0.49n})$ word operations.", font_size=34),
            Tex(r"Correct with probability $\ge 2/3$; the time bound holds on every run;", font_size=28,
                color=GREY_A),
            Tex(r"word RAM, integers with polynomially many bits.", font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.22)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3)).shift(UP * 1.5)
        nl = NumberLine(x_range=[0.45, 1.0, 0.05], length=10, include_numbers=True, font_size=26,
                        decimal_number_config={"num_decimal_places": 2}).shift(DOWN * 1.6)
        nl_l = MathTex(r"\text{exponent } c \text{ in } 2^{cn}", font_size=30).next_to(nl, DOWN, buff=0.45)
        marks = VGroup()
        for v, txt, col in [(1.0, "brute force", RED_3B), (0.5, "1974", BLUE_3B), (0.49, "new", YELLOW_3B)]:
            d = Dot(nl.n2p(v), color=col, radius=0.1)
            lab = Tex(txt, font_size=28, color=col).next_to(d, UP, buff=0.2)
            marks.add(VGroup(d, lab))
        marks[2][1].shift(LEFT * 0.3)
        marks[1][1].shift(RIGHT * 0.3 + UP * 0.35)
        with self.say("Here is the claim. {t}A randomized algorithm decides every instance of n integers in "
                      "order two to the zero point four nine n operations. It is correct with probability at least "
                      "two thirds, its time bound holds on every run, and the integers may have polynomially many bits. "
                      "{nl}On the scale of exponents, it is a small step, from one half to zero point four nine. "
                      "{w}But it is a step in the exponent, worth a factor of two to the n over a hundred, "
                      "on every input.") as s:
            s.wait_until("t")
            self.play(Write(thm[:2]), Create(tb[1]), run_time=2.5)
            self.play(FadeIn(thm[2:]))
            s.wait_until("nl")
            self.play(Create(nl), FadeIn(nl_l))
            self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.2) for m in marks], lag_ratio=0.4), run_time=2)
            s.wait_until("w")
            self.play(Indicate(marks[2], color=YELLOW_3B))
        self.play(FadeOut(VGroup(tb, nl, nl_l, marks)))

        # ------------------------------------------------------------ isolation + dichotomy
        iso = VGroup(Tex(r"\textbf{Step 0.} Random tie-breaking weights: if a solution exists,", font_size=32),
                     Tex(r"some shifted target has \emph{exactly one} (Isolation Lemma)", font_size=32)).arrange(
            DOWN, buff=0.12).to_edge(UP, buff=0.4)
        hd = Tex(r"\textbf{Step 1.} How many \emph{distinct} sums does a random half have?", font_size=32,
                 color=YELLOW_3B).next_to(iso, DOWN, buff=0.45)
        st_all = sorted(SV)
        scol = VGroup(*[MathTex(str(v), font_size=32, color=TEAL_3B) for v in st_all]).arrange_in_grid(
            2, 8, buff=(0.3, 0.3)).move_to([-3.4, 0.0, 0])
        st_l = MathTex(r"\{5,10,15,20\}", font_size=32, color=TEAL_3B).next_to(scol, UP, buff=0.3)
        dist = sorted(set(SV))
        dcol = VGroup(*[MathTex(str(v), font_size=32, color=TEAL_3B) for v in dist]).arrange(RIGHT, buff=0.2)
        dcol.next_to(scol, DOWN, buff=0.55)
        d_l = Tex(r"16 subsets, only 11 sums", font_size=28, color=TEAL_3B).next_to(dcol, DOWN, buff=0.25)
        ocol = VGroup(*[MathTex(str(v), font_size=32, color=BLUE_3B) for v in LV]).arrange_in_grid(
            2, 8, buff=(0.22, 0.3)).move_to([3.4, 0.0, 0])
        o_l = MathTex(r"\{28,9,33,43\}", font_size=32, color=BLUE_3B).next_to(ocol, UP, buff=0.3)
        o_n = Tex(r"16 subsets, 16 sums", font_size=28, color=BLUE_3B).next_to(ocol, DOWN, buff=0.55)
        case1 = Tex(r"few sums $\Rightarrow$ shorter lists:\\ meet in the middle already wins", font_size=28,
                    color=GREEN_3B).move_to([-3.4, -2.9, 0])
        case2 = Tex(r"nearly distinct sums:\\ the hard case", font_size=28, color=RED_3B).move_to([3.4, -2.9, 0])
        with self.say("How does the proof get there? {iso}First, a standard trick: random tie-breaking weights, "
                      f"through the Isolation Lemma of {MVV}, ensure that if a solution exists, "
                      "some slightly shifted target has exactly one. "
                      "{d}Then the proof asks one question: how many distinct sums does a random half of the numbers have? "
                      "{few}If many subsets share the same sum, the lists in meet in the middle shrink once duplicates "
                      "are merged. With at most two to the zero point four nine n distinct sums, "
                      "the old algorithm is already fast enough. {many}So the hard case is when "
                      "the sums are nearly all distinct.") as s:
            s.wait_until("iso")
            self.play(FadeIn(iso))
            s.wait_until("d")
            self.play(FadeIn(hd))
            s.wait_until("few")
            self.play(FadeIn(st_l), FadeIn(scol))
            self.play(*[ReplacementTransform(VGroup(*[scol[k].copy() for k in range(16) if st_all[k] == v]), dcol[d])
                        for d, v in enumerate(dist)], run_time=1.5)
            self.play(FadeIn(d_l), FadeIn(case1))
            s.wait_until("many")
            self.play(FadeIn(o_l), FadeIn(ocol), FadeIn(o_n), FadeIn(case2))
        self.play(FadeOut(VGroup(iso, hd, scol, st_l, dcol, d_l, ocol, o_l, o_n, case1, case2)))

        # ------------------------------------------------------------ phase checksum
        eq = MathTex(r"\sum_{\text{sum}=t}\chi(I)", "=", r"\sum_{\text{sum}\equiv t\ (\mathrm{mod}\ P)}\chi(I)", "-",
                     r"\sum_{\text{aliases}}\chi(I)", font_size=36).to_edge(UP, buff=0.35)
        eq[0].set_color(YELLOW_3B)
        eq[4].set_color(RED_3B)
        chi = MathTex(r"\chi(I)=e^{2\pi i\,\sum_{i\in I}\phi_i/P}", font_size=34).next_to(eq, DOWN, buff=0.3)
        org = np.array([-1.6, 1.6, 0])
        sc = 0.85
        order = [k for k in range(len(PH)) if IS_AL[k]] + [k for k in range(len(PH)) if not IS_AL[k]]
        arrows = VGroup()
        p = org.copy()
        for k in order:
            ang = 2 * np.pi * PH[k] / PR
            q2 = p + sc * np.array([np.cos(ang), np.sin(ang), 0])
            arrows.add(Arrow(p, q2, buff=0, stroke_width=4, color=RED_3B if IS_AL[k] else YELLOW_3B,
                             max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=12))
            p = q2
        n_al = int(IS_AL.sum())
        a_end = arrows[n_al - 1].get_end()
        m_end = arrows[-1].get_end()
        Mv = Arrow(org, m_end, buff=0, color=WHITE, stroke_width=5)
        Av = Arrow(org, a_end, buff=0, color=RED_3B, stroke_width=3).set_opacity(0.7)
        o_dot = Dot(org, color=WHITE)
        side = VGroup(
            Tex(r"prime $P=%d$ (illustration)" % PR, font_size=28, color=GREY_A),
            Tex(r"%d subsets hit $t$ mod $P$" % len(PH), font_size=28),
            Tex(r"%d aliases (red)" % n_al, font_size=28, color=RED_3B),
            Tex(r"1 true solution (yellow)", font_size=28, color=YELLOW_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.6, 0.4, 0])
        Ml = Tex("modular sum", font_size=28).next_to(Mv.get_center(), LEFT, buff=0.35)
        Al = Tex("alias sum", font_size=28, color=RED_3B).next_to(a_end, DOWN, buff=0.2)
        with self.say("For the hard case, the algorithm builds a checksum. {ph}Each number gets a random phase, "
                      "and each subset gets the product of its numbers' phases: a unit arrow, chi of I. "
                      "{ex}Add up the arrows of all subsets that hit the target exactly. With no solution the "
                      "total is zero. With an isolated solution it is a single arrow of length one. "
                      "{mod}Working modulo a random prime P, the total can be estimated. "
                      "{al}But modulo P, impostors also hit the target. Call them aliases. "
                      "{fin}So the exact total is the modular total, minus the aliases. Here, twelve red alias arrows, "
                      "and one yellow solution.") as s:
            s.wait_until("ph")
            self.play(Write(chi))
            s.wait_until("ex")
            self.play(Write(eq[0]))
            s.wait_until("mod")
            self.play(Write(eq[1:3]))
            s.wait_until("al")
            self.play(Write(eq[3:]))
            self.play(FadeIn(o_dot), FadeIn(side[0]))
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows[:n_al]], lag_ratio=0.25), FadeIn(side[1:]),
                      run_time=3)
            s.wait_until("fin")
            self.play(GrowArrow(arrows[n_al]))
            self.play(GrowArrow(Mv), FadeIn(Ml))
            self.play(GrowArrow(Av), FadeIn(Al))
            self.play(Indicate(arrows[n_al], color=YELLOW_3B, scale_factor=1.5))
        thr = VGroup(Tex(r"need error $<\tfrac14$,", font_size=32, color=GREEN_3B),
                     Tex(r"then compare the length with $\tfrac12$", font_size=32, color=GREEN_3B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).next_to(side, DOWN, buff=0.5).align_to(side, LEFT)
        with self.say("Both totals can be large, while the answer is zero or one, so both must be found to "
                      "within an absolute error of a quarter. Then compare with one half.") as s:
            self.play(FadeIn(thr))
        self.play(FadeOut(VGroup(eq, chi, arrows, Mv, Av, o_dot, side, Ml, Al, thr)))

        # ------------------------------------------------------------ the two procedures
        hdr = Tex("Two new procedures, each within $2^{0.49n}$", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.4)
        p1t = Tex(r"\textbf{1. Estimate the modular sum}", font_size=32, color=BLUE_3B)
        p1f = MathTex(r"\frac1P\sum_{k=0}^{P-1} e_P(-kt)\prod_{i=1}^n\big(1+e_P(\phi_i+kc_i)\big)", font_size=34)
        p1a = Tex(r"too many frequencies $k$: write $k=hL+l$,", font_size=28)
        p1b = Tex(r"store short lists of high- and low-digit vectors,", font_size=28)
        p1c = Tex(r"random filters sample matching pairs", font_size=28)
        p1 = VGroup(p1t, p1f, p1a, p1b, p1c).arrange(DOWN, buff=0.22).move_to([-3.4, -0.4, 0])
        p2t = Tex(r"\textbf{2. List every alias}", font_size=32, color=RED_3B)
        p2a = Tex(r"each subset has many representations", font_size=28)
        p2b = Tex(r"as a pair of half-records;", font_size=28)
        p2c = Tex(r"distinct sums $\Rightarrow$ enough of them survive;", font_size=28)
        p2d = Tex(r"a random prime keeps false matches rare", font_size=28)
        p2 = VGroup(p2t, p2a, p2b, p2c, p2d).arrange(DOWN, buff=0.22).move_to([3.5, -0.4, 0])
        div = Line(UP * 2.4, DOWN * 3.2, color=GREY_D)
        with self.say("Two new procedures make this fit in the time budget. {p1}The modular total is a Fourier "
                      "average over P frequencies, far too many to visit, since P is larger than the running time. "
                      "{p1b}So each frequency is split into high and low digits. The algorithm stores two short lists "
                      "of phase vectors, and random filters sample matching pairs. "
                      "A second-moment bound keeps the estimate accurate. "
                      "{p2}The aliases are listed by giving each subset many representations as pairs of half-records. "
                      "{p2b}This is where nearly distinct sums are needed: they guarantee enough representations "
                      "survive to catch every alias. {fin}Subtract, compare with one half, and the instance is decided.") as s:
            self.play(Write(hdr))
            s.wait_until("p1")
            self.play(FadeIn(p1t), Write(p1f), Create(div), run_time=2)
            s.wait_until("p1b")
            self.play(FadeIn(p1a), FadeIn(p1b), FadeIn(p1c), run_time=1.5)
            s.wait_until("p2")
            self.play(FadeIn(p2t), FadeIn(p2a), FadeIn(p2b))
            s.wait_until("p2b")
            self.play(FadeIn(p2c), FadeIn(p2d))
        self.play(FadeOut(VGroup(hdr, p1, p2, div)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Worst-case Subset Sum on $n$ integers in $O(2^{0.49n})$ time",
             r"randomized, success probability $\ge 2/3$, time bound on every run",
             r"word RAM, polynomial-bit inputs",
             r"Manuscript: 33 pages, produced by an OpenAI model"],
            False, r"\emph{Subset Sum in Time $O(2^{0.49n})$} (Oct.\ 2026)")
        with self.say("This manuscript, produced by an OpenAI model, has not been formalized or peer reviewed, "
                      "and it needs careful checking by experts. {c}If it holds, the exponent one half of meet in the "
                      "middle is not the end of the story for worst-case Subset Sum.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("c")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
