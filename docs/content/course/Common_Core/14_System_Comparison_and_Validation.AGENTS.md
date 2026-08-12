# Module 14 Content Governance (`14_System_Comparison_and_Validation.AGENTS.md`)

This document defines the **non-negotiable content contract** for `14_System_Comparison_and_Validation.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **System Comparison and Validation** using MolSysMT's `msm.contains()`, `msm.is_composed_of()`, and `msm.compare()` functions.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must introduce system validation and comparison across data forms.
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Checking What a System Contains
* Must demonstrate testing attribute or element presence using `msm.contains()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.contains`.

### 3. Section 2: Verifying System Composition
* Must demonstrate verifying element counts and molecule composition using `msm.is_composed_of()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.is_composed_of`.

### 4. Section 3: Comparing Systems Across Forms
* Must demonstrate form-agnostic comparison across data forms using `msm.compare()`.
* Must demonstrate detailed attribute mismatch auditing using `output_type='dictionary'`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.compare`.

### 5. Challenge & See Also
* Must include **Challenge 14: The System Validator** using T4 Lysozyme (`lysozyme`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-comparing-systems-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 13 and Module 15.
