"""SCENE 3 - "The Scoreboard" (HERO).

Animated grouped bar chart of the three Grad-CAM metrics on CIFAR10 where the
direction of improvement is sharp:
  Faithfulness  (Pixel-Flipping AUC, lower better)
  Continuity    (SSIM, higher better)
  Complexity    (entropy CM, lower better)

Three bars per metric (CE / SCL / TL), real values labeled, with a per-metric
up/down arrow glyph showing which direction is better. Bar heights are
NORMALIZED per metric for legibility, but the PRINTED numbers are the true
published values from results_data. SCL (the winner) is highlighted with a glow
pulse on all three metrics. A compact accuracy strip proves comparable accuracy.

All bars/numbers are real (Table 4 / accuracy table of the paper). Nothing here
is schematic; this is the quantitative core.
"""

from manim import (
    Scene, Text, VGroup, Rectangle, RoundedRectangle, Line, Triangle,
    SurroundingRectangle, FadeIn, GrowFromEdge, Create, Write, Indicate,
    WHITE, BOLD, UP, DOWN, LEFT, RIGHT, DEGREES, there_and_back,
)

from results_data import OBJ_COLOR, OBJECTIVES, METRICS, ACCURACY, TAKEAWAYS


class TheScoreboard(Scene):
    def construct(self):
        self.camera.background_color = "#11141a"

        # ---------------------------------------------------------------
        # Title
        # ---------------------------------------------------------------
        title = Text("The Scoreboard", weight=BOLD, color=WHITE).scale(0.95)
        title.to_edge(UP, buff=0.35)
        subtitle = Text(
            "Grad-CAM explanation quality on CIFAR10",
            color="#aeb6c2",
        ).scale(0.42)
        subtitle.next_to(title, DOWN, buff=0.12)
        scalenote = Text(
            "mean ± std over 5 runs · each metric on its own axis (note the tick labels)",
            color="#6f7785",
        ).scale(0.30)
        scalenote.next_to(subtitle, DOWN, buff=0.08)
        self.play(Write(title), run_time=0.9)
        self.play(FadeIn(subtitle, shift=DOWN * 0.1), run_time=0.6)
        self.play(FadeIn(scalenote), run_time=0.4)

        # ---------------------------------------------------------------
        # Chart geometry
        # ---------------------------------------------------------------
        # The three "sharp" metrics SCL wins on.
        metric_names = ["Faithfulness", "Continuity", "Complexity"]

        baseline_y = -2.35           # y of bar bases / x-axis
        max_bar_h = 2.05             # plot height for each per-group axis
        group_centers_x = [-4.2, 0.0, 4.2]
        bar_w = 0.58
        gap = 0.12                   # gap between bars in a group

        # baseline axis line
        axis = Line(
            [-6.4, baseline_y, 0], [6.4, baseline_y, 0],
            color="#3a4150", stroke_width=2,
        )
        self.play(FadeIn(axis), run_time=0.4)

        # ---- Honest per-group scaling --------------------------------------
        # The three metrics have very different natural ranges (PF~0.3, SSIM~0.57,
        # entropy~6.7), so each group gets its OWN y-axis. To keep bars TRUE TO
        # SCALE we map a per-group [floor, ceil] window linearly to [0, max_bar_h].
        # The window is chosen around the data (incl. error bars) with a small pad,
        # and BOTH endpoints are printed as tick labels next to each group, so the
        # reader can see the axis does not start at zero -- the heights then encode
        # real proportional differences rather than a min-max stretch.
        def group_window(vals, stds):
            lo = min(v - s for v, s in zip(vals, stds))
            hi = max(v + s for v, s in zip(vals, stds))
            span = max(hi - lo, 1e-6)
            pad = 0.35 * span
            floor = lo - pad
            ceil = hi + pad
            return floor, ceil

        def to_h(v, floor, ceil):
            return (v - floor) / (ceil - floor) * max_bar_h

        bar_groups = {}     # metric -> list of Rectangle (CE, SCL, TL order)
        value_labels = {}   # metric -> list of Text
        obj_labels = {}     # metric -> list of Text (CE/SCL/TL under bars)
        err_bars = {}       # metric -> list of VGroup (error-bar whisker+caps)
        metric_titles = {}
        arrow_glyphs = {}
        axis_ticks = {}     # metric -> VGroup(floor/ceil tick labels + ticks)

        for gi, metric in enumerate(metric_names):
            md = METRICS[metric]
            vals = [md["CIFAR10"][o] for o in OBJECTIVES]
            stds = [md["std_CIFAR10"][o] for o in OBJECTIVES]
            floor, ceil = group_window(vals, stds)
            heights = [to_h(v, floor, ceil) for v in vals]
            cx = group_centers_x[gi]

            # bar x-positions for the 3 objectives, centered on cx
            total_w = 3 * bar_w + 2 * gap
            x0 = cx - total_w / 2 + bar_w / 2
            xs = [x0 + i * (bar_w + gap) for i in range(3)]

            bars = []
            vlabels = []
            olabels = []
            ebars = []
            for i, obj in enumerate(OBJECTIVES):
                h = heights[i]
                bar = Rectangle(
                    width=bar_w, height=h,
                    fill_color=OBJ_COLOR[obj], fill_opacity=0.92,
                    stroke_color=OBJ_COLOR[obj], stroke_width=1.5,
                )
                # place so its bottom sits on the baseline
                bar.move_to([xs[i], baseline_y + h / 2, 0])
                bars.append(bar)

                # error bar: +/- 1 std, mapped through the same window, with caps
                s = stds[i]
                top_y = baseline_y + h
                if s > 1e-9:
                    dh = s / (ceil - floor) * max_bar_h
                    cap = bar_w * 0.32
                    whisker = Line([xs[i], top_y - dh, 0], [xs[i], top_y + dh, 0],
                                   color="#e9edf3", stroke_width=2.4)
                    cap_hi = Line([xs[i] - cap, top_y + dh, 0],
                                  [xs[i] + cap, top_y + dh, 0],
                                  color="#e9edf3", stroke_width=2.4)
                    cap_lo = Line([xs[i] - cap, top_y - dh, 0],
                                  [xs[i] + cap, top_y - dh, 0],
                                  color="#e9edf3", stroke_width=2.4)
                    ebars.append(VGroup(whisker, cap_hi, cap_lo))
                    label_anchor_y = top_y + dh
                else:
                    ebars.append(None)
                    label_anchor_y = top_y

                # true printed value (+/- std) above the bar / error cap
                txt = f"{vals[i]:.2f}" + (f"±{s:.2f}" if s > 1e-9 else "")
                vl = Text(txt, color=WHITE, weight=BOLD).scale(0.30)
                vl.move_to([xs[i], label_anchor_y + 0.22, 0])
                vlabels.append(vl)

                # objective name under the bar
                ol = Text(obj, color=OBJ_COLOR[obj], weight=BOLD).scale(0.34)
                ol.next_to([xs[i], baseline_y, 0], DOWN, buff=0.12)
                olabels.append(ol)

            bar_groups[metric] = bars
            value_labels[metric] = vlabels
            obj_labels[metric] = olabels
            err_bars[metric] = ebars

            # ---- per-group y-axis with floor/ceil tick labels --------------
            # short vertical axis just left of the group, with two ticks so the
            # non-zero baseline is explicit and honest.
            ax_x = x0 - bar_w / 2 - 0.30
            yax = Line([ax_x, baseline_y, 0], [ax_x, baseline_y + max_bar_h, 0],
                       color="#3a4150", stroke_width=1.6)
            tick_lo = Line([ax_x - 0.07, baseline_y, 0], [ax_x, baseline_y, 0],
                           color="#3a4150", stroke_width=1.6)
            tick_hi = Line([ax_x - 0.07, baseline_y + max_bar_h, 0],
                           [ax_x, baseline_y + max_bar_h, 0],
                           color="#3a4150", stroke_width=1.6)
            lo_lab = Text(f"{floor:.2f}", color="#6f7785").scale(0.24)
            lo_lab.next_to(tick_lo, LEFT, buff=0.06)
            hi_lab = Text(f"{ceil:.2f}", color="#6f7785").scale(0.24)
            hi_lab.next_to(tick_hi, LEFT, buff=0.06)
            axis_ticks[metric] = VGroup(yax, tick_lo, tick_hi, lo_lab, hi_lab)

            # metric title + unit + direction arrow, above the group
            top_y = baseline_y + max_bar_h + 1.30
            mtitle = Text(metric, color=WHITE, weight=BOLD).scale(0.46)
            mtitle.move_to([cx, top_y, 0])

            # direction-of-better arrow glyph
            arrow_up = (md["arrow"] == "up")
            tri = Triangle(
                color="#cfd6e0", fill_color="#cfd6e0", fill_opacity=1.0,
                stroke_width=0,
            ).scale(0.16)
            if not arrow_up:
                tri.rotate(180 * DEGREES)
            dir_txt = Text(
                f"({md['unit']},  {'higher' if arrow_up else 'lower'} = better)",
                color="#8b93a1",
            ).scale(0.30)
            glyph = VGroup(tri, dir_txt).arrange(RIGHT, buff=0.14)
            glyph.next_to(mtitle, DOWN, buff=0.12)

            metric_titles[metric] = mtitle
            arrow_glyphs[metric] = glyph

        # ---------------------------------------------------------------
        # Staged reveal: metric titles + arrows, then grow bars, then labels
        # ---------------------------------------------------------------
        self.play(
            *[FadeIn(metric_titles[m], shift=DOWN * 0.1) for m in metric_names],
            *[FadeIn(arrow_glyphs[m]) for m in metric_names],
            run_time=0.9,
        )

        # draw the per-group y-axes + tick labels (makes the non-zero scale explicit)
        self.play(
            *[Create(axis_ticks[m]) for m in metric_names],
            run_time=0.7,
        )

        # grow all bars from the baseline together
        grow_anims = []
        for m in metric_names:
            for bar in bar_groups[m]:
                grow_anims.append(GrowFromEdge(bar, UP))
        self.play(*grow_anims, run_time=1.3)

        # error bars (+/- 1 std over 5 runs) on top of the bars
        ebar_anims = [
            Create(eb) for m in metric_names for eb in err_bars[m] if eb is not None
        ]
        if ebar_anims:
            self.play(*ebar_anims, run_time=0.7)

        # objective labels under bars
        self.play(
            *[FadeIn(ol) for m in metric_names for ol in obj_labels[m]],
            run_time=0.5,
        )
        # true value labels on top
        self.play(
            *[FadeIn(vl, shift=UP * 0.06) for m in metric_names for vl in value_labels[m]],
            run_time=0.7,
        )

        # ---------------------------------------------------------------
        # Highlight SCL as the winner on each metric (glow pulse)
        # SCL is index 1 in OBJECTIVES.
        # ---------------------------------------------------------------
        scl_idx = OBJECTIVES.index("SCL")
        glow_rects = []
        for m in metric_names:
            scl_bar = bar_groups[m][scl_idx]
            glow = SurroundingRectangle(
                scl_bar, color=OBJ_COLOR["SCL"], buff=0.06,
                stroke_width=3.5, corner_radius=0.04,
            )
            glow_rects.append(glow)

        # add and pulse the winner highlights
        self.play(
            *[FadeIn(g) for g in glow_rects],
            *[Indicate(bar_groups[m][scl_idx], color=OBJ_COLOR["SCL"],
                       scale_factor=1.06) for m in metric_names],
            run_time=1.0,
        )
        # gentle pulse
        self.play(
            *[g.animate.set_stroke(width=6) for g in glow_rects],
            run_time=0.5, rate_func=there_and_back,
        )

        winner_tag = Text(
            "SCL wins all three", color=OBJ_COLOR["SCL"], weight=BOLD,
        ).scale(0.42)
        # park it in the open band between the Continuity group title and the
        # subtitle, horizontally centered so it cannot clip or overlap a column
        winner_tag.move_to([0, baseline_y + max_bar_h + 1.95, 0])
        self.play(FadeIn(winner_tag, shift=DOWN * 0.1), run_time=0.5)

        # ---------------------------------------------------------------
        # Accuracy strip: comparable accuracy proves it's the loss, not accuracy
        # ---------------------------------------------------------------
        acc = ACCURACY["CIFAR10"]
        acc_items = []
        for obj in OBJECTIVES:
            swatch = Rectangle(
                width=0.18, height=0.18,
                fill_color=OBJ_COLOR[obj], fill_opacity=1.0, stroke_width=0,
            )
            lab = Text(
                f"{obj}  {acc[obj]:.2f}%", color="#cfd6e0",
            ).scale(0.34)
            acc_items.append(VGroup(swatch, lab).arrange(RIGHT, buff=0.12))

        acc_row = VGroup(*acc_items).arrange(RIGHT, buff=0.5)
        acc_head = Text(
            "Test accuracy (comparable):", color="#8b93a1",
        ).scale(0.34)
        acc_strip = VGroup(acc_head, acc_row).arrange(RIGHT, buff=0.35)
        acc_box = RoundedRectangle(
            corner_radius=0.10,
            width=acc_strip.width + 0.5, height=acc_strip.height + 0.32,
            fill_color="#171b22", fill_opacity=1.0,
            stroke_color="#3a4150", stroke_width=1.5,
        )
        acc_group = VGroup(acc_box, acc_strip)
        acc_strip.move_to(acc_box.get_center())
        acc_group.move_to([0, baseline_y - 0.72, 0])

        self.play(FadeIn(acc_group, shift=UP * 0.1), run_time=0.8)

        # ---------------------------------------------------------------
        # Caption: TAKEAWAYS[3]
        # ---------------------------------------------------------------
        caption = Text(TAKEAWAYS[3], color="#aeb6c2").scale(0.40)
        caption.to_edge(DOWN, buff=0.18)
        # ensure no overlap with the accuracy box
        if caption.get_top()[1] > acc_group.get_bottom()[1] - 0.08:
            caption.next_to(acc_group, DOWN, buff=0.16)
            caption.to_edge(DOWN, buff=0.18)
        self.play(Write(caption), run_time=1.0)

        self.wait(2.0)
