# Module 14 Content Governance (`14_Covalent_Connectivity.AGENTS.md`)

This document defines the **non-negotiable content contract** for `14_Covalent_Connectivity.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Covalent Connectivity** in MolSysMT (bonded atom pairs, covalent blocks, connectivity-based selections, bond inference, and NetworkX Graph conversion).

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Extracting Covalent Bonds
* Must demonstrate querying `bonded_atom_pairs` using `msm.get(lysozyme, element='system', bonded_atom_pairs=True)`.

### 3. Section 2: Topological Analysis
* Must demonstrate extracting independent connected sets using `msm.topology.get_covalent_blocks()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.topology.get_covalent_blocks`.

### 4. Section 3: Selection by Connectivity
* Must demonstrate selecting atoms using connectivity operators (`selection='all bonded to atom_index==10'`).

### 5. Section 4: Reconstructing Missing Bonds
* Must demonstrate bond inference on unbonded PDB files using `msm.build.add_missing_bonds()`.

### 6. Section 5: NetworkX Graph Conversion
* Must demonstrate converting a molecular topology to a `networkx.Graph` object (`msm.convert(sys, to_form='networkx.Graph')`).

### 7. Challenge & See Also
* Must include **Challenge 14: The Bond Detective** using T4 Lysozyme (`lysozyme`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-14-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 13 and Module 15.
