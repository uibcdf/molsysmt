# Dependency Management Architecture

MolSysMT uses a sophisticated **Decorator-based Lazy Loading** architecture to handle external dependencies. This ensures fast startup times, robustness against missing optional libraries, and introspection capabilities.

## 1. Core Principles

- **Zero-Cost Startup:** Importing `molsysmt` never triggers the import of a soft dependency (like `openmm`, `mdtraj`).
- **Single Source of Truth:** All dependency metadata is centralized in `molsysmt/_depdigest.py`.
- **Runtime Validation:** The `@dep_digest` decorator enforces availability just-in-time.
- **Lazy Discovery:** Form modules are only scanned and imported when accessed, allowing for dynamic capability filtering.

## 2. Configuration & Mapping

### Dependency Definitions (`molsysmt/_depdigest.py`)

This file defines which libraries are `hard` (required) and `soft` (optional).

```python
LIBRARIES = {
    'numpy': {'type': 'hard', 'pypi': 'numpy'},
    'mdtraj': {'type': 'soft', 'pypi': 'mdtraj'},
    # ...
}
```

### Form Directory Mapping

Crucially, this file also maps **Form Directories** to their required libraries. This enables the Lazy Loader to know that `mdtraj_Trajectory` needs `mdtraj` *without* opening the folder.

```python
MAPPING = {
    'mdtraj_Trajectory': 'mdtraj',
    'openmm_Topology': 'openmm',
    # ...
}
```

**Developer Rule:** If you add a new form that depends on an external library, you **MUST** add it to this map.

## 3. The `@dep_digest` Decorator

This decorator is provided by the `depdigest` package and configured by
`molsysmt/_depdigest.py`.

**Usage:**

```python
from depdigest import dep_digest

@dep_digest('mdtraj')
def to_mdtraj(item):
    import mdtraj # Safe lazy import
    ...
```

**Features:**
1.  **Validation:** Checks if the library is installed. Raises `LibraryNotFoundError` with a clear message if not.
2.  **Metadata:** Tags the function with `_dependencies` for introspection and tooling.
3.  **Caching:** Optimizes checks to have negligible runtime overhead.

## 4. The Lazy Form Loader (`molsysmt.form`)

The `__init__.py` in `molsysmt/form` implements a custom dictionary (`_FormsDictionary`) that:
1.  **Does not import anything** at startup.
2.  When a form is requested (e.g., `convert(..., to_form='mdtraj.Trajectory')`):
    - Checks `MAPPING`.
    - Checks `msm.config.show_all_capabilities`.
    - Checks if the required library is installed.
    - If all checks pass, it imports the module.
    - If filtering is active and lib is missing, the form remains "invisible".

## 5. Validation Script

We provide a script to enforce architectural rules:
`devtools/scripts/validate_dependencies.py`

**What it checks:**
- No top-level imports of soft dependencies (e.g., `import openmm` at module level).
- Scans the entire codebase (AST analysis).

**Exempt Zones:**
Some directories are exempt from the "Zero Soft Dependency" rule because they are dev tools or tests:
- `molsysmt/data/_make/`
- `tests/`
- `molsysmt/docs/generate_static_views/`
- `sandbox/`

## 6. Integration Testing

To verify the runtime behavior of the dependency system (filtering, mocking), use:

```bash
pytest tests/test_dependencies_architecture.py
```

## 7. User Introspection

Users can check the status of the MolSysMT ecosystem at any time using:

```python
import molsysmt as msm
msm.supported.dependencies()
```

This returns a Pandas-formatted table showing which libraries are installed, whether they are hard or soft dependencies, and the commands to install them if missing.

## 8. How to Add a New Dependency

1.  **Register it:** Add it to `LIBRARIES` in `molsysmt/_depdigest.py`.
2.  **Map it:** If it has associated forms, add them to `MAPPING`.
3.  **Use it:** Use `@dep_digest('new_lib')` in your functions.
4.  **Import it:** Always import it **inside** the function/method.

## 7. Troubleshooting

- **"ModuleNotFoundError" vs "LibraryNotFoundError":**
    - `LibraryNotFoundError` means the system works: it detected the missing lib and warned you.
    - `ModuleNotFoundError` (for a soft dep) usually means a **Top-Level Import** leaked into the code. Run the validation script!

- **Form not showing up:**
    - Check if `show_all_capabilities` is False.
    - Check if it's mapped in `MAPPING`.
    - Check the logs (debug level) for skipped forms.
