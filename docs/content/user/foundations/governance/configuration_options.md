(user-foundations-governance-configuration-options)=
# Configuration Options

MolSysMT provides a centralized configuration manager, **`molsysmt.configure`**, allowing users and workflows to customize execution defaults globally.

---

## Key Configuration Parameters

Global options exposed under `molsysmt.configure` include:

- **`max_ram_usage`**: Maximum RAM threshold (default: 50% of detected physical system RAM) before switching from eager to chunked execution.
- **`chunk_size`**: Number of structures per chunk block (default: 100) during chunked execution.
- **`heavy_mode`**: Execution path control (`'auto'`, `'force'`, or `'off'`).
- **`emit_heavy_telemetry`**: Toggle for SMonitor progress and decision telemetry events (default: `True`).
- **`memory_pressure_threshold`**: RSS memory pressure warning threshold (default: `0.80`).
- **`show_all_capabilities`**: Filter available form conversions based on installed soft dependencies.

---

## Global and Contextual Configuration

Users can update parameters globally or apply temporary overrides using context managers:

```python
import molsysmt as msm

# 1. Global update
msm.configure.chunk_size = 500
msm.configure.heavy_mode = 'force'

# 2. Context manager override for a specific code block
with msm.configure.set(chunk_size=200, heavy_mode='auto'):
    center = msm.structure.get_center('system.h5msm')
```
