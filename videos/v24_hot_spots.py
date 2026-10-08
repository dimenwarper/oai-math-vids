from pathlib import Path

import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(Path(__file__).parent / "data" / "v24.npz")
NEU = "[Neumann](/nˈYmən/)"
BUR = "[Burdzy](/bˈʊɹʤi/)"
ROH = "[Rohleder](/ɹˈOlAdəɹ/)"
NAD = "[Nadirashvili](/nɑdiɹɑʃvˈili/)"
RAUCH = "[Rauch](/ɹˈWʧ/)"

STOPS = np.array([[30, 60, 140], [88, 196, 221], [240, 240, 240], [255, 180, 80], [252, 98, 85]]) / 255.0
EXT = D["extent"]  # x0, x1, y0, y1 of the grid
MASK = D["mask"]
NY, NX = MASK.shape
HX = (EXT[1] - EXT[0]) / (NX - 1)


def colorize(F):
    m = ~np.isnan(F)
    v = np.zeros_like(F)
    lo, hi = np.nanmin(F), np.nanmax(F)
    v[m] = (F[m] - lo) / (hi - lo)
    x = v * 4
    i = np.clip(x.astype(int), 0, 3)
    f = (x - i)[..., None]
    rgb = STOPS[i] * (1 - f) + STOPS[i + 1] * f
    rgba = np.concatenate([rgb, m[..., None].astype(float)], -1)
    return (rgba[::-1] * 255).astype(np.uint8)


class Field:
    """Maps grid coordinates to the screen: scale k, centre c."""

    def __init__(self, k, c):
        self.k, self.c = k, np.array([c[0], c[1], 0.0], dtype=float)

    def p(self, x, y):
        return self.c + self.k * np.array([x, y, 0.0])

    def image(self, F):
        im = ImageMobject(colorize(F))
        im.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        im.stretch_to_fit_width(self.k * HX * NX)
        im.stretch_to_fit_height(self.k * HX * NY)
        im.move_to(self.p((EXT[0] + EXT[1]) / 2, (EXT[2] + EXT[3]) / 2))
        return im

    def boundary(self, color=WHITE, width=3):
        b = D["boundary"]
        return VMobject(color=color, stroke_width=width).set_points_as_corners([self.p(x, y) for x, y in b])


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "369", r"The Hot Spots Conjecture",
                          r"Smooth simply connected planar domains: no interior critical points")
        with self.say("After a long time, where is the hottest point of an insulated plate?"):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ heat flow on an actual domain
        G = Field(1.85, [-1.6, -0.35])
        frames, times = D["frames"], D["times"]
        hot, cold = D["hot"], D["cold"]
        kt = ValueTracker(0)

        def fidx():
            return int(round(kt.get_value() * (len(frames) - 1)))

        img = G.image(frames[0])

        def upd_img(m):
            m.become(G.image(frames[fidx()]))

        bnd = G.boundary()
        hd = always_redraw(lambda: Dot(G.p(*hot[fidx()]), radius=0.11, color=YELLOW_3B).set_stroke(BLACK, 2))
        cd = always_redraw(lambda: Dot(G.p(*cold[fidx()]), radius=0.11, color=BLUE_E).set_stroke(WHITE, 2))
        path = always_redraw(lambda: VMobject(color=YELLOW_3B, stroke_width=3).set_points_as_corners(
            [G.p(*q) for q in hot[: fidx() + 1]] + ([G.p(*hot[fidx()])] if fidx() == 0 else [])))
        leg = VGroup(
            VGroup(Dot(radius=0.11, color=YELLOW_3B), Tex("hottest point", font_size=30)).arrange(RIGHT, buff=0.2),
            VGroup(Dot(radius=0.11, color=BLUE_E).set_stroke(WHITE, 2), Tex("coldest point", font_size=30)).arrange(
                RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 4.9 + UP * 1.6)
        tl = Tex(r"time $t=$", font_size=30).move_to(RIGHT * 4.6 + UP * 0.2)
        tv = DecimalNumber(0, num_decimal_places=3, font_size=30).next_to(tl, RIGHT, buff=0.15)
        tv.add_updater(lambda m: m.set_value(times[fidx()]))
        note = Tex(r"insulated edge;\\ colors rescaled\\ at each moment", font_size=26, color=GREY_A).move_to(
            RIGHT * 4.9 + DOWN * 1.3)
        with self.say("Take a flat metal plate, insulated along its edge so no heat can escape, and give it an uneven "
                      "starting temperature. {go}Now let the heat flow. The bumps smooth out, and the hottest point, "
                      "in yellow, wanders. {late}After a long time the temperature settles into a single shape, and "
                      "the hottest and coldest points end up on the boundary. {q}Is that always what happens?") as s:
            self.play(FadeIn(img), Create(bnd), FadeIn(leg), FadeIn(tl), FadeIn(tv), FadeIn(note))
            self.add(path, hd, cd)
            s.wait_until("go")
            img.add_updater(upd_img)
            self.play(kt.animate.set_value(1), run_time=11, rate_func=linear)
            img.clear_updaters()
            s.wait_until("q")
            self.play(Flash(hd, color=YELLOW_3B), Flash(cd, color=BLUE_3B))
        tv.clear_updaters()
        self.play(FadeOut(Group(img, bnd, hd, cd, path, leg, tl, tv, note)))
        self.remove(hd, cd, path)

        # ------------------------------------------------------------ the eigenfunction
        G2 = Field(1.6, [-2.9, -0.5])
        im1 = G2.image(D["phi1"])
        b2 = G2.boundary()
        eq = VGroup(MathTex(r"\Delta u+\mu\,u=0", r"\ \text{ in }\Omega", font_size=38),
                    MathTex(r"\partial_\nu u=0", r"\ \text{ on }\partial\Omega", font_size=38),
                    Tex(r"$\mu$ = first positive Neumann eigenvalue", font_size=28, color=GREY_A),
                    ).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.9 + UP * 1.2)
        heat = MathTex(r"\text{temperature}(t)\ \approx\ \text{average}+c\,e^{-\mu t}\,u", font_size=34).move_to(
            RIGHT * 3.6 + DOWN * 1.0)
        qq = Tex(r"Where are the extremes of $u$?", font_size=36, color=YELLOW_3B).move_to(RIGHT * 3.6 + DOWN * 2.3)
        with self.say("Why a single shape? Heat flow splits into modes, each fading at its own rate. The constant mode "
                      "never fades: it is the average temperature. {u}The slowest mode that does fade is the first "
                      f"nonconstant {NEU} eigenfunction, u: it solves the Helmholtz equation inside, and has zero "
                      "normal derivative on the edge. {h}After a long time, the temperature is the average plus a "
                      "multiple of u. {q}So the real question is: where are the extremes of u?") as s:
            self.play(FadeIn(im1), Create(b2))
            s.wait_until("u")
            self.play(FadeIn(eq[:2]), FadeIn(eq[2]))
            s.wait_until("h")
            self.play(Write(heat))
            s.wait_until("q")
            self.play(FadeIn(qq))
        self.play(FadeOut(Group(im1, b2, eq, heat, qq)))

        # ------------------------------------------------------------ history
        hc = LEFT * 3.6 + DOWN * 0.2
        outer = Ellipse(width=5.4, height=3.6, color=WHITE).move_to(hc).set_fill(GREY_E, 0.6)
        holes = VGroup(Circle(radius=0.45, color=WHITE).set_fill(BLACK, 1).move_to(hc + LEFT * 1.2 + UP * 0.3),
                       Circle(radius=0.45, color=WHITE).set_fill(BLACK, 1).move_to(hc + RIGHT * 1.2 + DOWN * 0.3))
        hs = Dot(hc + DOWN * 0.15 + LEFT * 0.05, radius=0.12, color=YELLOW_3B)
        hl = Tex(r"with holes the hot spot\\ can sit inside (schematic)", font_size=28).next_to(outer, DOWN, buff=0.3)
        items = VGroup(
            Tex(r"1975: Rauch's hot spots question", font_size=30),
            Tex(r"1999: Burdzy--Werner, counterexample with 2 holes", font_size=30, color=RED_3B),
            Tex(r"2000: Bass--Burdzy, both extremes inside", font_size=30, color=RED_3B),
            Tex(r"2005: Burdzy, a counterexample with 1 hole", font_size=30, color=RED_3B),
            Tex(r"Conjecture (Burdzy): true for simply connected domains", font_size=30, color=YELLOW_3B),
            Tex(r"Known: convex with two symmetry axes (Jerison--Nadirashvili),", font_size=26, color=GREY_A),
            Tex(r"lip domains (Atar--Burdzy), all triangles (Judge--Mondal), \dots", font_size=26, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 3.0 + DOWN * 0.1)
        with self.say(f"The question goes back to Jeffrey Rauch in 1975, and the hope was that hot spots always go "
                      f"to the boundary. {{bw}}But in 1999, {BUR} and Werner built a counterexample: a domain with two "
                      f"holes. {{bb}}Bass and {BUR} then got both extremes inside, {{one}}and {BUR} later did it with "
                      "just one hole. {c}So topology matters. The conjecture that survived is for simply connected "
                      f"domains, those without holes, stated by {BUR}. {{k}}Special cases were proved: convex domains "
                      "with two axes of symmetry, so called lip domains, and every triangle.") as s:
            self.play(FadeIn(items[0]))
            s.wait_until("bw")
            self.play(FadeIn(outer), FadeIn(holes), FadeIn(hs, scale=2), FadeIn(hl), FadeIn(items[1]))
            s.wait_until("bb")
            self.play(FadeIn(items[2]))
            s.wait_until("one")
            self.play(FadeIn(items[3]))
            s.wait_until("c")
            self.play(FadeIn(items[4]))
            s.wait_until("k")
            self.play(FadeIn(items[5:]))
        self.play(FadeOut(VGroup(outer, holes, hs, hl, items)))

        # ------------------------------------------------------------ theorem
        thm = VGroup(
            Tex(r"\textbf{Theorem.} Let $\Omega\subset\mathbb{R}^2$ be bounded, simply connected,", font_size=38),
            Tex(r"with smooth boundary. Every eigenfunction $u\neq0$ for the first", font_size=38),
            Tex(r"positive Neumann eigenvalue satisfies $\nabla u\neq0$ everywhere in $\Omega$.", font_size=38),
            Tex(r"So $\min_{\partial\Omega}u<u(x)<\max_{\partial\Omega}u$ inside, even if $\mu$ is multiple.",
                font_size=32, color=GREY_A),
        ).arrange(DOWN, buff=0.25)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3))
        with self.say("A manuscript in OpenAI's math catalogue, produced by an OpenAI model and not yet peer "
                      "reviewed, proves a strict form of the conjecture. On every smooth, bounded, simply connected "
                      "planar domain, every first nonconstant eigenfunction has nonzero gradient everywhere inside. "
                      "{nc}No interior critical points at all: no interior maximum, no minimum, not even a saddle. "
                      "And this holds even when the eigenvalue is repeated.") as s:
            self.play(FadeIn(tb), run_time=2)
            s.wait_until("nc")
            self.play(Indicate(thm[2], color=YELLOW_3B))
        self.play(FadeOut(tb))

        # ------------------------------------------------------------ proof 1: tangent gradients and Rohleder
        hdr = Tex("The gradient field of $u$ is tangent to the boundary", font_size=36, color=YELLOW_3B).to_edge(
            UP, buff=0.35)
        G3 = Field(1.5, [-3.0, -0.6])
        im3 = G3.image(D["phi1"]).set_opacity(0.55)
        b3 = G3.boundary()
        bd = D["boundary"]
        arrows = VGroup()
        A = D["arrows"]
        mags = np.hypot(A[:, 2], A[:, 3])
        for x, y, gx, gy in A:
            dist = np.min(np.hypot(bd[:, 0] - x, bd[:, 1] - y))
            m = np.hypot(gx, gy)
            L = 0.12 + 0.35 * np.sqrt(m / mags.max())
            d = np.array([gx, gy, 0]) / (m + 1e-12)
            p = G3.p(x, y)
            arrows.add(Arrow(p - d * L / 2, p + d * L / 2, buff=0, stroke_width=2.5,
                             color=YELLOW_3B if dist < 0.16 else WHITE, max_tip_length_to_length_ratio=0.35))
        rows = VGroup(
            Tex(r"Neumann condition $\Rightarrow$ $\nabla u$ is tangent on $\partial\Omega$", font_size=30),
            Tex(r"Rohleder: for every tangent field $X$,", font_size=30),
            MathTex(r"\int_\Omega(\operatorname{div}X)^2+(\operatorname{curl}X)^2\ \ge\ \mu\int_\Omega|X|^2",
                    font_size=34),
            Tex(r"with equality exactly for $X=\nabla u$, $u$ in the eigenspace", font_size=30, color=YELLOW_3B),
        ).arrange(DOWN, buff=0.3).move_to(RIGHT * 3.4 + DOWN * 0.3)
        with self.say("Here is the idea of the proof. {gr}Look at the gradient of u. The insulated, or Neumann, "
                      "condition says it has no component pointing out of the domain: along the edge, the gradient "
                      f"is tangent to the boundary. {{ro}}A variational principle of {ROH} says that for any vector "
                      "field tangent to the boundary, its divergence and curl energy is at least mu times its size, "
                      "{eq}with equality exactly for gradients of first eigenfunctions. So these gradients are the "
                      "zero set of a nonnegative energy.") as s:
            self.play(Write(hdr))
            s.wait_until("gr")
            self.play(FadeIn(im3), Create(b3))
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.01), FadeIn(rows[0]), run_time=2.5)
            s.wait_until("ro")
            self.play(FadeIn(rows[1]), Write(rows[2]), run_time=2)
            s.wait_until("eq")
            self.play(FadeIn(rows[3]))
        self.play(FadeOut(Group(hdr, im3, b3, arrows, rows)))

        # ------------------------------------------------------------ proof 2: multipliers and the kernel theorem
        hdr = Tex("Scalar multipliers on the boundary circle", font_size=36, color=YELLOW_3B).to_edge(UP, buff=0.35)
        G4 = Field(0.75, [-5.3, 1.2])
        b4 = G4.boundary()
        dc = Circle(radius=1.1, color=WHITE).move_to(LEFT * 1.6 + UP * 1.2)
        phi = Arrow(dc.get_left() + LEFT * 0.05, b4.get_right() + RIGHT * 0.05, buff=0.1, color=GREY_B)
        phl = MathTex(r"\Phi", font_size=32).next_to(phi, UP, buff=0.05)
        sang, tang = 2.3, -0.5
        sp_ = dc.point_at_angle(sang)
        tp_ = dc.point_at_angle(tang)
        st = VGroup(Dot(sp_, color=TEAL_3B), Dot(tp_, color=TEAL_3B), DashedLine(sp_, tp_, color=TEAL_3B),
                    MathTex("s", font_size=28).next_to(sp_, UL, buff=0.05),
                    MathTex("t", font_size=28).next_to(tp_, DR, buff=0.05))
        en = MathTex(r"E(bg)=\tfrac12\iint N(s,t)\,\big(b(s)-b(t)\big)^2\,g(s)\cdot g(t)\,ds\,dt",
                     font_size=30).move_to(RIGHT * 3.2 + UP * 1.5)
        enl = Tex(r"$g$ = boundary gradient (tangent), $b$ = scalar multiplier", font_size=26, color=GREY_A).next_to(
            en, DOWN, buff=0.2)
        kern = MathTex(r"D_p(s,t)=\frac{K(p,s)\,K(p,t)}{N(s,t)}", font_size=38).move_to(LEFT * 3.4 + DOWN * 1.5)
        kl = Tex(r"is a squared distance:\\ the circle embeds in a Hilbert space", font_size=28).next_to(
            kern, DOWN, buff=0.25)
        hc3 = RIGHT * 2.4 + DOWN * 1.55

        def knot(t):
            return hc3 + 0.36 * np.array([np.sin(t) + 2 * np.sin(2 * t), np.cos(t) - 2 * np.cos(2 * t), 0])

        ts_ = np.linspace(0, TAU, 240)
        curve3 = VMobject(color=TEAL_3B, stroke_width=3).set_points_smoothly([knot(t) for t in ts_])
        ks, kt_ = knot(0.6), knot(3.4)
        chord = VGroup(Dot(ks, color=WHITE, radius=0.06), Dot(kt_, color=WHITE, radius=0.06),
                       DashedLine(ks, kt_, color=WHITE, stroke_width=2))
        chl = MathTex(r"\sqrt{D_p(s,t)}", font_size=28).next_to(chord[2], RIGHT, buff=0.1).shift(DOWN * 0.3)
        hlab = Tex(r"circle in Hilbert space\\ (schematic)", font_size=24, color=GREY_A).next_to(
            curve3, RIGHT, buff=0.3).shift(UP * 0.75)
        sumid = MathTex(r"\sum_j E(b_j\,g)\ =\ \tfrac12\,\big|\nabla u(\Phi(p))\big|^2", font_size=38,
                        color=YELLOW_3B).move_to(RIGHT * 3.3 + DOWN * 3.35)
        with self.say("Now map the domain onto a disk, by a conformal map. {mul}Multiply the boundary gradient g by "
                      "any scalar function b: it stays tangent. Its energy works out to a double integral over the "
                      "circle, with a positive kernel N, but the factor g of s dotted with g of t has no fixed sign. "
                      "{ker}The central new theorem handles this. For each interior point p, a kernel built from "
                      "Green's function, D sub p, is conditionally negative definite: it is the squared distance of "
                      "an embedding of the circle into a Hilbert space. {sum}Using its coordinates as multipliers, "
                      "the energies add up to exactly half the squared gradient of u at the point p.") as s:
            self.play(Write(hdr))
            self.play(Create(b4), Create(dc), GrowArrow(phi), FadeIn(phl))
            s.wait_until("mul")
            self.play(FadeIn(st), Write(en), FadeIn(enl), run_time=2)
            s.wait_until("ker")
            self.play(Write(kern), FadeIn(kl))
            self.play(Create(curve3), FadeIn(hlab), run_time=1.5)
            self.play(FadeIn(chord), FadeIn(chl))
            s.wait_until("sum")
            self.play(Write(sumid), run_time=2)
        self.play(FadeOut(VGroup(hdr, b4, dc, phi, phl, st, en, enl, kern, kl, curve3, chord, chl, hlab, sumid)))

        # ------------------------------------------------------------ proof 3: contradiction
        chain = VGroup(
            Tex(r"Suppose $\nabla u(x_0)=0$ at an interior point $x_0=\Phi(p)$.", font_size=34),
            MathTex(r"\Rightarrow\ E(b_j\,g)=0\ \text{ for every } j", font_size=38),
            Tex(r"$\Rightarrow$ each $b_j\,g$ is the gradient of another first eigenfunction", font_size=34),
            Tex(r"$\Rightarrow$ more independent eigenfunctions than the eigenspace can hold", font_size=34),
            Tex(r"(on these domains its dimension is at most 2: Nadirashvili)", font_size=30, color=GREY_A),
            Tex(r"Contradiction: $\nabla u\neq0$ everywhere inside.", font_size=38, color=GREEN_3B),
        ).arrange(DOWN, buff=0.35)
        with self.say("Now suppose the gradient vanished at some interior point. {z}Then every one of these "
                      "multiplied fields has zero energy, {e}so by the equality case, each one is the gradient of "
                      "another first eigenfunction. {m}That produces more independent eigenfunctions than the "
                      f"eigenspace can hold: on these domains its dimension is at most two, a result of {NAD}. "
                      "{c}So the gradient never vanishes, and the hot spots are on the boundary.") as s:
            self.play(FadeIn(chain[0]))
            s.wait_until("z")
            self.play(FadeIn(chain[1]))
            s.wait_until("e")
            self.play(FadeIn(chain[2]))
            s.wait_until("m")
            self.play(FadeIn(chain[3:5]))
            s.wait_until("c")
            self.play(FadeIn(chain[5], scale=1.1))
        self.play(FadeOut(chain))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Smooth bounded simply connected $\Omega\subset\mathbb{R}^2$: first Neumann eigenfunctions",
             r"have no interior critical points, so all extrema lie on $\partial\Omega$",
             r"Manuscript: 21 pages, produced by an OpenAI model"],
            True, r"\emph{Strict hot spots and absence of interior critical points} (Sept.\ 2026)")
        with self.say("The manuscript is only twenty one pages, and the full theorem, including repeated "
                      "eigenvalues, has been formalized and checked in the Lean proof assistant. {c}It covers "
                      "smooth boundaries; domains with corners, like polygons, are outside this statement.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("c")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
