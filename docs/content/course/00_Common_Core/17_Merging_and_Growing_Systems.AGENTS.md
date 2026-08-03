# Module 17 Content Governance (`17_Merging_and_Growing_Systems.AGENTS.md`)

This document defines the **non-negotiable content contract** for `17_Merging_and_Growing_Systems.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Merging and Growing Systems** using `msm.merge()`, `msm.add()`, and `msm.append_structures()`.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Merging Independent Systems
* Must demonstrate fusing two independent systems (e.g. protein and ligand in `molsysmt.MolSys` form) using `msm.merge()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.merge`.

### 3. Section 2: Adding Elements
* Must demonstrate appending selected elements into an existing modifiable system using `msm.add()`.

### 4. Section 3: Concatenating Trajectory Structures
* Must demonstrate joining trajectory structures along the time/structure axis using `msm.append_structures()`.

### 5. Challenge & See Also
* Must include **Challenge 17: The Systems Builder** using Villin Headpiece (`1vii.pdb`) and Benzamidine (`benzamidine.pdb`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-17-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 16 and Module 18.
