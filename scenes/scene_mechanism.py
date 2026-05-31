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
        # The dot cloud lives in a centered region; we keep everything in [-7,7]x[-4,4].
        stage_center = np.array([0.0, -0.35, 0.0])

        # Loose (CE) cluster centers: close together, overlapping-ish.
        loose_a_center = stage_center + np.array([-1.05, 0.55, 0.0])
        loose_b_center = stage_center + np.array([1.05, -0.55, 0.0])

        # Tight (SCL) cluster centers: pushed far apart.
        tight_a_center = stage_center + np.array([-2.75, 0.95, 0.0])
        tight_b_center = stage_center + np.array([2.75, -0.95, 0.0])

        n_per_class = 11

        def sample_cluster(center, spread, n):
            pts = []
            for _ in range(n):
                ang = rng.uniform(0, 2 * np.pi)
                r = spread * np.sqrt(rng.uniform(0, 1))
                pts.append(center + np.array([r * np.cos(ang), r * np.sin(ang), 0.0]))
            return pts

        loose_a = sample_cluster(loose_a_center, 1.15, n_per_class)
        loose_b = sample_cluster(loose_b_center, 1.15, n_per_class)
        tight_a = sample_cluster(tight_a_center, 0.55, n_per_class)
        tight_b = sample_cluster(tight_b_center, 0.55, n_per_class)

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
        legend.to_corner(LEFT + DOWN, buff=0.5).shift(UP * 0.2)

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
            f"Supervised Contrastive ({OBJ_LONG['SCL']})",
            color=OBJ_COLOR["SCL"],
            weight=BOLD,
            font_size=26,
        ).to_edge(UP, buff=0.35).shift(DOWN * 1.55)
        new_phase_note = Text(
            "pull same class together  -  push different classes apart",
            color=GREY_B,
            font_size=20,
        ).next_to(new_phase_label, DOWN, buff=0.12)
        self.play(
            Transform(phase_label, new_phase_label),
            Transform(phase_note, new_phase_note),
            run_time=0.8,
        )

        # ---------- PULL arrows (same class -> center) ----------
        pull_arrows_a = VGroup()
        for d, target in zip(dots_a, tight_a):
            start = d.get_center()
            end = np.array(target)
            if np.linalg.norm(end - start) > 0.25:
                pull_arrows_a.add(
                    Arrow(
                        start, end, buff=0.05,
                        stroke_width=3, max_tip_length_to_length_ratio=0.18,
                        color=CLASS_A_COLOR,
                    )
                )
        pull_arrows_b = VGroup()
        for d, target in zip(dots_b, tight_b):
            start = d.get_center()
            end = np.array(target)
            if np.linalg.norm(end - start) > 0.25:
                pull_arrows_b.add(
                    Arrow(
                        start, end, buff=0.05,
                        stroke_width=3, max_tip_length_to_length_ratio=0.18,
                        color=CLASS_B_COLOR,
                    )
                )

        pull_word = Text("pull", color=WHITE, weight=BOLD, font_size=22)
        pull_word.move_to(stage_center + np.array([0.0, 1.95, 0.0]))

        self.play(
            FadeIn(pull_word, scale=0.6),
            *[GrowArrow(a) for a in pull_arrows_a],
            *[GrowArrow(a) for a in pull_arrows_b],
            run_time=1.1,
        )

        # Move dots to tight clusters.
        move_anims = []
        for d, target in zip(dots_a, tight_a):
            move_anims.append(d.animate.move_to(target))
        for d, target in zip(dots_b, tight_b):
            move_anims.append(d.animate.move_to(target))
        self.play(
            *move_anims,
            FadeOut(pull_arrows_a),
            FadeOut(pull_arrows_b),
            FadeOut(pull_word),
            run_time=1.3,
            rate_func=rate_functions.ease_in_out_sine,
        )

        # ---------- PUSH arrows (clusters apart) ----------
        a_now = dots_a.get_center()
        b_now = dots_b.get_center()
        sep_dir = (a_now - b_now)
        sep_dir = sep_dir / (np.linalg.norm(sep_dir) + 1e-9)

        push_a = Arrow(
            a_now, a_now + sep_dir * 1.0, buff=0.1,
            stroke_width=6, color=WHITE,
        )
        push_b = Arrow(
            b_now, b_now - sep_dir * 1.0, buff=0.1,
            stroke_width=6, color=WHITE,
        )
        push_word = Text("push", color=WHITE, weight=BOLD, font_size=22)
        push_word.move_to(stage_center + np.array([0.0, 1.95, 0.0]))

        self.play(
            FadeIn(push_word, scale=0.6),
            GrowArrow(push_a),
            GrowArrow(push_b),
            run_time=0.9,
        )
        self.play(FadeOut(push_a), FadeOut(push_b), FadeOut(push_word), run_time=0.5)

        # ---------- Highlight the well-clustered geometry ----------
        ring_a = Circle(radius=0.95, color=CLASS_A_COLOR, stroke_width=2.5)
        ring_a.move_to(dots_a.get_center())
        ring_b = Circle(radius=0.95, color=CLASS_B_COLOR, stroke_width=2.5)
        ring_b.move_to(dots_b.get_center())
        self.play(Create(ring_a), Create(ring_b), run_time=0.8)

        # ---------- Linear probe (f_head) ----------
        # A thin separating line between the two clusters -> the f_head that makes
        # Grad-CAM possible for contrastive models.
        mid = 0.5 * (dots_a.get_center() + dots_b.get_center())
        perp = np.array([-sep_dir[1], sep_dir[0], 0.0])
        probe = Line(
            mid + perp * 2.2,
            mid - perp * 2.2,
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
