# Module 10 Content Governance (`10_Modifying_Molecular_Attributes.AGENTS.md`)

This document defines the **non-negotiable content contract** for `10_Modifying_Molecular_Attributes.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Modifying Molecular Attributes** using MolSysMT's primary setter function **`msm.set()`**, serving as the direct counterpart to `msm.get()` (Module 08).

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).
* Must explain the concept of **Modifiable Forms**: on-disk static files are non-modifiable; in-memory native objects like `molsysmt.MolSys` are modifiable.

### 2. Section 1: Modifiable Forms
* Must demonstrate converting a non-modifiable form to `molsysmt.MolSys` prior to modification.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.set``.

### 3. Section 2: Modifying Coordinates
* Must demonstrate updating atomic coordinates using `msm.set(molsys, element='atom', selection=..., coordinates=...)` using physical quantities or strings.

### 4. Section 3: Modifying Attributes
* Must demonstrate updating group names, chain IDs (e.g. changing chain 'A' to 'X'), or entity identifiers, and verifying changes using `msm.info()` or `msm.get()`.

### 5. Challenge & See Also
* Must include **Challenge 10: The Molecular Editor** using T4 Lysozyme (`lysozyme`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-10-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 9 and Module 11.
