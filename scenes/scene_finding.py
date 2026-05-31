"""Scene 1 — "The Finding" (the hook).

Companion visualization for the published paper:
  Arrighi, Belloni, Gallet, Gentile, Lippi, Zullich,
  "On the Properties of Feature Attribution for Supervised Contrastive Learning",
  XAI World Conference 2026.

One input image, three Grad-CAM saliency overlays (CE / SCL / TL), drawn as
SCHEMATIC heatmaps that honestly reflect the reported qualitative trend
(CE diffuse/wide, SCL compact/focused, TL medium). All numeric content
(accuracy) is imported verbatim from results_data — never hardcoded.

Render: manim -pql scenes/scene_finding.py TheFinding   (720p30 -> use -qm for 720p)
"""

from manim import (
    Scene, VGroup, Text, RoundedRectangle, Rectangle, Polygon, Circle, Dot,
    FadeIn, FadeOut, Write, Create, GrowFromCenter,
    UP, DOWN, LEFT, RIGHT, ORIGIN, BOLD, WHITE, GREY_B,
    ManimColor,
)
import numpy as np

from results_data import (
    OBJ_COLOR, OBJ_LONG, OBJECTIVES, ACCURACY, TAKEAWAYS,
)

BG = "#11141a"


class TheFinding(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ---------------------------------------------------------------
        # Title
        # ---------------------------------------------------------------
        title = Text(
            "The Finding", weight=BOLD, color=WHITE, font_size=44
        ).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.9)

        # ---------------------------------------------------------------
        # Helper: a stylized "bird" schematic object, centered at ORIGIN,
        # scaled to fit a unit-ish footprint. Returns a VGroup.
        # ---------------------------------------------------------------
        def make_bird(body_color="#cdd6e2"):
            # body (teardrop-ish polygon)
            body = Polygon(
                [-0.55, -0.05, 0], [-0.15, 0.35, 0], [0.35, 0.30, 0],
                [0.55, 0.0, 0], [0.30, -0.35, 0], [-0.30, -0.35, 0],
                color=body_color, fill_opacity=1.0, stroke_width=0,
            )
            # head
            head = Circle(radius=0.22, color=body_color,
                          fill_opacity=1.0, stroke_width=0).move_to([0.42, 0.22, 0])
            # beak
            beak = Polygon(
                [0.60, 0.26, 0], [0.86, 0.18, 0], [0.60, 0.10, 0],
                color="#e0a458", fill_opacity=1.0, stroke_width=0,
            )
            # wing accent (slightly darker)
            wing = Polygon(
                [-0.35, 0.05, 0], [0.05, 0.20, 0], [0.10, -0.10, 0],
                [-0.25, -0.20, 0],
                color="#aab4c2", fill_opacity=1.0, stroke_width=0,
            )
            # tail
            tail = Polygon(
                [-0.55, -0.05, 0], [-0.90, 0.12, 0], [-0.88, -0.18, 0],
                color=body_color, fill_opacity=1.0, stroke_width=0,
            )
            # eye
            eye = Dot(point=[0.50, 0.28, 0], radius=0.035, color=BG)
            return VGroup(tail, body, wing, head, beak, eye)

        # ---------------------------------------------------------------
        # Helper: schematic Grad-CAM heatmap as concentric translucent
        # blobs. `spread` controls diffuseness, `cx,cy` the focus point.
        #   - CE  : wide / diffuse  (large spread, off the object)
        #   - SCL : compact / focused (small spread, on the object)
        #   - TL  : medium
        # Drawn as nested circles fading warm-to-hot.
        # ---------------------------------------------------------------
        def make_heatmap(spread, cx, cy, base_color):
            col = ManimColor(base_color)
            g = VGroup()
            n = 5
            for i in range(n):
                t = i / (n - 1)            # 0 outer -> 1 inner
                r = spread * (1.0 - 0.78 * t)
                blob = Circle(
                    radius=max(r, 0.05),
                    color=col,
                    fill_opacity=0.16 + 0.30 * t,
                    stroke_width=0,
                ).move_to([cx, cy, 0])
                g.add(blob)
            return g

        # ---------------------------------------------------------------
        # Build three panels (CE / SCL / TL) side by side.
        # Panel frame is a rounded rect; inside: bird + heatmap overlay.
        # ---------------------------------------------------------------
        panel_w, panel_h = 3.35, 3.35
        xs = {"CE": -4.2, "SCL": 0.0, "TL": 4.2}
        panel_cy = -0.15

        # per-objective schematic heatmap parameters (honest trend)
        hm_params = {
            # (spread, focus_dx, focus_dy)  dx/dy relative to bird center
            "CE":  (1.45, -0.05, 0.10),   # wide & diffuse, slightly off-object
            "SCL": (0.70, 0.05, 0.05),    # compact, centered on the body/head
            "TL":  (1.05, -0.25, -0.05),  # medium, a bit scattered
        }

        panels = {}
        frames = {}
        labels = {}
        acc_labels = {}
        birds = {}
        heatmaps = {}

        for obj in OBJECTIVES:
            cx = xs[obj]
            col = OBJ_COLOR[obj]

            frame = RoundedRectangle(
                width=panel_w, height=panel_h, corner_radius=0.14,
                stroke_color=col, stroke_width=3.0,
                fill_color="#161a22", fill_opacity=1.0,
            ).move_to([cx, panel_cy, 0])

            # objective short label (top of panel)
            lab = Text(obj, weight=BOLD, color=col, font_size=30)
            lab.next_to(frame.get_top(), DOWN, buff=0.16)

            # long name (small, under short label)
            long = Text(OBJ_LONG[obj], color=GREY_B, font_size=13)
            long.next_to(lab, DOWN, buff=0.06)

            # bird inside panel, scaled and positioned a touch lower
            bird = make_bird()
            bird.scale(1.05)
            bird.move_to([cx, panel_cy - 0.10, 0])

            # accuracy readout (CIFAR10, real number from results_data)
            acc = ACCURACY["CIFAR10"][obj]
            acc_lab = Text(f"acc {acc:.2f}%", color=GREY_B, font_size=15)
            acc_lab.next_to(frame.get_bottom(), UP, buff=0.14)

            panels[obj] = VGroup(frame, lab, long, bird, acc_lab)
            frames[obj] = frame
            labels[obj] = VGroup(lab, long)
            acc_labels[obj] = acc_lab
            birds[obj] = bird

        # ---------------------------------------------------------------
        # Reveal 1: the SAME input image in all three panels (frames + birds)
        # ---------------------------------------------------------------
        self.play(
            *[Create(frames[o]) for o in OBJECTIVES],
            run_time=1.1,
        )
        self.play(
            *[FadeIn(birds[o], shift=UP * 0.12) for o in OBJECTIVES],
            run_time=1.0,
        )
        self.play(
            *[FadeIn(labels[o]) for o in OBJECTIVES],
            *[FadeIn(acc_labels[o]) for o in OBJECTIVES],
            run_time=0.8,
        )
        self.wait(0.4)

        # ---------------------------------------------------------------
        # Reveal 2: overlay the schematic Grad-CAM heatmaps, staged
        # ---------------------------------------------------------------
        for obj in OBJECTIVES:
            spread, dx, dy = hm_params[obj]
            bc = birds[obj].get_center()
            hm = make_heatmap(spread, bc[0] + dx, bc[1] + dy, OBJ_COLOR[obj])
            # clip-ish: scale so the widest blob stays within the panel
            # (heatmaps are drawn after birds so they sit on top, translucent)
            heatmaps[obj] = hm

        # "Grad-CAM" tool tag, top-center between title and panels
        tool_tag = Text("Grad-CAM saliency overlays", color=GREY_B, font_size=18)
        tool_tag.next_to(title, DOWN, buff=0.12)
        self.play(FadeIn(tool_tag), run_time=0.5)

        self.play(GrowFromCenter(heatmaps["CE"]), run_time=0.9)
        self.play(GrowFromCenter(heatmaps["SCL"]), run_time=0.9)
        self.play(GrowFromCenter(heatmaps["TL"]), run_time=0.9)

        # bring birds + labels back to front (so the object stays visible
        # under the translucent heat). Re-add on top.
        self.play(
            *[birds[o].animate.set_opacity(1.0) for o in OBJECTIVES],
            run_time=0.3,
        )
        for o in OBJECTIVES:
            self.add(birds[o], labels[o])
        self.wait(0.4)

        # small "schematic" disclaimer for the heatmaps
        schematic = Text(
            "heatmaps: schematic illustration of the reported trend "
            "(bars/numbers are real)",
            color="#6f7785", font_size=13,
        )
        schematic.next_to(VGroup(frames["CE"], frames["TL"]), DOWN, buff=0.18)
        # keep within frame
        if schematic.get_bottom()[1] < -3.55:
            schematic.shift(UP * (-3.55 - schematic.get_bottom()[1]))
        self.play(FadeIn(schematic), run_time=0.5)
        self.wait(0.6)

        # ---------------------------------------------------------------
        # Caption (the hook) + thesis from TAKEAWAYS[0]
        # ---------------------------------------------------------------
        caption = Text(
            "Same image. Same architecture. Same ~95% accuracy.\n"
            "Different training loss → different explanation quality.",
            color=WHITE, font_size=20, line_spacing=0.8,
        )
        caption.next_to(schematic, DOWN, buff=0.16)
        if caption.get_bottom()[1] < -3.9:
            caption.shift(UP * (-3.9 - caption.get_bottom()[1]))

        # fade the disclaimer slightly and bring up the caption block
        self.play(
            schematic.animate.set_opacity(0.55),
            FadeIn(caption, shift=UP * 0.1),
            run_time=1.0,
        )
        self.wait(1.0)

        # Thesis line: TAKEAWAYS[0], emphasized, replaces the caption focus
        thesis = Text(
            TAKEAWAYS[0],
            weight=BOLD, color=OBJ_COLOR["SCL"], font_size=24,
        )
        thesis.move_to(caption.get_center())
        self.play(
            FadeOut(caption, shift=DOWN * 0.1),
            run_time=0.5,
        )
        self.play(Write(thesis), run_time=1.2)
        self.wait(1.6)

        # gentle outro
        self.play(
            *[FadeOut(m) for m in [
                title, tool_tag, schematic, thesis,
                *[panels[o] for o in OBJECTIVES],
                *[heatmaps[o] for o in OBJECTIVES],
            ]],
            run_time=1.0,
        )
        self.wait(0.3)
