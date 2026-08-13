# Performance and JIT

> **Status (updated 2026-03-23)**
>
> This document reflects the architecture as implemented for `1.0.0`.
> The three-layer kernel boundary model, `ValidatedPayload` trusted-path
> protocol, and float64 normalization policy are all in place and adopted
> across the main Tier 1 hot paths.
> The heavy-trajectory `ChunkedExecutor` / `Reducer` architecture is also
> fully implemented and follows the same boundary discipline — see
> `SCALABILITY.md`.

## Import Strategy (Lightweight Startup)
`import molsysmt` must remain fast. Performance-heavy kernels are loaded and
compiled lazily. Avoid importing heavy modules or soft dependencies at module
level.

The current performance model relies on a strict split:

- public APIs remain import-light and user-oriented;
- numeric kernels live in `molsysmt/lib`;
- compilation happens on first use, not on import.

This is not a micro-optimization. It is a library-level requirement. MolSysMT
is large enough that eager JIT compilation or heavy top-level imports would make
startup costs unacceptable and would also make troubleshooting of optional
runtime environments much harder.

## Numba Policy
Numba kernels live in `molsysmt/lib`. Use the `lazy_njit` helper for all JIT
functions so compilation happens on first use and is tracked consistently.

### Rules
- Do not use `@nb.njit` directly in library modules.
- Use `lazy_njit(signature, cache=True)` from `molsysmt._private.jit`.
- Avoid heavy global initialization in `molsysmt/lib` modules.
- Nested kernels must resolve against compiled dispatchers, not Python wrappers.
- Public wrappers must normalize numeric inputs before crossing the JIT boundary.

### Current JIT observability
`lazy_njit(...)` now emits a structured one-time warning through SMonitor when a
kernel compiles on a cold cache. The warning is not meant to blame the user; it
exists so that developers, QA, and power users can distinguish first-use JIT
latency from steady-state performance.

Relevant payload fields include:
- `kernel`
- `module`
- `cache_state`
- `operation='jit_compile'`

## Current Kernel Boundary Model
During the March 2026 performance hardening pass, MolSysMT converged on a more
explicit kernel-boundary model.

The current architecture distinguishes three layers:

1. **Public wrapper layer**
   - user-facing functions in `molsysmt.structure`, `molsysmt.pbc`, and related
     modules;
   - responsible for public semantics, units, output shape, and diagnostics.

2. **Trusted preparation layer**
   - helper logic that converts validated public inputs into raw numeric arrays
     suitable for kernels;
   - currently centered around `molsysmt.lib.structure._kernel_inputs` and
     caller-aware digestion helpers.

3. **Numeric kernel layer**
   - Numba kernels in `molsysmt/lib`;
   - unit-agnostic and designed to receive already-prepared numeric arrays.

This split is now intentional and should be preserved.

## Scope Within the 1.0.0 Support Contract
This document describes the current performance and JIT architecture of the
Tier 1 core execution path. It is not a blanket performance promise for every
form or every public operation in MolSysMT.

The support contract for forms and capabilities is defined in:
- `devguide/support_tiers.ipynb`
- `devguide/testing_strategy.md`

This document should be read as the performance source of truth for:
- the native/core path;
- trusted structural and PBC execution paths;
- the current JIT boundary discipline used by Tier 1 analysis wrappers.

## Trusted Path and Validated Payloads
One of the most important changes in the current architecture is the emergence
of a trusted path for hot numeric workflows.

The key idea is simple:

- expensive validation and digestion should happen at the public boundary;
- once an internal execution path has already established shape, dtype, and unit
  correctness, the inner loop must not pay that cost again.

### Coordinates digestion and the passport model
`molsysmt._private.argdigest.argument.coordinates.digest_coordinates(...)`
now recognizes trusted internal callers and can issue a `ValidatedPayload`
passport for structural kernel paths.

This means that, for trusted structural execution paths:

- coordinates have already been validated structurally;
- dtype has already been normalized;
- unit semantics are already known;
- the inner loop can avoid redundant validation passes.

This is important for two reasons:

1. it removes avoidable overhead in hot loops;
2. it gives a clear architectural answer to the question “where should
   scientific validation stop and numeric execution begin?”

### Current trusted-path policy
At the moment, the trusted path is conservative.
It is not a global bypass. It is only granted for internal high-frequency paths
where the upstream preparation is known and controlled.

That is the correct posture for `1.0.0`: trusted execution should be explicit,
limited, and auditable.

The same principle extends directly to the heavy-trajectory architecture, which
is described in `SCALABILITY.md`. Implementation status must be confirmed by the
heavy-execution test suite. The
`ValidatedPayload` passport is not a structure-only trick: chunk payloads
delivered by `ChunkedExecutor` or the public `msm.Iterator` to the analysis kernels
already follow the same trusted-boundary contract. Shape, dtype, and unit semantics
are established once at the chunk boundary, and inner execution loops do not re-enter
digestion or validation for each frame of the chunk.

### `skip_digestion=True` for internal callers

All public MolSysMT functions that are decorated with `@arg_digest` perform
argument validation on every call.  When one public function calls another
**internally** — for example, a `build/` function calling `get()` or `select()`
after its own arguments have already been validated — this repeated validation is
wasted work.

The accepted pattern for eliminating this cost is to pass `skip_digestion=True`
to every internal `get()`, `select()`, `convert()`, or other public-API call
that happens inside a function whose outer arguments are already validated:

```python
# Inside build/add_missing_heavy_atoms.py — arguments are already digested
atom_names = get(molsys, element='atom', selection='all',
                 attribute='atom_name', skip_digestion=True)
```

**Rules:**
- `skip_digestion=True` must only be used when the caller has **already** ensured
  the arguments are valid (correct types, shapes, and units).
- Never pass `skip_digestion=True` to calls that receive *user-facing* inputs
  directly — only to calls on data that has already been through the public path.
- All `build/` functions that make internal calls **must** use this flag.
  Failure to do so causes a measurable runtime cost (from ~48 s to < 1 s for
  Barnase–Barstar in `get_missing_heavy_atoms` before and after applying the flag).

This is the inner-loop counterpart to the `ValidatedPayload` passport model: both
exist to ensure that validation cost is paid **once, at the public boundary**, not
repeatedly along the internal call chain.

## Unit-Agnostic Kernels and Alignment on Demand
The structure and PBC kernels should not enforce a single canonical user-level
unit such as `nm` merely because the kernels are hot.

The accepted architectural rule is:

- public wrappers preserve public unit semantics;
- kernels remain unit-agnostic;
- alignment happens only when needed for a particular numeric comparison.

This avoids the old “standardization tax”, where wrappers paid conversion cost
just to feed kernels, even when the public working unit was already coherent.

This is now an explicit design principle:

- **align on demand, not by default**

## Structure Kernel Input Preparation
The local helper layer for structure kernels currently lives in:
- `molsysmt.lib.structure._kernel_inputs`

Current helpers:
- `extract_coordinates_value_and_unit(...)`
- `align_coordinates_values_and_unit(...)`

These helpers are responsible for:
- rank normalization;
- extraction of raw numeric values as `float64`;
- paired-input unit alignment when required;
- returning the working unit that the public wrapper will later use to rebuild
  the public quantity.

This is not accidental duplication of PyUnitWizard functionality.
The helper layer exists because MolSysMT needs domain-specific preparation logic
that is both:
- performance-aware;
- and explicitly tied to the structure-kernel contract.

### Why this layer exists even after recent PyUnitWizard improvements
PyUnitWizard now exposes more explicit extraction control (`value_type`,
`dtype`) and fast-track behavior. That helps, but it does not remove the need
for a MolSysMT-specific preparation layer.

MolSysMT still needs local control over:
- coordinate rank normalization;
- pairwise alignment of coordinate sets;
- wrapper-to-kernel handoff discipline;
- reconstruction of public outputs after kernel execution.

## Float64 Normalization Policy
One of the most important practical hardening decisions taken before `1.0.0` is
this:

- structural and PBC JIT kernels receive `float64` arrays;
- public wrappers are responsible for enforcing that before kernel entry.

This policy exists because real upstream ecosystems frequently provide mixed
numeric dtypes, especially `float32`, and JIT signatures are not forgiving.

The rule should be read as:

- public APIs may remain flexible;
- the JIT boundary may not.

This is why several public wrappers now cast explicitly to `np.float64` before
calling the kernel layer. That is not cargo cult. It is boundary hardening.

This should be read as the current Tier 1 kernel contract, not as a claim that
all future kernels in every domain must forever standardize on `float64`. If a
later domain introduces a different numeric contract, that contract must be made
explicit and measured rather than assumed implicitly.

## Current Adoption of the Prepared-Boundary Model
The current prepared-boundary model is already adopted in important hot paths,
including:

- `get_center`
- `get_distances`
- `get_rmsd`
- `get_least_rmsd`
- `least_rmsd_fit`
- `get_angles`
- `get_dihedral_angles`
- `principal_component_analysis`
- `set_dihedral_angles`
- relevant PBC wrappers such as `wrap_to_mic` and `wrap_to_pbc`

This list matters because it means the pattern is no longer experimental. It is
part of the active architecture.

## Dynamic Parallel JIT & Thread Controls (1.0.0 Stabilization)

To achieve maximum performance scaling on multi-core systems while completely avoiding performance degradation from over-threading on smaller systems or server environments, MolSysMT implements a dynamic JIT parallelization and thread pool scaling architecture.

### 1. Global Configurations
- `msm.configure.parallel_mode`: Sets the active parallelization posture.
  - `'auto'` (default): Scales active threads dynamically between `1` and `num_threads` based on the payload size (workload-based thread scaling). Parallelizes only if payload exceeds `parallel_threshold`.
  - `True`: Forces parallel compilation and execution across the maximum configured threads (`num_threads`), completely bypassing size checks and workload-based scaling.
  - `False`: Completely deactivates parallel JIT. All kernels compile and execute in 100% sequential serial mode.
- `msm.configure.num_threads`: The maximum number of threads dedicated to parallel loops (default `-1` to use all available CPU cores).
- `msm.configure.parallel_threshold`: The payload size threshold (default `500,000` float64 items, i.e., structures * atoms * 3) above which `'auto'` enables parallel execution.
- `msm.configure.min_payload_per_thread`: The minimum payload size (default `250,000` items) allocated per thread under `'auto'` mode.

### 2. Workload-Based Thread Scaling Heuristic
Under `'auto'` mode, running too many threads on small or medium payloads frequently degrades performance due to cache bouncing and thread synchronization overhead. MolSysMT automatically scales the dedicated threads according to the estimated workload size:
$$\text{optimal\_threads} = \max\left(1, \frac{\text{payload\_size}}{250,000}\right)$$
$$\text{active\_threads} = \min(\text{num\_threads}, \text{optimal\_threads})$$

### 3. Local Function Overrides & Thread-Safe Context Manager
- **Context Manager**: Developers and users can temporarily override parallel settings within a thread-safe context block using:
  ```python
  with msm.configure.context(parallel_mode=True, num_threads=4):
      # parallel execution with exactly 4 threads
  ```
- **Local Overrides**: Public structural and mathematical functions (e.g. `get_center`, `get_distances`, `get_rmsd`) accept `parallel` and `num_threads` keyword arguments. These parameters are automatically intercepted and applied thread-safely via the `@with_configure_overrides` decorator.

### 4. Zero-Copy Views and Write-Protection
To completely eliminate memory allocation and deep-copy overhead when retrieving coordinates or box vectors, the native `Structures` class getter properties return direct, zero-copy NumPy views.
To prevent accidental side-effects and mutation of the native state, returned views are write-protected (`val.flags.writeable = False`). In-place mutators within `Structures` (such as `set_coordinates` and `set_box`) temporarily unlock the writeability flag inside a `try...finally` block, perform the update, and immediately re-lock it to guarantee lifecycle integrity.

## Fast Paths and Fast Tracks
The current ecosystem now has two related but distinct ideas that should not be
confused.

### 1. Fast tracks
These are lightweight unit-level shortcuts registered through PyUnitWizard, for
example in `molsysmt/_pyunitwizard.py`.

They exist to accelerate common unit conversions and quantity handling for very
frequent canonical units such as:
- nanometers
- picoseconds
- kelvin

### 2. Fast paths
These are trusted internal execution paths in MolSysMT where:
- the input is already validated;
- the numeric representation is already normalized;
- the inner execution path should not re-digest or re-validate the same data.

The passport/trusted-path model belongs to the second category.

This distinction should remain explicit in docs and code review. A unit fast
track is not the same thing as a trusted kernel fast path.

## Baseline Measurement Snapshot
A lightweight baseline lives in:
- `benchmarks/structure_coordinate_paths.py`

The first stable run uses the bundled `particles 4` `XYZ` trajectory to isolate
coordinate-path cost without mixing in heavier topology rebuilds.

Representative measurements from the documented baseline:
- `extract_coordinates_value_and_unit(...)` around `6.5e-4 s`
- `align_coordinates_values_and_unit(...)` around `8.2e-4 s`
- `structure.get_center(...)` around `2.13e-1 s`
- `structure.get_distances(...)` around `2.22e-1 s`
- `structure.get_rmsd(...)` around `2.63e-1 s`

Interpretation:
- local kernel-input preparation is not the dominant bottleneck;
- this justifies keeping preparation logic in a dedicated local helper layer;
- if more optimization is needed, the next likely bottlenecks are higher in the
  public retrieval/wrapper path, not in `_kernel_inputs` itself.

## Peptide Builder Performance Notes
`build_peptide(engine="MolSysMT")` relies on repeated non-bonded heavy-atom
distance evaluations during geometry optimization. The hot loops must stay in
reusable JIT kernels under `molsysmt/lib`, for example:
- `molsysmt.lib.math.minimum_distance_masked_not_bonded`
- `molsysmt.lib.math.minimum_distance_between_coordinate_sets`

This split is intentional:
- Python layer: topology/template logic and search strategy.
- JIT layer: tight numeric loops (distance scans, masks, bonded exclusions).

## Nested Kernels and Signature Rules
- Nested JIT calls must resolve against compiled dispatchers, not Python
  wrappers.
- The lazy compiler binds only symbols actually referenced by the function
  bytecode.
- For optional `None` arguments in signatures, use the `[numba_type, None]`
  pattern through `make_numba_signature(...)`.
- This is translated to `numba.optional(numba_type)` and must not be handled as
  `Omitted(None)`.

## Warmup
Explicit precompilation remains available through:

```python
molsysmt.warmup_numba()
```

This is the explicit user/developer path to avoid first-use latency in known
hot kernels.

## First-Use Warning
The first cold JIT compilation triggers a one-time SMonitor warning so users and
developers understand why a first call may feel slower than steady-state
execution.

## GPU Acceleration

MolSysMT includes optional CUDA GPU kernels for the most compute-intensive
structure analysis functions. The full design is documented in
`devguide/gpu_acceleration.md`.

Key integration points with the performance model:

- The dispatch layer (`molsysmt/_private/gpu.py`: `resolve_use_gpu`) follows
  the same boundary discipline as the CPU kernels — it sits between the public
  wrapper and the numeric kernel.
- The global switch `molsysmt.configure.use_gpu` defaults to `False` (CPU only),
  so no GPU overhead is paid unless the user opts in.
- All GPU-eligible wrappers accept a `use_gpu` keyword (`None` inherits from
  config, `True`/`False` forces, `'auto'` auto-selects by payload threshold).
- CUDA kernels live in `molsysmt/lib/structure/get_*_cuda.py` and
  `principal_component_analysis_cuda.py` — they are never imported unless
  a GPU code path is actually taken.

GPU support is **NVIDIA CUDA only** for `1.0.0` (via Numba). Cross-vendor
GPU support (ROCm, oneAPI) is deferred post-`1.0.0`.

## Known Risks and Open Post-1.0 Cleanup
For `1.0.0`, the current split between:
- public `get()`
- trusted preparation helpers
- numeric kernels

is considered sufficient. The heavy-trajectory path (`ChunkedExecutor` /
`Reducer`) is now also implemented and follows the same three-layer boundary
discipline — see `SCALABILITY.md`.

What remains open after `1.0.0`:
- if similar kernel helpers spread widely across multiple MolSysMT domains,
  common preparation rules should be centralized more aggressively rather than
  copied;
- thread-safety expectations around lazy JIT should be reviewed if parallel
  user workloads become common enough to justify stronger guarantees;
- heavier `MolSys` and HDF5 coordinate workflows should be profiled separately,
  without conflating I/O cost with the correctness of the current trusted-path
  design;
- the `ChunkedExecutor` performance model (chunk I/O cost, reducer overhead,
  ETA accuracy) should be profiled and documented once representative large
  trajectories are available for benchmarking.

## Correction — 2026-08-13

This historical assessment described `ValidatedPayload` as an adopted optimization.
It never became a live MolSysMT protocol: the only issuance path was unreachable, with
zero decorated callers under `molsysmt.lib.*` and zero hits in the instrumented suite.
The dependency and its dead trust branch were removed under uibcdf/molsysmt#153.
Current code uses ordinary digestion or an explicit, caller-owned
`skip_digestion=True` delegation after the complete callee contract is established.
