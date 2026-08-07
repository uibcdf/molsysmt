(user-foundations-performance-parallelization)=
# Parallel Execution

MolSysMT leverages multi-core CPU architectures through parallel thread distribution and hardware vectorization.

---

## Multi-Core Parallel Distribution

Analytical kernels in MolSysMT divide independent frame tasks across available CPU cores using **Rayon** multi-threading:

- **Frame Parallelism**: Trajectory frames are partitioned into independent work units executed concurrently across threads.
- **Thread Allocation**: Thread pool sizing is managed globally via `molsysmt.configure.set_parallelization(num_threads=N)` or per-function call.

---

## Hardware SIMD Vectorization

In addition to multi-core thread distribution, inner numerical loops within MolSysMT's compiled kernels maintain sequential, memory-contiguous array layouts. This design allows compilers to generate **SIMD (Single Instruction, Multiple Data)** instructions, enabling CPUs to process multiple coordinate floats in parallel within a single clock cycle.
