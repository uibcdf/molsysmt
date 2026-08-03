# Module 14 Content Governance (`15_Comparing_Systems.AGENTS.md`)

This document defines the **non-negotiable content contract** for `15_Comparing_Systems.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Comparing Systems** using MolSysMT's universal comparator function **`msm.compare()`**.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Basic Topology Comparison
* Must demonstrate verifying system equality across different forms using `msm.compare(sys1, sys2)`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.compare`.

### 3. Section 2: Selective Attribute Comparison
* Must demonstrate comparing specific attribute types (e.g. `attribute_type='topological'` vs. `attribute_type='structural'`).

### 4. Section 3: Detailed Difference Auditing
* Must demonstrate extracting dictionary reports using `output_type='dictionary'` to diagnose attribute mismatches.

### 5. Challenge & See Also
* Must include **Challenge 14: The System Comparator** using T4 Lysozyme (`lysozyme`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-14-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 14 and Module 16.
