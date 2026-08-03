# Module 11 Content Governance (`11_Navigating_Between_Levels.AGENTS.md`)

This document defines the **non-negotiable content contract** for `11_Navigating_Between_Levels.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Navigating Between Hierarchical Levels** (`atom`, `group`, `component`, `molecule`, `chain`, `entity`, `system`) using `msm.get()` and `msm.select()`.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Upward Hierarchical Mapping
* Must demonstrate querying parent properties (e.g., `group_name`, `group_index`, `chain_id`) from child selections (e.g., atom indices).

### 3. Section 2: Downward Hierarchical Mapping
* Must demonstrate querying constituent child elements (e.g. `atom_index`, `group_index`) from parent selections (e.g. `entity_name == "BENZENE"` or chain selections).

### 4. Section 3: Cross-Level Summaries
* Must demonstrate extracting cross-level element counts (e.g., `n_groups` or `n_atoms` per chain) across structural levels.

### 5. Challenge & See Also
* Must include **Challenge 11: The Hierarchy Traveler** using T4 Lysozyme (`lysozyme`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-11-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 10 and Module 12.
