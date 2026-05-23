# GPU Acceleration

MolSysMT includes optional GPU-accelerated kernels for the most compute-intensive
structure analysis functions.  The implementation uses **Numba CUDA** — pure Python
decorated with `@cuda.jit`, no separate C/CUDA compilation required.

---

## Overview

Eight public functions expose GPU dispatch:

| Function | GPU kernel file |
|---|---|
| `molsysmt.structure.get_distances` | `get_distances_cuda.py`, `get_mic_distances_cuda.py` |
| `molsysmt.structure.get_rmsd` | `get_rmsd_cuda.py` |
| `molsysmt.structure.get_least_rmsd` | `get_least_rmsd_cuda.py` |
| `molsysmt.structure.get_radius_of_gyration` | `get_radius_of_gyration_cuda.py` |
| `molsysmt.structure.get_dihedral_angles` | `get_dihedral_angles_cuda.py` |
| `molsysmt.structure.get_principal_axes` | `get_principal_axes_cuda.py` |
| `molsysmt.structure.principal_component_analysis` | `principal_component_analysis_cuda.py` |

All kernel files live under `molsysmt/lib/structure/`.

The GPU path is **purely optional and transparent**: all functions fall back to
the CPU (Numba JIT) kernel when no CUDA GPU is present, without raising errors.


---

## Requirements

```
numba[cuda]   # Numba with CUDA support
```

A CUDA-capable NVIDIA GPU with the appropriate driver.  No CUDA SDK installation
is required — Numba ships its own PTX compiler.

> **Note:** Numba CUDA currently requires an NVIDIA GPU.  AMD (ROCm) and Intel
> (oneAPI) are not supported.  For open alternatives see the section below.

---

## Configuration

### Global switch — `config.use_gpu`

Set once at the start of a session to control all GPU-eligible calls:

```python
import molsysmt.configure as config

config.use_gpu = False    # (default) CPU only — disables GPU even in 'auto' mode
config.use_gpu = True     # always use GPU when available
config.use_gpu = 'auto'   # (same as per-call 'auto', explicit global opt-in)
```

`config.use_gpu = False` acts as a **global kill switch**: even per-call
`use_gpu='auto'` respects it and falls back to CPU.

### Payload threshold — `config.gpu_threshold`

When `use_gpu='auto'`, the GPU is only used when the estimated payload
(number of floating-point elements) exceeds this threshold:

```python
config.gpu_threshold = 3_000_000   # default: ~3M elements
```

For `get_distances` the payload is `n_structures × n_atoms²`; for `get_rmsd`
and `get_radius_of_gyration` it is `n_structures × n_atoms × 3`.

---

## Per-call `use_gpu` parameter

Every GPU-eligible function accepts a `use_gpu` keyword argument:

| Value | Behaviour |
|---|---|
| `None` | **(default)** Inherit from `config.use_gpu` |
| `True` | Force GPU; emit `GpuNotAvailableWarning` and fall back to CPU if none found |
| `False` | Force CPU |
| `'auto'` | Use GPU when a GPU is available and payload ≥ `config.gpu_threshold` |

---

## Usage examples

### Automatic (default)

```python
import molsysmt as msm

# default: use_gpu=None → inherits config.use_gpu=False → CPU
rmsd = msm.structure.get_rmsd(mol)

# enable GPU globally (auto mode: GPU when payload is large enough)
import molsysmt.configure as config
config.use_gpu = 'auto'

rmsd = msm.structure.get_rmsd(mol)                 # GPU if payload large enough
dist = msm.structure.get_distances(mol)            # GPU if payload large enough
rg   = msm.structure.get_radius_of_gyration(mol)  # GPU if payload large enough
```

### Per-call override

```python
# Force GPU for this call only
rmsd = msm.structure.get_rmsd(mol, use_gpu=True)

# Force CPU for this call (e.g. small system, GPU overhead not worth it)
rg = msm.structure.get_radius_of_gyration(mol, use_gpu=False)
```

### Benchmarking GPU vs CPU

```python
import time
import molsysmt as msm

mol = msm.convert('1abc', to_form='molsysmt.MolSys')

t0 = time.perf_counter()
rmsd_cpu = msm.structure.get_rmsd(mol, use_gpu=False)
t_cpu = time.perf_counter() - t0

t0 = time.perf_counter()
rmsd_gpu = msm.structure.get_rmsd(mol, use_gpu=True)
t_gpu = time.perf_counter() - t0

print(f"CPU: {t_cpu:.3f}s   GPU: {t_gpu:.3f}s   speedup: {t_cpu/t_gpu:.1f}x")
```

---

## Dispatch logic (`molsysmt._private.gpu`)

The module `molsysmt._private.gpu` provides two public helpers used by all
GPU-eligible wrappers:

```python
from molsysmt._private.gpu import gpu_available, resolve_use_gpu

gpu_available()                    # bool — cached after first probe
resolve_use_gpu(use_gpu, payload)  # bool — should this call use GPU?
```

`resolve_use_gpu` priority:

1. `use_gpu=True/False` → immediate decision (no config consulted).
2. `use_gpu=None` → delegate entirely to `config.use_gpu`.
3. `use_gpu='auto'` → GPU iff `gpu_available()` AND `payload >= config.gpu_threshold`.

---

## Kernel design

All CUDA kernels use **Numba `@cuda.jit`** (Python compiled to PTX at runtime):

### `get_distances_cuda.py`

Thread assignment: **(frame, atom_i, atom_j)** — 3-D grid.
`threads_per_block = (4, 8, 8)`.
Two kernels: `get_distances_single_system` (all-vs-all) and `get_distances` (cross-system).

### `get_mic_distances_cuda.py`

Same grid as `get_distances_cuda`.  Adds a device-function MIC wrapper that
handles both **orthogonal** (fast modular shift) and **triclinic** (Cramer
inverse + fractional-coordinate rounding) boxes.

### `get_rmsd_cuda.py`

Thread assignment: **one thread per frame**. `threads_per_block = 256`.
Each thread loops over atoms.  Two entry points: multi-reference and
single-reference (broadcast).

### `get_radius_of_gyration_cuda.py`

One thread per frame, two passes (weighted centre → weighted Rg).
`threads_per_block = 256`.

### `get_dihedral_angles_cuda.py`

Thread assignment: **(frame, quartet_index)** — 2-D grid.
`threads_per_block = (16, 16)`.
All math (cross product, dot product, sign-corrected acos) is inlined as
CUDA device functions — no shared memory needed.

### `get_principal_axes_cuda.py`

One thread per frame.  Contains a **Jacobi iterative 3×3 symmetric eigensolver**
implemented as a CUDA device function using `cuda.local.array` for thread-local
stack arrays — no shared memory, no cuSOLVER dependency.
Provides both `get_principal_inertia_axes` and `get_principal_geometric_axes`.

### `principal_component_analysis_cuda.py`

Hybrid GPU/CPU approach:

1. **CPU** — flatten coordinates, mean-subtract, apply √weights.
2. **GPU** — 2-D kernel (thread per covariance element) accumulates
   `cov[i,j] = Σ_frames flat_w[frame,i] * flat_w[frame,j] / n_structures`.
   `threads_per_block = (16, 16)`.
3. **CPU** — `np.linalg.eigh` on the covariance matrix (eigendecomposition of an
   `n_features × n_features` matrix stays on CPU; only the O(n²·n_frames) inner
   product is offloaded).

---

## Warning: `GpuNotAvailableWarning`

When `use_gpu=True` is requested but no CUDA GPU is accessible, MolSysMT emits a
`GpuNotAvailableWarning` and transparently falls back to the CPU kernel.

```python
from molsysmt._private.smonitor import GpuNotAvailableWarning
import warnings
warnings.filterwarnings('error', category=GpuNotAvailableWarning)  # turn into error
```

---

## Roadmap

| Priority | Function | Status |
|---|---|---|
| Tier 1 | `get_distances` (vacuum + MIC) | ✅ implemented |
| Tier 1 | `get_rmsd` | ✅ implemented |
| Tier 1 | `get_radius_of_gyration` | ✅ implemented |
| Tier 1 | `get_dihedral_angles` | ✅ implemented |
| Tier 1 | `get_principal_axes` | ✅ implemented |
| Tier 1 | `principal_component_analysis` | ✅ implemented (hybrid) |
| Tier 1 | `get_least_rmsd` (Kabsch) | ✅ implemented |
| Tier 2 | `get_sasa` | future (MDTraj CUDA) |


---

## Notes on open alternatives to CUDA

Numba does **not** currently support OpenCL or ROCm/HIP natively.  For
cross-vendor GPU execution, alternatives worth watching are:

- **CuPy** — NumPy-compatible GPU array library; can replace NumPy-style
  operations but does not compile arbitrary Python loops.
- **Taichi** — cross-backend (CUDA, Vulkan, Metal, OpenCL) kernel language;
  could be used to write MolSysMT kernels that run on non-NVIDIA hardware,
  at the cost of an additional dependency.
- **PyOpenCL** — direct OpenCL bindings; verbose but truly vendor-agnostic.

For 1.0.0 the Numba CUDA path covers the target hardware (NVIDIA GPUs common in
HPC and workstations).  Cross-vendor support is deferred post-1.0.0.

---

## Next Generation GPU & Parallelization Proposals (Post-1.0.0)

To further scale performance, optimize memory efficiency, and support heterogeneous hardware architectures, the following next-generation optimization and parallelization pathways are proposed for the roadmap:

### 1. Dynamic JIT Parallelization and Active Thread Regulation
- **Concept**: Expand the dynamic runtime scheduling of multi-threaded CPU kernels compiled via Numba JIT (`@lazy_njit(parallel=True)`). Rather than using static core counts, the library dynamically computes the optimal thread count based on the payload size (using configuration bounds like `config.min_payload_per_thread` and `config.parallel_threshold`) and programmatically adjusts the thread pool size via `numba.set_num_threads()` on-the-fly.
- **Impact**: Eliminates thread-scheduling and synchronization overheads on small molecular systems (e.g., dialanine or single-frame coordinates), where the cost of orchestrating multiple threads exceeds the actual mathematical computation time, while automatically leveraging the full power of multi-core workstations for large, heavy trajectories.

### 2. Strict Thread-Safety and Thread-Local Allocation Patterns in JIT
- **Concept**: Codify strict thread-safety invariants for Numba parallel JIT kernels utilizing `numba.prange`. Specifically, any auxiliary memory buffers, coordinate slices, or temporary work structures must be allocated/initialized *inside* the parallel loop block rather than passed as shared references or sliced outside the loop.
- **Impact**: Guarantees thread isolation and prevents silent write race conditions and memory corruption when multiple JIT threads concurrently execute heavy geometric solvers (such as centroid extraction or alignment calculations).

### 3. Zero-Copy Protected Memory Views
- **Concept**: Transition the core getter methods of native structures (such as `self.coordinates` and `self.box`) to return zero-copy NumPy array views instead of performing expensive deep copies. To safeguard internal structure state against accidental external mutation, returned views are protected by setting their writeable flag to read-only (`view.flags.writeable = False`).
- **Impact**: Removes a massive source of CPU-side garbage collection pressure and array duplication latency in high-frequency analytical workflows. When legitimate in-place modification is required internally (e.g., inside `set_coordinates` or `set_box`), the system temporarily toggles the writeable flag within a strict `try...finally` block.
- **Memory Security Integration**: Returning read-only NumPy array views automatically makes any derived Pint quantities or PyUnitWizard units read-only, establishing a robust, end-to-end immutable contract for user-facing coordinate reads.

### 4. Zero-Copy CuPy Array Form Integration
- **Concept**: Integrate `cupy.ndarray` as a first-class supported format in the `MAPPING` and form registry inside `molsysmt/_depdigest.py`.
- **Impact**: Allows users to load and store trajectories directly in GPU memory as CuPy arrays. This enables complete multi-step structural pipelines (alignment $\rightarrow$ RMSD $\rightarrow$ PCA $\rightarrow$ contacts) to run entirely inside GPU memory without a single CPU-GPU Host-to-Device/Device-to-Host transfer tax, removing the PCI-Express bus bottleneck.

### 5. High-Performance GPU Cell-List Kernels
- **Concept**: Implement O(N) spatial search and neighbor indexing in CUDA using GPU-based Cell Lists.
- **Impact**: Accelerates map-of-contacts (`get_contacts`), neighbor search (`get_neighbors`), and hydrogen bonding (`hbonds`) routines, delivering **10x to 50x speedups** on massive solvated systems ($>1,000,000$ atoms) where O(N^2) CPU/GPU searches are prohibitive.

### 6. Mixed Precision Computing Policies (Float32 Mode)
- **Concept**: Offer an optional `float32` precision mode for compute-heavy structural kernels on consumer GPUs.
- **Impact**: While CPU/HPC runs standard double precision (`float64`), consumer GPUs (such as NVIDIA GeForce RTX series) have highly restricted double-precision compute units. Running kernels in `float32` delivers up to **32x speedups** on standard desktop workstation GPUs.

### 7. Cross-Vendor Portability with Open Standards (Taichi, HIP/ROCm, OpenCL 3.0/SPIR-V, WebGPU)
- **Concept**: Transition post-1.0.0 GPU acceleration from closed, NVIDIA-locked Numba CUDA to hardware-independent, open-standard compute environments:
  - **Taichi Lang**: A high-performance graphics and physical simulation compiler that compiles Python code JIT directly to Vulkan, Metal, OpenGL, and CUDA. Using Taichi enables writing a single, unified mathematical kernel in Python that runs optimally on NVIDIA, AMD, Intel, and Apple Silicon GPUs with equal efficiency.
  - **HIP/ROCm (AMD)**: Enables compiling and executing identical JIT-capable kernel codes on both NVIDIA (via CUDA backend) and AMD (via ROCm backend) hardware with zero performance tax.
  - **Modern OpenCL (OpenCL 3.0 & SPIR-V) via PyOpenCL**: Leverage modern OpenCL 3.0 alongside SPIR-V (Standard Portable Intermediate Representation) for portable cross-vendor binaries. By using Numba's experimental SPIR-V code generator or compiling computational kernels into SPIR-V bytecodes, MolSysMT can JIT-compile and execute high-performance kernels on any OpenCL-compliant device (Intel integrated graphics, AMD APUs, NVIDIA accelerators, and ARM Mali architectures) using `pyopencl`. This ensures the codebase is completely independent of proprietary hardware ecosystems.
  - **WebGPU / WGSL**: As modern web systems transition to WebGPU for high-performance compute in browser sandboxes, standardizing computational descriptors to WebGPU-friendly representations allows seamless backend-to-frontend execution.



