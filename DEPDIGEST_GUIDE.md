<!--
SYNCHRONIZED MOLSYSSUITE GUIDE — DO NOT EDIT COMPONENT COPIES.
Canonical source: https://github.com/uibcdf/depdigest/blob/main/standards/DEPDIGEST_GUIDE.md
-->

# DepDigest Guide (Canonical)

Source of truth for integrating and using **DepDigest** in this library.

Metadata
- Source repository: `depdigest`
- Source document: `standards/DEPDIGEST_GUIDE.md`
- Source version: `depdigest@0.5.0-dev`
- Last synced: 2026-02-27

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
    "numpy": {"type": "hard", "pypi": "numpy"},
    "mdtraj": {"type": "soft", "pypi": "mdtraj"},
    "openmm.unit": {"type": "soft", "pypi": "openmm", "conda": "openmm"},
}

# Map sub-directories to their required library (for LazyRegistry)
MAPPING = {
    "mdtraj_Trajectory": "mdtraj",
    "openmm_Topology": "openmm.unit",
}

# Global visibility toggle
SHOW_ALL_CAPABILITIES = True

# Custom exception class (Recommended for professional APIs)
from .exceptions import MyLibraryNotFoundError

EXCEPTION_CLASS = MyLibraryNotFoundError
```

## 2. Core API for Developers

### 2.1 The `@dep_digest` Decorator
Resolved at runtime. It checks `is_installed(library_key)` before executing the function.
The optional `pypi` field is used for installation hints/messages.

```python
from depdigest import dep_digest


@dep_digest("mdtraj")
def to_mdtraj(item):
    import mdtraj  # Lazy import is MANDATORY

    ...
```

**Conditional Check**: Enforce the dependency only if a specific argument is passed.
```python
@dep_digest("openmm.unit", when={"to_form": "openmm.unit"})
def convert(item, to_form): ...
```

### 2.2 The `LazyRegistry`
Acts as a dictionary. It only imports a sub-module if its dependency (defined in `MAPPING`) is installed or if `SHOW_ALL_CAPABILITIES` is `True`.

```python
# MyLibrary/plugins/__init__.py
from depdigest import LazyRegistry

registry = LazyRegistry(
    package_prefix="MyLibrary.plugins",
    directory="/path/to/plugins",
    attr_name="plugin_name",  # Each plugin file must have a 'plugin_name' variable
)
```

Optional entry-point mode:

```python
registry = LazyRegistry(
    package_prefix="MyLibrary.plugins",
    directory="/unused",
    attr_name="plugin_name",
    discovery_mode="entry_points",
    entrypoint_group="MyLibrary.plugins",
)
```

## 3. Advanced Integration

### 3.1 Manual Configuration Registration
Useful for testing or dynamic plugin systems where a root `_depdigest.py` is not feasible.

```python
from depdigest import register_package_config, DepConfig

register_package_config(
    "my_dynamic_pkg",
    DepConfig(
        libraries={"secret_lib": {"type": "soft", "pypi": "secret"}},
        exception_class=ValueError,
    ),
)
```

You can remove or scope these overrides:

```python
from depdigest import unregister_package_config, temporary_package_config

unregister_package_config("my_dynamic_pkg")

with temporary_package_config("my_dynamic_pkg", DepConfig(libraries={})):
    ...
```

### 3.2 User Introspection
Expose a function to let users know their environment's status:

```python
from depdigest import get_info


def dependency_info():
    return get_info("MyLibrary")
```

Machine-readable status is also available:

```python
payload = get_info("MyLibrary", format="dict")  # or format='json'
```

`dict/json` outputs follow schema `depdigest.get_info@1.0`.

### 3.3 Architecture Audit in CI
Use the audit command to detect top-level imports of soft dependencies:

```bash
depdigest audit --src-root MyLibrary --soft-deps mdtraj,openmm
```

## Required behavior (non-negotiable)

### Optional original engines

Guard the narrowest external backend and keep imports inside the guarded function.
Native implementations, persisted results, and web-service reachability are distinct
capabilities. A provider's absence must not silently switch the requested method.

Declare installation routes explicitly. `pypi: None` and `conda: None` disable their
respective routes; omission retains legacy defaults. Use `channel` for the declared
Conda channel. Diagnostics and `get_info` honor disabled routes and the channel.

Executable dependencies use a logical key with `kind: 'executable'`, optionally
`executable: 'command-or-path'`. Their checks use the current PATH and permissions,
not Python import discovery, and never run or install the engine. For example:

```python
LIBRARIES = {
    "pocketeer": {"type": "soft", "pypi": "pocketeer", "conda": None},
    "fpocket": {
        "type": "soft",
        "kind": "executable",
        "executable": "fpocket",
        "pypi": None,
        "conda": "fpocket",
        "channel": "conda-forge",
    },
}
```

`@dep_digest` and `LazyRegistry` use the same availability rules. Module keys remain
import names for `kind: 'python'` (the default); executable keys are capability names.
Availability does not certify transitive imports, versions, ABI, service state, or
scientific correctness. Preserve those failures at the consumer boundary and test
the adapter against a direct upstream run. Full adoption examples are in
`docs/content/user/optional-engines.md` in the DepDigest repository.

1.  **Lazy Imports**: Never import a soft dependency at the module top-level. Always inside the guarded function.
2.  **Package Identity**: Use the importable package name for Python keys in `LIBRARIES` (e.g., `'openmm.unit'`); executable entries use a capability key and declare `kind: 'executable'`.
3.  **Standardization**: Use `@dep_digest` even for internal utility functions that depend on optional tools.

## SMonitor Integration

DepDigest is instrumented with `@smonitor.signal(tags=["dependency"])`. Every dependency check and automated loading process is traceable in the breadcrumb trail.

---
*Document created on February 6, 2026, as the authority for DepDigest integration. Updated on September 30, 2026.*
