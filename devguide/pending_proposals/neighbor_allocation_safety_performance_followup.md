---
summary: Profile allocation-safe neighbor search overhead without weakening resource guards.
issue: uibcdf/molsysmt#692
status: open
opened: 2026-11-10
closed:
verification: measured
area: [structure, performance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Profile allocation-safe neighbor search overhead without weakening resource guards.

## What

Investigate the additional CPU cost of #690 while preserving checked sizing,
population-bounded grids and observed-output admission. This is advisory work,
not a numerical defect or a new release blocker.

## How

The [paired pilot](../../devtools/data/native_neighbor_allocation_receiving_690_20261110.json)
records one controlled CPU, same inputs/runtime, three warmups and fifteen
repetitions on each of three 4 × 1,000-atom workloads. Median new/old ratios are
1.1542 compact vacuum, 1.0786 compact periodic and 1.2149 dilute vacuum.
Offsets/indices agree exactly and distances within 1e-13 nm. The old/new order,
short duration and kernel-only scope do not establish a representative ranking.

## Why

The accepted #567 policy keeps correct implementations available. Investigate
comparable differences above roughly 15% with measurements, rather than
removing a correct tool or weakening its resource/scientific guard.

## Acceptance and exclusions

Repeat interleaved comparable campaigns, profile occupancy/coarsening, atomic
admission and small-query scheduling, then document an optimization or an
accepted safety tradeoff. Preserve independent geometry and budget controls.
No new dependency, API, cutoff floor, schema or release-scope requirement.

## Python projection follow-up from #693 — 2026-11-11

The [compatibility-output receipt](../../devtools/data/compatibility_output_memory_693_20261110.json)
adds separate Python projection measurements. It does not remeasure #690's
native kernel. The bounded output model reduces large neighbor-row peaks and
mapped-contact projection peaks; those paths also improve in the measured
untraced timings. Unmapped self-contact conversion remains an advisory warning:
current/legacy median ratios are approximately 1.48, 1.85 and 1.69 for 16, 128
and 512 atoms, with bounded counting/packing instead of whole-map temporaries.
The 512-atom median is about 36.7 ms versus 21.7 ms. Tiny unmapped cases can
also increase peak allocation as fixed/slab overhead dominates; keep those
samples visible rather than asserting a universal improvement.

These are one controlled CPU, two warmups/five samples, projection-only
observations. Alternating order, broader sparse populations and profiling are
needed before a representative performance conclusion. Evaluate vectorized
bounded counting/packing and reuse of sparse occurrence output without weakening
the memory guard, label ordering, periodic/cutoff semantics or empty results.
This warning remains in the open advisory issue under #567. Correctness passing
and reduced peak allocation justify the bounded route; it is not a release gate.
