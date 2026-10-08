"""Shared look for the series: 3b1b-style palette, title and closing cards."""
from manim import *

config.background_color = "#0b0b0e"

# 3b1b-ish palette
BLUE_3B = "#58C4DD"
BROWN_3B = "#9C7B57"
YELLOW_3B = "#FFE066"
TEAL_3B = "#5CD0B3"
RED_3B = "#FC6255"
GREEN_3B = "#83C167"
PURPLE_3B = "#9A72AC"
GREY_3B = "#888888"
ORANGE_3B = "#FF9F43"

Tex.set_default(font_size=40)
MathTex.set_default(font_size=44)


def T(s, **kw):
    """Plain prose line in Computer Modern."""
    return Tex(s, **kw)


def title_card(scene, number, title, subtitle, seg_time=None):
    """Opening card. Returns the group so callers can fade it."""
    tag = Tex(rf"OpenAI math catalogue \textperiodcentered{{}} result {number}", font_size=28, color=GREY_3B)
    head = Tex(title, font_size=60)
    sub = Tex(subtitle, font_size=32, color=BLUE_3B)
    grp = VGroup(tag, head, sub).arrange(DOWN, buff=0.45)
    if grp.width > 12.5:
        grp.scale_to_fit_width(12.5)
    return grp


def status_card(lines, formalized, paper):
    """Closing card listing what is claimed and how verified it is."""
    head = Tex("The claim", font_size=48, color=YELLOW_3B)
    body = VGroup(*[Tex(l, font_size=32) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    if formalized:
        badge = Tex(r"Main theorem formalized in Lean \checkmark", font_size=32, color=GREEN_3B)
    else:
        badge = Tex(r"Not yet formalized \textemdash{} awaiting expert verification", font_size=32, color=ORANGE_3B)
    src = Tex(r"\texttt{github.com/openai/math}", font_size=26, color=GREY_3B)
    ref = Tex(paper, font_size=26, color=GREY_3B)
    grp = VGroup(head, body, badge, VGroup(src, ref).arrange(DOWN, buff=0.12)).arrange(DOWN, buff=0.5)
    if grp.width > 12.5:
        grp.scale_to_fit_width(12.5)
    return grp


def caption_box(mob, color=GREY_3B, buff=0.2):
    return SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.1, stroke_width=2)
