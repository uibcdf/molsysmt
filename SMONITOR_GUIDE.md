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
- `A/_private/smonitor/catalog.py`: Catalog entries (meta-data about each signal).
- `A/_private/smonitor/meta.py`: Project metadata (URLs for documentation and issues).
- `A/_private/smonitor/__init__.py`: Exports `CATALOG`, `META`, and `PACKAGE_ROOT`.

## 2. Initialization Protocol

In your library's `__init__.py`, ensure SMonitor is configured on import. This activates the "System Nervous System":

```python
from smonitor.integrations import ensure_configured
from ._private.smonitor import PACKAGE_ROOT

ensure_configured(PACKAGE_ROOT)
```

## 3. Emission via Catalog (Mandatory)

All diagnostic output must be driven by the catalog. **Never hardcode strings** in the scientific logic.

### Pattern:
```python
from smonitor.integrations import emit_from_catalog
from A._private.smonitor import CATALOG, META, PACKAGE_ROOT

emit_from_catalog(
    CATALOG["my_signal"],
    package_root=PACKAGE_ROOT,
    meta=META,
    extra={"param": value}, # Data for template interpolation
)
```

**Note**: When using `emit_from_catalog`, the message is automatically resolved from `_smonitor.py` based on the active profile (`user`, `dev`, `debug`, etc.).

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

## Required behavior (non-negotiable)

1.  **Zero String Hardcoding**: If it's a warning or error, it belongs in the catalog.
2.  **Lazy Diagnostics**: Do not perform expensive string formatting before calling `emit`. Pass raw data in `extra` and let SMonitor handle the interpolation.
3.  **Traceability First**: Use `@signal` generously in orchestration layers but avoid it in high-frequency tight loops.

---
*Document created on February 6, 2026, as the authority for SMonitor integration.*