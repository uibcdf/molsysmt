# MolSysMT 1.0 Rust Runtime Benchmark

**Date:** 2026-07-28  
**Exact source commit:** `746e22c5f87c031c25eaba98aa53b64818582f32`  
**Machine-readable result:** `release_1_0_rust_runtime_benchmark.json`

## Purpose

This artifact closes release stage E6. It measures the maintained Rust-only
runtime rather than comparing it with the retired Numba implementation. The
benchmark separates:

- native import and first-call latency;
- repeated-call latency;
- peak resident memory;
- explicit 1/2/4-thread scaling;
- bounded concurrent calls using multiple Rayon pools;
- absence of Numba JIT cache creation.

Every timed workload checks its numerical result. Timings are measurements on
one host, not portable performance guarantees.

## Reproduction

```bash
python benchmarks/rust/bench_release_runtime.py \
  --output devguide/release_1_0_rust_runtime_benchmark.json
```

The command was run from a clean checkout of the exact commit above. Each case
ran in a fresh child process. The JSON records Python, NumPy, platform, CPU,
logical CPU count, source path, private-extension path, and the SHA-256 of the
executed native binary.

The editable environment exposed stale distribution metadata
(`0.20.0+163.g8606b24c9.dirty`). That string is not used as source identity.
The clean Git commit and native-extension SHA-256 are the authoritative
evidence. Installed-wheel identity belongs to C4/E4 and is intentionally not
claimed here.

## Results

Environment:

- Python 3.13.12;
- NumPy 2.3.5;
- Intel Xeon E5-2630 v4, 20 logical CPUs;
- native extension SHA-256
  `7bcc90b31a5aef8329a58caffde5f5f9915f2e17fda866a6b5b54860dab4a1d4`.

Observed results:

| Contract | Result |
| --- | --- |
| Native import | 0.4482 s |
| First native call | 0.0110 s |
| Best repeated call | 0.0069 s |
| First/repeated ratio | 1.60x |
| Numba cache files created | 0 |
| Payload for memory case | 27.48 MiB |
| Incremental call peak | 3.80 MiB |
| Two-thread speedup | 1.93x |
| Four-thread speedup | 3.47x |
| Nested-concurrency case | four simultaneous calls, two Rayon threads each |
| Nested-concurrency result | all four results correct; completed in 0.527 s |

The thread measurements used a `(1200, 2500, 3)` float64 coordinate array and
five raw timing samples per thread count. The full samples are retained in the
JSON artifact.

## Interpretation

- Ahead-of-time Rust execution has a small first-call effect attributable to
  ordinary import, allocation, pool, and cache state; there is no JIT
  compilation phase or Numba cache.
- The representative center kernel scales materially through four threads on
  this host.
- Four concurrent Python calls using bounded two-thread Rayon pools complete
  without corruption, deadlock, or unbounded global-pool mutation.
- The native call adds a small measured high-water increment relative to its
  input payload for this reduction workload.

This artifact complements, rather than replaces, the complete `-n 12` suite,
the threading-boundary regressions, and the installed-wheel matrix.
