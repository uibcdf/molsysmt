# API Surface and Stability Classification

> **Status (updated 2026-03-23)**
>
> This document is the authoritative stability classification for the MolSysMT
> public API surface at `1.0.0`. It classifies each public namespace and its
> exported functions into one of three tiers:
>
> - **Stable** — contractually guaranteed for the `1.x` line; regressions are
>   patch-priority; semantics will not change without a formal deprecation cycle.
> - **Experimental** — publicly available but not contractually guaranteed;
>   signatures or behavior may change in `1.x` minor releases without formal
>   deprecation.
> - **Outside contract** — present in the codebase but explicitly excluded from
>   the `1.0.0` support contract; may be promoted in later releases.

---

## 1. What counts as public API

The public API is defined by symbols imported in `molsysmt/__init__.py`.
Anything not imported there is internal. Modules under `molsysmt/_private` are
internal implementation details and must not be re-exported.

---

## 2. Stability classification by namespace

### 2.1 Root-level exports (`import molsysmt as msm`)

| Symbol | Stability | Notes |
| :--- | :---: | :--- |
| `msm.MolSysBuilder` | **Stable** | Native editable molecular system; core Builder API |
| `msm.MolSysDict` | **Stable** | Declarative in-memory form |
| `msm.TopologyDict` | **Stable** | Declarative topology form |
| `msm.pyunitwizard` | **Stable** | Re-exported unit bridge; canonical unit handling entry point |
| `msm.warmup_numba` | **Stable** | Explicit JIT precompilation; stable utility |
| `msm.systems` | Experimental | Example system registry; contents may be extended or reorganized |
| Exception classes (`ArgumentError`, `LibraryNotFoundError`, etc.) | **Stable** | Part of the public error-handling contract |

---

### 2.2 `msm.basic` — core operations

These are the primary daily-use API functions. All are re-exported at the root
level via `from .basic import *`.

| Function | Stability | Notes |
| :--- | :---: | :--- |
| `get` | **Stable** | Central getter; Tier 1 contractual |
| `set` | **Stable** | Central setter; Tier 1 contractual |
| `convert` | **Stable** | Central conversion; Tier 1 contractual |
| `select` | **Stable** | Selection engine; Tier 1 contractual |
| `extract` | **Stable** | Subsystem extraction; Tier 1 contractual |
| `copy` | **Stable** | Deep copy of molecular system |
| `merge` | **Stable** | Merge multiple molecular systems |
| `add` | **Stable** | Add atoms/groups to a system |
| `remove` | **Stable** | Remove atoms/groups from a system |
| `append_structures` | **Stable** | Append structure frames |
| `concatenate_structures` | **Stable** | Concatenate structure arrays |
| `info` | **Stable** | Human-readable system summary |
| `view` | **Stable** | Viewer entry point (viewer availability is soft-dep) |
| `Iterator` | **Stable** | Chunk iterator for trajectory workflows |
| `get_form` | **Stable** | Identify the form of a molecular system object |
| `is_a_molecular_system` | **Stable** | Type check |
| `are_multiple_molecular_systems` | **Stable** | Type check for lists |
| `has_attribute` | **Stable** | Attribute presence check |
| `get_attributes` | **Stable** | List available attributes |
| `where_is_attribute` | **Stable** | Locate attribute in form hierarchy |
| `get_label` | **Stable** | Return a canonical label string |
| `is_composed_of` | **Stable** | Composition query |
| `contains` | **Stable** | Containment query |
| `compare` | **Stable** | Structural comparison between systems |

---

### 2.3 `msm.structure` — structural analysis and manipulation

| Function | Stability | Notes |
| :--- | :---: | :--- |
| `get_center` | **Stable** | Heavy-mode supported (`file:h5msm`, `molsysmt.H5MSMFileHandler`) |
| `get_distances` | **Stable** | Heavy-mode supported; `use_gpu` parameter (GPU-optional) |
| `get_rmsd` | **Stable** | Heavy-mode supported; `use_gpu` parameter (GPU-optional) |
| `get_least_rmsd` | **Stable** | |
| `least_rmsd_fit` | **Stable** | |
| `least_rmsd_align` | **Stable** | |
| `get_radius_of_gyration` | **Stable** | `use_gpu` parameter (GPU-optional) |
| `get_minimum_distances` | **Stable** | |
| `get_maximum_distances` | **Stable** | |
| `get_contacts` | **Stable** | |
| `get_neighbors` | **Stable** | |
| `get_angles` | **Stable** | |
| `get_dihedral_angles` | **Stable** | `use_gpu` parameter (GPU-optional) |
| `set_dihedral_angles` | **Stable** | |
| `shift_dihedral_angles` | **Stable** | |
| `get_principal_axes` | **Stable** | `use_gpu` parameter (GPU-optional) |
| `principal_component_analysis` | **Stable** | `use_gpu` parameter (GPU-optional) |
| `align_principal_axes` | **Stable** | |
| `translate` | **Stable** | |
| `center` | **Stable** | |
| `rotate` | **Stable** | |
| `flip` | **Stable** | |
| `move_away` | **Stable** | |
| `show_contacts` | Experimental | Viewer-dependent; output format may evolve |

---

### 2.4 `msm.build` — structure preparation and construction

The build namespace depends heavily on external tools (PDBFixer, tleap, OpenMM).
The MolSysMT-native path (`editable`) is Stable; external-tool-dependent
functions are Experimental for `1.0.0`.

| Function | Stability | Notes |
| :--- | :---: | :--- |
| `editable` | **Stable** | Entry point to the `MolSysBuilder` editing workflow |
| `build_peptide` (engine=`"MolSysMT"`) | **Stable** | Native peptide builder |
| `build_peptide` (other engines) | Experimental | Depends on external tools |
| `get_missing_heavy_atoms` | Experimental | |
| `get_missing_terminal_cappings` | Experimental | |
| `get_missing_residues` | Experimental | |
| `get_missing_bonds` | Experimental | |
| `get_non_standard_residues` | Experimental | |
| `get_disulfide_bonds` | Experimental | |
| `has_hydrogens` | Experimental | |
| `add_missing_hydrogens` | Experimental | Depends on PDBFixer or equivalent |
| `add_missing_heavy_atoms` | Experimental | Depends on external tools |
| `add_missing_terminal_cappings` | Experimental | |
| `add_missing_bonds` | Experimental | |
| `solve_atoms_with_alternate_location` | Experimental | |
| `make_bioassembly` | Experimental | |
| `is_solvated` | Experimental | |
| `solvate` | Experimental | Depends on external solvation tools |
| `make_water_box` | Experimental | |
| `mutate` | Experimental | |
| `remove_overlapping_molecules` | Experimental | |

---

### 2.5 `msm.pbc` — periodic boundary conditions

| Function | Stability | Notes |
| :--- | :---: | :--- |
| `wrap_to_pbc` | **Stable** | |
| `wrap_to_mic` | **Stable** | |
| `unwrap` | **Stable** | |
| `has_pbc` | **Stable** | |
| `get_box_from_lengths_and_angles` | **Stable** | |
| `get_lengths_from_box` | **Stable** | |
| `get_angles_from_box` | **Stable** | |
| `get_lengths_and_angles_from_box` | **Stable** | |
| `get_box_with_shape` | **Stable** | |
| `get_shape_from_box` | **Stable** | |
| `get_shape_from_angles` | **Stable** | |
| `get_volume_from_box` | **Stable** | |
| `get_volume_from_lengths_and_angles` | **Stable** | |

---

### 2.6 `msm.physchem` — physicochemical properties

| Function | Stability | Notes |
| :--- | :---: | :--- |
| `get_mass` | **Stable** | Lookup-table based; well-defined |
| `get_charge` | **Stable** | Lookup-table based |
| `get_atomic_radius` | **Stable** | Lookup-table based |
| `get_polarity` | Experimental | Lookup-table; coverage may extend in `1.x` |
| `get_hydrophobicity` | Experimental | Lookup-table; scale choice may be revised |
| `get_transmembrane_tendency` | Experimental | Lookup-table |
| `get_area_buried` | Experimental | |
| `get_buried_fraction` | Experimental | |
| `get_sasa` | Experimental | Depends on external SASA solver |
| `get_surface_area` | Experimental | |
| `get_volume` | Experimental | |

---

### 2.7 `msm.topology` — topological analysis

| Function | Stability | Notes |
| :--- | :---: | :--- |
| `get_covalent_chains` | **Stable** | |
| `get_covalent_blocks` | **Stable** | |
| `get_dihedral_quartets` | **Stable** | |
| `get_bondgraph` | **Stable** | Returns a `networkx.Graph` |
| `get_sequence_alignment` | Experimental | Algorithm and output format may evolve |
| `get_sequence_identity` | Experimental | |

---

### 2.8 `msm.hbonds` — hydrogen bond detection

| Function | Stability | Notes |
| :--- | :---: | :--- |
| `get_acceptor_atoms` | Experimental | Rule-based; rules may be revised |
| `get_donor_atoms` | Experimental | Rule-based |
| `get_buch_hbonds` | Experimental | Algorithm-specific; signature may evolve |
| `get_luzard_chandler_hbonds` | Experimental | Algorithm-specific |

---

### 2.9 `msm.molecular_mechanics` — MM energy and forces

| Function | Stability | Notes |
| :--- | :---: | :--- |
| `potential_energy_minimization` | Outside contract | Depends on OpenMM; not contractual for `1.0.0` |
| `get_potential_energy` | Outside contract | |
| `get_non_bonded_potential_energy` | Outside contract | |
| `get_forces` | Outside contract | |
| `get_engine_forcefield` | Outside contract | |

---

### 2.10 `msm.molecular_dynamics`

Commented out in `__init__.py`. Explicitly outside the `1.0.0` support contract.
Stays in-tree for development continuity.

---

### 2.11 `msm.third_party`

Internal bridge to external tools (tleap, OpenMM utilities). Not part of the
public API contract. Subject to change without deprecation notice.

---

## 3. General rules

### 3.1 Required decorators
- All public functions **must** use `@arg_digest`.
- Internal helpers under `molsysmt/_private` **must not** use `@arg_digest`.

### 3.2 Return conventions
- Getter-style functions return **Python lists** (or lists of lists), not NumPy
  arrays, when returning collections of per-element data.
- Single numeric values should be scalars (`int`, `float`, `str`) as
  appropriate.

### 3.3 Naming and signatures
Follow existing naming conventions in adjacent modules. When adding public
functions, keep argument names aligned with standard terms:
`molecular_system`, `selection`, `structure_indices`, `syntax`,
`skip_digestion`, `to_form`.

### 3.4 Not-implemented policy
Public APIs must not silently expose partial behavior.

- If a parameter combination is not implemented, raise a typed exception
  (`NotImplementedMethodError`) with `caller` and an actionable message.
- Do not document unimplemented behavior as available.

### 3.5 Stability guarantees by tier

| Stability | Guarantee |
| :--- | :--- |
| **Stable** | No breaking changes across `1.x`; regressions are patch-priority; formal deprecation required before removal or signature change |
| **Experimental** | Available and tested, but signature or behavior may change in `1.x` minor releases without a full deprecation cycle |
| **Outside contract** | Present in codebase; no stability guarantee; may be promoted to Experimental or Stable in future releases |
