"""Source-of-truth numbers for the CLXAI visualization.

EVERY value here is transcribed verbatim from the published paper:
  Arrighi, Belloni, Gallet, Gentile, Lippi, Zullich,
  "On the Properties of Feature Attribution for Supervised Contrastive Learning",
  XAI World Conference 2026.  (Tables 3 = accuracy, 4 = FA metrics.)

No number in any scene is invented. Qualitative saliency-map panels are clearly
labeled "schematic" because the paper's actual PNG figures are not in this workspace;
all *quantitative* content is the real published value.
"""

# ---- Paper identity ----
PAPER_TITLE = "On the Properties of Feature Attribution for Supervised Contrastive Learning"
PAPER_VENUE = "XAI World Conference 2026"
PAPER_AUTHORS = "Arrighi, Belloni, Gallet, Gentile, Lippi, Zullich"
PAPER_REPO = "https://github.com/ivan-gentile/CLXAI"

# ---- The three training objectives (the independent variable) ----
OBJECTIVES = ["CE", "SCL", "TL"]
OBJ_LONG = {
    "CE": "Cross-Entropy",
    "SCL": "Supervised Contrastive Loss",
    "TL": "Triplet Loss",
}
# Brand colors: CE = warm/neutral baseline, SCL = the winner (cool/strong), TL = amber
OBJ_COLOR = {
    "CE": "#9aa4b2",   # muted slate (baseline)
    "SCL": "#5ac8a8",  # teal-green (the winner)
    "TL": "#e0a458",   # amber
}

# ---- Accuracy (Table: mean over 5 runs) ----
# All objectives reach comparable accuracy -> FA differences are NOT an accuracy artifact.
ACCURACY = {
    "CIFAR10":     {"CE": 95.32, "SCL": 94.83, "TL": 94.68},
    "ImageNet-S50":{"CE": 89.17, "SCL": 85.85, "TL": 82.55},
}
ACCURACY_STD = {
    "CIFAR10":     {"CE": 0.10, "SCL": 0.12, "TL": 0.17},
    "ImageNet-S50":{"CE": 0.38, "SCL": 0.29, "TL": 0.64},
}

# ---- Feature-attribution quality (Grad-CAM), mean +/- std over 5 runs ----
# arrow: lower-better (downarrow) or higher-better (uparrow)
METRICS = {
    "Faithfulness": {
        "tool": "Grad-CAM", "unit": "Pixel-Flipping AUC", "arrow": "down",
        "blurb": "Does the map point at the pixels the model truly relies on?",
        "CIFAR10":      {"CE": 0.37, "SCL": 0.27, "TL": 0.32, "best": "SCL"},
        "ImageNet-S50": {"CE": 0.17, "SCL": 0.10, "TL": 0.19, "best": "SCL"},
        "std_CIFAR10":  {"CE": 0.01, "SCL": 0.00, "TL": 0.01},
        "std_ImageNet-S50": {"CE": 0.00, "SCL": 0.00, "TL": 0.01},
    },
    "Continuity": {
        "tool": "Grad-CAM", "unit": "SSIM", "arrow": "up",
        "blurb": "Does the map stay stable under tiny input noise?",
        "CIFAR10":      {"CE": 0.54, "SCL": 0.57, "TL": 0.57, "best": "SCL"},
        "ImageNet-S50": {"CE": 0.38, "SCL": 0.61, "TL": 0.39, "best": "SCL"},
        "std_CIFAR10":  {"CE": 0.02, "SCL": 0.01, "TL": 0.02},
        "std_ImageNet-S50": {"CE": 0.00, "SCL": 0.00, "TL": 0.01},
    },
    "Complexity": {
        "tool": "Grad-CAM", "unit": "entropy (CM)", "arrow": "down",
        "blurb": "Is the map compact and focused rather than diffuse?",
        "CIFAR10":      {"CE": 6.81, "SCL": 6.39, "TL": 6.71, "best": "SCL"},
        "ImageNet-S50": {"CE": 10.20, "SCL": 9.70, "TL": 10.07, "best": "SCL"},
        "std_CIFAR10":  {"CE": 0.00, "SCL": 0.01, "TL": 0.00},
        "std_ImageNet-S50": {"CE": 0.01, "SCL": 0.01, "TL": 0.01},
    },
    "Contrastivity": {
        "tool": "Grad-CAM", "unit": "SSIM", "arrow": "down",
        "blurb": "Do maps for different classes differ? (the metric where SCL does NOT lead)",
        # SSIM lower = better (more contrastive). On CIFAR10 the values are tiny and noisy
        # (TL nominally lowest); on ImageNet-S50 CE is clearly the most contrastive.
        # The paper's claim is that SCL has OVERALL LOWER (worse) contrastivity.
        "CIFAR10":      {"CE": 0.003, "SCL": 0.006, "TL": 0.001, "best": "TL"},
        "ImageNet-S50": {"CE": 0.20, "SCL": 0.34, "TL": 0.28, "best": "CE"},
        "std_CIFAR10":  {"CE": 0.003, "SCL": 0.002, "TL": 0.001},
        "std_ImageNet-S50": {"CE": 0.00, "SCL": 0.00, "TL": 0.00},
    },
}

# Eigen-CAM continuity is the most dramatic single contrast in the paper (CIFAR10):
# CE 0.49 -> SCL 0.69 -> TL 0.80. Used as a supporting callout.
EIGENCAM_CONTINUITY_CIFAR10 = {"CE": 0.49, "SCL": 0.69, "TL": 0.80}

# ---- Coherence: reported HONESTLY as inconclusive (ImageNet-S50 only) ----
COHERENCE_INCONCLUSIVE = {
    "PG": {"CE": 0.84, "SCL": 0.85, "TL": 0.67, "std": {"CE": 0.37, "SCL": 0.36, "TL": 0.47}},
    "AL": {"CE": 0.63, "SCL": 0.68, "TL": 0.55, "std": {"CE": 0.26, "SCL": 0.24, "TL": 0.27}},
    "note": "high variance -> no winner can be declared",
}

# ---- The five Co-12 facets evaluated ----
FACETS = [
    ("Faithfulness", "alignment with the model's true decision process", "PF AUC"),
    ("Coherence", "overlap with human ground-truth segmentation", "PG / AL"),
    ("Continuity", "stability under small input perturbation", "SSIM"),
    ("Contrastivity", "sensitivity to a change of explained class", "SSIM"),
    ("Complexity", "how compact / focused the map is", "entropy"),
]

# ---- One-line scientific takeaways (verbatim spirit of the paper) ----
TAKEAWAYS = [
    "Training objective shapes explanation quality.",
    "Contrastive learning builds a well-clustered embedding space...",
    "...and that geometry yields more faithful, more continuous, less complex saliency maps.",
    "Same backbone, comparable accuracy: the difference is the loss, not the accuracy.",
    "Honest caveats: SCL does NOT win contrastivity; coherence is inconclusive.",
]

# Precise, dataset-aware caveat strings (used by scenes / page so wording stays exact).
CONTRASTIVITY_CAVEAT = (
    "Contrastivity is the one facet where SCL does not lead: it is overall lower "
    "(worse) for SCL. On ImageNet-S50 CE is the most contrastive; on CIFAR10 the "
    "differences are tiny and noisy."
)
COHERENCE_CAVEAT = (
    "Coherence (overlap with ground-truth segmentation, ImageNet-S50 only) is "
    "inconclusive: the variance is too high to declare a winner."
)

# Where SCL wins (for the headline scoreboard): 3 of 4 sharp metrics, both datasets.
SCL_WINS = ["Faithfulness", "Continuity", "Complexity"]
CE_WINS = ["Contrastivity"]
INCONCLUSIVE = ["Coherence"]
