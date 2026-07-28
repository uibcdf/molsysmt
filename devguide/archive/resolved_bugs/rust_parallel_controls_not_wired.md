# Rust Parallel Controls Were Not Wired to Rayon

**Status:** resolved
**Release relevance:** pre-1.0 API-contract decision
**Discovered:** 2026-07-28 during the Rust-only cut
**Resolved:** 2026-07-28

## Problem

Several public structure functions accept `parallel` and `num_threads`, and the
configuration module still exposes `parallel_mode`, `num_threads`,
`parallel_threshold`, and `min_payload_per_thread`.

The Rust kernels do execute in parallel: distance, RMSD, geometry, SASA,
neighbour-list, and related implementations use Rayon, while PCA configures
Faer's Rayon parallelism. However, the Python controls are not currently passed
to those native implementations. Rayon therefore uses its own global pool and
the advertised per-call controls do not determine the active thread count.

This is not a loss of parallel execution. It is a mismatch between the public
control surface and the runtime behavior.

## Why it matters

- A user may request `num_threads=1` and reasonably expect serial execution.
- Nested parallel applications need a way to prevent oversubscription.
- Benchmarks that vary `parallel` or `num_threads` would currently measure the
  same native thread policy.
- Leaving documented but ineffective controls would weaken trust in the 1.0
  API contract.

## Decision

MolSysMT retains both intended control levels:

- session defaults through `molsysmt.configure`;
- `parallel` and `num_threads` overrides on an individual public operation.

The implementation does not resize Rayon's global pool. It caches independent
Rayon pools by thread count and installs each native operation in the pool
selected by the resolved policy. A Python `ContextVar` carries function-local
overrides through nested public calls without mutating session configuration.

## Runtime contract

- `parallel=None`, `num_threads=None`: inherit the session;
- `parallel=False`: use one thread;
- `parallel=True`: use the requested or session thread count;
- `parallel="auto"`: select from payload size, thresholds, and the thread limit;
- `num_threads=-1`: use the processors available to the process;
- contradictory local `parallel=False, num_threads=N` with `N != 1`: raise
  `ArgumentConflictError`.

Nested decorated operations inherit the outer function override. Session
contexts remain module-global and are covered by the separate configuration
thread-safety report.

## Native implementation

Parallel work is split across independent outer slabs or blocks. Inner
coordinate and reduction loops remain sequential and contiguous where possible
so release compilation can auto-vectorize them. RMSF uses parallel folds over
contiguous structure slabs and merges per-worker accumulators instead of
walking strided atom columns.

Faer's process-global PCA parallelism setting is protected while the operation
runs, and the calculation is installed in the selected Rayon pool.

## Evidence

- Rust unit suite: 80 passed.
- Affected Python surface: 165 passed.
- Direct pool observation in one process: pool sizes 1, 2, and 1 are selected
  in sequence, demonstrating reusable non-global sizing.
- Tests cover session inheritance, local overrides, nested overrides,
  automatic thresholds, conflicts, and serial/parallel numerical agreement.
- Representative release-build minimum timings and four-thread speedups on the
  investigation host:

  | Kernel | 1 thread | 4 threads | Speedup |
  | --- | ---: | ---: | ---: |
  | distance matrix | 0.1553 s | 0.0519 s | 2.99× |
  | weighted centers | 0.2446 s | 0.0691 s | 3.54× |
  | radius of gyration | 0.3614 s | 0.1030 s | 3.51× |
  | RMSF | 0.0645 s | 0.0236 s | 2.73× |

These measurements demonstrate scaling on one host; they are not portable
performance guarantees. Oversubscription and the full platform matrix remain
Segment E validation work.
