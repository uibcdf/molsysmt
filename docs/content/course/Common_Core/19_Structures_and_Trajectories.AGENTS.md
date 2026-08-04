# Module 19 Content Governance (`19_Structures_and_Trajectories.AGENTS.md`)

This document defines the **non-negotiable content contract** for `19_Structures_and_Trajectories.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Structures and Trajectories**, detailing the universal technical term **`structure`** (coordinate array tensor shape `(n_structures, n_atoms, 3)`), inspecting structural attributes (`n_structures`, `structure_id`, `box`, `time`), and slicing conformational series using `structure_indices`.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must introduce structural ensembles and multi-structure datasets.
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Structural Invariants
* Must demonstrate querying `n_structures` using `msm.get(..., element='system', n_structures=True)`.
* Must feature the **Terminology Note: "Structure" vs. "Frame"** custom admonition box (````{admonition} Terminology Note: "Structure" vs. "Frame"\n:class: dropdown info`).

### 3. Section 2: Slicing Trajectories
* Must demonstrate extracting coordinates or box vectors for specific structures using `structure_indices` in `msm.get()`.

### 4. Challenge & See Also
* Must include **Challenge 19: The Trajectory Master** using T4 Lysozyme trajectory or demonstration system, and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-19-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 18 and Module 20.
