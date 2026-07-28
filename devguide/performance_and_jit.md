# Performance and Native-Kernel Contract

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

## Imports and native compilation

- Soft dependencies must remain lazily imported.
- Numerical kernels are compiled into the private `molsysmt._rust` extension
  when the distribution is built.
- Supported installations must contain that extension; there is no Python or
  JIT fallback.
- Kernel signatures, error conversion, GIL release, thread behavior, and
  numerical properties must be covered by tests.

There is no kernel warm-up API. Applications that intentionally want eager
Python imports should import the required public namespaces explicitly.

## Precision

`molsysmt.configure.precision` defaults to `"double"`. Structure preparation
helpers select `float64` in double mode and `float32` in single mode. The heavy
trajectory chunk contract is different: `ChunkedExecutor._build_chunk()`
currently normalizes coordinates, box, and time to `float64` canonical values.

Consequently, do not document a package-wide float64 or mixed-precision
guarantee. Each public operation and backend needs parity tests for every
precision mode it exposes.

## CPU parallel execution

Selected native kernels use Rayon internally. Parallelization has two
compatible control levels:

```python
import molsysmt as msm

# Session policy
msm.configure.set_parallelization(parallel="auto", num_threads=8)

# One-call override
distances = msm.structure.get_distances(
    molecular_system,
    parallel=True,
    num_threads=2,
)
```

`parallel=None` and `num_threads=None` inherit the session policy.
`parallel=False` selects a one-thread pool for that call. `parallel=True`
selects the configured or explicitly requested thread count. In `"auto"` mode,
payloads below `parallel_threshold` use one thread; larger payloads use up to
one thread per `min_payload_per_thread`, capped by `num_threads`. The value
`num_threads=-1` means all processors available to the current process.

MolSysMT caches Rayon pools by size. A per-call override therefore neither
rebuilds a kernel nor resizes an irreversible global pool, and nested public
calls inherit the outer override. Passing `parallel=False` together with a
local `num_threads` value other than `1` is an argument conflict.

Parallel kernels distribute independent outer slabs or work blocks. Their
inner numerical loops remain sequential, contiguous where the data contract
allows it, and suitable for LLVM auto-vectorization. Parallelism is not a
replacement for vectorization; both must be measured in release builds.

Per-function thread-policy overrides use a `ContextVar` and do not mutate the
session. `molsysmt.configure.context()` still mutates module-level session
configuration. It restores values for ordinary nested, single-threaded use,
but overlapping session contexts are **not thread-safe**. Do not overlap them
across threads until the defect in
`pending_bugs/configure_context_is_not_thread_safe.md` is resolved.

When using xdist, multiprocessing, or another threaded host, set a conservative
session or per-call limit to prevent each process from claiming all available
processors.

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

MolSysMT 1.0 has no supported GPU kernel backend. Compatibility arguments fall
back to the Rust CPU path; an explicit GPU request emits a warning. Future Rust
GPU work is tracked separately. Chunked trajectory processing is described in
`SCALABILITY.md`.

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
