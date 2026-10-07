(user-foundations-performance-gpu-roadmap)=
# GPU Acceleration

MolSysMT provides a strategic roadmap for GPU-accelerated molecular structure sequence processing and spatial calculations in Post-1.0 releases.

---

## Current CPU Acceleration vs. GPU Roadmap

MolSysMT currently optimizes CPU execution using multi-core Rayon parallelization and compiled Rust kernels. For massive structure sequence datasets—such as multi-terabyte datasets containing millions of atoms—GPU hardware acceleration provides an order-of-magnitude throughput increase.

---

## Post-1.0 GPU Acceleration Features

The long-term performance roadmap for MolSysMT introduces dedicated GPU acceleration kernels:

- **WGPU and CUDA Kernels**: Native WebGPU (WGPU) and CUDA compute pipelines for platform-agnostic GPU execution across NVIDIA, AMD, Apple Silicon, and Intel hardware.
- **Massive Pair Distance & Contact Maps**: Parallel GPU evaluation of pair distance matrices, contact frequency maps, and solvent accessibility surfaces across thousands of structures simultaneously.
- **Zero-Copy Trajectory and Structure Streaming to VRAM**: Direct streaming of H5MSM structure sequence chunks into GPU VRAM buffers to maximize compute throughput.
