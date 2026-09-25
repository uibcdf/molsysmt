(user-foundations-governance-configuration-options)=
# Configuration Options

MolSysMT provides a centralized configuration manager, **`molsysmt.configure`**, allowing users and workflows to customize execution defaults globally or contextually.

---

## Comprehensive Overview of Configuration Parameters

All global options are attributes of `molsysmt.configure`:

### 1. Memory Management & Heavy Execution
- **`max_ram_usage`**: Maximum RAM threshold (default: 50% of detected physical system RAM) before switching from eager to chunked execution.
- **`chunk_size`**: Default number of structures per chunk block (default: 100) during chunked execution.
- **`heavy_mode`**: Execution path control (`'auto'`, `'force'`, or `'off'`).
- **`memory_pressure_threshold`**: RSS memory pressure warning threshold (default: `0.80`).
- **`chunk_memory_fraction`**: Maximum safe fraction of `max_ram_usage` allocated to a single chunk block (default: `0.10`).

### 2. Native CPU Parallelization
- **`parallel_mode`**: Thread execution policy (`'auto'`, `True`, or `False`).
- **`num_threads`**: Thread pool size (`-1` uses all available physical CPU cores, or a positive integer).
- **`set_parallelization(parallel="auto", num_threads=-1)`**: Convenience function to update parallel settings.

### 3. Selection Syntaxes & Custom Shortcuts
- **`selection_shortcuts`**: Dictionary defining custom query aliases (e.g. `'backbone'`, `'heavy atoms'`, `'solvent'`). Users can register custom selection shortcuts for domain-specific workflows.

### 4. Visibility & Ecosystem Capabilities
- **`show_all_capabilities`**: Boolean flag (`True`/`False`). When `True`, MolSysMT exposes all supported forms; when `False`, it filters available forms based on installed soft dependencies.

### 5. Molecular Mechanics & Viewer Defaults
- **`default_attribute`**: Dictionary specifying default parameters for forcefields (`'AMBER14'`), water models (`'TIP3P'`), integrators (`'Langevin'`), and compute platforms (`'CPU'`). GPU platforms must be requested explicitly.
- **`default_viewer`**: Default 3D visualization backend (default: `'MolSysViewer'`).

### 6. Backend Control & Telemetry
- **`silence_backend_stdout`**: Suppresses unflagged C-level stdout printouts from third-party libraries (e.g. MDTraj DCD reader).
- **`emit_heavy_telemetry`**: Enables SMonitor progress and decision telemetry events (default: `True`).

---

## Programmatic Usage & Context Managers

```python
import molsysmt as msm

# 1. Inspecting current configuration
print(msm.configure.chunk_size)
print(msm.configure.max_ram_usage)

# 2. Updating global settings
msm.configure.chunk_size = 500
msm.configure.heavy_mode = 'force'

# 3. Contextual override for a specific code block
with msm.configure.set(chunk_size=200, heavy_mode='auto'):
    center = msm.structure.get_center('system.h5msm')
```
