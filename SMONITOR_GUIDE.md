# SMonitor Guide (Canonical)

Source of truth for integrating **SMonitor** in this library.

Metadata
- Source repository: `smonitor`
- Source document: `standards/SMONITOR_GUIDE.md`
- Source version: `smonitor@0.10.0`
- Last synced: 2026-02-06

## What is SMonitor

SMonitor is the diagnostics layer for the MolSys ecosystem. It centralizes warnings, errors, and developer signals so that user messages are consistent, actionable, and traceable across libraries.

SMonitor is not a logging wrapper. It is the single source of truth for message templates, severity, categories, and structured metadata.

## Why this matters in this library

- Users see clear, consistent messages.
- Developers and QA can trace the exact signal code across tools.
- Agents can parse structured events and automate fixes.

## Required files in this library

If the library is named `A` and the source code lives in the `A/` directory at the repository root, these paths are relative to the repository root:

- `_smonitor.py`: runtime configuration and code templates.
- `A/_private/smonitor/catalog.py`: catalog entries (code/category/level/source).
- `A/_private/smonitor/meta.py`: metadata (docs/issues/api URLs).
- `A/_private/smonitor/__init__.py`: exports `CATALOG`, `META`, `PACKAGE_ROOT`.

## Required behavior (non-negotiable)

All warnings and errors must be emitted through the catalog. Do not write new hardcoded warning/exception strings in library code.

## Minimum initialization (required)

In the library `__init__.py`, ensure SMonitor is configured on import:

```python
from smonitor.integrations import ensure_configured as _ensure_smonitor_configured
from ._private.smonitor import PACKAGE_ROOT as _SMONITOR_PACKAGE_ROOT

_ensure_smonitor_configured(_SMONITOR_PACKAGE_ROOT)
```

## Minimal integration example

Catalog entry (`A/_private/smonitor/catalog.py`):

```python
CATALOG = {
    "missing_dependency": {
        "code": "A-MISSING-DEPENDENCY",
        "source": "A.dependencies",
        "category": "dependency",
        "level": "ERROR",
    }
}
```

Code templates (`A/_smonitor.py`):

```python
CODES = {
    "A-MISSING-DEPENDENCY": {
        "title": "Missing dependency",
        "user_message": "Optional dependency '{library}' was not found.",
        "user_hint": "Install '{library}' to enable this feature.",
        "dev_message": "Missing optional dependency '{library}' in '{caller}'.",
        "dev_hint": "Guard optional imports and document the dependency.",
    }
}
```

Emission from code:

```python
from smonitor.integrations import emit_from_catalog
from A._private.smonitor import CATALOG, META, PACKAGE_ROOT

emit_from_catalog(
    CATALOG["missing_dependency"],
    package_root=PACKAGE_ROOT,
    meta=META,
    extra={"library": lib_name, "caller": caller},
)
```

## Signal contract and required extras

If the signal needs context, add it to `SIGNALS` in `_smonitor.py` and enforce it:

```python
SIGNALS = {
    "A.missing_dependency": {
        "extra_required": ["library", "caller"],
    }
}
```

If `extra_required` is missing, SMonitor can fail validation or emit incomplete messages. Treat missing extras as a bug.

## Metadata (META) and URLs

`A/_private/smonitor/meta.py` should expose URLs used in hints:

```python
DOC_URL = "https://..."
ISSUES_URL = "https://..."
API_URL = "https://..."
```

These are merged into `META` and passed to emissions so templates can include `{doc_url}` and `{issues_url}`.

## Naming conventions

- Catalog keys: short and stable (e.g., `missing_dependency`, `not_digested_argument`).
- Codes: `LIB-NAME-UPPER-SIGNAL` (e.g., `MOLSYSVIEWER-VIEWER-INIT-FAILED`).
- Sources: dotted paths to feature area (e.g., `molsysviewer.loaders.molsysmt`).

## Compatibility with legacy exceptions

Legacy classes may remain, but must emit SMonitor events and use catalog messages.

Example wrapper:

```python
from A._private.smonitor_emit import message_from_catalog

class ArgumentError(Exception):
    def __init__(self, argument, caller=None, message=None):
        default_message = f"Error in {caller} due to {argument}."
        full_message = message_from_catalog(
            "argument_error",
            extra={"argument": argument, "caller": caller, "detail": message},
            default_message=default_message,
        )
        super().__init__(full_message)
```

## Configuration and runtime overrides

- Default configuration is in `_smonitor.py`.
- Users or agents can override at runtime:

```python
import smonitor
smonitor.configure(profile="dev", level="INFO", event_buffer_size=200)
```

Runtime configuration always takes precedence over `_smonitor.py`.

Profiles typically used:
- `user`: default, minimal noise.
- `dev`: more context, tracebacks.
- `qa`: similar to dev but stable for test runs.
- `agent`: machine-readable emphasis.
- `debug`: full verbosity.

## Testing pattern

Use the event buffer to assert emissions:

```python
import smonitor
smonitor.configure(event_buffer_size=50)

# call code that should emit
report = smonitor.report()
assert report["events_buffered"] >= 1
```

You can also assert on specific `code` values and message fragments.

## Common mistakes

- Adding a catalog entry but forgetting the `CODES` template.
- Emitting without required `extra` fields.
- Hardcoding messages directly in exceptions or warnings.
- Forgetting to call `ensure_configured(PACKAGE_ROOT)` on import.

## Message quality rules

- User messages must be explicit and actionable.
- Hints should include the most useful next step (docs/issues if relevant).
- Tone: helpful, neutral, concise.
