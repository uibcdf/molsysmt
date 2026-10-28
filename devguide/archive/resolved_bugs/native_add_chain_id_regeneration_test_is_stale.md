---
summary: Native add chain-ID regeneration test expects an obsolete numeric policy.
issue: uibcdf/molsysmt#522
status: resolved
opened: 2026-10-28
closed: 2026-10-28
severity: low
verification: reproduced
area: [tests, structure]
guard: tests/basic/add/test_chain_identifiers.py::test_native_topology_add_keeps_labels_and_can_explicitly_regenerate_them
normative:
blocked_by: []
supersedes: []
---

# Native add chain-ID test expects an obsolete numeric policy

**Reported:** 2026-10-28, receiving native composition for
uibcdf/molsysviewer#264 / uibcdf/molsysmt#421.
**Status:** resolved; the regression now follows the alphabetic string-ID policy.

## What

On 5bcd2b76086b1fc4af9d1ab595cfb2866fad7d41 the affected-source receiving
passes 812 cases and fails one stale native test. The guard
`tests/basic/add/test_chain_identifiers.py::test_native_topology_add_keeps_labels_and_can_explicitly_regenerate_them`
expects `['0', '1', '2']` after `keep_ids=False`; native output is
`['A', 'B', 'C']`.

## How

`Topology.rebuild_chains` documents generated IDs as A through Z, then AA, AB
and onward, using the shared chain-name generator. The hierarchy extension
changed this implementation/contract but retained the old numeric assertion.
The accepted repair changes only that expected output and checks string dtype
after regeneration. The scientific implementation remains unchanged.

## Why

The stale test blocks valid composition qualification. `keep_ids=True` must
still preserve duplicate explicit IDs independently of chain positional indices,
and the source labels must remain untouched. This does not reopen #353 or infer
biological identity from generated labels.

## What is measured and what is assumed

The exact failure is reproduced on the isolated source checkout with the suite
Python 3.14 environment. The current implementation and docstring agree.
The source is a bundled real molecular system; no Viewer or mock is involved.

## Acceptance criteria

The named guard and complete test module pass with alphabetic string IDs;
duplicate declared IDs, selected source remapping, source preservation and
writer checks retain all their assertions. No scientific algorithm, library
floor or published tag changes.


## Resolution — 2026-10-28

Only the stale expected labels change to A/B/C; an additional dtype assertion
keeps regenerated IDs explicitly string-valued. All existing keep_ids=True,
source-preservation, selected-source mapping and PDBQT writer checks remain.
The addressed guard passes (1/1), followed by the entire module (5/5), against
5bcd2b76086b1fc4af9d1ab595cfb2866fad7d41 plus this test-only adjustment.
No scientific implementation or provider/consumer normalization changes.
The prior 812/813 receiving result remains a distinct recorded failed attempt.
