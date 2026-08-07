(user-foundations-performance-chunked-execution)=
# Chunked Execution

Chunked execution is MolSysMT's core strategy for processing trajectories that exceed available physical RAM without crashing or requiring user code refactoring.

---

## The Memory Wall Problem

A single-precision coordinate array for a 1-million-atom system across 10,000 trajectory frames occupies approximately 120 GB of RAM. Loading such a trajectory using standard eager allocation exceeds the memory capacity of most workstations.

To overcome this **memory wall**, MolSysMT implements a dual-path execution model that transparently scales from small test systems to massive production trajectories.

---

## Eager Path vs. Heavy Path

MolSysMT provides two execution modes managed by the `ChunkedExecutor` engine:

- **Eager Path**: For small systems, the full coordinate array is loaded into RAM, and analysis kernels process the dataset in a single high-speed pass.
- **Heavy Path (`ChunkedExecutor`)**: For large trajectories, MolSysMT streams coordinate frames in bounded blocks (chunks), passes each chunk to the analysis kernel, and accumulates partial results iteratively.

---

## Transparent Control (`heavy_mode`)

All structural analysis functions in MolSysMT accept the `heavy_mode` parameter:

- `'auto'` *(default)*: MolSysMT estimates the memory footprint of the request. If the estimated footprint fits within `molsysmt.configure.max_ram_usage`, it selects the Eager Path; otherwise, it switches to the Heavy Path automatically.
- `'force'`: Forces the chunked Heavy Path regardless of trajectory size (ideal for memory-bounded execution).
- `'off'`: Forces the Eager Path, bypassing decision overhead when RAM availability is guaranteed.

---

## Memory Pressure Monitoring

MolSysMT integrates with **SMonitor** to track Real Resident Set Size (RSS) memory pressure during execution. If RAM consumption exceeds `molsysmt.configure.memory_pressure_threshold`, a `MemoryPressureWarning` is emitted, allowing workflows to adapt dynamically.
