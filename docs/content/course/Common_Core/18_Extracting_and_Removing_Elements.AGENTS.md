# Module 18 Content Governance (`18_Extracting_and_Removing_Elements.AGENTS.md`)

This document defines the **non-negotiable content contract** for `18_Extracting_and_Removing_Elements.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents sub-system extraction and removal operations using `msm.extract()` and `msm.remove()`.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must introduce extraction and removal operations (`msm.extract()`, `msm.remove()`).
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Extracting Sub-Systems (`msm.extract`)
* Must demonstrate creating an independent sub-system using `msm.extract()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.extract`.

### 3. Section 2: Removing Elements (`msm.remove`)
* Must demonstrate purging unwanted components (water, ions) using `msm.remove()`.

### 4. Challenge & See Also
* Must include **Challenge 18: The Subsystem Specialist** using T4 Lysozyme (`181L`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-18-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 17 and Module 19.
