# Proposal: Exploring an AOT Rust Backend to Replace Numba Kernels

**Status:** early exploration; implementation status and adoption sequence
superseded by the 2026-07-26 Rust-only 1.0 decision
**Primary objective:** reduce and eventually eliminate runtime JIT compilation and `molsysmt.warmup()`
**Non-objective:** rewrite MolSysMT or its public API in Rust

> This document preserves the original decision framework. Its environment
> inventory, prototype status, progressive fallback, and lifecycle timing are
> historical. All recorded CPU kernels are now ported. Use
> [`rust_numba_coexistence_and_cut_plan.md`](../archive/resolved_proposals/rust_numba_coexistence_and_cut_plan.md)
> for migration evidence and
> [`release_1_0_execution_plan.md`](release_1_0_execution_plan.md) for current
> execution order.

## Decision context

MolSysMT uses Numba for a substantial collection of numerical kernels. The
repository currently contains 107 `lazy_njit` or direct `numba.njit` decorator
sites across 37 files under `molsysmt/lib`. Numba is a hard runtime dependency,
and the lazy registry compiles kernels on first use or through
`molsysmt.warmup()`.

Ahead-of-time compiled Rust extensions could remove first-call compilation for
migrated kernels and improve deployment on read-only or shared systems. This is
a hypothesis until numerical behavior, warm and cold performance, packaging,
and maintenance cost are measured.

The current development environment does not have `cargo`, `rustc`, or
`maturin` installed. The package uses `setuptools.build_meta`; introducing a
Rust extension therefore requires an explicit toolchain and packaging decision
before a prototype can be built.

## Desired end state

Python remains the public API, orchestration, form, unit, digestion, and
diagnostic layer. Rust is considered only for stable, coarse-grained numerical
kernels with a narrow NumPy boundary.

The migration succeeds only if it can eventually provide:

- no JIT latency for migrated CPU kernels;
- no mandatory warmup for ordinary MolSysMT workflows;
- numerical and scientific equivalence with the maintained implementation;
- binary packages for Python 3.11, 3.12, and 3.13 on supported platforms;
- predictable behavior when a binary is unavailable;
- a measurable maintenance benefit, not only a microbenchmark speedup.

Removing the `warmup()` function and the Numba dependency are separate gates.
MolSysMT may stop needing warmup before every Numba use, including CUDA paths,
has been replaced or retired.

## Architecture boundary

The Python wrapper must:

1. digest and normalize public inputs;
2. use PyUnitWizard to convert quantities to canonical nm, ps, radians, or other
   explicitly documented units;
3. validate dtype, shape, writability, and contiguity;
4. copy only when the Rust contract requires a contiguous buffer;
5. invoke one coarse-grained native operation;
6. translate native failures into the existing exception and diagnostic
   catalog;
7. attach units and preserve the existing public return contract.

Rust must receive numeric arrays and scalar metadata, not Python quantity,
Topology, or form objects. Rust code must not access Python objects while the
GIL is released.

## Phase 0: inventory and baseline

Before creating a crate, produce a machine-readable kernel inventory containing:

- Python module and callable;
- signatures and dtypes;
- callers and public workflows;
- whether it compiles lazily or at import time;
- parallel, fastmath, PBC, and CUDA behavior;
- existing unit, parity, and scientific-oracle tests;
- first-call compilation time, warm execution time, and cache behavior.

Measure these scenarios independently:

- clean environment with no Numba cache;
- populated Numba cache;
- `warmup()` cost and number of registered factories;
- first representative public call;
- repeated steady-state calls;
- import time and memory before and after loading `molsysmt.lib`.

This baseline determines whether eliminating warmup is a meaningful user-facing
gain and identifies the kernels responsible for most compilation latency.

## Phase 1: one leaf-kernel prototype

Select a stable CPU kernel that has:

- a small, explicit NumPy contract;
- deterministic reference tests;
- enough work per call to measure the Python/Rust boundary;
- no dependency on mutable Python objects;
- representative dtype and shape validation.

The pilot should compare three implementations where practical:

1. current Numba cold and warm paths;
2. a NumPy reference used as a readability and correctness oracle;
3. an AOT Rust implementation exposed through PyO3 and built with Maturin.

The pilot must not alter the default backend. It is an isolated benchmark and
compatibility experiment.

## Phase 2: representative scientific kernel

Only after the leaf seam is validated, prototype one operation that exercises
important MolSysMT behavior, such as batched distances or a PBC/MIC kernel.
Cover:

- empty and singleton inputs;
- multiple structures;
- C-contiguous, Fortran-contiguous, and strided arrays;
- `float32` and `float64` policy;
- orthogonal and triclinic boxes where applicable;
- invalid shapes, NaN/Inf policy, and index bounds;
- deterministic thread-count behavior;
- canonical units at the Python boundary.

Use existing public API parity tests plus an independent analytical or
reference oracle. Rust-versus-Numba agreement alone is not scientific
validation.

## Performance decision gates

Record distributions rather than single timings. At minimum report median,
dispersion, warm-up policy, hardware, compiler flags, dependency versions, and
commit.

Adopt a Rust path only if:

- cold-call latency improves materially;
- warm execution is not meaningfully slower in representative workloads;
- boundary conversion and copying do not erase the gain;
- peak memory is no worse without a documented reason;
- parallel execution scales without oversubscribing NumPy/OpenMP/Numba thread
  pools;
- small inputs do not suffer an unacceptable boundary penalty.

Exact thresholds must be chosen from the phase-0 baseline rather than invented
in advance.

## Packaging decision gates

The prototype must prove builds and imports for Python 3.11-3.13. Before making
the extension mandatory, CI and release workflows must cover the supported
Linux, macOS, and Windows architectures and the Conda distribution path.

The project must explicitly choose one deployment model:

- required native core with wheels and source-build instructions;
- optional Rust accelerator with the current implementation as fallback; or
- separate accelerator package.

Silent fallback is forbidden. Backend selection must be introspectable and
diagnostic. Source installations without a Rust toolchain must have a defined
outcome.

## Progressive migration

If both prototypes pass their gates:

1. add an internal backend seam without changing public signatures;
2. migrate kernels by coherent families, not file-by-file translation;
3. run the complete affected public tests under both backends;
4. retain Numba only as long as it has an explicit fallback or CUDA role;
5. shrink the warmup registry as families move to AOT;
6. make `warmup()` a no-op compatibility function only when no normal workflow
   requires JIT compilation;
7. deprecate and remove warmup in a later lifecycle-complete change;
8. remove Numba as a hard dependency only when CPU and GPU usage inventories
   reach zero or the remaining features become explicit optional dependencies.

Each migration must include benchmarks, numerical parity, scientific checks,
Ruff/Python tests, Rust formatting and linting, and wheel smoke tests.

## Risks

- binary distribution can cost more than the kernels save;
- Rust and Python implementations can drift scientifically;
- implicit array copies can hide at the binding boundary;
- `fastmath` differences can change numerical behavior;
- native parallelism can oversubscribe existing thread pools;
- supporting two backends can increase maintenance during migration;
- Numba CUDA usage prevents declaring Numba fully removed until GPU policy is
  addressed.

## Stop conditions

Stop or postpone the migration if the prototype shows negligible cold-start
benefit, repeated-call regression, fragile packaging on supported Python
versions, unclear scientific equivalence, or a maintenance burden larger than
the measured user benefit.

## Relationship to other proposals

This proposal concerns numerical AOT kernels and the future of Numba/warmup. It
does not choose a topology storage engine and does not require DuckDB, Polars,
or a Rust rewrite of selections. Direct Pandas hierarchy gathering remains the
near-term selection optimization.
