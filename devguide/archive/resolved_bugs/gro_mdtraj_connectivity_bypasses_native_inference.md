---
summary: GRO conversion to MDTraj bypasses the supported native connectivity rules.
issue: uibcdf/molsysmt#30
status: resolved
opened: 2026-10-05
closed: 2026-10-05
severity: medium
verification: reproduced
area: [form, convert]
guard: tests/form/file_gro/test_mdtraj_connectivity.py
normative:
blocked_by: []
supersedes: []
---

# GRO conversion to MDTraj bypasses native connectivity

**Reported:** Historical #30, freshly reproduced during S1 on 2026-10-05.
**Status:** Resolved by reusing the existing native connectivity policy, with regression coverage.

## What

```python
import molsysmt as msm
topology = msm.convert(msm.systems['nglview']['md_1u19.gro'], to_form='mdtraj.Topology')
```

On source `0efb14144`, this produces 152 connected components for 5,547 atoms,
349 groups and 5,480 inferred bonds. There are 147 singleton atoms, including
unconnected ASH and GLH atoms. The bundled GRO is byte-identical to the installed
NGLView `datafiles.GRO` named in the original report.

## How

`form/file_gro/to_mdtraj_Trajectory.py` uses `mdtraj.load()` directly;
`to_mdtraj_Topology.py` extracts that topology. MDTraj's GRO reader invokes its
standard templates, which do not cover all group labels in this input. The
native GRO conversion already uses the public `build.get_missing_bonds()` tool
and yields a different graph. MolSysMT exposes inconsistent connectivity by
choosing the output form, despite having a reusable native route.

## Why

Molecule/component queries and analyses over the MDTraj output see fragments
created by backend template coverage. This is a supported-route inconsistency,
not authorization to expand chemistry or infer a universally correct graph.

## Correction and exclusions

Retain MDTraj's coordinate/time/box reader, but replace its topology using the
existing native GRO-to-Topology and native-to-MDTraj converters. Infer once on
the full first-structure atom axis before selection. Multiple structures and
their explicit selection remain available. No new inference method is added.

Native GRO grouping now recognizes a change of group name even when consecutive
group IDs repeat. The file-to-native topology wrapper closes its owned handler
on success or failure. Borrowed handlers keep their existing semantics.

GRO does not declare bonds or full chemical identity. The native template and
distance candidates remain heuristics; a graph with one component does not
scientifically validate every edge, bond order, ligand identity or preparation.
The new route may take more work than raw MDTraj loading. No performance claim
or chemically complete coverage is made.

## What was refuted

The failure is not caused by a missing MDTraj installation or lost coordinates:
direct upstream loading reproduces the same 152 components. Merely changing
molecule counts would conceal the incomplete graph. Replacing the coordinate
reader with the one-entry native handler would lose multi-structure GRO support.

## Acceptance criteria

- Independent ASH/GLH heavy-atom fixture retains its 16 expected edges.
- Native labels, atom order, selected induced bonds and nonconsecutive structures
  remain correct; MDTraj coordinates/time/cells keep its nm/ps conventions under
  a non-default PyUnitWizard session policy.
- Bundled original-input guard pins the current native candidate profile without
  presenting that count as scientific validation of all inferred edges.
- Existing GRO contracts and the affected native/MDTraj routes pass.

## Provenance

2026-10-05, Linux, Python 3.14.7, MDTraj 1.11.1, NGLView 4.0.1.
Original GRO SHA-256:
`8eec93cb0b45c43abc50ec40e49f983e2c2484671077777db19bf7340c068c76`.
Scientific commands use the qualified suite 3.14 environment with the released
PyUnitWizard 0.28.1 and ArgDigest 0.13.0 development boundary recorded in
[the execution ledger](../release_1_0_status.md). Initial naming/alternate
selection: 35 passed; first new GRO run: 7 passed/1 failed due to an existing
test assuming `import openmm` imports `openmm.app`. That oracle test now imports
its actual optional submodule, retaining all numerical comparisons.

## Resolution and qualification

The corrected original-input route yields 5,632 candidate bonds and one
component, retaining all 5,547 atoms and 349 source groups. The native candidate
profile remains experimental; this is **Contract-tested** route consistency,
with an independent 16-edge fixture for the supported acidic groups, not
scientific validation of every original-input edge.

The affected Python 3.14 selection passes **819 tests in 358.97 s**, including
the GRO contracts, alternate-site queries, local naming, MDTraj topology getters,
trajectory conversion and three converter doctests. Four warnings retain
external PDB dummy-box notices and the legacy H5MSM deprecation. Focused earlier
runs overlap this selection and are not additional independent test counts.
Ruff, lazy dependencies, public dependency routes, the API registry, devguide
and current 156-module course validator pass. The documentation builds in the
existing Python 3.13 environment with 40 warnings; the 3.14 documentation
environment lacks extensions and remains a #237 qualification obligation.
No full release matrix or installed candidate is certified here.
