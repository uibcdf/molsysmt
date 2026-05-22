# Competitive Performance Comparison Results

This document presents the benchmark results comparing **MolSysMT** (Public APIs and native JIT-compiled kernels) against industry-standard structural biology libraries: **MDTraj** and **MDAnalysis** (and optimized Scientific Python workflows using **Scipy**).

Timings represent the median execution values recorded on standard x86_64 Linux developer environments under garbage collection isolation, pre-warmed JIT caches, and SMonitor QA profiling.

---

## 1. Benchmarking Timing Matrix

The following table summarizes the performance timings across multiple critical domains. All values denote median durations of execution.

| Operation Area | MolSysMT Public | MolSysMT JIT | MDTraj | MDAnalysis |
| :--- | :---: | :---: | :---: | :---: |
| **Trajectory Load (DCD)** | 176.951 ms | *N/A* | 29.655 ms | 49.119 ms |
| **Selection Simple (CA)** | 5.838 ms | *N/A* | 3.959 ms | 0.218 ms |
| **Selection Complex** | 10.545 ms | *N/A* | 58.336 ms | 0.706 ms |
| **Center of Geometry** | 291.132 ms | 9.389 ms | 1.796 ms | 193.224 ms |
| **RMSD Calculation** | 306.491 ms | 8.349 ms | 0.654 ms | 177.921 ms |
| **Pairwise Distances** | 640,028.151 ms | 24,324.180 ms | 4,649.972 ms | 3,496.193 ms |

> [!NOTE]
> * **MDTraj** does not provide a native all-to-all pairwise distance matrix computation. Thus, for MDTraj, we utilize a standard scientific Python workflow combining coordinate access with optimized C-based `scipy.spatial.distance.cdist`.
> * Trajectory load is evaluated using chicken villin HP35 (4,369 atoms, 20 frames).
> * Geometric calculations are performed on chicken villin HP35 (4,369 atoms).
> * Selections are parsed and mapped on Trp-Cage miniprotein `1l2y.pdb` (20 structures, 304 atoms).

---

## 2. In-Depth Architectural Analysis & Trade-Offs

### A. Trajectory Loading
* **Observations:** MDTraj is the fastest at loading eager coordinates (29.6 ms), with MDAnalysis taking slightly longer (49.1 ms). MolSysMT Public experiences a **~6x slower** latency (176.9 ms) relative to MDTraj.
* **Diagnosis:** MolSysMT parses trajectory coordinates eager-style by converting the file representation through the dynamic convert network, wrapping it into high-level Python form objects, and resolving units with PyUnitWizard. This creates cumulative Python instantiation tax.
* **Strategy:** For standard trajectories, eager loading is sufficient. However, for massive trajectory files exceeding RAM boundaries, MolSysMT's chunked memory streaming (`msm.Iterator`) bypasses eager loading taxes by yielding coordinates on-demand, which maintains a low, flat Resident Set Size (RSS) profile.

### B. Selection Syntax Resolution
* **Observations:** 
  - For **Simple Queries** (`'name CA'`), MDAnalysis is extremely fast (0.218 ms), while MolSysMT takes 5.8 ms.
  - For **Complex Queries** (`'(name CA or name CB) and resname ALA VAL LEU'`), MolSysMT completes in **10.5 ms**, outperforming MDTraj's compilation time (**58.3 ms**) by **~5.5x**.
* **Diagnosis:** MDAnalysis uses a direct parsed selection engine with low overhead. MDTraj compiles query strings into Python byte-code loops which introduces heavy compilation delay on its first parse. MolSysMT utilizes a smart cached query parsing system that converts strings to internal selection lists efficiently.
* **Strategy:** MolSysMT is highly competitive in complex queries. By adding persistent selection query caching, we can lower the lookup time for simple queries to microsecond ranges on repeated calls.

### C. Geometric Kernels: Public wrappers vs. Raw JIT
* **Observations:**
  - **Center of Geometry:** MolSysMT JIT kernel (9.38 ms) is **~20x faster** than MDAnalysis's NumPy wrapper (193.2 ms).
  - **RMSD:** MolSysMT JIT kernel (8.34 ms) is **~21x faster** than MDAnalysis's Cython wrapper (177.92 ms).
  - **Pairwise Distances:** MDAnalysis is the fastest (3.49 s), closely followed by Scipy (4.6 s). MolSysMT JIT kernel is third (24.3 s), while MolSysMT Public wrapper is extremely slow (640.0 s).
* **Diagnosis of the "Public API Tax":**
  Calling the JIT kernel directly (e.g. `jit_get_center`) takes 9.38 ms. Calling the same operation through `msm.structure.get_center` takes 291.13 ms. This represents a **31x overhead factor**!
  For pairwise distances, the difference is even more staggering: **24.3 seconds** (JIT) versus **640 seconds** (Public) — a **26x overhead factor**!
  This overhead is driven by:
  1. **PyUnitWizard / Pint Resolution:** Standardizing coordinates and returning arrays wrapped in physical units (nanometers).
  2. **PBC and Argument Digestion:** High-frequency validation, selection parsing, and checking bounds via `@arg_digest`.
* **Diagnosis of the JIT Distance Bottleneck:**
  MolSysMT's JIT pairwise distance calculation (24.3 s) is slower than MDAnalysis (3.49 s) and Scipy (4.6 s). The JIT function uses an explicit double loop in Numba that indexes sliced vectors and invokes a separate distance JIT helper.
  Inside Numba, indexing coordinates in a loop triggers memory views or virtual array allocations, and calling a non-inlined function inside a 190-million-iteration loop adds heavy numerical processing overhead. MDAnalysis and Scipy use vectorized C-libraries that bypass Python/Numba loop logic completely.

---

## 3. Concrete Engineering Interventions

Based on these competitive benchmarks, we register three high-priority optimization tasks:

1. **Direct Fast-Paths for Sister Libraries:**
   Sister packages (such as TopoMT) that depend on MolSysMT for heavy geometric processing should **never** import or call public APIs. They must bypass the public wrappers completely and directly import the underlying JIT kernels from `molsysmt.lib.structure.*`. This eliminates the 31x "Public API Tax" immediately.
2. **Vectorization of JIT Kernels:**
   We must rewrite the JIT loop inside `molsysmt/lib/structure/get_distances.py` and `get_mic_distances.py`. By replacing explicit element loops with vectorized NumPy array operations and leveraging Numba's `@njit(parallel=True, fastmath=True)` directives, we can achieve parity with Scipy's compiled C engines.
3. **Pint / PyUnitWizard Fast-Track unit bypass:**
   PyUnitWizard must implement a "Fast-Track" bypass registry. When standard units (nanometers, picoseconds) are detected on NumPy arrays, the wrapper must strip the units instantly using primitive pointer slicing, rather than performing full dimensional checks inside Pint.
