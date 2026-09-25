# SMonitor integration

MolSysMT uses **SMonitor** to centralize warnings, errors, and structured
telemetry. Catalogs define message content, and code emits through the catalog
entries.

## Files

- `molsysmt/_smonitor.py`
- `molsysmt/_private/smonitor/catalog.py`
- `molsysmt/_private/smonitor/meta.py`

## Emission pattern

```python
from smonitor.integrations import emit_from_catalog, merge_extra
from molsysmt._private.smonitor import CATALOG, META, PACKAGE_ROOT

emit_from_catalog(
    CATALOG["molsysmt.warning.selection_ambiguous"],
    extra=merge_extra(META, {"selection": selection}),
    package_root=PACKAGE_ROOT,
    meta=META,
)
```

## Guidance

- Keep user messages explicit and actionable.
- Keep hints concise and link to docs/issues when useful.
- Avoid hardcoded messages outside the catalog.
