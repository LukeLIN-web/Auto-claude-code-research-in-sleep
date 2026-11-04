# Writing Plan Example: ManhattanSDF Introduction

From the notes' worked example (写作思路典例). The plan comes before any English prose: first one line per paragraph, then one line per sentence. Chinese plan text is translated; English sentences are kept as written in the notes, placeholders included.

## Paragraph-level plan

1. Problem to solve: scene reconstruction -> COLMAP works well, and how it works -> COLMAP fails on low-textured regions such as floors and walls, and why.
2. Traditional methods: use planes to help scene reconstruction -> complex pipeline with many parameters to tune -> when the planes are poor, the reconstruction is poor.
3. Recent methods: NeRF, VolSDF and NeuS reconstruct objects well -> experiments show that they fail on low-textured indoor regions -> large low-textured regions admit many geometries that explain the images.
4. Our method: use semantics to help reconstruction, and optimize the semantics during reconstruction -> Specifically, detect floors and walls and make them respect their semantic properties -> assume a Manhattan world: surface normals on floors and walls must satisfy the corresponding properties; the wall normal is optimized -> considering that the segmentation may be wrong, we define a semantic MLP -> multi-view consistency improves the semantic segmentation, while the geometric loss optimizes the segmentation probability.
5. Experiments.

## Sentence-level plan

**Problem to solve**

1. Reconstructing 3D scenes from multi-view images is a cornerstone of many applications such as augmented reality, robotics, and autonomous driving.
2. Given input images, traditional methods generally estimate the depth map for each image based on the multi-view stereo and then fuse estimated depth maps into 3D geometries.
3. Although these methods achieve impressive reconstruction results, they have difficulty in handling low-textured regions such as floors and walls of indoor scenes due to unreliable matching in these regions.

**Traditional methods use the planar prior**

1. To overcome this problem, some methods utilize the planar prior to help reconstruction.
2. [How they use the planar prior.]
3. [How planes are modeled:] triangulation \cite{planar prior}, superpixel \cite{tapa}, or learning-based plane segmentation methods \cite{}.
4. Although these methods improve the performance, when depth estimation or plane segmentation is inaccurate, they tend to perform poorly.

**Recent methods**

1. Recently, \cite{SRN, NeRF, IDR} represent 3D scenes as implicit neural representations and learn the representations from images with differentiable renderers.
2. IDR \cite{} uses a signed distance field to represent the scene and renders it into images based on the differentiable surface rendering. -> Although it produces high-quality reconstruction results, it tends to fail in complex scenes, as illustrated in \cite{volsdf, neus}. -> A reason is that the surface rendering only enables the gradient back-propagation on the surface point, which is prone to local optima.
3. To solve this problem, \cite{unsurf, volsdf, neus} propose to render implicit surfaces with volume rendering techniques, which produce gradient signals on multiple points along camera rays. -> This enables them to handle complex scenes without the additional mask supervision.
4. However, they still have poor performance in low-textured planar regions, as demonstrated by our experiments in Section~\ref{}.
5. This is because that there are many possible 3D representations that produce the same observed images, especially in low-textured planar regions.

**Our method**

1. In this paper, we propose a novel implicit neural representation that encodes geometric and semantic information for 3D reconstruction of indoor scenes.
2. Our innovation is utilizing semantic properties of planar regions to resolve ambiguities in the reconstruction, while optimizing the estimated plane segmentation based on the geometric properties.
3. Specifically, we use an MLP network to predict the signed distance and color for any point in 3D space. Given the segmentation of floor and wall regions, we enforce the signed distance field to respect corresponding geometric structures in these regions based on the Manhattan-world assumption.
4. Considering that inaccurate segmentation results may mislead the optimization, we additionally use a network to predict a semantic label for each 3D point and jointly optimize it based on the geometric loss.

## Which templates this plan uses (our reading)

1. Paragraph 1 is Task Version 4: the opening paragraph already exposes the challenge through a previous method (MVS on low-textured regions).
2. Paragraphs 2–3 are Technical-Challenge Version 2: the insight (planar prior) has a traditional line behind it, and recent methods still fail for a stated technical reason.
3. Paragraph 4 is Pipeline Version 2: contribution 2 (the jointly optimized semantic network) answers a challenge that contribution 1 itself faces (inaccurate segmentation).
