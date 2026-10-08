import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(__file__.replace("v26_logspace.py", "data/v26.npz"))
SIZES = [int(v) for v in D["sizes"]]
EDGES = [tuple(int(x) for x in e) for e in D["E"]]
NUM, DEN = D["num"], D["den"]
EST, P0, GOOD = D["est"], float(D["p0"]), D["isgood"]

AKLLR = ("[Aleliunas](/ˌæləlˈunəs/), Karp, Lipton, [Lovász](/lˈOvɑs/) and [Rackoff](/ɹˈækɔf/)")
BCP = "[Borodin](/bəɹˈOdɪn/), Cook and [Pippenger](/pˈɪpənʤəɹ/)"
NISAN = "[Nisan](/nisˈɑn/)"
SZ = "[Saks](/sˈæks/) and [Zhou](/ʤˈO/)"
HOZA = "[Hoza](/hˈOzə/)"
REIN = "[Reingold](/ɹˈAnɡOld/)"


def frac(n, d):
    if d == 1:
        return str(n)
    return r"\tfrac{%d}{%d}" % (n, d)


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "103", r"$\mathsf{L}=\mathsf{RL}=\mathsf{BPL}$",
                          r"Randomness does not help logarithmic-space computation")
        with self.say("Does randomness help a computer that has almost no memory?"):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ the machine
        cells = VGroup(*[Square(0.42, stroke_color=GREY_B, stroke_width=2) for _ in range(26)]).arrange(RIGHT, buff=0)
        cells.to_edge(UP, buff=0.7)
        bits = "0110100111010010110101101"
        inp = VGroup(*[MathTex(b, font_size=24).move_to(c) for b, c in zip(bits, cells[:25])])
        in_l = Tex(r"input: $n$ symbols, read-only", font_size=28, color=GREY_A).next_to(cells, UP, buff=0.12)
        head = Triangle(color=YELLOW_3B, fill_opacity=1).scale(0.12).next_to(cells[3], DOWN, buff=0.05)
        work = VGroup(*[Square(0.42, stroke_color=BLUE_3B, stroke_width=2) for _ in range(5)]).arrange(RIGHT, buff=0)
        work.next_to(cells, DOWN, buff=0.85).align_to(cells, LEFT)
        wbits = VGroup(*[MathTex(b, font_size=24, color=BLUE_3B).move_to(c) for b, c in zip("10110", work)])
        w_l = Tex(r"work memory: $O(\log n)$ bits", font_size=28, color=BLUE_3B).next_to(work, RIGHT, buff=0.3)
        coin = VGroup(Circle(radius=0.3, color=YELLOW_3B, fill_opacity=0.25), MathTex(r"\tfrac12", font_size=28)
                      ).next_to(w_l, RIGHT, buff=0.8)
        coin_l = Tex("fair coins", font_size=28, color=YELLOW_3B).next_to(coin, RIGHT, buff=0.2)
        # random walk on a small graph
        gp = {0: (-4.5, -1.0), 1: (-3.2, -0.3), 2: (-3.4, -1.9), 3: (-1.9, -1.2), 4: (-0.6, -0.4), 5: (-0.7, -2.2),
              6: (0.8, -1.3), 7: (2.0, -0.4), 8: (2.2, -2.3), 9: (3.5, -1.3)}
        ge = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (3, 5), (4, 5), (4, 6), (5, 6), (6, 7), (6, 8), (7, 8),
              (7, 9), (8, 9)]
        gpts = {k: np.array([x, y - 0.6, 0]) for k, (x, y) in gp.items()}
        gv = VGroup(*[Dot(gpts[k], radius=0.1, color=GREY_B) for k in range(10)])
        gl = VGroup(*[Line(gpts[a], gpts[b], color=GREY_C, stroke_width=2.5) for a, b in ge])
        sl = MathTex("s", font_size=32, color=GREEN_3B).next_to(gv[0], LEFT, buff=0.15)
        tl = MathTex("t", font_size=32, color=RED_3B).next_to(gv[9], RIGHT, buff=0.15)
        walk = [0, 1, 3, 2, 3, 4, 5, 6, 4, 6, 8, 7, 9]
        tok = Dot(gpts[0], radius=0.14, color=YELLOW_3B)
        mem = Tex(r"remember only: current vertex, step count", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.say("Picture a machine that reads an input of length n, but has only about log n bits of scratch "
                      "memory: room for a few counters and pointers into the input, nothing more. "
                      "{coin}Now let it flip fair coins. "
                      "{walk}A famous example: to test whether two vertices of an undirected graph are connected, "
                      "walk at random from one of them, remembering only where you are and how many steps you have "
                      f"taken. {{y79}}In 1979, {AKLLR} showed that a polynomial-length walk finds the target with high "
                      "probability. {q}And they asked: can every such randomized computation be simulated "
                      "deterministically, in the same logarithmic space?") as s:
            self.play(FadeIn(cells), FadeIn(inp), FadeIn(in_l), FadeIn(head))
            self.play(FadeIn(work), FadeIn(wbits), FadeIn(w_l))
            self.play(head.animate.next_to(cells[11], DOWN, buff=0.05), run_time=1.2)
            s.wait_until("coin")
            self.play(FadeIn(coin), FadeIn(coin_l))
            self.play(Rotate(coin, PI, axis=UP), run_time=0.8)
            s.wait_until("walk")
            self.play(Create(gl), FadeIn(gv), FadeIn(sl), FadeIn(tl), run_time=1.5)
            self.play(FadeIn(tok), FadeIn(mem))
            for v in walk[1:]:
                self.play(tok.animate.move_to(gpts[v]), run_time=0.4)
            self.play(Flash(gv[9], color=RED_3B))
            s.wait_until("y79")
            cite = Tex(r"1979: Aleliunas, Karp, Lipton, Lov\'asz, Rackoff", font_size=30, color=GREY_A).move_to(mem)
            self.play(FadeOut(mem), FadeIn(cite))
            s.wait_until("q")
            ques = Tex(r"Can randomized log space be made deterministic, in log space?", font_size=34,
                       color=YELLOW_3B).move_to(mem)
            self.play(FadeOut(cite), FadeIn(ques))
        self.play(FadeOut(VGroup(cells, inp, in_l, head, work, wbits, w_l, coin, coin_l, gv, gl, sl, tl, tok, ques)))

        # ------------------------------------------------------------ the classes
        def pbar(lo_txt, hi_txt, lo, hi, title, col):
            ax_ = NumberLine(x_range=[0, 1, 0.5], length=4.2, include_numbers=False, color=GREY_B)
            zero = MathTex("0", font_size=24).next_to(ax_.n2p(0), DOWN, buff=0.12)
            one = MathTex("1", font_size=24).next_to(ax_.n2p(1), DOWN, buff=0.12)
            no_r = Line(ax_.n2p(lo[0]), ax_.n2p(lo[1]), color=RED_3B, stroke_width=12)
            yes_r = Line(ax_.n2p(hi[0]), ax_.n2p(hi[1]), color=GREEN_3B, stroke_width=12)
            if lo[0] == lo[1]:
                no_r = Dot(ax_.n2p(0), color=RED_3B, radius=0.1)
            nt = Tex(lo_txt, font_size=24, color=RED_3B).next_to(no_r, UP, buff=0.15)
            yt = Tex(hi_txt, font_size=24, color=GREEN_3B).next_to(yes_r, UP, buff=0.15)
            ttl = Tex(title, font_size=34, color=col).next_to(ax_, LEFT, buff=0.5)
            return VGroup(ttl, ax_, zero, one, no_r, yes_r, nt, yt)

        L_t = VGroup(Tex(r"$\mathsf{L}$", font_size=40, color=BLUE_3B),
                     Tex(r"deterministic, $O(\log n)$ space", font_size=30)).arrange(RIGHT, buff=0.5)
        rl = pbar("no: never accept", r"yes: $\ge\tfrac12$", (0, 0), (0.5, 1), r"$\mathsf{RL}$", TEAL_3B)
        bpl = pbar(r"no: $\le\tfrac13$", r"yes: $\ge\tfrac23$", (0, 1 / 3), (2 / 3, 1), r"$\mathsf{BPL}$", YELLOW_3B)
        cls = VGroup(L_t, rl, bpl).arrange(DOWN, buff=0.7, aligned_edge=LEFT).scale(1.2).shift(UP * 0.3)
        sub = Tex(r"acceptance probability; polynomial time, $O(\log n)$ space", font_size=28,
                  color=GREY_A).next_to(cls, UP, buff=0.4)
        chain = MathTex(r"\mathsf{L}\ \subseteq\ \mathsf{RL}\ \subseteq\ \mathsf{BPL}", r"\qquad\text{equal?}",
                        font_size=44).to_edge(DOWN, buff=0.5)
        chain[1].set_color(YELLOW_3B)
        with self.say("Three classes capture the question. {l}L is what deterministic machines decide in logarithmic "
                      "space. {rl}RL allows polynomial-time randomized machines with one-sided error: they never accept "
                      "a no instance, and accept a yes instance with probability at least a half. "
                      "{bpl}BPL allows two-sided error: probability at most a third on no instances, and at least two "
                      "thirds on yes instances. {c}Each class contains the previous one. Are they all equal?") as s:
            s.wait_until("l")
            self.play(FadeIn(L_t))
            s.wait_until("rl")
            self.play(FadeIn(rl), FadeIn(sub))
            s.wait_until("bpl")
            self.play(FadeIn(bpl))
            s.wait_until("c")
            self.play(Write(chain))
        self.play(FadeOut(VGroup(cls, sub, chain)))

        # ------------------------------------------------------------ history ladder
        hdr = Tex(r"Deterministic space for $\mathsf{BPL}$: $(\log n)^{c}$", font_size=40,
                  color=YELLOW_3B).to_edge(UP, buff=0.4)
        rows = [(2.0, r"Borodin--Cook--Pippenger;\ Nisan (also polynomial time)", r"c=2", BLUE_3B),
                (1.5, r"Saks--Zhou", r"c=\tfrac32", TEAL_3B),
                (1.47, r"Hoza: $\log^{3/2}n/\sqrt{\log\log n}$", r"c\approx\tfrac32", GREEN_3B),
                (1.0, r"the goal: $\mathsf{L}$", r"c=1", YELLOW_3B)]
        unit = 2.3
        bars = VGroup()
        for k, (v, txt, cl, col) in enumerate(rows):
            b = Rectangle(width=v * unit, height=0.55, stroke_width=0, fill_color=col, fill_opacity=0.7)
            b.move_to([-5.6 + v * unit / 2, 1.5 - 1.05 * k, 0])
            lab = MathTex(cl, font_size=32).next_to(b, LEFT, buff=0.1).shift(RIGHT * 0)
            lab.move_to(b.get_center())
            tx = Tex(txt, font_size=28).next_to(b, RIGHT, buff=0.3)
            bars.add(VGroup(b, lab, tx))
        bars[3][0].set_fill(opacity=0.25).set_stroke(YELLOW_3B, 2)
        rein = Tex(r"2005: Reingold puts undirected connectivity in $\mathsf{L}$", font_size=30,
                   color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.say(f"Progress came in steps. {BCP} simulated these machines in log squared space. "
                      f"{NISAN}, building on his pseudorandom generator, achieved log squared space together with polynomial time. "
                      f"{{sz}}{SZ} reduced the space to log to the three halves, {{hz}}and {HOZA} improved that slightly. "
                      f"{{r}}And for the random walk example, {REIN} found a deterministic logarithmic-space algorithm "
                      "for undirected connectivity in 2005. {g}But for general randomized computations, logarithmic "
                      "space was the missing goal.") as s:
            self.play(Write(hdr))
            self.play(FadeIn(bars[0]))
            s.wait_until("sz")
            self.play(FadeIn(bars[1]))
            s.wait_until("hz")
            self.play(FadeIn(bars[2]))
            s.wait_until("r")
            self.play(FadeIn(rein))
            s.wait_until("g")
            self.play(FadeIn(bars[3]))
        self.play(FadeOut(VGroup(hdr, bars, rein)))

        # ------------------------------------------------------------ the theorem
        thm = VGroup(Tex(r"\textbf{Theorem.}\quad $\mathsf{L}=\mathsf{RL}=\mathsf{BPL}$", font_size=48),
                     Tex(r"Every bounded-error, polynomial-time, log-space randomized machine", font_size=32),
                     Tex(r"can be simulated deterministically in $O(\log n)$ space.", font_size=32)).arrange(
            DOWN, buff=0.3)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.35)).shift(UP * 1.3)
        more = VGroup(
            Tex(r"Acceptance probability to within $2^{-q}$ in $O(\log n+q)$ space", font_size=30),
            Tex(r"An explicit compiler: randomized program $\to$ deterministic decider", font_size=30),
        ).arrange(DOWN, buff=0.25).next_to(tb, DOWN, buff=0.6)
        with self.say("A manuscript in OpenAI's math catalogue claims the full answer. {t}L equals RL equals BPL. "
                      "Every bounded-error randomized machine running in polynomial time and logarithmic space "
                      "can be simulated deterministically in logarithmic space. "
                      "{m}More precisely, it approximates the acceptance probability itself, to within two to the "
                      "minus q, using order log n plus q space, {c}and it comes with an explicit compiler from "
                      "randomized programs to deterministic ones.") as s:
            s.wait_until("t")
            self.play(Write(thm[0]), Create(tb[1]), run_time=2)
            self.play(FadeIn(thm[1:]))
            s.wait_until("m")
            self.play(FadeIn(more[0]))
            s.wait_until("c")
            self.play(FadeIn(more[1]))
        self.play(FadeOut(VGroup(tb, more)))

        # ------------------------------------------------------------ configuration graph
        hdr = Tex(r"Configurations, laid out by time", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.35)
        nl = len(SIZES)
        X0, DX = -5.4, 2.0
        npos = {}
        for li, sz in enumerate(SIZES):
            for v in range(sz):
                npos[(li, v)] = np.array([X0 + DX * li, 0.3 + 1.3 * ((sz - 1) / 2 - v), 0])
        nodes = VGroup(*[Circle(radius=0.4, color=GREY_B, stroke_width=2.5).move_to(npos[k]) for k in npos])
        keys = list(npos.keys())
        earrs = VGroup(*[Arrow(npos[(li, v)], npos[(li + 1, w)], buff=0.42, stroke_width=2.5, color=GREY_C,
                               max_tip_length_to_length_ratio=0.12) for li, v, w in EDGES])
        half = Tex(r"each arrow: a coin flip, probability $\tfrac12$", font_size=28, color=GREY_A).move_to(
            [3.3, 2.3, 0])
        tlab = VGroup(*[MathTex(f"t={li}", font_size=26, color=GREY_A).move_to([X0 + DX * li, -1.75, 0])
                        for li in range(nl)])
        vals = {}
        for li in range(nl):
            for v in range(SIZES[li]):
                c = YELLOW_3B if li == 0 else (GREEN_3B if NUM[li][v] == DEN[li][v] else (
                    RED_3B if NUM[li][v] == 0 else WHITE))
                vals[(li, v)] = MathTex(frac(int(NUM[li][v]), int(DEN[li][v])), font_size=32, color=c).move_to(
                    npos[(li, v)])
        acc_l = Tex(r"accept $=1$, reject $=0$", font_size=28).next_to(nodes[keys.index((nl - 1, 1))], RIGHT, buff=0.4)
        rec = MathTex(r"p=e+Sp\quad\Rightarrow\quad p=(I-S)^{-1}e", font_size=40).to_edge(DOWN, buff=0.55)
        memo = Tex(r"backward sweep stores a whole layer: far more than $\log n$ bits", font_size=28,
                   color=RED_3B).next_to(rec, UP, buff=0.25)
        with self.say("Why is this hard? A log-space machine has only polynomially many configurations: its state, "
                      "head positions and memory contents. {lay}Lay them out by time. Each coin flip is a pair of "
                      "edges with probability one half. {fin}At the final time, accepting configurations get value "
                      "one, rejecting ones zero. {back}Working backwards, each configuration's acceptance probability "
                      "is the average of its two successors, all the way back to the start: thirteen sixteenths. "
                      "{mat}In matrix form, p equals e plus S p, so p is the inverse of I minus S, applied to e. "
                      "{mem}But the backward sweep must store a whole layer of numbers, far more than log n bits.") as s:
            self.play(Write(hdr))
            s.wait_until("lay")
            self.play(FadeIn(nodes), FadeIn(tlab))
            self.play(LaggedStart(*[GrowArrow(a) for a in earrs], lag_ratio=0.05), FadeIn(half), run_time=2)
            s.wait_until("fin")
            self.play(*[FadeIn(vals[(nl - 1, v)]) for v in range(SIZES[-1])], FadeIn(acc_l))
            s.wait_until("back")
            for li in range(nl - 2, -1, -1):
                self.play(*[FadeIn(vals[(li, v)], scale=1.3) for v in range(SIZES[li])], run_time=0.8)
            s.wait_until("mat")
            self.play(Write(rec))
            s.wait_until("mem")
            self.play(FadeIn(memo))
        self.play(FadeOut(VGroup(hdr, nodes, earrs, half, tlab, *vals.values(), acc_l, rec, memo)))

        # ------------------------------------------------------------ correction hierarchy
        hdr = Tex(r"An exact correction identity", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.35)
        idt = MathTex(r"D=C-E+EC", r"\qquad\Longrightarrow\qquad", r"I-D=(I+E)(I-C)", font_size=42).next_to(
            hdr, DOWN, buff=0.35)
        expl = Tex(r"same $p$: new transitions $D$, removed weight moved into the reward", font_size=30,
                   color=GREY_A).next_to(idt, DOWN, buff=0.25)
        ax = Axes(x_range=[0, 10, 2], y_range=[-40, 30, 10], x_length=6.2, y_length=3.9, tips=False,
                  axis_config={"color": GREY_B, "font_size": 24, "include_numbers": True}).shift(LEFT * 2.6 + DOWN * 1.6)
        xl = Tex("stage $l$", font_size=26).next_to(ax.x_axis, RIGHT, buff=0.15).shift(DOWN * 0.3)
        yl = MathTex(r"\log_2", font_size=28).next_to(ax.y_axis, UP, buff=0.12)
        H, LV0 = 4, 20
        c_ent = ax.plot(lambda l: -H * l, x_range=[0, 10], color=RED_3B)
        c_ver = ax.plot(lambda l: LV0 + l, x_range=[0, 10], color=BLUE_3B)
        c_err = ax.plot(lambda l: LV0 - (H - 1) * l, x_range=[0, 10], color=GREEN_3B)
        leg = VGroup(Tex(r"largest transition entry $\le 2^{-Hl}$", font_size=28, color=RED_3B),
                     Tex(r"active vertices: at most double", font_size=28, color=BLUE_3B),
                     Tex(r"error $\le |V_0|\,2^{-(H-1)l}$", font_size=28, color=GREEN_3B),
                     Tex(r"$O(\log n)$ stages suffice", font_size=30, color=YELLOW_3B),
                     Tex(r"(plotted: $H=4$, $|V_0|=2^{20}$)", font_size=24, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.7, -1.5, 0])
        with self.say("The proof attacks that inverse with an exact identity. {id}Take a transition matrix C, and a "
                      "correction E, and set D equal to C minus E plus E C. Then I minus D factors as I plus E, times "
                      "I minus C. {ex}So the same probability vector is described by new transitions D, with the "
                      "removed transition weight moved into a reward. {st}Each stage shrinks every transition entry "
                      "by a fixed factor, two to the H, {v}while using copies of vertices so the number of active "
                      "vertices at most doubles. {e}After order log n stages, the reward at the start copy is within "
                      "any fixed inverse polynomial of the true acceptance probability.") as s:
            self.play(Write(hdr))
            s.wait_until("id")
            self.play(Write(idt), run_time=2.5)
            s.wait_until("ex")
            self.play(FadeIn(expl))
            s.wait_until("st")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(c_ent), FadeIn(leg[0]))
            s.wait_until("v")
            self.play(Create(c_ver), FadeIn(leg[1]))
            s.wait_until("e")
            self.play(Create(c_err), FadeIn(leg[2]))
            self.play(FadeIn(leg[3:]))
        self.play(FadeOut(VGroup(hdr, idt, expl, ax, xl, yl, c_ent, c_ver, c_err, leg)))

        # ------------------------------------------------------------ estimate & enumerate
        hdr = Tex(r"Estimate, then try every random environment", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.35)
        pts1 = VGroup(
            Tex(r"later matrices are never stored: entries are estimated", font_size=30),
            Tex(r"in one shared random environment of $O(\log n)$ bits", font_size=30),
            Tex(r"on more than $\tfrac34$ of environments the estimate is accurate", font_size=30, color=GREEN_3B),
        ).arrange(DOWN, buff=0.18).next_to(hdr, DOWN, buff=0.35)
        nl2 = NumberLine(x_range=[0, 1, 0.25], length=10, include_numbers=True, font_size=24,
                         decimal_number_config={"num_decimal_places": 2}).shift(DOWN * 1.9)
        rng = np.random.default_rng(1)
        jit = rng.uniform(-0.55, 0.55, size=len(EST))
        dots = VGroup(*[Dot(nl2.n2p(e) + UP * (0.95 + jit[k]), radius=0.07,
                            color=GREEN_3B if GOOD[k] else RED_3B) for k, e in enumerate(EST)])
        half_l = DashedLine(nl2.n2p(0.5) + DOWN * 0.1, nl2.n2p(0.5) + UP * 1.9, color=GREY_B)
        half_t = MathTex(r"\tfrac12", font_size=28).next_to(half_l, UP, buff=0.08)
        med = float(np.median(EST))
        med_l = Line(nl2.n2p(med) + DOWN * 0.1, nl2.n2p(med) + UP * 1.9, color=YELLOW_3B, stroke_width=5)
        med_t = Tex("median", font_size=28, color=YELLOW_3B).next_to(med_l, UP, buff=0.08).shift(RIGHT * 0.3)
        sch = Tex(r"64 environments (schematic)", font_size=24, color=GREY_A).next_to(nl2, DOWN, buff=0.45)
        poly = MathTex(r"2^{O(\log n)}=n^{O(1)}\ \text{environments}", font_size=34).next_to(pts1, DOWN, buff=0.3)
        with self.say("The matrices of later stages are never written down. {e}Instead, their entries are estimated "
                      "inside one shared random environment, described by only order log n bits. "
                      "{a}The analysis shows that on more than three quarters of the environments, the estimate is "
                      "accurate. {p}And here is the payoff of a logarithmic-length seed: there are only polynomially "
                      "many environments. {t}So try them all, one at a time, reusing the same small memory, "
                      "{m}and take the median. Since more than three quarters are accurate, so is the median. "
                      "Compare it with one half, and you have a deterministic answer.") as s:
            self.play(Write(hdr))
            s.wait_until("e")
            self.play(FadeIn(pts1[:2]))
            s.wait_until("a")
            self.play(FadeIn(pts1[2]))
            s.wait_until("p")
            self.play(Write(poly))
            s.wait_until("t")
            self.play(Create(nl2), FadeIn(sch))
            self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.04), run_time=3)
            s.wait_until("m")
            self.play(Create(half_l), FadeIn(half_t))
            self.play(Create(med_l), FadeIn(med_t))
        hard = Tex(r"Most of the 108 pages: every estimate, accurate or not, halts in $O(\log n)$ space", font_size=30,
                   color=TEAL_3B).next_to(sch, DOWN, buff=0.2)
        with self.say("Most of the hundred and eight pages go into one guarantee: every estimate, even an inaccurate "
                      "one, halts within logarithmic space. That takes fingerprints to compare vertices, "
                      "a shared catalytic workspace, and a space budget that telescopes along the chain of "
                      "recursive calls.") as s:
            self.play(FadeIn(hard))
        self.play(FadeOut(VGroup(hdr, pts1, nl2, dots, half_l, half_t, med_l, med_t, sch, poly, hard)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"$\mathsf{L}=\mathsf{RL}=\mathsf{BPL}$: bounded-error randomized log space is deterministic log space",
             r"acceptance probabilities to within $2^{-q}$ in $O(\log n+q)$ space",
             r"Manuscript: 108 pages, produced by an OpenAI model"],
            False, r"\emph{Exact Derandomization of Logarithmic Space: $\mathsf{L}=\mathsf{RL}=\mathsf{BPL}$} (Sept.\ 2026)")
        with self.say("This is a long and intricate argument from an OpenAI model. It has not been formalized or peer "
                      "reviewed, and it needs careful checking by experts. {c}If it holds, then for polynomial-time, "
                      "logarithmic-space computation, randomness can always be removed, at the cost of only a constant "
                      "factor in memory.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("c")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
