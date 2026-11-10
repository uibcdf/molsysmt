# Benchmarking Contract

Active benchmark code and recorded JSON sessions live under `benchmarks/`.
Historical May 2026 interpretations, comparisons, paper notes, and implementation
plans are archived under `devguide/archive/benchmarking/`; they are not current
performance guarantees.

The operational [H5MSM benchmark guide](h5msm.md) documents the current
interaction-layer probe, recorded evidence, interpretation, and remaining
measurements for the modular 0.5 format.

The [ionic calculation guide](ionic.md) records molecular and synthetic
controls, projected H5MSM calculation, resident sparse output, independent
correctness checks, and eager/chunked timing and memory tradeoffs.

The [ring participant guide](rings.md) records chemistry preparation on known
isolated cycles and a large acyclic tail, with result buffer sizes and explicit
limits on interpreting total process memory.

The [resident native-copy guide](native_copy.md) measures actual molecular
copies, controlled edits/invalidation, coordinate consumers and complete-system
H5MSM 0.5 conversion. It distinguishes production paths from layout prototypes
and immutable backing bytes from allocator tracing and process RSS.

The [ChemicalStates separation comparison](../chemical_domain_separation_benchmarks.md)
records the dated #255 baseline/target measurements, including all-state copies,
large stable inventories, coordinate isolation and projected H5MSM reads. Its
machine-readable artifact retains ranges, source/backend hashes and the limits
of process high-water RSS.

## What to measure

Measure separately:

- cold import and first-use compilation;
- warm public API latency;
- argument/unit preparation;
- raw kernel execution;
- file I/O and conversion;
- peak memory and output size;
- eager versus chunked execution;
- CPU, parallel CPU, and each GPU backend.

Every timed scientific result needs a correctness or parity assertion outside
the timed region. A faster invalid or partial result is a benchmark failure.

## Reproducibility record

Each result must include commit, dirty-state flag, date, OS, Python and package
versions, CPU/GPU, memory, storage, thread settings, precision, cache/warm-up
state, input dimensions, repetitions, and raw samples or sufficient statistics.

Do not claim that a ratio is hardware-independent. Keep cold and warm results
separate, and do not combine dependency import time with algorithm runtime
unless the benchmark explicitly models end-user startup.

## Current implementation

The [session comparability contract](comparable_sessions.md) describes the
versioned competitive data, numerical prechecks, isolated case factories,
advisory warnings, unevaluable historical data and reviewed reference renewal.

The repository currently includes:

- `benchmarks/harness.py`, whose competitive route uses fresh spawn factories,
  warm-up calls, raw repeat samples and process high-water RSS; arbitrary
  closure/fork callbacks remain explicitly legacy and finitely bounded;
- micro digestion/unit benchmarks;
- macro kernel and trajectory benchmarks;
- an exact-parity direct-gather versus `pandas.merge()` topology-expansion
  benchmark for 100,000 atoms;
- competitor loading, geometry, and selection scripts;
- JSON snapshots under `benchmarks/baselines/`;
- `benchmarks/compare_runs.py` and an advisory GitHub Actions performance job.

The [performance observation policy](performance_policy.md) keeps scientifically
correct implementations available regardless of relative timing. Comparable,
consistent inefficiency above the default 15 percent threshold is improvement
issue evidence, not grounds for rejecting an implementation.

Important limitations:

- `fork` and `/proc` assumptions reduce portability;
- high-water RSS is not allocation attribution;
- the comparer reports medians, raw sample ranges and an advisory 15% threshold;
  these are not confidence estimates or runner calibration;
- missing reference measurements fail diagnostically; new unreferenced paths
  remain unassessed;
- stored competitor results are dated environment snapshots;
- declared workload/environment compatibility is checked conservatively; it
  does not establish equal shared-host contention or causal attribution. CI
  retains current/reference sessions separately and never renews the tracked
  reference during comparison.

Until these limitations are addressed, timing observations are signals, not
strong statistical evidence or attributed product regressions. See
[the remaining comparability work](../pending_proposals/benchmark_baseline_comparability_and_competitor_gating.md).

## Reporting rule

Reusable interaction preparation has separate operational guides:
[ring participants](rings.md) and [plane fitting](planes.md). Their synthetic
controls establish those bounded stages, not full pi-pi detector performance.

Publication, README, or release claims must link to the exact result artifact
and reproducible command. Re-run competitor comparisons against current pinned
versions and describe semantic differences; do not infer architectural
superiority from one operation or dataset.

The [cation-pi controls](cation_pi.md) separate attributed ProLIF geometry from
the custom proposal and record calculation, queries, memory and H5MSM costs.
Scientific comparison remains tracked by uibcdf/molsysmt#271.
