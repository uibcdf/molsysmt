---
summary: Selected hierarchy counts follow missing parent indices
issue: uibcdf/molsysmt#392
status: resolved
opened: 2026-10-21
closed: 2026-10-21
severity: medium
verification: reproduced
area: [attribute, selection]
guard: tests/native/test_native_queries.py::test_selected_hierarchy_counts_exclude_missing_membership
normative:
blocked_by: []
supersedes: []
---

# Selected hierarchy counts follow missing parent indices

**Reported:** 2026-10-21, during native get/info implementation under
uibcdf/molsysmt#128.
**Status:** Resolved through the existing nullable hierarchy provider.

## What

A valid atom inventory without assigned groups cannot be summarized over an
explicit atom subset. The group count includes the missing-parent sentinel;
the molecule/entity count uses that sentinel as an array index:

```python
import molsysmt as msm
from molsysmt.native import MolSys

molsys = MolSys(n_atoms=4)
msm.get(molsys, element='atom', selection=[2], n_molecules=True)
# IndexError: arrays used as indices must be of integer (or boolean) type
```

Typed group/molecule counts used by system summaries follow the same missing
links. An explicitly selected atom without declared parent membership must
contribute zero memberships rather than invent a group or fail.

## How

The native Topology form provider indexes NumPy group/molecule arrays with
unassigned atom-to-group or group-to-molecule links. Several counts apply
`unique` to the link array without excluding nulls. The existing
`_get_hierarchy_from_atom` helper already resolves nullable parent links safely
for identity attributes, but the count providers did not use it.

Selected group/molecule/entity counts now reuse that mapping; chain counts use
their independent atom-aligned declared chain links. Typed group/molecule
counts deduplicate only existing mapped parents before applying the original
type criterion. Full-system calls retain complete declared table counts,
including declared but currently unrepresented parents. No group classification
or hierarchy reconstruction is performed.

## Why

Small molecules and partial native inventories can legitimately lack groups.
Both native methods and the form-agnostic toolbox need the same coherent
membership semantics. Fixing only an info wrapper would leave the public get
attribute routes incorrect and duplicate mapping rules.

## What is measured and what is assumed

The failure was executed through the shared provider while running the new
native spatial-summary tests. The inspected original provider is present in
source `3466ba8f0901aa7136c54ee9b4bbaeb3b28335b8`. Literal zero-count and
partial-parent fixtures exercise the correction; no performance claim is made.

## What was refuted

The error is not a parser failure or wrong structure index: a plain explicit
atom subset follows the same failing parent-index path. Creating fabricated
groups to make the query succeed would change the molecular inventory and is
not a valid repair.

## Scope and exclusions

Selected hierarchy and typed hierarchy counts in the native Topology provider.
Keep existing public functions/signatures, type criteria and full-inventory
counts. This does not change group recognition, chemical connectivity,
component inference, molecular construction or external-format interpretation.

## Acceptance criteria

- No-parent atom subsets return zero group/molecule/entity/chain memberships.
- Partially assigned hierarchy counts only explicit links and distinct parents;
  repeated atoms do not duplicate parents and empty selections count zero.
- Preserve the original group- versus molecule-type criteria.
- Basic and native access share the corrected providers; selected system info
  works without inventing group labels.
- Run existing basic/native/interaction regressions and update the native
  query guidance and affected public count docstrings/examples.

## Provenance

Linux x86_64, Python 3.14.7 development environment, 2026-10-21.
Fixtures use four unassigned atoms and five atoms with explicit partial parent
links. They need no external molecular files or engines.


## Resolution — 2026-10-21

**Contract-tested.** Selected hierarchy counts reuse nullable parent mappings;
typed counts share one helper with the original group/molecule type criteria.
Chain counts use their independent declared atom-chain links. Full inventory
counts remain distinct from selected represented membership counts.

The guard asserts literal zero memberships for unassigned atoms through basic
and native queries and an independently expected selected-system summary.
`test_hierarchy_counts_follow_only_explicit_parent_links` additionally checks
partial group/molecule/entity/chain links, typed groups/molecules, duplicate
atoms and empty selections. The old providers count a missing sentinel or
index an empty table and fail these expectations.

The combined basic/native/interaction/connectivity selection passes 2,285 tests.
The updated count docstrings and existing adjacent count examples pass 34
executed doctest examples. The native-query contract and executed guide/course
examples retain missing hierarchy rather than synthesizing labels.
