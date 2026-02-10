# SMonitor Integration

MolSysMT uses SMonitor as the single diagnostics layer. All warnings and
errors must be emitted through the catalog.

## Required Files
- `molsysmt/_smonitor.py`
- `molsysmt/_private/smonitor/catalog.py`
- `molsysmt/_private/smonitor/meta.py`

## Rules
- Emit through catalog entries only.
- Use `molsysmt._private.smonitor.warn` for user warnings.
- Inherit from `CatalogException` for all errors.
- Keep user messages explicit and actionable.
- Keep URLs in `meta.py` for consistent hints.
- **Noise Control**: Use the `silence` list in `_smonitor.py` to suppress noisy third-party loggers (e.g., `pint`, `networkx`).

## Implementation
The diagnostic plumbing is centralized in `molsysmt/_private/smonitor/`.
- `emitter.py`: Defines the `DiagnosticBundle` instance (`bundle`) and exports `warn`, `warn_once`, and `resolve`.
- `exceptions.py`: Implementation of catalog-backed exceptions.
- `warnings.py`: Implementation of catalog-backed warnings.
