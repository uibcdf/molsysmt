# Module 13 Content Governance (`13_Topological_Analysis.AGENTS.md`)

This document defines the **non-negotiable content contract** for `13_Topological_Analysis.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Topological Analysis** using MolSysMT's `msm.topology` module.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must include text introducing the **`msm.topology`** function module for non-spatial topological properties.
* Must feature the **Glossary Box** titled `Glossary: msm.topology module` explaining `msm.topology` vs 3D spatial properties (`msm.structure`).
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Covalent Blocks
* Must demonstrate partitioning connected covalent components using `msm.topology.get_covalent_blocks()` and cutting bonds with `remove_bonds`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.topology.get_covalent_blocks`.

### 3. Section 2: Topological Bond Graphs
* Must demonstrate extracting the topological bond graph as a `networkx.Graph` using `msm.topology.get_bondgraph()`.

### 4. Section 3: Covalent Paths
* Must demonstrate calculating shortest topological paths between atom pairs using `msm.topology.get_covalent_paths()`.

### 5. Challenge & See Also
* Must include **Challenge 13: The Topology Master** using T4 Lysozyme (`lysozyme`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-13-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 12 and Module 14.
