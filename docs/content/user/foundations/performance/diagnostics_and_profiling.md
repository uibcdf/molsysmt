(user-foundations-performance-diagnostics-and-profiling)=
# Diagnostics & Profiling with SMonitor

MolSysMT integrates a built-in diagnostics and profiling engine managed through **SMonitor** to track execution timelines, memory pressure, and performance telemetry during complex calculations.

---

## Performance Diagnostics and Profiling

Analyzing large molecular systems involves non-trivial execution costs split across file I/O, selection parsing, form conversion, and numeric kernel evaluation.

MolSysMT uses **SMonitor** to provide structured execution profiling:

- **Kernel vs. I/O Profiling**: Measures the precise time spent reading coordinate blocks from disk versus executing numerical kernels (e.g. distance evaluations or SASA integrations).
- **Execution Timelines**: Tracks function entry and exit events across nested API calls to pinpoint bottlenecks in custom workflows.
- **External Documentation & Governance**: SMonitor's standalone documentation is hosted at [https://www.uibcdf.org/smonitor](https://www.uibcdf.org/smonitor), and its architectural role in MolSysMT is detailed in the **Governance** module.

---

## Controlling Diagnostics and Telemetry

Users can configure SMonitor telemetry and monitor diagnostic events programmatically:

```python
import molsysmt as msm

# 1. Enable progress and decision telemetry events during chunked execution
msm.configure.emit_heavy_telemetry = True

# 2. Set RAM memory pressure warning threshold (80% of max_ram_usage)
msm.configure.memory_pressure_threshold = 0.80

# 3. Running heavy analysis emits diagnostic events and MemoryPressureWarning if pressure is high
center = msm.structure.get_center('large_system.h5msm', selection='all')
```
