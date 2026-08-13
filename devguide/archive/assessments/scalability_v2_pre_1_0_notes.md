# Scalability and Heavy Trajectory Processing Strategy v2
## A Pre-1.0 Working Design for Out-of-Core Analysis in MolSysMT

> **Implementation status (updated 2026-03-19)**
>
> The Tier 1 committed slice described in this document is fully implemented and tested.
> Several Tier 2 features (multi-reducer, checkpoint/resume, parallel reduction via `merge()`,
> and `PersistentResultHandle` with disk-budget pre-flight check) were advanced ahead of the
> original schedule and are also implemented and tested.
>
> Sections 3.2, 8, 14, and 16 have been updated to reflect the current state.

## 1. Purpose

This document defines a realistic and executable path for heavy-trajectory processing in MolSysMT before `1.0.0`.

The current repository already identifies memory scalability as a strategic weakness. That diagnosis is correct. MolSysMT still assumes, in many workflows, that trajectory-sized coordinate arrays can be loaded eagerly into RAM. That assumption breaks for large simulations and excludes a relevant class of scientific workloads.

However, the previous version of this document mixed:
- a justified strategic ambition,
- a long-term vision,
- and several advanced features that are not required to establish a credible `1.0.0` path.

This `v2` document narrows the design to a minimum viable chunked-execution architecture that:
- is technically coherent,
- can be validated before `1.0.0`,
- does not overpromise enterprise-grade orchestration,
- and creates a solid base for later expansion.

The goal is not to solve all scalability problems before `1.0.0`.
The goal is to define exactly what MolSysMT should support in the `1.0.0` line, what it will explicitly not support yet, and how that support should be implemented and validated.

## 2. Why This Matters

MolSysMT is already a high-value library for:
- molecular-system representation,
- conversion between forms,
- structural analysis,
- and cross-ecosystem interoperability.

But for trajectories that exceed memory, the current eager-loading model becomes a hard limit.

This matters for three reasons:

### 2.1 Scientific reality
Modern trajectories can easily exceed tens or hundreds of gigabytes. A workstation with 32-64 GB of RAM is common. A library that only works comfortably when the whole trajectory fits in memory has a natural ceiling.

### 2.2 Product credibility
A `1.0.0` line should not imply that MolSysMT solves large-scale analysis completely, but it should demonstrate that the project has a coherent and explicit plan for workloads beyond eager in-memory operation.

### 2.3 Architectural alignment
A chunked, out-of-core path is not only about "big trajectories." It also forces clarity about:
- data ownership,
- iterator semantics,
- reducer interfaces,
- kernel contracts,
- and observability.

Those are healthy architectural constraints even for smaller workloads.

## 3. Scope Split: What Is In 1.0.0 and What Is Not

This section is the most important addition to the previous manifesto. It separates a realistic `1.0.0` commitment from post-`1.0.0` ambition.

### 3.1 Committed pre-1.0 / 1.0.0 slice

Before or at `1.0.0`, MolSysMT should provide:

- a pre-flight memory footprint estimate;
- a deterministic decision between eager and heavy processing;
- a sequential chunked processing path for supported local trajectory forms;
- a minimal reducer protocol for operations that can be accumulated safely;
- a minimal persistent result handle (for example, disk-backed NumPy memmap or HDF5-backed storage) to avoid memory crashes when delivering very large outputs;
- integration with the ValidatedPayload protocol so inner execution loops avoid redundant validation;
- mandatory SMonitor telemetry for heavy-mode decisions and progress;
- parity tests that compare eager and heavy results for supported operations;
- explicit diagnostics for unsupported heavy-mode combinations.

This is the minimum serious slice.

### 3.2 Explicitly out of scope for 1.0.0

The following are valuable, but they should not be treated as `1.0.0` commitments:

- cloud and remote streaming;
- `fsspec`-based byte-range access;
- GPU offloading;
- adaptive throttling based on live system load;
- real-time dashboards beyond basic telemetry;
- enterprise-style scheduling or workflow orchestration.

These remain valid roadmap items, but they should be documented as `1.x` or later work.

> **Note (2026-03-19):** `full checkpoint/resume` and `multi-analysis read-once orchestration`
> were originally on this list. Both have since been implemented as part of the
> `ChunkedExecutor` / `Reducer` architecture (see sections 8 and 14). They are no longer
> out of scope.

## 4. Core Design Principles

The previous document had good intuitions. This version keeps them, but makes them operational.

### 4.1 API continuity
If an operation supports heavy mode, the public function signature should remain the same. The user should not need a second API just because the dataset is large.

Heavy mode should be an execution strategy, not a separate user model.

### 4.2 Explicit support
Not every operation needs heavy support in `1.0.0`. It is better to support a small set well than a large set ambiguously.

### 4.3 Observable decisions
If MolSysMT chooses eager or heavy mode, that decision should be visible through structured telemetry. The user and the developer should be able to answer:
- why this path was chosen,
- what resource assumptions were made,
- and what the library is doing now.

### 4.4 Reducer-oriented design
Heavy processing should be driven by operations that can consume chunks and accumulate results safely. That means the architecture should privilege operations that naturally fit a reducer model.

### 4.5 No fake promises
If a form or operation cannot support chunked heavy processing yet, MolSysMT should say so clearly and fail explicitly. It should not silently fall back to broken behavior.

### 4.6 Read once, analyze many
Even though full multi-analysis orchestration is outside the `1.0.0` committed slice, MolSysMT should preserve this as a design principle.

The long-term chunked-execution architecture should avoid rereading the same trajectory data for multiple compatible analyses when one pass through disk or network storage would be sufficient. This is one of the strongest practical reasons to invest in a chunked-execution architecture at all: for large workloads, I/O cost dominates quickly. I/O efficiency should therefore be treated as a first-class architectural constraint, not as a secondary optimization.

This principle is not a `1.0.0` feature commitment. It is a design constraint that should guide the internal architecture so that post-`1.0.0` multitask orchestration remains possible without redesigning the execution model.

### 4.7 Location-agnostic future design
The first committed slice focuses on local chunked processing. However, the chunked-execution architecture should not be designed in a way that makes future remote or cloud-backed execution unnatural.

This does not mean remote streaming must be implemented before `1.0.0`. It means that the chunking model, reducer protocol, and telemetry contract should remain compatible with a future location-agnostic engine. The same principle applies to hardware empathy: the architecture should remain compatible with future resource-policy profiles ranging from workstation-friendly execution to throughput-oriented HPC execution, even if adaptive throttling itself is postponed beyond `1.0.0`.

## 5. Definitions

To keep implementation and discussion precise, the following terms are used in this document.

### 5.1 Eager path
The traditional in-memory execution path:
- all required coordinates are materialized in memory;
- analysis proceeds on full arrays.

### 5.2 Heavy path
The chunked out-of-core execution path:
- trajectory data is processed in pieces;
- chunks are passed to one or more reducers;
- full coordinate arrays are not required in RAM at once.

### 5.3 Footprint estimate
A pre-flight estimate of the memory required by eager execution.

A basic form is:

`estimated_bytes = n_atoms * n_structures * 3 * dtype_size`

This should include a safety margin.

### 5.4 Chunk
A contiguous subset of structures/frames with the same per-frame topology assumptions as the source trajectory.

### 5.5 Reducer
An object or protocol that:
- receives chunks,
- updates intermediate state,
- and produces a final result after all chunks are consumed.

### 5.6 Iterator form
A form or adapter capable of exposing trajectory data incrementally rather than only as full in-memory arrays.

## 6. The 1.0.0 Minimum Execution Contract

This section describes exactly what MolSysMT should do in the `1.0.0` line. Tier 1 must solve both the input memory wall and, in a minimal but explicit way, the output memory wall.

### 6.1 Pre-flight footprint calculation

Before loading a large trajectory eagerly, MolSysMT should estimate whether eager execution is acceptable.

At minimum, the estimate should consider:
- number of atoms,
- number of structures,
- coordinate dimensionality,
- numeric dtype size,
- a safety margin.

The estimate must apply a mandatory 20% safety margin over the raw coordinate-size calculation to account for Python overhead, metadata management, temporary array views, and executor-side bookkeeping.

The estimate does not need to be perfect. It needs to be conservative enough to avoid obvious memory failures.

### 6.2 Decision policy

The library should have an explicit policy such as:

- if estimated eager footprint is below `molsysmt.configure.max_ram_usage`:
  - use eager path;
- otherwise:
  - if the operation and form support heavy mode, use heavy path;
  - if not, fail with an explicit diagnostic.

This is preferable to silent behavior because the user can understand and override policy when necessary.

#### 6.2.1 Footprint-Aware Chunk Size Heuristics

To optimize performance and avoid excessive chunk loop overhead on intermediate-sized trajectories, `ChunkedExecutor` incorporates a dynamic footprint-aware chunk size optimization system:

1. **Parameters & Budgeting:**
   - **`molsysmt.configure.chunk_memory_fraction`** (default `0.10` / 10% of the total `max_ram_usage` budget) dictates the maximum memory footprint allowed per chunk.
   - **Memory footprint per frame** is estimated using the coordinate size: `n_atoms * 3 * 8 * 1.20` bytes.

2. **Optimal Chunk Size Heuristic:**
   - `optimal_chunk_size = (max_ram_usage * chunk_memory_fraction) // footprint_per_frame`

3. **Constraints and Safety:**
   - The executor scales up `chunk_size = max(advisory_chunk_size, optimal_chunk_size)` to amortize Python/IO latency.
   - The adjusted `chunk_size` is capped at the total number of selected structures to prevent over-allocation.
   - Users can disable this heuristic and force exactly the advisory chunk size by setting `molsysmt.configure.chunk_memory_fraction = 0.0`.
   - Telemetry events through SMonitor track `advisory_chunk_size` alongside the resulting `optimized_chunk_size`.

### 6.3 Supported heavy-mode operations in the first slice

The `1.0.0` slice should focus on operations that naturally fit chunk accumulation.

Candidate operations include:
- distances;
- centers;
- RMSD against a reference;
- possibly neighborhood-based or frame-local metrics that do not need global covariance-like state.

Operations that require whole-trajectory global state should not be forced into the first slice unless their reducer logic is already clear and stable.

### 6.4 Supported heavy-mode inputs in the first slice

The first slice should focus on local file-backed trajectory sources for which chunk access is realistic and already conceptually aligned with MolSysMT forms.

The exact list can remain modest. The key point is to support a small set of real cases well.

### 6.5 Explicit failure for unsupported combinations

If the user requests an operation on a form that cannot provide chunked access and the eager footprint exceeds the configured budget, MolSysMT should fail with an actionable diagnostic.

That diagnostic should explain:
- the estimated footprint,
- the configured threshold,
- whether the form lacks heavy support,
- and what the user can do next.

### 6.6 Minimal output strategy

Tier 1 must also address the output wall. Solving input streaming alone is insufficient if the final analysis result still needs to be materialized eagerly into RAM and can therefore fail at delivery time.

For this reason, the ChunkedExecutor must support a fallback output mode. When the predicted size of the final result exceeds a safety threshold, the executor must be able to return a `PersistentResultHandle` instead of a fully materialized in-memory array.

This handle may initially point to a simple disk-backed implementation such as:
- a temporary `.npy` file exposed through NumPy memmap, or
- an HDF5-backed result store.

Tier 1 does not require a rich persistent-result ecosystem. It does require a minimal and explicit mechanism that prevents heavy-mode success on input from turning into output-stage memory failure.

The Tier 1 lifecycle contract should remain simple: handles are temporary by default, must expose a path or equivalent retrieval mechanism, and must document whether cleanup is automatic or caller-controlled.

Because Tier 1 already allows disk-backed output delivery, storage-aware preflight checks also belong in Tier 1. The executor must estimate whether the predicted persistent output can fit in the target storage budget and must fail early when the result would clearly exhaust available disk space. A storage kill switch is therefore a Tier 1 safety feature, not only a Tier 2 convenience feature.

## 7. Core Data Model for Heavy Processing

The previous version assumed a chunked executor but did not define the core data model strongly enough. That is a gap.

For `1.0.0`, the heavy path needs a minimal and explicit data model.

### 7.1 Minimal chunk payload

A chunk should expose at least:
- `coordinates`
- optional `box`
- optional `time`
- `structure_indices`

Every chunk payload delivered to inner kernels must be wrapped in a `ValidatedPayload`. This is part of the inner-loop contract: once chunk boundaries have established trusted shape, dtype, and unit semantics, the executor should not re-enter redundant digestion or validation layers for every chunk operation.

This is enough for many frame-local analyses.

### 7.2 Separation of orchestration and analysis

The chunked executor should not own scientific logic.
Its responsibility should be:
- iterating chunks,
- respecting memory policy,
- emitting telemetry,
- calling reducer methods,
- finalizing results.

Scientific logic should remain in:
- existing kernels,
- analysis wrappers,
- and reducer implementations.

This separation is essential. Otherwise the chunked executor becomes a second analysis library, which is not the goal.

### 7.3 Iterator contract

A chunk-capable source should provide a stable iteration contract. The exact object may evolve later, but pre-`1.0.0` the design should already assume that heavy processing relies on a predictable chunk iterator abstraction rather than ad hoc loops per operation.

That iterator contract should support source-level atom selection and stride-aware extraction whenever the underlying form can provide it. The design goal is to avoid reading broad coordinate payloads only to discard most of them in RAM. In heavy workflows, selection should happen as close to the source as possible.

## 8. Reducer Protocol

The `Reducer` ABC (`molsysmt._private.execution.reducer.Reducer`) defines the full protocol for chunked analysis. It is implemented and tested.

### 8.1 Mandatory lifecycle (three abstract methods)

```
reducer.initialize(metadata)     # called once before the chunk loop
reducer.consume(chunk)           # called once per chunk (read-only chunk)
result = reducer.finalize()      # called once after all chunks
```

### 8.2 Optional extensions (four concrete methods with defaults)

These override the base-class no-ops / NotImplementedError defaults to enable specific features:

| Method | Purpose | Default |
|---|---|---|
| `estimate_output_shape(metadata)` | Return output array shape so executor can pre-allocate a `PersistentResultHandle` instead of in-RAM accumulation. Return `None` to always use RAM. | `None` |
| `checkpoint()` | Return a serializable state dict for checkpoint/resume. Return `None` if not supported. | `None` |
| `restore(state)` | Restore accumulated state from a checkpoint dict. | `NotImplementedError` |
| `merge(other)` | Merge another reducer's partial state into self (earlier frames first). Used for parallel reduction. | `NotImplementedError` |

### 8.3 Chunk contract

Every chunk dict delivered to `consume()` contains:
- `'coordinates'`: `np.ndarray`, float64, nm, shape `(n_chunk, n_atoms, 3)`, **read-only**
- `'box'`: `np.ndarray`, float64, nm, shape `(n_chunk, 3, 3)` or `None`
- `'time'`: `np.ndarray`, float64, ps, shape `(n_chunk,)` or `None`
- `'structure_indices'`: `np.ndarray`, int, global frame indices

Chunks are read-only views. Reducers must copy before mutating.

### 8.4 Why this matters
Without a reducer contract:
- every heavy-enabled operation will invent its own ad hoc accumulation model;
- behavior becomes inconsistent;
- testing becomes harder;
- parallel or resumable execution becomes harder later.

The reducer protocol is the interface that keeps heavy-mode implementations disciplined.

## 9. Developer Contract for Heavy-Compatible Operations

Heavy-compatible analysis code must follow a stricter internal contract than ordinary eager-only workflows.

### 9.1 Stateless analysis functions
Chunk-level analysis functions should be stateless with respect to the full trajectory. They must operate only on the chunk they receive and on explicit metadata passed to them.

Persistent cross-chunk state belongs in reducers, not in ad hoc hidden global or closure state.

### 9.2 Reducer-owned accumulation
If an analysis needs accumulation across chunks, that accumulation must live in a reducer object with explicit lifecycle methods. This keeps heavy-mode logic testable, composable, and future-proof for parallel reduction.

### 9.3 Low-copy discipline
Heavy-mode boundaries should avoid unnecessary copies. Chunk payloads should be treated as views or minimally copied arrays whenever the underlying form permits it.

This is important because memory scalability is not only about peak RAM usage. It is also about avoiding avoidable allocation churn and hidden duplication across chunk transitions.

## 10. SMonitor Contract for Heavy Mode

The following event range is reserved for Tier 1 heavy-mode diagnostics. The range may be extended later for Tier 2 and Tier 3 execution features:
- `MSM-INFO-HVY-001`: heavy path selected;
- `MSM-INFO-HVY-002`: eager path accepted after estimate;
- `MSM-WARN-HVY-001`: slow chunk I/O detected;
- `MSM-WARN-HVY-002`: corrupt frame detected and skipped;
- `MSM-ERROR-HVY-001`: unsupported heavy-mode combination;
- `MSM-ERROR-HVY-002`: output persistence failure.


The previous version mentioned observability, but not precisely enough.

For `1.0.0`, heavy mode should emit a minimum set of structured events.

### 10.1 Mandatory decision events
At minimum:
- eager path accepted;
- eager path rejected due to footprint;
- heavy path activated;
- unsupported heavy combination rejected.

### 10.2 Mandatory progress events
At minimum:
- chunk progress;
- estimated total chunks;
- current chunk index;
- dynamic ETA if available.

### 10.3 Mandatory failure and degradation events
At minimum:
- frame skipped;
- chunk failed;
- analysis aborted due to insufficient support;
- analysis aborted due to footprint/budget conflict.

### 10.4 Required payload fields
Heavy-mode telemetry should include, where relevant:
- `operation`
- `resource`
- `form`
- `footprint_bytes`
- `max_ram_usage`
- `chunk_index`
- `n_chunks`
- `eta_s`

This makes the system useful to:
- users,
- developers,
- QA,
- and agents.

### 10.5 User-facing cost transparency
Heavy mode should communicate cost clearly enough that users understand what is happening before and during long-running analysis.

For the `1.0.0` slice, this does not require a rich dashboard or interactive prompt. It does require that:
- heavy/eager decisions are visible;
- progress is visible;
- ETA is exposed when it can be estimated responsibly.

The ChunkedExecutor must perform a lightweight dry-run on the first chunk whenever feasible for supported chunk-capable operations. This first-pass estimate should be used to emit a baseline ETA through SMonitor. The goal is not perfect prediction; the goal is to protect the user from launching blind multi-hour jobs without an initial throughput estimate.

The guiding principle is simple: heavy mode must not feel like a silent black box.

## 11. Failure Policy

The previous manifesto correctly valued resilience, but did not distinguish failure classes clearly enough.

For `1.0.0`, the policy should be explicit.

### 11.1 Abort conditions
Abort immediately when:
- file header or structural metadata is unreadable;
- the operation requires global eager materialization and no heavy path exists;
- chunk iteration is impossible for the selected form;
- reducer logic fails in a non-recoverable way.

### 11.2 Recoverable conditions
Recover, warn, and continue only when:
- a frame is corrupt but the surrounding trajectory remains readable;
- a chunk can be skipped safely without invalidating the computation semantics.

This should be conservative. Recovery must never silently produce scientifically misleading results. Frames should only be skipped when the scientific meaning of the final result remains valid. When that condition holds, the preferred policy is to preserve run continuity instead of aborting an otherwise healthy long-running analysis because of a small number of damaged frames.

### 11.3 Diagnostics
Every recovery or abort path should have a structured diagnostic, not just a free-text warning.

## 12. Testing Strategy for the Heavy Slice

A pre-`1.0.0` heavy design is not credible without a concrete testing plan.

The testing strategy should include:

### 12.1 Unit tests
- footprint calculation;
- decision policy eager vs heavy;
- reducer protocol behavior;
- chunk boundary correctness.

### 12.2 Integration tests
- synthetic large trajectory fixtures;
- parity between eager and heavy for supported operations;
- telemetry contract tests.

### 12.3 Fault tests
- corrupt frame handling;
- unsupported form/operation combinations;
- budget-based aborts.

### 12.4 Determinism
The heavy path must be tested against deterministic synthetic or bundled trajectory sources. This avoids giant real trajectory fixtures while still validating chunk logic.

## 13. Configuration Contract

The original document listed a broad configuration set. For `1.0.0`, this should be narrowed.

Recommended minimal configuration:

- `max_ram_usage`
- `heavy_mode = auto | force | off`
- `chunk_size`
- `emit_heavy_telemetry`

`chunk_size` should be treated as an advisory configuration value. Different forms or iterator backends may need to adjust the effective chunking strategy in order to preserve correctness or exploit natural storage boundaries.

Everything else should wait until the architecture is proven.

This keeps configuration understandable and reduces unstable surface area before `1.0.0`.

## 14. Tiered Roadmap

### 14.1 Tier 1 - Pre-1.0 committed slice ✅ DONE

- pre-flight footprint estimate (`estimate_footprint`, `decide_mode`);
- eager/heavy decision policy (`heavy_mode = auto | force | off`);
- sequential local chunking (`ChunkedExecutor` + form `StructuresIterator`);
- `_heavy_support` dict per form module for attribute-level validation;
- `Reducer` ABC with mandatory lifecycle (initialize / consume / finalize);
- `PersistentResultHandle` (disk-backed memmap for large outputs);
- `check_disk_budget` pre-flight storage check;
- SMonitor telemetry: HeavyPathSelected, EagerPathAccepted, ChunkProcessed (ETA), SlowChunkIOWarning, CorruptFrameSkippedWarning, UnsupportedHeavyOperationError, HeavyOutputFailureError;
- heavy support in `get_center`, `get_rmsd`, `get_distances`;
- heavy support in `file:h5msm` and `molsysmt.H5MSMFileHandler` forms;
- `heavy_mode` argument digested by argdigest;
- eager/heavy parity tests for all three operations.

### 14.2 Tier 2 - Early post-1.0 ✅ FULLY DONE (all advanced ahead of schedule)

- **multi-reducer** (`ChunkedExecutor(reducers=[...])`) — single pass, multiple analyses;
- **checkpoint / resume** (`checkpoint_interval`, `checkpoint_path`, `restore_from` on `ChunkedExecutor`; `checkpoint()` / `restore()` on `Reducer`);
- **parallel reduction via merge** (`Reducer.merge(other)` protocol — split segments independently, merge in order);
- **`estimate_output_shape`** on `Reducer` — triggers `PersistentResultHandle` allocation when output exceeds RAM budget;
- `_DistancesReducer.estimate_output_shape` writes directly into the handle per chunk;
- **richer adaptive ETA** — exponential moving average (`_EMA_ALPHA=0.3`) updated per chunk; emitted in `ChunkProcessed` telemetry as `eta_s`;
- **memory-pressure telemetry** — RSS monitored via `psutil` each chunk; `MemoryPressureWarning` emitted when RSS exceeds `config.memory_pressure_threshold` (default 0.80); graceful fallback when psutil not installed;
- **richer `PersistentResultHandle` lifecycle** — `output_path` parameter on `ChunkedExecutor` and `path` parameter on `PersistentResultHandle`; user-specified files are not deleted on `cleanup()`, giving callers full lifecycle control; parent directories created automatically.

All three items previously marked "still pending" are confirmed implemented and tested (March 2026).

### 14.3 Tier 3 - Advanced / enterprise-like features
- cloud streaming;
- remote byte-range access;
- adaptive throttling;
- GPU offloading;
- richer dashboards and workflow orchestration.

## 15. Relationship with the 1.0.0 Support Contract

This must be stated directly.

The heavy-trajectory architecture is part of the strategic path to excellence, but only the Tier 1 slice belongs in the `1.0.0` support contract.

Everything else should be treated as future work, even if design language already exists for it.

This is important because otherwise:
- the roadmap becomes impossible to fulfill,
- the support contract becomes ambiguous,
- and documentation overpromises.

## 16. Open Questions — Resolved

These questions were open when this document was written. They are now answered.

1. **What exact iterator abstraction will MolSysMT standardize for chunk delivery?**
   Each form module exposes a `StructuresIterator` class. `ChunkedExecutor` uses the form's
   iterator directly (bypassing the public `msm.Iterator` API) via `_dict_modules[form].StructuresIterator(...)`.
   The iterator is used as a context manager (`with ... as it: for raw_chunk in it:`).

2. **Which public operations are officially in the first heavy-support slice?**
   `get_center`, `get_rmsd`, `get_distances` (all in `molsysmt/structure/`).

3. **Which trajectory forms are in scope for the first heavy-support slice?**
   `file:h5msm` and `molsysmt.H5MSMFileHandler`. Both declare `_heavy_support = {'coordinates': True, 'box': True}`.

4. **What is the minimum lifecycle contract for Tier 1 `PersistentResultHandle` objects?**
   Temporary by default (backing file in `tempfile.gettempdir()`). Exposes `__getitem__`/`__setitem__`
   (array-like), `to_memory()`, `flush()`, `cleanup()`, and context-manager protocol. Cleanup is
   caller-controlled (or automatic if used as a context manager).

5. **Which additional SMonitor event codes should be reserved beyond the Tier 1 heavy-mode baseline?**
   See section 10. The range `MSM-INFO-HVY-001..003` and `MSM-WARN-HVY-001..002` and
   `MSM-ERROR-HVY-001..002` are defined and registered in `catalog.py`.
   `MSM-INFO-HVY-003` = `ChunkProcessed` (progress telemetry with ETA).

## 17. Summary

The correct pre-`1.0.0` goal is not to deliver a complete chunked-execution platform. If the project keeps using the name "ChunkedExecutor" for the future orchestration layer, it should be understood as a post-`1.0.0` internal execution concept, not as a claim that the full platform already exists in the `1.0.0` line.

The correct goal is to deliver a disciplined Tier 1 heavy-processing slice that:
- makes memory decisions explicit,
- processes supported trajectories chunk-by-chunk,
- exposes progress and failure through structured diagnostics,
- and preserves the public API where support exists.

That is achievable, testable, and worthy of `1.0.0`.

Everything more ambitious should remain clearly marked as post-`1.0.0`.

## Correction — 2026-08-13

Any passport requirement described above was a proposal, not an implemented runtime
contract. The evaluated `ValidatedPayload` mechanism had no live consumer and was
withdrawn rather than replaced under uibcdf/molsysmt#153. Current performance work may
use explicit `skip_digestion=True` delegation only after the complete callee contract
has already been established.
