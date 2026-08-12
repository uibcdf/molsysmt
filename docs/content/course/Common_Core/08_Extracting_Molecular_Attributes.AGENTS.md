# Module 08 Content Governance (`08_Extracting_Molecular_Attributes.AGENTS.md`)

This document defines the **non-negotiable content contract** for `08_Extracting_Molecular_Attributes.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Extracting Molecular Attributes & Hierarchical Navigation** using MolSysMT's primary extraction engine **`msm.get()`**.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Extracting Single Attributes
* Must demonstrate extracting single properties into direct Python primitives and NumPy arrays using `msm.get()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.get`.

### 3. Section 2: Extracting Multiple Attributes
* Must demonstrate extracting multiple attributes simultaneously using tuple unpacking.

### 4. Section 3: Extracting Coordinate Tensors
* Must demonstrate extracting 3D coordinate tensors with shape `(n_structures, n_atoms, 3)`.

### 5. Section 4: Extracting Periodic Box Properties
* Must demonstrate extracting box lengths, angles, and volumes.

### 6. Section 5: Extracting Covalent Bonds
* Must demonstrate extracting the covalent bond matrix using `bonded_atom_pairs=True`.

### 7. Section 6: Upward Hierarchical Mapping
* Must demonstrate querying parent properties (e.g. `group_name`, `group_index`, `chain_id`) from child selections (e.g. atom indices).

### 8. Section 7: Downward Hierarchical Mapping
* Must demonstrate querying constituent child elements (e.g. `atom_index`) from parent selections (e.g. `entity_name == "BENZENE"`).

### 9. Section 8: Cross-Level Summaries
* Must demonstrate extracting cross-level element counts (e.g. `n_groups` per chain).

### 10. Challenge & See Also
* Must include **Challenge 8: The Data Scientist** using T4 Lysozyme (`lysozyme`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-programmatic-extraction-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 7 and Module 9.
