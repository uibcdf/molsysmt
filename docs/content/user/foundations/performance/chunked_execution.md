(user-foundations-performance-chunked-execution)=
# Chunked Execution

Chunked execution is MolSysMT's core strategy for processing molecular structure sequences that exceed available physical RAM without crashing or requiring complex user code refactoring.

---

## The Memory Wall Problem

A single-precision coordinate array for a 1-million-atom system across 10,000 structures occupies approximately 120 GB of RAM. Loading such a system using standard eager allocation exceeds the memory capacity of most workstations.

To overcome this **memory wall**, MolSysMT implements a dual-path execution model that transparently scales from small test systems to massive production structure sequences.

---

## Eager Path vs. Heavy Path

MolSysMT manages execution through the `ChunkedExecutor` engine:

- **Eager Path**: For small systems, the full coordinate array is loaded into RAM, and analysis kernels process the dataset in a single high-speed pass.
- **Heavy Path (`ChunkedExecutor`)**: For large structure sequences, MolSysMT streams coordinate blocks in bounded chunks, passes each chunk to the analysis kernel, and accumulates partial results iteratively.

---

## Controlling Execution (`heavy_mode`)

All structural analysis functions in MolSysMT accept the `heavy_mode` parameter. Users can configure this behavior globally for the entire session or override it per function call:

### Session Configuration vs. Function Override

```python
import molsysmt as msm

# 1. Global session configuration
msm.configure.heavy_mode = 'force'   # Force heavy chunked path globally
msm.configure.chunk_size = 500       # Set global chunk size to 500 structures
msm.configure.max_ram_usage = '8GB' # Set RAM ceiling threshold

# 2. Per-function call argument override
# Auto mode: MolSysMT decides based on estimated memory footprint
center = msm.structure.get_center('system.h5msm', selection='all', heavy_mode='auto')

# Force chunked path explicitly for one call
center = msm.structure.get_center('system.h5msm', selection='all', heavy_mode='force')

# Force eager path for one call
center = msm.structure.get_center('system.h5msm', selection='all', heavy_mode='off')
```

---

## Custom Chunking Scripts with Iterators

If you need to program a custom analysis script or building pipeline that processes large structure sequences in chunked blocks, you do not need to rewrite low-level file parsing. You can build custom chunked execution loops directly using MolSysMT's `Iterator` objects:

```python
import molsysmt as msm

# Stream a large file in chunks of 200 structures
iterator = msm.Iterator('large_system.h5msm', element='structure', chunk_size=200)

for chunk_index, coordinates in enumerate(iterator):
    # Process each chunk of coordinates independently with custom logic
    print(f"Processing chunk {chunk_index} with shape {coordinates.shape}")
```

---

## Memory Pressure Monitoring

MolSysMT integrates with **SMonitor** to track Real Resident Set Size (RSS) memory pressure during execution. If RAM consumption exceeds `molsysmt.configure.memory_pressure_threshold`, a `MemoryPressureWarning` is emitted, allowing workflows to adapt dynamically.
