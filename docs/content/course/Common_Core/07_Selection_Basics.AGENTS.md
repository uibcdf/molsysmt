# Module 07 Content Governance (`07_Selection_Basics.AGENTS.md`)

This document defines the **non-negotiable content contract** for `07_Selection_Basics.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Selection Mechanism** using MolSysMT's universal selection engine **`msm.select()`**.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Index & List-Based Selections
* Must demonstrate selecting all items (`'all'`) or explicit index lists using `msm.select()`.

### 3. Section 2: Boolean Attribute Expressions & Logical Operators
* Must demonstrate boolean expressions (`atom_name`, `group_name`, `molecule_type`) combined with logical operators (`and`, `or`, `not`).
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.select`.

### 4. Section 3: Element-Scoped Selections
* Must demonstrate scoping query outputs to specific structural elements using `element=...` (`group`, `molecule`, `chain`).

### 5. Section 4: Spatial & Proximity Selections
* Must demonstrate distance-based proximity queries using the `within` operator.

### 6. Section 5: Connectivity Selections
* Must demonstrate topological connectivity queries using the `all bonded to ...` operator.

### 7. Challenge & See Also
* Must include **Challenge 7: The Selection Master** using SARS-CoV-2 Protease (`pdb_id:6LU7`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-selection-basics-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 6 and Module 8.
