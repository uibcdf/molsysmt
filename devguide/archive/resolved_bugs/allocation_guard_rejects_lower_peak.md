---
summary: Correct allocation guard that rejects lower memory consumption
issue: uibcdf/molsysmt#412
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: low
verification: reproduced
area: [tests, performance]
guard: tests/interactions/test_frame_replacement.py::test_replacing_one_frame_does_not_copy_large_occurrence_tables
normative:
blocked_by: []
supersedes: []
---

# Allocation growth guard

## What

The sparse replacement allocation guard takes the absolute difference between
small and large input peaks, rejecting sufficiently large reductions as well as
increases. That contradicts its purpose of detecting growing edit allocations.

## How

Compare `large_peak - small_peak` with the existing 30,000-byte growth ceiling.
Warm one ordinary validated call on a separate source before tracing, then collect
garbage before each fresh measured source. Exclude one-time validation/provider
initialization from the per-edit growth check, keeping measured sources fresh.
Stop tracing in a finally block. Keep the existing 100,000-byte maximum peak
ceiling unchanged. No production code, measured workload size or threshold changes.

## Why

The final #406 regression selection measured 52,365 bytes for 100 occurrences
and 7,373 bytes for 200,000 occurrences. Its absolute difference, 44,992 bytes,
failed despite reduced memory use. Full copies of a 200,000-row occurrence column
would still exceed the unchanged absolute ceiling; individual evidence entries
alone occupy 800,000 bytes before array overhead.

## What is measured and what is assumed

The values above are the actual failing tracemalloc peaks from
`tests/interactions/test_frame_replacement.py::test_replacing_one_frame_does_not_copy_large_occurrence_tables`
in the 2026-10-22 Linux/Python 3.14.7 source regression run. They are traced
allocations, not process RSS or a performance campaign. Initial-call/caching noise
is a possible explanation for the difference, not an established root cause.
The wrong comparison direction is established regardless of that explanation.

An additional run recorded 167,342 bytes for the small case and 7,533 for the
large one: the original cold, uncollected measurement can also exceed its absolute
ceiling before the large table is involved. Warm-up and garbage collection make
the intended per-edit measurement boundary explicit; they do not establish a
lower first-ever invocation cost or attribute every incidental allocation.

## What was refuted

This failure does not demonstrate dense occurrence copying. Increasing the
ceilings or dropping the allocation guard would weaken its intent and is not
needed: only allocation growth, not reduction, should fail its growth check.

## Scope and exclusions

One existing allocation test. Sparse replacement/sharing assertions remain.
No claim of universal allocation stability, scientific accuracy or release readiness.

## Acceptance criteria

The allocation test and adjacent replacement tests pass with both existing
ceilings, source blocks and unpacked replacement state still asserted.

## Resolution

The growth comparison no longer penalizes reductions. A separate validated
warm-up and explicit garbage collection isolate per-edit allocations before
tracing fresh small and large sources. Both numerical ceilings remain unchanged.
The complete replacement module passes in the final 125-case focused selection
recorded under #406. Production interaction code is unchanged; no first-ever-call
allocation guarantee or universal memory improvement is inferred.
