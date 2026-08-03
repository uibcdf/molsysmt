# Module 16 Content Governance (`16_Semantic_Labeling.AGENTS.md`)

This document defines the **non-negotiable content contract** for `16_Semantic_Labeling.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Semantic Labeling** in MolSysMT using `msm.get_label()`.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Default Labeling
* Must demonstrate extracting standard human-readable nomenclature strings using `msm.get_label()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.get_label`.

### 3. Section 2: Custom Formatting Templates
* Must demonstrate custom string formatting templates using attribute tokens (e.g. `label='{group_name}:{group_id}'`).

### 4. Section 3: Batch Labeling
* Must demonstrate batch labeling for selections of atoms or groups to build clean labels for reports or legends.

### 5. Challenge & See Also
* Must include **Challenge 16: The Semantic Labeler** using T4 Lysozyme (`lysozyme`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-16-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 15 and Module 17.
