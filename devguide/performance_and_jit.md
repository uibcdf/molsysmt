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

Validation may be bypassed internally only when the caller can prove that every
value already satisfies the callee's contract. `skip_digestion=True` is an
explicit whole-call trusted path, not a general performance switch. MolSysMT
has no value-passport protocol. Never apply the bypass to unvalidated user
input.

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

`molsysmt.configure.precision` defaults to `"double"`. Native coordinate
preparation and the canonical chunk contract use `float64`, as required by the
bundled CPU kernels. A `"single"` request emits `MSM-WARN-PRECISION-001` when
those preparation/execution paths consume it. The diagnostic identifies the
requested and effective arithmetic; it is not evidence for a float32 CPU backend.
Canonical float64 coordinate payloads do not acquire an extra dtype copy.

Working precision and coordinate publication are separate. `least_rmsd_fit`
and its alignment consumer retain their supported final single-coordinate
quantization. A quantity output may carry float32 magnitudes; native containers
store the quantized values under their float64 storage invariant. This does not
reduce native-container RAM by half. Float32 input values cannot regain bits
already lost in their source representation. File/export precision is a separate
format contract. Other engines retain their own documented arithmetic behavior;
no package-wide dtype promise is made for third-party objects or outputs.

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
configuration, and MolSysMT configuration is deliberately **process-global** for
1.0. Context writers are serialized for their full lifetime with a reentrant
lock, so overlapping contexts cannot corrupt each other's snapshot or
restoration, and nested contexts in one thread remain supported. This is
serialization, not isolation: code running concurrently *outside* a context can
still observe its temporary values, and direct module assignments do not take
the lock. Public session setters participate in writer serialization. The
complete configuration key/alias declaration is checked before any change;
private, callable and module names are not settings. A synchronous context must
not span awaits in overlapping asynchronous tasks. The diagnosis and the
rejected `contextvars` alternative are recorded
in
[`archive/resolved_bugs/configure_context_is_not_thread_safe.md`](archive/resolved_bugs/configure_context_is_not_thread_safe.md).

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
