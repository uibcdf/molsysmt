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
* Must distinguish the moving `selection`, contained `source_center_selection`, and mutually exclusive `target_coordinates` / initial `target_center_selection`, with executable examples for both destinations.

### 3. Section 2: Spatial Translation (`translate`)
* Must demonstrate translating coordinates along 3D vectors with unit safety using `msm.structure.translate()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.structure.translate`.
* Preserve the executable `move_away` comparison of automatic separation
  increments and explicit final offsets, the initial reference snapshot,
  single-structure scope and unchanged-system checks on rejection.
* Preserve reflection's default z plane, normal-scale invariance, inverse check,
  handedness distinction and unchanged chemical assignments.

### 4. Section 3: Structural Alignment and RMSD (`get_rmsd` and `least_rmsd_align`)
* Must demonstrate computing Root-Mean-Square Deviation using `msm.structure.get_rmsd()` and performing rigid superposition with `msm.structure.least_rmsd_align()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.structure.get_rmsd`.

### 5. Challenge & See Also
* Must include **Challenge 16: The Structural Master** using T4 Lysozyme (`181L`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-structural-operations-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 15 and Module 17.

Preserve the experimental addon bridge for native minimization: independent
outputs by default, explicit in-place retained-axis coordinates, projection-only
deferral/retry, native analysis invalidation and bounded single-structure CPU
receiving. Keep local optimization distinct from equilibrium or global stability.

Preserve the source-qualified Analysis bridge for raw/optimal RMSD, gyration and
RMSF. Their calculations do not edit or automatically align source coordinates.
Distinguish positional reference correspondence, per-structure scalar series and
per-atom fluctuations. Core trajectory plots require complete canonical structure
coverage; no repeated/subset or atom axis is padded or relabelled to fit it.


Preserve the Geometry/Rotate bridge: molecular-axis signed angle with explicit
degree/radian units, per-structure unweighted selection center as the GUI
default, explicit origin/fixed point alternatives, serialized apply-time native
centers and full independent results. Keep the camera and box distinction,
minimum-image limits, unchanged native expert defaults and projection-only retry.


Preserve the principal-axis GUI bridge's separate moving/reference populations,
inertia/covariance and weight choices, center restoration/subtraction and row
basis targets. State arbitrary signs, degeneracy and disjoint-reference limits;
keep native all-structure preflight and shared result/sync ownership separate
from remaining external-reference and sequence-matching GUI workflows.


Preserve degeneracy diagnostics in the molecular-system structure-index space,
including the separate zero-based selection position and unchanged coordinates
and interaction coverage on all-structure preflight rejection. IDs remain labels.
