import numpy as np
from manim import *

from style import *
from vo import NarratedScene

RAD = "[Rădulescu](/ɹˌædulˈɛsku/)"
VOI = "[Voiculescu](/vˌYkulˈɛsku/)"
DYK = "[Dykema](/dˈIkəmə/)"
KAD = "[Kadison](/kˈædɪsən/)"

D = np.load("videos/data/v36.npz")


def tree(center, valence, depth=4, L0=1.2, ratio=0.5, color=GREY_B):
    """Cayley graph of a free group: node keys are tuples of direction indices."""
    dirs = [np.array([np.cos(TAU * k / valence), np.sin(TAU * k / valence), 0]) for k in range(valence)]
    pts = {(): np.array(center, dtype=float)}
    g = VGroup()
    frontier = [((), None)]
    for d in range(depth):
        L = L0 * ratio**d
        new = []
        for node, back in frontier:
            for k in range(valence):
                if back is not None and k == (back + valence // 2) % valence:
                    continue
                child = node + (k,)
                pts[child] = pts[node] + dirs[k] * L
                g.add(Line(pts[node], pts[child], color=color, stroke_width=max(0.8, 2.6 - 0.5 * d)))
                new.append((child, k))
        frontier = new
    return g, pts


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "287", r"The Free Group Factors Are Isomorphic",
                          r"$L(\mathbb{F}_2)\cong L(\mathbb{F}_3)$: the free group factor problem")
        with self.say("Two different groups, with the same operator algebra."):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ free groups
        t2, p2 = tree([-3.4, 0.2, 0], 4, depth=4, L0=1.35)
        t3, p3 = tree([3.4, 0.2, 0], 6, depth=3, L0=1.25, ratio=0.42)
        root2 = Dot(p2[()], radius=0.08, color=YELLOW_3B)
        root3 = Dot(p3[()], radius=0.08, color=YELLOW_3B)
        l2 = MathTex(r"\mathbb{F}_2=\langle a,b\rangle", font_size=40).next_to(t2, DOWN, buff=0.35)
        l3 = MathTex(r"\mathbb{F}_3=\langle a,b,c\rangle", font_size=40).next_to(t3, DOWN, buff=0.35).match_y(l2)
        la = MathTex("a", font_size=30, color=BLUE_3B).move_to((p2[()] + p2[(0,)]) / 2 + DOWN * 0.22)
        lb = MathTex("b", font_size=30, color=BLUE_3B).move_to((p2[()] + p2[(1,)]) / 2 + RIGHT * 0.22)
        word = MathTex(r"a\,b\,a^{-1}b^{-1}a\cdots", font_size=36, color=GREY_A).to_edge(UP, buff=0.5)
        ab = VGroup(MathTex(r"\mathbb{F}_2\ \xrightarrow{\ \text{letters commute}\ }\ \mathbb{Z}^2", font_size=36),
                    MathTex(r"\mathbb{F}_3\ \xrightarrow{\ \text{letters commute}\ }\ \mathbb{Z}^3", font_size=36)
                    ).arrange(RIGHT, buff=1.2).to_edge(UP, buff=0.45)
        with self.say("Start with the free group on two letters, a and b: all words in the letters and their "
                      "inverses, with no cancellations. Its picture is an infinite tree where every vertex has "
                      "four neighbors. {f3}The free group on three letters gives a tree with "
                      "six neighbors at every vertex. {diff}These groups are genuinely different: let the letters "
                      "commute, and one becomes a flat grid, the other a three-dimensional one.") as s:
            self.play(FadeIn(word))
            self.play(Create(t2), FadeIn(root2), FadeIn(la), FadeIn(lb), run_time=2.5)
            self.play(Write(l2))
            s.wait_until("f3")
            self.play(Create(t3), FadeIn(root3), Write(l3), run_time=2.5)
            s.wait_until("diff")
            self.play(FadeOut(word), FadeIn(ab))
        self.play(FadeOut(VGroup(t3, root3, l3, ab)), VGroup(t2, root2, la, lb, l2).animate.shift(LEFT * 0.4))

        # ------------------------------------------------------------ operators
        shift = LEFT * 0.4
        src = [(), (1,), (1, 1)]
        dst = [(0,), (0, 1), (0, 1, 1)]
        bumps = VGroup(*[Dot(p2[k] + shift, radius=0.13, color=YELLOW_3B) for k in src])
        fn = Tex(r"functions on the vertices, $\xi\in\ell^2(G)$", font_size=34).to_edge(UP, buff=0.45).shift(
            RIGHT * 3)
        eqs = VGroup(
            MathTex(r"(\lambda(g)\xi)(h)=\xi(g^{-1}h)", font_size=38),
            Tex(r"the shift by $g$: what sat at $h$ moves to $gh$", font_size=30, color=GREY_A),
            MathTex(r"L(G)=\{\lambda(g):g\in G\}''", font_size=40, color=YELLOW_3B),
            Tex(r"add, multiply, take limits", font_size=30, color=GREY_A),
            MathTex(r"\tau(x)=\langle x\,\delta_e,\delta_e\rangle", font_size=40, color=TEAL_3B),
            Tex(r"the trace: what $x$ sends back to the root", font_size=30, color=GREY_A),
        ).arrange(DOWN, buff=0.22).move_to(RIGHT * 3.3 + DOWN * 0.3)
        for k in (2, 4):
            eqs[k].shift(DOWN * 0.15)
            eqs[k + 1].shift(DOWN * 0.15)
        la_op = Tex(r"pattern shifted by $\lambda(a)$", font_size=32, color=YELLOW_3B).move_to([-4.2, 3.3, 0])
        with self.say("Now turn the group into operators. {fn}Put numbers on the vertices of the tree, with a finite "
                      "sum of squares. {sh}Each group element g gives a shift operator, "
                      "lambda of g, which slides the whole pattern along: whatever sat at vertex h moves to g h. "
                      "{alg}Take all these shifts, add and multiply them, and close up under limits. The result is "
                      "the group von Neumann algebra, L of G. {tr}It comes with a trace, tau, which measures how "
                      "much of the root's value an operator sends back to the root.") as s:
            s.wait_until("fn")
            self.play(FadeIn(fn), FadeIn(bumps, scale=1.5))
            s.wait_until("sh")
            self.play(FadeIn(eqs[0:2]))
            self.play(*[b.animate.move_to(p2[k] + shift) for b, k in zip(bumps, dst)], FadeIn(la_op), run_time=2)
            s.wait_until("alg")
            self.play(FadeIn(eqs[2:4]))
            s.wait_until("tr")
            self.play(FadeIn(eqs[4:6]))
        self.play(FadeOut(VGroup(t2, root2, la, lb, l2, bumps, fn, eqs, la_op)))

        # ------------------------------------------------------------ factors, continuous dimension
        cen = VGroup(
            Tex(r"Every $g\neq e$ in $\mathbb{F}_n$ has infinitely many conjugates", font_size=34),
            MathTex(r"\Longrightarrow\ \text{center of } L(\mathbb{F}_n)=\mathbb{C}\cdot 1", font_size=38),
            Tex(r"a \textbf{factor}: an indivisible building block", font_size=34, color=YELLOW_3B),
        ).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.5)
        nl_m = NumberLine(x_range=[0, 1, 0.25], length=8, include_numbers=False, color=GREY_B).shift(DOWN * 0.5)
        dots_m = VGroup(*[Dot(nl_m.n2p(v), radius=0.1, color=BLUE_3B) for v in np.linspace(0, 1, 5)])
        lab_m = Tex(r"$4\times4$ matrices: dimensions $0,\tfrac14,\tfrac12,\tfrac34,1$", font_size=30,
                    color=BLUE_3B).next_to(nl_m, UP, buff=0.3)
        nl_f = NumberLine(x_range=[0, 1, 0.25], length=8, include_numbers=False, color=GREY_B).shift(DOWN * 2.2)
        bar_f = Line(nl_f.n2p(0), nl_f.n2p(1), color=TEAL_3B, stroke_width=12)
        lab_f = Tex(r"$L(\mathbb{F}_2)$: dimensions $\tau(p)$ fill all of $[0,1]$ \quad (type II$_1$)", font_size=30,
                    color=TEAL_3B).next_to(nl_f, UP, buff=0.3)
        n0 = VGroup(MathTex("0", font_size=28).next_to(nl_f.n2p(0), DOWN, buff=0.15),
                    MathTex("1", font_size=28).next_to(nl_f.n2p(1), DOWN, buff=0.15))
        with self.say("For free groups, every element other than the identity has infinitely many conjugates. "
                      "{c}That forces the center of the algebra to be trivial: only multiples of the identity "
                      "commute with everything. {f}Such an algebra is called a factor, an indivisible building "
                      "block. {m}And these factors are strange. In a four by four matrix algebra, subspaces have "
                      "dimension zero, one quarter, one half, and so on. {cont}In L of F two, the trace assigns "
                      "dimensions that fill the whole interval from zero to one. Murray and von Neumann called "
                      "this type two one.") as s:
            self.play(FadeIn(cen[0]))
            s.wait_until("c")
            self.play(Write(cen[1]))
            s.wait_until("f")
            self.play(FadeIn(cen[2]))
            s.wait_until("m")
            self.play(Create(nl_m), FadeIn(lab_m), LaggedStart(*[FadeIn(d, scale=2) for d in dots_m], lag_ratio=0.2))
            s.wait_until("cont")
            self.play(Create(nl_f), FadeIn(n0), FadeIn(lab_f))
            self.play(Create(bar_f), run_time=2)
        self.play(FadeOut(VGroup(cen, nl_m, dots_m, lab_m, nl_f, bar_f, lab_f, n0)))

        # ------------------------------------------------------------ history
        q = MathTex(r"L(\mathbb{F}_2)\ \overset{?}{\cong}\ L(\mathbb{F}_3)", font_size=60, color=YELLOW_3B).to_edge(
            UP, buff=0.5)
        hist = VGroup(
            Tex(r"Murray--von Neumann: $L(\mathbb{F}_n)$ is not the hyperfinite factor", font_size=34),
            Tex(r"rank question credited to Kadison; a central problem for decades", font_size=34),
            Tex(r"Voiculescu: free probability, noncommuting random variables", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(q, DOWN, buff=0.6)
        nl = NumberLine(x_range=[1, 6, 1], length=9, include_numbers=False, color=GREY_B).shift(DOWN * 1.25)
        nums = VGroup(*[MathTex(str(k), font_size=28).next_to(nl.n2p(k), DOWN, buff=0.15) for k in range(2, 6)],
                      MathTex(r"\cdots\ \infty", font_size=28).next_to(nl.n2p(6), DOWN, buff=0.15))
        open1 = Circle(radius=0.08, color=GREY_B).move_to(nl.n2p(1))
        cont = Line(nl.n2p(1.05), nl.n2p(6), color=PURPLE_3B, stroke_width=8)
        rl = MathTex(r"L(\mathbb{F}_r),\ \ 1<r\le\infty", font_size=34, color=PURPLE_3B).next_to(nl, UP, buff=0.25)
        dich = Tex(r"Dykema, R\u{a}dulescu: \emph{all isomorphic} \quad or \quad \emph{all different}", font_size=34
                   ).next_to(nums, DOWN, buff=0.4)
        with self.say("Murray and von Neumann showed that the free group factors differ from the factor built out "
                      "of finite matrices, the hyperfinite one. But nobody could tell L of F two from L of F three. "
                      f"{{k}}The question of whether the number of generators matters, credited to {KAD}, became a "
                      f"central problem of the field. {{v}}{VOI}'s free probability, a theory of noncommuting random "
                      f"variables, became the main tool for studying these algebras. {{d}}Then {DYK} "
                      f"and {RAD} built a whole continuum of interpolated free group factors, one for every real "
                      "number r above one, and proved a stark dichotomy. {all}Either all of them are isomorphic, "
                      "or all of them are different.") as s:
            self.play(Write(q))
            self.play(FadeIn(hist[0]))
            s.wait_until("k")
            self.play(FadeIn(hist[1]))
            s.wait_until("v")
            self.play(FadeIn(hist[2]))
            s.wait_until("d")
            self.play(Create(nl), FadeIn(nums), FadeIn(open1))
            self.play(Create(cont), FadeIn(rl), run_time=1.5)
            s.wait_until("all")
            self.play(FadeIn(dich))
        self.play(FadeOut(VGroup(q, hist, nl, nums, open1, cont, rl, dich)))

        # ------------------------------------------------------------ theorem
        thm = VGroup(Tex(r"\textbf{Theorem.} For every $n\ge3$:\quad $L(\mathbb{F}_n)\cong L(\mathbb{F}_{n+1})$",
                         font_size=40),
                     Tex(r"(unital, normal, trace-preserving $*$-isomorphism)", font_size=28, color=GREY_A)
                     ).arrange(DOWN, buff=0.2)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3)).to_edge(UP, buff=0.4)
        chain = MathTex(r"L(\mathbb{F}_3)", r"\cong", r"L(\mathbb{F}_4)", r"\cong", r"L(\mathbb{F}_5)",
                        font_size=46).next_to(tb, DOWN, buff=0.6)
        amp = MathTex(r"L(\mathbb{F}_r)^{t}\cong L(\mathbb{F}_{1+(r-1)/t^2})", r"\qquad t=\sqrt2:\ \ 3\mapsto 2,\ \ "
                      r"5\mapsto 3", font_size=38).next_to(chain, DOWN, buff=0.45)
        amp[1].set_color(BLUE_3B)
        res = MathTex(r"L(\mathbb{F}_2)\cong L(\mathbb{F}_3)", font_size=56, color=YELLOW_3B).next_to(amp, DOWN,
                                                                                                    buff=0.45)
        cons = Tex(r"$\Rightarrow$ all $L(\mathbb{F}_r)$, $1<r\le\infty$, are one algebra; fundamental group "
                   r"$\mathbb{R}_{>0}$", font_size=32).next_to(res, DOWN, buff=0.35)
        with self.say("A twenty-three page manuscript in OpenAI's math catalogue, not yet peer reviewed, claims to "
                      "settle it. {t}Its core theorem: for every n at least three, L of F n is isomorphic to L of F "
                      "n plus one. {c}So F three, F four and F five all give the same algebra. {a}Now amplify by "
                      f"root two. {DYK}'s formula sends three to two, and five to three, {{r}}so L of F two is "
                      "isomorphic to L of F three. {all}By the dichotomy, every interpolated free group factor, "
                      "even L of F infinity, is the same algebra. A bonus: Voiculescu's free entropy dimension "
                      "is not an invariant of the algebra.".replace(
                          "Voiculescu", VOI)) as s:
            s.wait_until("t")
            self.play(Write(tb), run_time=2)
            s.wait_until("c")
            self.play(Write(chain))
            s.wait_until("a")
            self.play(FadeIn(amp))
            s.wait_until("r")
            self.play(Write(res))
            s.wait_until("all")
            self.play(FadeIn(cons))
        self.play(FadeOut(VGroup(tb, chain, amp, res, cons)))

        # ------------------------------------------------------------ the flow
        hdr = Tex(r"Absorbing a free generator", font_size=42, color=YELLOW_3B).to_edge(UP, buff=0.35)
        setup = VGroup(
            Tex(r"In $L(\mathbb{F}_{n+1})$: free Haar unitaries $A_1,\dots,A_n$ and $C=e^{iS}$", font_size=34),
            Tex(r"Goal: $n$ free Haar unitaries that generate everything, $C$ included",
                font_size=32, color=GREY_A),
        ).arrange(DOWN, buff=0.25).next_to(hdr, DOWN, buff=0.5)
        flow = MathTex(r"\frac{d}{dt}A_j=i\,s_t(h_j)\,A_j,\qquad s_t(h)=\sum_{g}h(g)\,A_g(t)\,S\,A_g(t)^*",
                       font_size=40).next_to(setup, DOWN, buff=0.6)
        inv = Tex(r"preserves every moment $\Rightarrow$ each time-$t$ map is an automorphism", font_size=32,
                  color=TEAL_3B).next_to(flow, DOWN, buff=0.35)
        est = VGroup(
            MathTex(r"\|\beta_1(A_j)-A_j\|\le 3\pi\,\|h_j\|", font_size=38),
            MathTex(r"\|\beta_1(A_w)-C\,A_w\|\le 3\pi\,\|D_w-\delta_e\|", font_size=38),
        ).arrange(RIGHT, buff=0.8).next_to(inv, DOWN, buff=0.6)
        want = Tex(r"need: $h$ tiny, \ but $D_w=T_m h\approx\delta_e$, \quad $T_m=1+\sum_{j=1}^m\lambda(p_j)$",
                   font_size=34, color=YELLOW_3B).next_to(est, DOWN, buff=0.6)
        with self.say("How do you absorb a free generator? Inside L of F n plus one sit free unitaries A one "
                      "through A n, plus one extra, C. {g}The goal is to find n new unitaries, still perfectly "
                      "free, that generate everything, C included. {f}The tool is a flow. Write C as e to the i S, "
                      "and let each A j evolve by a differential equation driven by conjugates of S. {i}A trace "
                      "identity, plus analyticity, shows that the flow preserves every moment, so each time-t map "
                      "is an automorphism. {e}Two estimates follow: each A j moves by at most three "
                      "pi times the size of its coefficients h, while a chosen word A w lands near C times A w. {w}So we need coefficients that are tiny, but whose "
                      "cocycle value, T m applied to h, is nearly the delta function at the identity.") as s:
            self.play(Write(hdr))
            self.play(FadeIn(setup[0]))
            s.wait_until("g")
            self.play(FadeIn(setup[1]))
            s.wait_until("f")
            self.play(Write(flow), run_time=2)
            s.wait_until("i")
            self.play(FadeIn(inv))
            s.wait_until("e")
            self.play(FadeIn(est[0]))
            self.play(FadeIn(est[1]))
            s.wait_until("w")
            self.play(FadeIn(want))
        self.play(FadeOut(VGroup(setup, flow, inv, est)), want.animate.next_to(hdr, DOWN, buff=0.3))

        # ------------------------------------------------------------ the spectrum of T_m T_m^*/m
        edges = D["edges"]
        ax = Axes(x_range=[0, 5, 1], y_range=[0, 2.2, 0.5], x_length=7.4, y_length=4.0, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": True, "font_size": 24}).to_edge(LEFT, buff=0.7
                                                                                                ).shift(DOWN * 0.75)
        xl = MathTex(r"\text{spectrum of } T_mT_m^*/m", font_size=28).next_to(ax.x_axis, DOWN, buff=0.4)

        def bars(m):
            h = np.minimum(D[f"h{m}"], 2.2)
            return VGroup(*[Rectangle(width=ax.x_axis.unit_size * (b - a), height=max(1e-3, ax.y_axis.unit_size * v),
                                      stroke_width=0.5, stroke_color=BLACK).set_fill(BLUE_3B, 0.75)
                          .move_to(ax.c2p((a + b) / 2, 0), aligned_edge=DOWN)
                          for a, b, v in zip(edges[:-1], edges[1:], h)])

        curve = ax.plot_line_graph(D["xs"], np.minimum(D["dens"], 2.2), add_vertex_dots=False, line_color=YELLOW_3B,
                                   stroke_width=4)
        mlab = MathTex("m=1", font_size=36, color=BLUE_3B).move_to(ax.c2p(4.1, 1.9))
        side = VGroup(
            Tex(r"$T_m$: identity $+$ $m$ free unitaries", font_size=28),
            Tex(r"Catalan moment count $\Rightarrow$", font_size=30),
            MathTex(r"d\nu=\frac{1}{2\pi}\sqrt{\frac{4-x}{x}}\,dx", font_size=36, color=YELLOW_3B),
            Tex(r"no atom at $0$", font_size=30, color=YELLOW_3B),
            Tex(r"$\Rightarrow$ invert $T_m$ off a sliver:", font_size=30, color=TEAL_3B),
            MathTex(r"\|h\|^2\le\frac{1}{d\,m}\to0", font_size=36, color=TEAL_3B),
        ).arrange(DOWN, buff=0.22).to_edge(RIGHT, buff=0.7).shift(DOWN * 0.6)
        sim = Tex(r"simulated with $600\times600$ random unitaries", font_size=22, color=GREY_B).next_to(
            ax, UP, buff=0.12).align_to(ax, RIGHT)
        cur = bars(1)
        with self.say("Now free probability enters. {t}T m is the identity plus m free unitaries, so it is "
                      "large. {c}Counting non-crossing matchings, which gives the Catalan numbers, shows that the "
                      "spectrum of T m T m star over m converges to this law, which has no atom at zero. {s}Here "
                      "it is, as m grows. {i}So T m can be inverted on all but a sliver of the "
                      "space, and the inverse is small: the coefficients h have size about one over root m.") as s:
            self.play(Create(ax), FadeIn(xl), FadeIn(sim))
            s.wait_until("t")
            self.play(FadeIn(cur), FadeIn(mlab), FadeIn(side[0]))
            s.wait_until("c")
            self.play(FadeIn(side[1:4]), Create(curve), run_time=2)
            s.wait_until("s")
            for m in [2, 4, 8, 16, 32]:
                nb = bars(m)
                self.play(Transform(cur, nb), Transform(mlab, MathTex(f"m={m}", font_size=36, color=BLUE_3B
                                                                      ).move_to(mlab)), run_time=0.9)
            s.wait_until("i")
            self.play(FadeIn(side[4:]))
        self.play(FadeOut(VGroup(ax, xl, sim, cur, mlab, curve, side, want)))

        # ------------------------------------------------------------ iteration
        rng = np.random.default_rng(3)
        pts, p = [], np.array([-5.6, 1.6, 0])
        eps = 2.0
        for k in range(8):
            pts.append(p.copy())
            ang = rng.uniform(-0.6, 0.6)
            p = p + eps * np.array([np.cos(ang), np.sin(ang) * 0.6 - 0.3, 0])
            eps *= 0.55
        limit = pts[-1] + np.array([0.05, -0.02, 0])
        adots = VGroup(*[Dot(q, radius=0.07, color=BLUE_3B) for q in pts])
        alabs = VGroup(*[MathTex(f"A^{{({k})}}", font_size=30, color=BLUE_3B).next_to(pts[k], d, buff=0.12)
                         for k, d in zip(range(2), [UP, DOWN])])
        balls = VGroup(*[Circle(radius=2.0 * 0.55**k, color=GREY_B, stroke_width=1.5).move_to(pts[k])
                         for k in range(1, 5)])
        segs = VGroup(*[Line(pts[k], pts[k + 1], color=BLUE_3B, stroke_width=2.5) for k in range(7)])
        lim = VGroup(Dot(limit, radius=0.1, color=YELLOW_3B),
                     MathTex(r"A^{(\infty)}", font_size=34, color=YELLOW_3B).next_to(limit, DOWN, buff=0.15))
        cpts = [np.array([3.4 + 2.4 * np.cos(1.7 * k), 1.0 + 1.5 * np.sin(2.3 * k + 0.4), 0]) for k in range(8)]
        cdots = VGroup(*[Dot(q, radius=0.07, color=RED_3B) for q in cpts])
        csegs = VGroup(*[Line(cpts[k], cpts[k + 1], color=RED_3B, stroke_width=1.5, stroke_opacity=0.6)
                         for k in range(7)])
        clab = MathTex(r"C^{(k)}\ \text{need not converge}", font_size=32, color=RED_3B).move_to(RIGHT * 2.8 + DOWN * 1.3)
        step = Tex(r"one step: each $A_j$ moves less than $\varepsilon_k$,\\ and a word in the new $A$'s is "
                   r"within $\varepsilon_k$ of $C$", font_size=30).to_edge(DOWN, buff=1.25)
        concl = Tex(r"limit tuple: still free Haar, and its words are dense $\Rightarrow$ "
                    r"$L(\mathbb{F}_n)\cong L(\mathbb{F}_{n+1})$", font_size=32, color=YELLOW_3B).to_edge(DOWN,
                                                                                                    buff=0.5)
        with self.say("So one step moves each A j by less than epsilon, "
                      "while a word in the new A's comes within epsilon of C. {it}Now repeat, with tolerances that "
                      "shrink, each chosen only after the previous word is known. {lim}The A's converge in norm, "
                      "and their limit is still a free family of Haar unitaries. {c}The extra generator is allowed "
                      "to keep changing; it never needs to converge. It is absorbed: {g}words in the limiting n unitaries "
                      "approximate everything, so they generate the whole algebra.") as s:
            self.play(FadeIn(step))
            self.play(FadeIn(adots[0]), FadeIn(alabs[0]), FadeIn(cdots[0]))
            s.wait_until("it")
            for k in range(1, 8):
                anims = [Create(segs[k - 1]), FadeIn(adots[k]), Create(csegs[k - 1]), FadeIn(cdots[k])]
                if k < 2:
                    anims.append(FadeIn(alabs[k]))
                if k <= 4:
                    anims.append(Create(balls[k - 1]))
                self.play(*anims, run_time=0.55)
            s.wait_until("lim")
            self.play(FadeIn(lim, scale=1.5))
            s.wait_until("c")
            self.play(FadeIn(clab))
            s.wait_until("g")
            self.play(FadeIn(concl))
        self.play(FadeOut(VGroup(hdr, adots, alabs, balls, segs, lim, cdots, csegs, clab, step, concl)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"$L(\mathbb{F}_2)\cong L(\mathbb{F}_3)$; in fact $L(\mathbb{F}_n)\cong L(\mathbb{F}_{n+1})$ for $n\ge3$",
             r"All interpolated free group factors, including $L(\mathbb{F}_\infty)$, are isomorphic",
             r"Fundamental group $\mathbb{R}_{>0}$; free entropy dimension is not an invariant",
             r"Manuscript: 23 pages, produced by an OpenAI model"],
            True, r"\emph{An isomorphism of the free group factors} (Sept.\ 2026)")
        with self.say("The manuscript was written by an OpenAI model. {l}Its main statement, that all the "
                      "interpolated free group factors are isomorphic, has been formalized in the Lean proof "
                      "assistant; the fundamental group conclusion follows from it but was not formalized "
                      "separately. If it holds up, the number of generators of a free group is invisible to its "
                      "von Neumann algebra.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
