# GPU Acceleration Contract

MolSysMT has optional GPU kernels for selected structure and physicochemical
operations. GPU support is operation-specific and does not imply a device-
resident workflow across arbitrary conversions or analyses.

## Configuration and dispatch

The active configuration is:

- `molsysmt.configure.gpu_mode`: `"auto"`, `True`, or `False`;
- `molsysmt.configure.use_gpu`: compatibility alias synchronized by managed
  configuration contexts;
- `molsysmt.configure.gpu_threshold`: auto-dispatch threshold;
- `molsysmt.configure.gpu_backend`: `"cuda"` or experimental `"taichi"`;
- `molsysmt.configure.precision`: `"double"` or `"single"` where implemented.

Both `gpu_mode` and `use_gpu` currently default to `"auto"`. Per-call
`use_gpu=None` inherits the global mode; `True` requests GPU with warning and CPU
fallback when unavailable; `False` selects CPU; `"auto"` also applies the
payload threshold.

Only some wrappers accept `gpu_backend` or `precision`. Consult the public
signature and tests rather than assuming all GPU-enabled functions expose the
same controls.

## Implemented backend map

This table records dispatch branches visible in the current source. It is not a
device compatibility or numerical-parity certificate.

| Public operation | CUDA branch | Taichi branch |
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

Taichi is experimental and imported lazily. The CUDA path requires compatible
Numba CUDA support, NVIDIA hardware, and a working driver/runtime stack. MolSysMT
does not currently implement HIP/ROCm, oneAPI, PyOpenCL, SPIR-V, or WebGPU
backends.

## Fallback and diagnostics

GPU unavailability may produce a warning and CPU fallback. A fallback is not
evidence that the GPU branch was tested. Tests and benchmarks must record the
backend actually selected, device information, precision, and any warning.

Backend-specific import or execution failures must not be silently represented
as successful GPU execution. Fallback behavior must preserve public units,
shape, ordering, and numerical tolerances.

## Precision and parity

GPU parity is defined per operation. Tests should cover:

- CPU versus each implemented backend;
- double and single precision only where the wrapper exposes them;
- PBC and non-PBC branches where applicable;
- weighted and unweighted variants;
- degenerate geometries and empty/small selections;
- fallback when dependencies or devices are absent.

Tolerance must follow the scientific operation and precision; a single global
GPU tolerance is insufficient.

## Data movement

`cupy_ndarray` is an optional registered form. Conversion between CuPy and CPU
forms transfers data between device and host. Most public wrappers also perform
host-side preparation. Do not claim end-to-end zero-copy or persistent device
residency without a workflow-level transfer test.

## Benchmark evidence

GPU speedups depend on transfer size, compilation state, kernel geometry,
precision, device, driver, and workload. Report raw timings with CPU/GPU parity,
warm-up state, repetitions, and payload dimensions. The dispatch threshold is a
heuristic configuration value, not a universal crossover guarantee.
