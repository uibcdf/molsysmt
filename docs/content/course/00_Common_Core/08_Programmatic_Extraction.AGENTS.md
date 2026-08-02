# Module 08 Content Governance (`08_Programmatic_Extraction.AGENTS.md`)

This document defines the **non-negotiable content contract** for `08_Programmatic_Extraction.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Extracting Molecular Attributes** using MolSysMT's form-agnostic retrieval engine **`msm.get()`**.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).
* **Note:** This module intentionally does **not** include a Glossary box.

### 2. Section 1: Extracting Single Attributes
* Must demonstrate extracting single attributes (e.g. `atom_name`, `n_atoms`) into direct Python primitives or NumPy arrays.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.get``.

### 3. Section 2: Extracting Multiple Attributes & Tuple Unpacking
* Must demonstrate extracting multiple attributes simultaneously (e.g. `atom_id`, `atom_name`, `atom_type`) using structured tuple unpacking.

### 4. Section 3: Extracting Coordinate Tensors & Spatial Geometry
* Must demonstrate retrieving 3D coordinate arrays and explain the invariant array shape `(n_structures, n_atoms, 3)`.
* Must demonstrate combining selection queries (`selection='molecule_type == "protein"'`) with coordinate extraction.

### 5. Section 4: Extracting Periodic Box Properties
* Must demonstrate extracting periodic box vectors (`box`), lengths (`box_lengths`), angles (`box_angles`), and volumes (`box_volume`).

### 6. Challenge & See Also
* Must include **Challenge 8: The Data Scientist** using T4 Lysozyme (`lysozyme`), computing geometric centers with `numpy.mean()`, and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-08-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 7 and Module 9.
