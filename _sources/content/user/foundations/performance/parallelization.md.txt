(user-foundations-performance-parallelization)=
# Parallel Execution

MolSysMT leverages multi-core CPU architectures through parallel thread distribution and hardware vectorization.

---

## Multi-Core Parallel Distribution

Analytical kernels in MolSysMT divide independent structure tasks across available CPU cores using **Rayon** multi-threading:

- **Structure Parallelism**: Large structure sequences are partitioned into independent work units executed concurrently across threads.
- **Thread Allocation**: Thread pool sizing can be set globally for the entire session or overridden for specific function calls.

### Global Configuration vs. Function Override

```python
import molsysmt as msm

# 1. Set global session default (use auto-detection with 8 threads)
msm.configure.set_parallelization(parallel='auto', num_threads=8)

# 2. Function call inheriting session configuration
distances = msm.structure.get_distances(system, selection='all')

# 3. Function call overriding parallelization for a single execution
distances = msm.structure.get_distances(system, selection='all', parallel=True, num_threads=4)

# 4. Force single-threaded execution
distances = msm.structure.get_distances(system, selection='all', parallel=False)
```

---

## Hardware SIMD Vectorization

In addition to multi-core thread distribution, inner numerical loops within MolSysMT's compiled Rust kernels maintain sequential, memory-contiguous array layouts. This design allows compilers to generate **SIMD (Single Instruction, Multiple Data)** instructions, enabling CPUs to process multiple coordinate floats in parallel within a single clock cycle.
