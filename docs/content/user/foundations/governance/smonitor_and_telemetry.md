(user-foundations-governance-smonitor-and-telemetry)=
# SMonitor & Diagnostic Telemetry

MolSysMT integrates with **SMonitor** to provide real-time diagnostic monitoring, execution profiling, and memory pressure warnings.

---

## Reliability Diagnostics with SMonitor

In complex structural biology pipelines, silent memory saturation or unprofiled bottlenecks can disrupt long-running calculations.

MolSysMT addresses this via SMonitor telemetry integration:

- **Real-Time Memory Monitoring**: SMonitor tracks process Real Resident Set Size (RSS). When RAM usage exceeds `molsysmt.configure.memory_pressure_threshold`, SMonitor emits a `MemoryPressureWarning`.
- **Execution Event Profiling**: Captures function entry/exit timelines and decision events during chunked execution.
- **Standalone Framework & Docs**: SMonitor is an independent diagnostic framework developed by UIBCDF. Detailed documentation and integration guides are hosted at [https://www.uibcdf.org/smonitor](https://www.uibcdf.org/smonitor).
