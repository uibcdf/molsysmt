# Benchmarking Baseline Snapshot

> **Snapshot date:** 2026-05-22. Script inventories and measurements below are
> historical observations. Inspect `benchmarks/` and rerun the harness for the
> current state.

This document tracks the current inventory of benchmark scripts in the MolSysMT repository and registers baseline performance metrics for critical hot paths.

## Existing Benchmark Scripts

At present, our benchmarking harness is focused on hot coordinate manipulation paths under the `benchmarks/` directory:

### 1. `benchmarks/structure_coordinate_paths.py`
- **Purpose:** Measures the execution speed of raw coordinate processing, input alignment, and public geometric wrappers on a small system.
- **Dataset:** `particles 4` (small coordinate trajectory from `molsysmt.systems`).
- **Timing Profile:** Measures five core operations:
  1. `kernel_extract_xyz_coordinates`: Validates raw extraction of value and unit from an `XYZ` form using native helpers.
  2. `kernel_align_xyz_coordinates`: Measures input coordinate alignment for two structures.
  3. `structure_get_center_xyz`: Profiles the public `msm.structure.get_center` function.
  4. `structure_get_distances_xyz`: Profiles the public `msm.structure.get_distances` function.
  5. `structure_get_rmsd_xyz`: Profiles the public `msm.structure.get_rmsd` function.
### 2. `benchmarks/macro/test_kernels.py`
- **Purpose:** Macro-benchmark profiling RMSD, center, and distances on a real NMR miniprotein structure (Trp-Cage, `1l2y.pdb`).
- **Timing Profile:** Profiles three core calculations comparing the high-overhead public API with unit digestion to the direct raw JIT compiled kernels.
- **Results:** Median times of JIT kernels (~1.1 ms for center, ~0.9 ms for RMSD) achieve up to 280x speedups compared to their public API counterparts (~280 ms), highlighting digestion/unit overhead.

### 3. `benchmarks/macro/test_trajectories.py`
- **Purpose:** Profiles heavy trajectory out-of-core reading and chunked execution capabilities using the solvated chicken villin HP35 DCD trajectory (20 frames, 4369 atoms).
- **Timing Profile:** Profiles and compares three modes:
  1. Eager trajectory loading (reading all coordinates in one call).
  2. Frame-by-frame out-of-core streaming via `msm.Iterator`.
  3. Out-of-core chunked processing via `ChunkedExecutor` in `heavy_mode='force'`.

---

## Baseline Execution Profiles

The following baseline metrics represent typical timing profiles captured in the development environment. These metrics serve as our point of reference for regression monitoring:

### Coordinate Baseline Profile (`particles 4` XYZ System)

| Operation Name | Target Component | Median Time per Call (μs) | Target Goal (1.0.0) |
| :--- | :--- | :---: | :---: |
| `kernel_extract_xyz_coordinates` | Input Preparation Helpers | ~5.2 μs | < 10 μs |
| `kernel_align_xyz_coordinates` | Input Preparation Helpers | ~6.5 μs | < 10 μs |
| `structure_get_center_xyz` | Public Wrapper & Kernel | ~310.0 μs | < 400 μs |
| `structure_get_distances_xyz` | Public Wrapper & Kernel | ~350.0 μs | < 400 μs |
| `structure_get_rmsd_xyz` | Public Wrapper & Kernel | ~480.0 μs | < 600 μs |

*Note: Timings are based on a reference CPU execution environment and will vary depending on developer hardware. However, the ratio between public wrapper overhead and native helper costs remains consistent across machines.*

---

## Resolved Hurdles & Sprint 2 Achievements

### Hardened JIT Caching Locator (SMonitor Integrated)
- **Status:** **Resolved.** JIT cache directory routing has been hardened in `molsysmt/_private/jit.py`.
- **Implementation:** Coupled directly to the active SMonitor profile level (`dev`, `qa`, `debug`, or `agent`). The environment variable `NUMBA_CACHE_DIR` is automatically set to a stable, repository-local `.numba_cache/` directory before Numba is imported, ensuring JIT-compiled math kernels are persistently cached across sessions.
- **Validation:** Confirmed correct generation of `.nbc` and `.nbi` compiled objects in `.numba_cache/` under the `qa` profile.

### Heavy Trajectory Stream Processing (DCD Iterator & Chunked Execution)
- **Status:** **Resolved.** Automated out-of-core streaming benchmarks are now fully integrated and executed.
- **Debug Actions:** Resolved several critical bugs in the DCD form during this integration:
  - Added missing `_heavy_support` flag in the `file:dcd` form adapter.
  - Implemented standard context manager protocols (`__enter__`/`__exit__`) for the DCD `StructuresIterator`.
  - Fixed seeking indices loop bug (`self.molecular_system.seek(int(ii))`) and normalized output shape appending by removing extra dimension size-1 arrays.
- **Performance Results:** Out-of-core streaming and chunked execution workloads are validated and perform within reasonable margins (e.g., median eager load ~164 ms vs. chunked execution ~356 ms on 20-frame solvated chicken villin).
