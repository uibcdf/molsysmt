---
summary: CIF conversion drops primary occupancy and misaligns alternate sites across models.
issue: uibcdf/molsysmt#556
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: high
verification: reproduced
area: [form, convert, attribute]
guard: tests/form/mmcif_PdbxContainers_DataContainer/test_primary_occupancy.py
normative:
blocked_by: []
supersedes: []
---

# CIF conversion drops primary occupancy

**Reported:** DockingMT source-inspection work, uibcdf/molsysmt#556.
**Status:** Corrected and contract-tested; published in the source checkpoint
identified by the closing issue comment.

## What

The mmCIF DataContainer converter reads occupancy values to choose alternate
sites but does not append the selected values to native Structures. A synthetic
two-atom, three-model source loses all six explicitly declared occupancies.
Unknown tokens additionally raise float-conversion errors; an absent column
raises KeyError. The direct occupancy getter ignores requested structure indices. The adjacent
B-factor getter has the same independent selection defect.

```bash
python -m pytest --receptor=llm -n 4 \
  tests/form/mmcif_PdbxContainers_DataContainer/test_primary_occupancy.py
```

## How

`form/mmcif_PdbxContainers_DataContainer/to_molsysmt_MolSys.py` must retain the
occupancy array when appending structures, reduce it with the same canonical
atom selection as coordinates, and filter the model-number array after alternate
reduction. Alternate-site keys must include the model number: observations of
one atom in different models are not alternate positions in the same structure.

The correction keeps unknown cells as NaN and uses None when the entire primary
field is unavailable, matching native PDB-reader representation. Import selects
the largest known alternate occupancy, then label A among tied maxima, then
source order; all-unknown sites retain their first source variant and their
unknown occupancy. All raw variants remain available for explicit resolution.
This deterministic import policy is not the separate half-occupancy tie rule of
`build.solve_atoms_with_alternate_location`.

Group occurrences are also separated at model boundaries, even for a one-group
ligand whose chain/group labels repeat. This lets explicit per-group connectivity
apply independently to each model. The model comparison excludes generated
global component-name ordinals, which are not source identity labels; inventory
and component membership still distinguish different molecular systems.

The four CIF/BinaryCIF file adapters previously did not declare occupancy, so
their direct public query returned None even after the native converter repair.
They now advertise the existing native delivery route; no parallel reader is
introduced.

## Why

Dropping source observations prevents downstream inspection and conditional
acceptance of partially occupied sites. Filling the gap with ones or with another
format's positional array would invent evidence or assume an unverified mapping.
Correct acquisition does not certify protonation, molecular preparation or
docking readiness.

## What is measured and what is assumed

On main 532d0362, eleven synthetic receiving cases fail: two primary arrays are
None, three multi-model alternate cases fail native extraction, five unknown
token cases fail float parsing, and the absent-column case fails lookup. The
joint run with nine assembly controls records twenty failures in
`.pytest_cache/cif-556-563/before.xml` (exit 1).

Occupancy and coordinate expectations are literal source values, independent of
the converter and of PDB output. No real CIF/PDB atom-axis parity is assumed.
The source values are dimensionless; coordinates and B-factors carry angstrom
and squared-angstrom source units before PyUnitWizard conversion.

Initial receiving exposed two incorrect test assumptions: conversion retains
native sorted atom-extraction order, while direct queries retain requested
order; and unit conversion is checked with numerical tolerance rather than
floating-point identity. The corrected guards check both contracts explicitly.
A subsequent explicit-bond control reproduced a real model mismatch caused by
shared group occurrences and generated global component names; the guarded
repair retains the declared double bond in both structures. A changed atom
inventory still warns and returns separate systems.

## What was refuted

This is not missing source data in the synthetic case: non-unit occupancies
are explicitly present. Changing the alternate resolver alone cannot recover
observations already dropped by conversion. No new file parser, dependency,
Rust kernel or chemical store is required; every CIF/BinaryCIF route already
shares the owning DataContainer adapter.

## Scope and exclusions

Keep native primary occupancy, alternate evidence and selected atom/structure
axes coherent; retain missing values explicitly. Reuse native extraction,
append, quantity conversion and H5MSM persistence. Preserve existing public
signatures and format identities. No occupancy inference, cross-format positional
repair or general malformed-mmCIF grammar expansion is included.

## Acceptance criteria

The guard covers non-unit values, missing tokens/columns, per-model alternatives,
nonconsecutive/repeated structure selection, native conversion extraction order,
ordered/repeated direct atom queries, selected B-factor observations, H5MSM round trips and unchanged input categories. Neighboring native,
CIF/BinaryCIF, alternate-resolution, assembly and persistence tests pass.
Docstrings, User Guide, Cookbook and course explain the same acquisition policy.

## Provenance

Receiving uses the existing Linux/Python 3.14.7 development environment and the
published Pytest Receptor 1.2.1 overlay. The input categories are declared in the
guard module and written to local CIF text for the file route; no provider
download, private molecular input or additional test environment is needed.
DockingMT's original source evidence remains in uibcdf/molsysmt#556; it is not
replaced or relabeled as this synthetic validation.

## Resolution — 2026-11-05

The native converter now retains aligned primary occupancy and model-local
alternate records. File CIF/BinaryCIF and compressed adapters advertise the
working occupancy route. Groups restart on model boundaries, preserving explicit
per-group bonds; generated global component labels no longer prevent matching
models from being assembled into an ensemble. A different atom inventory still
produces the existing explicit mismatch warning and separate systems.

The direct occupancy and B-factor getters now forward structure selection to
their native delegate. An additional independent B-factor guard first reproduced
a `(2, 1)` result for a requested `(3, 1)` observation sequence, then verifies
`[20, 21, 20]` squared angstroms in the requested `[1, 0, 1]` structure order.

Broader source receiving passes 5,376 selected tests (exit 0, four workers).
A subsequent final B-factor forwarding correction has its own current-source
receiving of 2,481 tests (exit 0, four workers) in the shared JSON receipt.
All 34 focused occupancy/assembly cases
pass with the declared published support-library floors, including the B-factor
regression. The floor route disables only the installed SMonitor pytest plugin
under the existing #524 entry-point limitation; runtime diagnostics, argument
validation and every scientific assertion remain active. Source/provider and
installed-release qualification are distinct.

An earlier broader attempt was interrupted (exit 2): 5,225 passed and five
network-acquisition failures, with 154 selected cases unexecuted. All failures
were in eight unmarked live PDB-ID conversion tests; #573 records their module
marker correction. Offline collection now deselects all eight (expected exit 5),
and network collection still admits all eight (exit 0, no live execution claim).
The completed 5,376-case result follows that correction; the interrupted run is
not relabeled or included as a successful gate.

Documentation receiving passes 551 controls, and both reader doctest items pass.
The Cookbook occupancy block executes against the bundled public coordinate
file and round-trips its `(1, 596)` occupancy array. Seven changed notebooks
retain identical executable cells, saved outputs and notebook metadata; existing
live-provider examples are not claimed as newly executed. Ruff, form delivery,
soft-dependency import, course and devguide validation retain their own results.

The fix remains in the existing adapter and native delivery routes, reusing
ArgDigest, PyUnitWizard, ChemicalStates storage, SMonitor diagnostics and H5MSM.
There is no new optional engine, schema or scientific detection method to
register with Ackredit; no support-library floor changes. The existing native
Rust binary and four unrelated human edits are unchanged. Source/test/JUnit
hashes and exact scope are retained in
`devtools/data/mmcif_observations_receiving_556_563_20261105.json`.


## Receiving correction note — 2026-11-05, terminal H reinsertion

The broader #568 build receiving found one stale expectation in
`test_real_est_reinsertion_preserves_partial_complex_and_source_pose`: CIF
import now correctly retains occupancy, so adding atoms under the existing
intersection policy reports both `b_factor` and `occupancy` as dropped. The
test now requires source occupancy to exist, remain unchanged, and be absent
on the expanded output alongside the exact two-field report. This strengthens
source preservation and drop reporting without changing reinsertion behavior
or weakening the strict-policy rejection.
