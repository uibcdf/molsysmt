(user-foundations-performance-gpu-roadmap)=
# GPU Acceleration

MolSysMT provides a strategic roadmap for GPU-accelerated trajectory analytics and spatial indexing in Post-1.0 releases.

---

## Current CPU Acceleration vs. GPU Roadmap

MolSysMT currently optimizes CPU execution using multi-core Rayon parallelization and Rust C-API kernels. For massive trajectory datasets—such as multi-terabyte simulations containing millions of atoms—GPU hardware acceleration provides an order-of-magnitude throughput increase.

---

## Post-1.0 GPU Acceleration Features

The long-term performance roadmap for MolSysMT introduces dedicated GPU acceleration kernels:

- **WGPU and CUDA Kernels**: Native WebGPU (WGPU) and CUDA compute pipelines for platform-agnostic GPU execution across NVIDIA, AMD, Apple Silicon, and Intel hardware.
- **Massive Pair Distance & Contact Maps**: Parallel GPU evaluation of pair distance matrices, contact frequency maps, and solvent accessibility surfaces across thousands of trajectory frames simultaneously.
- **Zero-Copy Trajectory Streaming to VRAM**: Direct streaming of H5MSM trajectory chunks into GPU VRAM buffers to maximize compute throughput.
