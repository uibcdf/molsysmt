# Module 04 Content Governance (`04_Native_Forms.AGENTS.md`)

This document defines the **non-negotiable content contract** for `04_Native_Forms.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents MolSysMT's native objects and the core philosophy surrounding the native orchestrator object **`molsysmt.MolSys`**.

Any future revision or enhancement of this notebook **MUST preserve** the following 4 sections and essential explanations:

### 1. Section 1: Presentation of `molsysmt.MolSys`
* Must introduce **`molsysmt.MolSys`** as the primary in-memory native orchestrator container of MolSysMT.
* Must naturally integrate the observation contrasting Python's internal `type(molsys)` with MolSysMT's canonical `msm.get_form(molsys)`.

### 2. Section 2: Domain Component Objects (`Topology`, `Structures`, `MolecularMechanics`)
* Must present component objects: `molsysmt.Topology`, `molsysmt.Structures`, and `molsysmt.MolecularMechanics`.
* Must explain the internal responsibilities of each component (e.g. `topology` for covalent graphs and biological hierarchies, `structures` for coordinate arrays `(n_structures, n_atoms, 3)` and periodic boxes, `molecular_mechanics` for forcefield parameters and energies).
* Must include explicit hyperlinked cross-references pointing to where deeper analysis of each domain can be found in future modules.

### 3. Section 3: Native Disk Storage (`file:h5msm`)
* Must present the **H5MSM** binary format (`file:h5msm`) as the HDF5-based disk counterpart of `molsysmt.MolSys`.
* Must explain its I/O performance advantages (chunked execution and trajectory streaming without full RAM loading).

### 4. Section 4: Native Dictionary Forms (`TopologyDict`, `StructuresDict`, `MolSysDict`)
* Must present lightweight native dictionary forms (`TopologyDict`, `StructuresDict`, `MolSysDict`).
* Must demonstrate transparent dictionary key lookup (e.g. `topo_dict.data['atoms']`) to showcase zero-overhead Python data access.
