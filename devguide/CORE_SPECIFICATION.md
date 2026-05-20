# MolSysMT Core Technical Specification (v1.0.0)

This document is the **Single Source of Truth** for the architectural invariants, object models, and core data structures of the MolSysMT framework.

---

## 1. High-Level Layout
The MolSysMT codebase is organized to separate high-level user verbs from low-level performance kernels and form-specific adapters.

```
molsysmt/
  basic/           # Universal Public API (get, set, convert, select, view, info)
  form/            # Adapters for 60+ external forms and files (Lazy Loading)
  native/          # Tier 1 Native Objects (MolSys, Topology, Structures)
  lib/             # Performance Kernels (Numba JIT, numeric math)
  build/           # System Construction, Repair, and Mutagenesis
  structure/       # Geometric and conformational analysis
  topology/        # Connectivity, sequence, and graph analysis
  physchem/        # Physicochemical property calculators
  pbc/             # Periodic Boundary Condition management
  hbonds/          # Hydrogen bond and non-covalent interaction networks
  third_party/     # Optional bridges to external engines (OpenMM, MDAnalysis)
  element/         # Canonical chemical knowledge and element-level helpers
  data/databases/  # Serialized topology templates and residue libraries
```

---

## 2. The Trinity: Native Data Model
MolSysMT treats every molecular system as an orchestration of three independent pillars. This separation allows for high-performance trajectory processing and memory-efficient analysis.

### 2.1 `molsysmt.native.MolSys`
The top-level orchestrator. It synchronizes a `Topology` and a `Structures` object.
- **Invariants:** `topology.n_atoms` must always equal `structures.n_atoms`.
- **Atomic Operations:** Public verbs like `extract` or `merge` are applied atomically to both components.

### 2.2 `molsysmt.native.Topology`
The static blueprint of the system. It manages identities, hierarchies, and connectivity.
- **Data Model:** Powered by specialized Pandas DataFrames (`Atoms_DataFrame`, `Groups_DataFrame`, etc.).
- **String ID Invariant:** All element IDs (`atom_id`, `group_id`, `molecule_id`, `chain_id`, `entity_id`) are stored as **strings** to ensure cross-format compatibility.
- **Orthogonal Hierarchies:** MolSysMT does not use a single linear hierarchy. It uses three specialized branches:
    1. **Semantic (Biological):** `Atom` $\subset$ `Group` $\rightarrow$ `Molecule` $\rightarrow$ `Entity`.
    2. **Connectivity (Physical):** `Atom` $\rightarrow$ `Component` (Sets of bonded atoms).
    3. **Structural (Spatial):** `Atom` $\rightarrow$ `Chain` (Sets of atoms sharing a chain ID).

### 2.3 `molsysmt.native.Structures`
The dynamic payload of the system. It manages time-dependent geometric and physical data.
- **Attributes:** Coordinates, velocities, box vectors, time, energies, and B-factors.
- **Centralized Logic:** `Structures` centralizes all low-level property access via methods (`get_coordinates`, `set_coordinates`, etc.).

---

## 3. Data Standards & Invariants

### 3.1 Numeric Tensors
- **Coordinates:** NumPy arrays with shape `(n_structures, n_atoms, 3)`.
- **Simulation Box:** NumPy arrays with shape `(n_structures, 3, 3)`.
- **Precision:** `float64` is the standard for internal MolSysMT native objects and kernels. `float32` is accepted during ingestion but promoted to `float64` at kernel boundaries.

### 3.2 Standard Units
MolSysMT enforces physical integrity via `molsysmt.pyunitwizard`.
- **Lengths:** Nanometers (nm).
- **Time:** Picoseconds (ps).
- **Energy:** kJ/mol.
- **Temperature:** Kelvin (K).

### 3.3 The "Group" Mandate
MolSysMT uses **"Group"** as the universal term for the first level of atomic aggregation. The term "Residue" is reserved strictly for amino acids and nucleotides in biological contexts. Calling a water molecule or an ion a "residue" is considered a topological error in MolSysMT.

---

## 4. Rebuild & Inference Logic
MolSysMT distinguishes between two layers:
1. **Public Element Layer (`molsysmt.element`):** Form-agnostic query helpers using dispatch and `get()`.
2. **Native Rebuild Layer (`molsysmt.native`):** Internal reconstruction of higher-order structures (molecules, entities) using graph logic over native tables.

### 4.1 Component vs Molecule: Orthogonal Concepts
In MolSysMT, `component` and `molecule` are distinct and orthogonal concepts.
- **Component:** A connected subgraph of atoms defined by **covalent bonds**.
- **Molecule:** A semantic chemical unit defined by **group types** within a chain.

**Rule:** One component may contain multiple molecules (e.g., a metal-ion chelated to a protein residue is ONE component but TWO molecules).

### 4.2 Molecule Inference Algorithm
Inference in `native/_topology_infer.py` uses group types to partition atoms into molecules within each chain:
- **Polymer types** (`amino acid`, `nucleotide`, etc.) extend the current molecule.
- **Standalone types** (`ion`, `water`, `small molecule`) each start their own molecule.

### 4.3 Canonical Fallback Rules
- `entity_index` is inferred from molecules (molecules with the same name and type map to the same entity).
- Water molecules are always collapsed into a single entity.
- Native rebuild must **never** depend on public dispatchers (`msm.get`, `msm.select`).

---

## 5. Persistence & Observability
- **H5MSM:** The canonical high-performance file format for MolSysMT systems.
- **SMonitor:** Every core operation must emit signals through `smonitor` for structured diagnostics and error traceability.
