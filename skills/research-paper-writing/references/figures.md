# Figures Guide

From the figure parts of Peng Sida's notes, plus what the group's published figures do. The lab's own figure template is shared only inside the lab and is not reproduced here. When to sketch and when to polish figures: writing order in `SKILL.md`, steps 1 and 6.

## First Impression

A paper earns good reviews when it looks polished at first glance: clean teaser and pipeline figures, clean tables and result figures, tidy layout.

## Pipeline (Method) Figure

1. Its job is to make the novelty stand out. The Method text, not the figure, is what lets readers understand the method.
2. It must look different from the pipeline figures of previous methods; one that resembles them leaves the reader with an impression of no novelty.
3. If the full pipeline, from input to output, is not novel, make the novel module stand out within it. Several small figures in place of one large one also work, but the paper loses some polish.
4. Examples named in the notes: NSFF and KiloNeRF (good), AniSDF (bad).

## What the Group's Published Figures Do

The template itself is private, but its style shows in the group's published papers. Below, the Figure 1 and method
figure of ten of them on arXiv, read on 2026-11-03; then what they have in common. For a taxonomy of Figure 1 types
across award papers, see `bestpaper-writing`, `references/figures.md` §3.

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

## Experiment Figures and Tables

See `references/experiments.md`, "Figure/Table Writing Rules".
