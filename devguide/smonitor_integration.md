# SMonitor Integration

MolSysMT uses SMonitor as the single diagnostics layer. All warnings and
errors must be emitted through the catalog.

## Required Files
- `molsysmt/_smonitor.py`
- `molsysmt/_private/smonitor/catalog.py`
- `molsysmt/_private/smonitor/meta.py`

## Rules
- Emit through catalog entries only.
- Keep user messages explicit and actionable.
- Keep URLs in `meta.py` for consistent hints.

## Canonical Guide
See `SMONITOR_GUIDE.md` for required behavior and patterns.
