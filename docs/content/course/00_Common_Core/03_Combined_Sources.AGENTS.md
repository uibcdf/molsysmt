# Module 03 Content Governance (`03_Combined_Sources.AGENTS.md`)

This document defines the **non-negotiable content contract** for `03_Combined_Sources.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents MolSysMT's ability to virtually assemble a single molecular system from multiple complementary data sources passed as a Python list.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Section 1: The Virtual Multi-Source System
* Must introduce the concept of passing a list of complementary forms (e.g. topology from an H5MSM file and trajectory from a DCD file) as a single virtual system.
* Must validate the list using `msm.is_a_molecular_system()` and inspect its canonical form string using `msm.get_form()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.is_a_molecular_system``.

### 2. Section 2: Attribute Precedence & `msm.where_is_attribute()`
* Must explain MolSysMT's precedence rule (the first item in the list providing a given attribute takes precedence).
* Must demonstrate how to query the exact source of attributes (`atom_name`, `coordinates`) using `msm.where_is_attribute()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.where_is_attribute``.

### 3. Section 3: Transparent Extraction & Coordinate Geometry (`msm.get()`)
* Must demonstrate unified attribute extraction across the composite list using `msm.get()`.
* Must explain the inviolable 3D coordinate array shape invariant `(n_structures, n_atoms, 3)`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.get``.
