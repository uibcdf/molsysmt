# Module 04 Content Governance (`04_Combined_Forms.AGENTS.md`)

This document defines the **non-negotiable content contract** for `04_Combined_Forms.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents MolSysMT's ability to virtually assemble a single molecular system from multiple complementary data forms passed as a Python list, and to consolidate multi-forms into a single native form.

Any future revision or enhancement of this notebook **MUST preserve** the following 4 sections and essential explanations:

### 1. Section 1: The Virtual Multi-Form System
* Must introduce the concept of passing a list of complementary forms (e.g. topology from an H5MSM file and trajectory from a DCD file) as a single virtual system.
* Must validate the list using `msm.is_a_molecular_system()` and inspect its canonical form string using `msm.get_form()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.is_a_molecular_system``.

### 2. Section 2: Attribute Precedence & `msm.where_is_attribute()`
* Must explain MolSysMT's precedence rule (the first item in the list providing a given attribute takes precedence).
* Must demonstrate how to query the exact source of attributes (`atom_name`, `coordinates`) using `msm.where_is_attribute()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.where_is_attribute``.

### 3. Section 3: Querying Attributes Across Multi-Forms (`msm.get()`)
* Must demonstrate unified attribute extraction across the composite list using `msm.get()`.
* Must explain the invariant 3D coordinate array shape `(n_structures, n_atoms, 3)`.

### 4. Section 4: Consolidating Multi-Forms into a Single Form (`msm.convert()`)
* Must demonstrate converting a multi-form system list `[topology_file, trajectory_file]` into a single unified native object (e.g. `msm.convert(composite_system, to_form='molsysmt.MolSys')`).
* Must explain that consolidation merges separate topology and trajectory inputs into a single in-memory native structure or disk container.
