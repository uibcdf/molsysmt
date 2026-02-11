# SMonitor Guide (Canonical)

Source of truth for integrating and using **SMonitor** in this library.

Metadata
- Source repository: `smonitor`
- Source document: `standards/SMONITOR_GUIDE.md`
- Source version: `smonitor@0.10.0`
- Last synced: 2026-02-06

## What is SMonitor

SMonitor is the diagnostics layer for the UIBCDF ecosystem. It centralizes warnings, errors, and developer signals so that user messages are consistent, actionable, and traceable across libraries.

SMonitor is not just a logging wrapper; it is a **Signal Orchestrator** that decouples event emission from message presentation.

## Why this matters in this library

- **Consistency**: Users see clear, helpful messages formatted as cards.
- **Traceability**: Developers can see the "Breadcrumb" trail across libraries.
- **AI-Ready**: Agents can parse structured events via the `agent` profile.

## 1. Required Configuration Structure

If the library is named `A`, the following files must exist relative to the repository root:

- `_smonitor.py`: Runtime configuration and message templates (CODES).

Example `_smonitor.py`:
```python
PROFILE = "user"

SMONITOR = {
    "level": "WARNING",
    "trace_depth": 3,
    "capture_warnings": True,
    "capture_logging": True,
    "theme": "plain",
    "silence": ["pint", "networkx"], # Noisy loggers to ignore
}
```
- `A/_private/smonitor/catalog.py`: Catalog entries (meta-data about each signal).
- `A/_private/smonitor/meta.py`: Project metadata (URLs for documentation and issues).
- `A/_private/smonitor/__init__.py`: Exports `CATALOG`, `META`, and `PACKAGE_ROOT`.

### 1.1 Single Source of Truth for Templates

`CODES` and `SIGNALS` must be resolved from exactly one authoritative place.

Recommended pattern:
- define `CATALOG`, `CODES`, and `SIGNALS` in `A/_private/smonitor/catalog.py`;
- in `_smonitor.py`, import them from `A._private.smonitor.catalog`.

This avoids drift where emitted catalog codes exist but template messages are missing at runtime.

## 2. Initialization Protocol

In your library's `__init__.py`, ensure SMonitor is configured on import. This activates the "System Nervous System":

```python
from smonitor.integrations import ensure_configured
from ._private.smonitor import PACKAGE_ROOT

ensure_configured(PACKAGE_ROOT)
```

## 3. Emission via Catalog (Mandatory)

All diagnostic output must be driven by the catalog. **Never hardcode strings** in the scientific logic.

### 3.1. Standard Warning Helper
Use the `DiagnosticBundle` to create consistent `warn` and `warn_once` helpers in your library's `_private/smonitor/emitter.py`:

```python
# A/_private/smonitor/emitter.py
from smonitor.integrations import DiagnosticBundle
from . import CATALOG, META, PACKAGE_ROOT

bundle = DiagnosticBundle(CATALOG, META, PACKAGE_ROOT)
warn = bundle.warn
warn_once = bundle.warn_once
resolve = bundle.resolve
```

### 3.2. Exceptions
All custom exceptions must inherit from `CatalogException` (provided by `smonitor.integrations`). This ensures messages are automatically hydrated from the catalog.

```python
# A/_private/smonitor/exceptions.py
from smonitor.integrations import CatalogException
from . import CATALOG, META

class MyLibException(CatalogException):
    def __init__(self, **kwargs):
        super().__init__(catalog=CATALOG, meta=META, **kwargs)

class ArgumentError(MyLibException):
    catalog_key = "ArgumentError"
    # ... logic to prepare extra dict ...
```

### 3.3. Warnings
Similarly, use `CatalogWarning` for warning classes:

```python
# A/_private/smonitor/warnings.py
from smonitor.integrations import CatalogWarning
from .emitter import bundle

class MyLibWarning(CatalogWarning):
    # ... setup catalog and meta ...
```

**Note**: The raw `emit_from_catalog` function is still available but `DiagnosticBundle` is the preferred high-level interface.

### 3.4 Emission Failures Must Not Be Silenced

Do not swallow diagnostics emission errors with `except Exception: pass`.

If emission fails in non-critical paths:
- fallback to a plain Python warning/log line;
- keep enough context (`caller`, signal key, exception text) for debugging.

Silencing emission failures causes loss of traceability and empty/noisy diagnostics in downstream libraries.

## 4. Telemetry with `@signal`

To enable execution traceability (breadcrumbs), decorate all major API entry points and internal orchestration functions.

```python
from smonitor import signal

@signal(tags=["topology"])
def get_atoms(molecular_system, selection="all"):
    ...
```

**Benefits**:
- On error, SMonitor reports the full call chain: `[A.api_func] -> [B.internal_logic] -> [ERROR]`.
- Performance telemetry can be enabled globally without changing the code.

## 5. Signal Contracts

Enforce structured data by defining required fields in `_smonitor.py`:

```python
SIGNALS = {
    "A.select": {
        "extra_required": ["selection"],
    }
}
```

Missing fields will trigger warnings or errors in `dev` and `qa` profiles, ensuring diagnostic quality.

## 6. Noise Control

SMonitor captures all exceptions by default as `ERROR`. For functions that perform exploratory checks (e.g., "is this string a unit?"), this creates log noise.

### Exploratory Functions
Use `exception_level="DEBUG"` in the `@signal` decorator to silence expected failures in normal operation.

```python
@signal(tags=["check"], exception_level="DEBUG")
def is_valid_format(data):
    # If this raises, it will be logged as DEBUG, not ERROR
    ...
```

### Assertive Parsing
For functions that *must* succeed (e.g., "parse this unit"), keep the default `ERROR` level. If a user provides malformed input where a valid one is expected, it *is* an error.

## Required behavior (non-negotiable)

1.  **Zero String Hardcoding**: If it's a warning or error, it belongs in the catalog.
2.  **Lazy Diagnostics**: Do not perform expensive string formatting before calling `emit`. Pass raw data in `extra` and let SMonitor handle the interpolation.
3.  **Traceability First**: Use `@signal` generously in orchestration layers but avoid it in high-frequency tight loops.
4.  **Template Wiring Integrity**: Every emitted catalog code must have a matching template in the active `_smonitor.py` configuration.
5.  **No Silent Emission Failures**: Never hide failed catalog emissions without an explicit fallback diagnostic.

---
*Document created on February 6, 2026, as the authority for SMonitor integration.*
