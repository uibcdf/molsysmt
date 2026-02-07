# Dependency Management System Specification

## 1. Motivation & Goals

MolSysMT integrates numerous external tools (OpenMM, MDTraj, etc.). The current dependency handling has several issues:
- **Zero-Cost Startup:** `import molsysmt` is now instantaneous and does not import soft dependencies.
- **Declarative Definition:** All dependencies are defined in `molsysmt/_depdigest.py`.
- **Robustness:** Functions fail gracefully at runtime with clear messages via `@dep_digest`.
- **Introspection:** Supports filtering capabilities based on `msm.config.show_all_capabilities`.

## 2. Architecture Components

### A. Configuration Source (`molsysmt/_depdigest.py`)
Defines the status of each library and maps form directories to libraries.

```python
LIBRARIES = { ... }
MAPPING = {
    'mdtraj_Trajectory': 'mdtraj',
    ...
}
```

### B. Dependency Manager (`depdigest`)
- `@dep_digest(library, when=None)`: The smart decorator (configured via `molsysmt/_depdigest.py`).
- `get_info('molsysmt')`: Returns a summary table of dependency status.

### C. Lazy Form Registry (`molsysmt.form`)
The `_dict_modules` is now a dynamic proxy (`_FormsDictionary`) that:
1.  Scans directories only when accessed.
2.  Uses `MAPPING` to check requirements before importing.
3.  Filters out missing capabilities if `msm.config.show_all_capabilities` is `False`.

## 3. Implementation Details

### Decorator Behavior
- Attaches `_dependencies` metadata to functions.
- Uses a cached `inspect.signature` for high-performance argument binding in conditional checks.

### Interaction with `@arg_digest`
`@dep_digest` must be placed **below** `@arg_digest` to work on normalized arguments.

## 4. Maintenance Protocol

### Moving Soft -> Hard
1. Update `type: 'hard'` in `molsysmt/_depdigest.py`.
2. (Optional) Move imports to top-level for minor performance gain.

### Moving Hard -> Soft
1. Move imports inside functions (Lazy).
2. Add `@dep_digest('lib')`.
3. Update `type: 'soft'` in `molsysmt/_depdigest.py`.
4. Ensure the form directory is mapped in `MAPPING`.

## 6. Exempt Zones (Dev Tools)



The following directories are exempt from the "Zero Soft Dependency" rule because they are development tools, tests, or data generation scripts intended for developers (who are assumed to have a full environment):



*   `molsysmt/data/_make/`

*   `molsysmt/docs/generate_static_views/`

*   `molsysmt/tests/`

*   `molsysmt/attic/`

*   `sandbox/`
