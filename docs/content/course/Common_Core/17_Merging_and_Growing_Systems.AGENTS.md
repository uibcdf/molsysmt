# Module 17 Content Governance (`17_Merging_and_Growing_Systems.AGENTS.md`)

This document defines the **non-negotiable content contract** for `17_Merging_and_Growing_Systems.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Merging and Growing Systems** using MolSysMT's four primary composition functions: `msm.merge()`, `msm.add()`, `msm.concatenate_structures()`, and `msm.append_structures()`.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must introduce the 2x2 matrix of system composition with row headers **`Topology`** and **`Structures`**.
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Merging Independent Systems (`msm.merge`)
* Must demonstrate out-of-place fusion of T4 Lysozyme protein (`molecule_type == "protein"`) and small molecule ligand (`molecule_type == "small molecule"`) into a new complex using `msm.merge()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.merge`.

### 3. Section 2: Adding Elements In-Place (`msm.add`)
* Must demonstrate in-place element/molecule addition to an existing system using `msm.add()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.add`.

### 4. Section 3: Concatenating Structures (`msm.concatenate_structures`)
* Must demonstrate out-of-place structure concatenation across multiple matching systems using `msm.concatenate_structures()`.
* Must avoid "frames" or "trajectories" terminology in favor of "structures".
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.concatenate_structures`.

### 5. Section 4: Appending Structures In-Place (`msm.append_structures`)
* Must demonstrate in-place structure appending onto an existing system using `msm.append_structures()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.append_structures`.

### 6. Challenge & See Also
* Must include **Challenge 17: The Systems Builder** using T4 Lysozyme (`181L`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-merging-and-growing-systems-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 16 and Module 18.
