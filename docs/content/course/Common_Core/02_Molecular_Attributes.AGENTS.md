# Module 02 Content Governance (`02_Molecular_Attributes.AGENTS.md`)

This document defines the **non-negotiable content contract** for `02_Molecular_Attributes.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Molecular Attributes** as one of the two foundational pillars of MolSysMT (alongside **Forms**).

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block & Glossary
* Must feature the **Glossary: Attribute** admonition (````{admonition} Glossary: Attribute\n:class: dropdown info`) with an active cross-reference link to the User Guide Foundations documentation (`{ref}`user-foundations``).
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: What is a Molecular Attribute?
* Must define an **Attribute** as any standardized data property describing a molecular system's identity, topology, spatial structure, chemical state, or physical mechanics.
* Must explain the 4 semantic categories of attributes: Topological, Structural, Chemical-State, and Mechanical.
* Must include a collapsible **Terminology Note** (`:::{note}\n:class: dropdown`) with the bold header line `**Terminology Note: "Group" vs. "Residue"**` explaining why MolSysMT uses the universal term **`group`** instead of "residue" (which is chemically inaccurate for waters, ions, lipids, or small-molecule drugs).
* Must demonstrate checking attribute presence with `msm.has_attribute()` and listing available attributes with `msm.get_attributes()`.

### 3. Section 2: Extracting Attributes (`msm.get()`)
* Must introduce **`msm.get()`** with a smooth narrative transition introducing an example query for `atom_name`, `group_name`, and `coordinates` for the first three atoms.
* Must explain and demonstrate the invariant 3D coordinate array shape `(n_structures, n_atoms, 3)`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.get``.

### 4. Section 3: Modifying Attributes (`msm.set()`)
* Must introduce **`msm.set()`** as the form-agnostic modification engine for updating attributes in mutable objects (`molsysmt.MolSys`).
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.set``.

### 5. Challenge & See Also
* Must include **Challenge 2: The Attribute Master** using SARS-CoV-2 Protease (`pdb_id:6LU7`) and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-02-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 1 and Module 3.
