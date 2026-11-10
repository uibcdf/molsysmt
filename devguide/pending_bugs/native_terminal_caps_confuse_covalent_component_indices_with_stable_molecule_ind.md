---
summary: Native terminal caps confuse covalent component indices with stable molecule indices
issue: uibcdf/molsysmt#684
status: active
opened: 2026-11-09
closed:
severity: medium
verification: reproduced
area: [build, selection]
guard: tests/build/add_missing_terminal_cappings/test_selection_axis.py::test_selection_reaches_only_the_touched_component_after_atom_repair
normative:
blocked_by: []
supersedes: []
---

# Keeping covalent component keys separate from stable molecule membership

## What

While extending #679's two-component control, both native and MDTraj routes
repair 79 source atoms to 80 but cap only one peptide, returning 92 instead of
104 atoms. The source remains unchanged. A missing CB leaves disconnected H
atoms, so covalent component indices differ from stable molecule positions.

## How

The caller keys cap placements by covalent component index. The shared native
reconstruction helper looks those keys up using stored molecule_index. Equal
indices on simple one-component examples conceal the error. The actual public
two-peptide test fails independently of the earlier selection-axis problem.

## Why and correction

Locate cap insertions by the declared first/last source group of each component.
Read its chain and component identity from that component's anchor atoms, and
inherit stable molecule membership separately from the source group. Do not
infer correspondence from equal counts, labels or coincident numeric positions.
Ambiguous repeated endpoint groups are refused before publication. Existing
chemical assignments, coordinates, source ownership and stable molecule tables
retain their native expansion contracts.

## Acceptance

Both native and actual MDTraj sources must receive the two intended caps per
selected peptide even after atom reordering or component renumbering; verify
52 atoms per completed AlaValPro component, expected group sequence, source
preservation and two stable molecules. Existing placement/domain tests must
still pass. This does not expand the scientific placement model to arbitrary
branched/cyclic chemistry or certify a force-field-ready chemical state.
