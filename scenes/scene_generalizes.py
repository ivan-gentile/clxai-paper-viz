"""SCENE 5 - "It Holds at Scale".

Two side-by-side mini-panels (CIFAR10 / ResNet-18 and ImageNet-S50 / ResNet-50)
showing the Faithfulness PF (down-better) trio CE/SCL/TL, making clear SCL wins on
BOTH datasets, plus the dramatic Eigen-CAM continuity callout on CIFAR10.

All numbers are imported from results_data (source of truth). Nothing hardcoded.
"""

from manim import (
    Scene,
    Text,
    MathTex,
    Rectangle,
    RoundedRectangle,
    Line,
    VGroup,
    Create,
    Write,
    FadeIn,
    GrowFromEdge,
    Indicate,
    WHITE,
    BOLD,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    DR,
    DEGREES,
)

from results_data import (
    METRICS,
    OBJECTIVES,
    OBJ_COLOR,
    EIGENCAM_CONTINUITY_CIFAR10,
)


class ItGeneralizes(Scene):
    def construct(self):
        self.camera.background_color = "#11141a"

        FAITH = METRICS["Faithfulness"]  # Pixel-Flipping AUC, lower better

        # ---- Title ----
        title = Text("It Holds at Scale", weight=BOLD, color=WHITE).scale(0.9)
        title.to_edge(UP, buff=0.35)

        subtitle = Text(
            "Faithfulness  (Grad-CAM, Pixel-Flipping AUC  -  lower is better)",
            color="#aeb6c2",
        ).scale(0.38)
        subtitle.next_to(title, DOWN, buff=0.16)

        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(subtitle, shift=DOWN * 0.1), run_time=0.7)

        # ---- Build the two panels ----
        left_panel = self._build_panel(
            dataset="CIFAR10",
            arch="ResNet-18",
            values=FAITH["CIFAR10"],
            best=FAITH["CIFAR10"]["best"],
        )
        right_panel = self._build_panel(
            dataset="ImageNet-S50",
            arch="ResNet-50",
            values=FAITH["ImageNet-S50"],
            best=FAITH["ImageNet-S50"]["best"],
        )

        left_panel.move_to([-3.45, -0.62, 0])
        right_panel.move_to([3.45, -0.62, 0])

        # Reveal panel frames
        self.play(
            Create(left_panel["frame"]),
            Create(right_panel["frame"]),
            run_time=1.0,
        )
        self.play(
            FadeIn(left_panel["header"]),
            FadeIn(right_panel["header"]),
            run_time=0.7,
        )

        # Grow bars staged: CE, then SCL, then TL on both panels together
        for key in OBJECTIVES:
            self.play(
                GrowFromEdge(left_panel["bars"][key], DOWN),
                GrowFromEdge(right_panel["bars"][key], DOWN),
                FadeIn(left_panel["labels"][key]),
                FadeIn(right_panel["labels"][key]),
                FadeIn(left_panel["vals"][key]),
                FadeIn(right_panel["vals"][key]),
                run_time=0.7,
            )

        # Highlight the winner (SCL lowest -> shortest bar) on both panels
        self.play(
            Indicate(left_panel["bars"]["SCL"], color=OBJ_COLOR["SCL"], scale_factor=1.12),
            Indicate(right_panel["bars"]["SCL"], color=OBJ_COLOR["SCL"], scale_factor=1.12),
            FadeIn(left_panel["winner_tag"]),
            FadeIn(right_panel["winner_tag"]),
            run_time=1.1,
        )

        win_note = Text(
            "SCL is the most faithful on BOTH datasets",
            color=OBJ_COLOR["SCL"],
            weight=BOLD,
        ).scale(0.46)
        win_note.move_to([0, -3.05, 0])
        self.play(FadeIn(win_note, shift=UP * 0.1), run_time=0.8)

        # ---- Eigen-CAM continuity callout (CIFAR10) ----
        callout = self._eigencam_callout()
        callout.move_to([0, 2.0, 0])
        self.play(
            FadeIn(callout["box"]),
            Write(callout["title"]),
            run_time=0.9,
        )
        self.play(
            *[FadeIn(m, shift=RIGHT * 0.15) for m in callout["chain"]],
            run_time=1.1,
        )
        self.play(Indicate(callout["tl_val"], color=OBJ_COLOR["TL"], scale_factor=1.2), run_time=0.8)

        # ---- Caption + closing line ----
        self.play(win_note.animate.move_to([0, -2.85, 0]).scale(0.92), run_time=0.5)

        caption = Text(
            "Replicates across datasets, architectures, and both Grad-CAM & Eigen-CAM",
            color="#aeb6c2",
        ).scale(0.4)
        caption.move_to([0, -3.35, 0])
        self.play(FadeIn(caption), run_time=0.8)

        closing = Text(
            "Choose the loss for transparency, not just accuracy.",
            weight=BOLD,
            color=WHITE,
        ).scale(0.52)
        closing.move_to([0, -3.78, 0])
        self.play(Write(closing), run_time=1.4)

        self.wait(1.8)

    # ------------------------------------------------------------------
    def _build_panel(self, dataset, arch, values, best):
        """One mini bar panel for a dataset. Bars are scaled so the largest
        value across BOTH panels is not needed; we scale per-panel to keep
        relative ordering legible. Heights encode the PF AUC values directly."""
        panel = VGroup()
        d = {}

        frame = RoundedRectangle(
            width=5.6, height=3.9, corner_radius=0.12,
            stroke_color="#2c333f", stroke_width=2.0,
            fill_color="#161a22", fill_opacity=0.55,
        )

        # Header text (dataset + architecture)
        head_name = Text(dataset, weight=BOLD, color=WHITE).scale(0.5)
        head_arch = Text(arch, color="#8b94a3").scale(0.34)
        head_arch.next_to(head_name, DOWN, buff=0.08)
        header = VGroup(head_name, head_arch)
        header.move_to(frame.get_top() + DOWN * 0.55)

        # Bar geometry: baseline near bottom of frame
        baseline_y = frame.get_bottom()[1] + 0.55
        max_h = 1.95  # max bar height
        # Scale so the max value in THIS panel maps to max_h
        vmax = max(values[k] for k in OBJECTIVES)
        bar_w = 0.95
        xs = [-1.55, 0.0, 1.55]  # relative to panel center

        bars = {}
        labels = {}
        vals = {}
        winner_tag = None

        for x, key in zip(xs, OBJECTIVES):
            v = values[key]
            h = (v / vmax) * max_h
            bar = Rectangle(
                width=bar_w, height=h,
                fill_color=OBJ_COLOR[key], fill_opacity=0.95,
                stroke_color=OBJ_COLOR[key], stroke_width=1.5,
            )
            # place bar so its bottom sits on the baseline (frame-relative coords)
            bar.move_to(frame.get_center() + [x, baseline_y - frame.get_center()[1] + h / 2, 0])

            name_lbl = Text(key, weight=BOLD, color=OBJ_COLOR[key]).scale(0.42)
            name_lbl.move_to(frame.get_center() + [x, baseline_y - frame.get_center()[1] - 0.28, 0])

            val_lbl = Text(f"{v:.2f}", color=WHITE).scale(0.4)
            val_lbl.next_to(bar, UP, buff=0.12)

            bars[key] = bar
            labels[key] = name_lbl
            vals[key] = val_lbl

            if key == best:
                tag = Text("winner", weight=BOLD, color=OBJ_COLOR[key]).scale(0.3)
                tag.next_to(val_lbl, UP, buff=0.08)
                winner_tag = tag

        # baseline rule
        base_line = Line(
            frame.get_center() + [-2.4, baseline_y - frame.get_center()[1], 0],
            frame.get_center() + [2.4, baseline_y - frame.get_center()[1], 0],
            color="#3a414e", stroke_width=1.5,
        )

        panel.add(frame, header, base_line, winner_tag)
        for key in OBJECTIVES:
            panel.add(bars[key], labels[key], vals[key])

        # expose pieces for animation
        d["frame"] = frame
        d["header"] = header
        d["base_line"] = base_line
        d["bars"] = bars
        d["labels"] = labels
        d["vals"] = vals
        d["winner_tag"] = winner_tag

        # Make the VGroup behave like a dict-accessor wrapper:
        d_group = _PanelGroup(panel, d)
        return d_group

    # ------------------------------------------------------------------
    def _eigencam_callout(self):
        c = {}
        box = RoundedRectangle(
            width=8.8, height=1.55, corner_radius=0.12,
            stroke_color="#3a414e", stroke_width=2.0,
            fill_color="#1b2029", fill_opacity=0.92,
        )

        title = Text(
            "Eigen-CAM continuity  (CIFAR10, SSIM  -  higher is better)",
            color="#cdd3dc",
        ).scale(0.4)
        title.move_to(box.get_top() + DOWN * 0.3)

        # CE -> SCL -> TL  chain of values from EIGENCAM_CONTINUITY_CIFAR10
        chain = VGroup()
        order = OBJECTIVES  # CE, SCL, TL
        prev = None
        tl_val = None
        xstart = -3.6
        spacing = 2.4
        for i, key in enumerate(order):
            v = EIGENCAM_CONTINUITY_CIFAR10[key]
            grp = VGroup()
            name = Text(key, weight=BOLD, color=OBJ_COLOR[key]).scale(0.4)
            num = Text(f"{v:.2f}", weight=BOLD, color=OBJ_COLOR[key]).scale(0.55)
            num.next_to(name, DOWN, buff=0.07)
            grp.add(name, num)
            grp.move_to([xstart + i * spacing, box.get_center()[1] - 0.12, 0])
            chain.add(grp)
            if key == "TL":
                tl_val = num

        # arrows between the three values
        arrows = VGroup()
        for i in range(len(order) - 1):
            a = MathTex(r"\rightarrow", color="#8b94a3").scale(0.8)
            a.move_to([xstart + i * spacing + spacing / 2, box.get_center()[1] - 0.12, 0])
            arrows.add(a)

        chain.add(arrows)

        c["box"] = box
        c["title"] = title
        c["chain"] = chain
        c["tl_val"] = tl_val

        container = VGroup(box, title, chain)
        return _PanelGroup(container, c)


class _PanelGroup(VGroup):
    """Thin wrapper that lets us index a panel by its named parts while still
    being a single Manim VGroup that can be moved/created."""

    def __init__(self, vgroup, parts):
        super().__init__(vgroup)
        self._parts = parts

    def __getitem__(self, key):
        if isinstance(key, str):
            return self._parts[key]
        return super().__getitem__(key)
