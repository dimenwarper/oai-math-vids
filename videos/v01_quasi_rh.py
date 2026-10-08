from pathlib import Path

import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(Path(__file__).parent / "data" / "v01.npz")
PRIMES = [p for p in range(2, 51) if all(p % d for d in range(2, int(p**0.5) + 1))]


def staircase(ax, xmax=50):
    pts, y = [ax.c2p(0, 0)], 0
    for p in PRIMES:
        if p > xmax:
            break
        pts += [ax.c2p(p, y), ax.c2p(p, y + 1)]
        y += 1
    pts.append(ax.c2p(xmax, y))
    return VMobject().set_points_as_corners(pts)


def curve(ax, xs, ys, **kw):
    m = VMobject(**kw)
    m.set_points_smoothly([ax.c2p(x, y) for x, y in zip(xs, ys)])
    return m


def explicit(ax, n, color=YELLOW_3B):
    ys = D["R"] + D["terms"][:n].sum(axis=0)
    return curve(ax, D["xs"], ys, color=color, stroke_width=3)


class Video(NarratedScene):
    def construct(self):
        # ---------------------------------------------------------------- title
        card = title_card(self, "003", "The Quasi-Riemann Hypothesis",
                          r"A zero-free wall for $\zeta(s)$ at $\operatorname{Re}(s)=7/8$")
        with self.say("The quasi-Riemann hypothesis."):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.8)
        self.play(FadeOut(card))

        # ---------------------------------------------------------------- hook: staircase
        ax = Axes(x_range=[0, 50, 10], y_range=[0, 16, 5], x_length=10.5, y_length=5.2, tips=False,
                  axis_config={"include_numbers": True, "font_size": 26, "color": GREY_B}).to_edge(DOWN, buff=0.7)
        stair = staircase(ax).set_color(BLUE_3B).set_stroke(width=4)
        pi_lab = MathTex(r"\pi(x)", color=BLUE_3B).next_to(ax.c2p(50, 15), UP + LEFT * 0.2)
        dots = VGroup(*[Dot(ax.c2p(p, 0), radius=0.045, color=YELLOW_3B) for p in PRIMES])
        plabs = VGroup(*[MathTex(str(p), font_size=26, color=YELLOW_3B).next_to(ax.c2p(p, 0), UP, buff=0.15)
                         for p in PRIMES[:5]])
        with self.say("Here is a staircase. It climbs one step at every prime number: "
                      "{p}two, three, five, seven, eleven, and so on. "
                      "{smooth}Gauss guessed that the staircase hugs a smooth curve, the logarithmic integral. "
                      "{err}And the question that has driven number theory for a century and a half is: "
                      "how far can the staircase stray from that curve?") as s:
            self.play(Create(ax), run_time=1.2)
            s.wait_until("p")
            self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.1),
                      Create(stair, rate_func=linear), FadeIn(pi_lab), run_time=s.until("smooth"))
            li = curve(ax, D["xs"], D["li"], color=WHITE, stroke_width=3)
            li_lab = MathTex(r"\operatorname{li}(x)=\int_0^x\frac{dt}{\ln t}", font_size=36).move_to(ax.c2p(13, 13))
            self.play(Create(li), Write(li_lab), run_time=2.5)
            s.wait_until("err")
            gap = VGroup(*[Line(ax.c2p(x, D["li"][i]), ax.c2p(x, sum(p <= x for p in PRIMES)),
                                color=RED_3B, stroke_width=3)
                           for i, x in enumerate(D["xs"]) if i % 60 == 30])
            q = Tex("How big is the gap?", color=RED_3B).move_to(ax.c2p(33, 4))
            self.play(LaggedStart(*[Create(g) for g in gap], lag_ratio=0.08), Write(q), run_time=2.5)
        self.play(FadeOut(VGroup(ax, stair, pi_lab, dots, li, li_lab, gap, q)))

        # ---------------------------------------------------------------- zeta & the strip
        zeta = MathTex(r"\zeta(s)", r"=", r"\sum_{n=1}^{\infty}\frac{1}{n^{s}}", font_size=56).to_edge(UP, buff=0.4)
        with self.say("In 1859, Riemann showed that the answer is written in the zeros of a single function: "
                      "the zeta function, the sum of one over n to the s. "
                      "{plane}Feed it a complex number s, and it extends to almost the whole complex plane. "
                      "{strip}All of its interesting zeros live in a narrow vertical strip, "
                      "between real part zero and real part one. "
                      "{line}Riemann conjectured that every one of them sits exactly on the line with real part one half. "
                      "{rh}That is the Riemann hypothesis, and it is still open.") as s:
            self.play(Write(zeta), run_time=2)
            s.wait_until("plane")
            self.play(zeta.animate.scale(0.75).to_corner(UL), run_time=1)
            cp = Axes(x_range=[-0.5, 1.5, 0.5], y_range=[0, 62, 10], x_length=6.5, y_length=6.6, tips=False,
                      axis_config={"color": GREY_B, "font_size": 24}).shift(DOWN * 0.35)
            cp.x_axis.add_numbers([0, 0.5, 1], num_decimal_places=1, font_size=24)
            cp.y_axis.add_numbers([10, 20, 30, 40, 50, 60], font_size=22)
            re_lab = MathTex(r"\operatorname{Re}(s)", font_size=28).next_to(cp.x_axis, RIGHT, buff=0.15)
            im_lab = MathTex(r"\operatorname{Im}(s)", font_size=28).next_to(cp.y_axis, UP, buff=0.1)
            self.play(Create(cp), FadeIn(re_lab, im_lab), run_time=1.5)
            s.wait_until("strip")
            strip = Polygon(cp.c2p(0, 0), cp.c2p(1, 0), cp.c2p(1, 62), cp.c2p(0, 62),
                            stroke_width=0, fill_color=BLUE_3B, fill_opacity=0.18)
            strip_lab = Tex("critical strip", font_size=30, color=BLUE_3B).next_to(cp.c2p(1, 55), RIGHT, buff=0.3)
            self.play(FadeIn(strip), Write(strip_lab))
            s.wait_until("line")
            zs = [g for g in D["gam"] if g < 62]
            zdots = VGroup(*[Dot(cp.c2p(0.5, g), radius=0.06, color=YELLOW_3B) for g in zs])
            half = DashedLine(cp.c2p(0.5, 0), cp.c2p(0.5, 62), color=YELLOW_3B, stroke_width=2)
            self.play(Create(half), LaggedStart(*[FadeIn(d, scale=3) for d in zdots], lag_ratio=0.15), run_time=3)
            s.wait_until("rh")
            rh = Tex(r"Riemann hypothesis:\\ every zero has $\operatorname{Re}=\tfrac12$",
                     font_size=32, color=YELLOW_3B).next_to(cp.c2p(1.5, 30), RIGHT, buff=0.1).shift(LEFT * 0.4)
            self.play(Write(rh))
        plane = VGroup(cp, re_lab, im_lab, strip, strip_lab, half, zdots)
        self.play(FadeOut(rh), FadeOut(zeta), plane.animate.scale(0.55).to_edge(LEFT, buff=0.3))

        # ---------------------------------------------------------------- waves
        ax2 = Axes(x_range=[0, 50, 10], y_range=[0, 16, 5], x_length=8.2, y_length=5, tips=False,
                   axis_config={"include_numbers": True, "font_size": 22, "color": GREY_B}).to_edge(RIGHT, buff=0.4)
        st2 = staircase(ax2).set_color(BLUE_3B).set_stroke(width=3, opacity=0.6)
        smooth = explicit(ax2, 0)
        nlab = Tex("smooth part only", font_size=30, color=YELLOW_3B).next_to(ax2, UP, buff=0.2)
        with self.say("Why should zeros control primes? "
                      "{w}Each zero contributes a wave to the prime count. "
                      "{sum}Start from the smooth curve, add the waves from more and more zeros, "
                      "and the staircase reappears, step for step.") as s:
            self.play(Create(ax2), Create(st2), run_time=1.5)
            s.wait_until("w")
            self.play(Create(smooth), FadeIn(nlab), Indicate(zdots[0], scale_factor=2.5), run_time=2)
            s.wait_until("sum")
            for n in [1, 3, 10, 30, 100]:
                lab = Tex(f"smooth part $+$ {n} zero{'s' if n > 1 else ''}", font_size=30,
                          color=YELLOW_3B).move_to(nlab)
                self.play(Transform(smooth, explicit(ax2, n)), Transform(nlab, lab), run_time=1.3)
                self.wait(0.15)
        self.play(FadeOut(VGroup(ax2, st2, smooth, nlab)))

        # wave size vs real part
        ax3 = Axes(x_range=[1, 100, 20], y_range=[-60, 60, 30], x_length=8, y_length=4.6, tips=False,
                   axis_config={"color": GREY_B}).to_edge(RIGHT, buff=0.5)
        g1 = D["gam"][0]
        w_half = ax3.plot(lambda x: x**0.5 * np.cos(g1 * np.log(x)), x_range=[1, 100, 0.05], color=BLUE_3B)
        w_far = ax3.plot(lambda x: x**0.88 * np.cos(g1 * np.log(x)), x_range=[1, 100, 0.05], color=RED_3B)
        env_h = VGroup(ax3.plot(lambda x: x**0.5, x_range=[1, 100], color=BLUE_3B, stroke_width=2),
                       ax3.plot(lambda x: -x**0.5, x_range=[1, 100], color=BLUE_3B, stroke_width=2))
        env_f = VGroup(ax3.plot(lambda x: x**0.88, x_range=[1, 100], color=RED_3B, stroke_width=2),
                       ax3.plot(lambda x: -x**0.88, x_range=[1, 100], color=RED_3B, stroke_width=2))
        for e in [*env_h, *env_f]:
            e.set_stroke(opacity=0.6)
        lab_h = MathTex(r"\operatorname{Re}\rho=\tfrac12:\ \text{height}\sim x^{1/2}", font_size=30,
                        color=BLUE_3B).next_to(ax3, UP, buff=0.15).align_to(ax3, LEFT)
        lab_f = MathTex(r"\operatorname{Re}\rho=\beta:\ \text{height}\sim x^{\beta}", font_size=30,
                        color=RED_3B).next_to(lab_h, RIGHT, buff=0.5)
        with self.say("And the size of each wave is set by where its zero sits. "
                      "{h}A zero with real part one half makes a wave whose height grows like the square root of x. "
                      "{f}A zero further right, at real part beta, makes a wave growing like x to the beta. "
                      "{c}So zeros near the right edge of the strip mean big errors in the prime count.") as s:
            self.play(Create(ax3))
            s.wait_until("h")
            self.play(Create(w_half), Create(env_h), Write(lab_h), run_time=2)
            s.wait_until("f")
            self.play(Create(w_far), Create(env_f), Write(lab_f), run_time=2.5)
            s.wait_until("c")
            self.play(Indicate(lab_f, color=RED_3B))
        self.play(FadeOut(VGroup(ax3, w_half, w_far, env_h, env_f, lab_h, lab_f)),
                  plane.animate.scale(1 / 0.55).move_to(ORIGIN).shift(LEFT * 3.0 + DOWN * 0.35))

        # ---------------------------------------------------------------- zero-free regions
        def zfr(c, color, top=62):
            ts = np.linspace(0, top, 120)
            left = [cp.c2p(1 - c / np.log(max(t, 3) + 2), t) for t in ts]
            return Polygon(*left, cp.c2p(1, top), cp.c2p(1, 0), stroke_width=0, fill_color=color, fill_opacity=0.55)

        one_line = Line(cp.c2p(1, 0), cp.c2p(1, 62), color=GREEN_3B, stroke_width=5)
        with self.say("So where are the zeros, really? "
                      "{pnt}In 1896, Hadamard and de la Vallée [Poussin](/pusˈæn/) proved there are none on the line "
                      "with real part one. That fact is the prime number theorem. "
                      "{reg}Later work carved out a zero-free region a little to the left, "
                      "but it is a region that thins out: the higher you go, the closer it hugs the line. "
                      "{up}Nobody could rule out zeros creeping arbitrarily close to one, far up the strip.") as s:
            s.wait_until("pnt")
            l1 = Tex("1896: no zeros on $\\operatorname{Re}(s)=1$", font_size=30, color=GREEN_3B)
            l1.next_to(cp.c2p(1.5, 50), RIGHT, buff=0.1).shift(LEFT * 0.3)
            self.play(Create(one_line), Write(l1), run_time=2)
            s.wait_until("reg")
            region = zfr(0.45, GREEN_3B)
            l2 = Tex(r"zero-free region\\ (schematic)", font_size=28, color=GREEN_3B).next_to(l1, DOWN, buff=0.5,
                                                                                            aligned_edge=LEFT)
            self.play(FadeIn(region), Write(l2), run_time=2)
            s.wait_until("up")
            ghost = VGroup(*[Dot(cp.c2p(1 - 0.45 / np.log(t + 2) - 0.035, t), radius=0.06, color=RED_3B)
                             for t in [40, 52, 61]])
            qs = VGroup(*[MathTex("?", color=RED_3B, font_size=30).next_to(d, LEFT, buff=0.08) for d in ghost])
            self.play(LaggedStart(*[FadeIn(g, scale=2) for g in ghost], lag_ratio=0.3), FadeIn(qs), run_time=2)

        with self.say("The quasi-Riemann hypothesis asks for something much weaker than Riemann, "
                      "but still out of reach. {wall}A single vertical wall, at some fixed number less than one, "
                      "with no zeros at all to its right, at any height.") as s:
            s.wait_until("wall")
            wall_q = DashedLine(cp.c2p(0.8, 0), cp.c2p(0.8, 62), color=WHITE)
            wq = MathTex(r"\sigma_0<1\,?", font_size=34).next_to(cp.c2p(0.8, 62), UP, buff=0.1)
            self.play(Create(wall_q), Write(wq), run_time=2)
        self.play(FadeOut(VGroup(ghost, qs, l1, l2, region)))

        # ---------------------------------------------------------------- the result
        thm = VGroup(
            Tex(r"\textbf{Theorem.} Every Dirichlet", font_size=34),
            Tex(r"$L$-function, including $\zeta(s)$,", font_size=34),
            Tex(r"has no zeros with $\operatorname{Re}(s)>\tfrac78$.", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        thm_box = VGroup(thm, caption_box(thm, YELLOW_3B)).to_edge(RIGHT, buff=0.4).shift(UP * 1.2)
        wall = Polygon(cp.c2p(7 / 8, 0), cp.c2p(1.5, 0), cp.c2p(1.5, 62), cp.c2p(7 / 8, 62),
                       stroke_width=0, fill_color=YELLOW_3B, fill_opacity=0.35)
        wline = Line(cp.c2p(7 / 8, 0), cp.c2p(7 / 8, 62), color=YELLOW_3B, stroke_width=5)
        w78 = MathTex(r"\tfrac78", font_size=40, color=YELLOW_3B).move_to(wq)
        arrow_up = Arrow(cp.c2p(1.15, 40), cp.c2p(1.15, 62) + UP * 0.6, color=YELLOW_3B, buff=0)
        forever = Tex(r"at every\\height", font_size=28, color=YELLOW_3B).next_to(arrow_up, RIGHT, buff=0.1)
        with self.say("A new manuscript in OpenAI's math catalogue claims exactly that wall, at seven eighths. "
                      "{thm}Every Dirichlet L-function, including zeta itself, has no zeros with real part "
                      "greater than seven eighths. "
                      "{all}Not just near the bottom of the strip. At every height, forever.") as s:
            self.play(Transform(wall_q, wline), Transform(wq, w78), FadeIn(wall), FadeOut(strip_lab), run_time=2)
            s.wait_until("thm")
            self.play(Write(thm_box), run_time=3)
            s.wait_until("all")
            self.play(GrowArrow(arrow_up), FadeIn(forever))
        self.play(FadeOut(VGroup(cp, re_lab, im_lab, strip, half, zdots, one_line, wall, wall_q, wq, arrow_up, forever)),
                  thm_box.animate.to_edge(UP, buff=0.3).set_x(0))

        # ---------------------------------------------------------------- consequences
        c1 = MathTex(r"\bigl|\,\pi(x)-\operatorname{li}(x)\,\bigr|", r"\;\le\;", r"C_\varepsilon\,x^{7/8+\varepsilon}",
                     font_size=48)
        c1[2].set_color(YELLOW_3B)
        c1_note = Tex("first power-saving error term in the prime number theorem", font_size=30, color=GREY_A)
        g1 = VGroup(c1, c1_note).arrange(DOWN, buff=0.25).shift(UP * 0.9)
        c2 = MathTex(r"n(p)", r"\le", r"C\,(\log p)^{A}", font_size=44)
        c2_note = Tex(r"$n(p)$ = least non-square modulo the prime $p$", font_size=28, color=GREY_A)
        c3 = Tex(r"$\Rightarrow$ square roots mod $p$ in deterministic polynomial time", font_size=32,
                 color=TEAL_3B)
        g2 = VGroup(c2, c2_note, c3).arrange(DOWN, buff=0.22).shift(DOWN * 1.9)
        with self.say("Plug this into the wave picture, and every wave is capped at x to the seven eighths. "
                      "{e}That gives the first error term in the prime number theorem that saves a genuine power of x. "
                      "{np}There are algorithmic payoffs too. For every prime p, the smallest number that is not a "
                      "perfect square modulo p is at most a fixed power of log p. "
                      "{alg}So square roots modulo a prime can be computed deterministically, in polynomial time. "
                      "Before, that was only known by assuming the generalized Riemann hypothesis.") as s:
            self.play(Write(c1), run_time=2)
            s.wait_until("e")
            self.play(FadeIn(c1_note, shift=UP * 0.2))
            s.wait_until("np")
            self.play(Write(c2), FadeIn(c2_note), run_time=2)
            s.wait_until("alg")
            self.play(FadeIn(c3, shift=UP * 0.2))
        self.play(FadeOut(VGroup(thm_box, g1, g2)))

        # ---------------------------------------------------------------- proof idea 1: fingerprint
        head = Tex("The idea: proof by contradiction", font_size=44, color=YELLOW_3B).to_edge(UP, buff=0.35)
        ax4 = Axes(x_range=[0, 10, 2], y_range=[0, 8, 2], x_length=6.2, y_length=4.4, tips=True,
                   axis_config={"color": GREY_B}).to_corner(DL, buff=0.6).shift(UP * 0.2)
        xl = MathTex(r"\log Z", font_size=30).next_to(ax4.x_axis, DOWN, buff=0.15).align_to(ax4.x_axis, RIGHT)
        yl = MathTex(r"\log|\text{signal}|", font_size=30).next_to(ax4.y_axis, UP, buff=0.1)
        sup = VGroup(
            Tex(r"Suppose some zero has $\operatorname{Re}\rho=\beta>\tfrac78$", font_size=32),
            MathTex(r"\Rightarrow\ \frac{1}{L(s)}\ \text{has a pole at}\ \rho", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5).shift(UP * 1.4)
        sig = MathTex(r"\text{signal}(Z)=\frac{1}{2\pi i}\int Z^{\,s+c}\,\frac{H(s)}{L(s)}\,e^{(s-5/6)^2}\,ds",
                      font_size=30).next_to(sup, DOWN, buff=0.45).align_to(sup, LEFT)
        with self.say("How does the proof work? By contradiction. "
                      "{sup}Suppose some L-function had a zero to the right of seven eighths, "
                      "and take the rightmost one, at real part beta. "
                      "{pole}Then one over L has a pole there. "
                      "{sig}Now package one over L into a signal: an integral that depends on a large scale Z. "
                      "{fp}A pole leaves a fingerprint. The signal must grow like a power of Z, "
                      "with the exponent set by beta. On a log-log plot, that is a line of a definite slope. "
                      "{slow}If you can show the signal grows even slightly slower, the pole cannot exist, "
                      "and neither can the zero.") as s:
            self.play(Write(head))
            s.wait_until("sup")
            self.play(Write(sup[0]), run_time=2)
            s.wait_until("pole")
            self.play(Write(sup[1]))
            s.wait_until("sig")
            self.play(Write(sig), run_time=2.5)
            s.wait_until("fp")
            self.play(Create(ax4), FadeIn(xl, yl))
            forced = DashedLine(ax4.c2p(0, 0.3), ax4.c2p(10, 7.6), color=RED_3B)
            fl = Tex(r"forced by a zero at $\beta$", font_size=28, color=RED_3B).next_to(ax4.c2p(5.3, 7.4), LEFT)
            self.play(Create(forced), FadeIn(fl), run_time=2)
            s.wait_until("slow")
            xs = np.linspace(0, 10, 200)
            proven = VMobject(color=GREEN_3B, stroke_width=4).set_points_smoothly(
                [ax4.c2p(x, 0.3 + 0.52 * x + 0.25 * np.sin(2.3 * x)) for x in xs])
            pl = Tex("what the proof shows", font_size=28, color=GREEN_3B).next_to(ax4.c2p(10, 5.2), UP, buff=0.1)
            self.play(Create(proven), FadeIn(pl), run_time=2)
            cross = Cross(sup[1], stroke_color=RED_3B, stroke_width=5)
            self.play(Create(cross))
        self.play(FadeOut(VGroup(ax4, xl, yl, forced, fl, proven, pl, sup, sig, cross)))

        # ---------------------------------------------------------------- proof idea 2: the arena + two computations
        w = np.exp(2j * np.pi / 3)
        lattice, primes_e = VGroup(), VGroup()

        def is_p(n):
            return n > 1 and all(n % d for d in range(2, int(n**0.5) + 1))

        for a in range(-40, 41):
            for b in range(-40, 41):
                z = a + b * w
                if abs(z) > 10.2:
                    continue
                pos = np.array([z.real * 0.3, z.imag * 0.3 - 0.55, 0])
                nrm = a * a - a * b + b * b
                eis = is_p(nrm) or (int(round(nrm**0.5)) ** 2 == nrm and is_p(int(round(nrm**0.5)))
                                    and int(round(nrm**0.5)) % 3 == 2 and (a == 0 or b == 0 or a == b))
                d = Dot(pos, radius=0.03 if not eis else 0.045, color=GREY_D if not eis else BLUE_3B)
                (primes_e if eis else lattice).add(d)
        arena_lab = Tex(r"Eisenstein integers $a+b\omega$, $\ \omega=e^{2\pi i/3}$ \quad(primes in blue)",
                        font_size=30).next_to(head, DOWN, buff=0.25)
        with self.say("The hard part is getting a handle on that signal. "
                      "{ar}The proof moves to the Eisenstein integers: a triangular lattice of complex numbers, "
                      "home to cubic and sextic characters. "
                      "{tw}Working with a whole family of twisted L-functions there, not just zeta, "
                      "turns out to be essential.") as s:
            self.play(Transform(head, Tex("Where the proof lives", font_size=44, color=YELLOW_3B).move_to(head)))
            s.wait_until("ar")
            self.play(FadeIn(lattice), FadeIn(arena_lab), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(d, scale=2.5) for d in primes_e], lag_ratio=0.004), run_time=2.5)
        self.play(FadeOut(VGroup(lattice, primes_e, arena_lab)))

        center = VGroup(MathTex(r"J(Z)", font_size=52),
                        Tex("one completed cubic-theta sum", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.12)
        center.next_to(head, DOWN, buff=0.45)
        cbox = caption_box(center, WHITE)
        left = VGroup(Tex(r"\textbf{Reflection}", font_size=32, color=BLUE_3B),
                      Tex(r"cubic theta reflection\\ $+$ large sieves", font_size=28),
                      MathTex(r"|J(Z)|\ \lesssim\ Z^{3/16+\omega}", font_size=36, color=BLUE_3B),
                      Tex("``the sum is small''", font_size=28, color=BLUE_3B)).arrange(DOWN, buff=0.22)
        right = VGroup(Tex(r"\textbf{Poisson summation}", font_size=32, color=ORANGE_3B),
                       MathTex(r"J(Z)=\underbrace{\text{signal}(Z)}_{\text{contains }1/L}\;+\;\text{rows}",
                               font_size=34),
                       Tex(r"rows: other $L$-functions,\\ tamed by a \emph{zero detector}\\ $+$ a sextic large sieve",
                           font_size=26, color=GREY_A)).arrange(DOWN, buff=0.22)
        left.move_to(LEFT * 3.6 + DOWN * 1.3)
        right.move_to(RIGHT * 3.3 + DOWN * 1.3)
        al = Arrow(cbox.get_bottom(), left.get_top(), color=BLUE_3B, buff=0.15)
        ar = Arrow(cbox.get_bottom(), right.get_top(), color=ORANGE_3B, buff=0.15)
        with self.say("There, the proof builds one sum, and computes it in two different exact ways. "
                      "{l}One way, using a reflection formula for cubic theta functions and large sieve "
                      "inequalities, shows that the sum is small. "
                      "{r}The other way, by Poisson summation, shows that the same sum equals the signal, "
                      "plus rows coming from other L-functions. "
                      "{det}A zero detector and a sextic large sieve show those rows are rare. "
                      "{fin}Put the two together, and the signal is too small to accommodate the zero.") as s:
            self.play(FadeIn(center), Create(cbox))
            s.wait_until("l")
            self.play(GrowArrow(al), FadeIn(left[:2]), run_time=1.5)
            self.play(Write(left[2:]), run_time=2)
            s.wait_until("r")
            self.play(GrowArrow(ar), FadeIn(right[:1]), Write(right[1]), run_time=2.5)
            s.wait_until("det")
            self.play(FadeIn(right[2]))
            s.wait_until("fin")
            self.play(Indicate(left[2], color=BLUE_3B), Indicate(right[1], color=ORANGE_3B), run_time=2)

        stages = VGroup(
            MathTex(r"\text{Pass 1: }\ \operatorname{Re}(s)>\tfrac{11}{12}", font_size=38),
            MathTex(r"\xrightarrow{\ \text{prime-by-prime compensation}\ }", font_size=38),
            MathTex(r"\text{Pass 2: }\ \operatorname{Re}(s)>\tfrac{7}{8}", font_size=38, color=YELLOW_3B),
        ).arrange(RIGHT, buff=0.3)
        if stages.width > 13:
            stages.scale_to_fit_width(13)
        self.play(FadeOut(VGroup(center, cbox, al, ar, left, right)))
        stages.arrange(DOWN, buff=0.35).move_to(UP * 0.4)
        with self.say("A first pass of this argument gives a wall at eleven twelfths. "
                      "{p2}A refined second pass, with prime-by-prime compensation and unbalanced scales, "
                      "pushes it to seven eighths. "
                      "{tr}A final factorization carries the wall from the Eisenstein world back to zeta "
                      "and every Dirichlet L-function.") as s:
            self.play(FadeIn(stages[0]))
            s.wait_until("p2")
            self.play(FadeIn(stages[1]), FadeIn(stages[2]), run_time=2)
            s.wait_until("tr")
            fact = MathTex(r"L_{\mathbb{Q}(\sqrt{-3})}(s,\chi\circ N)=L(s,\chi)\,L(s,\chi\chi_{-3})",
                           font_size=36, color=TEAL_3B).next_to(stages, DOWN, buff=0.6)
            self.play(Write(fact), run_time=2)
        self.play(FadeOut(Group(*self.mobjects)))

        # ---------------------------------------------------------------- closing
        card = status_card(
            [r"$\zeta(s)\neq0$ and $L(s,\chi)\neq0$ whenever $\operatorname{Re}(s)>7/8$",
             r"Riemann hypothesis ($\operatorname{Re}=\tfrac12$) remains open",
             r"Manuscript: 199 pages, produced by an OpenAI model"],
            True, r"\emph{The Quasi-Riemann Hypothesis: A Zero-Free Half-Plane} (Sept.\ 2026)")
        with self.say("Seven eighths is not one half, so the Riemann hypothesis itself remains open. "
                      "{c}But no fixed wall below one had ever been established before. "
                      "The manuscript runs to nearly two hundred pages, written by an OpenAI model, "
                      "{l}and its statement for the zeta function has been formalized in the Lean proof assistant, "
                      "using only the standard axioms.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
