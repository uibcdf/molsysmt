# Benchmarking & Performance Optimization Ideas

This document collects developer proposals, performance optimization experiments, and ideas for strengthening MolSysMT's benchmarking and execution capabilities.

---

## 1. JIT Compilation Caching & SMonitor Profile Coupling

### The Problem
During development and deployment, Numba JIT-compiled kernels suffer from startup latency on their first invocation because the compiler must generate optimized machine code. While Numba supports a persistent disk cache (`cache=True` in `njit`), this relies on a stable caching directory locator. In complex development checkouts, this locator can fail or write files to unstable temporary paths, leading to compilation repeating across sessions.

### Proposed Solution
Implement a profile-driven Numba cache locator strategy for MolSysMT:
1. **SMonitor Profile Coupling:** At package import time in `molsysmt/_private/jit.py`, query the active SMonitor profile from `smonitor.get_manager().config.profile`.
2. **Repository-Local Cache for Developers:** If the active profile is `"dev"`, `"qa"`, `"debug"`, or `"agent"`, automatically set the Numba cache directory path to a persistent folder `.numba_cache/` in the repository root:
   ```python
   import os
   import smonitor
   from molsysmt._private.smonitor import PACKAGE_ROOT
   
   try:
       _profile = smonitor.get_manager().config.profile
   except Exception:
       _profile = "user"
   
   if _profile in ("dev", "qa", "debug", "agent"):
       if "NUMBA_CACHE_DIR" not in os.environ:
           os.environ["NUMBA_CACHE_DIR"] = str(PACKAGE_ROOT.parent / ".numba_cache")
   ```
3. **User Isolation:** For standard `"user"` profiles, do not override the default Numba cache directory, preventing intrusive writes outside the library installation directory.

---

## 2. Memory-Efficient Views vs. Array Copies

### The Problem
When extracting coordinates or topological indices from various forms (e.g. converting from `mdtraj.Topology` to raw arrays), we often copy data to satisfy strict structure or type requirements. Copies increase memory usage and add significant latency when dealing with large trajectory trajectories.

### Proposed Solution
- **Zero-Copy Views:** Standardize on returning NumPy views (`ndarray.view()`) instead of deep copies when the underlying form has the correct layout and type.
- **Read-Only Enforcements:** For hot-path coordinate parameters, enforce read-only arrays (`array.flags.writeable = False`) to allow safe view sharing without risking side-effects or system corruption.
- **Audit Tooling:** Add a memory-tracking utility in our benchmark suites to trace how many temporary arrays are instantiated during standard operations.

---

## 3. Profiling Tools & Methodology Evaluation

To get fine-grained insights into where MolSysMT spends its time, we should evaluate and standardize on the following developer profiling tools:

### Micro-Profiling (Function/Line Level)
- **`line_profiler`:** Excellent for dissecting exactly which Python statements within `@digest` or input-preparation helpers consume CPU cycles.
- **`py-spy`:** A sampling profiler that can be attached to running processes without code modification. Highly useful for diagnosing hung trajectory loading or out-of-core streaming bottlenecks.

### Memory & System Profiling
- **`scalene`:** A high-performance CPU, GPU, and memory profiler for Python. It can accurately distinguish between time spent in Python code, native C/C++ libraries, and JIT compiled code.
- **`tracemalloc`:** Standard Python library utility. We can wrap core converters in test suites using `tracemalloc` to assert that memory allocations scale linearly (or remain constant) rather than quadratically.

---

## 4. JIT Kernel Optimizations

For mathematical operations under `molsysmt.lib.structure`, we should test the performance gains of:
- **`fastmath=True`:** Enables JIT to utilize aggressive IEEE 754 floating-point optimizations (such as ignoring NaNs/Infs and enabling vectorization). This can yield substantial speedups for distance and RMSD calculations.
- **`parallel=True`:** Use Numba's automatic parallelization (`prange`) for heavy coordinate loops, such as computing pairwise distances for multiple frames. This must be toggleable to prevent conflicts when MolSysMT is run within existing MPI or multiprocessing workflows.

---

## 5. Eager Import Latency & Lazy Loading Architecture

### The Problem
MolSysMT currently suffers from a significant **cold import latency of ~3.68 seconds**. This slow startup hampers user experience (CLI startup delays) and critically pollutes external performance evaluations. For example, when other libraries (such as `topomt`) run benchmarks that depend on MolSysMT, their timed execution is dominated by the overhead of importing MolSysMT rather than their own scientific algorithms.

The import time analysis (`python -X importtime`) reveals the primary drivers of this latency:
- Sequential eager submodule imports in `molsysmt/__init__.py` (e.g. `.basic`, `.form`, `.topology`, `.structure`, `.build`, `.physchem`, `.molecular_mechanics`, `.hbonds`, `.third_party`).
- Heavy external dependencies (e.g. `numba` takes ~284ms, `networkx` takes ~173ms, `numpy` takes ~50ms, compiled binary modules take ~297ms) loaded eagerly during startup.

### Proposed Solution (PEP 562 Lazy Loading)
To achieve a cold import time of **under 0.1 seconds**, we propose refactoring `molsysmt/__init__.py` to implement lazy submodule loading based on Python 3.7+ module-level `__getattr__` and `__dir__`:

1. **Replace Eager Submodule Imports:** Remove all top-level eager imports of submodules like `.basic`, `.structure`, `.topology`, etc., in `molsysmt/__init__.py`.
2. **Implement `__getattr__` Routing:**
   ```python
   import importlib
   
   _LAZY_SUBMODULES = {
       "basic": "molsysmt.basic",
       "structure": "molsysmt.structure",
       "topology": "molsysmt.topology",
       "build": "molsysmt.build",
       "physchem": "molsysmt.physchem",
       "molecular_mechanics": "molsysmt.molecular_mechanics",
       "hbonds": "molsysmt.hbonds",
       "third_party": "molsysmt.third_party",
       "systems": "molsysmt.systems",
       "warmup_numba": "molsysmt.warmup_numba",
   }
   
   def __getattr__(name):
       if name in _LAZY_SUBMODULES:
           return importlib.import_module(_LAZY_SUBMODULES[name])
       raise AttributeError(f"module 'molsysmt' has no attribute '{name}'")
       
   def __dir__():
       return sorted(list(globals().keys()) + list(_LAZY_SUBMODULES.keys()))
   ```
3. **Core Functions Promotion:** For frequently used public functions (e.g. `msm.convert`, `msm.select`, `msm.get`, `msm.set`) normally imported from `basic`, we can lazily load them as well:
   ```python
   _LAZY_FUNCTIONS = {
       "convert": "molsysmt.basic.convert",
       "select": "molsysmt.basic.select",
       "get": "molsysmt.basic.get",
       "set": "molsysmt.basic.set",
       "info": "molsysmt.basic.info",
   }
   # Add to __getattr__ matching logic to dynamically load and return the callable.
   ```

By implementing this architecture, we defer loading of heavy scientific submodules and third-party dependencies entirely until they are actively accessed by the user, achieving near-instantaneous imports.

