# SMonitor integration

MolSysMT uses SMonitor as the single diagnostics layer.

## Files

- `molsysmt/_smonitor.py`
- `molsysmt/_private/smonitor/catalog.py`
- `molsysmt/_private/smonitor/meta.py`

## Rules

- Emit through catalog entries only.
- Keep user messages explicit and helpful.
- Keep URLs in `meta.py` so hints remain consistent.
