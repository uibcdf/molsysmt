# Module 17 Content Governance (`18_Surgical_Extraction_and_Removal.AGENTS.md`)

This document defines the **non-negotiable content contract** for `18_Surgical_Extraction_and_Removal.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Surgical Extraction and Removal** using `msm.extract()`, `msm.remove()`, and `msm.copy()`.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Extracting Sub-Systems
* Must demonstrate extracting specific molecular sub-systems into a new object using `msm.extract()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.extract`.

### 3. Section 2: Removing Elements
* Must demonstrate purging unwanted components (e.g. water or ions) using `msm.remove()`.

### 4. Section 3: Duplicating Systems
* Must demonstrate creating true independent deep copies using `msm.copy()`.

### 5. Challenge & See Also
* Must include **Challenge 17: The Molecular Surgeon** using T4 Lysozyme (`lysozyme`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-17-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 17 and Module 19.
