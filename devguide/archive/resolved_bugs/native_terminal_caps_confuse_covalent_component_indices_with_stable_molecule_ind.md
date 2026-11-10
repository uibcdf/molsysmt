---
summary: Native terminal caps confuse covalent component indices with stable molecule indices
issue: uibcdf/molsysmt#684
status: resolved
opened: 2026-11-09
closed: 2026-11-09
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


## Resolution — 2026-11-09

Component endpoint groups locate cap insertion independently of stable molecule indices. The former 92-atom result becomes the expected 104 for both real source forms. Native stable molecule membership remains two; external MDTraj retains its own connected-molecule interpretation. Ambiguous repeated endpoint groups refuse before publication; no new placement science or force-field-ready state is claimed.

Clean c643a728f receives 170 expanded placement/repair/writer/doctest controls,
sixteen tiny benchmark/evidence controls, fourteen fast gates and five inspected
HTML pages. Failures remain distinct, including corrected fixture assumptions.
The [core receipt](../../../devtools/data/incoming_core_receiving_677_679_680_684_20261110.json)
and [consumer receipt](../../../devtools/data/terminal_audit_consumer_receiving_679_20261110.json)
retain exact source identities and limits. This adds no weighted milestone bonus
and does not qualify installed/platform/final-candidate or addon GUI behavior.
