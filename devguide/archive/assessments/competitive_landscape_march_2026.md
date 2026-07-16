# Competitive Landscape and Vision

> **Document role:** Strategy. Capability and performance statements in this
> document are development targets or dated observations unless backed by a
> current code path and executable test. Normative contracts take precedence.

This document captures the strategic analysis of MolSysMT's position relative to
established tools like mdtraj and MDAnalysis, the strengths and weaknesses identified
during the March 2026 audit, and the specific development targets needed to match or
exceed them.

This is a living document.  It should be updated as capabilities are added and the
competitive picture changes.

---

## The fundamental bet — we don't compete, we supersede

MolSysMT is not trying to be a better mdtraj or a better MDAnalysis on their own terms.
The bet is different and more ambitious:

> **The right abstraction layer for working with molecular systems is the form-agnostic
> unified API.  Everything else — analysis, visualization, simulation — should plug into
> that layer as backends or modules.**

If that bet is right, the comparison with mdtraj and MDAnalysis is a category error.
They are not competitors — they are backends.  MolSysMT can call mdtraj's `shrake_rupley`
for SASA, BioPython's DSSP for secondary structure, and MDAnalysis for any algorithm
they have built over a decade — all from any input form, with consistent error handling,
consistent units, and a consistent selection language.  The user never needs to know which
engine did the work.

This is not a roadmap aspiration.  The architecture already works this way for sequence
analysis (BioPython), SASA (mdtraj), and visualization (nglview).  The pattern is proven.

The consequence of this architecture is that the comparison table in this document is
partly misleading: when we say MolSysMT has a capability, it may be implemented natively
or by delegation — but from the user's perspective it does not matter.  And when we say
a capability is "missing", what we usually mean is that the delegation wrapper has not
been written yet, not that there is a fundamental gap.

**The right framing is not "can MolSysMT do what mdtraj and MDAnalysis can do?"  The
right framing is "does MolSysMT provide the layer above mdtraj and MDAnalysis that makes
them all accessible uniformly?"  The answer to the second question is already yes.**

---

## Where MolSysMT already leads

### 1. Form abstraction — genuinely unique

Neither mdtraj nor MDAnalysis have anything equivalent to the form system.

- In **mdtraj**, you always work with `Trajectory` or `Topology` objects.
- In **MDAnalysis**, you always work with `Universe` or `AtomGroup`.
- In **MolSysMT**, you work with whatever you already have.  The API is identical
  regardless of whether the input is a PDB file, an openmm.Topology, an MDAnalysis.Universe,
  a SMILES string, or a MolSys object.

This is not a cosmetic convenience.  It removes an entire class of cognitive overhead
from scientific workflows.

### 2. The MolSysSuite ecosystem — native support layers

This is an advantage that is invisible until you look inside:

| Library | Role | Benefit over ad hoc solutions |
|---|---|---|
| **argdigest** | Argument validation and normalization | Consistent, informative errors across the entire API; no ad hoc `if` chains scattered through functions |
| **depdigest** | Optional dependency management | True lazy loading; clean `LibraryNotFoundError` with install instructions; no `try/except ImportError` debris |
| **pyunitwizard** | Unit bridge | Works simultaneously with pint, openmm, mdtraj units; units errors are caught at the API boundary, not buried in kernels |
| **smonitor** | Structured diagnostics and support tiers | Users know exactly what is contractually guaranteed vs experimental; no silent failures |
| **molsysviewer** | Native visualization | Visualization is part of the ecosystem, not an afterthought plugin |

MDAnalysis handles optional dependencies with scattered `try/except` blocks.  mdtraj
has no unit system at all.  Neither has anything like smonitor's support-tier contract.

The consequence for the user experience: when something goes wrong in MolSysMT, the
error is informative and consistent.  When something goes wrong in MDAnalysis or mdtraj,
the error is whatever Python happens to throw.

### 3. Modern architecture

- **Lazy loading 2.0** — `import molsysmt` is near-instantaneous regardless of which
  optional libraries are installed.  MDAnalysis is notoriously slow to import.
- **Topological Normalization Engine** — Automatically "pacifies" inconsistent atom/residue
  naming across force fields (AMBER, CHARMM, GROMOS). A fundamental differentiator for
  interoperability.
- **Precision Policy** — Explicit handling of `float32` vs `float64` noise at the API
  boundary, ensuring numerical robustness for high-precision analysis.
- **Declarative serialization** — `MolSysDict`, `TopologyDict`, `StructuresDict`,
  `file:molsys_yaml`, `file:topology_yaml` have no equivalent in either tool.
- **MolSysBuilder** — declarative, step-by-step system construction with a clean API.
- **Support tier protocol** — explicit, machine-checkable runtime contract on what is
  Tier 1 (stable), Tier 2 (best-effort), or Tier 3 (experimental).
- **Dirty-bit optimization** in `Topology` — avoids redundant hierarchy rebuilds.
- **String-based lazy converter registry** — `_convert_to` values are strings resolved
  by `importlib` only when the conversion path is actually traversed.

### 4. Unified analysis API

A user running `msm.get(item, element='atom', x=True)` gets coordinates regardless of
whether `item` is a PDB file, an OpenMM Context, or an MDAnalysis Universe.  That level
of uniformity does not exist elsewhere.

### 5. System building — a genuine differentiator

mdtraj has no system-building capabilities at all.  MDAnalysis has limited and fragmented
tools.  MolSysMT ships a full `molsysmt.build` module:

| Function | Capability |
|---|---|
| `build_peptide()` | Build a peptide from a sequence, engine-agnostic (MolSysMT, LEaP) |
| `solvate()` | Add explicit solvent to a molecular system |
| `mutate()` | Mutate residues in-place |
| `add_missing_hydrogens()` | Add H atoms to any supported form |
| `add_missing_heavy_atoms()` | Reconstruct missing heavy atoms |
| `add_missing_terminal_cappings()` | Add ACE/NME cappings |
| `make_bioassembly()` | Generate biological assembly from asymmetric unit |
| `make_water_box()` | Create a pure solvent box |
| `get_disulfide_bonds()` | Detect disulfide pairs |
| `solve_atoms_with_alternate_location()` | Resolve alternate location records |
| `remove_overlapping_molecules()` | Clean overlapping solvent molecules |
| `editable()` | Ergonomic `MolSysBuilder` entrypoint for editing existing systems |

This is a capability class that has no direct parallel in either competitor.

### 6. Physical chemistry module — unique breadth

Neither mdtraj nor MDAnalysis expose per-atom physicochemical properties as a
first-class module.  MolSysMT ships `molsysmt.physchem`:

| Function | Capability |
|---|---|
| `get_mass()` | Atomic and group masses |
| `get_charge()` | Formal charges |
| `get_sasa()` | Solvent-accessible surface area (delegates to mdtraj's `shrake_rupley`) |
| `get_atomic_radius()` | van der Waals radii |
| `get_hydrophobicity()` | Residue hydrophobicity scales |
| `get_polarity()` | Residue polarity |
| `get_volume()` | Atomic/residue volumes |
| `get_area_buried()` | Buried surface area |
| `get_buried_fraction()` | Fraction of surface area buried |
| `get_surface_area()` | Exposed surface area |
| `get_transmembrane_tendency()` | Transmembrane insertion tendency |

The breadth of the `physchem` module has no equivalent in either tool.

### 7. Third-party simulation integration (`third_party/`)

MolSysMT provides explicit integration modules for:

- **OpenMM** — system preparation, simulation, and result retrieval through the MolSysMT form adapter for `openmm.Context`, `openmm.Simulation`, and `openmm.Modeller`.
- **nglview** — native visualization via `molsysmt.third_party.nglview` and the `nglview.NGLWidget` form adapter; `msm.view()` delegates here.
- **tleap** — AMBER `tleap` integration for system preparation and force-field parametrization.

This makes MolSysMT the connective tissue between simulation engines, not a replacement for them.

### 8. PBC utilities

`molsysmt.pbc` provides: `wrap_to_mic()`, `wrap_to_pbc()`, `unwrap()`, and box geometry
helpers (`get_box_from_lengths_and_angles()`, `get_lengths_from_box()`,
`get_volume_from_box()`, etc.).  These are integrated into the form-agnostic API so PBC
corrections can be applied to any supported trajectory form.

---

## Where MolSysMT currently lags

### Capability comparison

| Capability | mdtraj | MDAnalysis | MolSysMT | Notes |
|---|---|---|---|---|
| RMSD | ✅ | ✅ | ✅ | Heavy-mode supported |
| RMSF | ✅ | ✅ | ✅ | `molsysmt.structure.get_rmsf()` — Numba JIT kernel |
| Distances / contacts | ✅ | ✅ | ✅ | |
| Angles / dihedrals | ✅ | ✅ | ✅ | |
| Least-RMSD alignment | ✅ | ✅ | ✅ | |
| PCA | ✅ | ✅ | ✅ | |
| H-bonds | ✅ | ✅ | ✅ | dedicated `hbonds` module |
| PBC wrapping / unwrapping | ✅ | ✅ | ✅ | `molsysmt.pbc` module |
| Sequence identity | — | ✅ | ✅ | |
| Radius of gyration | ✅ | ✅ | ✅ | `molsysmt.structure.get_radius_of_gyration()` — Numba JIT kernel |
| SASA | ✅ | ✅ | ✅ | `molsysmt.physchem.get_sasa()` via mdtraj engine |
| Secondary structure | ✅ | ✅ | ✅ | `molsysmt.structure.get_secondary_structure()` — DSSP via mdtraj |
| Sequence alignment | — | ✅ | ⚠️ | BioPython engine only; others are stubs |
| Clustering | — | ✅ | ❌ | |
| Heavy trajectories | ✅ | ✅ | ✅ | **Out-of-Core** implemented: ChunkedExecutor, Reducer, Iterator |
| System building | ❌ | ⚠️ | ✅ | `molsysmt.build`: peptide, solvate, mutate, bioassembly, ... |
| Physicochemical properties | ❌ | ❌ | ✅ | `molsysmt.physchem`: mass, charge, hydrophobicity, ... |
| Simulation integration | ⚠️ | ⚠️ | ✅ | `third_party/`: OpenMM, tleap, nglview |
| Form-agnostic API | ❌ | ❌ | ✅ | |
| Declarative serialization | ❌ | ❌ | ✅ | |
| Support tier contract | ❌ | ❌ | ✅ | |
| Native unit system | ❌ | ❌ | ✅ | via pyunitwizard |
| Topological Normalization | ❌ | ❌ | ✅ | Automatic nomenclature "pacification" |
| Precision Policy | ❌ | ❌ | ✅ | Explicit float32/64 noise handling |

### Performance

mdtraj uses Cython and C extensions with years of optimization.  MolSysMT uses Numba
JIT kernels which are competitive for single-pass operations but have a warmup cost.
The heavy-trajectory pipeline (chunked reading, reducer protocol) is now implemented for
the Tier 1 slice — see `SCALABILITY.md`. The remaining
performance gap vs mdtraj is in the eager path for operations that do not yet have JIT
kernels, not in the chunked-execution architecture itself.

### Ecosystem and community

This cannot be fixed with code.  It requires time, publications, documentation quality,
and adoption.  The paper and a thorough user-facing tutorial site are the primary levers.

---

## Module-by-module status

### `molsysmt/structure/`

25 functions.  Core functionality solid.  Key gaps below.

| Function | Status | Priority |
|---|---|---|
| `get_distances()` | ✅ fully implemented (most comprehensive) | — |
| `get_minimum_distances()` | ✅ | — |
| `get_maximum_distances()` | ✅ | — |
| `get_contacts()` | ✅ (docstring placeholder) | low |
| `get_neighbors()` | ✅ (docstring placeholder) | low |
| `get_angles()` | ✅ | — |
| `get_dihedral_angles()` | ✅ | — |
| `set_dihedral_angles()` | ✅ | — |
| `shift_dihedral_angles()` | ✅ | — |
| `get_center()` | ✅ (docstring placeholder) | low |
| `get_least_rmsd()` | ✅ | — |
| `get_rmsd()` | ✅ (docstring placeholder) | low |
| `get_principal_axes()` | ✅ | — |
| `principal_component_analysis()` | ✅ | — |
| `least_rmsd_fit()` | ✅ | — |
| `least_rmsd_align()` | ✅ | — |
| `align_principal_axes()` | ✅ | — |
| `translate()` | ✅ | — |
| `rotate()` | ✅ | — |
| `flip()` | ✅ (docstring placeholder) | low |
| `center()` | ✅ (docstring placeholder) | low |
| `move_away()` | ✅ | — |
| `show_contacts()` | ✅ (docstring placeholder) | low |
| **`get_radius_of_gyration()`** | ✅ implemented — Numba JIT kernel, uniform and mass-weighted (March 2026) | — |
| **`get_rmsf()`** | ✅ implemented — Numba JIT kernel (March 2026) | — |
| **`get_sasa()`** | ❌ not here — see `molsysmt.physchem.get_sasa()` | — |
| **secondary structure** | ✅ implemented — `get_secondary_structure()`, DSSP via MDTraj (March 2026) | — |

**Docstring placeholders ("To be written soon..."):** `get_contacts`, `get_neighbors`,
`get_rmsd`, `center`, `flip`, `show_contacts` — and several others.  These need to be
written before 1.0.0 documentation is considered complete.

### `molsysmt/topology/`

6 functions.  Small module, mostly working.

| Function | Status | Priority |
|---|---|---|
| `get_bondgraph()` | ✅ | — |
| `get_covalent_blocks()` | ✅ | — |
| `get_covalent_chains()` | ✅ | — |
| `get_dihedral_quartets()` | ✅ | — |
| `get_sequence_identity()` | ✅ | — |
| **`get_sequence_alignment()`** | ⚠️ BioPython engine only; other engines are stubs | medium |
| **disulfide bond detection** | ❌ missing here — `msm.build.get_disulfide_bonds()` exists | low |
| **contact graph** | ❌ missing | low |

### `molsysmt/physchem/`

11 functions.  Unique breadth — no equivalent in mdtraj or MDAnalysis.

| Function | Status | Priority |
|---|---|---|
| `get_mass()` | ✅ | — |
| `get_charge()` | ✅ | — |
| `get_atomic_radius()` | ✅ | — |
| `get_hydrophobicity()` | ✅ | — |
| `get_polarity()` | ✅ | — |
| `get_volume()` | ✅ | — |
| `get_area_buried()` | ✅ | — |
| `get_buried_fraction()` | ✅ | — |
| `get_surface_area()` | ✅ | — |
| `get_transmembrane_tendency()` | ✅ | — |
| **`get_sasa()`** | ⚠️ implemented (mdtraj engine via `shrake_rupley`); docstring placeholder | medium |

Most functions are implemented.  The main outstanding work is writing the missing docstrings.

### `molsysmt/build/`

20 functions.  No equivalent in mdtraj; MDAnalysis has limited fragments.

| Function | Status | Priority |
|---|---|---|
| `build_peptide()` | ✅ MolSysMT + LEaP engines; parity validation system in place | — |
| `solvate()` | ✅ | — |
| `mutate()` | ✅ | — |
| `make_bioassembly()` | ✅ | — |
| `make_water_box()` | ✅ | — |
| `add_missing_hydrogens()` | ✅ | — |
| `add_missing_heavy_atoms()` | ✅ | — |
| `add_missing_terminal_cappings()` | ✅ | — |
| `add_missing_bonds()` | ✅ | — |
| `get_disulfide_bonds()` | ✅ | — |
| `get_missing_bonds()` | ✅ | — |
| `get_missing_heavy_atoms()` | ✅ | — |
| `get_missing_residues()` | ✅ | — |
| `get_missing_terminal_cappings()` | ✅ | — |
| `get_non_standard_residues()` | ✅ | — |
| `has_hydrogens()` | ✅ | — |
| `is_solvated()` | ✅ | — |
| `solve_atoms_with_alternate_location()` | ✅ | — |
| `remove_overlapping_molecules()` | ✅ | — |
| `editable()` | ✅ ergonomic entrypoint for `MolSysBuilder` | — |

---

## Development targets

### Immediate (quick wins, days not weeks)

1. ~~**Re-enable `get_radius_of_gyration()`**~~ ✅ Done — fully rewritten with Numba JIT
   kernel (March 2026).
2. **Write missing docstrings** — several functions in `structure/` still have placeholder
   docstrings.  Mechanical but critical for documentation quality and the API reference.

### Short term (weeks)

3. ~~**Implement `get_rmsf()`**~~ ✅ Done — Numba JIT kernel (March 2026).
4. **Complete `get_sequence_alignment()`** — add at least one more engine beyond BioPython
   (e.g., a pure-Python pairwise aligner or delegation to BioPython's PairwiseAligner).
5. **Tests for `structure/`, `topology/`, `physchem/`, and `build/`** — the modules have
   good implementations but low test coverage; this is both a coverage and quality issue.

### Medium term (months)

6. ~~**Implement secondary structure assignment**~~ ✅ Done — `get_secondary_structure()`,
   delegates to DSSP via MDTraj (March 2026).
7. ~~**Heavy trajectory pipeline**~~ ✅ Done — Tier 1 slice (ChunkedExecutor, Reducer,
   PersistentResultHandle, SMonitor telemetry, heavy support in `get_center`,
   `get_rmsd`, `get_distances`) fully implemented and tested (March 2026).
   See `SCALABILITY.md` section 14.1.

### Long term (release cycle)

8. **Clustering** — trajectory-level clustering is a significant analysis capability
   gap vs MDAnalysis.
9. **User-facing documentation site** — comprehensive tutorials, cookbook, and quickstart
    guide.  The notebooks exist but are not organized as a coherent user journey.
10. **Paper** — the primary lever for community adoption.

---

## The delegation strategy

For capabilities that are better implemented elsewhere (SASA, DSSP, some clustering
algorithms), the correct MolSysMT approach is delegation, not reimplementation:

1. Accept any supported form as input (the MolSysMT API layer handles this).
2. Convert internally to the form required by the backend library.
3. Call the backend.
4. Return the result in the MolSysMT standard format.

This is exactly what `get_sequence_identity()` and `get_sequence_alignment()` already do
with BioPython.  The pattern should be generalized: the user never needs to know which
backend is doing the work.

This is the architecture that makes the aspiration realistic: MolSysMT does not need to
reimplement everything mdtraj and MDAnalysis have built over a decade.  It needs to be
able to **call** what they have built, uniformly, from any input form.

---

## Summary

MolSysMT's architecture is already more modern and more coherent than its established
competitors.  The form abstraction, the MolSysSuite ecosystem, the support tier
contract, and the declarative serialization layer are genuine advantages that neither
mdtraj nor MDAnalysis have.

Beyond architecture, MolSysMT already **leads** in several capability areas that its
competitors do not match:

- `molsysmt.build` — full system construction pipeline (peptide building, solvation,
  mutation, bioassembly, hydrogen/capping handling); mdtraj has nothing comparable;
  MDAnalysis has scattered fragments.
- `molsysmt.physchem` — per-atom physicochemical properties (mass, charge, SASA,
  hydrophobicity, polarity, transmembrane tendency); no equivalent in either tool.
- `third_party/` — explicit integration with OpenMM, tleap, and nglview through the
  form-agnostic adapter layer.

The remaining capability gap is specific and addressable:

- A small number of disabled or missing analysis functions (radius of gyration, RMSF,
  secondary structure) — none require architectural work.
- `get_sasa()` in `physchem/` is implemented but needs its docstring; the `structure/`
  module also has placeholder docstrings that must be filled before 1.0.0.
- ~~Heavy trajectory support~~ — Tier 1 slice fully implemented (March 2026).
- Documentation and community — time and consistency.

The foundation is right.  The path from here to "better than mdtraj and MDAnalysis" is
a known path, not an open research problem — and in several important dimensions,
MolSysMT is already there.
