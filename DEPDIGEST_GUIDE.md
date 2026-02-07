# DepDigest Guide (Canonical)

Source of truth for integrating and using **DepDigest** in this library.

Metadata
- Source repository: `depdigest`
- Source document: `standards/DEPDIGEST_GUIDE.md`
- Source version: `depdigest@0.1.1`
- Last synced: 2026-02-06

## What is DepDigest

DepDigest is a lightweight infrastructure library designed to manage **optional dependencies** and **lazy loading**. It ensures that heavy external packages are only checked and imported when strictly necessary, maintaining a "Zero-Cost Startup" for the host library.

## Why this matters in this library

- **Startup Performance**: Prevents accidental top-level imports of optional libraries.
- **Robustness**: Enforces availability at runtime with professional error messages.
- **Dynamic Discovery**: Supports lazy plugin/form registries that respond to user-defined visibility settings.
- **Auditability**: Provides tools to scan the codebase for "leaky" imports.

## 1. Required Configuration (`_depdigest.py`)

Create a file named `_depdigest.py` in your package root. DepDigest uses the module name of the decorated function to find this file automatically.

```python
# MyLibrary/_depdigest.py

# Define all external dependencies
LIBRARIES = {
    'numpy': {'type': 'hard', 'pypi': 'numpy'},
    'mdtraj': {'type': 'soft', 'pypi': 'mdtraj'},
    'openmm.unit': {'type': 'soft', 'pypi': 'openmm', 'conda': 'openmm'},
}

# Map sub-directories to their required library (for LazyRegistry)
MAPPING = {
    'mdtraj_Trajectory': 'mdtraj',
    'openmm_Topology': 'openmm.unit',
}

# Global visibility toggle
SHOW_ALL_CAPABILITIES = True

# Custom exception class (Recommended for professional APIs)
from .exceptions import MyLibraryNotFoundError
EXCEPTION_CLASS = MyLibraryNotFoundError
```

## 2. Core API for Developers

### 2.1 The `@dep_digest` Decorator
Resolved at runtime. It checks `is_installed(pypi_name)` before executing the function.

```python
from depdigest import dep_digest

@dep_digest('mdtraj')
def to_mdtraj(item):
    import mdtraj # Lazy import is MANDATORY
    ...
```

**Conditional Check**: Enforce the dependency only if a specific argument is passed.
```python
@dep_digest('openmm.unit', when={'to_form': 'openmm.unit'})
def convert(item, to_form):
    ...
```

### 2.2 The `LazyRegistry`
Acts as a dictionary. It only imports a sub-module if its dependency (defined in `MAPPING`) is installed or if `SHOW_ALL_CAPABILITIES` is `True`.

```python
# MyLibrary/plugins/__init__.py
from depdigest import LazyRegistry

registry = LazyRegistry(
    package_prefix='MyLibrary.plugins',
    directory='/path/to/plugins',
    attr_name='plugin_name' # Each plugin file must have a 'plugin_name' variable
)
```

## 3. Advanced Integration

### 3.1 Manual Configuration Registration
Useful for testing or dynamic plugin systems where a root `_depdigest.py` is not feasible.

```python
from depdigest import register_package_config, DepConfig

register_package_config('my_dynamic_pkg', DepConfig(
    libraries={'secret_lib': {'type': 'soft', 'pypi': 'secret'}},
    exception_class=ValueError
))
```

### 3.2 User Introspection
Expose a function to let users know their environment's status:

```python
from depdigest import get_info

def dependency_info():
    return get_info('MyLibrary')
```

## Required behavior (non-negotiable)

1.  **Lazy Imports**: Never import a soft dependency at the module top-level. Always inside the guarded function.
2.  **Package Identity**: Always use the importable package name as the key in `LIBRARIES` (e.g., `'openmm.unit'`).
3.  **Standardization**: Use `@dep_digest` even for internal utility functions that depend on optional tools.

## SMonitor Integration

DepDigest is instrumented with `@smonitor.signal(tags=["dependency"])`. Every dependency check and automated loading process is traceable in the breadcrumb trail.

---
*Document created on February 6, 2026, as the authority for DepDigest integration.*