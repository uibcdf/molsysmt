# Module 10 Content Governance (`10_Modifying_Molecular_Attributes.AGENTS.md`)

This document defines the **non-negotiable content contract** for `10_Modifying_Molecular_Attributes.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents attribute modification using `msm.set()` and deep system copying using `msm.copy()`.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must introduce form modifiability and `msm.set()`.
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Modifiable Forms
* Must explain why static files require conversion to modifiable forms (`molsysmt.MolSys`).
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.set`.

### 3. Section 2: Modifying Coordinates
* Must demonstrate updating 3D atomic coordinates using `msm.set(..., coordinates=...)`.

### 4. Section 3: Modifying Attributes
* Must demonstrate updating topology identifiers (such as `chain_id`).

### 5. Section 4: Duplicating Systems Before Modification
* Must demonstrate deep copying objects with `msm.copy()` before applying in-place modifications.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.copy`.

### 6. Challenge & See Also
* Must include **Challenge 10: The Molecular Editor** using T4 Lysozyme (`181L`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-10-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 9 and Module 11.
