# Module 12 Content Governance (`12_Building_Repairing_and_Auditing_Systems.AGENTS.md`)

This document defines the **non-negotiable content contract** for `12_Building_Repairing_and_Auditing_Systems.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Building, Repairing and Auditing Systems** using MolSysMT's `msm.build` module.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must include the **`msm.build` Function Overview** text before the glossary box, detailing the three functional pillars (`Audit and Inspection`, `Repair and Completion`, `Synthesis and Solvation`).
* Must feature the **Glossary Box** titled `Glossary: MolSysMT modules` explaining `msm.basic` vs `msm.build` (clarifying they are function modules, not submodules).
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Auditing Anomalies
* Must demonstrate detecting non-standard groups and sequence gaps using `msm.build.get_non_standard_residues()`, `msm.build.get_missing_residues()`, and `msm.build.has_hydrogens()` on T4 Lysozyme (`lysozyme`).
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.build.get_non_standard_residues`.

### 3. Section 2: Repairing Missing Atoms
* Must demonstrate system repair by adding missing hydrogens using `msm.build.add_missing_hydrogens()`.

### 4. Section 3: Reconstructing Covalent Bonds
* Must demonstrate auditing missing covalent bonds using `msm.build.get_missing_bonds()` and reconstructing bonds using `msm.build.add_missing_bonds()`.

### 5. Challenge & See Also
* Must include **Challenge 12: The Quality Auditor** using T4 Lysozyme (`pdb_id:181L`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-12-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 11 and Module 13.
