from math import gamma

import numpy as np
from manim import *

from style import *
from vo import NarratedScene

SANT = "[Santaló](/sˌæntəlˈO/)"


def lp_area(p):
    if p > 400:
        return 4.0
    return 4 * gamma(1 + 1 / p) ** 2 / gamma(1 + 2 / p)


def lp_curve(ax, p, color, sx=1.0, n=240):
    e = 2 / p
    ts = np.linspace(0, TAU, n)
    pts = [ax.c2p(sx * np.sign(np.cos(t)) * abs(np.cos(t)) ** e, np.sign(np.sin(t)) * abs(np.sin(t)) ** e)
           for t in ts]
    return Polygon(*pts, color=color, stroke_width=4).set_fill(color, 0.15)


def wire(verts, edges, color, scale=1.0, shift=ORIGIN):
    R = np.array([[np.cos(0.6), 0, np.sin(0.6)], [0, 1, 0], [-np.sin(0.6), 0, np.cos(0.6)]])
    T = np.array([[1, 0, 0], [0, np.cos(0.35), -np.sin(0.35)], [0, np.sin(0.35), np.cos(0.35)]])
    P = [(T @ R @ np.array(v, float)) * scale for v in verts]
    pts = [np.array([p[0], p[1], 0]) + shift for p in P]
    return VGroup(*[Line(pts[a], pts[b], color=color, stroke_width=3) for a, b in edges])


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "087", "The Mahler Conjecture",
                          r"Convex bodies and their polars: $|K|\,|K^\circ|\ge 4^n/n!$")
        with self.say("The Mahler conjecture."):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ polar bodies
        ax = Axes(x_range=[-2.2, 2.2, 1], y_range=[-2.2, 2.2, 1], x_length=6.4, y_length=6.4, tips=False,
                  axis_config={"color": GREY_D}).shift(LEFT * 3.0 + DOWN * 0.3)
        s = ValueTracker(0.5)  # 1/p
        sx = ValueTracker(1.0)
        K = always_redraw(lambda: lp_curve(ax, 1 / s.get_value(), BLUE_3B, sx.get_value()))
        Kp = always_redraw(lambda: lp_curve(ax, 1 / (1 - s.get_value()), YELLOW_3B, 1 / sx.get_value()))
        defn = VGroup(MathTex(r"K", font_size=40, color=BLUE_3B), Tex(": a convex shape, symmetric about the center",
                                                                       font_size=30)).arrange(RIGHT, buff=0.15)
        defp = VGroup(MathTex(r"K^\circ", font_size=40, color=YELLOW_3B),
                      MathTex(r"=\{\,p:\ \langle q,p\rangle\le 1\ \text{for all } q\in K\,\}", font_size=34)
                      ).arrange(RIGHT, buff=0.15)
        side = VGroup(defn, defp).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_corner(UR, buff=0.5)

        def readout():
            p = 1 / s.get_value()
            q = 1 / (1 - s.get_value())
            a, b = lp_area(p), lp_area(q)
            g = VGroup(
                MathTex(rf"|K|={a:.3f}", font_size=36, color=BLUE_3B),
                MathTex(rf"|K^\circ|={b:.3f}", font_size=36, color=YELLOW_3B),
                MathTex(rf"|K|\cdot|K^\circ|={a * b:.3f}", font_size=42),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            return g.next_to(side, DOWN, buff=0.7).align_to(side, LEFT)

        ro = always_redraw(readout)
        with self.say("Take a convex shape K, symmetric about its center. {p}Its polar, K circle, is the set of "
                      "directions p whose dot product with every point of K is at most one. "
                      "{d}A round disk is its own polar. {sq}Squash the disk toward a diamond, and the polar swells "
                      "toward a square, and vice versa. {st}Stretch K one way, and its polar shrinks the same way. "
                      "{prod}Now multiply their areas. Stretching cannot change this product, but the shape can.") as sc:
            self.play(Create(ax), FadeIn(defn))
            self.add(K)
            self.play(FadeIn(K))
            sc.wait_until("p")
            self.add(Kp)
            self.play(FadeIn(Kp), FadeIn(defp))
            sc.wait_until("sq")
            self.play(s.animate.set_value(0.97), run_time=2.5)
            self.play(s.animate.set_value(0.03), run_time=3)
            self.play(s.animate.set_value(0.5), run_time=1.5)
            sc.wait_until("st")
            self.play(sx.animate.set_value(1.6), run_time=1.5)
            self.play(sx.animate.set_value(1.0), run_time=1.0)
            sc.wait_until("prod")
            self.add(ro)
            self.play(FadeIn(ro))
            self.play(sx.animate.set_value(1.5), run_time=1.5)
            self.play(sx.animate.set_value(1.0), run_time=1.0)

        with self.say("For the disk, the product is pi squared, about nine point eight seven. "
                      "{m}Morph toward the diamond and its square polar, and the product drops, bottoming out "
                      "at exactly eight. {b}The round disk is the maximum, a classical theorem of Blaschke and "
                      f"{SANT}. {{min}}The square and the diamond are the minimum.") as sc:
            sc.wait_until("m")
            self.play(s.animate.set_value(0.985), run_time=3.5)
            self.play(s.animate.set_value(0.5), run_time=2)
            sc.wait_until("min")
            self.play(s.animate.set_value(0.015), run_time=2.5)
        self.remove(K, Kp, ro)
        self.play(FadeOut(VGroup(ax, side)), FadeOut(lp_curve(ax, 1 / 0.015, BLUE_3B)),
                  FadeOut(lp_curve(ax, 1 / 0.985, YELLOW_3B)))

        # ------------------------------------------------------------ the conjecture
        conj = VGroup(
            Tex(r"\textbf{Mahler's conjecture} (1939)", font_size=40, color=YELLOW_3B),
            MathTex(r"|K|\,|K^\circ|\ \ge\ \frac{4^n}{n!}", r"\quad\text{for every symmetric convex }K\subset\mathbb{R}^n",
                    font_size=40),
            Tex(r"with equality for the cube and the cross-polytope", font_size=32, color=GREY_A),
        ).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.4)
        cube_v = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
        cube_e = [(a, b) for a in range(8) for b in range(a + 1, 8)
                  if sum(u != v for u, v in zip(cube_v[a], cube_v[b])) == 1]
        oct_v = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        oct_e = [(a, b) for a in range(6) for b in range(a + 1, 6) if a // 2 != b // 2]
        pri_v = [(x, y, z) for z in (-1, 1) for (x, y) in [(1, 0), (0, 1), (-1, 0), (0, -1)]]
        pri_e = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
        shapes = VGroup(wire(cube_v, cube_e, BLUE_3B, 0.8), wire(oct_v, oct_e, YELLOW_3B, 1.15),
                        wire(pri_v, pri_e, TEAL_3B, 0.95)).arrange(RIGHT, buff=1.5).shift(DOWN * 1.3)
        slabs = VGroup(Tex("cube", font_size=28), Tex("cross-polytope", font_size=28),
                       Tex(r"diamond $\times$ segment", font_size=28))
        for l, sh in zip(slabs, shapes):
            l.next_to(sh, DOWN, buff=0.3)
        hann = Tex(r"\emph{Hanner polytopes}: all tie at $4^3/3!$", font_size=30, color=TEAL_3B).to_edge(DOWN,
                                                                                                         buff=0.3)
        known = VGroup(
            Tex(r"known: $n=2$ (Mahler), $n=3$ (Iriyeh--Shibata, 2020),", font_size=30),
            Tex(r"special classes; asymptotically up to $c^n$ (Bourgain--Milman)", font_size=30),
        ).arrange(DOWN, buff=0.15)
        with self.say("In 1939, Kurt Mahler conjectured that in every dimension n, this product is at least four to the n "
                      "over n factorial, the value for the cube and its polar, the cross-polytope. "
                      "{h}In three dimensions there are other ties too, like a diamond times a segment: the family of "
                      "Hanner polytopes. {k}Mahler proved the plane case himself. Dimension three took until 2020. "
                      "In general, Bourgain and Milman showed the bound holds up to a factor exponential in n. "
                      "But the exact conjecture, in all dimensions, stayed open for eighty-seven years.") as sc:
            self.play(FadeIn(conj[0]), Write(conj[1]), run_time=2.5)
            self.play(FadeIn(conj[2]), Create(shapes[0]), Create(shapes[1]), FadeIn(slabs[:2]), run_time=2)
            sc.wait_until("h")
            self.play(Create(shapes[2]), FadeIn(slabs[2]), FadeIn(hann))
            sc.wait_until("k")
            self.play(FadeOut(VGroup(shapes, slabs, hann)))
            self.play(FadeIn(known))
        self.play(FadeOut(VGroup(conj, known)))

        thm = VGroup(Tex(r"\textbf{Theorem.} For every origin-symmetric convex body $K\subset\mathbb{R}^n$,",
                         font_size=36),
                     MathTex(r"|K|\,|K^\circ|\ \ge\ \frac{4^n}{n!},", font_size=46),
                     Tex(r"with equality exactly for linear images of Hanner polytopes.", font_size=34),
                     Tex(r"Companion: for general convex bodies, simplices are the minimizers.", font_size=30,
                         color=GREY_A)).arrange(DOWN, buff=0.3)
        tb = VGroup(thm[:3], caption_box(thm[:3], YELLOW_3B, 0.3))
        with self.say("Manuscripts in OpenAI's math catalogue claim to settle it completely. {t}For every symmetric "
                      "convex body, in every dimension, the product is at least four to the n over n factorial, "
                      "with equality exactly for the Hanner polytopes. {g}A companion paper settles the "
                      "non-symmetric version too, where simplices are the minimizers.") as sc:
            sc.wait_until("t")
            self.play(Write(thm[:3]), Create(tb[1]), run_time=3)
            sc.wait_until("g")
            thm[3].next_to(tb, DOWN, buff=0.35)
            self.play(FadeIn(thm[3]))
        self.play(FadeOut(VGroup(tb, thm[3])))

        # ------------------------------------------------------------ symplectic route
        hdr = Tex("The surprising route: physics", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.35)
        axq = Axes(x_range=[-1.6, 1.6, 1], y_range=[-1.6, 1.6, 1], x_length=3.4, y_length=3.4, tips=False,
                   axis_config={"color": GREY_D}).shift(LEFT * 4.2 + UP * 0.2)
        axp = Axes(x_range=[-1.6, 1.6, 1], y_range=[-1.6, 1.6, 1], x_length=3.4, y_length=3.4, tips=False,
                   axis_config={"color": GREY_D}).shift(LEFT * 0.2 + UP * 0.2)
        Kq = lp_curve(axq, 60, BLUE_3B)
        Kpp = lp_curve(axp, 1.02, YELLOW_3B)
        lq = Tex(r"positions $q\in K$", font_size=30, color=BLUE_3B).next_to(axq, DOWN, buff=0.2)
        lp = Tex(r"momenta $p\in K^\circ$", font_size=30, color=YELLOW_3B).next_to(axp, DOWN, buff=0.2)
        times = MathTex(r"\times", font_size=50).move_to((axq.get_center() + axp.get_center()) / 2)
        ps = Tex(r"phase space region\\ $K\times K^\circ\subset\mathbb{R}^{2n}$", font_size=32).next_to(axp, RIGHT,
                                                                                                      buff=0.6)
        vol = MathTex(r"\mathrm{vol}(K\times K^\circ)=|K|\,|K^\circ|", font_size=38).to_edge(DOWN, buff=1.3)
        with self.say("The proof takes a detour through physics. {ph}Think of K as the allowed positions of a "
                      "particle, and the polar K circle as its allowed momenta. Together they form a region of "
                      "phase space, K times K circle, {v}whose volume is exactly the product we care about.") as sc:
            self.play(Write(hdr))
            sc.wait_until("ph")
            self.play(Create(axq), Create(Kq), FadeIn(lq), run_time=1.5)
            self.play(FadeIn(times), Create(axp), Create(Kpp), FadeIn(lp), run_time=1.5)
            self.play(FadeIn(ps))
            sc.wait_until("v")
            self.play(Write(vol))
        self.play(FadeOut(VGroup(axq, axp, Kq, Kpp, lq, lp, times, ps)), vol.animate.to_edge(UP, buff=1.1))

        # nonsqueezing and ball capacity
        ball = Circle(radius=1.3, color=TEAL_3B, fill_opacity=0.25).shift(LEFT * 4 + DOWN * 0.6)
        bl = Tex(r"symplectic ball\\ of capacity $c$", font_size=28, color=TEAL_3B).next_to(ball, DOWN, buff=0.2)
        cyl = VGroup(Line(LEFT * 1.2 + UP * 0.8, RIGHT * 1.6 + UP * 0.8), Line(LEFT * 1.2 + DOWN * 0.8,
                                                                                  RIGHT * 1.6 + DOWN * 0.8)).shift(
            RIGHT * 0.2 + DOWN * 0.6).set_color(GREY_A)
        nsq = Tex(r"Gromov: a ball can't be squeezed\\ into a thinner cylinder, even with room to spare",
                  font_size=28).next_to(cyl, DOWN, buff=0.75)
        xx = Cross(scale_factor=0.3, stroke_color=RED_3B).move_to(cyl.get_center())
        chain = VGroup(
            Tex(r"Symplectic maps preserve volume. So if a ball of capacity $c$ fits inside $K\times K^\circ$:",
                font_size=30),
            MathTex(r"|K|\,|K^\circ|\ \ge\ \mathrm{vol}\,B^{2n}(c)=\frac{c^n}{n!}", font_size=42, color=TEAL_3B),
            MathTex(r"c\to 4\quad\Longrightarrow\quad |K|\,|K^\circ|\ \ge\ \frac{4^n}{n!}", font_size=42,
                    color=YELLOW_3B),
        ).arrange(DOWN, buff=0.35).to_edge(DOWN, buff=0.4)
        with self.say("Phase space has a hidden rigidity. The maps of classical mechanics, called symplectic maps, "
                      "preserve volume, but they also obey Gromov's nonsqueezing theorem: {g}you cannot push a ball "
                      "through a thinner cylinder, even if the volume would fit. A ball is measured by its capacity. "
                      "{fit}Now the key move. If a symplectic ball of capacity c fits inside K times K circle, "
                      "its volume, c to the n over n factorial, is a lower bound for the product. "
                      "{four}So Mahler's conjecture would follow if balls of every capacity below four fit inside. "
                      "Artstein-Avidan, Karasev, and Ostrover pointed out this connection in 2014.") as sc:
            self.play(FadeIn(ball), FadeIn(bl))
            sc.wait_until("g")
            self.play(Create(cyl), FadeIn(nsq))
            self.play(ball.animate.shift(RIGHT * 2.2), run_time=1.5)
            self.play(Create(xx), ball.animate.shift(LEFT * 2.2), run_time=1)
            sc.wait_until("fit")
            self.play(FadeOut(VGroup(ball, bl, cyl, nsq, xx)))
            self.play(FadeIn(chain[0]), Write(chain[1]), run_time=2.5)
            sc.wait_until("four")
            self.play(Write(chain[2]), run_time=2)
        self.play(FadeOut(VGroup(vol, chain, hdr)))

        hdr2 = Tex(r"The new theorem: balls of every capacity $c<4$ fit", font_size=40, color=YELLOW_3B).to_edge(
            UP, buff=0.35)
        how = VGroup(
            Tex(r"\textbf{1.} A holomorphic map vanishing to order $k$ at a point", font_size=32),
            Tex(r"\quad hides a symplectic ball of capacity almost $\pi k$", font_size=32),
            Tex(r"\textbf{2.} A conformal map of the disk onto a lens shape, raised to the $k$-th power,", font_size=32),
            Tex(r"\quad builds such a map inside $K\times K^\circ$, with momenta scaled by about $\pi k/4$",
                font_size=32),
            MathTex(r"\frac{\pi k}{\pi k/4}=4", font_size=46, color=TEAL_3B),
            Tex(r"Gromov width of $K\times K^\circ$ is exactly 4, for every symmetric $K$", font_size=34,
                color=YELLOW_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(hdr2, DOWN, buff=0.45)
        how[4].set_x(0)
        how[5].set_x(0)
        with self.say("That is exactly what the new paper proves. {h1}Its construction starts from a principle in "
                      "complex geometry: a holomorphic map that vanishes to order k at a point hides a symplectic ball "
                      "of capacity almost pi k. {h2}Then it builds such a map out of a conformal map from the disk to a "
                      "lens-shaped region, raised to the k-th power, and fits the result inside K times K circle, "
                      "with momenta scaled by about pi k over four. {r}The ratio tends to four. "
                      "{w}So balls of every capacity below four fit, for every symmetric body, and Mahler's conjecture "
                      "follows.") as sc:
            self.play(Write(hdr2))
            sc.wait_until("h1")
            self.play(FadeIn(how[0:2]))
            sc.wait_until("h2")
            self.play(FadeIn(how[2:4]))
            sc.wait_until("r")
            self.play(Write(how[4]))
            sc.wait_until("w")
            self.play(FadeIn(how[5]))
        self.play(FadeOut(VGroup(hdr2, how)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Symmetric Mahler: $|K||K^\circ|\ge 4^n/n!$, equality exactly for Hanner polytopes",
             r"General Mahler: simplices minimize; and $K\times K^\circ$ has Gromov width $4$",
             r"Manuscripts produced by an OpenAI model"],
            True, r"\emph{The symmetric Mahler conjecture and its equality cases} (Sept.\ 2026)")
        with self.say("All three statements, the symmetric conjecture with its equality cases, the general version, "
                      "and the symplectic width theorem, have been formalized in the Lean proof assistant. "
                      "{c}The manuscripts were written by an OpenAI model. An eighty-seven-year-old question about "
                      "shapes, answered with the geometry of classical mechanics.") as sc:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            sc.wait_until("c")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
