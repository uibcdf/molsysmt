# SMonitor Guide (Canonical)

Source of truth for integrating and using **SMonitor** in this library.

Metadata
- Source repository: `smonitor`
- Source document: `standards/SMONITOR_GUIDE.md`
- Source version: `smonitor@0.11.5`
- Last synced: 2026-03-10

## What is SMonitor

SMonitor is the diagnostics layer for the UIBCDF ecosystem. It centralizes warnings, errors, and developer signals so that user messages are consistent, actionable, and traceable across libraries.

SMonitor is not just a logging wrapper; it is a **Signal Orchestrator** that decouples event emission from message presentation.

## Why this matters in this library

- **Consistency**: Users see clear, helpful messages formatted as cards.
- **Traceability**: Developers can see the "Breadcrumb" trail across libraries.
- **AI-Ready**: Agents can parse structured events via the `agent` profile.

## Integration levels

Treat this guide in three layers:

1. **Mandatory**
   - required for a correct SMonitor integration in any sibling library.
2. **Recommended**
   - expected for modern QA/support readiness.
3. **Advanced / CI-support**
   - valuable once the mandatory and recommended layers are already in place.

If time is constrained, implement in that order.

## Minimum modern integration recipe

At minimum, a sibling library should have:

1. `_smonitor.py` plus private catalog/meta files.
2. `ensure_configured(PACKAGE_ROOT)` in package initialization.
3. catalog-driven emission via `DiagnosticBundle` / catalog exceptions and warnings.
4. `@signal` on public orchestration entry points.
5. `context_extra(...)` for repeated structured diagnostic fields.
6. one smoke test covering config + bundle export.

## 1. Required Configuration Structure

If the library package is named `mylib`, the following files must exist relative to the repository root:

- `_smonitor.py`: Runtime configuration and message templates (CODES).

Example `_smonitor.py`:
```python
PROFILE = "user"

SMONITOR = {
    "level": "WARNING",
    "trace_depth": 3,
    "capture_warnings": True,
    "capture_logging": True,
    "theme": "plain",
    "silence": ["pint", "networkx"], # Noisy loggers to ignore
}
```
- `mylib/_private/smonitor/catalog.py`: Catalog entries (meta-data about each signal).
- `mylib/_private/smonitor/meta.py`: Project metadata (URLs for documentation and issues).
- `mylib/_private/smonitor/__init__.py`: Exports `CATALOG`, `META`, and `PACKAGE_ROOT`.

### 1.1 Single Source of Truth for Templates

`CODES` and `SIGNALS` must be resolved from exactly one authoritative place.

Recommended pattern:
- define `CATALOG`, `CODES`, and `SIGNALS` in `mylib/_private/smonitor/catalog.py`;
- in `_smonitor.py`, import them from `mylib._private.smonitor.catalog`.

This avoids drift where emitted catalog codes exist but template messages are missing at runtime.

## 2. Initialization Protocol

Level: **Mandatory**

In your library's `__init__.py`, ensure SMonitor is configured on import. This activates the "System Nervous System":

```python
from smonitor.integrations import ensure_configured
from ._private.smonitor import PACKAGE_ROOT

ensure_configured(PACKAGE_ROOT)
```

## 3. Emission via Catalog (Mandatory)

Level: **Mandatory**

All diagnostic output must be driven by the catalog. **Never hardcode strings** in the scientific logic.

### 3.1. Standard Warning Helper
Use the `DiagnosticBundle` to create consistent `warn` and `warn_once` helpers in your library's `_private/smonitor/emitter.py`:

```python
# mylib/_private/smonitor/emitter.py
from smonitor.integrations import DiagnosticBundle
from . import CATALOG, META, PACKAGE_ROOT

bundle = DiagnosticBundle(CATALOG, META, PACKAGE_ROOT)
warn = bundle.warn
warn_once = bundle.warn_once
resolve = bundle.resolve
```

### 3.2. Exceptions
All custom exceptions must inherit from `CatalogException` (provided by `smonitor.integrations`). This ensures messages are automatically hydrated from the catalog.

```python
# mylib/_private/smonitor/exceptions.py
from smonitor.integrations import CatalogException
from . import CATALOG, META

class MyLibException(CatalogException):
    def __init__(self, **kwargs):
        super().__init__(catalog=CATALOG, meta=META, **kwargs)

class ArgumentError(MyLibException):
    catalog_key = "ArgumentError"
    # ... logic to prepare extra dict ...
```

### 3.3. Warnings
Similarly, use `CatalogWarning` for warning classes:

```python
# mylib/_private/smonitor/warnings.py
from smonitor.integrations import CatalogWarning
from .emitter import bundle

class MyLibWarning(CatalogWarning):
    # ... setup catalog and meta ...
```

**Note**: The raw `emit_from_catalog` function is still available but `DiagnosticBundle` is the preferred high-level interface.

### 3.4 Emission Failures Must Not Be Silenced

Do not swallow diagnostics emission errors with `except Exception: pass`.

If emission fails in non-critical paths:
- fallback to a plain Python warning/log line;
- keep enough context (`caller`, signal key, exception text) for debugging.

Silencing emission failures causes loss of traceability and empty/noisy diagnostics in downstream libraries.

## 4. Telemetry with `@signal`

Level: **Recommended**

To enable execution traceability (breadcrumbs), decorate all major API entry points and internal orchestration functions.

```python
from smonitor import signal

@signal(tags=["topology"])
def get_atoms(molecular_system, selection="all"):
    ...
```

**Benefits**:
- On error, SMonitor reports the full call chain: `[mylib.api_func] -> [otherlib.internal_logic] -> [ERROR]`.
- Performance telemetry can be enabled globally without changing the code.

## 5. Signal Contracts

Level: **Recommended**

Enforce structured data by defining required fields in `_smonitor.py`:

```python
SIGNALS = {
    "mylib.select": {
        "extra_required": ["selection"],
    }
}
```

Missing fields will trigger warnings or errors in `dev` and `qa` profiles, ensuring diagnostic quality.

## 5.1 Structured Signal Context and Profiling

Level: **Recommended**

Recent pre-1.0 stabilization work added several profiling and machine-diagnostics capabilities that integrators should use deliberately:

- `@signal(..., extra_factory=...)` can attach structured per-call context without emitting a separate warning or error event.
- `report()` now exposes `timings_by_tag` in addition to timings by function and module.
- `slow_signal_ms` and `slow_signal_level` enable opt-in slow-call events (`SMONITOR-SIGNAL-SLOW`) for developer and QA workflows.

Recommended usage:

```python
from smonitor import signal

@signal(
    tags=["api", "selection"],
    extra_factory=lambda args, kwargs: {"selection": kwargs.get("selection")},
)
def get_atoms(molecular_system, selection="all"):
    ...
```

These features are intended for observability and QA; they should remain opt-in and must not flood end-user output by default.

## 5.2 Canonical Structured Context Helper

Level: **Recommended**

For library-generated diagnostics, prefer `smonitor.integrations.context_extra(...)` when building repeated `extra` payloads.

```python
from smonitor.integrations import context_extra, emit_from_catalog

emit_from_catalog(
    CATALOG["warnings"]["DownloadWarning"],
    extra=context_extra(
        caller="mylib.form.file_pdb.download",
        resource="181l.pdb",
        provider="RCSB",
        operation="download",
        extra={"attempt": 2, "retries": 5},
    ),
)
```

Use this helper for stable shared keys such as `caller`, `form`, `requested_attribute`, `resource`, `provider`, and `operation`.

Current canonical additive fields also include:
- retry metadata: `retry_attempt`, `retry_max`, `retry_exhausted`, `retry_delay_s`;
- causal metadata: `failure_class`, `last_failure_reason`, `cause_exception_type`, `cause_code`, `causal_chain`;
- decision metadata: `incident_kind`, `severity`, `priority`, `diagnostic_confidence`, `recommended_action`, `next_step`, `retryable`, `support_needed`;
- structured `evidence` for compact `expected`/`observed`/`resource`/`operation` facts.

Compact modern example:

```python
from smonitor.integrations import context_extra

extra = context_extra(
    caller="mylib.io.download_structure",
    resource="181l.pdb",
    provider="RCSB",
    operation="download",
    retry_attempt=2,
    retry_max=5,
    retry_exhausted=False,
    failure_class="network",
    last_failure_reason="timeout",
    incident_kind="network",
    recommended_action="retry",
    next_step="check-network",
    evidence={"expected": "download ok", "observed": "timeout"},
)
```

## 5.3 Report, Bundle, and Machine-Oriented Output

Level: **Advanced / CI-support**

SMonitor now exposes QA-oriented summaries beyond raw event streams:

- events carry stable `fingerprint`, `run_id`, `session_id`, and optional `correlation_id`.
- events also carry a stable additive `human_summary` block for concise human-facing handoff.
- `report()` includes `events_by_code`, `events_by_category`, `events_by_fingerprint`, `slow_signals_recent`, and `coalesced_warnings`.
- `report()` also exposes operational triage sections such as `top_codes`, `top_sources`, `top_fingerprints`, `most_noisy_resources`, `most_expensive_entries`, `blocking_incidents`, `actionable_incidents`, and `recurrent_incidents`.
- bundle exports mirror those summaries under `triage`.
- bundle exports also carry a `runtime` block and can be compared locally with `smonitor compare`.
- `JsonHandler` includes a `normalized` payload section with stable machine-oriented fields for cross-library ingestion, including retry/causal metadata, decision metadata, structured `evidence`, and mirrored `human_summary`.

These additions should be treated as the preferred source for automated QA summaries before scanning raw event buffers.

Minimal CI/support flow:

1. run tests or the representative workflow;
2. export a local bundle;
3. inspect `triage` first, not raw events;
4. compare against a previous bundle when asking “what changed?”;
5. only fall back to raw event streams when the summaries are insufficient.

## 5.4 Human-Readable Output and Coalescing

Level: **Advanced / CI-support**

Two usability rules now apply:

- Human-readable handlers may truncate very large structured payload fragments for `qa`, `dev`, and `debug` profiles. The underlying event payload is not altered.
- Repeated transient warnings can be coalesced with `warning_coalesce_window_s`. The first warning is emitted normally; suppressed duplicates are summarized in `coalesced_warnings`.

Use coalescing only for clearly repeated transient diagnostics such as download retries, not for semantically distinct warnings.

More general duplicate handling is also available through `duplicate_policy`, keyed by incident fingerprint. The current pre-1.0 supported policies are:
- `off`
- `emit_summary`
- `emit_every_n`

Use duplicate policies for genuinely repeated incidents where aggregate counts are more useful than verbatim repetition.

## 6. Noise Control

Level: **Recommended**

SMonitor captures all exceptions by default as `ERROR`. For functions that perform exploratory checks (e.g., "is this string a unit?"), this creates log noise.

### Exploratory Functions
Use `exception_level="DEBUG"` in the `@signal` decorator to silence expected failures in normal operation.

```python
@signal(tags=["check"], exception_level="DEBUG")
def is_valid_format(data):
    # If this raises, it will be logged as DEBUG, not ERROR
    ...
```

### Assertive Parsing
For functions that *must* succeed (e.g., "parse this unit"), keep the default `ERROR` level. If a user provides malformed input where a valid one is expected, it *is* an error.

## Required behavior (non-negotiable)

1.  **Zero String Hardcoding**: If it's a warning or error, it belongs in the catalog.
2.  **Lazy Diagnostics**: Do not perform expensive string formatting before calling `emit`. Pass raw data in `extra` and let SMonitor handle the interpolation.
3.  **Traceability First**: Use `@signal` generously in orchestration layers but avoid it in high-frequency tight loops.
4.  **Template Wiring Integrity**: Every emitted catalog code must have a matching template in the active `_smonitor.py` configuration.
5.  **No Silent Emission Failures**: Never hide failed catalog emissions without an explicit fallback diagnostic.

---
*Document created on February 6, 2026, as the authority for SMonitor integration.*
