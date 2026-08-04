# Module 16 Content Governance (`16_Merging_and_Growing_Systems.AGENTS.md`)

This document defines the **non-negotiable content contract** for `16_Merging_and_Growing_Systems.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Merging and Growing Systems** using MolSysMT's four primary composition functions: `msm.merge()`, `msm.add()`, `msm.concatenate_structures()`, and `msm.append_structures()`.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must introduce the 2x2 matrix of system composition (Topology/Elements vs Structure/Frames; Out-of-place vs In-place).
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Merging Systems (`msm.merge`)
* Must demonstrate out-of-place fusion of multiple independent systems into a new complex using `msm.merge()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.merge`.

### 3. Section 2: Adding Elements In-Place (`msm.add`)
* Must demonstrate in-place element/molecule addition to an existing system using `msm.add()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.add`.

### 4. Section 3: Concatenating Trajectory Frames (`msm.concatenate_structures`)
* Must demonstrate out-of-place frame concatenation across multiple matching systems using `msm.concatenate_structures()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.concatenate_structures`.

### 5. Section 4: Appending Frames In-Place (`msm.append_structures`)
* Must demonstrate in-place frame appending onto an existing trajectory using `msm.append_structures()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.append_structures`.

### 6. Challenge & See Also
* Must include **Challenge 16: The Systems Builder** and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-16-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 15 and Module 17.
