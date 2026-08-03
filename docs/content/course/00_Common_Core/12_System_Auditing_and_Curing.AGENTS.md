# Module 12 Content Governance (`13_System_Auditing_and_Curing.AGENTS.md`)

This document defines the **non-negotiable content contract** for `13_System_Auditing_and_Curing.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **System Auditing and Curing** using MolSysMT's `msm.build` audit submodule.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Identifying Non-Standard Groups
* Must demonstrate detecting non-standard groups or co-crystallized ligands using `msm.build.get_non_standard_residues()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.build.get_non_standard_residues`.

### 3. Section 2: Detecting Missing Gaps & Atoms
* Must demonstrate detecting sequence gaps and missing heavy atoms using `msm.build.get_missing_residues()` and `msm.build.get_missing_heavy_atoms()`.

### 4. Section 3: Auditing Covalent Bonds
* Must demonstrate auditing missing covalent connectivity and disulfide bridges using `msm.build.get_missing_bonds()` and `msm.build.get_disulfide_bonds()`.

### 5. Challenge & See Also
* Must include **Challenge 12: The Quality Auditor** using SARS-CoV-2 Protease (`pdb_id:6LU7`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-12-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 12 and Module 14.
