# Module 12 Content Governance (`12_Building_Repairing_and_Auditing_Systems.AGENTS.md`)

This document defines the **non-negotiable content contract** for `12_Building_Repairing_and_Auditing_Systems.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module introduces the **`msm.build`** specialized function module, focusing on auditing structural anomalies, repairing missing hydrogens and covalent bonds, and synthesizing peptides from sequence.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must introduce `msm.build` functions (`add_missing_hydrogens`, `add_missing_bonds`, `build_peptide`).
* Must feature the **Glossary: MolSysMT modules** custom admonition (````{admonition} Glossary: MolSysMT modules\n:class: dropdown info`).
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Auditing Anomalies
* Must demonstrate auditing non-standard groups with `msm.build.get_non_standard_residues()` and checking hydrogen status with `msm.build.has_hydrogens()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.build.get_non_standard_residues`.

### 3. Section 2: Repairing Missing Atoms
* Must demonstrate repairing incomplete structures by adding missing hydrogens with `msm.build.add_missing_hydrogens()`.

### 4. Section 3: Reconstructing Covalent Bonds
* Must demonstrate auditing missing covalent connectivity with `msm.build.get_missing_bonds()` and reconstructing bonds with `msm.build.add_missing_bonds()`.

### 5. Section 4: Building Peptides from Sequence
* Must demonstrate synthesizing a 3D peptide structure from sequence using `msm.build.build_peptide()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.build.build_peptide`.

### 6. Challenge & See Also
* Must include **Challenge 12: The Quality Auditor** using T4 Lysozyme (`181L`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-12-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 11 and Module 13.
