# Module 13 Content Governance (`13_Topological_Analysis.AGENTS.md`)

This document defines the **non-negotiable content contract** for `13_Topological_Analysis.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Topological Analysis** using MolSysMT's `msm.topology` module.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must introduce the **`msm.topology`** function module for non-spatial topological properties, explicitly defining its utility and listing key functions (`get_covalent_blocks()`, `get_covalent_paths()`, `get_sequence_alignment()`, `get_sequence_identity()`).
* Must NOT include a glossary box.
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Covalent Blocks and Paths
* Must demonstrate partitioning connected covalent components using `msm.topology.get_covalent_blocks()` and cutting bonds with `remove_bonds`.
* Must demonstrate measuring topological covalent paths using `msm.topology.get_covalent_paths()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.topology.get_covalent_blocks`.

### 3. Section 2: Sequence Alignment and Identity
* Must demonstrate sequence alignment and sequence identity calculations using `msm.topology.get_sequence_alignment()` and `msm.topology.get_sequence_identity()` comparing T4 Lysozyme (`181L`) with T4 Lysozyme variant (`5X33`).

### 4. Challenge & See Also
* Must include **Challenge 13: The Sequence & Topology Master** using T4 Lysozyme (`181L`) and T4 Lysozyme variant (`5X33`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-covalent-connectivity-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 12 and Module 14.
