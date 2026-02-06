# SMonitor Guide

Metadata
- Source repository: `smonitor`
- Source document: `standards/SMONITOR_GUIDE.md`
- Source version: `smonitor@0.10.0`
- Reference stack version: `MolSysMT 0.10.0`
- Target repository: `molsysmt`
- Last synced: 2026-02-06

## Purpose

SMonitor is the single diagnostics layer for the MolSys ecosystem. Libraries must
use the SMonitor catalog for warnings/errors and avoid hardcoded messages.

## Required files in each library

- `_smonitor.py`: runtime configuration + code templates.
- `_private/smonitor/catalog.py`: catalog entries (code/category/level/source).
- `_private/smonitor/meta.py`: metadata (docs/issues/api URLs).
- `_private/smonitor/__init__.py`: exports `CATALOG`, `META`, `PACKAGE_ROOT`.

## Emission rule (non-negotiable)

All warnings/errors must be emitted via the catalog:

```python
from smonitor.integrations import emit_from_catalog
from <library>._private.smonitor import CATALOG, META, PACKAGE_ROOT

emit_from_catalog(
    CATALOG["<entry_key>"],
    package_root=PACKAGE_ROOT,
    meta=META,
    extra={"key": "value"},
)
```

Do not write new hardcoded warning/exception strings in library code.

## Adding a new signal

1. Add an entry to `_private/smonitor/catalog.py`.
2. Add the code template to `_smonitor.py`.
3. Emit via `emit_from_catalog(...)`.
4. Add a focused test that asserts the emitted code/message.

## Message quality rules

- User messages must be explicit and actionable.
- Hints should include the most useful next step (docs/issues if relevant).
- Tone: helpful, neutral, and concise.

## Compatibility

Legacy exception/warning classes may remain, but must emit SMonitor events and
use catalog messages.
