# Module 18 Content Governance (`19_Structures_and_Trajectories.AGENTS.md`)

This document defines the **non-negotiable content contract** for `19_Structures_and_Trajectories.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Structures and Trajectories** in MolSysMT (the universal technical term `structure`, coordinate array shapes `(n_structures, n_atoms, 3)`, and slicing with `structure_indices`).

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Structural Invariants
* Must explain the universal technical term **`structure`** (`n_structures`, array shape `(n_structures, n_atoms, 3)`).

### 3. Section 2: Slicing Trajectories
* Must demonstrate extracting structural coordinates for specific frames using `structure_indices` in `msm.get()`.

### 4. Challenge & See Also
* Must include **Challenge 18: The Trajectory Master** using Villin Headpiece trajectory (`villin_traj`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-18-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 18 and Module 20.
