"""Scene 2 - "Why": the contrastive mechanism.

Companion visualization for the PUBLISHED paper:
  Arrighi, Belloni, Gallet, Gentile, Lippi, Zullich,
  "On the Properties of Feature Attribution for Supervised Contrastive Learning",
  XAI World Conference 2026.

This scene is a SCHEMATIC illustration of the mechanism narrative: contrastive
learning pulls same-class embeddings together and pushes different-class clusters
apart, producing a well-clustered embedding space; a thin linear probe (f_head)
makes Grad-CAM possible for CL models; that geometry yields better saliency maps.

The dot cloud is illustrative. Every textual takeaway is imported verbatim from
results_data (TAKEAWAYS[1], TAKEAWAYS[2]); no metric value is invented.
"""

import numpy as np
from manim import (
    Scene,
    Text,
    Dot,
    Arrow,
    Line,
    Circle,
    VGroup,
    SurroundingRectangle,
    Create,
    Write,
    FadeIn,
    FadeOut,
    GrowArrow,
    Transform,
    Indicate,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    BOLD,
    WHITE,
    GREY_B,
    rate_functions,
)

from results_data import OBJ_COLOR, OBJ_LONG, TAKEAWAYS

# Class accent colors borrowed from the objective palette (used as class identities
# here, purely for visual distinction). SCL is the winner color; that is the loss
# whose geometry we are illustrating.
CLASS_A_COLOR = OBJ_COLOR["SCL"]  # teal-green
CLASS_B_COLOR = OBJ_COLOR["TL"]   # amber
PROBE_COLOR = "#e6e6e6"


class TheMechanism(Scene):
    def construct(self):
        self.camera.background_color = "#11141a"

        rng = np.random.default_rng(7)

        # ---------- Title ----------
        title = Text(
            "Why contrastive learning helps",
            weight=BOLD,
            color=WHITE,
            font_size=40,
        ).to_edge(UP, buff=0.35)
        subtitle = Text(
            "the embedding geometry behind better saliency maps",
            color=GREY_B,
            font_size=22,
        ).next_to(title, DOWN, buff=0.16)
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(subtitle, shift=DOWN * 0.15), run_time=0.7)

        # ---------- Stage layout ----------
        # Symmetric, horizontal layout so "pull together / push apart" reads cleanly.
        # Everything stays inside [-7,7]x[-4,4]. Three beats:
        #   loose (overlapping near center) -> pull (each class contracts to its center)
        #   -> push (the two tight clusters slide apart, left vs right).
        stage_center = np.array([0.0, -0.55, 0.0])

        # Loose (CE) cluster centers: close together near the middle, so they overlap.
        loose_a_center = stage_center + np.array([-0.85, 0.0, 0.0])
        loose_b_center = stage_center + np.array([0.85, 0.0, 0.0])

        # Tight-but-still-central (after PULL): same horizontal offset, just contracted.
        pull_a_center = loose_a_center
        pull_b_center = loose_b_center

        # Pushed-apart centers (after PUSH): far to the left / right, same height.
        tight_a_center = stage_center + np.array([-3.2, 0.0, 0.0])
        tight_b_center = stage_center + np.array([3.2, 0.0, 0.0])

        n_per_class = 11

        def sample_cluster(center, spread, n):
            pts = []
            for _ in range(n):
                ang = rng.uniform(0, 2 * np.pi)
                r = spread * np.sqrt(rng.uniform(0, 1))
                pts.append(center + np.array([r * np.cos(ang), r * np.sin(ang), 0.0]))
            return pts

        # Loose clouds overlap in the middle (wide spread). The pulled/pushed targets
        # reuse the SAME per-dot angular layout, just contracted around a moving center,
        # so each dot's motion is legible (contract in place, then translate sideways).
        unit_a = sample_cluster(np.array([0.0, 0.0, 0.0]), 1.0, n_per_class)
        unit_b = sample_cluster(np.array([0.0, 0.0, 0.0]), 1.0, n_per_class)

        loose_a = [loose_a_center + 1.35 * u for u in unit_a]
        loose_b = [loose_b_center + 1.35 * u for u in unit_b]
        pull_a = [pull_a_center + 0.55 * u for u in unit_a]
        pull_b = [pull_b_center + 0.55 * u for u in unit_b]
        tight_a = [tight_a_center + 0.55 * u for u in unit_a]
        tight_b = [tight_b_center + 0.55 * u for u in unit_b]

        dots_a = VGroup(*[
            Dot(p, radius=0.085, color=CLASS_A_COLOR, fill_opacity=0.95)
            for p in loose_a
        ])
        dots_b = VGroup(*[
            Dot(p, radius=0.085, color=CLASS_B_COLOR, fill_opacity=0.95)
            for p in loose_b
        ])

        # Legend (top-left, well clear of clusters).
        legend = VGroup(
            VGroup(
                Dot(radius=0.085, color=CLASS_A_COLOR),
                Text("class A", color=GREY_B, font_size=20),
            ).arrange(RIGHT, buff=0.18),
            VGroup(
                Dot(radius=0.085, color=CLASS_B_COLOR),
                Text("class B", color=GREY_B, font_size=20),
            ).arrange(RIGHT, buff=0.18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        legend.to_corner(LEFT + DOWN, buff=0.5).shift(UP * 0.95)

        # ---------- Phase label (CE) ----------
        phase_label = Text(
            f"Cross-Entropy ({OBJ_LONG['CE']})",
            color=OBJ_COLOR["CE"],
            weight=BOLD,
            font_size=26,
        ).to_edge(UP, buff=0.35).shift(DOWN * 1.55)
        phase_note = Text(
            "embeddings: loosely separated, clusters overlap",
            color=GREY_B,
            font_size=20,
        ).next_to(phase_label, DOWN, buff=0.12)

        self.play(
            FadeIn(dots_a, lag_ratio=0.05),
            FadeIn(dots_b, lag_ratio=0.05),
            FadeIn(legend),
            run_time=1.2,
        )
        self.play(FadeIn(phase_label), FadeIn(phase_note), run_time=0.7)
        self.wait(0.8)

        # ---------- Transition to SCL phase label ----------
        new_phase_label = Text(
            "Supervised Contrastive Loss",
            color=OBJ_COLOR["SCL"],
            weight=BOLD,
            font_size=26,
        ).to_edge(UP, buff=0.35).shift(DOWN * 1.55)
        new_phase_note = Text(
            "same-class points pull together, different classes push apart",
            color=GREY_B,
            font_size=20,
        ).next_to(new_phase_label, DOWN, buff=0.12)
        self.play(
            Transform(phase_label, new_phase_label),
            Transform(phase_note, new_phase_note),
            run_time=0.8,
        )

        # A reusable place for the beat word: BELOW the clusters (which sit around
        # y in [-1.7, +0.6]) and above the legend, so it never collides with the
        # header text or the dots.
        beat_word_pos = np.array([0.0, -2.55, 0.0])

        # ============ BEAT 1: PULL (each class contracts to its own center) ============
        # Short inward arrows from each loose dot toward its contracted position.
        pull_arrows = VGroup()
        for d, target in zip(list(dots_a) + list(dots_b), pull_a + pull_b):
            start = d.get_center()
            end = np.array(target)
            if np.linalg.norm(end - start) > 0.18:
                pull_arrows.add(
                    Arrow(
                        start, end, buff=0.04,
                        stroke_width=2.5, max_tip_length_to_length_ratio=0.25,
                        color=GREY_B,
                    )
                )

        pull_word = Text("PULL  together", color=CLASS_A_COLOR, weight=BOLD, font_size=24)
        pull_word.move_to(beat_word_pos)

        self.play(
            FadeIn(pull_word, scale=0.7),
            *[GrowArrow(a) for a in pull_arrows],
            run_time=1.0,
        )
        # Dots contract in place (centers stay put), so PULL reads as tightening.
        self.play(
            *[d.animate.move_to(t) for d, t in zip(dots_a, pull_a)],
            *[d.animate.move_to(t) for d, t in zip(dots_b, pull_b)],
            FadeOut(pull_arrows),
            run_time=1.2,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.play(FadeOut(pull_word), run_time=0.4)

        # ============ BEAT 2: PUSH (the two tight clusters slide apart) ============
        a_now = dots_a.get_center()
        b_now = dots_b.get_center()
        # Big horizontal push arrows pointing outward from the gap between clusters.
        gap = 0.5 * (a_now + b_now)
        push_a = Arrow(
            gap + LEFT * 0.35, gap + LEFT * 2.0, buff=0.0,
            stroke_width=7, max_tip_length_to_length_ratio=0.3, color=WHITE,
        )
        push_b = Arrow(
            gap + RIGHT * 0.35, gap + RIGHT * 2.0, buff=0.0,
            stroke_width=7, max_tip_length_to_length_ratio=0.3, color=WHITE,
        )
        push_word = Text("PUSH  apart", color=WHITE, weight=BOLD, font_size=24)
        push_word.move_to(beat_word_pos)

        self.play(
            FadeIn(push_word, scale=0.7),
            GrowArrow(push_a),
            GrowArrow(push_b),
            run_time=0.8,
        )
        # The clusters actually translate outward, following the push arrows.
        self.play(
            *[d.animate.move_to(t) for d, t in zip(dots_a, tight_a)],
            *[d.animate.move_to(t) for d, t in zip(dots_b, tight_b)],
            push_a.animate.shift(LEFT * 1.3),
            push_b.animate.shift(RIGHT * 1.3),
            run_time=1.3,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.play(FadeOut(push_a), FadeOut(push_b), FadeOut(push_word), run_time=0.4)

        # ---------- Highlight the well-clustered geometry ----------
        ring_a = Circle(radius=0.95, color=CLASS_A_COLOR, stroke_width=2.5)
        ring_a.move_to(dots_a.get_center())
        ring_b = Circle(radius=0.95, color=CLASS_B_COLOR, stroke_width=2.5)
        ring_b.move_to(dots_b.get_center())
        self.play(Create(ring_a), Create(ring_b), run_time=0.8)

        # ---------- Linear probe (f_head) ----------
        # A thin vertical separating line between the two (now horizontal) clusters ->
        # the f_head that makes Grad-CAM possible for contrastive models.
        mid = 0.5 * (dots_a.get_center() + dots_b.get_center())
        probe = Line(
            mid + UP * 1.7,
            mid + DOWN * 1.7,
            color=PROBE_COLOR,
            stroke_width=3.5,
        )
        probe_label = Text(
            "linear probe  f_head  (enables Grad-CAM for CL)",
            color=PROBE_COLOR,
            font_size=20,
        )
        # Place label below the probe, kept inside frame.
        probe_label.next_to(probe, DOWN, buff=0.2)
        if probe_label.get_bottom()[1] < -3.7:
            probe_label.move_to(np.array([0.0, -3.5, 0.0]))

        self.play(Create(probe), run_time=0.8)
        self.play(FadeIn(probe_label, shift=UP * 0.1), run_time=0.6)
        self.play(Indicate(probe, color=PROBE_COLOR, scale_factor=1.05), run_time=0.7)

        # ---------- Takeaways (verbatim from results_data) ----------
        take1 = Text(TAKEAWAYS[1], color=WHITE, font_size=22)
        take2 = Text(TAKEAWAYS[2], color=OBJ_COLOR["SCL"], font_size=22)
        takeaways = VGroup(take1, take2).arrange(DOWN, buff=0.14)
        takeaways.to_edge(DOWN, buff=0.32)

        # Make room: nudge the probe label up slightly if it would collide.
        self.play(
            FadeOut(probe_label),
            run_time=0.4,
        )
        self.play(FadeIn(take1, shift=UP * 0.12), run_time=0.9)
        self.play(FadeIn(take2, shift=UP * 0.12), run_time=0.9)

        # Gentle final emphasis on the geometry.
        self.play(
            Indicate(ring_a, color=CLASS_A_COLOR, scale_factor=1.08),
            Indicate(ring_b, color=CLASS_B_COLOR, scale_factor=1.08),
            run_time=1.0,
        )
        self.wait(1.4)
