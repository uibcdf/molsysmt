# GPU from Rust: options and recommendation

**Status:** original landscape retained; near-term recommendation superseded by
the Rust-only 1.0 decision of 2026-07-26.
**Relates to:** `../archive/resolved_proposals/rust_numba_coexistence_and_cut_plan.md`,
`linear_algebra_backend_for_rust_kernels.md`.

> MolSysMT 1.0 will not retain Numba solely for CUDA. The current Numba-CUDA
> surface must be removed before 1.0. A generic GPU contract may remain only if
> a non-Numba backend satisfies its declared scientific and failure contracts.
> See [`release_1_0_execution_plan.md`](release_1_0_execution_plan.md).

## The question

Now that the CPU kernels are ported to Rust, should the Rust layer also target the GPU —
replacing or complementing the current GPU backends — or should GPU stay where it is?

## Current state

MolSysMT already has GPU, and it is **orthogonal** to the numba/rust CPU choice:

- GPU kernels: Numba CUDA (`molsysmt/lib/structure/*_cuda.py`) and Taichi
  (`*_taichi.py`), selected by `configure.use_gpu` / `configure.gpu_backend`
  (`'cuda'|'taichi'`).
- The Rust migration replaces the **CPU** Numba kernels. It does not touch the GPU path;
  `_private/gpu.py` is intentionally left unrouted.

So there are two independent axes, and they should stay independent:

| | `use_gpu=False` | `use_gpu=True` |
|---|---|---|
| `kernel='numba'` | Numba CPU | GPU (cuda/taichi) |
| `kernel='rust'` | Rust CPU | GPU (cuda/taichi) |

`kernel` picks the CPU backend; `use_gpu` picks CPU-vs-GPU. Rust is not in the GPU cell.

## The Rust GPU landscape

There is a real ecosystem, at three levels:

| crate | what it is | portability |
|---|---|---|
| `cudarc` | safe CUDA driver bindings (+ cuBLAS/cuFFT/NCCL), actively maintained | NVIDIA only, needs CUDA runtime |
| `cust` (Rust-CUDA) | write kernels in Rust → PTX; ambitious, recently revived after a dormant spell | NVIDIA only |
| `wgpu` | cross-platform compute (Vulkan/Metal/DX12/WebGPU) | NVIDIA + AMD + Apple + Intel |
| `rust-gpu` | compile Rust → SPIR-V compute shaders | Vulkan-class |
| `candle` / `burn` | ML tensor frameworks with GPU backends | multi, heavy |

## The deciding constraint is the same one as LAPACK: packaging

The migration's value rests on a single self-contained `cp311-abi3` wheel with no system
dependency (see `linear_algebra_backend_for_rust_kernels.md`). GPU collides with that in
exactly the same way:

- **CUDA (`cudarc`/`cust`)** links the CUDA runtime → breaks the portable wheel, and is
  NVIDIA + x86/ARM-CUDA only. It also duplicates what Numba CUDA already does.
- **`wgpu`** is portable and pure-Rust-ish, but pulls a large dependency and a driver
  surface (Vulkan/Metal), and will not match hand-tuned CUDA on NVIDIA hardware.

Neither belongs in the default wheel.

## Updated Recommendation

1. **Do not add GPU code to the default Rust wheel for the 1.0 cut.** Keep the
   portable CPU wheel focused and self-contained.

2. **Remove Numba-CUDA before 1.0.** Audit Taichi independently. If it cannot
   satisfy the declared operation, scientific parity, dependency, and error
   contracts, narrow or remove the GPU API for 1.0 rather than retaining Numba.

3. **If GPU-from-Rust is pursued later, `wgpu` is the default-wheel-compatible choice** —
   portable across NVIDIA/AMD/Apple Silicon/Intel, no CUDA lock-in, accepting that it will
   not beat tuned CUDA on NVIDIA. For NVIDIA users who want maximum performance, an
   **optional CUDA-feature wheel variant** (`cudarc`, a separate wheel, not the default)
   is the clean way to offer it without polluting the portable wheel — the same
   "optional accelerated variant" pattern discussed for MKL.

4. **A unified Rust CPU+GPU kernel remains a long-term option, not a 1.0 goal.**
   Its appeal is one source of truth for each kernel (CPU and GPU from the same Rust code
   via `wgpu`), retiring both the Numba CPU *and* the Numba-CUDA/Taichi GPU paths. That is
   attractive for maintenance, but it is a large piece of work and should be weighed only
   after the CPU cut has proven itself in dogfooding.

## Summary

GPU-from-Rust is possible and, with `wgpu`, even portable, but it is a separate
post-cut decision. The CPU migration does not wait for a replacement GPU
implementation; the 1.0 cleanup removes Numba-CUDA and retains only independently
validated non-Numba capability.
