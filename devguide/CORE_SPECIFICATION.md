# MolSysMT Core Technical Specification (v1.0.0)

This document defines the maintained architectural invariants, object models,
and core data structures of MolSysMT. Current code and executable tests remain
the implementation evidence for these rules.

---

## 1. High-Level Layout
The MolSysMT codebase is organized to separate high-level user verbs from low-level performance kernels and form-specific adapters.

```
molsysmt/
  basic/           # Universal Public API (get, set, convert, select, view, info)
  form/            # Adapters for 60+ external forms and files (Lazy Loading)
  native/          # Tier 1 Native Objects (MolSys, Topology, Structures)
  lib/             # Compatibility facade for native Rust kernels
  build/           # System Construction, Repair, and Mutagenesis
  structure/       # Geometric and conformational analysis
  topology/        # Connectivity, sequence, and graph analysis
  physchem/        # Physicochemical property calculators
  pbc/             # Periodic Boundary Condition management
  interactions/    # Chemically classified interaction analyses by family
  hbonds/          # Compatibility path for hydrogen-bond analysis
  third_party/     # Optional bridges to external engines (OpenMM, MDAnalysis)
  element/         # Canonical chemical knowledge and element-level helpers
  data/databases/  # Serialized topology templates and residue libraries
```

---

## 2. Independent Native Domains
`MolSys` coordinates independently optional `Topology`, `ChemicalStates`,
`Structures` and named `Interactions` domains. `MolecularMechanics` remains an
experimental in-memory domain without H5MSM 0.5 persistence.

### 2.1 `molsysmt.native.MolSys`
The top-level orchestrator synchronizes the domains actually supplied.
- **Invariants:** Present domains with declared atom axes agree in cardinality;
  missing domains remain absent. Equality of counts is a shape check, not proof
  of molecular identity. Correspondence is declared by construction or mapping.
- **Coordinated Operations:** Extraction/removal/permutation apply shared maps to
  every represented dependent domain, preserving state associations and analyses.

### 2.2 `molsysmt.native.Topology`
The stable inventory manages atom identities and represented hierarchy. It owns
no chemical states, bonds or components, including when attached to MolSys.
- **Data Model:** Powered by specialized Pandas DataFrames (`Atoms_DataFrame`, `Groups_DataFrame`, etc.).
- **String ID Invariant:** All element IDs (`atom_id`, `group_id`, `molecule_id`, `chain_id`, `entity_id`) are stored as **strings** to ensure cross-format compatibility.
- **Orthogonal Hierarchies:** MolSysMT does not use a single linear hierarchy. It uses three specialized branches:
    1. **Semantic (Biological):** `Atom` $\subset$ `Group` $\rightarrow$ `Molecule` $\rightarrow$ `Entity`.
    2. **Represented chains:** ordered group memberships and/or atom chain indices.
    3. **Group-free molecules:** optional atom-aligned stable molecule membership;
       grouped atoms instead inherit their group's molecule. Neither reads chemistry.

### 2.3 `molsysmt.native.Structures`
The dynamic payload of the system. It manages time-dependent geometric and physical data.
- **Attributes:** Structure IDs, coordinates, velocities, box vectors, time,
  energies, temperature, B-factors, occupancy, alternate locations, and
  bioassembly metadata where available.
- **Centralized Logic:** `Structures` centralizes all low-level property access via methods (`get_coordinates`, `set_coordinates`, etc.).

### 2.4 `molsysmt.ChemicalStates`
The collection owns state-local bonds, atom assignments and components on a
shared atom-index axis. A standalone collection begins with zero states; ordinary
MolSys/Builder construction creates one explicitly unknown working state.
Absent chemistry, zero states, unknown connectivity and complete edge-free
connectivity are different conditions. State selection does not mutate the
reference or implicitly assign states to structures.

Graph tools live in `molsysmt.chemical_states`. Sequence alignment/identity and
stable represented chains remain in `molsysmt.topology`. Component reconstruction
uses stored edges and participation declarations; optional stable context labels
components without redefining molecules. Controlled edits stage changes and
interaction invalidation before publication. Live pandas tables are not a
validated editing boundary. See [native queries](native_queries.md).

---

## 3. Data Standards & Invariants

### 3.1 Numeric Tensors
- **Coordinates:** NumPy arrays with shape `(n_structures, n_atoms, 3)`.
- **Simulation Box:** NumPy arrays with shape `(n_structures, 3, 3)`.
- **Precision:** Native coordinates and box vectors are stored as `float64`.
  Double precision is the default kernel policy; selected paths may opt into the
  configured single-precision mode and must document their tolerances.

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
- **Component:** A selected state's stored graph partition under its declared
  bond participation and completeness; owned by ChemicalStates.
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
- A producer/builder may initially materialize a selected component partition as
  stable molecule membership when no better declaration exists. Subsequent graph
  edits never update that stable membership implicitly.

---

## 5. Persistence & Observability
- **H5MSM:** The canonical high-performance file format for MolSysMT systems.
  New files use modular root version 0.5 defined in
  [h5msm_format.md](h5msm_format.md). Versions 0.3/0.4 remain deprecated readable
  inputs with explicit migration. Topology layers 1/2 remain readable; layer 3
  carries optional stable group-free molecule membership.
- **Dictionary transport:** TopologyDict/MolSysDict writers use schema 0.2 with
  explicit independent domains and typed array/quantity transport. Readers retain
  the separate 0.1 interpretation. Unsupported extensions/metadata are refused
  rather than omitted. Nonempty MolecularMechanics remains outside this schema.
- **SMonitor:** Public and failure-prone boundaries use the structured diagnostic
  catalog. Functions should remain silent on success unless telemetry is part of
  their documented contract; direct `print` calls are not a diagnostic channel.
