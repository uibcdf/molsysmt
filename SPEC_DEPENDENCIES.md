# Dependency Management System Specification

## 1. Motivation & Goals

MolSysMT integrates numerous external tools (OpenMM, MDTraj, etc.). The current dependency handling has several issues:
- **Zero-Cost Startup:** `import molsysmt` is now instantaneous and does not import soft dependencies.
- **Declarative Definition:** All dependencies are defined in `molsysmt/config/dependencies.py`.
- **Robustness:** Functions fail gracefully at runtime with clear messages via `@requires`.
- **Introspection:** Supports filtering capabilities based on `msm.config.show_all_capabilities`.

## 2. Architecture Components

### A. Configuration Source (`molsysmt.config.dependencies`)
Defines the status of each library and maps form directories to libraries.

```python
dependencies = { ... }
form_dir_to_library = {
    'mdtraj_Trajectory': 'mdtraj',
    ...
}
```

### B. Dependency Manager (`molsysmt.dependencies`)
- `check_dependency(name)`: Validates availability.
- `is_installed(name)`: Cached check.
- `@requires(library, when=None)`: The smart decorator.

### C. Lazy Form Registry (`molsysmt.form`)
The `_dict_modules` is now a dynamic proxy (`_FormsDictionary`) that:
1.  Scans directories only when accessed.
2.  Uses `form_dir_to_library` to check requirements before importing.
3.  Filters out missing capabilities if `msm.config.show_all_capabilities` is `False`.

## 3. Implementation Details

### Decorator Behavior
- Attaches `_dependencies` metadata to functions.
- Uses a cached `inspect.signature` for high-performance argument binding in conditional checks.

### Interaction with `@digest`
`@requires` must be placed **below** `@digest` to work on normalized arguments.

## 4. Maintenance Protocol

### Moving Soft -> Hard
1. Update `type: 'hard'` in `molsysmt/config/dependencies.py`.
2. (Optional) Move imports to top-level for minor performance gain.

### Moving Hard -> Soft
1. Move imports inside functions (Lazy).
2. Add `@requires('lib')`.
3. Update `type: 'soft'` in `molsysmt/config/dependencies.py`.
4. Ensure the form directory is mapped in `form_dir_to_library`.

## 6. Exempt Zones (Dev Tools)



The following directories are exempt from the "Zero Soft Dependency" rule because they are development tools, tests, or data generation scripts intended for developers (who are assumed to have a full environment):



*   `molsysmt/data/_make/`

*   `molsysmt/docs/generate_static_views/`

*   `molsysmt/tests/`

*   `molsysmt/attic/`

*   `sandbox/`
