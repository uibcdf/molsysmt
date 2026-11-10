---
summary: Neighbor admission rejects tiny numerical budgets with a fixed per-worker allowance.
issue: uibcdf/molsysmt#703
status: active
opened: 2026-11-10
closed:
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
