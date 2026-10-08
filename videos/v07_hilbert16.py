import numpy as np
from manim import *

from style import *
from vo import NarratedScene

LIEN = "[Liénard](/ljˈAnɑɹ/)"


def vdp(p):
    x, y = p
    return np.array([y - (x**3 / 3 - x), -x])


EPS = 0.12


def quint(p):
    x, y = p
    F = EPS * (2.5 * x - 25 / 6 * x**3 + x**5)
    return np.array([y - F, -x])


def integrate(f, p0, T, dt=0.01, sign=1):
    p = np.array(p0, float)
    out = [p.copy()]
    for _ in range(int(T / dt)):
        k1 = f(p)
        k2 = f(p + sign * dt / 2 * k1)
        k3 = f(p + sign * dt / 2 * k2)
        k4 = f(p + sign * dt * k3)
        p = p + sign * dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        out.append(p.copy())
    return np.array(out)


def return_map(f, r, dt=0.005):
    """Start at (r, 0) on the positive x-axis; follow until the next crossing of y=0 with x>0."""
    p = np.array([r, 0.0])
    t = 0
    prev = p
    while t < 50:
        k1 = f(p); k2 = f(p + dt / 2 * k1); k3 = f(p + dt / 2 * k2); k4 = f(p + dt * k3)
        nxt = p + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        t += dt
        if t > 1 and p[1] > 0 >= nxt[1] and nxt[0] > 0 or t > 1 and p[1] < 0 <= nxt[1] and nxt[0] > 0:
            a = p[1] / (p[1] - nxt[1])
            return p[0] + a * (nxt[0] - p[0])
        p = nxt
    return np.nan


class Video(NarratedScene):
    def traj(self, ax, pts, color, width=2.5):
        m = VMobject(color=color, stroke_width=width)
        m.set_points_smoothly([ax.c2p(*q) for q in pts[::4]])
        return m

    def construct(self):
        card = title_card(self, "143", r"Hilbert's 16th Problem: Limit Cycles",
                          r"A uniform bound on limit cycles for each degree")
        with self.say("Hilbert's sixteenth problem."):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ vector field & a limit cycle
        ax = Axes(x_range=[-3.5, 3.5, 1], y_range=[-3.5, 3.5, 1], x_length=7.2, y_length=7.2, tips=False,
                  axis_config={"color": GREY_D}).shift(LEFT * 2.6)
        field = ArrowVectorField(lambda p: (lambda v: np.array([v[0], v[1], 0]) / (1 + np.linalg.norm(v)) * 0.55)(
            vdp(ax.p2c(p)[:2])), x_range=[ax.c2p(-3.3, 0)[0], ax.c2p(3.3, 0)[0], 0.55],
            y_range=[ax.c2p(0, -3.3)[1], ax.c2p(0, 3.3)[1], 0.55], colors=[GREY_B, GREY_A], opacity=0.55)
        eq = MathTex(r"\dot x = y - \left(\tfrac{x^3}{3}-x\right)", r"\\", r"\dot y = -x", font_size=40).to_corner(
            UR, buff=0.6)
        cyc_pts = integrate(vdp, [2.0, 0.0], 40)[-800:]
        cyc = self.traj(ax, cyc_pts, YELLOW_3B, 6)
        t_in = self.traj(ax, integrate(vdp, [0.15, 0.0], 18), BLUE_3B)
        t_out = self.traj(ax, integrate(vdp, [3.3, 3.0], 12), TEAL_3B)
        lc = Tex(r"a \textbf{limit cycle}:\\ an isolated loop that\\ nearby paths spiral toward", font_size=32,
                 color=YELLOW_3B).next_to(eq, DOWN, buff=0.8)
        with self.say("Take two polynomials, and read them as a flow in the plane: at every point, "
                      "they tell you which way to move. {t}Follow the arrows, and trajectories trace out the motion. "
                      "{c}Often they wind toward an isolated closed loop, a limit cycle: a rhythm the system falls "
                      "into from any nearby start. This is the Van der Pol oscillator, from the early days of radio.") as s:
            self.play(Create(ax), Write(eq), run_time=1.5)
            self.play(Create(field), run_time=2)
            s.wait_until("t")
            self.play(Create(t_in), run_time=4, rate_func=linear)
            s.wait_until("c")
            self.play(Create(t_out), run_time=3, rate_func=linear)
            self.play(Create(cyc), FadeIn(lc), run_time=2)
        self.play(FadeOut(VGroup(t_in, t_out, field)), FadeOut(lc))

        # ------------------------------------------------------------ the question
        q = VGroup(
            Tex(r"\textbf{Hilbert, 1900, problem 16 (second part):}", font_size=34, color=YELLOW_3B),
            Tex(r"for polynomial flows of degree $d$,\\ how many limit cycles can there be?", font_size=34),
            MathTex(r"H(d)=\ ?", font_size=50, color=YELLOW_3B),
            Tex(r"degree 2: at least 4 are possible (1979--80)\\ is there \emph{any} finite bound? unknown", font_size=30,
                color=GREY_A),
        ).arrange(DOWN, buff=0.35).to_edge(RIGHT, buff=0.5)
        with self.say("In 1900, Hilbert asked: for polynomials of degree d, how many limit cycles can such a flow have? "
                      "{q}It is part of the sixteenth problem on his list, and one of only a few never resolved. "
                      "{d2}Even for degree two, quadratic flows, examples with four limit cycles have been known since "
                      "1980, and nobody could prove there is any upper bound at all.") as s:
            self.play(FadeOut(eq), FadeIn(q[0:2]), run_time=1.5)
            s.wait_until("q")
            self.play(Write(q[2]))
            s.wait_until("d2")
            self.play(FadeIn(q[3]))
        self.play(FadeOut(q))

        # ------------------------------------------------------------ return map
        hdr = Tex("Counting cycles: the return map", font_size=38, color=YELLOW_3B).to_corner(UR, buff=0.5)
        seg = Line(ax.c2p(0.2, 0), ax.c2p(3.4, 0), color=ORANGE_3B, stroke_width=6)
        r0 = 0.8
        one = integrate(vdp, [r0, 0.0], 8.5, dt=0.005)
        # cut at first return
        k = next(i for i in range(200, len(one)) if one[i - 1][1] > 0 >= one[i][1] and one[i][0] > 0)
        loop = self.traj(ax, one[:k + 1], BLUE_3B, 4)
        d0 = Dot(ax.c2p(r0, 0), color=WHITE)
        d1 = Dot(ax.c2p(one[k][0], 0), color=BLUE_3B)
        l0 = MathTex("r", font_size=34).next_to(d0, DOWN, buff=0.15)
        l1 = MathTex(r"\Pi(r)", font_size=34, color=BLUE_3B).next_to(d1, DOWN, buff=0.15)
        ax2 = Axes(x_range=[0, 3.4, 1], y_range=[-1.6, 1.6, 1], x_length=4.6, y_length=2.8, tips=False,
                   axis_config={"color": GREY_B}).to_corner(DR, buff=0.5)
        rs = np.linspace(0.25, 3.3, 30)
        disp = np.array([return_map(vdp, r) - r for r in rs])
        dcurve = VMobject(color=ORANGE_3B, stroke_width=4).set_points_smoothly([ax2.c2p(r, d) for r, d in zip(rs, disp)])
        dl = MathTex(r"\Pi(r)-r", font_size=30, color=ORANGE_3B).next_to(ax2, UP, buff=0.1)
        rl = MathTex("r", font_size=28).next_to(ax2.x_axis, RIGHT, buff=0.1)
        z = rs[np.argmin(np.abs(disp))]
        zdot = Dot(ax2.c2p(z, 0), color=YELLOW_3B, radius=0.09)
        expl = Tex(r"limit cycles $=$ isolated zeros\\ of the displacement", font_size=30).next_to(dl, UP, buff=0.3)
        with self.say("How do you count limit cycles? {seg}Draw a short segment crossing the flow. "
                      "{go}Start at a point r, follow the flow once around, and see where you land: call it Pi of r. "
                      "{cyc}A closed orbit is exactly a point that lands back on itself. "
                      "{plot}So limit cycles are the isolated zeros of the displacement, Pi of r minus r.") as s:
            self.play(Write(hdr))
            s.wait_until("seg")
            self.play(Create(seg))
            s.wait_until("go")
            self.play(FadeIn(d0), FadeIn(l0))
            self.play(Create(loop), run_time=3, rate_func=linear)
            self.play(FadeIn(d1), FadeIn(l1))
            s.wait_until("plot")
            self.play(Create(ax2), FadeIn(dl, rl), Create(dcurve), run_time=2)
            self.play(FadeIn(zdot, scale=2), FadeIn(expl))
        self.play(FadeOut(VGroup(hdr, seg, loop, d0, d1, l0, l1, ax2, dcurve, dl, rl, zdot, expl, cyc, ax)))

        # ------------------------------------------------------------ history
        rows = VGroup(
            Tex(r"1923 \quad Dulac claims every \emph{single} flow has finitely many cycles", font_size=32),
            Tex(r"1981 \quad a gap is found in Dulac's proof", font_size=32, color=RED_3B),
            Tex(r"1991--92 \quad \'Ecalle and Ilyashenko: finiteness for each single flow", font_size=32),
            Tex(r"open \quad a bound depending \emph{only on the degree} (Smale's 13th problem)", font_size=32,
                color=YELLOW_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        with self.say("Even proving that one single flow has finitely many limit cycles was hard. "
                      "{dul}Henri Dulac claimed it in 1923. {gap}Nearly sixty years later, a gap was found. "
                      "{ei}[Écalle](/ˌAkˈæl/) and Ilyashenko finally proved it around 1991, with hundreds of pages of "
                      "asymptotic analysis. {u}But a bound depending only on the degree remained open. "
                      "Steve Smale put it on his list of problems for the twenty-first century.") as s:
            s.wait_until("dul")
            self.play(FadeIn(rows[0]))
            s.wait_until("gap")
            self.play(FadeIn(rows[1]))
            s.wait_until("ei")
            self.play(FadeIn(rows[2]))
            s.wait_until("u")
            self.play(FadeIn(rows[3]))
        self.play(FadeOut(rows))

        # ------------------------------------------------------------ the theorem
        thm = VGroup(Tex(r"\textbf{Theorem.} For each degree $d$ there is a finite $B(d)$ such that every real",
                         font_size=36),
                     Tex(r"planar polynomial vector field of degree $\le d$ has at most $B(d)$ limit cycles.",
                         font_size=36),
                     Tex(r"(any coefficients, positions, stability; no explicit formula for $B(d)$)",
                         font_size=28, color=GREY_A)).arrange(DOWN, buff=0.25)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3)).shift(UP * 1.5)
        lien = VGroup(Tex(r"Companion: quintic Li\'enard systems have at most \textbf{2} limit cycles", font_size=30,
                          color=TEAL_3B),
                      Tex(r"(and 2 really occurs)", font_size=28, color=TEAL_3B),
                      MathTex(r"\dot x=y-F(x),\quad \dot y=-x,\quad \deg F\le 5", font_size=34, color=TEAL_3B)
                      ).arrange(DOWN, buff=0.2).shift(DOWN * 1.6)
        with self.say("A manuscript in OpenAI's math catalogue claims exactly that bound. "
                      "{t}For every degree d, there is a finite number B of d, such that every polynomial flow of "
                      "degree d has at most B of d limit cycles. The proof does not give a formula for it. "
                      f"{{l}}A companion paper settles a concrete case exactly: {LIEN} systems with a fifth-degree "
                      "polynomial have at most two limit cycles, and two really happens.") as s:
            s.wait_until("t")
            self.play(Write(thm[:2]), Create(tb[1]), run_time=3)
            self.play(FadeIn(thm[2]))
            s.wait_until("l")
            self.play(FadeIn(lien))
        self.play(FadeOut(VGroup(tb, lien)))

        # quintic Liénard picture with two cycles
        ax3 = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=6.4, y_length=6.4, tips=False,
                   axis_config={"color": GREY_D}).shift(LEFT * 2.8)
        stable = integrate(quint, [2.0, 0.0], 120, dt=0.02)[-400:]
        unstable = integrate(quint, [1.02, 0.0], 120, dt=0.02, sign=-1)[-400:]
        cs = self.traj(ax3, stable, YELLOW_3B, 6)
        cu = self.traj(ax3, unstable, RED_3B, 6)
        tr = VGroup(self.traj(ax3, integrate(quint, [1.15, 0.0], 60, dt=0.02), BLUE_3B, 2),
                    self.traj(ax3, integrate(quint, [0.9, 0.0], 60, dt=0.02), TEAL_3B, 2),
                    self.traj(ax3, integrate(quint, [2.8, 0.0], 60, dt=0.02), BLUE_3B, 2))
        leg = VGroup(Tex("stable cycle", font_size=30, color=YELLOW_3B),
                     Tex("unstable cycle", font_size=30, color=RED_3B),
                     MathTex(r"F(x)=\tfrac{3}{25}\left(x^5-\tfrac{25}{6}x^3+\tfrac52 x\right)", font_size=32)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.6)
        with self.say("Here are two such cycles, in a quintic {LIEN} system. ".replace("{LIEN}", LIEN) +
                      "{tr}Paths starting between them are pushed outward to the stable cycle, "
                      "or fall inward to the center. {u}The unstable cycle is the watershed.") as s:
            self.play(Create(ax3), FadeIn(leg[2]))
            s.wait_until("tr")
            self.play(*[Create(t) for t in tr], run_time=4, rate_func=linear)
            self.play(Create(cs), FadeIn(leg[0]))
            s.wait_until("u")
            self.play(Create(cu), FadeIn(leg[1]))
        self.play(FadeOut(VGroup(ax3, cs, cu, tr, leg)))

        # ------------------------------------------------------------ proof idea
        hdr = Tex("Why uniform bounds are hard", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.4)
        ax4 = Axes(x_range=[0, 1.2, 1], y_range=[0, 1.2, 1], x_length=4, y_length=4, tips=False,
                   axis_config={"color": GREY_D}).shift(LEFT * 4 + DOWN * 0.6)
        lam = 2.0
        hyps = VGroup(*[ax4.plot(lambda x, c=c: c / x**lam, x_range=[(c / 1.15) ** (1 / lam), 1.15],
                                 color=GREY_B, stroke_width=2, use_smoothing=False)
                        for c in [0.002, 0.01, 0.04, 0.12]])
        rr = 0.35
        flow = ax4.plot(lambda x: rr**lam / x**lam, x_range=[rr, 1.0], color=BLUE_3B, stroke_width=5, use_smoothing=False)
        din = Dot(ax4.c2p(rr, 1), color=WHITE)
        dout = Dot(ax4.c2p(1, rr**lam), color=BLUE_3B)
        flow2 = ax4.plot(lambda x: rr**lam / x**lam, x_range=[rr, 1.0], color=BLUE_3B, stroke_width=5)
        sad = MathTex(r"(r,1)\ \mapsto\ (1,\ r^{\lambda})", font_size=36, color=BLUE_3B).next_to(ax4, UP, buff=0.3).align_to(
            ax4, LEFT)
        sadl = Tex(r"passing a saddle: time $\log\frac1r$", font_size=28).next_to(ax4, DOWN, buff=0.3)
        pts = VGroup(
            Tex(r"As coefficients vary, cycles can be born from loops through saddles.", font_size=30),
            Tex(r"Return maps become compositions of powers $r^{\lambda}$, logarithms,", font_size=30),
            Tex(r"and exponentially small terms: no single convergent series.", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.1)
        with self.say("Why is a uniform bound so hard? {v}As you vary the coefficients, cycles can be born from loops "
                      "that pass through saddle points. {s}Near a saddle, a path entering at height r leaves at "
                      "r to the lambda, after a time of log one over r. "
                      "{c}Glue several such passages together, and the return map becomes a tangle of powers, "
                      "logarithms, and exponentially small corrections, with no single convergent series to "
                      "count zeros with.") as s:
            self.play(Write(hdr))
            s.wait_until("v")
            self.play(FadeIn(pts[0]))
            s.wait_until("s")
            self.play(Create(ax4), Create(hyps), run_time=1.5)
            self.play(FadeIn(din), Write(sad))
            self.play(Create(flow), run_time=2)
            self.play(FadeIn(dout), FadeIn(sadl))
            s.wait_until("c")
            self.play(FadeIn(pts[1:]), run_time=1.5)
        self.play(FadeOut(VGroup(ax4, hyps, flow, din, dout, sad, sadl, pts)), FadeOut(flow2))

        # the strategy
        steps = VGroup(
            Tex(r"\textbf{1.} Track each return map by a \emph{packet}: a tree of asymptotic", font_size=31),
            Tex(r"\quad expansions on nested complex domains", font_size=31),
            Tex(r"\textbf{2.} Separation theorem: if all the expansions vanish,", font_size=31),
            Tex(r"\quad the function vanishes \emph{exactly} $\Rightarrow$ zeros cannot pile up", font_size=31),
            Tex(r"\textbf{3.} For fixed degree, finitely many geometric templates", font_size=31),
            Tex(r"\quad (boxes, annuli, passage words of bounded length)", font_size=31),
            Tex(r"\textbf{4.} A projection-counting argument turns ``finite'' into ``uniformly bounded''",
                font_size=31, color=YELLOW_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(hdr, DOWN, buff=0.5)
        nested = VGroup(*[Ellipse(width=2.6 - 0.5 * i, height=1.6 - 0.3 * i, color=[BLUE_3B, TEAL_3B, GREEN_3B][i % 3],
                                  stroke_width=3) for i in range(4)]).to_corner(DR, buff=0.6)
        with self.say("The new proof attacks this tangle directly. {p}It tracks each return map with what it calls "
                      "a packet: a tree of successive asymptotic expansions, each valid on a nested complex domain. "
                      "{sep}Its key separation theorem says: if every expansion in the tree vanishes, the function "
                      "itself is exactly zero. That is what stops zeros from accumulating. "
                      "{tpl}For a fixed degree, the geometry reduces to finitely many templates. "
                      "{cnt}And a counting argument, applied across all of them, converts finiteness into a bound "
                      "that depends only on the degree.") as s:
            self.play(Transform(hdr, Tex("The strategy", font_size=40, color=YELLOW_3B).move_to(hdr)))
            s.wait_until("p")
            self.play(FadeIn(steps[0:2]), LaggedStart(*[Create(e) for e in nested], lag_ratio=0.3), run_time=2)
            s.wait_until("sep")
            self.play(FadeIn(steps[2:4]))
            s.wait_until("tpl")
            self.play(FadeIn(steps[4:6]))
            s.wait_until("cnt")
            self.play(FadeIn(steps[6]))
        self.play(FadeOut(VGroup(hdr, steps, nested)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Every degree-$d$ planar polynomial flow has at most $B(d)<\infty$ limit cycles",
             r"Quintic Li\'enard: at most 2 limit cycles \emph{(this part formalized in Lean)}",
             r"Manuscript: 160 pages, produced by an OpenAI model"],
            False, r"\emph{Uniform bounds for planar polynomial limit cycles} (Sept.\ 2026)")
        with self.say("A caveat. The quintic {LIEN} result has been formalized in the Lean proof assistant, ".replace(
                "{LIEN}", LIEN) +
                      "but the hundred-and-sixty-page uniform-bound proof has not, and it needs careful expert checking. "
                      "{c}If it holds, one of the last open parts of Hilbert's list has fallen, although nobody yet knows "
                      "the actual numbers, not even for degree two.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("c")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
