---
summary: ParmEd selection desynchronizes coordinates and periodic cells.
issue: uibcdf/molsysmt#464
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: high
verification: reproduced
area: [form, convert]
guard: tests/form/parmed_Structure/test_bridge_contract.py
normative:
blocked_by: []
supersedes: []
---

# ParmEd selection desynchronizes coordinates and periodic cells

**Reported:** 2026-10-26, while testing independent geometric witnesses for
uibcdf/molsysmt#181 and the dispatch repair under uibcdf/molsysmt#463.
**Status:** resolved. Selected topology, coordinates and cells remain aligned.

## What

A partial, nonmonotonic atom list such as `[3, 1, 2]` reaches the ParmEd-to-MDTraj
converter with topology in source order but coordinates in supplied-list order.
ParmEd self-extraction also leaves all original periodic cells beside a reordered
structure subset such as `[2, 0]`.

```bash
python -m pytest tests/form/parmed_Structure/test_bridge_contract.py -k selected_geometry --receptor=llm -n 12
```

## How

`parmed_Structure.to_mdtraj_Trajectory` delegates topology selection through OpenMM,
whose extractor retains source atom order, then independently slices raw coordinates
using the original selection list. Its box path reads `item.box`, which exposes only
the first cell, instead of the structure-resolved `get_box('all')` data.

`parmed_Structure.extract` slices coordinates but does not subset the separate box
store. The existing structural getter must also account for a single cell shared
by multiple coordinate structures. The repair belongs in these owning tools:
source-order normalization in the converter, consistent box extraction, and
broadcasting shared cells without materializing a trajectory-sized intermediate.

## Why

Expected output form and counts can coexist with scientifically incorrect geometry.
Downstream distance and periodic calculations would use coordinates assigned to
wrong atom labels or cells assigned to wrong structures. This is separate from
runtime dispatch defects: the affected converters can finish successfully.

## What is measured and what is assumed

The first per-structure-cell witness confirms four direct/public/unit-policy
failures for ParmEd self-extraction and four for ParmEd-to-MDTraj atom alignment.
A broader control adds shared-cell and nonperiodic inputs, native conversion and
mechanical partial-charge retention. The expanded initial run failed 28 cases and passed 36 in 6.86 seconds; its selection also includes the repaired MDTraj-to-ParmEd controls.
A NumPy assertion initially failed on the nullable native charge dtype; that oracle
now explicitly converts charge values to float, consistent with existing tests.
It was not evidence of a charge-delivery defect.

## What was refuted

The target representation is not the limitation: MDTraj and ParmEd both support
per-structure cells. Reordering structures is explicit input and must also reorder
cells. A topology-only native conversion has no structural axis and is outside
this geometry check.

## Scope and exclusions

Preserve selection correspondence for ParmEd self-extraction and MDTraj output,
including shared/no-cell data. Exercise native structures and MolSys as separate
controls. Force-field parameterization, inferred chemistry and arbitrary provider
field preservation remain outside this bounded contract. This does not change
the native extraction rule or introduce a new atom-permutation API.

## Acceptance criteria

- Labels, bonds, geometry and cells agree after nonconsecutive selections.
- Shared cells are valid for every represented structure; absent cells stay absent.
- Sources are unchanged, and native mechanical charges remain aligned.
- Both direct/public routes and nm/angstrom standard-unit policies pass.

## Provenance

Linux development environment, Python 3.14. The bounded #181 execution receipt
will retain exact provider versions, commands and tested source hashes.


## Resolution and validation — 2026-10-26

The source adapters retain normal argument digestion and lazy provider guards.
Atom selections use source order when the topology exporter does, and structure
selections also reorder the cells. The adapters reuse structural getters, general
PBC conversion and the existing OpenMM box setter. Shared cells are broadcast as
a view before selecting output cells, without a trajectory-sized repeated table.

The final regression passes 2,514 tests with no failures or skips in 142.33 seconds
using `--receptor=llm -n 12`; the mirrored bridge module contains 76 cases. Four
converter doctests pass, and the updated Cookbook and Common Core module execute
successfully. The [bounded receipt](../../../devtools/data/conversion_execution_parmed_20261026.json)
records exact commands, dependency versions, source hashes and the separate
execution/fidelity/release scope. See the [operational guide](../../conversion_execution.md)
for current profile commands and remaining debt.

Ruff lint/format and the fourteen fast gates pass. The full-site HTML command
exits zero with pre-existing notebook-schema diagnostics recorded under
uibcdf/molsysmt#144; the changed examples execute, but no clean-site claim is made.
