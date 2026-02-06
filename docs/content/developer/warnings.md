# MolSysMT Warning Catalog (via smonitor)

MolSysMT warnings are defined and emitted through **smonitor catalogs**. This
ensures consistent messages, profiles, and metadata across the entire ecosystem.

---

## 1) Catalog-driven design

Warnings and errors are defined in:

- `molsysmt/_private/smonitor/catalog.py`
- `molsysmt/_private/smonitor/meta.py`

The catalog holds message templates for each profile. Metadata provides URLs
used in hints (docs, API, issues).

---

## 2) Example catalog entry

```python
"molsysmt.warning.selection_ambiguous": {
    "code": "MSM-W010",
    "level": "WARNING",
    "title": "Selection ambiguous",
    "category": "selection",
    "user_message": "Selection {selection} is ambiguous.",
    "user_hint": "Use a more specific selection. Docs: {doc_url}",
    "dev_message": "Selection {selection} is ambiguous.",
    "dev_hint": "Provide explicit selectors. Docs: {doc_url}",
    "extra_required": ["selection"],
}
```

---

## 3) Emitting a warning

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

The catalog entry defines **what** to say; the caller only provides context.

---

## 4) Message quality rules

- Make the **user message explicit** and actionable.
- Use **hints** to point to fixes, docs, or issue tracker.
- Avoid blaming language; be helpful and concise.

---

## 5) Deprecations and legacy categories

If legacy warning classes still exist, they should map to catalog entries and
emit through smonitor. Avoid new hardcoded warning messages.

---

## 6) Testing warnings

Enable event buffering and assert on the resulting events:

```python
import smonitor

smonitor.configure(event_buffer_size=50)
# call code that emits
report = smonitor.report()
assert report["events_buffered"] >= 1
```
