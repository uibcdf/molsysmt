---
summary: mmCIF native conversion drops deposited model labels despite declared structure_id support.
issue: uibcdf/molsysmt#600
status: open
opened: 2026-11-06
closed:
severity: medium
verification: reproduced
area: [form, attribute]
guard:
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
labels from positions or mutate the source. This report is separate from the
active ordered-resolution list; no implementation or release is claimed.

## Provenance

Linux/Python 3.14.7, main/PR owner receiving base
282e8337e04c14003622c19a359b7cd35d2b5e4b plus local #304 policy changes.
The bounded public reproduction uses the existing fixture in
 tests/form/mmcif_PdbxContainers_DataContainer/test_primary_occupancy.py.
No network input, external structure redistribution or numerical-model claim.
