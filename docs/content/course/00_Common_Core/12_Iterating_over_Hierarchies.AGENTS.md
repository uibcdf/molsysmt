# Module 12 Content Governance (`12_Iterating_over_Hierarchies.AGENTS.md`)

This document defines the **non-negotiable content contract** for `12_Iterating_over_Hierarchies.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Iterating over Hierarchies** using MolSysMT's chunked streaming engine **`msm.Iterator()`**.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Biological Element Loops
* Must demonstrate iterating over biological levels (e.g. `group`, `chain`) yielding requested attributes (e.g. `group_name`, `atom_index`).
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.Iterator`.

### 3. Section 2: Chunked Iteration
* Must demonstrate processing elements in batches using the `chunk` parameter in `msm.Iterator()`.

### 4. Section 3: Trajectory Structure Iteration
* Must demonstrate iterating over trajectory structures step by step using `msm.Iterator(villin_traj, coordinates=True)` without loading full trajectories into RAM.

### 5. Challenge & See Also
* Must include **Challenge 12: The Efficient Coder** using T4 Lysozyme (`lysozyme`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-12-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 11 and Module 13.
