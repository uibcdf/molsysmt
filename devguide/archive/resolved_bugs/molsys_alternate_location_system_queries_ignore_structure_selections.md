---
summary: MolSys alternate-location system queries ignore structure selections
issue: uibcdf/molsysmt#331
status: resolved
opened: 2026-10-05
closed: 2026-10-05
severity: medium
verification: reproduced
area: [form, attribute]
guard: tests/form/molsysmt_MolSys/test_alternate_location_selection.py::test_system_alternate_location_preserves_structure_selection
normative:
blocked_by: []
supersedes: []
---

# MolSys alternate-location system queries ignore structure selections

**Reported:** 2026-10-05 during the public alternate-site index controls for
uibcdf/molsysmt#329.
**Status:** Resolved; the system getter forwards the requested structure indices.

## What

A system-level alternate-location query on native MolSys or a materialized
H5MSM 0.5 result returns every structure even when an explicit subset is given.
A three-structure source queried with `structure_indices=[2]` returns the first
structure's mapping first; `structure_indices=[]` incorrectly returns all three.
Atom queries with an explicit selection delegate to a different getter and did
preserve the requested structure axis.

```python
import numpy as np
import molsysmt as msm
from molsysmt.native import MolSys
molsys = MolSys(n_atoms=2)
molsys.structures.coordinates = msm.pyunitwizard.quantity(np.zeros((3, 2, 3)), 'nm')
molsys.structures.alternate_location = [
    {0: {'atom_id': ['100']}}, {}, {1: {'atom_id': ['200']}}]
result = msm.get(molsys, structure_indices=[2], alternate_location=True)
print([list(sites) for sites in result])  # expected [[1]], observed all three
```

## How

`form/molsysmt_MolSys/get_structural_attributes.py` delegates
`get_alternate_location_from_system()` with `structure_indices='all'` instead of
its validated argument. Forward the requested indices to the existing owning
Structures getter; no custom slicing or competing representation is needed.

## Why

A client joining alternate-site evidence to a selected coordinate structure can
receive evidence from a different structure. This affects system-level queries,
including modular H5MSM materialization, even after the key-type fix in #329.

## What is measured and what is assumed

**Reproduced:** the five-form #329 controls exposed incorrect single-structure
rereads and empty selections for native MolSys and H5MSM 0.5.
**Inspected:** literal 'all' delegation explains the discrepancy.
No exhaustive external-form audit or consumer biological failure is claimed.

## Scope and exclusions

Forward structure selections for system-level alternate-site queries. Preserve
source atom-index keys, repeated structure order, empty selections and stored
mappings. This does not change structural iteration, extraction or storage.

## Acceptance criteria

The public query guard
`tests/form/molsysmt_MolSys/test_alternate_location_selection.py::test_system_alternate_location_preserves_structure_selection`
checks nonconsecutive repeated indices, a structure without sites and an empty
selection against an independently specified source layout. The five-form #329
guard also covers this route through public H5MSM 0.5 queries.

## Provenance

Linux x86_64, 2026-10-05, Python 3.14.7, NumPy 2.4.6, released ArgDigest 0.13.0
source overlay. Editable-source controls based on `bac92dcdb`; no installed
release or complete platform matrix qualification is claimed.

## Resolution — 2026-10-05

The MolSys adapter passes its validated `structure_indices` to the existing
Structures getter. The named public guard asserts the exact independently
specified keys for `[2, 0, 2]`, the empty structure `[1]`, and `[]`; the source
mappings remain unchanged. The combined 147-control #329 checkpoint also covers
this path through public H5MSM 0.5 materialization and detached result edits.

No coordinate copying, schema change, custom slicing engine or atom-domain
renumbering is introduced. Documentation of `msm.get` explains outer-list
selection order and structures without sites. These are focused editable-source
controls, not full-suite or installed-release qualification.

Validation also passes Ruff, the current normative course gate
(`devtools/scripts/validate_course.py`: 156 notebooks), docstring validation,
public-signature stability and developer-guide integrity. Sphinx HTML compiles
with 30 warnings in this incremental build, including legacy course heading
levels, an unknown key-takeaway directive, existing admonition syntax and the
undefined user-foundations label. The changed notebooks retain that preexisting
markup. Incremental builds read different page sets; the prior checkpoint's
27 warnings do not establish a matched warning baseline. This does not claim
a warning-free build or zero new warning messages.
