# Module 02 Content Governance (`02_Molecular_Attributes.AGENTS.md`)

This document defines the **non-negotiable content contract** for `02_Molecular_Attributes.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Molecular Attributes** as one of the two foundational pillars of MolSysMT (alongside **Forms**).

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Section 1: What is a Molecular Attribute?
* Must define an **Attribute** as any data property describing a molecular system's identity, topology, spatial structure, chemical state, or physical mechanics.
* Must explain the semantic classification of attributes (Topological, Structural, Chemical, Mechanical).
* Must demonstrate checking attribute availability with `msm.has_attribute()` and listing available attributes with `msm.get_attributes()`.

### 2. Section 2: Extracting Attributes (`msm.get()`)
* Must introduce **`msm.get()`** as the form-agnostic extraction engine for querying attributes.
* Must explain and demonstrate the invariant 3D coordinate array shape `(n_structures, n_atoms, 3)`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.get``.

### 3. Section 3: Modifying Attributes (`msm.set()`)
* Must introduce **`msm.set()`** as the form-agnostic modification engine for updating attributes in a system.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.set``.
