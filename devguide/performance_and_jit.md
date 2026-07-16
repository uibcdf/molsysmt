# Performance and JIT Contract

This document records the maintained execution contract. Historical performance
notes and pre-1.0 claims are archived under `archive/assessments/`; measured
speedups are valid only with a dated benchmark environment and result file.

## Boundaries

MolSysMT separates three responsibilities:

1. public wrappers validate arguments, preserve units, shape outputs, and emit
   diagnostics;
2. preparation helpers extract and align numerical arrays;
3. kernels under `molsysmt/lib` operate on prepared, unit-free values.

Validation may be bypassed internally only when the caller can prove that the
values already satisfy the callee's contract. `ValidatedPayload` passports and
`skip_digestion=True` are trusted-path mechanisms, not general performance
switches. Do not apply either to unvalidated user input.

## Imports and lazy compilation

- Soft dependencies must remain lazily imported.
- Numba kernels should use `molsysmt._private.jit.lazy_njit` rather than eager
  compilation at import time.
- Kernel signatures, nested calls, and cache behavior must be covered by tests.
- First-call compilation latency and steady-state runtime must be measured
  separately.

Use the maintained warm-up entry point when precompilation is useful:

```python
import molsysmt as msm

report = msm.warmup(strict=True, return_report=True)
```

`msm.warmup_numba()` remains a compatibility alias but is deprecated for new
code. The default return remains the compiled-kernel count. A structured report
distinguishes loaded attributes, expected optional-dependency skips, and
unexpected failures. Use `strict=True` in QA so unexpected lazy-import failures
propagate immediately.

## Precision

`molsysmt.configure.precision` defaults to `"double"`. Structure preparation
helpers select `float64` in double mode and `float32` in single mode. The heavy
trajectory chunk contract is different: `ChunkedExecutor._build_chunk()`
currently normalizes coordinates, box, and time to `float64` canonical values.

Consequently, do not document a package-wide float64 or mixed-precision
guarantee. Each public operation and backend needs parity tests for every
precision mode it exposes.

## CPU parallel execution

`lazy_njit` may compile kernels with Numba parallel support and choose the
active thread count from:

- `parallel_mode` (`"auto"`, `True`, or `False`);
- `num_threads`;
- `parallel_threshold`;
- `min_payload_per_thread`.

Only kernels compiled with `parallel=True` use this runtime branch. The current
payload heuristic uses the largest NumPy array argument; it is not a general
cost model and no fixed speedup is guaranteed.

`molsysmt.configure.context()` and `with_configure_overrides` mutate module-level
configuration. They restore values for ordinary nested, single-threaded use,
but they are **not thread-safe**. Do not overlap configuration contexts across
threads until the defect in
`pending_bugs/configure_context_is_not_thread_safe.md` is resolved.

Numba thread-count changes are process-global runtime state. Concurrent callers
that request different thread policies need dedicated tests before concurrency
can be advertised as supported.

## Copies, views, and mutability

Native structural arrays are protected against accidental mutation in important
paths, and trusted helpers avoid unnecessary conversions when possible. This is
not a universal zero-copy guarantee: unit wrappers, dtype normalization,
selection, alignment, and backend transfers may allocate. Any zero-copy claim
must identify the exact form, property, unit backend, dtype, and identity test.

## Fast tracks and fast paths

- A PyUnitWizard **fast track** accelerates a known unit conversion or quantity
  operation.
- A MolSysMT **fast path** accepts an already validated payload at an internal
  boundary.

Neither mechanism weakens public validation or scientific invariants.

## GPU and out-of-core execution

GPU dispatch is described in `gpu_acceleration.md`. Chunked trajectory
processing is described in `SCALABILITY.md`. These paths have operation-specific
eligibility and fallback rules; their existence does not imply that every
operation, form, precision, or output type is accelerated.

## Topology selection expansion

Native selection and `Topology.get_atom_indices()` share a direct hierarchy
gather implemented in `molsysmt._private.topology_expansion`. It replaces the
former repeated `pandas.merge()` pipelines while preserving inner-join handling
of invalid hierarchy links, atom ordering, and source dtypes. The parity tests
and reproducible 100,000-atom benchmark are described in
`pending_proposals/topology_selection_indexing_and_pyarrow.md`.

## Benchmark evidence

Performance claims require:

- date, commit, Python and dependency versions;
- CPU/GPU and storage details;
- warm/cold state and repetition count;
- input system dimensions and units;
- correctness or parity checks;
- raw machine-readable results.

The benchmark material under `devguide/benchmarking/` is a mixture of active
guidance, observations, and proposals. It must not be used as a timeless
performance guarantee.
