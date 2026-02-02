# Dependency Management Architecture

MolSysMT uses a sophisticated **Decorator-based Lazy Loading** architecture to handle external dependencies. This ensures fast startup times, robustness against missing optional libraries, and introspection capabilities.

## 1. Core Principles

- **Zero-Cost Startup:** Importing `molsysmt` never triggers the import of a soft dependency (like `openmm`, `mdtraj`).
- **Single Source of Truth:** All dependency metadata is centralized in `molsysmt/config/dependencies.py`.
- **Runtime Validation:** The `@requires` decorator enforces availability just-in-time.
- **Lazy Discovery:** Form modules are only scanned and imported when accessed, allowing for dynamic capability filtering.

## 2. Configuration & Mapping

### Dependency Definitions (`molsysmt/config/dependencies.py`)

This file defines which libraries are `hard` (required) and `soft` (optional).

```python
dependencies = {
    'numpy': Dependency('numpy', 'hard', 'numpy', 'numpy'),
    'mdtraj': Dependency('mdtraj', 'soft', 'mdtraj', 'mdtraj'),
    # ...
}
```

### Form Directory Mapping

Crucially, this file also maps **Form Directories** to their required libraries. This enables the Lazy Loader to know that `mdtraj_Trajectory` needs `mdtraj` *without* opening the folder.

```python
form_dir_to_library = {
    'mdtraj_Trajectory': 'mdtraj',
    'openmm_Topology': 'openmm',
    # ...
}
```

**Developer Rule:** If you add a new form that depends on an external library, you **MUST** add it to this map.

## 3. The `@requires` Decorator

Located in `molsysmt.dependencies`, this decorator is the guardian of the codebase.

**Usage:**

```python
from molsysmt.dependencies import requires

@requires('mdtraj')
def to_mdtraj(item):
    import mdtraj # Safe lazy import
    ...
```

**Features:**
1.  **Validation:** Checks if the library is installed. Raises `LibraryNotFoundError` with a clear message if not.
2.  **Metadata:** Tags the function with `_dependencies`, allowing `msm.info()` (future) to show requirements.
3.  **Caching:** Optimizes checks to have negligible runtime overhead.

## 4. The Lazy Form Loader (`molsysmt.form`)

The `__init__.py` in `molsysmt/form` implements a custom dictionary (`_FormsDictionary`) that:
1.  **Does not import anything** at startup.
2.  When a form is requested (e.g., `convert(..., to_form='mdtraj.Trajectory')`):
    - Checks `form_dir_to_library`.
    - Checks `msm.config.show_all_capabilities`.
    - Checks if the required library is installed.
    - If all checks pass, it imports the module.
    - If filtering is active and lib is missing, the form remains "invisible".

## 5. Validation Script

We provide a script to enforce architectural rules:
`scripts/validate_dependencies.py`

**What it checks:**
- No top-level imports of soft dependencies (e.g., `import openmm` at module level).
- Scans the entire codebase (AST analysis).

**Exempt Zones:**
Some directories are exempt from the "Zero Soft Dependency" rule because they are dev tools or tests:
- `molsysmt/data/_make/`
- `molsysmt/tests/`
- `molsysmt/docs/generate_static_views/`
- `sandbox/`

## 6. How to Add a New Dependency

1.  **Register it:** Add it to `dependencies` in `molsysmt/config/dependencies.py`.
2.  **Map it:** If it has associated forms, add them to `form_dir_to_library`.
3.  **Use it:** Use `@requires('new_lib')` in your functions.
4.  **Import it:** Always import it **inside** the function/method.

## 7. Troubleshooting

- **"ModuleNotFoundError" vs "LibraryNotFoundError":**
    - `LibraryNotFoundError` means the system works: it detected the missing lib and warned you.
    - `ModuleNotFoundError` (for a soft dep) usually means a **Top-Level Import** leaked into the code. Run the validation script!

- **Form not showing up:**
    - Check if `show_all_capabilities` is False.
    - Check if it's mapped in `form_dir_to_library`.
    - Check the logs (debug level) for skipped forms.