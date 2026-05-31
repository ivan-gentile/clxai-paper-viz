export const meta = {
  name: 'clxai-viz-build',
  description: 'Author + render + verify Manim scenes and a public HTML page for the CLXAI paper',
  phases: [
    { title: 'Author scenes', detail: 'one agent per Manim scene, grounded in results_data.py' },
    { title: 'Render + frame-review', detail: 'render each scene, adversarially review a sampled frame, fix' },
    { title: 'Page + factcheck', detail: 'build index.html and verify every number against the paper' },
  ],
}

const VIZ = '/home/ivangentile/clxai-viz'
const SCENES_DIR = `${VIZ}/scenes`
const ENV = `${VIZ}/.manim-env`

// Shared context every scene-author agent must respect.
const COMMON = `
You are authoring ONE Manim Community v0.20.1 scene for a public visualization companion to the
PUBLISHED paper "On the Properties of Feature Attribution for Supervised Contrastive Learning"
(Arrighi, Belloni, Gallet, Gentile, Lippi, Zullich; XAI World Conference 2026).

HARD RULES (scientific convention — utmost correctness & clarity):
- Import the source-of-truth numbers: from results_data import ... (the file is at ${SCENES_DIR}/results_data.py).
  NEVER hardcode or invent a metric value. Use the constants. If you show a number, it must come from results_data.
- The paper's finding: training objective shapes Grad-CAM/Eigen-CAM explanation QUALITY. Supervised contrastive
  losses (SCL, TL) yield MORE faithful (lower PF AUC), MORE continuous (higher SSIM), LESS complex (lower entropy)
  saliency maps than Cross-Entropy (CE), at COMPARABLE accuracy. SCL is the overall winner.
  HONEST caveats you must not hide: CE leads on contrastivity; coherence is inconclusive (high variance).
- Mechanism narrative: contrastive learning pulls same-class embeddings together / pushes different-class apart,
  producing a well-clustered embedding space, and that geometry is what yields better saliency maps.
- Any saliency-map heatmap you draw procedurally is a SCHEMATIC illustration of the reported qualitative trend
  (CE = wide/diffuse; SCL = compact/focused; TL = scattered on ImageNet). If you render such a panel, include a
  small "schematic" caption so it is never mistaken for the paper's exact figure. All BARS/NUMBERS are real.

STYLE (match the existing Wordle viz house style):
- self.camera.background_color = "#11141a"
- Object colors from results_data OBJ_COLOR (CE muted slate, SCL teal-green winner, TL amber).
- Title via Text(..., weight=BOLD, color=WHITE).to_edge(UP, buff=0.35).
- Keep everything inside frame: x in [-7,7], y in [-4,4]. Labels must not overlap or clip. Leave generous buffers.
- Aim for ~18-32s of animation; clear staged reveals; a short caption line at the bottom summarizing the point.
- 720p30. Use only Manim CE 0.20.1 API. No external assets, no images, no LaTeX-heavy constructs that may fail
  (prefer Text/MathTex sparingly; if MathTex, keep it simple).

OUTPUT CONTRACT:
- Write the scene to the given file path with the Write tool.
- The file MUST define exactly one Scene subclass with the given class name.
- Do NOT render it yourself. Do NOT run manim. Just write correct, self-contained code.
- Return ONLY a short JSON-free confirmation: the class name and a one-sentence description of what it shows.
`

phase('Author scenes')

const SCENES = [
  {
    file: 'scene_finding.py', cls: 'TheFinding',
    brief: `SCENE 1 "The Finding" (the hook). Show ONE input image (draw a simple schematic object, e.g. a stylized
    bird/truck shape) with THREE Grad-CAM saliency overlays side by side, one per objective CE/SCL/TL, drawn as
    schematic heatmaps that honestly reflect the trend: CE diffuse/wide, SCL compact/focused on the object, TL
    medium. Caption: "Same image. Same architecture. Same ~95% accuracy. Different training loss -> different
    explanation quality." Then a one-line thesis from TAKEAWAYS[0]. This scene sets up the question.`,
  },
  {
    file: 'scene_mechanism.py', cls: 'TheMechanism',
    brief: `SCENE 2 "Why" (the mechanism). Animate the contrastive idea: a cloud of dots in 2 (or 3) classes;
    under CE they are loosely separated; under SCL arrows pull same-class dots together and push different-class
    clusters apart into tight well-separated clusters (the embedding geometry). Then a thin "linear probe" line
    appears (the f_head used to make Grad-CAM possible for CL models). Caption ties geometry -> better saliency:
    TAKEAWAYS[1] then TAKEAWAYS[2]. Use OBJ_COLOR for class accents but make the contrastive pull/push the star.`,
  },
  {
    file: 'scene_scoreboard.py', cls: 'TheScoreboard',
    brief: `SCENE 3 "The Scoreboard" (HERO, the quantitative core). Animated grouped bar chart of the THREE
    Grad-CAM metrics where the direction is sharp: Faithfulness (PF down), Continuity (SSIM up), Complexity (entropy down),
    for CIFAR10. Three bars per metric (CE/SCL/TL) using OBJ_COLOR, with the real values from METRICS labeled on/above bars,
    and a small up/down arrow glyph per metric showing which direction is better. Normalize bar heights per-metric so
    they read clearly, but PRINT the true value. Highlight SCL as the winner (glow/pulse) on the 3 metrics it wins.
    Add a compact accuracy strip showing CE 95.32 / SCL 94.83 / TL 94.68 to prove "comparable accuracy". Caption: TAKEAWAYS[3].`,
  },
  {
    file: 'scene_facets.py', cls: 'TheFacets',
    brief: `SCENE 4 "Five Facets, Honestly" (the integrity scene). Show the five Co-12 facets from FACETS as a row of
    cards (Faithfulness, Coherence, Continuity, Contrastivity, Complexity), each with its one-line meaning and metric.
    Then stamp a verdict on each: SCL wins Faithfulness/Continuity/Complexity (green check), CE wins Contrastivity
    (amber, honest "CE leads here"), Coherence = inconclusive (gray "?", high variance). This is the scene that proves
    the work is honest. Caption: TAKEAWAYS[4]. Use SCL_WINS/CE_WINS/INCONCLUSIVE and COHERENCE_INCONCLUSIVE.`,
  },
  {
    file: 'scene_generalizes.py', cls: 'ItGeneralizes',
    brief: `SCENE 5 "It Holds at Scale". Two side-by-side mini-panels: CIFAR10 (ResNet-18) and ImageNet-S50 (ResNet-50).
    For each, show the Faithfulness PF (down-better) trio CE/SCL/TL from METRICS, making clear SCL wins on BOTH datasets
    (CIFAR10 0.37/0.27/0.32; ImageNet 0.17/0.10/0.19). Add the dramatic Eigen-CAM continuity callout on CIFAR10
    (EIGENCAM_CONTINUITY_CIFAR10: 0.49->0.69->0.80). Caption: the finding replicates across datasets, architectures,
    and both Grad-CAM and Eigen-CAM. End on the closing line: "Choose the loss for transparency, not just accuracy."`,
  },
]

const authored = await parallel(SCENES.map(s => () =>
  agent(`${COMMON}\n\nWrite this scene to ${SCENES_DIR}/${s.file} with class name ${s.cls}.\n\nSCENE BRIEF:\n${s.brief}`,
    { label: `author:${s.cls}`, phase: 'Author scenes' })
    .then(desc => ({ ...s, desc }))
))

const ok = authored.filter(Boolean)
log(`Authored ${ok.length}/${SCENES.length} scenes`)

phase('Render + frame-review')

// Render each scene, sample a frame, adversarially review for clipping/overlap/wrong-number, fix, re-render.
const rendered = await pipeline(
  ok,
  async (s) => {
    const r = await agent(
      `Render the Manim scene at ${SCENES_DIR}/${s.file} (class ${s.cls}) and verify it.
       Run EXACTLY:
         cd ${VIZ} && micromamba run -p ${ENV} manim -qm --disable_caching ${SCENES_DIR}/${s.file} ${s.cls} 2>&1 | tail -30
       The mp4 lands at ${VIZ}/media/videos/${s.file.replace('.py','')}/720p30/${s.cls}.mp4.
       If render FAILS: read the traceback, open the scene file, fix the Manim-CE-0.20.1 API misuse (root-cause, not
       guess), and re-render until EXIT 0. Common issues: wrong Text/Arrow kwargs, VGroup arrange, out-of-frame coords.
       Then extract ONE representative frame near the end with ffmpeg:
         micromamba run -p ${ENV} ffmpeg -y -sseof -2 -i <mp4> -frames:v 1 /tmp/clxai_${s.cls}.png 2>/dev/null
       Read /tmp/clxai_${s.cls}.png with the Read tool and ADVERSARIALLY review: any text clipped at frame edges?
       any overlapping labels? any number that disagrees with results_data.py? is the SCL-winner story legible?
       If you find a defect, fix the scene file and re-render+re-check. Iterate up to 3 times.
       Return: the final mp4 absolute path, EXIT status, and a one-line verdict on the reviewed frame.`,
      { label: `render:${s.cls}`, phase: 'Render + frame-review' })
    return { ...s, render: r }
  }
)

const done = rendered.filter(Boolean)
log(`Rendered+reviewed ${done.length} scenes`)

phase('Page + factcheck')

// Build the public HTML page and an independent fact-check, in parallel (page references files; factcheck reads data).
const [pageResult, factcheck] = await parallel([
  () => agent(
    `Collect every rendered scene mp4 from ${VIZ}/media/videos/*/720p30/*.mp4 and copy them into ${VIZ}/site_media/
     (create it). Then write a SINGLE self-contained public web page at ${VIZ}/index.html for a general + scientific
     convention audience explaining the paper "On the Properties of Feature Attribution for Supervised Contrastive
     Learning" (Arrighi et al., XAI World Conference 2026, repo https://github.com/ivan-gentile/CLXAI).
     Structure: hero title + one-paragraph plain-language thesis; then one <section> per scene in this order
     [TheFinding, TheMechanism, TheScoreboard, TheFacets, ItGeneralizes] each with a heading, 2-3 sentences of
     prose, and a <video controls muted playsinline> tag pointing to site_media/<Class>.mp4; then a "By the numbers"
     section with an HTML table of the real CIFAR10 + ImageNet-S50 Grad-CAM metrics (read them from
     ${SCENES_DIR}/results_data.py — do not invent), with up/down arrows and SCL bolded where it wins; an honest
     "What we do NOT claim" box (CE wins contrastivity; coherence inconclusive); a footer crediting the authors and
     linking the repo. Dark theme matching #11141a background, teal #5ac8a8 accents. Inline CSS only, no external deps.
     Mobile-friendly. Return the absolute path to index.html and the list of videos embedded.`,
    { label: 'page:index.html', phase: 'Page + factcheck' }),
  () => agent(
    `Fact-check integrity pass. Read ${SCENES_DIR}/results_data.py and EACH scene file in ${SCENES_DIR}/scene_*.py.
     For every metric value that appears as a literal number in any scene file, confirm it is either (a) imported from
     results_data, or (b) exactly equal to the corresponding results_data value. Flag ANY hardcoded number that does
     not match, ANY invented metric, and ANY place a caveat (CE-wins-contrastivity, coherence-inconclusive) is
     misrepresented as SCL winning. Return a JSON-free bullet list: PASS or a list of concrete violations with file:line.`,
    { label: 'factcheck', phase: 'Page + factcheck' }),
])

return {
  scenes: done.map(s => ({ cls: s.cls, render: s.render })),
  page: pageResult,
  factcheck,
}
