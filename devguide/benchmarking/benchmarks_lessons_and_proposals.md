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

---


## 2. Engineering Proposals for MolSysMT & Sister Libraries

We propose the following engineering interventions to resolve active hurdles and streamline imports across MolSysMT and sister packages (such as TopoMT):

### Proposal 1: Unified Validation Passports (`ValidatedPayload`)
* **Problem:** Internal routines repeatedly check and re-verify units and argument definitions, adding cumulative safety tax.
* **Solution:** Introduce a "Validation Passport" (`ValidatedPayload`) through `argdigest`. When an object enters the public API, it is validated once and marked with a secure passport token. Trust-internal functions inspect this token and immediately bypass `@arg_digest` checks, reducing internal overhead.

### Proposal 2: Extreme Lazy Loading via PEP 562
* **Problem:** MolSysMT's cold import latency is relatively high (~3.68 seconds) because it eagerly loads multiple heavy third-party packages (e.g., MDTraj, OpenMM, MDAnalysis). This pollutes the startup speed of external benchmark scripts and benchmarks of sister libraries.
* **Solution:** Re-engineer `molsysmt/__init__.py` using standard PEP 562 lazy-loading imports (`__getattr__` and `__dir__`). Submodules should only be loaded when their attributes are explicitly accessed, dropping initial package import time to milliseconds.

### Proposal 3: Global Preheat/Warmup Utility (`msm.benchmarks.preheat()`)
* **Problem:** Transient developer systems or ephemeral CI pipelines experience a "first-call delay" due to JIT compilation during initial execution.
* **Solution:** Provide a lightweight warmup utility `msm.benchmarks.preheat()`. When executed, it runs minimal geometric calculations on a dummy 1-atom coordinate array to pre-warm and compile all core math kernels into Python process memory before actual benchmarking begins.

### Proposal 4: Footprint-Aware Heuristics in `ChunkedExecutor`
* **Problem:** Chunked execution imposes heavy processing overhead on small trajectories where eager loading would be significantly faster.
* **Solution:** Equip `ChunkedExecutor` with a footprint estimator. If the estimated coordinate dataset fits comfortably within a pre-defined threshold of the system's available memory, the executor should scale the chunk size up to the maximum, or transparently fall back to eager loading under the hood.

### Proposal 5: Automated Form Adapter Interface Validation
* **Problem:** Custom form adapters are prone to silent interface omissions (like missing context managers `__enter__`/`__exit__` or missing `_heavy_support` dictionary keys) until runtime.
* **Solution:** Create a validation linting utility under `devtools/` (or run it as a pytest suite) that loops over all registered forms in `molsysmt/_depdigest.py` and inspects their modules for structural conformance. The validator will check if the modules have defined `form_name`, `form_type`, `form_info`, context managers for iterators, and correct dimensions for expected conversions.

### Proposal 6: Modular "Core" Mode for Sister Libraries (e.g., TopoMT)
* **Problem:** Sister packages that depend on MolSysMT for fast math kernels inherit the full ~3.68-second cold import delay.
* **Solution:** Develop a lightweight "molsysmt-core" import level that exposes direct mathematical JIT kernels and basic structural formats without importing high-level wrappers, documentation tools, or the comprehensive `PyUnitWizard` registry. This allows TopoMT to gain the benefits of MolSysMT's math performance without suffering import latency.

### Proposal 7: Memory Footprint Tracking & Peak RAM Profiling in Benchmark Suites
* **Problem:** Performance matrices do not reflect memory resource constraints, making it easy to overlook high-RAM bottlenecks or memory leaks during trajectory digestion and conversion.
* **Solution:** Integrate memory telemetry into the benchmark runner (`run_matrix.py`). Use standard libraries like `tracemalloc` or cross-platform process utilities (e.g., `psutil`) to capture peak Resident Set Size (RSS) for each benchmark iteration. Include a "Peak RAM (MB)" column in the benchmark comparison tables and JSON baselines to ensure optimization efforts target both execution speed and memory efficiency.

