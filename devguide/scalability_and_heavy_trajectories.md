# Scalability and Heavy Trajectory Processing Strategy: The "HeavyAnalysisEngine" Manifesto

> **Status: Long-term Vision (superseded for 1.0.0 planning)**
>
> This document describes the long-term aspirational architecture for out-of-core
> trajectory processing. It is **not** the current execution plan.
>
> For the actual pre-1.0.0 implementation roadmap (minimum viable chunked execution,
> `MSM-*-HVY-*` signal codes, and the reducer protocol), see:
>
> → **`devguide/scalability_and_heavy_trajectories_v2.md`** (current working design)
>
> This file is kept as a reference for the long-term direction after 1.0.0.

## 1. The Context: Breaking the "Memory Wall"
As MolSysMT evolves towards its 1.0.0 release, it must address its primary scalability bottleneck: the **Eager Loading Model**. In the modern era of "Big Data" simulations, trajectories often exceed 100GB, while standard research workstations remain capped at 16GB–64GB of RAM. To lead the next generation of analysis tools, MolSysMT adopts an **Out-of-Core** architecture that processes data larger than physical memory.

## 2. Core Philosophy: The Four Pillars of Scalability
1.  **UX Invisibility**: The scientist uses the same API regardless of data size. MolSysMT manages the complexity.
2.  **Hardware Empathy**: The library adapts to the environment (laptop vs. HPC node).
3.  **Trust via Observability**: SMonitor provides transparency on every internal decision.
4.  **I/O Efficiency**: Disk access is the ultimate bottleneck; we must "Read Once, Analyze Many."

## 3. The "Brain": Metadata-Driven Decision Making
Before reading any coordinate, MolSysMT performs a **Pre-flight Footprint Calculation**:
- `Footprint = N_atoms * M_structures * 3_dims * 8_bytes (float64) + 20% Safety Margin`.
- If `Footprint < molsysmt.configure.max_ram_usage`: **Eager Path** (Maximum speed).
- If `Footprint >= molsysmt.configure.max_ram_usage`: **Heavy Path** (Activate `HeavyAnalysisEngine`).

## 4. Advanced Analytical Orchestration

### 4.1 Analytical Multitasking (The "Read-Once" Principle)
The engine supports chaining multiple tasks to minimize I/O overhead.
- **Mechanism**: Instead of reading a 500GB file three times for distances, RMSD, and center of geometry, the engine reads a chunk once and passes it to all registered tasks in memory.
- **Benefit**: Up to 3x–10x speedup by eliminating redundant disk reads.

### 4.2 Cloud & Remote Streaming
The `HeavyAnalysisEngine` is designed to be location-agnostic.
- **Streaming**: Supports reading chunks directly from remote buckets (S3, Google Cloud, HTTP) via `fsspec` integration.
- **Logic**: The engine requests only the byte-ranges needed for the current chunk, avoiding the need for a full local download.

## 5. The Resilient Tank: Operational Safety & Protection

### 5.1 The Predictive "Dry Run" & ETA
Processes the first chunk to estimate total time and memory.
- **Output**: *"Estimated Analysis Time: 4h 20m. Constant RAM usage: 1.2GB. Proceed? [Y/n]"*

### 5.2 Storage "Kill Switch"
Checks available disk space before starting heavy output tasks. Aborts early if storage is insufficient.

### 5.3 Native Checkpointing (Resumable Analysis)
Incrementally saves partial results to a persistent buffer. Allows resuming from the last successful chunk after an interruption.

### 5.4 Error Tolerance (Bad Frame Shield)
Detects and skips corrupt frames, logging errors via SMonitor without crashing the entire pipeline.

## 6. Resource Governance & Telemetry

### 6.1 Adaptive Resource Throttling
MolSysMT should be a "Good Citizen" on the user's OS.
- **Work Mode**: Uses 50% of CPU cores to allow background workstation use.
- **HPC Mode**: Uses 100% of resources for maximum throughput.
- **Adaptive**: Dynamically scales resource usage based on system load.

### 6.2 Real-Time Telemetry Dashboard
For long-running tasks, the engine provides a live status update:
- **Throughput**: Current frames/second.
- **Memory Pressure**: Real-time RAM consumption vs. limit.
- **Hardware Health**: CPU temperature and I/O wait times.
- **Dynamic ETA**: Completion prediction that adjusts to disk/network speed fluctuations.

## 7. Tiered Implementation Roadmap
- **Tier 1 (Core)**: Sequential chunking, basic SMonitor feedback, and basic ETA.
- **Tier 2 (Performance)**: Multi-core parallelism, analytical multitasking, and SSD/HDD awareness.
- **Tier 3 (Enterprise)**: Cloud streaming, GPU offloading, and checkpointing.

## 8. Handling the "Output Wall"
The engine avoids memory crashes by returning **Lazy Result Handles** (backed by HDF5 or Zarr) for heavy outputs, ensuring end-to-end memory safety.

## 9. Developer Contract
Functions must be **Stateless**, provide a **Reducer** for accumulative logic, and use **Memory Views** to avoid copies.

## 10. User Configuration (`molsysmt.configure`)
- `max_ram_usage`: RAM threshold for "Heavy" mode.
- `priority_profile`: 'Work', 'HPC', or 'Adaptive'.
- `remote_streaming`: Enable/disable cloud I/O.
- `checkpointing`: Toggle for resumable tasks.

## 11. Conclusion
The `HeavyAnalysisEngine` represents MolSysMT's maturity as a data orchestration platform. It allows researchers to handle trajectories of any size, from any location, with absolute confidence in the system's resilience and efficiency.
