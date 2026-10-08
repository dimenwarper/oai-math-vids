import numpy as np
from manim import *

from style import *
from vo import NarratedScene

BLOCH = "[Bloch](/blɑk/)"
TOTH = "[Tóth](/tOt/)"
LIEB = "[Lieb](/lˈib/)"
FROH = "[Fröhlich](/fɹˈAlɪk/)"
MERMIN = "[Mermin](/mˈɜɹmɪn/)"

D = np.load("videos/data/v40.npz")


class Video(NarratedScene):
    def construct(self):
        card = title_card(self, "271", r"Bloch's $T^{3/2}$ Law",
                          r"Spontaneous magnetization of the quantum Heisenberg ferromagnet")
        with self.say(f"{BLOCH}'s law, and the quantum Heisenberg ferromagnet."):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ hook: spins and spin waves
        nx, ny, sp = 9, 5, 0.72
        origin = np.array([-3.6, 0.0, 0])
        sites = [origin + np.array([(i - (nx - 1) / 2) * sp, (j - (ny - 1) / 2) * sp * 1.1, 0])
                 for j in range(ny) for i in range(nx)]
        tt = ValueTracker(0.0)
        amp = ValueTracker(0.0)

        def spins():
            g = VGroup()
            th = amp.get_value()
            for k, p in enumerate(sites):
                i = k % nx
                ph = 0.8 * i - tt.get_value()
                d = np.array([np.sin(th) * np.cos(ph), np.cos(th) * 0.95 + 0.25 * np.sin(th) * np.sin(ph), 0])
                d = d / np.linalg.norm(d) * 0.5
                g.add(Arrow(p - d / 2, p + d / 2, buff=0, color=BLUE_3B, stroke_width=4,
                            max_tip_length_to_length_ratio=0.35))
            return g

        sv = always_redraw(spins)
        ax = Axes(x_range=[0, 0.6, 0.1], y_range=[0.8, 1.0, 0.05], x_length=5.0, y_length=3.6, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": True, "font_size": 22,
                               "decimal_number_config": {"num_decimal_places": 2}}).move_to(RIGHT * 3.6 + DOWN * 0.3)
        T, bl = D["T"], D["bloch"]
        msk = T <= 0.6
        curve = ax.plot_line_graph(T[msk], bl[msk] / 0.5, add_vertex_dots=False, line_color=YELLOW_3B,
                                   stroke_width=4)
        xl = MathTex("T", font_size=30).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = MathTex(r"m/S", font_size=30).next_to(ax.y_axis, UP, buff=0.15)
        lawl = MathTex(r"S-m\ \approx\ 0.0586\,(T/S)^{3/2}", font_size=32, color=YELLOW_3B).next_to(ax, UP,
                                                                                                buff=0.45)
        sl = Tex(r"spin $S=\tfrac12$, low temperature", font_size=24, color=GREY_B).next_to(lawl, DOWN, buff=0.1)
        z0 = Tex(r"$T=0$: all aligned", font_size=30).next_to(VGroup(*[Dot(p) for p in sites]), DOWN, buff=0.5)
        z1 = Tex(r"$T>0$: spin waves (magnons)", font_size=30, color=TEAL_3B).move_to(z0)
        with self.say("A ferromagnet is made of atoms whose tiny quantum spins prefer to point the same way as their "
                      "neighbors. {z}At absolute zero, they all line up. {w}Warm the magnet a little, and the spins "
                      "start to wobble together, in waves: spin waves, or magnons. {b}In 1930, Felix "
                      f"{BLOCH} used them to predict how fast the magnetization drops: by an amount proportional to "
                      "the temperature to the power three halves.") as s:
            self.add(sv)
            self.play(FadeIn(sv))
            s.wait_until("z")
            self.play(FadeIn(z0))
            s.wait_until("w")
            self.play(FadeOut(z0), FadeIn(z1), amp.animate.set_value(0.5), tt.animate.set_value(2.5), run_time=2.5,
                      rate_func=linear)
            self.play(tt.animate.set_value(5.0), run_time=2.0, rate_func=linear)
            s.wait_until("b")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), tt.animate.set_value(7.0), run_time=1.5, rate_func=linear)
            self.play(Create(curve), FadeIn(lawl), FadeIn(sl), tt.animate.set_value(10.0), run_time=2.5,
                      rate_func=linear)
            self.play(tt.animate.set_value(13.0), run_time=s.remaining(), rate_func=linear)
        self.remove(sv)
        self.play(FadeOut(VGroup(spins(), ax, xl, yl, curve, lawl, sl, z1)))

        # ------------------------------------------------------------ the model and the history
        H = MathTex(r"H=-\sum_{x\sim y}\ \vec S_x\cdot\vec S_y", font_size=50).to_edge(UP, buff=0.5)
        Hl = Tex(r"Heisenberg (1928): no preferred direction", font_size=30, color=GREY_A).next_to(H, DOWN,
                                                                                                buff=0.2)
        q = Tex(r"At zero field, does an infinite lattice pick a direction by itself?", font_size=34,
                color=YELLOW_3B).next_to(Hl, DOWN, buff=0.45)
        hist = VGroup(
            Tex(r"Mermin--Wagner (1966): impossible in dimensions 1 and 2", font_size=32),
            Tex(r"$d\ge3$: Fr\"ohlich--Simon--Spencer (1976), classical spins", font_size=32),
            Tex(r"$d\ge3$: Dyson--Lieb--Simon (1978), quantum antiferromagnets", font_size=32),
            Tex(r"quantum \emph{ferro}magnet: reflection positivity fails", font_size=32, color=ORANGE_3B),
            Tex(r"posed as an open problem by Lieb (1999)", font_size=32, color=ORANGE_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).next_to(q, DOWN, buff=0.5)
        with self.say("The quantum Heisenberg model adds up the dot products of neighboring spin operators. Rotate "
                      "every spin together and nothing changes. {q}So the question is whether an infinite lattice, "
                      "at a small positive temperature and zero field, still picks a direction on its own: "
                      f"spontaneous magnetization. {{mw}}{MERMIN} and Wagner proved this is impossible in one or two "
                      f"dimensions. {{d3}}In three dimensions, {FROH}, Simon and Spencer proved ordering for classical "
                      f"spins, and Dyson, {LIEB} and Simon for quantum antiferromagnets, using reflection positivity. "
                      "{fm}But that tool fails for the quantum ferromagnet, the very model behind Bloch's law. "
                      f"{{l}}{LIEB} posed it as an open problem in 1999.".replace("Bloch's", f"{BLOCH}'s")) as s:
            self.play(Write(H), FadeIn(Hl))
            s.wait_until("q")
            self.play(FadeIn(q))
            s.wait_until("mw")
            self.play(FadeIn(hist[0]))
            s.wait_until("d3")
            self.play(FadeIn(hist[1]))
            self.play(FadeIn(hist[2]))
            s.wait_until("fm")
            self.play(FadeIn(hist[3]))
            s.wait_until("l")
            self.play(FadeIn(hist[4]))
        self.play(FadeOut(VGroup(H, Hl, q, hist)))

        # ------------------------------------------------------------ the theorems
        t1 = VGroup(Tex(r"\textbf{Theorem 1.} $d\ge3$, any spin $S$, any low enough temperature:", font_size=32),
                    Tex(r"a translation-invariant equilibrium state with magnetization $\ge S/4$.", font_size=32)
                    ).arrange(DOWN, buff=0.15)
        b1 = VGroup(t1, caption_box(t1, TEAL_3B, 0.25)).to_edge(UP, buff=0.4)
        t2 = VGroup(Tex(r"\textbf{Theorem 2 (Bloch's law).} 3D, any spin, any finite-range coupling:",
                        font_size=32),
                    MathTex(r"\lim_{T\to0}\ \frac{S-m(T)}{T^{3/2}}\ =\ \frac{\zeta(3/2)}{8\pi^{3/2}\sqrt{\det D}}",
                            font_size=46)).arrange(DOWN, buff=0.25)
        b2 = VGroup(t2, caption_box(t2, YELLOW_3B, 0.25)).next_to(b1, DOWN, buff=0.4)
        Dl = Tex(r"$D$: quadratic part of the magnon energy; nearest neighbors: $D=S\cdot I$", font_size=28,
                 color=GREY_A).next_to(b2, DOWN, buff=0.25)
        ordl = Tex(r"limits in order: infinite volume, then field $\downarrow0$, then $T\to0$", font_size=28,
                   color=GREY_A).next_to(Dl, DOWN, buff=0.15)
        comp = Tex(r"companions: the first lattice correction; the spherical magnetization law", font_size=28,
                   color=GREY_A).next_to(ordl, DOWN, buff=0.3)
        with self.say("Manuscripts in OpenAI's math catalogue, not yet peer reviewed, claim to settle both. "
                      "{a}First: in every dimension three or higher, for every spin, at every low enough "
                      "temperature, there is a translation-invariant equilibrium state with magnetization at least "
                      f"S over four. {{b}}Second: {BLOCH}'s law itself, with its exact coefficient. As the "
                      "temperature goes to zero, the magnetization deficit divided by T to the three halves tends "
                      "to zeta of three halves, over eight pi to the three halves times the square root of the "
                      "determinant of D. {d}Here D is the quadratic part of the magnon energy. {o}The limits are "
                      "taken in a careful order: infinite volume first, then zero field, then low temperature. "
                      "{c}Companion papers add the first lattice correction, and a spherical magnetization "
                      "law.") as s:
            s.wait_until("a")
            self.play(FadeIn(b1), run_time=1.5)
            s.wait_until("b")
            self.play(FadeIn(b2), run_time=2)
            s.wait_until("d")
            self.play(FadeIn(Dl))
            s.wait_until("o")
            self.play(FadeIn(ordl))
            s.wait_until("c")
            self.play(FadeIn(comp))
        self.play(FadeOut(VGroup(b1, b2, Dl, ordl, comp)))

        # ------------------------------------------------------------ the loop picture
        L, beta = int(D["L"]), float(D["beta"])
        segs, marks = D["segs"], D["marks"]
        X0, DX, Y0, HT = -5.5, 0.62, -2.5, 4.6
        xof = lambda i: X0 + DX * i
        yof = lambda t: Y0 + HT * t / beta
        hdr = Tex(r"T\'oth's loop picture", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.35)
        rails = VGroup(*[Line([xof(i), yof(0), 0], [xof(i), yof(beta), 0], color=GREY_D, stroke_width=2)
                         for i in range(L)])
        mk = VGroup()
        for t, b in marks:
            b = int(b)
            if b < L - 1:
                mk.add(Line([xof(b), yof(t), 0], [xof(b + 1), yof(t), 0], color=GREY_B, stroke_width=3))
            else:
                mk.add(Line([xof(L - 1), yof(t), 0], [xof(L - 1) + DX / 2, yof(t), 0], color=GREY_B, stroke_width=3))
                mk.add(Line([xof(0) - DX / 2, yof(t), 0], [xof(0), yof(t), 0], color=GREY_B, stroke_width=3))
        tax = VGroup(Arrow([X0 - 0.75, yof(0), 0], [X0 - 0.75, yof(beta) + 0.2, 0], buff=0, color=GREY_B,
                           stroke_width=3),
                     MathTex(r"0", font_size=26).move_to([X0 - 1.05, yof(0), 0]),
                     MathTex(r"\beta", font_size=28).move_to([X0 - 1.05, yof(beta), 0]))
        tlab = Tex(r"imaginary time, a circle of length $\beta=1/T$", font_size=24, color=GREY_B).next_to(
            rails, UP, buff=0.15)
        nloops = int(segs[:, 4].max()) + 1
        rng = np.random.default_rng(1)
        color_up = rng.random(nloops) < 0.5
        color_up[3] = False

        def loop_mob(k, col, w=4):
            g = VGroup()
            for x0, t0, x1, t1, lp, kind in segs:
                if int(lp) != k:
                    continue
                x0, x1 = int(x0), int(x1)
                if kind == 0:
                    g.add(Line([xof(x0), yof(t0), 0], [xof(x0), yof(t1), 0], color=col, stroke_width=w))
                elif abs(x1 - x0) == 1:
                    g.add(Line([xof(x0), yof(t0), 0], [xof(x1), yof(t0), 0], color=col, stroke_width=w))
                else:
                    sgn = 1 if x0 == L - 1 else -1
                    g.add(Line([xof(x0), yof(t0), 0], [xof(x0) + sgn * DX / 2, yof(t0), 0], color=col, stroke_width=w))
                    g.add(Line([xof(x1) - sgn * DX / 2, yof(t0), 0], [xof(x1), yof(t0), 0], color=col, stroke_width=w))
            return g

        big = loop_mob(3, YELLOW_3B, 6)
        allloops = VGroup(*[loop_mob(k, BLUE_3B if color_up[k] else RED_3B, 4) for k in range(nloops)])
        # time-zero spins from the loop colours
        site_loop = {}
        for x0, t0, x1, t1, lp, kind in segs:
            if kind == 0 and t0 == 0.0:
                site_loop[int(x0)] = int(lp)
        def spin_arrow(i):
            up = color_up[site_loop[i]]
            a_, b_ = np.array([xof(i), yof(0) - 0.65, 0]), np.array([xof(i), yof(0) - 0.15, 0])
            return Arrow(a_ if up else b_, b_ if up else a_, buff=0, stroke_width=4,
                         max_tip_length_to_length_ratio=0.4, color=BLUE_3B if up else RED_3B)

        arrows0 = VGroup(*[spin_arrow(i) for i in range(L)])
        side = VGroup(
            Tex(r"spin $S$ $\to$ $2S$ slots of spin $\tfrac12$", font_size=30),
            Tex(r"neighbors swap at random times", font_size=30),
            Tex(r"follow a line up; wrap at $\beta$", font_size=30),
            Tex(r"lines close into loops", font_size=30, color=YELLOW_3B),
            Tex(r"each loop: all up or all down", font_size=30, color=TEAL_3B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 4.35 + UP * 0.3)
        wl = Tex(r"this loop winds around time 3 times", font_size=28, color=YELLOW_3B).next_to(side, DOWN, buff=0.5)
        with self.say(f"The proof uses a random loop picture, due to {TOTH}. {{s}}Split each spin S into two S "
                      "slots of spin one half. {t}Run imaginary time around a circle whose length is one over the "
                      "temperature, and let neighboring slots swap at random times. {f}Follow a line upward: at "
                      "each swap it jumps, and at the top it wraps around to the bottom. {l}The lines close up into "
                      "loops. This one winds around time three times. {c}Each loop is either all up or all down, "
                      "and the magnetization is the balance of up and down slots.") as s:
            self.play(Write(hdr))
            s.wait_until("s")
            self.play(FadeIn(side[0]))
            s.wait_until("t")
            self.play(Create(rails), FadeIn(tax), FadeIn(tlab), FadeIn(side[1]))
            self.play(LaggedStart(*[Create(m) for m in mk], lag_ratio=0.05), run_time=1.5)
            s.wait_until("f")
            self.play(FadeIn(side[2]))
            s.wait_until("l")
            self.play(Create(big), FadeIn(side[3]), run_time=3, rate_func=linear)
            self.play(FadeIn(wl))
            s.wait_until("c")
            self.play(FadeIn(allloops), FadeOut(big), FadeIn(side[4]), FadeOut(wl))
            self.play(FadeIn(arrows0))
        self.play(FadeOut(VGroup(hdr, rails, mk, tax, tlab, allloops, arrows0, side)))
        hdr = Tex(r"From loops to returns", font_size=40, color=YELLOW_3B).to_edge(UP, buff=0.35)

        # ------------------------------------------------------------ pins, returns, random walk
        pin = VGroup(
            Tex(r"pin the boundary up: loops touching it must be up", font_size=32),
            Tex(r"a slot is down only if its loop avoids every pin", font_size=32),
            MathTex(r"\Pr(\text{down})=\frac{r}{1+r}", font_size=44, color=YELLOW_3B),
            Tex(r"$r$: chance its line returns to it, after winding around time, before any pin",
                font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.25).next_to(hdr, DOWN, buff=0.4)
        with self.say("To magnetize the system, pin the boundary: loops that touch it must be up. {d}Then a slot "
                      "points down only if its loop avoids every pin. {r}The paper turns this into a return "
                      "probability: the chance of being down is r over one plus r, where r is the chance that the "
                      "line from the slot comes back to it, after winding around time, before it meets a pin.") as s:
            self.play(Write(hdr), FadeIn(pin[0]))
            s.wait_until("d")
            self.play(FadeIn(pin[1]))
            s.wait_until("r")
            self.play(Write(pin[2]), FadeIn(pin[3]), run_time=2)
        self.play(FadeOut(pin))

        ts, pr, asy = D["ts"], D["pret"], D["asym"]
        # log-log axes; coordinates shifted so the axes sit at the lower-left corner
        ax2 = Axes(x_range=[0, 3.6, 1], y_range=[0, 5, 1], x_length=5.4, y_length=4.0, tips=False,
                   axis_config={"color": GREY_B}).move_to(LEFT * 3.3 + UP * 0.1)
        LP = lambda lx, ly: ax2.c2p(lx + 1.3, ly + 5)
        xt = VGroup(*[MathTex(f"10^{{{k}}}", font_size=22).next_to(LP(k, -5), DOWN, buff=0.12) for k in (-1, 0, 1, 2)])
        xtk = VGroup(*[Line(LP(k, -5) + DOWN * 0.07, LP(k, -5) + UP * 0.07, color=GREY_B) for k in (-1, 0, 1, 2)])
        yt = VGroup(*[MathTex(f"10^{{{k}}}", font_size=22).next_to(LP(-1.3, k), LEFT, buff=0.12)
                      for k in (-4, -2, 0)])
        xt.add(xtk)
        g1 = ax2.plot_line_graph(np.log10(ts) + 1.3, np.log10(pr) + 5, add_vertex_dots=False, line_color=TEAL_3B,
                                 stroke_width=4)
        m2 = (np.log10(asy) > -5.0) & (np.log10(asy) < -0.05)
        g2 = DashedVMobject(ax2.plot_line_graph(np.log10(ts[m2]) + 1.3, np.log10(asy[m2]) + 5, add_vertex_dots=False,
                                                line_color=YELLOW_3B, stroke_width=3)["line_graph"], num_dashes=40)
        l1 = Tex(r"return probability $p_t$\\ of a walk on $\mathbb{Z}^3$", font_size=26, color=TEAL_3B).move_to(
            LP(1.2, -1.0))
        l2 = MathTex(r"\kappa\,t^{-3/2}", font_size=32, color=YELLOW_3B).move_to(LP(1.75, -3.3))
        xlab = MathTex("t", font_size=28).next_to(ax2.x_axis, DOWN, buff=0.45)
        terms = D["terms"]
        ax3 = Axes(x_range=[0, 13, 1], y_range=[0, 2.8, 0.5], x_length=5.0, y_length=4.0, tips=False,
                   axis_config={"color": GREY_B, "include_numbers": False}).move_to(RIGHT * 3.5 + UP * 0.1)
        cum = np.cumsum(terms)
        bars = VGroup()
        for n_, (tv, cv) in enumerate(zip(terms, cum), start=1):
            r = Rectangle(width=ax3.x_axis.unit_size * 0.7, height=ax3.y_axis.unit_size * tv, stroke_width=0)
            r.set_fill(BLUE_3B, 0.85).move_to(ax3.c2p(n_, cv - tv / 2))
            bars.add(r)
        zl = DashedLine(ax3.c2p(0, float(D["z32"])), ax3.c2p(13, float(D["z32"])), color=YELLOW_3B)
        zt = MathTex(r"\zeta(3/2)=\sum_n n^{-3/2}=2.612\ldots", font_size=30, color=YELLOW_3B).next_to(
            zl, UP, buff=0.12)
        nlab = Tex(r"returns after $n=1,2,3,\dots$ windings", font_size=26).next_to(ax3, DOWN, buff=0.2)
        res = MathTex(r"S-m\ \approx\ \sum_{n\ge1}p_{n\beta}\ \approx\ \kappa\,\zeta(3/2)\,\beta^{-3/2}",
                      font_size=40, color=YELLOW_3B).to_edge(DOWN, buff=0.3)
        with self.say("At low temperature, the line wanders like a random walk on the lattice. {p}Coming back after "
                      "n windings has probability close to the walk's return probability at time n beta, which in "
                      "three dimensions decays like time to the minus three halves. {z}Now add up the returns over "
                      "every number of windings: one, plus two to the minus three halves, plus three to the minus "
                      "three halves, and so on. {s}The sum is zeta of three halves, {f}and that is exactly where "
                      f"{BLOCH}'s coefficient comes from.") as s:
            self.play(Create(ax2), FadeIn(xt), FadeIn(yt), FadeIn(xlab))
            s.wait_until("p")
            self.play(Create(g1), FadeIn(l1), run_time=1.5)
            self.play(Create(g2), FadeIn(l2))
            s.wait_until("z")
            self.play(Create(ax3), FadeIn(nlab))
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in bars], lag_ratio=0.25), run_time=3)
            s.wait_until("s")
            self.play(Create(zl), FadeIn(zt))
            s.wait_until("f")
            self.play(Write(res))
        self.play(FadeOut(VGroup(ax2, xt, yt, g1, g2, l1, l2, xlab, ax3, bars, zl, zt, nlab, res)))

        hard = VGroup(
            Tex(r"The hard part: arbitrarily late returns,", font_size=36, color=ORANGE_3B),
            Tex(r"in a random environment that repeats every period", font_size=36, color=ORANGE_3B),
            Tex(r"tools: stable polynomials and negative dependence (Borcea--Br\"and\'en--Liggett),", font_size=28),
            Tex(r"Nash's energy method for diffusion, and flows to infinity", font_size=28),
        ).arrange(DOWN, buff=0.25).next_to(hdr, DOWN, buff=0.8)
        with self.say("The hard part is controlling returns after arbitrarily many windings, in a random environment "
                      "that repeats every period. {t}For that the papers combine negative dependence from stable "
                      "polynomials, Nash's energy method for diffusion, and carefully routed flows.") as s:
            self.play(FadeIn(hard[:2]))
            s.wait_until("t")
            self.play(FadeIn(hard[2:]))
        self.play(FadeOut(VGroup(hdr, hard)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"Bloch's $T^{3/2}$ law with its exact coefficient,",
             r"\quad for every spin and all 3D finite-range couplings",
             r"Spontaneous magnetization $\ge S/4$ for $d\ge3$ \emph{(this part formalized in Lean)}",
             r"Also: the first lattice correction, and the spherical magnetization law",
             r"Manuscripts produced by an OpenAI model"],
            False, r"\emph{Bloch's Law for Finite-Range Heisenberg Ferromagnets}\\ \emph{in Three Dimensions} (Oct.\ 2026)")
        with self.say("A caveat on verification. The spontaneous magnetization theorem has been formalized in the "
                      f"Lean proof assistant. {{l}}{BLOCH}'s law itself, its lattice correction, and the spherical law "
                      f"have not, and await expert checking. If they hold, {BLOCH}'s prediction from 1930 is finally "
                      "a theorem.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("l")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
