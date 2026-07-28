# Benchmarking Lessons, Issues, and Strategic Proposals

This living document registers critical lessons, architectural hurdles, and strategic engineering proposals compiled during the benchmarking passes of MolSysMT. These insights guide future performance hardening cycles.

---

## 1. Core Lessons Learned & Telemetry Insights

### A. The "Digestion & Unit Conversion Tax" is Extremely Severe
* **The Insight:** Geometric calculations executed via direct raw JIT-compiled kernels (e.g., center calculation, RMSD) complete in **sub-millisecond ranges (~0.9 to 1.2 ms)**. However, calling the corresponding public API wrappers takes **~270 to 288 ms** on the same system (Trp-Cage `1l2y.pdb`). This represents an overhead factor of **~240x to 280x**.
* **Analysis:** The performance tax is not numerical; it is entirely algorithmic and overhead-driven inside Python wrapper layers:
  1. **`@arg_digest` Decorator:** Heavy argument parsing, type checks, selection parsing, and matching logic.
  2. **`PyUnitWizard` Parsing:** Physical units wrapping, conversion to canonical units (e.g., nanometers), and dimension checks (e.g., `[L]^1`).
* **Developer Directive:** Raw JIT-compiled math kernels should always be accessed directly in high-frequency internal pathways (or inside Sister libraries like TopoMT), completely bypassing public wrappers.

### B. Out-of-Core Processing Timings & Memory Tradeoffs
* **The Insight:** Comparative performance on the solvated chicken villin trajectory (20 frames, 4369 atoms) revealed a clear hierarchy of speeds:
  * **Eager Trajectory Loading:** **~164.17 ms**
  * **Frame-by-Frame Iterator Streaming:** **~225.05 ms** (37% slower than eager)
  * **Chunked Execution (`ChunkedExecutor`):** **~356.60 ms** (117% slower than eager)
* **Analysis:** Eager loading is faster because it issues a single contiguous disk read and avoids incremental loop boundaries. Incremental streaming (`Iterator`) introduces repeated I/O overhead. `ChunkedExecutor` adds additional boundary checking, chunk-slicing logic, and Reducer invocation overhead in Python.
* **Developer Directive:** Out-of-core streaming is vital for massive trajectories that exceed RAM boundaries, but for small-to-medium trajectories, eager loading should remain the default execution mode.

### C. The Importance of JIT Cache Hardening and Profile Coupling
* **The Insight:** Uncontrolled Numba cache directory settings cause compilation latency to leak into transient execution runs (such as ephemeral virtual environments or Docker nodes).
* **Analysis:** By coupling Numba's `NUMBA_CACHE_DIR` directly to active SMonitor profiles (`dev`, `qa`, `debug`, or `agent`), we successfully routed compiled assets (`.nbc` and `.nbi` files) into a repository-local directory (`.numba_cache/`). This keeps compilations persistent across independent processes and containerized pipelines.
* **Developer Directive:** Developer and testing runs must always run under coupled SMonitor profiles to ensure compiled caches are loaded rather than compiled from scratch.

### D. Form Adapter API Verification Gaps
* **The Insight:** Integration of new macro-benchmarks frequently exposes silent runtime crashes in form adapters due to missing API protocols (e.g., missing context managers, incorrect dimension shapes, missing heavy execution support flags).
* **Analysis:** Because form adapters are dynamically discovered and lazily imported, many compatibility issues are only caught when active out-of-core processing is executed.
* **Developer Directive:** Form adapters must be systematically verified using automated interface checks rather than waiting for integration tests.

### E. Memory Footprint and Peak RAM Profiling Gaps
* **The Insight:** Execution speed (CPU/wall-clock time) provides only a partial picture of overall efficiency. For large-scale molecular dynamics (MD) trajectories, memory footprint (peak RAM consumption) and memory leaks are equally critical. For instance, eager loading of large systems triggers significant RAM spikes compared to memory-mapped or low-overhead numpy/DCD streaming.
* **Analysis:** Current benchmark suites primarily track CPU/wall-clock time. Without tracking peak memory usage (e.g., via `tracemalloc` or Resident Set Size), we cannot detect memory bloat introduced by eager conversion steps, copying data during argument digestion, or intermediate array allocations in JIT/Numba kernels.
* **Developer Directive:** Benchmarking metrics must be expanded to systematically profile peak RAM consumption alongside execution time, especially when evaluating out-of-core streaming and format conversion.

### F. Empirical Timings: JIT Compiles with High Competitiveness vs. Public API Slack
* **The Insight:** Empirical comparisons run on the solvated chicken villin topology (4369 atoms) show that MolSysMT's raw JIT kernels are exceptionally fast—running the Center of Geometry in **~8.20 ms**, RMSD in **~7.93 ms**, and 35-atom Pairwise Distances in **~1.44 ms**. However, public API wrappers suffer a **35x to 220x timing tax**, taking **~280 to 324 ms** for the same operations.
* **Analysis:** JIT math kernels operate within the same single-digit millisecond scale as dedicated C++ packages like MDTraj (which takes ~1.60 ms for Center and ~0.29 ms for RMSD) and actually outperform standard Python loops in MDAnalysis by up to **20x** (MDAnalysis takes ~169 ms for Center and ~161 ms for RMSD). However, the Public API wrapper layer consumes almost 98% of total run time in unit matching and argument parsing. Additionally, complex selections in MolSysMT (~8.54 ms) are **6x faster** than MDTraj (~49.67 ms), showcasing selection engine excellence.
* **Developer Directive:** The raw numerical JIT engines are highly optimized. All development efforts must target reducing the public API decorator and Unit matching overhead, rather than optimizing JIT core code itself.

### G. RSS High-Water Mark Characteristics
* **The Insight:** Measuring the peak Resident Set Size (RSS) process-wide via `/proc/self/status` provides a robust, low-overhead baseline. However, as process-wide high-water mark memory is monotonically increasing, later phases inherit the peak memory of earlier heavy operations (such as MDTraj/MDAnalysis complex selections and coordinate arrays spiking RAM to **~2.19 GB**).
* **Analysis:** While process-wide RSS peak perfectly highlights the global maximum stress point of running the entire suite, it lacks step-by-step granularity because memory once allocated remains associated with the process's high-water mark.
* **Developer Directive:** Global telemetry is excellent for overall stress testing. However, for fine-grained per-competitor analysis, metrics should be isolated to prevent RAM allocation leaks between benchmark steps.

---


## 2. Engineering Proposals for MolSysMT & Sister Libraries

We propose the following engineering interventions to resolve active hurdles and streamline imports across MolSysMT and sister packages (such as TopoMT):

### Proposal 1: Unified Validation Passports (`ValidatedPayload`) — ✅ Done (May 2026)
* **Problem:** Internal routines repeatedly check and re-verify units and argument definitions, adding cumulative safety tax.
* **Solution:** Introduced a "Validation Passport" (`ValidatedPayload`) through `argdigest`. When an object enters the public API, it is validated once and marked with a secure passport token. Trust-internal functions inspect this token and immediately bypass `@arg_digest` checks, reducing internal overhead.
* **Recorded status:** Implemented in the May 2026 benchmark pass. Revalidate
  against current code and tests. See [digestion and dependencies](../../digestion_and_dependencies.md)
  and the repository [ArgDigest guide](../../ARGDIGEST_GUIDE.md).

### Proposal 2: Extreme Lazy Loading via PEP 562 — ✅ Done (May 2026)
* **Problem:** MolSysMT's cold import latency is relatively high (~3.68 seconds) because it eagerly loads multiple heavy third-party packages (e.g., MDTraj, OpenMM, MDAnalysis). This pollutes the startup speed of external benchmark scripts and benchmarks of sister libraries.
* **Solution:** Re-engineered `molsysmt/__init__.py` using standard PEP 562 lazy-loading imports (`__getattr__` and `__dir__`). Submodules are only loaded when their attributes are explicitly accessed, dropping package startup time to milliseconds.
* **Recorded status:** Active in the May 2026 benchmark pass. The **3.34 s to
  approximately 500 ms** measurement is environment-specific; reproduce it
  before reuse. See [digestion and dependencies](../../digestion_and_dependencies.md).

### Proposal 3: Global Preheat/Warmup Utility (`msm.warmup()`) — ✅ Done (May 2026)
* **Problem:** Transient developer systems or performance profiling sessions experience first-use timing distortions due to JIT pre-compilation and lazy loading.
* **Solution:** Developed the unified `molsysmt.warmup(numba=True, modules=True)` preheating engine (replacing the deprecated `warmup_numba()` alias). It programmatically pre-loads all submodules into memory and precompiles all registered JIT kernels.
* **Recorded status:** Implemented in the May 2026 benchmark pass. Revalidate
  against [`molsysmt/warmup.py`](../../molsysmt/warmup.py) and
  [digestion and dependencies](../../digestion_and_dependencies.md).

### Proposal 4: Footprint-Aware Heuristics in `ChunkedExecutor` — ✅ Done (May 2026)
* **Problem:** Chunked execution imposes heavy processing overhead on small trajectories where eager loading would be significantly faster.
* **Solution:** Equipped `ChunkedExecutor` with a memory footprint-aware chunk size estimator. If the selection fits comfortably in RAM, it runs on the eager path. On the heavy path, the executor dynamically scales `chunk_size` up to the safe memory threshold (`chunk_memory_fraction` = 0.10) to minimize I/O passes and Python loop boundaries.
* **Recorded status:** Active in the May 2026 benchmark pass. Confirm with the
  current heavy-execution tests and [SCALABILITY.md](../../SCALABILITY.md).

### Proposal 5: Automated Form Adapter Interface Validation — ✅ Done (May 2026)
* **Problem:** Custom form adapters are prone to silent interface omissions (like missing context managers `__enter__`/`__exit__` or missing `_heavy_support` dictionary keys) until runtime.
* **Solution:** Created the Dynamic Form Adapter QA Linter (`devtools/scripts/validate_form_adapters.py`) and Developer Scaffolding Tool (`devtools/scripts/scaffold_form.py`) to systematically audit and template conforming form modules.
* **Recorded status:** The May 2026 pass reported compliance across 91 adapters.
  This count and conclusion are a dated observation, and known delivery gaps are
  tracked under `pending_bugs/`. See
  [form adapter implementation](../../form_adapter_implementation.md).

### Proposal 6: Modular "Core" Mode for Sister Libraries (e.g., TopoMT) — ✅ Done (May 2026)
* **Problem:** Sister packages that depend on MolSysMT JIT kernels inherit the full ~3.68-second cold import delay.
* **Solution:** Developed a public-facing, lightweight `molsysmt.core` layer that exposes direct mathematical JIT submodules (`math`, `pbc`, `structure`, `topology`) perezosamente under PEP 562 without loading high-level wrappers or the comprehensive `PyUnitWizard` registry.
* **Status:** Fully active. Cold import latency of `import molsysmt.core` drop to sub-400 ms.

### Proposal 7: Memory Footprint Tracking & Peak RAM Profiling in Benchmark Suites — ✅ Done (May 2026)
* **Problem:** Performance matrices do not reflect memory resource constraints, making it easy to overlook high-RAM bottlenecks or memory leaks during trajectory digestion and conversion.
* **Solution:** Integrated peak Resident Set Size (RSS) memory delta tracking (`base_rss_mb`, `peak_rss_mb`, `delta_rss_mb`) inside `BenchmarkHarness` to record memory profiles during timing executions.
* **Status:** Fully active. Baseline JSON results successfully output memory profiles alongside execution times.

### Proposal 8: Boundary-Only Unit Wrapping (Unitless Core Internals) — ✅ Done (May 2026)
* **Problem:** Eager unit wrapping via `PyUnitWizard` on every trajectory read or coordinate query adds massive timing latency (~6x slower DCD loading compared to MDTraj, and 35x-280x slower math wrappers).
* **Solution:** Re-engineered the native `Structures` storage class to use Python properties backed by raw unitless `float64` NumPy arrays in canonical units. Setters dynamically strip units using `_raw_value`, and the public API `msm.get` boundary automatically wraps them in canonical units. High-frequency loops and JIT preparation layers access raw fields directly, completely bypassing the 98% wrapping tax.
* **Status:** Fully active. Passed all 349 basic unit and regression tests with 100% success rate.

### Proposal 9: Isolated Subprocess Memory Telemetry — ✅ Done (May 2026)
* **Problem:** Process-wide RSS metrics act as a cumulative high-water mark, causing later lightweight benchmark runs to inherit the peak memory of earlier heavy operations.
* **Solution:** Re-engineered `BenchmarkHarness.run` to spawn a dedicated worker in a short-lived child process utilizing the fast, memory-copying `fork` start context. Base and peak memory metrics are computed inside the isolated child process and sent back to the parent via a Queue, preventing process-wide memory contamination.
* **Status:** Fully active. Benchmarking session baselines successfully reflect isolated memory metrics starting at a clean baseline of ~477 MB.
