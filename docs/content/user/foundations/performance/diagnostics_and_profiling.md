(user-foundations-performance-diagnostics-and-profiling)=
# Diagnostics & Profiling with SMonitor

MolSysMT integrates a built-in diagnostics and profiling engine managed through **SMonitor** to track execution timelines, memory pressure, and performance telemetry during complex calculations.

---

## Performance Diagnostics and Profiling

Analyzing large molecular systems involves non-trivial execution costs split across file I/O, selection parsing, form conversion, and numeric kernel evaluation.

MolSysMT uses **SMonitor** to provide structured execution profiling:

- **Kernel vs. I/O Profiling**: Measures the precise time spent reading coordinate blocks from disk versus executing numerical kernels (e.g. distance evaluations or SASA integrations).
- **Execution Timelines**: Tracks function entry and exit events across nested API calls to pinpoint bottlenecks in custom workflows.

---

## Memory Pressure & Telemetry Events

During trajectory analysis, SMonitor actively monitors memory pressure and operational events:

- **Memory Pressure Warnings (`MemoryPressureWarning`)**: SMonitor monitors Real Resident Set Size (RSS) memory consumption. If process memory exceeds `molsysmt.configure.memory_pressure_threshold`, SMonitor triggers a diagnostic warning.
- **Telemetry Configuration**: Chunked execution progress and decision telemetry can be toggled using `molsysmt.configure.emit_heavy_telemetry`.
