(user-foundations-governance-smonitor-and-telemetry)=
# SMonitor & Diagnostic Telemetry

This page is the primary reference guide for **SMonitor**, the diagnostic monitoring, memory pressure auditing, and telemetry framework integrated within MolSysMT.

---

## What is SMonitor?

**SMonitor** is an open-source diagnostic and telemetry library developed by UIBCDF ([https://www.uibcdf.org/smonitor](https://www.uibcdf.org/smonitor)). Its purpose is to provide real-time visibility into execution health, memory consumption, function profiling, and operational events during scientific computing workflows.

---

## What Does SMonitor Do in MolSysMT?

In MolSysMT, SMonitor operates silently in the background to ensure execution safety and performance transparency:

1. **Memory Pressure Auditing**: SMonitor continuously tracks process Real Resident Set Size (RSS). If RAM usage exceeds `molsysmt.configure.memory_pressure_threshold` (default: 80% of `max_ram_usage`), SMonitor emits a `MemoryPressureWarning`.
2. **Chunked Execution Telemetry**: Emits telemetry events during `ChunkedExecutor` operations, logging chunk progress, decision criteria, and array allocation sizes.
3. **Execution Profiling**: Captures function entry/exit timing and kernel execution timelines.

---

## Interpreting SMonitor Signals and Warnings

When SMonitor detects operational thresholds, it emits structured signals:

- **`MemoryPressureWarning`**: Indicates that current process RAM consumption is approaching physical memory capacity. When this warning appears, consider enabling `heavy_mode='force'` or reducing `molsysmt.configure.chunk_size`.
- **Heavy Execution Telemetry Logs**: Displays chunk indices, RAM allocation fractions (`chunk_memory_fraction`), and Eager vs. Heavy path selection decisions.
- **Signal Dictionary**: Comprehensive signal definitions and error codes are detailed in the official SMonitor documentation at [https://www.uibcdf.org/smonitor](https://www.uibcdf.org/smonitor).

---

## Customizing and Controlling SMonitor Behavior

Users can configure SMonitor behavior globally or programmatically:

```python
import molsysmt as msm
import warnings

# 1. Enable or disable heavy execution telemetry events
msm.configure.emit_heavy_telemetry = True

# 2. Adjust RSS memory pressure warning threshold (e.g. 75% of max_ram_usage)
msm.configure.memory_pressure_threshold = 0.75

# 3. Catching SMonitor memory pressure warnings programmatically
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    center = msm.structure.get_center('large_system.h5msm', selection='all')
    
    for warning in w:
        print(f"Captured SMonitor Warning: {warning.message}")
```
