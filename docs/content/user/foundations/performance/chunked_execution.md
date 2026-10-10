(user-foundations-performance-chunked-execution)=
# Chunked Execution

Chunked execution processes supported molecular structure sequences in coordinate blocks. Each operation has its own input, selection, and output limits; streaming coordinates does not guarantee that its complete result fits in RAM.

---

## The Memory Wall Problem

A single-precision coordinate array for a 1-million-atom system across 10,000 structures occupies approximately 120 GB of RAM. Loading such a system using standard eager allocation exceeds the memory capacity of most workstations.

MolSysMT's canonical coordinate buffers use float64, so the same array occupies approximately 240 GB. Supported operations can read selected coordinate blocks instead of materializing the whole sequence.

---

## Eager Path vs. Heavy Path

MolSysMT manages execution through the `ChunkedExecutor` engine:

- **Eager Path**: The selected coordinate array is loaded into RAM and supplied to the reducer in one block.
- **Heavy Path (`ChunkedExecutor`)**: For large structure sequences, MolSysMT streams coordinate blocks in bounded chunks, passes each chunk to the analysis kernel, and accumulates partial results iteratively.

---

## Controlling Execution (`heavy_mode`)

The public chunked route is available for `get_center`, `get_rmsd`, and `get_distances`, subject to each function's supported combinations. The experimental ionic detector also accepts a keyword-only `heavy_mode`, supporting native MolSys and H5MSM 0.5 paths with integer atom-index selections or `'all'`.

### Session Configuration vs. Function Override

```python
import molsysmt as msm

# 1. Global session configuration
msm.configure.chunk_size = 500       # Set global chunk size to 500 structures
msm.configure.max_ram_usage = 8 * 1024**3 # Numeric working budget in bytes

# 2. Per-function call argument override
# Auto mode: MolSysMT decides based on estimated memory footprint
center = msm.structure.get_center('system.h5msm', selection='all', heavy_mode='auto')

# Force chunked path explicitly for one call
center = msm.structure.get_center('system.h5msm', selection='all', heavy_mode='force')

# Force eager path for one call
center = msm.structure.get_center('system.h5msm', selection='all', heavy_mode='off')
```

Configuration sets working estimates rather than an operating-system memory cap. `auto` selects a route using input footprint estimates; ionic calculation also considers its selected coordinate workspace. Unsupported forced combinations raise an explicit error.

## Owning disk-backed results

When a supported operation returns a disk-backed result handle, manage its
lifetime with a context or explicit `cleanup()`. Automatically created backing
files are removed on cleanup and on failed mapping construction. A path supplied
by you stays under your control and is not deleted by those operations. Cleanup
errors propagate so that failed disk retirement remains visible. Avoid copying
the complete result into RAM unless it fits your working budget.

## Ionic analyses and H5MSM 0.5

For supported file calculations, the ionic detector prepares topology, chemical states, and association metadata once, without reading all coordinates or stored analyses. It then projects eligible participant atoms in blocks. Atom-axis identity must be declared, and structure-assigned chemistry must resolve to one known state for the selected structures.

The complete `Interactions` result remains in memory. Coordinate, candidate, and sparse-result working estimates are checked separately; they exclude caller-owned coordinates, full chemistry tables, runtime caches, and Python object overhead. Conservative candidate bounds can reject a calculation even when actual contacts are sparse. There is no incremental result writer or checkpoint/resume interface for this detector.

See {ref}`Getting ionic interactions <Tutorial_Get_ionic_interactions>` for an executable comparison of eager and chunked execution, and {ref}`Saving ionic interactions <Cookbook_Saving_ionic_interactions>` for recalculating directly from H5MSM 0.5 and saving a named analysis. Choose eager execution when the selected input and result fit comfortably; use blocks to control coordinate workspace when necessary. Smaller blocks can add I/O and orchestration cost.

---

## Custom Chunking Scripts with Iterators

If you need to program a custom analysis script or building pipeline that processes large structure sequences in chunked blocks, you do not need to rewrite low-level file parsing. You can build custom chunked execution loops directly using MolSysMT's `Iterator` objects:

```python
import molsysmt as msm

# Stream a large file in chunks of 200 structures
iterator = msm.Iterator('large_system.h5msm', chunk=200, coordinates=True)

for chunk_index, coordinates in enumerate(iterator):
    # Process each chunk of coordinates independently with custom logic
    print(f"Processing chunk {chunk_index} with shape {coordinates.shape}")
```

---

## Memory Pressure Monitoring

MolSysMT integrates with **SMonitor** to track Real Resident Set Size (RSS) memory pressure during execution. If RAM consumption exceeds `molsysmt.configure.memory_pressure_threshold`, a `MemoryPressureWarning` is emitted, allowing workflows to adapt dynamically.
