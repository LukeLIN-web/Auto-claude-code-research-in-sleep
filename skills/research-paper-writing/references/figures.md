# Figures Guide

Fused from the figure parts of Peng Sida's notes (plus what his group's published figures do; the lab's own template is private and not reproduced) and the figures of 44 of the 55 award papers. Award papers argue with their figures as much as with their text. Reviewers look at Figure 1, the method overview and the main qualitative comparison before they read a paragraph, so each of these figures has to carry one claim on its own. When to sketch and when to polish figures: writing order in `SKILL.md`. Statistics are given for **two-column** (CVPR/ICCV, 26 papers) and **one-column** (NeurIPS, 18 papers) layouts.

## First Impression
A paper earns good reviews when it looks polished at first glance: clean teaser and pipeline figures, clean tables and result figures, tidy layout.

## What Award Papers Do
| Observation | Two-column (CVPR/ICCV) | One-column (NeurIPS) |
|---|---|---|
| Figures in the main paper | median 7 (p10–p90: 3–9) | median 5 (3–6) |
| Tables in the main paper | median 3 (0–5) | median 0 (0–2) |
| Floats per main page | median 1.1 (0.5–1.6) | median 0.7 (0.5–0.9) |
| Figure 1 on page 1 | 21 / 26; above the abstract in 13 | on page 2 in 13 / 18 |
| Figure 1 full width | 16 / 26 | 17 / 18 |
| Method overview figure (caption says overview, pipeline, architecture, framework) | 15 / 26, usually Figure 2 | 6 / 18 |
| Figure caption length (words) | median 42 (10–91) | median 46 (14–102) |
| Figure 1 caption length (words) | median 65 (32–100) | median 66 (21–153) |
| First caption sentence (words) | median 7 (2–20) | median 10 (4–21) |
| Caption opens with a bold title | 48 % | 30 % |
| Caption names sub-panels ((a), left, top) | 27 % | 39 % |

So a two-column vision paper has about one float per page: a teaser on page 1, an overview as Figure 2, two to four result figures and three tables. A NeurIPS paper has fewer, larger figures, and its Figure 1 is often a plot or a concept illustration on page 2.

## The Figure Plan
Plan the figures from the evidence map (Step 5b) before drawing anything. Every figure answers one claim; a figure that answers none moves to the appendix.

```text
| Fig | Place | Claim it carries | Type (Figure 1 types below) | Panels | Material needed | Status | Caption takeaway |
| 1 | p.1, full width | prior work decodes densely; we query points | contrast-schematic + plot | (a) prior (b) ours (c) acc. vs. time | timing numbers for (c) | draw (a)(b) now; (c) placeholder | "Decoding on demand." |
| 2 | Sec. 3 top, full width | one encoder pass + one shared decoder | overview | single | architecture details | draw now (schematic) | "Overview of X." |
| 3 | Sec. 4.2 | ours keeps moving objects sharp | qualitative grid | 3 scenes × 4 methods | renders | placeholder | ... |
```

Rules:
1. **One claim per figure**, written as the caption's first sentence before the figure is drawn.
2. **Status** is `draw now` only for schematics whose content the user has stated (mechanism, components, data flow). Everything that shows results (images, renders, plots, numbers) is a `placeholder` until the user provides the material. Never invent a result image, a curve or a number.
3. **Material needed** is concrete: which scenes, which baselines, which metric, which axis, which resolution.
4. The plan goes into `report.md` (section "Figure plan"). In LaTeX, placeholders are blank framed areas and the full plan of each one is written into its caption as a red `\TODO{Figure plan: …}` (`assets/figures/figures_preamble.tex`).
5. Count check: about one float per page in two-column papers; do not exceed the corpus p90 (9 figures, 5 tables in 8 pages) without moving material to the supplement. Only material that is not a main-text claim's decisive evidence moves.

## Figure 1
### Types (Figure 1 of 44 award papers)

| Type | What it shows | Two-col | One-col | Examples |
|---|---|---|---|---|
| `showcase` | inputs → outputs, or a gallery of what the method can do | 9 | 2 | DreamBooth, VGGT, OmniMotion, FlowEdit, Imagen |
| `contrast-schematic` | prior mechanism next to ours, drawn as diagrams | 6 | 2 | Mip-NeRF (ray vs. cone), Swin vs. ViT, OpenGAN, DPO (RLHF vs. DPO), MAC |
| `contrast-results` / `diagnosis` | prior work failing on a real input, ours fixing it, often with the mechanism of the failure | 2 | 0 | DynIBaR, Mip-Splatting |
| `concept` | the idea or phenomenon itself, abstracted | 3 | 5 | EPro-PnP, Pixel-Perfect SfM, superposition, memorization regimes |
| `plot` | the headline result or the motivating phenomenon as a chart | 2 | 7 | scaling laws, emergence curves, depth scaling in RL |
| `system` | task, model and data (or applications) in two or three panels | 2 | 2 | Segment Anything, Navigation World Models, MineDojo |
| `resource` | the dataset itself, with its scale | 2 | 0 | CO3D, PixMo |

### Choose by route

| Route (`routing.md`) | Figure 1 | Why |
|---|---|---|
| `failure` | `diagnosis` or `contrast-results`: the baseline failing under the condition, ours fixing it, the mechanism drawn next to it | the reader sees the gap before reading it |
| `cost` | `contrast-schematic` (old mechanism vs. ours, with the cost written on it), optionally plus a cost/accuracy plot | the cost is a property of the mechanism, so draw the mechanism |
| `capability-gap`, `trend` | `showcase`: real inputs on the left, all outputs on the right | the capability is the claim |
| `insight` | `contrast-schematic` or `concept`: the pipeline that disappears | DPO removes a reward model; draw it disappearing |
| L3 scaling, L4 re-examination | `plot` with annotations on the curve | the regularity or the reversal is the claim |
| L5 mechanism, L6 theory | `concept`, then a plot | the phenomenon has to be seen to be puzzling |
| L7 resource | `resource` gallery with one scale number, or `system` | scale and diversity are the claim |
| L8 measurement | `showcase` of the measured phenomenon | the new signal is the claim |

### Rules
- **Two-column papers**: put Figure 1 on page 1 (21 / 26), full width in most cases (16 / 26), as a `strip` teaser above the abstract or at the top of the right column. **One-column papers**: Figure 1 at the top of page 2 is normal.
- It must be understandable without the paper: method names on panels, “Ours” or the method name on our panel, one visual contrast.
- The caption is the longest in the paper (median 65 words): the takeaway, then what each panel shows, then how to read it (colours, symbols).
- Reference it in the introduction (29 / 55 do), at the sentence that introduces the idea.

### What one group's published figures do

The template itself is private, but its style shows in the group's published papers. Below, the Figure 1 and method
figure of ten of them on arXiv, read on 2026-11-03; then what they have in common. The taxonomy of Figure 1 types across award papers is under "Types" above.

| Paper | Figure 1 | Method figure |
|---|---|---|
| PVNet (CVPR'19, 1812.11788) | basic idea on a real image, stage by stage (a)–(f); occlusion and truncation cases in a dashed group | network as 3D blocks; each intermediate output drawn as its real visualization (vector field, labels, hypotheses, distributions) |
| Deep Snake (CVPR'20, 2001.01629) | basic idea on a real image: initial contour → feature learning on the contour → offsets | (a) architecture as colour-grouped blocks; (b) the pipeline as a strip of real images with the contour at each stage |
| Neural Body (CVPR'21, 2012.15838) | input → output: bold "Input: a sparse multi-view video" over real frames, "Output: 3D geometry and appearance" over novel views and reconstructions | a separate basic-idea figure (Figure 2) with real body renders; pipeline with real renders at both ends |
| Animatable NeRF (ICCV'21, 2105.02872) | the same input → output layout | real body renders in observation and canonical space; networks as small coloured blocks |
| ENeRF (SIGGRAPH Asia'22, 2112.01517) | result frames along a time axis in a mock application window with a "24 FPS" badge | real input images; networks as pale blocks |
| ManhattanSDF (CVPR'22, 2205.02836) | core idea: real geometry and segmentation before → "Joint optimization" → after | real 3D scene with a ray; rendered image, geometry and segmentation drawn as images beside their losses |
| Humans in minutes (CVPR'23, 2302.12237) | ours vs. Neural Body renders at 1, 5 and 10 minutes, beside the LPIPS-over-time curve | two colour-coded panels (deformation space, canonical space) with 3D renders |
| MLP Maps (CVPR'23, 2304.06717) | schematic basic idea, drawn in 3D: the only Figure 1 here without real data | coloured blocks with real input-view thumbnails |
| 4K4D (CVPR'24, 2310.11448) | ground truth, ours and two baselines on one frame, each with an LPIPS and FPS badge on the image | four rounded panels (a)–(d), each with real point clouds or renders |
| Street Gaussians (ECCV'24, 2401.01339) | ours vs. two baselines with zoom-in insets and a "Train: 30min, FPS: 135" badge per method | real point clouds and tracked boxes in; rendered images, decomposition and semantic maps out |

What they share:

1. **Figure 1 shows real data of the task.** Nine of the ten contain real images, renders or reconstructions, and so do
   both good examples the notes name (NSFF: a gallery of results; KiloNeRF: one large MLP vs. thousands of small ones,
   each above its rendered scene, with "56s → 0.02s, 2548× faster"). A Figure 1 made only of text boxes and arrows is
   outside this style.
2. **Data is drawn as data.** Whatever flows between modules (an image, a vector field, a contour, a point cloud, a
   render) appears as its real visualization at that stage. Boxes are kept for networks and operations, filled in pale
   colours and grouped by colour.
3. **The headline number sits on the image** when the claim is quality or speed: a small dark badge with the metric on
   each method's panel (4K4D, Street Gaussians, KiloNeRF).
4. **Layout labels are short**: bold "Input: …" / "Output: …" headers over the two halves, a few words under each image,
   (a)/(b)/(c) under the panels.
5. **What it does and how it works are separate figures** when space allows (Neural Body Figures 1 and 2).
6. **Hard cases get their own group** inside Figure 1 (PVNet: occlusion and truncation in a dashed box).

## Method Overview Figure
1. Its job is to make the novelty stand out. The Method text, not the figure, is what lets readers understand the method.
2. It must look different from the pipeline figures of previous methods; one that resembles them leaves the reader with an impression of no novelty.
3. If the full pipeline, from input to output, is not novel, make the novel module stand out within it. Several small figures in place of one large one also work, but the paper loses some polish.
4. Examples named in the notes: NSFF and KiloNeRF (good), AniSDF (bad).

Present in 15 / 26 two-column papers, most often as Figure 2 at the top of the method section, usually full width.
- **Data flows left to right** (or top to bottom for stacked blocks). Real input examples on the left and real outputs on the right (VGGT, Segment Anything, MAC, OmniMotion) make the diagram concrete; use placeholders until the user supplies them.
- **Boxes are named exactly as the method subsections and use the same symbols as the equations** (OmniMotion's canonical volume and bijections, FlowEdit's latents). A symbol in the figure that the text does not define is an error.
- **Colour encodes role, consistently across all figures**: e.g., one colour for what is learned, grey for frozen or given components, one accent for our new component, one for data/queries. Swin, DDT-LLaMA and Gated Attention colour modules by type, and DDT-LLaMA marks the trained encoder with an icon.
- **Show the delta**: highlight the new component; draw reused parts in grey.
- **Sub-panels** separate representation from computation, or training from inference ((a)/(b) in OmniMotion, FlowEdit).
- Repetition as `× L`; grouping with dashed boxes; no layer counts or hyperparameters unless they are the contribution.

## Result Figures
### Qualitative comparisons
- A grid: **rows = inputs/scenes, columns = methods** with the method name above each column; order is input, baselines, ours, ground truth (MegaSaM, BrickGPT, Mip-Splatting, 3D Student Splatting).
- Same crop, viewpoint, colour map and point size for every method; ours is not cherry-picked against a different frame.
- **Zoom-in insets** with a coloured box on the full image and the crop beside it; at most two per image.
- Put the per-image metric in a corner of the image when it helps (DynIBaR LPIPS, 3D Student Splatting PSNR), or a status label under each result (BrickGPT stable/unstable).
- Pick inputs that stress the claim (fast motion, large zoom, long video) and say so in the caption.

### Plots
- **One colour per method across every plot in the paper**; ours in the saturated accent colour and drawn on top, baselines in muted colours. Use `assets/figures/bestpaper.mplstyle` and `plot_style.py`.
- **Label curves directly** at their ends, or with one shared legend above the panels; no legend boxes covering data.
- Log axes for scaling studies; mark the regime, frontier or slope on the plot itself (data-constrained scaling marks regions; superposition draws the slope triangle).
- No plot titles inside the figure when the caption carries them; axis labels with units; tick labels at least 6 pt in print.
- Export vector PDF, not PNG.

### Ablation and analysis figures
One question per figure, matching an ablation in the text; the caption states the answer.

## Captions
Template (two-column vision papers):

```latex
\caption{\textbf{<Takeaway in 3 to 10 words>.}
<What is shown, panel by panel: (a) …, (b) …>.
<How to read it: colours, symbols, insets>.
<Why it happens, or a pointer: “see Sec. 4.3”>.}
```

- The **first sentence is the takeaway**, not a description: “Decoding on demand.”, “3D Gaussian Splatting aliases when zooming out.”, not “Results on dataset X.” (median 7 words, p90 20).
- Bold title in about half of two-column papers and a third of NeurIPS papers; either is fine, but be consistent across the paper.
- Length: median 42 words; Figure 1 longer (median 65). Below 10 words a caption explains nothing; above about 100 the content belongs in the text.
- **Name the colours** used in the figure and write the key words in those colours if the template allows (Mip-Splatting colours its key terms in the caption to match the figure).
- Name sub-panels with (a), (b) or left/right when there is more than one.
- Same no-dash rule as the text (author preference); no workflow notes except `\TODO{}`.

## Layout and Typography
| Item | Rule |
|---|---|
| Widths | `\linewidth` inside `figure` (one column, 3.25 in in CVPR) or inside `figure*`/`strip` (6.875 in). Never absolute widths wider than the column. |
| Placement | `[t]`, after or on the page of the first reference; teaser via `strip` (CVPR kit) |
| Text in figures | sans-serif, 6–8 pt at print size, never larger than the caption (9 pt); one font family for all figures |
| Maths in figures | the same symbols as the paper, set in LaTeX (TikZ) or with matplotlib mathtext |
| Lines | 0.5–1 pt; arrows with the same head everywhere |
| Colour | 2–3 accent colours plus greys; colour-blind safe; one fixed colour for “ours”; light fills (20–30 % tint) for boxes, saturated colour only for what matters |
| Sub-panel labels | “(a) short name” centred below each panel, same size everywhere |
| Avoid | 3D effects, shadows, gradients, clip art, rainbow colour maps for ordered data (use viridis), screenshots of tables |
| Resolution | vector PDF for diagrams and plots; images at ≥ 300 dpi at print size |

## Honesty and Placeholders
- Draw schematics only from mechanisms the user has stated. Where a mechanism is `[TODO]` in the method, draw that part dashed and say so in the caption.
- Never fabricate result images, renders, curves, tables in figures, or numbers on figures.
- A placeholder is a blank framed area of the planned size with “Figure placeholder (see caption)”; its caption contains the plan ("The Figure Plan"). `scripts/check_figures.py` lists all remaining placeholders.

## Toolkit (`assets/figures/`)
| File | Use |
|---|---|
| `figures_preamble.tex` | colours, TikZ styles (`module`, `frozen`, `ours`, `data`, `flow`), `\figplaceholder{w}{h}`, `\FigPlan{…}` |
| `teaser_strip.tex` | two-column teaser with three panels (CVPR `strip`) |
| `overview_tikz.tex` | left-to-right overview skeleton: inputs, encoder, representation, new module, outputs |
| `qualitative_grid.tex` | rows × methods grid with column labels and zoom insets; falls back to placeholders when images are missing |
| `bestpaper.mplstyle`, `plot_style.py` | matplotlib style, fixed method colours (ours highlighted), column/full-width sizes, direct curve labels |

## Experiment Figures and Tables
See `references/experiments.md`, "Figure/Table Writing Rules".

## Checklist
- [ ] A figure plan exists; every figure carries one claim and every main claim has a figure or table.
- [ ] Figure 1 type matches the route; it is understandable alone; it is on page 1 (two-column) and referenced in the introduction.
- [ ] Overview: left to right, names and symbols match the method, colour by role, new component highlighted.
- [ ] Results: same order and colours for methods everywhere; ours last before ground truth; insets where differences are small.
- [ ] Captions: takeaway first; 10–100 words (Figure 1 longer); colours and panels named; consistent title style.
- [ ] Widths relative to `\linewidth`; fonts 6–8 pt; vector plots; ≤ 3 accent colours.
- [ ] No fabricated results; placeholders listed in `report.md`.
- [ ] `python3 scripts/check_figures.py main.tex` shows no ERROR and each WARN is fixed or justified.
