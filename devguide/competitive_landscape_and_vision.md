# Competitive Landscape and Vision

This document captures the strategic analysis of MolSysMT's position relative to
established tools like mdtraj and MDAnalysis, the strengths and weaknesses identified
during the March 2026 audit, and the specific development targets needed to match or
exceed them.

This is a living document.  It should be updated as capabilities are added and the
competitive picture changes.

---

## The fundamental bet

MolSysMT is not trying to be a better mdtraj or a better MDAnalysis on their own terms.
The bet is different:

> **The right abstraction layer for working with molecular systems is the form-agnostic
> unified API.  Everything else — analysis, visualization, simulation — should plug into
> that layer as backends or modules.**

If that bet is right, mdtraj and MDAnalysis do not compete with MolSysMT.  They become
optional backends that MolSysMT can delegate to when their specific algorithms are the
best available option (SASA via mdtraj, DSSP via BioPython, etc.).

This is the architecture we are building toward.

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

---

## Where MolSysMT currently lags

### Capability comparison

| Capability | mdtraj | MDAnalysis | MolSysMT | Notes |
|---|---|---|---|---|
| RMSD | ✅ | ✅ | ✅ | |
| Distances / contacts | ✅ | ✅ | ✅ | |
| Angles / dihedrals | ✅ | ✅ | ✅ | |
| Least-RMSD alignment | ✅ | ✅ | ✅ | |
| PCA | ✅ | ✅ | ✅ | |
| H-bonds | ✅ | ✅ | ✅ | dedicated `hbonds` module |
| PBC | ✅ | ✅ | ✅ | minimum image convention |
| Sequence identity | — | ✅ | ✅ | |
| Radius of gyration | ✅ | ✅ | ❌ | code exists, disabled — quick fix |
| RMSF | ✅ | ✅ | ❌ | straightforward given RMSD |
| SASA | ✅ | ✅ | ❌ | delegate to FreeSASA or mdtraj |
| Secondary structure | ✅ | ✅ | ❌ | delegate to DSSP via mdtraj or BioPython |
| Sequence alignment | — | ✅ | ⚠️ | BioPython engine only; others are stubs |
| RMSF | ✅ | ✅ | ❌ | |
| Clustering | — | ✅ | ❌ | |
| Heavy trajectories | ✅ | ✅ | ❌ | roadmap exists, not yet implemented |
| Form-agnostic API | ❌ | ❌ | ✅ | |
| Declarative serialization | ❌ | ❌ | ✅ | |
| Support tier contract | ❌ | ❌ | ✅ | |
| Native unit system | ❌ | ❌ | ✅ | via pyunitwizard |

### Performance

mdtraj uses Cython and C extensions with years of optimization.  MolSysMT uses Numba
JIT kernels which are competitive for single-pass operations but have a warmup cost.
The heavy-trajectory pipeline (chunked reading, reducer protocol) is the most significant
remaining performance gap.

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
| **`get_radius_of_gyration()`** | ❌ disabled — code exists, raises `NotImplementedMethodError` | **high** |
| **`get_rmsf()`** | ❌ missing | high |
| **`get_sasa()`** | ❌ missing | medium |
| **secondary structure** | ❌ missing | medium |

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
| **disulfide bond detection** | ❌ missing | low |
| **contact graph** | ❌ missing | low |

---

## Development targets

### Immediate (quick wins, days not weeks)

1. **Re-enable `get_radius_of_gyration()`** — the commented implementation exists; verify
   and restore it.  This is a high-visibility gap for any user coming from mdtraj.
2. **Write missing docstrings** — at least 17 functions have placeholder docstrings.
   This is mechanical but critical for documentation quality and the API reference.

### Short term (weeks)

3. **Implement `get_rmsf()`** — straightforward given the RMSD and distance infrastructure.
4. **Complete `get_sequence_alignment()`** — add at least one more engine beyond BioPython
   (e.g., a pure-Python pairwise aligner or delegation to BioPython's PairwiseAligner).
5. **Tests for `structure/` and `topology/`** — the modules have good implementations
   but low test coverage; this is both a coverage and quality issue.

### Medium term (months)

6. **Implement `get_sasa()`** — delegate to FreeSASA (via its Python bindings) or to
   mdtraj as a backend.  The MolSysMT API should be engine-agnostic.
7. **Implement secondary structure assignment** — delegate to DSSP via mdtraj or
   BioPython.  Same engine-agnostic pattern.
8. **Heavy trajectory pipeline** — the roadmap exists in
   `devguide/scalability_and_heavy_trajectories_v2.md`.  This is the largest remaining
   technical item and the most important for performance parity.

### Long term (release cycle)

9. **Clustering** — trajectory-level clustering is a significant analysis capability
   gap vs MDAnalysis.
10. **User-facing documentation site** — comprehensive tutorials, cookbook, and quickstart
    guide.  The notebooks exist but are not organized as a coherent user journey.
11. **Paper** — the primary lever for community adoption.

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

The remaining gap is specific and addressable:

- A handful of missing or disabled analysis functions (radius of gyration, RMSF, SASA,
  secondary structure) — none of these require architectural work.
- Heavy trajectory support — significant work, but the design is already drafted.
- Documentation and community — time and consistency.

The foundation is right.  The path from here to "better than mdtraj and MDAnalysis" is
a known path, not an open research problem.
