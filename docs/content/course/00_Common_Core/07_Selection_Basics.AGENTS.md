# Module 07 Content Governance (`07_Selection_Basics.AGENTS.md`)

This document defines the **non-negotiable content contract** for `07_Selection_Basics.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **MolSysMT's Selection Mechanism** as the primary unified querying engine (`msm.select()`).

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block & Glossary
* Must feature the **Glossary: Selection Mechanism** admonition (````{admonition} Glossary: Selection Mechanism\n:class: dropdown info`) with an active cross-reference link to `{ref}`user-foundations``.
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Index & List-Based Selections
* Must demonstrate direct integer and list selections (`selection=[0, 1, 2]`, `selection='all'`).

### 3. Section 2: Boolean Attribute Expressions & Logical Operators
* Must demonstrate attribute selection expressions (`atom_name`, `group_name`, `molecule_type`) combined with logical operators (`and`, `or`, `not`).

### 4. Section 3: Element-Scoped Selections (`element=...`)
* Must demonstrate scoping selection outputs to specific hierarchical elements using `msm.select(system, element='group', ...)`, `element='molecule'`, and `element='chain'`.

### 5. Section 4: Spatial & Proximity Selections
* Must demonstrate spatial distance selections (`within X nanometers of ...`).

### 6. Challenge & See Also
* Must include **Challenge 7: The Selection Master** using SARS-CoV-2 Protease (`pdb_id:6LU7`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-07-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 6 and Module 8.
