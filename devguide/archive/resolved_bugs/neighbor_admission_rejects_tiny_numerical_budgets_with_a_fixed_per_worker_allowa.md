---
summary: Neighbor admission rejects tiny numerical budgets with a fixed per-worker allowance.
issue: uibcdf/molsysmt#703
status: resolved
opened: 2026-11-10
closed: 2026-11-10
severity: medium
verification: reproduced
area: [structure, performance, tests]
guard: tests/interactions/ionic/test_chunked_ionic.py
normative:
blocked_by: []
supersedes: []
---

# Neighbor admission rejects tiny numerical budgets with a fixed per-worker allowance

## What / How / Why

On frozen 5f241cfa7 with canonical backend 58653b1d4, the complete default
suite has 33,519 passes, five failures and two intentional skips. Two failures
are ionic tiny-budget controls: a valid six-structure calculation with a 6,000-byte
numerical working budget rejects at 66,048 bytes; an 8,000-byte sparse-result
refusal is preempted at 65,920 bytes before its result accumulator runs.

Source inspection identifies an unconditional 65,536-byte allowance per Rayon
worker in neighbors.rs working_budget, beyond the population-bounded scratch
terms. No corresponding 64 KiB numeric allocation exists: new_scratch uses
three Vec descriptors with reference-population-bounded storage. This numerical
workspace budget is explicitly distinct from process RSS and worker stacks.

Replace the unexplained allowance with the actual scratch descriptor layout,
retaining conservative storage/reallocation accounting, checked sizes, observed
output charging and fail-closed allocation. Bound active scratch contexts by
query rows as well as workers. Do not raise the test budgets, alter ionic
criteria, change cutoff/MIC/order, or bypass admission.

Receive the unchanged ionic controls, direct tiny native budgets, large sparse
and dense output refusal, periodic/vacuum and threading paths, Rust tests,
scientific controls and the rebuilt canonical extension. This is a supplemental
correctness regression linked to #690, distinct from #692 advisory performance.
The complete failed session remains failed; targeted correction alone does not
claim a new full-suite or release matrix pass.

## Bounded baseline and correction — 2026-11-10

The direct ten-case baseline retains six failures and four passing too-small-
budget refusals, using the unchanged 58653b1d4 backend. Four failing direct
queries cover vacuum/periodic geometry and requested thread limits, with a
1,536-byte admitted numeric workspace; the original two ionic controls fail too.
No result, budget or expectation was changed to obtain those observations.

The source correction replaces 65,536 bytes with sizeof(Scratch), whose three
Vec descriptors are the actual numeric state, retaining 64 bytes per reference
entry for bounded buffers/reallocation. Active contexts are bounded by query
rows and worker count. Rust and public guards retain successful geometry and
small-budget refusal. The canonical rebuilt extension and broader receiving
are required before resolution; process RSS and worker stacks remain excluded
from this explicitly numerical allowance.

## Resolution — 2026-11-10

Source **93b3a6ea6** and canonical Rust 1.97.1 release backend
`4ffb82e4250a1862fff17dbe7725fb8f0770d613ffef2648370389a66983d345`
pass **133 directed cases**, **1,782 affected cases**, all **88 Rust tests**,
required library Clippy and **116 registered scientific cases / 74 nodes**.
Selections overlap and are not summed. Numerical outputs, original budgets,
refusal behavior, cutoff/MIC/order and complete warning/export assertions are
retained. No owned OOM or host-reserve stop occurs.

The [receiving record](../../../devtools/data/numeric_neighbor_budget_receiving_703_704_20261110.json)
retains the original complete default session: **33,519 pass, five failures and
two skips**. Its numerical-budget failures belong to #703; its three incomplete
peptide-control failures belong to #704. Targeted receiving corrects those
mechanisms; it does not turn that session green or replace a new full suite,
installed/platform or candidate qualification. The exact namespace remains
protected by `tests/chemical_states/test_namespace.py`; every catalog warning
remains protected by `tests/_private/smonitor/test_xdist_warning_reconstruction.py`.
No original plan credit, public scientific method or release authority changes.
