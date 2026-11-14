---
summary: select ignores invalid structure indices for numeric and all selections
issue: uibcdf/molsysmt#750
status: resolved
opened: 2026-11-13
closed: 2026-11-13
severity: medium
verification: reproduced
area: [api, basic]
guard: tests/basic/select/test_structure_scope.py::test_all_selection_branches_refuse_invalid_structure_indices
normative:
blocked_by: []
supersedes: []
---

# Selection branches ignore an invalid explicit structure scope

## What

During #746's finite molecular-owner review, a six-call public probe on clean
`0dc250bb9` shows that `select(..., selection=[0] or 'all',
structure_indices=[9] or [-1])` returns atom indices on a three-structure
source. The equivalent `atom_index==0` expression raises ArgumentError.
The complete pre-correction regression reports 12 failures and six passes:
scalar/list/all selections do not raise on both native MolSys and H5MSM;
expression refusals and valid repeated structure requests pass.

```bash
python -m pytest --receptor=llm -n0 tests/basic/select/test_structure_scope.py
```

## How

`basic.select` previously called the existing structure-index validator only
inside its expression branch. Earlier numeric and all-element branches bypassed
it. The correction moves the same check before the branches and removes the
old duplicate expression-site call. Its metadata/count route and original
ArgDigest/SMonitor contracts remain; no coordinate or chemical calculation is
added. Bounds are asserted against available axis cardinality, not fabricated
for an undeclared source domain.

## Why

An explicit unsupported context must not look accepted because the membership
selector happens to be static. BindingMT #111/#746 needs actual index facts,
while counts and labels remain caller-declared correspondence rather than
source authentication. The caller must still admit the source and the required
axis; the provider now consistently refuses known out-of-range structures.

## What was refuted

The original failure does not require molecular geometry or an external parser.
The same two structure bounds already refuse with a string expression. Native
and H5MSM cases expose the same branch discrepancy. No new matching or validation
framework is necessary: the shared helper already expresses the intended rule.

## Resolution and acceptance

The new guard covers negative and high bounds on scalar, numeric-list, all and
expression branches in both forms; valid `[2,0,2]` structure scope preserves
numeric atom order. The selected owner/query/map/selection receiving passes
356 cases without omissions, followed by 18 final state/persistence controls.
The User Guide and Common Core selection lesson explain the refusal while
preserving every executable cell, output, cell order and metadata. The docstring
states the rule. The [receipt](../../../devtools/data/binding_membership_receiving_746_750_20261113.json)
records exact source, actual outcomes, applicable quality checks, units and
bounded resource limits. This closes the owning validation defect, not the
consumer's molecular resolution or final installed-pair qualification.

## Provenance and limits

2026-11-13, Linux/Python 3.14.7, unchanged native ABI3 `4ffb82e4`, frozen
provider composition in the receipt. Serial one-CPU/two-GiB services preserve
a monitored 6.5-GiB host reserve, zero own swap and original records. There is
no new engine, public API argument, dependency floor or scientific method.
Complete-source/nightly and exact-candidate gates remain due; candidate,
hosted, tag and publication pauses remain.
