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
    CATALOG["warnings"]["SelectionWarning"],
    extra=merge_extra(META, {"selection": selection}),
    package_root=PACKAGE_ROOT,
    meta=META,
)
```

## Guidance

- Keep user messages explicit and actionable.
- Keep hints concise and link to docs/issues when useful.
- Avoid hardcoded messages outside the catalog.

## Structural rejections

`MSM-ERR-STRUCT-003` retains the exception's structured `reason` and renders it
for user, developer, QA and agent audiences. Treat the reason as the explanation
of the violated contract. The shared hints cover geometry, dimensions and index
correspondence; atom/group/structure comparison advice is conditional on actually
comparing or merging systems. A single-system target-basis rejection must not be
interpreted as a request to match two molecular systems. Consumers should preserve
the native code and reason rather than translate the message locally.

For principal-axis degeneracy, distinguish the molecular-system
`structure_index` from the selected-array position and from a structure ID label.
For example, `[2, 0]` can reject source `structure_index 0` at selection position 1.
