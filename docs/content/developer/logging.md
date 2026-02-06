# MolSysMT Diagnostics and Logging (via smonitor)

MolSysMT routes **warnings, errors, and structured diagnostics** through `smonitor`.
This replaces the older `logging_setup.py`-based redirection and keeps all
signal handling consistent across the ecosystem.

---

## 1) Overview

- `smonitor` is the single control point for diagnostics.
- MolSysMT defines its catalog and metadata under `molsysmt/_private/smonitor/`.
- Project defaults are declared in `molsysmt/_smonitor.py`.
- Runtime configuration always wins: users can call `smonitor.configure(...)`.

---

## 2) Where configuration lives

**Package root:** `molsysmt/_smonitor.py`

```python
PROFILE = "user"

SMONITOR = {
    "level": "WARNING",
    "trace_depth": 2,
    "capture_warnings": True,
    "capture_logging": True,
    "capture_exceptions": True,
    "theme": "plain",
}
```

---

## 3) Where catalog and metadata live

**Catalog:** `molsysmt/_private/smonitor/catalog.py`

- `CATALOG`: message definitions and hints
- `CODES`: mapping for codes to catalog entries
- `SIGNALS`: contracts for sources and required extras

**Metadata:** `molsysmt/_private/smonitor/meta.py`

- `DOC_URL`, `ISSUES_URL`, `API_URL` for consistent link injection

---

## 4) Emitting warnings and errors

MolSysMT should emit diagnostics through the catalog. Typical flow:

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

If a warning or exception helper is provided in MolSysMT, it should **only**
wrap this emission logic (no hardcoded messages).

---

## 5) Runtime overrides (user control)

Users can tailor the experience without touching MolSysMT internals:

```python
import smonitor

smonitor.configure(profile="dev", level="INFO", event_buffer_size=200)
```

---

## 6) Testing diagnostics

In tests, you can enable buffering and inspect emitted events:

```python
import smonitor

smonitor.configure(event_buffer_size=100)
# call code that emits
report = smonitor.report()
assert report["events_buffered"] > 0
```

---

## 7) Legacy note

Older logging redirection via `logging.captureWarnings(...)` is now considered
legacy. Keep it only for backward compatibility and migrate to smonitor-based
emission.
