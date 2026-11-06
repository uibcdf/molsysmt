---
summary: mmCIF native conversion drops deposited model labels despite declared structure_id support.
issue: uibcdf/molsysmt#600
status: active
opened: 2026-11-06
closed:
severity: medium
verification: reproduced
area: [form, attribute]
guard: tests/form/mmcif_PdbxContainers_DataContainer/test_structure_ids.py
normative:
blocked_by: []
supersedes: []
---

# Missing mmCIF model-label delivery

## What

The DataContainer form declares structure_id capability but its public getter
returns None. Native conversion also leaves Structures.structure_id as None,
although source atom_site.pdbx_PDB_model_num labels are present. Coordinates and
selected structure indices remain available; labels and indices are distinct.

## How

The existing _container test fixture with three two-atom models explicitly
contains labels 1, 2, 3. A public native conversion selecting [2, 0] produces
shape (2, 2, 3) and no native model labels. Public has_attribute returns True;
get(structure_id=True) returns None. Inspection confirms the getter is an
unconditional stub and native construction does not publish model labels.
This was discovered during #304; that policy test does not silently establish
a new model-label guarantee.

## Why and acceptance

Retain exact deposited labels as native string IDs, independently of positions.
Check DataContainer, CIF/BCIF and gzip getter/conversion routes, nonconsecutive
and repeated selections, nondefault labels and appropriate persistence. Missing
labels and incompatible model inventories need explicit handling. Do not infer
labels from positions or mutate the source. The maintainer explicitly added
this report to the fifteen-issue goal after #599 and before #601; release
qualification remains separate.

## Provenance

Linux/Python 3.14.7, main/PR owner receiving base
282e8337e04c14003622c19a359b7cd35d2b5e4b plus local #304 policy changes.
The bounded public reproduction uses the existing fixture in
 tests/form/mmcif_PdbxContainers_DataContainer/test_primary_occupancy.py.
No network input, external structure redistribution or numerical-model claim.

## Implementation and verification — 2026-11-06

The shared private adapter model_axis helper retains original label spelling
separately from numeric model keys. It keeps the existing ascending numeric
coordinate-model order, stores only an atom-scale integer vector plus one label
per model, and is reused by conversion, model counts and the public label getter.
Every extracted native model receives its own string ID before compatible models
are appended. Genuine inventory mismatches retain their warning and separate
results with individually retained labels. No Topology chemistry facade, graph
repair, new dependency, unit-policy change or compiled calculation is introduced.

An entirely absent/unknown model column leaves IDs unavailable and interprets its
atom inventory as one unlabeled structure. Partly missing labels, noninteger or
out-of-range numbers and conflicting source spellings for one numeric model raise
FormatError. Model boundaries and IDs are not guessed from positions, duplicate
atom names or label counts. Public get/convert retain their ArgDigest boundary;
invalid source metadata uses existing SMonitor diagnostics with parsing causes.

All 23 initial focused controls fail against the previous implementation: missing
native/getter labels, unsupported unknown columns/cells, accepted ambiguous aliases,
and unlabeled separate-model results. They pass after the implementation.
Expanding unavailable-label controls across all five representations produces
**925 passing affected tests/doctests**, no failures or omissions, using the
published Pytest Receptor and twelve workers. This covers DataContainer, CIF,
BinaryCIF, both gzip routes and basic comparison, with 30 expected legacy-H5MSM
warnings. A separate bundled 1L2Y NMR control checks selected/repeated labels
against source model records and their independently read first-atom coordinates.
It is serial because it is one real-input control, not a second full-suite run.
**38 published-provider-floor cases pass**, including the focused synthetic
profile and public docstrings, with only the development SMonitor pytest plugin
disabled; runtime diagnostics and validation remain active.

The existing HP35 getter test now verifies its actual deposited label '1' rather
than asserting the previous unconditional None stub. No geometry tolerance,
model-compatibility predicate or strict native guard is relaxed. Source rows and
file bytes remain unchanged. Leading zeros, numeric model reordering,
nonconsecutive/repeated selections and H5MSM persistence are explicitly covered.
Local receipts: .pytest_cache/600-model-labels-before.xml,
600-model-labels-after.xml, 600-affected-final.xml, 600-provider-floors.xml and
600-real-nmr-labels.xml.

Public getter/converter docstrings, the five form overviews, native Structures
Foundations, the conversion Cookbook and Module 19 describe labels versus indices
and explicit ambiguity limits. Seven narrative notebook cells change; every code
cell, output, cell count and notebook metadata remain unchanged. Module 19's
existing code does not directly consume CIF/BinaryCIF; the public model-label
contract is executed in the focused guards and doctests. The incremental complete
Sphinx HTML build passes without warnings. Twenty unrelated generated autosummary
stubs are restored to their prior committed bytes in the isolated worktree.
The actual public forms remain experimental; no H5MSM schema or release is changed.
