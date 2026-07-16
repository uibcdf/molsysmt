# GPU Acceleration

MolSysMT includes optional GPU-accelerated kernels for the most compute-intensive
structure analysis functions.  The implementation uses **Numba CUDA** — pure Python
decorated with `@cuda.jit`, no separate C/CUDA compilation required.

---

## Overview

The core CUDA dispatch is exposed by these seven public functions:

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

A CUDA-capable NVIDIA GPU and a compatible driver/runtime stack are required.
Follow the dependency versions supported by the active MolSysMT environment;
GPU availability must be checked on the target machine.

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

## Implemented backend map

This table records dispatch paths visible in the current source. It does not
certify numerical parity on every supported device; backend-specific tests are
required for that claim.

| Public operation | CUDA dispatch | Taichi dispatch |
|---|---:|---:|
| `structure.get_distances` | Yes | No |
| `structure.get_rmsd` | Yes | No |
| `structure.get_radius_of_gyration` | Yes | No |
| `structure.get_dihedral_angles` | Yes | No |
| `structure.get_principal_axes` | Yes | No |
| `structure.principal_component_analysis` | Yes | No |
| `structure.get_least_rmsd` | Yes | No |
| `structure.get_angles` | Yes | Yes |
| `structure.get_contacts` | Yes | Yes |
| `structure.least_rmsd_fit` | Yes | Yes |
| `physchem.get_sasa` | Yes | Yes |

The Taichi paths are optional and limited to the operations listed above. This
guide makes no general guarantee for all Taichi targets, drivers, or operating
systems.

## CuPy form boundary

`cupy_ndarray` is a registered optional form. Conversions between it and CPU
forms necessarily transfer data between device and host. The existence of the
form does not imply that arbitrary multi-operation MolSysMT workflows remain on
the GPU without intermediate transfers.

MolSysMT does not currently contain a PyOpenCL, HIP/ROCm, SPIR-V, or WebGPU
execution backend. Such backends must be documented as proposals until code and
parity tests exist.

## Related CPU execution features

Parallel CPU dispatch, precision configuration, and the contact cell-list solver
are separate from GPU support. Their contracts belong in
`performance_and_jit.md` and their performance must be demonstrated with dated,
reproducible benchmarks. Do not infer a fixed speedup from the presence of a
cell-list implementation.
