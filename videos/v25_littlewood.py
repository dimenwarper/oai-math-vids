from pathlib import Path

import numpy as np
from manim import *

from style import *
from vo import NarratedScene

D = np.load(Path(__file__).parent / "data" / "v25.npz")
ERD = "[Erdős](/ˈɛɹdəʃ/)"
KAH = "[Kahane](/kɑˈɑn/)"
BOL = "[Bollobás](/bˈɔlɔbɑʃ/)"
SAHA = "[Sahasrabudhe](/sɑhɑsɹɑbˈudA/)"
TIBA = "[Tiba](/tˈibə/)"
GOL = "[Golay](/ɡoʊlˈA/)"
TUR = "[Turyn](/tˈʊɹɪn/)"
MEKA = "[Meka](/mˈAkə/)"
TS = D["ts"]


class Video(NarratedScene):
    def axes(self, ymax=2.1, w=10.5, h=3.6, y_step=0.5):
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, ymax, y_step], x_length=w, y_length=h, tips=False,
                  axis_config={"color": GREY_B, "font_size": 24},
                  x_axis_config={"numbers_to_include": [0, 0.25, 0.5, 0.75, 1],
                                 "decimal_number_config": {"num_decimal_places": 2}},
                  y_axis_config={"numbers_to_include": list(np.arange(y_step, ymax + 1e-9, y_step)),
                                 "decimal_number_config": {"num_decimal_places": 1}})
        return ax

    def curve(self, ax, ys, color, width=2.5, step=2):
        pts = [ax.c2p(t, min(y, ax.y_range[1])) for t, y in zip(TS[::step], ys[::step])]
        pts.append(ax.c2p(1, min(ys[0], ax.y_range[1])))
        return VMobject(color=color, stroke_width=width).set_points_as_corners(pts)

    def bars(self, c, width, height, color_pos=BLUE_3B, color_neg=RED_3B):
        n = len(c)
        w = width / n
        g = VGroup()
        for k, v in enumerate(c):
            r = Rectangle(width=w * 0.8, height=max(abs(v), 1e-3) * height / 2, stroke_width=0).set_fill(
                color_pos if v > 0 else color_neg, 0.9)
            r.move_to(np.array([-width / 2 + (k + 0.5) * w, v * height / 4, 0]))
            g.add(r)
        return g

    def construct(self):
        card = title_card(self, "076", r"Ultraflat Littlewood Polynomials",
                          r"Signs $\pm1$, modulus $(1+o(1))\sqrt N$ on the whole unit circle")
        with self.say("Can a polynomial whose coefficients are all plus or minus one be perfectly flat?"):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(card))

        # ------------------------------------------------------------ the setup
        sm = D["small"]
        cb = self.bars(sm, 6.0, 1.6).move_to(UP * 2.3)
        poly = MathTex(r"p(z)=\sum_{k=0}^{N-1}\varepsilon_k z^k,\qquad \varepsilon_k\in\{-1,+1\}", font_size=38
                       ).next_to(cb, DOWN, buff=0.3)
        ax = self.axes().move_to(DOWN * 1.6)
        xl = MathTex(r"z=e^{2\pi i t}", font_size=28).next_to(ax.x_axis, DOWN, buff=0.4).shift(RIGHT * 4.6)
        yl = MathTex(r"|p(z)|/\sqrt N", font_size=30).next_to(ax.y_axis, UP, buff=0.15).shift(RIGHT * 0.6)
        one = DashedLine(ax.c2p(0, 1), ax.c2p(1, 1), color=YELLOW_3B, stroke_width=2.5)
        c_small = self.curve(ax, D["small_mod"], TEAL_3B, 3, 1)
        par = MathTex(r"\frac1{2\pi}\int_0^{2\pi}|p(e^{i\theta})|^2\,d\theta=N", font_size=32, color=YELLOW_3B
                      ).move_to(RIGHT * 4.9 + UP * 1.05)
        c_rand = self.curve(ax, D["rand_mod"], RED_3B, 2.5)
        rl = Tex(r"random signs, $N=128$", font_size=30, color=RED_3B).move_to(ax.c2p(0.78, 1.95))
        with self.say("Take a polynomial whose coefficients are all plus or minus one, like this one, with sixteen "
                      "terms. {circ}Plug in points z going once around the unit circle, and plot how big the "
                      "polynomial is, divided by root N. {par}Parseval's identity says the average of its squared "
                      "size is exactly N, the number of terms. So its typical size is root N, and the question, "
                      f"going back to Littlewood and {ERD}, is how close to root N it can stay everywhere. {{rand}}"
                      "Random signs are terrible: with a hundred and twenty eight terms, the size swings from almost "
                      "zero to nearly twice root N.") as s:
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if v > 0 else UP) for b, v in zip(cb, sm)], lag_ratio=0.05),
                      Write(poly), run_time=2)
            s.wait_until("circ")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(c_small), run_time=2.5)
            s.wait_until("par")
            self.play(Create(one), FadeIn(par))
            s.wait_until("rand")
            self.play(FadeOut(c_small), FadeOut(cb), Create(c_rand), FadeIn(rl), run_time=2)
        self.play(FadeOut(VGroup(c_rand, rl, poly, par)))

        # ------------------------------------------------------------ history: Rudin-Shapiro, unimodular chirps, BBMST
        c_rs = self.curve(ax, D["rs_mod"], BLUE_3B, 2.5)
        rsl = Tex(r"Rudin--Shapiro, $N=128$: never above $\sqrt2$", font_size=30, color=BLUE_3B).move_to(
            ax.c2p(0.72, 1.95))
        s2 = DashedLine(ax.c2p(0, np.sqrt(2)), ax.c2p(1, np.sqrt(2)), color=BLUE_3B, stroke_width=1.5)
        c_cx = self.curve(ax, D["cplx_mod"], GREEN_3B, 2.5)
        cxl = Tex(r"complex coefficients $e^{\pi i k^2/N}$, $N=512$", font_size=30, color=GREEN_3B).move_to(
            ax.c2p(0.7, 1.95))
        hist = VGroup(
            Tex(r"Shapiro, Rudin: real signs with $\max|p|\le\sqrt{2N}$ at lengths $2^m$", font_size=30),
            Tex(r"Kahane: \emph{complex} unimodular coefficients can be ultraflat", font_size=30),
            Tex(r"Balister--Bollob\'as--Morris--Sahasrabudhe--Tiba: real signs with", font_size=30),
            Tex(r"$c_1\sqrt N\le|p|\le c_2\sqrt N$ (flat up to constants)", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(UP, buff=0.35)
        with self.say("Shapiro and Rudin found signs that do much better: {rs}at lengths that are powers of two, "
                      "the size never exceeds root two times root N. But it can still drop to zero. "
                      f"{{cx}}If you allow complex coefficients of size one, quadratic phases like these, used by "
                      f"Littlewood, are flat over most of the circle, and {KAH} proved that such polynomials can be ultraflat: "
                      "within a factor tending to one of root N, everywhere. {bb}For real signs, the best result "
                      f"came just a few years ago, when Balister, {BOL}, Morris, {SAHA} and {TIBA} proved that real "
                      "flat polynomials exist: between two fixed constant multiples of root N.") as s:
            s.wait_until("rs")
            self.play(FadeIn(hist[0]), Create(s2), Create(c_rs), FadeIn(rsl), run_time=2)
            s.wait_until("cx")
            self.play(FadeOut(c_rs), FadeOut(rsl), FadeOut(s2), Create(c_cx), FadeIn(cxl), FadeIn(hist[1]), run_time=2)
            s.wait_until("bb")
            self.play(FadeIn(hist[2:]))
        self.play(FadeOut(VGroup(c_cx, cxl, hist, ax, xl, yl, one)))

        # ------------------------------------------------------------ merit factor
        mf = MathTex(r"F=\frac{N^2}{2\sum_{u\ge1}C_u^2},\qquad C_u=\sum_j\varepsilon_j\varepsilon_{j+u}", font_size=40
                     ).to_edge(UP, buff=0.5)
        rows = [("random signs, $N=128$", D["rand_merit"]), ("Rudin--Shapiro, $N=128$", D["rs_merit"]),
                ("rotated Legendre sequence, $N=127$", D["leg_merit"])]
        tab = VGroup(*[VGroup(Tex(a, font_size=32), DecimalNumber(float(v), num_decimal_places=2, font_size=32))
                       for a, v in rows])
        tab.add(VGroup(Tex(r"best proven limit (Jedwab--Katz--Schmidt)", font_size=32),
                       MathTex(r"\to 6.34", font_size=32)))
        for r in tab:
            r[1].move_to(RIGHT * 4.2 + r[1].get_y() * UP)
        tab.arrange(DOWN, buff=0.28)
        for r in tab:
            r[0].next_to(LEFT * 5.6 + r.get_y() * UP, RIGHT, buff=0)
            r[1].move_to(RIGHT * 4.3 + r.get_y() * UP)
        tab.move_to(UP * 0.5)
        tur = Tex(r"Turyn's conjecture: $F$ stays bounded", font_size=34, color=RED_3B).next_to(tab, DOWN, buff=0.4)
        idt = MathTex(r"\frac1F=\frac1{2\pi}\int_0^{2\pi}\Big(\frac{|p(e^{i\theta})|^2}{N}-1\Big)^2d\theta",
                      font_size=38, color=YELLOW_3B).to_edge(DOWN, buff=0.35)
        idl = Tex(r"flat $\Rightarrow F\to\infty$", font_size=32, color=YELLOW_3B).next_to(idt, RIGHT, buff=0.4)
        with self.say(f"This matters outside pure math too. In radar and communications, engineers want binary "
                      f"sequences whose shifted copies barely correlate with themselves, measured by {GOL}'s merit "
                      "factor. {tab}Random signs give a merit factor near one, Rudin Shapiro about three, and the "
                      "best families with a proven limit, built from Legendre sequences, approach about six point "
                      "three four. "
                      f"{{tur}}{TUR} conjectured that merit factors stay bounded. {{id}}But one over the merit factor "
                      "is exactly the average squared deviation of the normalized size from one. So flat polynomials "
                      "would have huge merit factors.") as s:
            self.play(Write(mf), run_time=2)
            s.wait_until("tab")
            self.play(LaggedStart(*[FadeIn(r) for r in tab], lag_ratio=0.4), run_time=3)
            s.wait_until("tur")
            self.play(FadeIn(tur))
            s.wait_until("id")
            self.play(Write(idt), run_time=2)
            self.play(FadeIn(idl))
        self.play(FadeOut(VGroup(mf, tab, tur, idt, idl)))

        # ------------------------------------------------------------ theorem
        thm = VGroup(
            Tex(r"\textbf{Theorem.} For every $\varepsilon>0$ and every sufficiently large $N$ there are", font_size=38),
            Tex(r"signs $\varepsilon_0,\dots,\varepsilon_{N-1}\in\{-1,1\}$ with", font_size=38),
            MathTex(r"(1-\varepsilon)\sqrt N\ \le\ \Big|\sum_{k<N}\varepsilon_k z^k\Big|\ \le\ (1+\varepsilon)\sqrt N"
                    r"\qquad(|z|=1).", font_size=42),
        ).arrange(DOWN, buff=0.3)
        tb = VGroup(thm, caption_box(thm, YELLOW_3B, 0.3)).shift(UP * 0.8)
        cons = VGroup(
            Tex(r"$\Rightarrow$ no fixed gap above $\sqrt N$ (real-sign analogue of an Erd\H{o}s conjecture fails)",
                font_size=30),
            Tex(r"$\Rightarrow$ merit factors tend to infinity: Turyn's conjecture fails", font_size=30),
            Tex(r"existential: no explicit signs, no efficient algorithm", font_size=30, color=GREY_A),
        ).arrange(DOWN, buff=0.22).next_to(tb, DOWN, buff=0.45)
        with self.say("Manuscripts in OpenAI's math catalogue, produced by an OpenAI model and not yet peer "
                      "reviewed, claim the strongest possible answer. For every epsilon, and every large enough "
                      "length N, there are plus and minus one signs whose polynomial stays between one minus epsilon "
                      f"and one plus epsilon times root N, all the way around the circle. {{c1}}So the {ERD} style gap "
                      "above root N does not exist for real signs, {c2}and merit factors grow without bound, "
                      "disproving Turyn's conjecture. {ex}The proof is existential: it gives no explicit signs and no "
                      "efficient way to find them, so I can't plot one for you.") as s:
            self.play(FadeIn(tb), run_time=2)
            s.wait_until("c1")
            self.play(FadeIn(cons[0]))
            s.wait_until("c2")
            self.play(FadeIn(cons[1]))
            s.wait_until("ex")
            self.play(FadeIn(cons[2]))
        self.play(FadeOut(VGroup(tb, cons)))

        # ------------------------------------------------------------ proof 1: chirps
        hdr = Tex("Quadratic phases: each stretch of coefficients lights up one stretch of the circle", font_size=32,
                  color=YELLOW_3B).to_edge(UP, buff=0.3)
        ax = self.axes(ymax=2.4, w=10.5, h=2.4, y_step=0.8).move_to(UP * 1.05)
        ax2 = self.axes(ymax=2.4, w=10.5, h=2.4, y_step=0.8).move_to(DOWN * 2.0)
        c1 = self.curve(ax, D["ccos_mod"], TEAL_3B, 2.5)
        h1 = DashedLine(ax.c2p(0, 1 / np.sqrt(2)), ax.c2p(1, 1 / np.sqrt(2)), color=TEAL_3B, stroke_width=2)
        l1 = Tex(r"$\varepsilon_k=\cos(\pi k^2/2N)$: flat near $1/\sqrt2$, but not signs", font_size=28,
                 color=TEAL_3B).move_to(ax.c2p(0.62, 2.15))
        c2 = self.curve(ax2, D["csgn_mod"], RED_3B, 2.5)
        o2 = DashedLine(ax2.c2p(0, 1), ax2.c2p(1, 1), color=YELLOW_3B, stroke_width=2)
        l2 = Tex(r"rounded to signs: harmonics collide, flatness breaks", font_size=28, color=RED_3B).move_to(
            ax2.c2p(0.62, 2.15))
        with self.say("How do the manuscripts do it? Start with a chirp: coefficients whose phase grows "
                      "quadratically, so the frequency sweeps steadily. By stationary phase, each stretch of "
                      "coefficients contributes to just one stretch of the circle. {c1}With real cosine "
                      "coefficients, here N is five hundred twelve, the size is nearly flat, but only at about root N "
                      "over root two, because cosines are not signs. {c2}Round them to signs, and it breaks: the "
                      "square wave has harmonics, which sweep the circle again at other speeds and collide with "
                      "each other.") as s:
            self.play(Write(hdr), Create(ax), Create(ax2))
            s.wait_until("c1")
            self.play(Create(c1), Create(h1), FadeIn(l1), run_time=2)
            s.wait_until("c2")
            self.play(Create(c2), Create(o2), FadeIn(l2), run_time=2)
        self.play(FadeOut(VGroup(hdr, ax, ax2, c1, h1, l1, c2, o2, l2)))

        # ------------------------------------------------------------ proof 2: packing
        hdr = Tex("Give every mode on every block its own arc of the circle", font_size=34, color=YELLOW_3B).to_edge(
            UP, buff=0.35)
        ax = self.axes(ymax=1.8, w=6.4, h=2.6, y_step=0.6).move_to(LEFT * 3.0 + UP * 0.6)
        x0, wdt, lam, eta = D["blk_params"]
        cb_ = self.curve(ax, D["blk_mod"], ORANGE_3B, 2.5, 1)
        br = BraceBetweenPoints(ax.c2p(eta - lam * wdt, 1.62), ax.c2p(eta + lam * wdt, 1.62), UP, color=ORANGE_3B)
        brl = Tex(r"width $\propto$ curvature", font_size=26, color=ORANGE_3B).next_to(br, UP, buff=0.1)
        bl = Tex(r"one chirp block (computed): two arcs,\\ at $\pm$ its frequency band", font_size=26).next_to(
            ax, DOWN, buff=0.5)
        cc = RIGHT * 3.6 + UP * 0.4
        circ = Circle(radius=1.7, color=GREY_B).move_to(cc)
        rng = np.random.default_rng(5)
        arcs = VGroup()
        pos, cols = 0.03, [BLUE_3B, TEAL_3B, GREEN_3B, YELLOW_3B, ORANGE_3B, RED_3B, PURPLE_3B]
        k = 0
        while pos < 0.47:
            w = rng.uniform(0.02, 0.07)
            if pos + w > 0.49:
                break
            c = cols[k % len(cols)]
            for sgn in (1, -1):
                a0 = sgn * TAU * (pos + w / 2) - TAU * w / 2 * 0.92
                arcs.add(Arc(radius=1.7, start_angle=a0, angle=TAU * w * 0.92, arc_center=cc, color=c,
                             stroke_width=12))
            pos += w + 0.006
            k += 1
        al = Tex(r"packed without overlap (schematic):\\ random hypergraph over $\mathbb{F}_q$\\ + Pippenger--Spencer",
                 font_size=26).next_to(circ, DOWN, buff=0.35)
        res = VGroup(
            Tex(r"$\Rightarrow$ at each point of the circle at most one contribution: $|Q|\lesssim(1+\delta)\sqrt N$",
                font_size=30),
            Tex(r"coefficients $x_k\in[-1,1]$ with mean square $\approx1$: almost all already near $\pm1$",
                font_size=30),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.say("The fix is to control every harmonic. The construction starts from a bounded real function "
                      "with many Fourier modes, gives each mode its own curvature, and samples it on many short "
                      "blocks. {blk}Each mode on each block lights up a pair of arcs of the circle, with width "
                      "proportional to its curvature. {pk}The art is to pack all these arcs so that none overlap. "
                      "The manuscript does it with a randomly built hypergraph over a finite field, and the "
                      "Pippenger Spencer theorem on nearly perfect packings. {res}Then at every point of the circle, "
                      "at most one contribution survives, so the size is at most about root N, {ms}while the "
                      "coefficients, real numbers between minus one and one, have mean square nearly one. So almost "
                      "all of them are already close to plus or minus one.") as s:
            self.play(Write(hdr))
            s.wait_until("blk")
            self.play(Create(ax), Create(cb_), FadeIn(bl), run_time=2)
            self.play(GrowFromCenter(br), FadeIn(brl))
            s.wait_until("pk")
            self.play(Create(circ), LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.05), run_time=3)
            self.play(FadeIn(al))
            s.wait_until("res")
            self.play(FadeIn(res[0]))
            s.wait_until("ms")
            self.play(FadeIn(res[1]))
        self.play(FadeOut(VGroup(hdr, ax, cb_, br, brl, bl, circ, arcs, al, res)))

        # ------------------------------------------------------------ proof 3: rounding, and the lower bound
        hdr = Tex("Round the last few coefficients with discrepancy theory", font_size=34, color=YELLOW_3B).to_edge(
            UP, buff=0.35)
        rng = np.random.default_rng(2)
        xk = np.where(np.cos(0.37 * np.arange(40) ** 2) >= 0, 1.0, -1.0)
        frac = rng.choice(40, 9, replace=False)
        xk[frac] = rng.uniform(-0.8, 0.8, 9)
        sg = np.where(xk >= 0, 1.0, -1.0)
        sg[frac] = np.where(rng.random(9) < 0.5, -1.0, 1.0)
        b0 = self.bars(xk, 10, 2.4).move_to(UP * 1.3)
        b1 = self.bars(sg, 10, 2.4).move_to(UP * 1.3)
        marks = VGroup(*[Triangle(color=YELLOW_3B, fill_opacity=1).scale(0.07).rotate(PI).move_to(
            b0[i].get_center() * RIGHT + UP * 2.85) for i in frac])
        bl0 = Tex(r"almost-sign real coefficients (schematic); fractional ones marked", font_size=28).next_to(
            b0, DOWN, buff=0.35)
        rows = VGroup(
            Tex(r"partial coloring (Spencer; Lovett--Meka): choose signs so that", font_size=30),
            MathTex(r"\max_{|z|=1}\Big|\sum_k(\varepsilon_k-x_k)z^k\Big|\ \le\ C\Big(1+\sqrt{\mu\log(80N/\mu)}\Big)"
                    r"=o(\sqrt N)", font_size=34),
            Tex(r"$\mu$ = total distance of the $x_k$ from $\pm1$, which is small", font_size=28, color=GREY_A),
            Tex(r"Lower bound (Oct.\ 5 manuscript): constant-modulus waves, joined smoothly", font_size=28,
                color=TEAL_3B),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.say("Finally, round. {r}The few coefficients that are not yet signs are rounded using discrepancy "
                      f"theory, the partial coloring method of Spencer, in a form due to Lovett and {MEKA}. "
                      "{b}The signs are chosen so that the polynomial changes by only a small fraction of root N, "
                      "everywhere on the circle at once. {lo}That gives the upper bound. The October manuscript adds "
                      "the matching lower bound, building waves of constant size and joining them smoothly across "
                      "the gaps, so the polynomial never dips.") as s:
            self.play(Write(hdr), FadeIn(b0), FadeIn(bl0))
            self.play(FadeIn(marks))
            s.wait_until("r")
            self.play(FadeIn(rows[0]))
            s.wait_until("b")
            self.play(Transform(b0, b1), FadeOut(marks), run_time=1.5)
            self.play(Write(rows[1]), FadeIn(rows[2]), run_time=2)
            s.wait_until("lo")
            self.play(FadeIn(rows[3]))
        self.play(FadeOut(VGroup(hdr, b0, bl0, rows)))

        # ------------------------------------------------------------ closing
        card = status_card(
            [r"$\pm1$ polynomials with $(1-\varepsilon)\sqrt N\le|p|\le(1+\varepsilon)\sqrt N$ on $|z|=1$, all large $N$",
             r"Merit factors $\to\infty$: Turyn's conjecture disproved",
             r"Lean: upper bound $(1+\eta)\sqrt N$ formalized; two-sided bound not yet"],
            False, r"\emph{Ultraflat real Littlewood polynomials} and companions (Sept.--Oct.\ 2026)")
        with self.say("What has been checked? The upper bound, at most one plus eta times root N at every large "
                      "length, has been formalized in Lean, and it already implies unbounded merit factors by a one "
                      "line inequality. {c}The two sided ultraflat bound, from the October manuscript, has not been "
                      "formalized, and awaits expert checking.") as s:
            self.play(FadeIn(card[0]), FadeIn(card[1]), run_time=2)
            s.wait_until("c")
            self.play(FadeIn(card[2:]), run_time=1.5)
        self.wait(2)
