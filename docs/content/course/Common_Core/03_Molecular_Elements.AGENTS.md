# Module 03 Content Governance (`03_Molecular_Elements.AGENTS.md`)

This document defines the **non-negotiable content contract** for `03_Molecular_Elements.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Molecular Elements** as the third foundational pillar of MolSysMT (alongside **Forms** and **Attributes**).

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block & Glossary
* Must feature the **Glossary: Element** admonition (````{admonition} Glossary: Element\n:class: dropdown info`) defining `element` as the structural hierarchy level (`atom`, `group`, `component`, `molecule`, `chain`, `entity`, `system`) with a link to `{ref}`user-foundations``.
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: The 6 Hierarchical Elements
* Must define and explain the 6 canonical element levels: `atom`, `group`, `component`, `molecule`, `chain`, and `entity`.
* Must explain how `element` parameter scopes operations in MolSysMT functions.

### 3. Section 2: Auditing Hierarchies (`msm.info(element=...)`)
* Must demonstrate filtering biological summaries by element level using `msm.info(system, element=...)`.

### 4. Section 3: Extracting Element Counts & Attributes (`msm.get(element=...)`)
* Must demonstrate querying element counts (`n_groups`, `n_molecules`, `n_chains`) and element-specific attributes using `msm.get(system, element=...)`.
* **Pedagogical Boundary:** `msm.select()` is intentionally **omitted** from this module as selection syntax is introduced later in the course (Modules 07 & 08). Do not introduce `msm.select()` here.

### 5. Challenge & See Also
* Must include **Challenge 3: The Hierarchy Architect** using SARS-CoV-2 Protease (`pdb_id:6LU7`) evaluated with `msm.info()` and `msm.get()`, and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-molecular-elements-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 2 and Module 4.
