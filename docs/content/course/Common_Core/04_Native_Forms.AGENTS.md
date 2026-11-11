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

### 2. Section 2: Domain Component Objects (`Topology`, `ChemicalStates`, `Structures`, `MolecularMechanics`)
* Must present component objects: `molsysmt.Topology`, `molsysmt.ChemicalStates`, `molsysmt.Structures`, and `molsysmt.MolecularMechanics`.
* Must explain the responsibilities of each component (`topology` for stable
  inventory and hierarchy, `chemical_states` for covalent bonds and assignments,
  `structures` for coordinates `(n_structures, n_atoms, 3)`, periodic boxes and
  per-structure observables including energies, `molecular_mechanics` for model
  requests, parameters and assignment reports).
* Distinguish registered native form names from Python constructors. Direct
  class construction uses `molsysmt.native`; not every form name is a root export.
* Must explain that Topology has no bonds/components/state facade; ChemicalStates is independently owned by MolSys.
* Preserve declared ChemicalStates/Structures composition without topology,
  ordered index selection and unknown multi-state structure association.
* Preserve the executed stored-axis query example: selected-state counts and
  component indices, collection-wide state inventory and unchanged reference.
* Retain the executed stored-field example: absent formal charges remain None,
  unknown bond fields retain edge cardinality and nullable stereo-reference pairs.
* Must include explicit hyperlinked cross-references pointing to where deeper analysis of each domain can be found in future modules.

### 3. Section 3: Native Disk Storage (`file:h5msm`)
* Must present the **H5MSM** binary format (`file:h5msm`) as the HDF5-based disk counterpart of `molsysmt.MolSys`.
* Explain chunk-oriented coordinate I/O while distinguishing supported iteration
  from resident conversion and layer reads. Do not promise constant-memory
  loading or a modular file-backed handler.
* Preserve default 1.0 writing and the executed small charge/coordinate round
  trip, explicit mechanics-free 0.5, experimental 0.6 and legacy 0.3/0.4 warning
  and migration routes. The named `migrate_to_05` helper still writes 0.5.

### 4. Section 4: Native Dictionary Forms (`TopologyDict`, `StructuresDict`, `MolSysDict`)
* Must present lightweight native dictionary forms (`TopologyDict`, `StructuresDict`, `MolSysDict`).
* Must demonstrate transparent dictionary key lookup (e.g. `topo_dict.data['atoms']`) to showcase zero-overhead Python data access.
* Must distinguish the typed NumPy column payloads in `ChemicalStatesDict` and `InteractionsDict` from JSON-compatible record dictionaries.

Preserve the executed ChemicalStatesDict direct-read example, selected-state bounds,
ordered/repeated positions and unchanged reference. Queries do not decode unrelated
states or history; raw dictionary mutation is not a controlled editing interface.

Retain controlled typed field assignment and state-aware count predicate examples.
Preserve compact group-name declarations, the sequence alphabet, native sequence
projection and pending other consumer migration, including unknown new groups,
persistence and interaction invalidation.
Retain explicit conversion source context, selected-group contradiction refusal
and unchanged input declarations during one-letter queries.


Preserve InteractionsDict's complete evidence table/code identity through .h5i
and named H5MSM persistence, including unused labels after invalidation. Keep
producer identity and evaluated-empty versus unevaluated coverage distinct.

Preserve the single-path H5MSM 0.5 whole-Topology projection with default
selection/context options: resident
stable inventory only, no unrelated domain payloads, explicit contextual-route
and requested-layer validation limits. Do not imply a constant-memory load.
