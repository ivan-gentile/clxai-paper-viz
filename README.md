# CLXAI — visual companion

A public, animated companion to the paper

> **On the Properties of Feature Attribution for Supervised Contrastive Learning**
> Leonardo Arrighi, Julia Eva Belloni, Aurélie Gallet, Ivan Gentile, Matteo Lippi, Marco Zullich
> — *XAI World Conference 2026*. Paper code: <https://github.com/ivan-gentile/CLXAI>

> 🎬 **Live page (general + scientific audience, with animations):**
> **https://ivan-gentile.github.io/clxai-paper-viz/**

## The finding, in one line

Hold the architecture (ResNet-18 / ResNet-50) and the data (CIFAR-10 / ImageNet-S₅₀) fixed
and change only the **training loss**. Networks trained with **supervised contrastive
learning** (SCL) and **triplet loss** (TL) produce Grad-CAM / Eigen-CAM saliency maps that
are **more faithful**, **more continuous**, and **less complex** than a **cross-entropy**
(CE) baseline — at **comparable accuracy**. The mechanism: contrastive training organizes a
better-clustered embedding space, and that geometry yields better explanations.

## What's here

Five hand-authored [Manim](https://www.manim.community/) scenes (Community v0.20.1), each
grounded in the paper's **real published numbers** (`scenes/results_data.py` is the single
source of truth — no value on screen is invented), plus a self-contained `index.html`.

| scene | shows |
|---|---|
| `TheFinding` | same image, three losses → three different Grad-CAM maps |
| `TheMechanism` | contrastive pull-together / push-apart → clustered geometry → better saliency |
| `TheScoreboard` | the real CIFAR-10 bars (Faithfulness ↓, Continuity ↑, Complexity ↓) at matched accuracy |
| `TheFacets` | the five Co-12 facets, scored **honestly** (SCL does **not** win contrastivity; coherence is inconclusive) |
| `ItGeneralizes` | the result replicates on ImageNet-S₅₀ and under Eigen-CAM |

### Honesty

Quantitative bars and numbers are the exact published values. Saliency-map heatmaps drawn
inside the scenes are **schematic illustrations** of the reported qualitative trend (labeled
as such), because this companion does not vendor the paper's original figure PNGs. The
caveats the paper makes — CE/TL lead on **contrastivity**, **coherence** is inconclusive —
are shown on screen, not averaged away.

## Render locally

```bash
# Manim CE 0.20.1 in a conda-forge env (no sudo needed)
micromamba run -p ./.manim-env manim -qm --disable_caching scenes/scene_scoreboard.py TheScoreboard
```

This is an independent visualization. It does **not** modify the original CLXAI repository.
