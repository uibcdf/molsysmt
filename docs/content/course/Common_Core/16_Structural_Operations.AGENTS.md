# Module 16 Content Governance (`16_Structural_Operations.AGENTS.md`)

This document defines the **non-negotiable content contract** for `16_Structural_Operations.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module introduces the **`msm.structure`** specialized function module, focusing on 3D spatial operations, geometric centering, spatial translations, rotations, and RMSD calculations.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must introduce the `msm.structure` module and spatial transformations.
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Geometric Centering (`get_center` and `center`)
* Must demonstrate calculating spatial centroids using `msm.structure.get_center()` and centering coordinates at the origin using `msm.structure.center()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.structure.get_center`.

### 3. Section 2: Spatial Translation (`translate`)
* Must demonstrate translating coordinates along 3D vectors with unit safety using `msm.structure.translate()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.structure.translate`.

### 4. Section 3: Structural Alignment and RMSD (`get_rmsd` and `least_rmsd_align`)
* Must demonstrate computing Root-Mean-Square Deviation using `msm.structure.get_rmsd()` and performing rigid superposition with `msm.structure.least_rmsd_align()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.structure.get_rmsd`.

### 5. Challenge & See Also
* Must include **Challenge 16: The Structural Master** using T4 Lysozyme (`181L`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-16-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 15 and Module 17.
