"""SCENE 4 - "Five Facets, Honestly" (the integrity scene).

Shows the five Co-12 facets as a row of cards, then stamps an honest verdict
on each: SCL wins Faithfulness / Continuity / Complexity; CE wins Contrastivity;
Coherence is inconclusive (high variance). All numbers/labels come from
results_data; nothing is invented.
"""

from manim import (
    Scene,
    Text,
    RoundedRectangle,
    VGroup,
    Line,
    Circle,
    FadeIn,
    FadeOut,
    Write,
    Create,
    GrowFromCenter,
    Indicate,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    WHITE,
    BOLD,
)

from results_data import (
    FACETS,
    OBJ_COLOR,
    SCL_WINS,
    CE_WINS,
    INCONCLUSIVE,
    COHERENCE_INCONCLUSIVE,
    TAKEAWAYS,
)

GREEN_OK = OBJ_COLOR["SCL"]   # teal-green = SCL the winner
AMBER = OBJ_COLOR["TL"]       # amber accent for the honest "CE leads here" stamp
GRAY_Q = "#7a828f"            # neutral gray for the inconclusive verdict


class TheFacets(Scene):
    def construct(self):
        self.camera.background_color = "#11141a"

        # ---- Title ----
        title = Text("Five Facets, Honestly", weight=BOLD, color=WHITE)
        title.scale(0.95).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=1.0)

        # ---- Build the five facet cards in a row ----
        n = len(FACETS)
        card_w = 2.45
        card_h = 4.0
        gap = 0.18
        total_w = n * card_w + (n - 1) * gap
        x0 = -total_w / 2 + card_w / 2

        # Verdict lookup: maps facet name -> ("ok" | "ce" | "inc")
        def verdict_for(name):
            if name in SCL_WINS:
                return "ok"
            if name in CE_WINS:
                return "ce"
            if name in INCONCLUSIVE:
                return "inc"
            return "inc"

        cards = []
        verdict_marks = []

        for i, (name, meaning, metric) in enumerate(FACETS):
            v = verdict_for(name)
            cx = x0 + i * (card_w + gap)

            card = RoundedRectangle(
                width=card_w,
                height=card_h,
                corner_radius=0.14,
                stroke_color="#39414e",
                stroke_width=2.0,
                fill_color="#1a1e26",
                fill_opacity=1.0,
            )
            card.move_to([cx, -0.35, 0])

            # Facet name (header)
            facet_name = Text(name, weight=BOLD, color=WHITE).scale(0.40)
            facet_name.move_to(card.get_top() + DOWN * 0.42)

            # thin divider under the name
            div = Line(
                card.get_left() + RIGHT * 0.18,
                card.get_right() + LEFT * 0.18,
                stroke_color="#39414e",
                stroke_width=1.2,
            )
            div.move_to([cx, card.get_top()[1] - 0.72, 0])

            # one-line meaning, wrapped to the card width at a readable size
            meaning_txt = Text(
                meaning,
                color="#dde3ec",
                line_spacing=0.8,
                width=card_w - 0.30,
            )
            # cap the height so long meanings don't overrun the metric chip
            if meaning_txt.height > 1.1:
                meaning_txt.scale_to_fit_height(1.1)
            meaning_txt.move_to([cx, 0.5, 0])

            # metric chip
            metric_lbl = Text(metric, weight=BOLD, color="#aeb6c2").scale(0.30)
            metric_box = RoundedRectangle(
                width=metric_lbl.width + 0.30,
                height=0.42,
                corner_radius=0.10,
                stroke_color="#39414e",
                stroke_width=1.2,
                fill_color="#222733",
                fill_opacity=1.0,
            )
            metric_grp = VGroup(metric_box, metric_lbl)
            metric_lbl.move_to(metric_box.get_center())
            metric_grp.move_to([cx, -0.85, 0])

            card_grp = VGroup(card, facet_name, div, meaning_txt, metric_grp)
            cards.append(card_grp)

            # ---- Build the verdict mark (revealed later) ----
            if v == "ok":
                color = GREEN_OK
                ring = Circle(radius=0.30, color=color, stroke_width=4.0)
                check = VGroup(
                    Line([-0.12, 0.0, 0], [-0.03, -0.11, 0], color=color, stroke_width=5),
                    Line([-0.03, -0.11, 0], [0.15, 0.13, 0], color=color, stroke_width=5),
                )
                glyph = VGroup(ring, check)
                vtext = Text("SCL wins", weight=BOLD, color=color).scale(0.30)
            elif v == "ce":
                color = AMBER
                ring = Circle(radius=0.30, color=color, stroke_width=4.0)
                bang = VGroup(
                    Line([0, 0.13, 0], [0, -0.05, 0], color=color, stroke_width=5),
                    Circle(radius=0.025, color=color, fill_color=color,
                           fill_opacity=1.0, stroke_width=0).move_to([0, -0.14, 0]),
                )
                glyph = VGroup(ring, bang)
                vtext = Text("SCL doesn't win", weight=BOLD, color=color).scale(0.28)
            else:  # inconclusive
                color = GRAY_Q
                ring = Circle(radius=0.30, color=color, stroke_width=4.0)
                q = Text("?", weight=BOLD, color=color).scale(0.42)
                q.move_to(ring.get_center())
                glyph = VGroup(ring, q)
                vtext = Text("inconclusive", weight=BOLD, color=color).scale(0.28)

            # place glyph + verdict text near the bottom of the card
            glyph.move_to([cx, -1.55, 0])
            vtext.move_to([cx, -2.02, 0])
            verdict_marks.append((v, color, VGroup(glyph, vtext)))

        cards_group = VGroup(*cards)

        # Reveal cards one-by-one
        self.play(
            *[FadeIn(c, shift=UP * 0.2) for c in cards],
            lag_ratio=0.12,
            run_time=2.6,
        )
        self.wait(0.4)

        # ---- Stamp verdicts ----
        # Order: the three SCL wins first, then the honest CE win, then inconclusive.
        order = []
        for idx, (name, _, _) in enumerate(FACETS):
            v = verdict_for(name)
            order.append((["ok", "ce", "inc"].index(v), idx))
        order.sort()

        for _, idx in order:
            v, color, mark = verdict_marks[idx]
            # highlight the card border in the verdict color, then stamp the glyph
            card_rect = cards[idx][0]
            self.play(
                card_rect.animate.set_stroke(color=color, width=3.0),
                GrowFromCenter(mark[0]),
                run_time=0.55,
            )
            self.play(Write(mark[1]), run_time=0.45)

        self.wait(0.4)

        # ---- Honest callout: coherence is inconclusive because of high variance ----
        coh_note = Text(
            "Coherence: " + COHERENCE_INCONCLUSIVE["note"],
            color=GRAY_Q,
        ).scale(0.34)
        coh_note.move_to([0, -3.05, 0])
        self.play(FadeIn(coh_note, shift=UP * 0.15), run_time=0.8)

        # briefly emphasize the inconclusive card
        for i, (name, _, _) in enumerate(FACETS):
            if verdict_for(name) == "inc":
                self.play(Indicate(cards[i][0], color=GRAY_Q, scale_factor=1.04),
                          run_time=0.8)
        self.wait(0.3)

        # ---- Bottom caption: the integrity takeaway ----
        # Fully remove the coherence note before writing the caption (no ghost overlap).
        self.play(FadeOut(coh_note, shift=DOWN * 0.1), run_time=0.4)
        self.remove(coh_note)

        caption = Text(TAKEAWAYS[4], weight=BOLD, color=WHITE).scale(0.40)
        if caption.width > 12.5:
            caption.scale(12.5 / caption.width)
        caption.move_to([0, -3.4, 0])
        self.play(Write(caption), run_time=1.6)
        self.wait(2.0)
