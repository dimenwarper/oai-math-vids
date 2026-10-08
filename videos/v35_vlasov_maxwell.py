from pathlib import Path

import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(Path(__file__).parent / "data" / "v35.npz")
VLA = "[Vlasov](/vlˈɑsɔf/)"
WOL = "[Wollman](/wˈʊlmən/)"
PFA = "[Pfaffelmoser](/pfˈæfəlmˌOzəɹ/)"
DIP = "[DiPerna](/dipˈɜɹnə/)"


def px(base):
    return max(1, int(round(base * config.pixel_width / 1920)))


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "362", "Plasmas Stay Smooth",
                          r"Global classical solutions of the 3D relativistic Vlasov--Maxwell system")
        with self.say(f"Do plasmas stay smooth? The relativistic {VLA} Maxwell system."):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.4)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ phase-space cartoon
        S = D["snaps"]
        ax = Axes(x_range=[-4, 4, 1], y_range=[-7, 7, 2], x_length=7.6, y_length=6.0, tips=False,
                  axis_config={"color": GREY_D}).shift(LEFT * 2.3 + DOWN * 0.3)
        xl = Tex("position", font_size=28).next_to(ax.x_axis.get_right(), DOWN, buff=0.15)
        vl = Tex("momentum", font_size=28).next_to(ax.y_axis.get_top(), RIGHT, buff=0.15)
        x0 = S[0, :, 0]
        cols = [interpolate_color(ManimColor(BLUE_3B), ManimColor(YELLOW_3B), (a + 1) / 2) for a in x0]
        ft = ValueTracker(0)

        rgbas = np.array([np.r_[c.to_rgb(), 1.0] for c in cols])

        def cloud():
            P = S[int(ft.get_value())]
            pm = PMobject(stroke_width=px(5))
            pts = np.array([ax.c2p(a, b) for a, b in P])
            pm.add_points(pts, rgbas=rgbas)
            return pm

        cl = always_redraw(cloud)
        note = Tex(r"a one-dimensional cartoon:\\ like charges, electric field only", font_size=28, color=GREY_A)
        note.to_corner(UR, buff=0.5)
        pts_ = VGroup(Tex(r"density $f(t,x,v)$ in phase space", font_size=30),
                      Tex(r"(3 position $+$ 3 momentum", font_size=28, color=GREY_A),
                      Tex(r"coordinates in reality)", font_size=28, color=GREY_A),
                      Tex(r"it folds and stretches,\\ but does it stay smooth?", font_size=30, color=YELLOW_3B)
                      ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(note, DOWN, buff=0.6).align_to(note, LEFT)
        pts_[3].shift(DOWN * 0.3)
        VGroup(note, pts_).to_edge(RIGHT, buff=0.35)
        with self.say("A plasma is a gas of charged particles so hot and thin that they almost never collide. "
                      "Instead, each particle is steered by the electric and magnetic fields created by all the "
                      "others. {f}Rather than tracking every particle, kinetic theory tracks their density in phase "
                      "space, which records position and momentum together. {c}Here is a one-dimensional cartoon: a "
                      "cloud of like charges, at first rushing inward. {g}As it evolves, the density folds and "
                      "stretches. The real question lives in six dimensions: does it stay smooth forever?") as s:
            self.play(Create(ax), FadeIn(xl), FadeIn(vl))
            s.wait_until("f")
            self.add(cl)
            self.play(FadeIn(pts_[0:3]))
            s.wait_until("c")
            self.play(FadeIn(note))
            self.play(ft.animate.set_value(len(S) - 1), run_time=max(4, s.remaining() - 0.5), rate_func=linear)
            self.play(FadeIn(pts_[3]), run_time=0.5)
        cl.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ------------------------------------------------------------ the equations; u(v)
        eqs = VGroup(
            MathTex(r"\partial_t f + u(v)\cdot\nabla_x f + \big(E + u(v)\times B\big)\cdot\nabla_v f = 0", font_size=40),
            MathTex(r"\partial_t E - \nabla\times B = -j_f,\qquad \partial_t B + \nabla\times E = 0", font_size=40),
            MathTex(r"\nabla\cdot E = \rho_f,\qquad \nabla\cdot B = 0", font_size=40),
        ).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.45)
        lab = VGroup(Tex(r"particles carried by the Lorentz force", font_size=26, color=GREY_A).next_to(eqs[0], DOWN,
                                                                                                    buff=0.08),
                     )
        eqs[1:].shift(DOWN * 0.3)
        ax2 = Axes(x_range=[0, 8, 2], y_range=[0, 1.2, 0.5], x_length=5.2, y_length=2.6, tips=False,
                   axis_config={"color": GREY_B, "include_numbers": True, "font_size": 22}).to_corner(DL, buff=0.6)
        ucurve = ax2.plot(lambda t: t / np.sqrt(1 + t * t), x_range=[0, 8], color=YELLOW_3B, stroke_width=4)
        one = DashedLine(ax2.c2p(0, 1), ax2.c2p(8, 1), color=GREY_B)
        ul = MathTex(r"u(v)=\frac{v}{\sqrt{1+|v|^2}}", font_size=36).next_to(ax2, RIGHT, buff=0.6).shift(UP * 0.5)
        ul2 = Tex(r"momentum $v$: unbounded\\ speed $|u|$: always below 1 (light)", font_size=28, color=GREY_A
                  ).next_to(ul, DOWN, buff=0.25)
        axl = MathTex("v", font_size=28).next_to(ax2.x_axis, RIGHT, buff=0.1)
        with self.say(f"In three dimensions, the model is the relativistic {VLA} Maxwell system. "
                      "{e1}The density is transported along the particle motion, driven by the Lorentz force. "
                      "{e2}The fields obey Maxwell's equations, with the particles' charge and current as sources. "
                      "{rel}Relativity enters through the velocity u, which is v over the square root of one plus v "
                      "squared. {cap}Momentum can grow without bound, but speed always stays below the speed of "
                      "light, set to one here.") as s:
            s.wait_until("e1")
            self.play(Write(eqs[0]), FadeIn(lab), run_time=2)
            s.wait_until("e2")
            self.play(Write(eqs[1:]), run_time=2)
            s.wait_until("rel")
            self.play(Create(ax2), FadeIn(axl), Write(ul))
            s.wait_until("cap")
            self.play(Create(ucurve), Create(one), FadeIn(ul2), run_time=2)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ------------------------------------------------------------ history
        hdr = Tex("Smooth forever, or a finite-time breakdown?", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.4)
        rows = VGroup(
            Tex(r"1984 \quad Wollman: smooth solutions exist for a short time", font_size=32),
            Tex(r"1986 \quad Glassey--Strauss: breakdown could only happen at high momenta", font_size=32,
                color=TEAL_3B),
            Tex(r"1987 \quad Glassey--Strauss: global for dilute (small) data", font_size=32),
            Tex(r"1989 \quad DiPerna--Lions: global \emph{weak} solutions (no uniqueness, no smoothness)", font_size=32),
            Tex(r"1990--98 \quad Glassey--Schaeffer: lower-dimensional versions", font_size=32),
            Tex(r"1992 \quad Pfaffelmoser: electrostatic cousin (Vlasov--Poisson), general data", font_size=32),
            Tex(r"2026 \quad Wang: large data with cylindrical symmetry", font_size=32),
            Tex(r"open \quad general large data in 3D, no symmetry", font_size=32, color=YELLOW_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).next_to(hdr, DOWN, buff=0.55)
        with self.say("Start from smooth data. Does the solution stay smooth forever, or can it break down in finite "
                      f"time? {{w}}{WOL} showed in 1984 that smooth solutions exist for a short time. {{gs}}In 1986, "
                      "Glassey and Strauss proved that a breakdown could only happen at high momenta: as long as "
                      "particle momenta stay bounded, the solution continues. {{sm}}Global results followed under "
                      f"restrictions: small, dilute data; {DIP} and Lions' weak solutions, without uniqueness or "
                      f"smoothness; lower-dimensional versions; and {{pf}}{PFA}'s 1992 solution of the electrostatic "
                      "cousin, the [Vlasov](/vlˈɑsɔf/) Poisson system. {wa}Work by [Xuecheng](/ʃˈuɛʧˌʌŋ/) Wang, completed this "
                      "July, handles large data with cylindrical symmetry. {op}General large data in three dimensions "
                      "remained unresolved.".replace(
                          "{{", "{").replace("}}", "}")) as s:
            self.play(Write(hdr))
            s.wait_until("w")
            self.play(FadeIn(rows[0]))
            s.wait_until("gs")
            self.play(FadeIn(rows[1]))
            s.wait_until("sm")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[2:5]], lag_ratio=0.6), run_time=3)
            s.wait_until("pf")
            self.play(FadeIn(rows[5]))
            s.wait_until("wa")
            self.play(FadeIn(rows[6]))
            s.wait_until("op")
            self.play(FadeIn(rows[7]))
        self.play(FadeOut(VGroup(hdr, rows)))

        # ------------------------------------------------------------ theorem
        thm = VGroup(Tex(r"\textbf{Theorem.} Every smooth admissible initial datum generates a unique", font_size=34),
                     Tex(r"global classical solution, smooth on every finite time interval.", font_size=34),
                     Tex(r"Admissible: smooth compactly supported $f_0\ge0$; finite-energy fields with", font_size=28,
                         color=GREY_A),
                     Tex(r"bounded derivatives; Gauss constraints. No smallness, no symmetry.", font_size=28,
                         color=GREY_A)).arrange(DOWN, buff=0.18)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3))
        with self.say("A manuscript in OpenAI's math catalogue now claims the answer: smooth forever. {t}Every smooth, "
                      "admissible initial state generates a unique global solution that stays smooth on every finite "
                      "time interval. {a}Admissible means the particle density is smooth and confined to a bounded "
                      "region, and the fields have finite energy and bounded derivatives. There is no smallness or "
                      "symmetry assumption.") as s:
            s.wait_until("t")
            self.play(Write(thm[:2]), Create(tb[1]), run_time=2.5)
            s.wait_until("a")
            self.play(FadeIn(thm[2:]))
        self.play(FadeOut(tb))

        # ------------------------------------------------------------ the doubling argument
        hdr = Tex("Why momenta cannot blow up", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.4)
        est = MathTex(r"|V(t_2)-V(t_1)| \le M P\sqrt{t_2-t_1} + A\,(t_2-t_1)\,\frac{P^2\log(2+P)}{w}", font_size=38)
        est.next_to(hdr, DOWN, buff=0.35)
        estl = Tex(r"signed impulse: integrate the force first, then take the size", font_size=28,
                   color=GREY_A).next_to(est, DOWN, buff=0.15)
        c_ = 3.0
        nmax = 40
        tn = np.cumsum([c_ / np.log(2 + 1024 * 2.0 ** k) for k in range(1, nmax + 1)])
        tn = np.r_[0, tn]
        ax3 = Axes(x_range=[0, 7, 1], y_range=[0, 40, 10], x_length=6.2, y_length=3.7, tips=False,
                   axis_config={"color": GREY_B, "include_numbers": True, "font_size": 22}).to_corner(DL, buff=0.55).shift(UP * 0.4)
        stair_pts = []
        for k in range(nmax):
            stair_pts += [ax3.c2p(tn[k], k), ax3.c2p(tn[k + 1], k), ax3.c2p(tn[k + 1], k + 1)]
        stair = VMobject(color=BLUE_3B, stroke_width=3).set_points_as_corners(stair_pts)
        a3x = Tex("time", font_size=26).next_to(ax3.x_axis, DOWN, buff=0.35)
        a3y = MathTex(r"\log_2(\text{max momentum})", font_size=26).next_to(ax3.y_axis, UP, buff=0.12).shift(RIGHT * 0.8)
        dbl = VGroup(Tex(r"time to double the largest momentum", font_size=30),
                     MathTex(r"\ \ge\ \frac{c}{\log(\text{momentum})}\ \sim\ \frac{c}{n}", font_size=38),
                     MathTex(r"\sum_n \frac{1}{n} = \infty", font_size=40, color=YELLOW_3B),
                     Tex(r"infinitely many doublings\\ take infinite time", font_size=30, color=YELLOW_3B)
                     ).arrange(DOWN, buff=0.25).to_corner(DR, buff=0.6)
        with self.say("Thanks to Glassey and Strauss, it is enough to show that particle momenta stay bounded on "
                      "every finite time interval. {est}The heart of the paper is an estimate on the change in a "
                      "particle's momentum over a time interval, where the size is taken only after integrating the "
                      "force, so that pushes in different directions can cancel. {dbl}It implies that doubling the "
                      "largest momentum takes at least a time of order one over its logarithm. Going from two to the "
                      "n minus one to two to the n takes time about c over n. {sum}Those times add up like the "
                      "harmonic series, which diverges. So infinitely many doublings would take infinite time, and "
                      "momenta can never blow up in finite time.") as s:
            self.play(Write(hdr))
            s.wait_until("est")
            self.play(Write(est), run_time=2.5)
            self.play(FadeIn(estl))
            s.wait_until("dbl")
            self.play(Create(ax3), FadeIn(a3x), FadeIn(a3y), FadeIn(dbl[0:2]))
            s.wait_until("sum")
            self.play(Create(stair), FadeIn(dbl[2]), run_time=3, rate_func=linear)
            self.play(FadeIn(dbl[3]))
        self.play(FadeOut(VGroup(est, estl, ax3, stair, a3x, a3y, dbl)))

        # ------------------------------------------------------------ light cone and the dangerous angles
        o = np.array([-3.7, -3.2, 0])
        P = lambda x, t: o + np.array([x, t, 0])
        X = lambda t: 0.4 * np.sin(0.45 * t)
        t0, win = 5.6, 3.0
        recv = ParametricFunction(lambda t: P(X(t), t), t_range=[0, t0], color=YELLOW_3B, stroke_width=5)
        rdot = Dot(P(X(t0), t0), color=YELLOW_3B, radius=0.1)
        rl = Tex("receiver", font_size=28, color=YELLOW_3B).next_to(rdot, UP, buff=0.12)
        apex = P(X(t0), t0)
        cl_, cr_ = P(X(t0) - win, t0 - win), P(X(t0) + win, t0 - win)
        cone = VGroup(Line(apex, cl_, color=WHITE, stroke_width=3), Line(apex, cr_, color=WHITE, stroke_width=3))
        cone_fill = Polygon(apex, cl_, cr_, stroke_width=0).set_fill(WHITE, 0.07)
        conel = Tex(r"past light cone", font_size=26).move_to(P(X(t0) - 1.0, t0 - win - 0.3))
        conel.add_background_rectangle(opacity=0.8, buff=0.05)
        fs = [lambda t: -2.1 + 0.45 * np.sin(0.7 * t + 0.3), lambda t: 1.5 + 0.5 * np.sin(0.5 * t + 1.2),
              lambda t: -0.8 + 0.35 * np.sin(0.9 * t + 2.0)]
        fast = lambda t: 3.05 - 0.9 * (t - 2.6)
        src_m, hits = VGroup(), VGroup()
        for f in fs + [fast]:
            ts = 2.2 if f is fast else 0
            src_m.add(ParametricFunction(lambda t, f=f: P(f(t), t), t_range=[ts, t0],
                                         color=ORANGE_3B if f is fast else BLUE_3B, stroke_width=3))
            tt = np.linspace(t0 - win, t0, 4000)
            g = np.abs(f(tt) - X(t0)) - (t0 - tt)
            idx = np.where(np.diff(np.sign(g)) != 0)[0]
            if len(idx):
                hits.add(Dot(P(f(tt[idx[0]]), tt[idx[0]]), color=RED_3B, radius=0.09))
        sl = Tex("sources", font_size=28, color=BLUE_3B).next_to(src_m[1].get_end(), RIGHT, buff=0.15)
        fl = VGroup(Tex("nearly along", font_size=24, color=ORANGE_3B), Tex("the light ray", font_size=24,
                    color=ORANGE_3B)).arrange(DOWN, buff=0.06).next_to(src_m[3].get_start(), DOWN, buff=0.1).shift(LEFT * 0.4)
        tax = Arrow(o + LEFT * 2.95 + DOWN * 0.1, o + LEFT * 2.95 + UP * 6.4, buff=0, color=GREY_B, stroke_width=3)
        tl_ = MathTex("t", font_size=30).next_to(tax.get_end(), RIGHT, buff=0.1)
        sch = Tex("(schematic, one space dimension)", font_size=24, color=GREY_B).to_corner(DL, buff=0.2).shift(RIGHT * 0.4)
        side = VGroup(
            Tex(r"the force comes from sources where", font_size=26),
            Tex(r"they cross the receiver's past light cone", font_size=26),
            Tex(r"sort them by momentum, distance, angle;", font_size=26),
            Tex(r"energy flux through the cone gives direct bounds", font_size=26),
            Tex(r"\textbf{the loss:} a factor $\sqrt{w}$, when a source moves", font_size=26, color=RED_3B),
            Tex(r"almost along the light ray", font_size=26, color=RED_3B),
            Tex(r"\textbf{the fix:} integrate along the source path", font_size=26, color=TEAL_3B),
            Tex(r"first: a total derivative plus milder terms", font_size=26, color=TEAL_3B),
            Tex(r"used twice: few direction changes, then", font_size=26),
            Tex(r"a coefficient $\le C/\sqrt{w}$, cancelling the loss", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.15)
        for k in (2, 4, 6, 8):
            side[k].shift(DOWN * 0.12)
            side[k + 1].shift(DOWN * 0.12)
        with self.say("Where does the estimate come from? {lc}The field acting on a particle, the receiver, is "
                      "produced by source particles at the moments they cross its backward light cone. {sort}The "
                      "proof sorts these sources by momentum, distance and angle, and uses the energy flowing through "
                      "the cone to bound each group directly. {loss}These direct bounds lose a factor of root w, "
                      "where w is the receiver's energy, exactly when a source moves almost along the light ray, more "
                      "closely than the receiver does. {fix}In that narrow window, the proof integrates the force along "
                      "the source's path before taking absolute values, which turns it into a total derivative plus "
                      "milder terms. {twice}This identity is used twice: first to show that particles cannot change "
                      "direction too often, and then to bound a coefficient by a constant over root w, which exactly "
                      "cancels the loss. A bootstrap argument then closes the estimate.") as s:
            self.play(Create(tax), FadeIn(tl_), Create(recv), FadeIn(sch), run_time=1.5)
            self.play(FadeIn(rdot), FadeIn(rl))
            s.wait_until("lc")
            self.play(Create(cone), FadeIn(cone_fill), FadeIn(conel))
            self.play(LaggedStart(*[Create(m) for m in src_m], lag_ratio=0.2), FadeIn(sl), FadeIn(fl), run_time=2)
            self.play(LaggedStart(*[FadeIn(h, scale=2) for h in hits], lag_ratio=0.2), FadeIn(side[0:2]))
            s.wait_until("sort")
            self.play(FadeIn(side[2:4]))
            s.wait_until("loss")
            self.play(FadeIn(side[4:6]), Indicate(hits[-1], color=RED_3B, scale_factor=2))
            s.wait_until("fix")
            self.play(FadeIn(side[6:8]))
            s.wait_until("twice")
            self.play(FadeIn(side[8:]))
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Every smooth admissible datum: a unique, globally smooth classical solution",
             r"3D, one species, relativistic; no smallness, symmetry, or neutrality assumption",
             r"Manuscript: 49 pages, produced by an OpenAI model, not yet peer reviewed"],
            True, r"\mbox{\emph{Global classical solutions of the 3D relativistic Vlasov--Maxwell system} (Sept.\ 2026)}")
        with self.say("The manuscript is forty-nine pages, written by an OpenAI model, and not yet peer reviewed. "
                      "{l}Its main theorem, global existence and uniqueness of smooth solutions, has been formalized "
                      "in the Lean proof assistant. It covers one species of particles; plasmas with several species "
                      "are not part of this result.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
