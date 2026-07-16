# Benchmarking Contract

Active benchmark code and recorded JSON sessions live under `benchmarks/`.
Historical May 2026 interpretations, comparisons, paper notes, and implementation
plans are archived under `devguide/archive/benchmarking/`; they are not current
performance guarantees.

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

The repository currently includes:

- `benchmarks/harness.py`, which uses a forked subprocess, warm-up call, repeated
  timings, and process high-water RSS;
- micro digestion/unit benchmarks;
- macro kernel and trajectory benchmarks;
- an exact-parity direct-gather versus `pandas.merge()` topology-expansion
  benchmark for 100,000 atoms;
- competitor loading, geometry, and selection scripts;
- JSON snapshots under `benchmarks/baselines/`;
- `benchmarks/compare_runs.py` and a GitHub Actions regression job.

Important limitations:

- `fork` and `/proc` assumptions reduce portability;
- high-water RSS is not allocation attribution;
- the comparer uses a single median and fixed 15% cutoff without confidence or
  runner calibration;
- missing/new benchmark keys do not fail the comparison;
- stored competitor results are dated environment snapshots;
- the CI job overwrites a tracked baseline path during its current run.

Until these limitations are addressed, the regression job is a useful signal,
not strong statistical evidence. See
`pending_proposals/benchmark_regression_gate_reliability.md`.

## Reporting rule

Publication, README, or release claims must link to the exact result artifact
and reproducible command. Re-run competitor comparisons against current pinned
versions and describe semantic differences; do not infer architectural
superiority from one operation or dataset.
