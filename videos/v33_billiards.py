from pathlib import Path

import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(Path(__file__).parent / "data" / "v33.npz")
ZK = "[Zemlyakov](/zɛmljəkˈɔf/)"
KER = "[Kerckhoff](/kˈɜɹkhɔf/)"
VOR = "[Vorobets](/vɔɹəbˈɛts/)"
CHA = "[Chaika](/ʧˈAkə/)"
ALPHA = 1.0


def to_screen(P, sc, off):
    P = np.atleast_2d(P)
    return np.c_[P[:, 0] * sc, P[:, 1] * sc, np.zeros(len(P))] + off


def table(T, sc, off, color=WHITE, width=4):
    return Polygon(*to_screen(T, sc, off), color=color, stroke_width=width)


def clip_line(T, n, c):
    """Segment of {x : x.n = c} inside triangle T (data coords), or None."""
    pts = []
    for i in range(3):
        a, b = T[i], T[(i + 1) % 3]
        fa, fb = a @ n - c, b @ n - c
        if fa * fb < 0:
            pts.append(a + (b - a) * fa / (fa - fb))
    return pts if len(pts) == 2 else None


class Video(NarratedScene):
    def pcloud(self, pts, color, size=None):
        if size is None:
            size = max(2, int(round(4 * config.pixel_width / 1920)))
        pm = PMobject(stroke_width=size)
        pm.add_points(pts, color=color)
        return pm

    def construct(self):
        Ti, Tr = D["Ti"], D["Tr"]
        card = title_card(self, "150", "Billiards in Irrational Triangles",
                          r"Every triangle with an angle irrational to $\pi$ has a weakly mixing billiard")
        with self.say("Billiards in a triangle."):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.4)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ hook: one ball
        sc, off = 7.0, np.array([-3.5, -2.3, 0])
        tab = table(Ti, sc, off)
        traj = to_screen(D["traj_i"], sc, off)
        nb = 14
        seg = np.linalg.norm(np.diff(traj[: nb + 1], axis=0), axis=1)
        cum = np.r_[0, np.cumsum(seg)]
        sv = ValueTracker(0.0)

        def partial_pts(s):
            k = int(np.searchsorted(cum, s, side="right"))
            k = min(max(k, 1), nb)
            f = (s - cum[k - 1]) / seg[k - 1]
            return np.vstack([traj[:k], traj[k - 1] + min(f, 1) * (traj[k] - traj[k - 1])])

        path = always_redraw(lambda: VMobject(color=YELLOW_3B, stroke_width=3).set_points_as_corners(
            partial_pts(max(sv.get_value(), 1e-3))))
        ball = always_redraw(lambda: Dot(partial_pts(max(sv.get_value(), 1e-3))[-1], radius=0.1, color=WHITE))
        many = VMobject(color=YELLOW_3B, stroke_width=1, stroke_opacity=0.35).set_points_as_corners(traj[: 500])
        with self.say("A ball rolls on a triangular table, with no friction. It moves in straight lines, "
                      "{b}and bounces off each side like light off a mirror: the angle in equals the angle out. "
                      "{long}Follow it long enough, and its path seems to fill the whole table. "
                      "{q}But does it really explore everything, evenly? For a given triangle, proving that has been "
                      "remarkably hard.") as s:
            self.play(Create(tab))
            self.add(path, ball)
            s.wait_until("b")
            self.play(sv.animate.set_value(cum[-1]), run_time=s.until("long") + 0.5, rate_func=linear)
            self.remove(path, ball)
            self.add(VMobject(color=YELLOW_3B, stroke_width=3).set_points_as_corners(traj[: nb + 1]))
            self.play(Create(many), run_time=4, rate_func=linear)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ------------------------------------------------------------ rational vs irrational: directions
        sc2 = 5.0
        offL, offR = np.array([-6.3, -0.1, 0]), np.array([0.8, -0.1, 0])
        tabR = table(Tr, sc2, offL)
        tabI = table(Ti, sc2, offR)
        trR = VMobject(color=BLUE_3B, stroke_width=1, stroke_opacity=0.4).set_points_as_corners(
            to_screen(D["traj_r"][:400], sc2, offL))
        trI = VMobject(color=YELLOW_3B, stroke_width=1, stroke_opacity=0.4).set_points_as_corners(
            to_screen(D["traj_i"][:400], sc2, offR))
        rc = 1.0
        cR, cI = offL + np.array([2.5, -1.9, 0]), offR + np.array([2.5, -1.9, 0])
        compR = Circle(rc, color=GREY_D, stroke_width=2).move_to(cR)
        compI = Circle(rc, color=GREY_D, stroke_width=2).move_to(cI)
        dR = np.mod(D["dirs_r"][:400], TAU)
        dI = np.mod(D["dirs_i"][:2000], TAU)
        spokesR = VGroup(*[Line(cR, cR + rc * np.array([np.cos(a), np.sin(a), 0]), color=BLUE_3B, stroke_width=3)
                           for a in np.unique(np.round(dR, 6))])
        nI = ValueTracker(1)
        # point count changes every frame, so swap the cloud instead of become()-interpolating it
        dotsI = Group()

        def _refresh_dots(m):
            m.submobjects = [self.pcloud(np.array([cI + rc * np.array([np.cos(a), np.sin(a), 0])
                                                   for a in dI[: max(1, int(nI.get_value()))]]), YELLOW_3B)]

        dotsI.add_updater(_refresh_dots)
        _refresh_dots(dotsI)
        lR = Tex(r"angles $60^\circ, 45^\circ, 75^\circ$", font_size=30, color=BLUE_3B).next_to(tabR, UP, buff=0.2)
        lI = Tex(r"angle at left corner: 1 radian", font_size=30, color=YELLOW_3B).next_to(tabI, UP, buff=0.2)
        dlR = Tex(r"only 24\\ directions", font_size=28, color=BLUE_3B).next_to(compR, LEFT, buff=0.3)
        dlI = Tex(r"directions\\ never repeat", font_size=28, color=YELLOW_3B).next_to(compI, LEFT, buff=0.3)
        with self.say("The answer depends on the angles. {rat}In this triangle, the angles are rational multiples of "
                      "pi: sixty, forty-five and seventy-five degrees. Each bounce changes the direction in a fixed, "
                      "finite pattern, {sp}so the ball only ever travels in twenty-four directions. "
                      "{inv}It can never explore all of its states, which record both its position and its direction. "
                      "{irr}Now change the angles slightly, so that one corner is exactly one radian, an irrational "
                      "multiple of pi. {dd}Now the directions never repeat, and they spread around the whole "
                      "circle.") as s:
            s.wait_until("rat")
            self.play(Create(tabR), FadeIn(lR))
            self.play(Create(trR), run_time=2.5, rate_func=linear)
            s.wait_until("sp")
            self.play(Create(compR), Create(spokesR), FadeIn(dlR), run_time=1.5)
            s.wait_until("irr")
            self.play(Create(tabI), FadeIn(lI))
            self.play(Create(trI), run_time=2.5, rate_func=linear)
            s.wait_until("dd")
            self.add(compI, dotsI)
            self.play(nI.animate.set_value(len(dI)), FadeIn(dlI), run_time=3, rate_func=linear)
        dotsI.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ------------------------------------------------------------ unfolding and history
        copies = D["copies"]
        allp = copies.reshape(-1, 2)
        sc3 = 6.2 / (allp[:, 0].max() - allp[:, 0].min())
        off3 = np.array([-0.1, 0.6, 0]) - sc3 * np.array([allp[:, 0].min(), allp[:, 1].min(), 0])
        off3[0] -= 0.0
        fold_off = np.array([-6.6, 0.75, 0])
        sc_f = 3.2
        orig = table(Ti, sc_f, fold_off)
        fold = VMobject(color=YELLOW_3B, stroke_width=3).set_points_as_corners(to_screen(D["fold_pts"], sc_f, fold_off))
        cps = VGroup(*[table(c, sc3, off3, color=GREY_B, width=2).set_fill(BLUE_3B, 0.12 if k else 0.3)
                       for k, c in enumerate(copies)])
        straight = Line(to_screen(D["fold_pts"][0], sc3, off3)[0], to_screen(D["endP"], sc3, off3)[0],
                        color=YELLOW_3B, stroke_width=3)
        unl = Tex(r"reflect the table, not the ball:\\ the path becomes straight", font_size=30).next_to(
            cps, DOWN, buff=0.25)
        hist = VGroup(
            Tex(r"1975 \quad Zemlyakov--Katok: unfolding", font_size=28),
            Tex(r"1986 \quad Kerckhoff--Masur--Smillie: rational tables, almost every direction;", font_size=28),
            Tex(r"\qquad\quad ergodic tables for a dense, topologically generic family", font_size=28),
            Tex(r"1997 \quad Vorobets: explicit examples with very fast rational approximation", font_size=28),
            Tex(r"2026 \quad Chaika--Forni: weak mixing for a dense, generic family of polygons", font_size=28),
            Tex(r"numerics: conflicting evidence for specific irrational triangles", font_size=28, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.3)
        with self.say("The classic tool is unfolding. {unf}Instead of bouncing the ball, reflect the table across "
                      f"the side it hits, and the path becomes a straight line. {ZK} and Katok used this in 1975. "
                      f"{{kms}}For rational tables, unfolding builds a flat surface, and {KER}, Masur and Smillie "
                      "proved in 1986 that the motion is uniquely ergodic in almost every direction. Their work also "
                      f"gave ergodic tables for a dense, topologically generic family. {{vor}}{VOR} found explicit "
                      "ergodic examples, whose angles are extremely well approximated by rational ones. "
                      f"{{cf}}Recently, {CHA} and Forni proved weak mixing for a dense, generic family of polygons. "
                      "{num}But for any particular irrational triangle, there was no proof, and computer experiments "
                      "pointed in conflicting directions.") as s:
            self.play(Create(orig), Create(fold), run_time=1.5)
            s.wait_until("unf")
            self.play(FadeIn(cps[0]))
            for k in range(1, len(cps)):
                self.play(TransformFromCopy(cps[k - 1], cps[k]), run_time=0.45)
            self.play(Create(straight), FadeIn(unl), run_time=1.5)
            self.play(FadeIn(hist[0]))
            s.wait_until("kms")
            self.play(FadeIn(hist[1:3]))
            s.wait_until("vor")
            self.play(FadeIn(hist[3]))
            s.wait_until("cf")
            self.play(FadeIn(hist[4]))
            s.wait_until("num")
            self.play(FadeIn(hist[5]))
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ------------------------------------------------------------ theorem + cloud
        thm = VGroup(Tex(r"\textbf{Theorem.} If a triangle has an angle that is an irrational multiple of $\pi$,",
                         font_size=34),
                     Tex(r"its billiard flow is \textbf{weakly mixing} (for area $\times$ direction).", font_size=34),
                     Tex(r"Companion paper: the flow is \textbf{ergodic}.", font_size=30, color=GREY_A)
                     ).arrange(DOWN, buff=0.2)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3)).to_edge(UP, buff=0.35)
        with self.say("Two manuscripts in OpenAI's math catalogue now settle the question for every such triangle. "
                      "{erg}The first, from September, proves that the billiard is ergodic whenever at least one angle "
                      "is an irrational multiple of pi: for almost every start, the ball spends time in each region "
                      "of positions and directions in proportion to its size. {wm}The second, from October, proves "
                      "more: the flow is weakly mixing.") as s:
            s.wait_until("erg")
            self.play(Write(thm[0]), Create(tb[1]), FadeIn(thm[2]), run_time=2)
            s.wait_until("wm")
            self.play(Write(thm[1]))

        sc4 = 4.6
        oL4, oR4 = np.array([-6.4, -1.5, 0]), np.array([0.6, -1.5, 0])
        tL, tR = table(Ti, sc4, oL4), table(Tr, sc4, oR4)
        ci, cr = D["cloud_i"], D["cloud_r"]
        di, dr = D["cdir_i"], D["cdir_r"]
        rc4 = 0.62
        ccL, ccR = oL4 + np.array([5.35, 0.6, 0]), oR4 + np.array([5.35, 0.6, 0])
        ft = ValueTracker(0)
        nshow = 900

        def cloud(P, o):
            return self.pcloud(to_screen(P[:nshow], sc4, o), WHITE)

        def comp(dirs, c, col):
            a = dirs[:nshow]
            return self.pcloud(np.c_[c[0] + rc4 * np.cos(a), c[1] + rc4 * np.sin(a), np.zeros(len(a))], col)

        cL = always_redraw(lambda: cloud(ci[int(ft.get_value())], oL4))
        cR_ = always_redraw(lambda: cloud(cr[int(ft.get_value())], oR4))
        kL = always_redraw(lambda: comp(di[int(ft.get_value())], ccL, YELLOW_3B))
        kR = always_redraw(lambda: comp(dr[int(ft.get_value())], ccR, BLUE_3B))
        rings = VGroup(Circle(rc4, color=GREY_D, stroke_width=2).move_to(ccL),
                       Circle(rc4, color=GREY_D, stroke_width=2).move_to(ccR))
        rl = VGroup(Tex("directions", font_size=24, color=GREY_A).next_to(rings[0], DOWN, buff=0.1),
                    Tex("directions", font_size=24, color=GREY_A).next_to(rings[1], DOWN, buff=0.1))
        tl = VGroup(Tex("irrational", font_size=30, color=YELLOW_3B).next_to(tL, DOWN, buff=0.15),
                    Tex("rational", font_size=30, color=BLUE_3B).next_to(tR, DOWN, buff=0.15))
        note = Tex(r"(simulation, 900 balls)", font_size=24, color=GREY_B).to_corner(DR, buff=0.25)
        hdr4 = Tex(r"Intuition: a cloud of balls, irrational vs.\ rational table", font_size=34,
                   color=YELLOW_3B).to_edge(UP, buff=0.45)
        with self.say("Here is the intuition. {cl}Start nine hundred balls close together, all heading the same way. "
                      "{go}In the irrational triangle, the cloud spreads over every position and every direction. "
                      "In the rational one, positions spread, but directions stay locked to twenty-four values. "
                      "{def}Precisely, weak mixing means there is no hidden clock: no measurable quantity that just "
                      "rotates at a steady rate as the ball moves. Equivalently, two independent balls, watched "
                      "together, still form an ergodic system.") as s:
            self.play(FadeOut(tb))
            self.play(Create(tL), Create(tR), FadeIn(tl), Create(rings), FadeIn(rl), FadeIn(note), FadeIn(hdr4))
            s.wait_until("cl")
            self.add(cL, cR_, kL, kR)
            self.wait(0.8)
            s.wait_until("go")
            self.play(ft.animate.set_value(len(D["times"]) - 1), run_time=max(6, s.until("def") + 3),
                      rate_func=linear)
        for m in (cL, cR_, kL, kR):
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ------------------------------------------------------------ proof: the double and the hidden clock
        hdr = Tex("The proof: no hidden clock", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.4)
        sc5 = 3.2
        o5 = np.array([-6.0, 0.0, 0])
        top = table(Ti, sc5, o5, color=WHITE).set_fill(BLUE_3B, 0.25)
        Tm = Ti * np.array([1, -1])
        bot = table(Tm, sc5, o5, color=WHITE).set_fill(TEAL_3B, 0.25)
        cone = VGroup(*[Dot(to_screen(Ti[k], sc5, o5)[0], radius=0.09, color=RED_3B) for k in range(3)],
                      Dot(to_screen(Tm[2], sc5, o5)[0], radius=0.09, color=RED_3B))
        vlab = VGroup(MathTex("A", font_size=30).next_to(cone[0], LEFT, buff=0.12),
                      MathTex("B", font_size=30).next_to(cone[1], RIGHT, buff=0.12),
                      MathTex("C", font_size=30).next_to(cone[2], UP, buff=0.12),
                      MathTex("C", font_size=30).next_to(cone[3], DOWN, buff=0.12))
        dl = Tex(r"two copies glued along all three sides:\\ a flat surface with 3 cone points", font_size=28).next_to(
            VGroup(top, bot, vlab), DOWN, buff=0.2)
        eqs = VGroup(
            MathTex(r"F(\text{state after time } t) = e^{i\lambda t}\,F(\text{state})", font_size=36),
            MathTex(r"X F = i\lambda F", r"\qquad Y F = \ ?", font_size=38),
            Tex(r"$X$: along the motion; \ $Y$: sideways. $F$ is only measurable.", font_size=28, color=GREY_A),
            MathTex(r"\|XF\|^2+\|YF\|^2 \le \lambda^2\|F\|^2", font_size=40, color=YELLOW_3B),
            MathTex(r"\Rightarrow\ YF = 0", font_size=40, color=YELLOW_3B),
        ).arrange(DOWN, buff=0.3).move_to(RIGHT * 2.6 + DOWN * 0.1)
        eqs[4].next_to(eqs[3], DOWN, buff=0.25)
        how = Tex(r"angular Fourier modes, smoothing away from the corners,\\ and two limits taken in the right order",
                  font_size=26, color=GREY_A).next_to(eqs[4], DOWN, buff=0.3)
        with self.say("How do you rule out a hidden clock? {dbl}First, glue two copies of the triangle along all three "
                      "sides. Bouncing becomes straight motion on a flat surface, with three cone points at the "
                      "corners. {clk}A hidden clock would be a quantity F that gets multiplied by e to the i lambda t "
                      "after time t. {xy}So its derivative along the motion is i lambda F. Its sideways derivative is "
                      "unknown: F might be wildly irregular. {key}The heart of the proof is an energy estimate, "
                      "using angular Fourier modes, smoothing only away from the corners, and two limits taken in "
                      "the right order. It gives exactly this sharp bound. {y0}Since the first term already equals "
                      "the right side, the sideways derivative must vanish.") as s:
            self.play(Write(hdr))
            s.wait_until("dbl")
            self.play(DrawBorderThenFill(top), run_time=1.2)
            self.play(TransformFromCopy(top, bot), run_time=1.2)
            self.play(FadeIn(cone), FadeIn(vlab), FadeIn(dl))
            s.wait_until("clk")
            self.play(Write(eqs[0]))
            s.wait_until("xy")
            self.play(Write(eqs[1]), FadeIn(eqs[2]))
            s.wait_until("key")
            self.play(Write(eqs[3]), FadeIn(how))
            s.wait_until("y0")
            self.play(Write(eqs[4]))
        self.play(*[FadeOut(m) for m in self.mobjects if m is not hdr])

        # ------------------------------------------------------------ plane waves and the irrational rotation
        sc6 = 6.0
        o6 = np.array([-6.5, -2.4, 0])
        tab6 = table(Ti, sc6, o6)
        ang = 0.55
        nvec = np.array([np.cos(ang), np.sin(ang)])
        ph = ValueTracker(0)
        lam = 2 * PI / 0.13

        def waves():
            g = VGroup()
            for c in np.arange(-0.2, 1.3, 0.13):
                seg_ = clip_line(Ti, nvec, c + ph.get_value() % 0.13)
                if seg_ is not None:
                    g.add(Line(*to_screen(np.array(seg_), sc6, o6), color=BLUE_3B, stroke_width=3))
            return g

        wv = always_redraw(waves)
        arr = Arrow(to_screen(np.array([0.32, 0.2]), sc6, o6)[0], to_screen(np.array([0.32, 0.2]) + 0.16 * nvec, sc6, o6)[0],
                    buff=0, color=YELLOW_3B, stroke_width=6)
        arr_l = MathTex("v", font_size=34, color=YELLOW_3B).next_to(arr.get_end(), UP, buff=0.05)
        pw = MathTex(r"F(x,v) = c(v)\, e^{i\lambda\, x\cdot v}", font_size=40).to_corner(UR, buff=0.5).shift(DOWN * 0.7)
        pwl = Tex(r"a plane wave, with an amplitude\\ depending on the direction", font_size=28, color=GREY_A).next_to(
            pw, DOWN, buff=0.2)
        with self.say("With no sideways change, inside the triangle F must be a plane wave: {pw}an amplitude c of v, "
                      "depending only on the direction, times a wave that advances steadily as the ball moves "
                      "along v.") as s:
            self.play(Create(tab6), FadeIn(wv), GrowArrow(arr), FadeIn(arr_l))
            s.wait_until("pw")
            self.play(Write(pw), FadeIn(pwl))
            self.play(ph.animate.set_value(0.39), run_time=s.remaining() + 0.3, rate_func=linear)
        wv.clear_updaters()
        self.play(FadeOut(VGroup(wv, arr, arr_l, pwl)), pw.animate.scale(0.85).to_corner(UR, buff=0.4).shift(DOWN * 0.7))

        A = to_screen(Ti[0], sc6, o6)[0]
        th0 = 0.35
        cc = RIGHT * 3.7 + DOWN * 1.45
        rr = 1.25
        dirv = lambda a: np.array([np.cos(a), np.sin(a), 0])
        ring = Circle(rr, color=GREY_D, stroke_width=2).move_to(cc)
        sideAB = Line(to_screen(Ti[0], sc6, o6)[0], to_screen(Ti[1], sc6, o6)[0], color=TEAL_3B, stroke_width=7)
        sideAC = Line(to_screen(Ti[0], sc6, o6)[0], to_screen(Ti[2], sc6, o6)[0], color=PURPLE_3B, stroke_width=7)
        mAB = DashedLine(cc - 1.45 * rr * dirv(0), cc + 1.45 * rr * dirv(0), color=TEAL_3B, stroke_width=3)
        mAC = DashedLine(cc - 1.45 * rr * dirv(ALPHA), cc + 1.45 * rr * dirv(ALPHA), color=PURPLE_3B, stroke_width=3)
        d0 = Arrow(cc, cc + rr * dirv(th0), buff=0, color=WHITE, stroke_width=5)
        d1 = Arrow(cc, cc + rr * dirv(-th0), buff=0, color=GREY_B, stroke_width=5)
        d2 = Arrow(cc, cc + rr * dirv(2 * ALPHA + th0), buff=0, color=YELLOW_3B, stroke_width=5)
        corner_l = MathTex(r"\alpha = 1", font_size=34, color=YELLOW_3B).move_to(A + 0.75 * dirv(0.5))
        rot_l = Tex(r"two reflections $=$ rotation by $2\alpha$", font_size=30)
        rot_l.next_to(pw, DOWN, buff=0.35).align_to(pw, RIGHT)
        dirs_l = Tex("directions", font_size=24, color=GREY_A).next_to(ring, DOWN, buff=0.12)
        kmax = ValueTracker(1)
        orbit = always_redraw(lambda: VGroup(*[Dot(cc + rr * dirv(th0 + 2 * k * ALPHA), radius=0.045, color=YELLOW_3B)
                                               for k in range(int(kmax.get_value()))]))
        dense = Tex(r"$\alpha/\pi$ irrational:\\ the orbit is dense", font_size=28, color=YELLOW_3B).next_to(
            ring, LEFT, buff=0.6)
        const = Tex(r"$\Rightarrow c(v)$ is constant", font_size=32, color=YELLOW_3B).next_to(dense, DOWN, buff=0.3)
        third = Tex(r"third side (away from that corner) $\Rightarrow \lambda=0$", font_size=30, color=TEAL_3B
                    ).to_corner(DL, buff=0.3)
        with self.say("Now the reflections take over. {two}Reflect the direction in one side through the "
                      "irrational corner, then in the other. The result is a rotation by twice that angle, and the "
                      "amplitude must be unchanged by it. {orb}Because the angle is an irrational multiple of pi, "
                      "repeated rotation sweeps densely around the circle, {cst}which forces the amplitude to be "
                      "constant. {thd}Finally, the third side, which misses that corner, forces lambda to be zero. "
                      "So the only clock is a constant. No hidden clock, and so the flow is weakly mixing.") as s:
            s.wait_until("two")
            self.play(FadeIn(corner_l), Create(sideAB), Create(sideAC), Create(ring), FadeIn(dirs_l))
            self.play(GrowArrow(d0))
            self.play(Create(mAB), TransformFromCopy(d0, d1))
            self.play(Create(mAC), TransformFromCopy(d1, d2), FadeIn(rot_l))
            s.wait_until("orb")
            self.add(orbit)
            self.play(kmax.animate.set_value(160), FadeIn(dense), run_time=3, rate_func=linear)
            s.wait_until("cst")
            self.play(FadeIn(const))
            s.wait_until("thd")
            self.play(FadeIn(third))
        orbit.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"\mbox{Every triangle with an angle irrational to $\pi$: the billiard flow is weakly mixing}",
             r"\mbox{Companion result: ergodicity \emph{(formalized in Lean)}; weak mixing is not}",
             r"\mbox{Manuscripts: 12 and 13 pages, produced by an OpenAI model, not yet peer reviewed}"],
            False, r"\mbox{\emph{Weak mixing of triangular billiards with an irrational angle} (Oct.\ 2026)}")
        with self.say("A note on verification. The ergodicity theorem has been formalized in the Lean proof "
                      "assistant. {c}The stronger weak mixing result has not been formalized yet, and both manuscripts, "
                      "written by an OpenAI model, still await peer review.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("c")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
