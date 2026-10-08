from pathlib import Path

import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(Path(__file__).parent / "data" / "v16.npz")

ERD = "[Erdős](/ˈɛɹdəʃ/)"
MOTZ = "[Motzkin](/mˈɑtskɪn/)"
TSU = "[Tsuchimura](/ʦˌuʧimˈʊɹə/)"
GETH = "[Gethner](/ɡˈɛθnəɹ/)"

ISL = [BLUE_3B, YELLOW_3B, TEAL_3B, RED_3B, GREEN_3B, ORANGE_3B, PURPLE_3B, "#E07BB0", "#7FA7FF", "#C9E265"]


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "028", "The Gaussian Moat Problem",
                          r"Can a walk with bounded steps reach infinity on the Gaussian primes?")
        with self.say("Can you walk to infinity on the Gaussian primes, if every step has bounded length?"):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.4)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ number line warm-up
        nl = NumberLine(x_range=[88, 132, 2], length=12, include_numbers=False, color=GREY_B).shift(UP * 0.3)
        primes = [89, 97, 101, 103, 107, 109, 113, 127, 131]
        pd = VGroup(*[Dot(nl.n2p(p), radius=0.09, color=YELLOW_3B) for p in primes])
        pl = VGroup(*[MathTex(str(p), font_size=28).next_to(nl.n2p(p), DOWN, buff=0.25) for p in primes])
        gap = Line(nl.n2p(113), nl.n2p(127), color=RED_3B, stroke_width=10).shift(UP * 0.35)
        gl = Tex(r"no primes from 114 to 126", font_size=32, color=RED_3B).next_to(gap, UP, buff=0.25)
        fact = MathTex(r"n!+2,\ n!+3,\ \dots,\ n!+n\ \text{ are all composite}", font_size=40).to_edge(DOWN, buff=1.0)
        with self.say("On the number line, the answer is no. {g}Gaps between primes can be as long as you like: "
                      "{f}the numbers n factorial plus two, up to n factorial plus n, are all composite. So a walker "
                      "with any fixed stride eventually gets stuck.") as s:
            self.play(Create(nl), LaggedStart(*[GrowFromCenter(d) for d in pd], lag_ratio=0.1), FadeIn(pl))
            s.wait_until("g")
            self.play(Create(gap), FadeIn(gl))
            s.wait_until("f")
            self.play(Write(fact))
        self.play(FadeOut(VGroup(nl, pd, pl, gap, gl, fact)))

        # ------------------------------------------------------------ the Gaussian primes
        sc = 0.068
        org = LEFT * 3.0 + DOWN * 0.1

        def P(a, b):
            return org + sc * np.array([a, b, 0.0])

        axes = VGroup(Line(P(-53, 0), P(53, 0), color=GREY_D, stroke_width=1.5),
                      Line(P(0, -53), P(0, 53), color=GREY_D, stroke_width=1.5))
        dots = VGroup(*[Dot(P(a, b), radius=0.024, color=GREY_B) for a, b in D["primes"]])
        expl = VGroup(
            Tex(r"Gaussian integers: $a+bi$ with $a,b\in\mathbb{Z}$", font_size=32),
            Tex(r"Gaussian prime: no factorization\\ into smaller Gaussian integers", font_size=32),
            MathTex(r"5=(2+i)(2-i)\quad\text{is not prime}", font_size=34, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.7 + UP * 1.6)
        with self.say("In the plane, things are different. {gi}The Gaussian integers are the points a plus b i with "
                      "whole-number coordinates. {pr}Some of them are prime: they cannot be factored into smaller "
                      "Gaussian integers. Five, for example, splits as two plus i, times two minus i. "
                      "{pl}Here is every Gaussian prime in this window: a strikingly symmetric dust.") as s:
            self.play(Create(axes))
            s.wait_until("gi")
            self.play(FadeIn(expl[0]))
            s.wait_until("pr")
            self.play(FadeIn(expl[1]), FadeIn(expl[2]))
            s.wait_until("pl")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.0008), run_time=3)
        self.play(FadeOut(expl))

        c2 = {tuple(p) for p in D["c2"]}
        comp = VGroup(*[d for d, (a, b) in zip(dots, D["primes"]) if (a, b) in c2])
        path = D["c2_path"]
        walk = VMobject(color=WHITE, stroke_width=3).set_points_as_corners([P(a, b) for a, b in path])
        frog = Dot(P(*path[0]), radius=0.07, color=RED_3B)
        moat = Circle(radius=46.6 * sc, color=RED_3B, stroke_width=3).move_to(org)
        moat.set_stroke(opacity=0.8)
        rules = VGroup(
            Tex(r"Hop from prime to prime,\\ each hop of length $\le D$", font_size=32),
            Tex(r"$D=2$: from $1+i$ you reach\\ exactly 720 primes", font_size=32, color=YELLOW_3B),
            Tex(r"then a \emph{moat}: no prime\\ within reach", font_size=32, color=RED_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(RIGHT * 3.9 + UP * 1.2)
        with self.say("Now a frog starts next to the origin and hops from prime to prime, each hop of length at most "
                      "some fixed D. {d2}With hops of length at most two, it can reach these seven hundred and twenty "
                      "primes, {w}and its farthest trip looks like this. {moat}But that is all: a ring of empty "
                      "space, a moat, surrounds them. {q}Longer hops reach farther. The question is whether, for some "
                      "D, the frog can go on forever.") as s:
            self.play(FadeIn(rules[0]), GrowFromCenter(frog))
            s.wait_until("d2")
            others = VGroup(*[d for d, (a, b) in zip(dots, D["primes"]) if (a, b) not in c2])
            self.play(comp.animate.set_color(YELLOW_3B), others.animate.set_color(GREY_D), FadeIn(rules[1]),
                      run_time=1.5)
            s.wait_until("w")
            self.play(Create(walk), MoveAlongPath(frog, walk), run_time=3, rate_func=linear)
            s.wait_until("moat")
            self.play(Create(moat), FadeIn(rules[2]), run_time=1.5)
        self.play(FadeOut(VGroup(axes, dots, walk, frog, moat, rules)))

        # ------------------------------------------------------------ history
        hist = VGroup(
            Tex(r"1962 ICM, Stockholm: Basil Gordon asks the question", font_size=34),
            Tex(r"Erd\H{o}s later credits Gordon and Motzkin", font_size=34, color=GREY_A),
            Tex(r"Tsuchimura (computer): from the origin, hops $\le 6$ cannot escape", font_size=34),
            Tex(r"Gethner, Wagon, Wick: arbitrarily large prime-free disks", font_size=34),
            Tex(r"\dots but a walker can go \emph{around} a disk", font_size=34, color=RED_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        with self.say(f"This is the Gaussian moat problem. It goes back to Basil Gordon at the 1962 International "
                      f"Congress in Stockholm, and {ERD} later credited Gordon and {MOTZ}. "
                      f"{{c}}Computers pushed the frog's range: {TSU} showed that, from the origin, hops of length up "
                      f"to six still cannot escape. {{d}}And {GETH}, Wagon and Wick built prime-free disks of any size. "
                      "{a}But a disk alone is not a moat. The frog can simply walk around it.") as s:
            self.play(FadeIn(hist[0]))
            self.play(FadeIn(hist[1]))
            s.wait_until("c")
            self.play(FadeIn(hist[2]))
            s.wait_until("d")
            self.play(FadeIn(hist[3]))
            s.wait_until("a")
            self.play(FadeIn(hist[4]))
        self.play(FadeOut(hist))

        thm = VGroup(
            Tex(r"\textbf{Theorem.} For every step bound $D$ there is a finite $B_D$ such that", font_size=38),
            Tex(r"every cluster of Gaussian primes joined by hops of length $\le D$", font_size=38),
            Tex(r"has at most $B_D$ primes, wherever it starts (axes included).", font_size=38),
            Tex(r"So no infinite walk with bounded steps exists.", font_size=38, color=YELLOW_3B),
        ).arrange(DOWN, buff=0.25)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3))
        with self.say("A manuscript in OpenAI's math catalogue claims the full answer. {t}For every step bound D, "
                      "there is a finite number, B of D, such that every cluster of Gaussian primes linked by hops of "
                      "length at most D has at most B of D primes, wherever it starts, even on the axes. "
                      "{n}So there is no walk to infinity.") as s:
            s.wait_until("t")
            self.play(FadeIn(tb[1]), Write(thm[:3]), run_time=3)
            s.wait_until("n")
            self.play(FadeIn(thm[3]))
        self.play(FadeOut(tb))

        # ------------------------------------------------------------ the finite sieve
        x0, y0, W, H = D["window"]
        g = 0.2
        worg = np.array([-(W - 1) * g / 2, -(H - 1) * g / 2 - 0.12, 0])

        def Wp(i, j):
            return worg + g * np.array([i, j, 0.0])

        w5, w3 = D["w5"], D["w3"]
        hdr = Tex(r"Delete multiples of $2\pm i$ (the factors of 5)", font_size=36).to_edge(UP, buff=0.3)
        allp = VGroup(*[Dot(Wp(i, j), radius=0.055, color=BLUE_3B) for i in range(W) for j in range(H)])
        idx = {(i, j): k for k, (i, j) in enumerate((i, j) for i in range(W) for j in range(H))}
        del5 = [allp[idx[(i, j)]] for i in range(W) for j in range(H) if w5[i, j] < 0]
        del3 = [allp[idx[(i, j)]] for i in range(W) for j in range(H) if w5[i, j] >= 0 > w3[i, j]]
        hdr2 = Tex(r"\dots and of the factors of 13 and 17: finite islands", font_size=36).to_edge(UP, buff=0.3)
        isl_anims = [allp[idx[(i, j)]].animate.set_color(ISL[w3[i, j] % len(ISL)])
                     for i in range(W) for j in range(H) if w3[i, j] >= 0]
        prm = VGroup(*[Circle(radius=0.085, color=WHITE, stroke_width=2).move_to(Wp(i, j)) for i, j in D["wprimes"]])
        best = int(D["best"][0])
        note = Tex(rf"computer check over a full period: all islands finite, the largest has {best} points",
                   font_size=26, color=GREY_A).to_edge(DOWN, buff=0.1)
        with self.say("The proof does not hunt for moats among the primes. Instead it sieves. "
                      "{s5}Take the two Gaussian prime factors of five, and delete every multiple of either one. "
                      "What survives is a periodic pattern, and a frog taking unit hops can still wander off to "
                      "infinity in it. {s3}Now also delete multiples of the factors of thirteen and seventeen. "
                      "{isl}The survivors shatter into islands. A computer check over one full period confirms that "
                      "every island is finite, and the largest has just eighty points. "
                      "{pr}And the Gaussian primes, shown circled, all sit on islands, because a prime cannot be a "
                      "multiple of a different prime.") as s:
            self.play(FadeIn(allp), run_time=1.5)
            s.wait_until("s5")
            self.play(Write(hdr), *[d.animate.set_color(GREY_D).scale(0.5) for d in del5], run_time=2)
            s.wait_until("s3")
            self.play(ReplacementTransform(hdr, hdr2), *[d.animate.set_color(GREY_D).scale(0.5) for d in del3],
                      run_time=2)
            s.wait_until("isl")
            self.play(*isl_anims, FadeIn(note), run_time=2)
            s.wait_until("pr")
            self.play(LaggedStart(*[Create(c) for c in prm], lag_ratio=0.01), run_time=2.5)
        self.play(FadeOut(VGroup(allp, hdr2, prm, note)))

        # ------------------------------------------------------------ periodicity -> uniform bound
        hdr = Tex(r"Step 1: a finite sieve gives a \emph{uniform} bound", font_size=38, color=YELLOW_3B).to_edge(
            UP, buff=0.35)
        tiles = VGroup()
        T = 1.2
        rng = np.random.default_rng(3)
        blob = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (1, 2), (3, 2), (0, -1)]
        for a in range(3):
            for b in range(3):
                sq = Square(T, color=GREY_D, stroke_width=2).move_to(LEFT * 4.9 + RIGHT * (a - 1) * T + UP * (b - 1)
                                                                    * T + DOWN * 0.4)
                tiles.add(sq)
        cen = tiles[4].get_center() + np.array([-0.3, -0.25, 0])
        isl = VGroup(*[Dot(cen + 0.16 * np.array([x, y, 0]), radius=0.05, color=TEAL_3B) for x, y in blob])
        copies = VGroup(*[isl.copy().shift(t.get_center() - tiles[4].get_center()).set_opacity(0.45)
                          for k, t in enumerate(tiles) if k != 4])
        Ql = MathTex(r"Q=5\cdot13\cdot17", font_size=32).next_to(tiles, DOWN, buff=0.25)
        pts = VGroup(
            Tex(r"The sieved set repeats with period $Q$.", font_size=30),
            Tex(r"An island holding $x$ and $x+Qv$ would be mapped", font_size=30),
            Tex(r"to itself by that shift: impossible if finite.", font_size=30),
            Tex(r"So every island has at most $Q^2$ points, and every", font_size=30),
            Tex(r"cluster of Gaussian primes meets only a few islands.", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        th = VGroup(
            Tex(r"\textbf{Thm.\ 1.2:} for every $D$, finitely many primes", font_size=30, color=YELLOW_3B),
            Tex(r"$p\equiv1 \pmod 4$ already block all walks with hops $\le D$.", font_size=30, color=YELLOW_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        VGroup(th, pts).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(RIGHT * 1.75 + DOWN * 0.4)
        with self.say("This is the shape of the whole argument. {t}The paper's finite sieve theorem says that for every "
                      "D, finitely many primes of this kind, each one more than a multiple of four, already block every "
                      "walk with hops up to D. {p}Periodicity then makes the bound uniform. The sieved pattern repeats "
                      "with period Q, the product of the primes. {i}An island containing two points that differ by a "
                      "period would be carried onto itself by that shift, which is impossible for a finite set. So "
                      "every island has at most Q squared points, {c}and every cluster of Gaussian primes is trapped "
                      "among a few islands, no matter where it starts.") as s:
            self.play(Write(hdr))
            s.wait_until("t")
            self.play(FadeIn(th))
            s.wait_until("p")
            self.play(Create(tiles), FadeIn(isl), FadeIn(Ql), FadeIn(pts[0]))
            self.play(FadeIn(copies))
            s.wait_until("i")
            self.play(FadeIn(pts[1:3]))
            s.wait_until("c")
            self.play(FadeIn(pts[3:5]))
        self.play(FadeOut(VGroup(hdr, tiles, isl, copies, Ql, pts, th)))

        # ------------------------------------------------------------ the information budget
        hdr = Tex(r"Step 2: why a finite sieve exists \textemdash{} an information budget", font_size=38,
                  color=YELLOW_3B).to_edge(UP, buff=0.35)
        left = VGroup(
            Tex(r"Suppose an infinite self-avoiding walk", font_size=30),
            Tex(r"dodges every deleted residue class.", font_size=30),
            Tex(r"A long walk has many distinct displacements,", font_size=30),
            Tex(r"so its residues mod $p$ spread out.", font_size=30),
            Tex(r"Dodging zero then forces each step to carry", font_size=30),
            Tex(r"information: each batch of primes in $[T,2T]$", font_size=30),
            Tex(r"costs at least $c/\log T$ per step.", font_size=30, color=ORANGE_3B),
            Tex(r"One step has $\le K_D$ options: budget $\log K_D$.", font_size=30, color=TEAL_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(LEFT, buff=0.4).shift(DOWN * 0.35)
        ax = Axes(x_range=[0, 60, 10], y_range=[0, 5, 1], x_length=4.5, y_length=4.0, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": False}).move_to(RIGHT * 2.6 + UP * 0.05)
        xl = Tex(r"number of prime batches, $T=2,4,8,\dots$", font_size=26).next_to(ax, DOWN, buff=0.2)
        yl = Tex(r"total cost", font_size=26).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        Hs = np.cumsum(1 / np.arange(1, 61))
        bars = VGroup(*[Rectangle(width=ax.x_length / 60 * 0.8, height=ax.y_length / 5 * h, stroke_width=0)
                        .set_fill(ORANGE_3B, 0.85).move_to(ax.c2p(j + 0.5, 0), aligned_edge=DOWN)
                        for j, h in enumerate(Hs)])
        budget = DashedLine(ax.c2p(0, 3.2), ax.c2p(60, 3.2), color=TEAL_3B, stroke_width=4)
        bl = Tex(r"budget\\ $\log K_D$", font_size=28, color=TEAL_3B).next_to(budget, RIGHT, buff=0.15)
        ser = MathTex(r"\frac{c}{\log 2}+\frac{c}{\log 4}+\frac{c}{\log 8}+\dots=\frac{c}{\log 2}"
                      r"\left(1+\tfrac12+\tfrac13+\dots\right)=\infty", font_size=36).to_edge(DOWN, buff=0.2)
        with self.say("But why should a finite sieve exist for every D? That is the heart of the paper, and it is an "
                      "argument about information. {w}Suppose some infinite self-avoiding walk dodges every deleted "
                      "class. {sp}A long walk has many distinct displacements, so its positions, read modulo many "
                      "primes, spread out over almost all residues, including those right next to the forbidden zero. "
                      "{c}To keep dodging zero, the steps must carry information about where the walk is. The paper "
                      "shows that each batch of primes between T and two T costs at least c over log T per step. "
                      "{b}But a single step has only finitely many options, so it carries at most log of K D. "
                      "{sum}Now add up batches at T equals two, four, eight, and so on. The costs form a harmonic "
                      "series, which diverges. {x}A finite budget cannot pay an infinite bill, so a finite set of "
                      "batches already blocks every walk.") as s:
            self.play(Write(hdr))
            s.wait_until("w")
            self.play(FadeIn(left[0:2]))
            s.wait_until("sp")
            self.play(FadeIn(left[2:4]))
            s.wait_until("c")
            self.play(FadeIn(left[4:7]), Create(ax), FadeIn(xl), FadeIn(yl))
            s.wait_until("b")
            self.play(FadeIn(left[7]), Create(budget), FadeIn(bl))
            s.wait_until("sum")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08), run_time=4)
            self.play(Write(ser))
            s.wait_until("x")
            cross = next(j for j, h in enumerate(Hs) if h > 3.2)
            self.play(Flash(bars[cross].get_top(), color=RED_3B), bars[cross:].animate.set_fill(RED_3B, 0.9))
        self.play(FadeOut(VGroup(hdr, left, ax, xl, yl, bars, budget, bl, ser)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"For every $D$: Gaussian-prime clusters with hops $\le D$ have bounded size",
             r"So no infinite bounded-step walk exists (the bound $B_D$ is not explicit)",
             r"Manuscript: 29 pages, produced by an OpenAI model"],
            True, r"\emph{Bounded-Step Walks on Gaussian Primes} (Sept.\ 2026)")
        with self.say("The bound is not explicit: the proof does not say how large the islands are. The manuscript is "
                      "twenty-nine pages, written by an OpenAI model and not yet peer reviewed, {l}and its main "
                      "theorem, the uniform bound for every step size, has been formalized in the Lean proof "
                      "assistant.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
