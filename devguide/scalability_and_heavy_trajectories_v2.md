# Scalability and Heavy Trajectory Processing Strategy v2
## A Pre-1.0 Working Design for Out-of-Core Analysis in MolSysMT

## 1. Purpose

This document defines a realistic and executable path for heavy-trajectory processing in MolSysMT before `1.0.0`.

The current repository already identifies memory scalability as a strategic weakness. That diagnosis is correct. MolSysMT still assumes, in many workflows, that trajectory-sized coordinate arrays can be loaded eagerly into RAM. That assumption breaks for large simulations and excludes a relevant class of scientific workloads.

However, the previous version of this document mixed:
- a justified strategic ambition,
- a long-term vision,
- and several advanced features that are not required to establish a credible `1.0.0` path.

This `v2` document narrows the design to a minimum viable heavy-analysis architecture that:
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
- mandatory SMonitor telemetry for heavy-mode decisions and progress;
- parity tests that compare eager and heavy results for supported operations;
- explicit diagnostics for unsupported heavy-mode combinations.

This is the minimum serious slice.

### 3.2 Explicitly out of scope for 1.0.0

The following are valuable, but they should not be treated as `1.0.0` commitments:

- cloud and remote streaming;
- `fsspec`-based byte-range access;
- GPU offloading;
- full checkpoint/resume;
- adaptive throttling based on live system load;
- multi-analysis read-once orchestration;
- real-time dashboards beyond basic telemetry;
- automatic spill-to-disk lazy result handles for every operation;
- enterprise-style scheduling or workflow orchestration.

These remain valid roadmap items, but they should be documented as `1.x` or later work.

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

The long-term heavy-analysis architecture should avoid rereading the same trajectory data for multiple compatible analyses when one pass through disk or network storage would be sufficient. This is one of the strongest practical reasons to invest in a heavy-processing architecture at all: for large workloads, I/O cost dominates quickly. I/O efficiency should therefore be treated as a first-class architectural constraint, not as a secondary optimization.

This principle is not a `1.0.0` feature commitment. It is a design constraint that should guide the internal architecture so that post-`1.0.0` multitask orchestration remains possible without redesigning the execution model.

### 4.7 Location-agnostic future design
The first committed slice focuses on local chunked processing. However, the heavy-processing architecture should not be designed in a way that makes future remote or cloud-backed execution unnatural.

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

This section describes exactly what MolSysMT should do in the `1.0.0` line.

### 6.1 Pre-flight footprint calculation

Before loading a large trajectory eagerly, MolSysMT should estimate whether eager execution is acceptable.

At minimum, the estimate should consider:
- number of atoms,
- number of structures,
- coordinate dimensionality,
- numeric dtype size,
- a safety margin.

The estimate does not need to be perfect. It needs to be conservative enough to avoid obvious memory failures.

### 6.2 Decision policy

The library should have an explicit policy such as:

- if estimated eager footprint is below `molsysmt.config.max_ram_usage`:
  - use eager path;
- otherwise:
  - if the operation and form support heavy mode, use heavy path;
  - if not, fail with an explicit diagnostic.

This is preferable to silent behavior because the user can understand and override policy when necessary.

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

## 7. Core Data Model for Heavy Processing

The previous version assumed a heavy engine but did not define the core data model strongly enough. That is a gap.

For `1.0.0`, the heavy path needs a minimal and explicit data model.

### 7.1 Minimal chunk payload

A chunk should expose at least:
- `coordinates`
- optional `box`
- optional `time`
- `structure_indices`

This is enough for many frame-local analyses.

### 7.2 Separation of orchestration and analysis

The heavy engine should not own scientific logic.
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

This separation is essential. Otherwise the heavy engine becomes a second analysis library, which is not the goal.

### 7.3 Iterator contract

A chunk-capable source should provide a stable iteration contract. The exact object may evolve later, but pre-`1.0.0` the design should already assume that heavy processing relies on a predictable chunk iterator abstraction rather than ad hoc loops per operation.

## 8. Reducer Protocol

This is one of the most important missing pieces in the previous version.

If heavy processing is to be credible, MolSysMT must define what a reducer is.

A minimal reducer protocol for the first slice should look like this:

- `initialize(metadata)`
- `consume(chunk)`
- `finalize()`

Optional later extensions:
- `merge(other)` for parallel reduction;
- `checkpoint()`;
- `restore(state)`.

For `1.0.0`, the minimal protocol is enough.

### Why this matters
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

A practical preferred strategy for ETA in the first slice is a lightweight dry-run over the first chunk. This does not need to be mandatory for every operation before `1.0.0`, but it is the most defensible way to estimate throughput and cost without inventing unsupported precision.

The guiding principle is simple: heavy mode must not feel like a silent black box.

## 11. Failure Policy

The previous manifesto correctly valued resilience, but did not distinguish failure classes clearly enough.

For `1.0.0`, the policy should be explicit.

### 10.1 Abort conditions
Abort immediately when:
- file header or structural metadata is unreadable;
- the operation requires global eager materialization and no heavy path exists;
- chunk iteration is impossible for the selected form;
- reducer logic fails in a non-recoverable way.

### 10.2 Recoverable conditions
Recover, warn, and continue only when:
- a frame is corrupt but the surrounding trajectory remains readable;
- a chunk can be skipped safely without invalidating the computation semantics.

This should be conservative. Recovery must never silently produce scientifically misleading results. When scientific validity can still be guaranteed, the preferred policy is to preserve run continuity instead of aborting an otherwise healthy long-running analysis because of a small number of damaged frames.

### 10.3 Diagnostics
Every recovery or abort path should have a structured diagnostic, not just a free-text warning.

## 12. Testing Strategy for the Heavy Slice

A pre-`1.0.0` heavy design is not credible without a concrete testing plan.

The testing strategy should include:

### 11.1 Unit tests
- footprint calculation;
- decision policy eager vs heavy;
- reducer protocol behavior;
- chunk boundary correctness.

### 11.2 Integration tests
- synthetic large trajectory fixtures;
- parity between eager and heavy for supported operations;
- telemetry contract tests.

### 11.3 Fault tests
- corrupt frame handling;
- unsupported form/operation combinations;
- budget-based aborts.

### 11.4 Determinism
The heavy path must be tested against deterministic synthetic or bundled trajectory sources. This avoids giant real trajectory fixtures while still validating chunk logic.

## 13. Configuration Contract

The original document listed a broad configuration set. For `1.0.0`, this should be narrowed.

Recommended minimal configuration:

- `max_ram_usage`
- `heavy_mode = auto | force | off`
- `chunk_size`
- `emit_heavy_telemetry`

Everything else should wait until the architecture is proven.

This keeps configuration understandable and reduces unstable surface area before `1.0.0`.

## 14. Tiered Roadmap

The original tiering was useful, but too broad. This version makes it operational.

### 13.1 Tier 1 - Pre-1.0 committed slice
- pre-flight footprint estimate;
- eager/heavy decision policy;
- sequential local chunking;
- reducer protocol;
- small set of supported heavy operations;
- basic SMonitor telemetry;
- eager/heavy parity tests.

### 14.2 Tier 2 - Early post-1.0
- multi-analysis read-once orchestration;
- local parallel reducers;
- checkpointing/resume;
- richer ETA, throughput, and memory-pressure telemetry;
- storage-aware preflight checks for heavy output workflows, which become mandatory before heavy output-producing workflows can be considered supported;
- lazy result handles for large-output workflows.

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

## 16. Open Questions That Must Be Resolved Before Implementation Starts

The following questions remain legitimate and should be answered explicitly before coding begins:

1. What exact iterator abstraction will MolSysMT standardize for chunk delivery?
2. Which public operations are officially in the first heavy-support slice?
3. Which trajectory forms are in scope for the first heavy-support slice?
4. Is a persistent result-handle abstraction needed before `1.0.0`, or can it wait?
5. Which SMonitor event codes should be reserved specifically for heavy-mode lifecycle events?

## 17. Summary

The correct pre-`1.0.0` goal is not to deliver a complete "HeavyAnalysisEngine" platform. If the project keeps using the name "HeavyAnalysisEngine" for the future orchestration layer, it should be understood as a post-`1.0.0` internal execution concept, not as a claim that the full platform already exists in the `1.0.0` line.

The correct goal is to deliver a disciplined Tier 1 heavy-processing slice that:
- makes memory decisions explicit,
- processes supported trajectories chunk-by-chunk,
- exposes progress and failure through structured diagnostics,
- and preserves the public API where support exists.

That is achievable, testable, and worthy of `1.0.0`.

Everything more ambitious should remain clearly marked as post-`1.0.0`.
