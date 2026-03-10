# Temporary SMonitor Feedback Proposals

This note is temporary. It captures feedback gathered while debugging MolSysMT data generation, online downloads, and lossy round-trips through PDB-backed forms such as `nglview.NGLWidget`.

## Local actions already justified in MolSysMT

- Library-specific catalogs should not collapse detailed warnings into generic text when the original message already carries actionable context.
- Download warnings should expose, at minimum:
  - resource identifier,
  - provider/backend,
  - retry counters,
  - failure reason,
  - emitting caller.
- MolSysMT should pass structured `extra` fields to SMonitor when emitting download warnings.

## Desired SMonitor capabilities for QA and developer workflows

### 1. Better profile-aware rendering of structured context

Current integrations allow contextual fields in `extra`, but QA- and agent-facing output still depends heavily on each library formatting that context into free text.

Desired behavior:
- `user` profile stays concise,
- `developer` profile surfaces the root cause and callsite,
- `qa` / `agent` profiles surface stable structured context directly in rendered output.

Example target for a download warning:
- resource: `181l.bcif.gz`
- provider: `RCSB PDB`
- attempt: `2/5`
- reason: `timed out`
- caller: `molsysmt.form.file_bcif_gz.download`

### 2. Support for structured retry diagnostics

Transient download failures are common in CI and data generation.

Desired behavior:
- stable event code for retryable download failures,
- explicit retry counters,
- differentiation between:
  - HTTP 429,
  - HTTP 5xx,
  - DNS / timeout / network errors,
  - final retry exhaustion.

### 3. Event coalescing for repeated transient warnings

Repeated retries can flood logs and slow QA triage.

Desired behavior:
- optional coalescing of repeated warnings with the same code/resource/caller,
- final summary event preserving total retry count and last failure reason.

### 4. Richer bundle output for support handoff

Bundles are already useful, but download and conversion investigations would benefit from richer normalized payloads.

Desired additions:
- operation name (`download`, `convert`, `rebuild`, `parse`),
- resource identifiers,
- backend/provider,
- normalized failure class,
- retry metadata,
- optional causal chain when one warning/error wraps another subsystem.

### 5. Cross-library propagation conventions

MolSysSuite libraries should agree on a small shared vocabulary in diagnostic payloads.

Candidate common keys:
- `resource`
- `provider`
- `operation`
- `attempt`
- `retries`
- `reason`
- `caller`
- `source_library`

This would make cross-repo QA and agent triage much faster.

### 6. Signal and profiling improvements in `smonitor` core

- Signal traces currently summarize timings by function key only; exposing decorator tags in reports or timeline views would make API/native/conversion hot paths much easier to audit during QA.
- The `signal` decorator would benefit from an optional structured `extra` hook so libraries can attach stable context (for example, form names or selection syntax) without emitting separate warnings.
- Slow-call threshold events in `smonitor` core would be useful for QA and performance triage, especially for import-time or first-call JIT latency investigations.
- Small helper APIs in `smonitor` core for common structured-context fields (for example, `caller`, `form`, `requested_attribute`, `record`) would reduce repetitive local wiring across libraries.

### 7. Upstream progress snapshot (2026-03-09)

Implemented upstream in `../smonitor` during this stabilization pass:
- `signal(..., extra_factory=...)` now supports structured per-call context without separate warning emissions.
- Profiling timeline entries now preserve signal tags and signal-provided meta context.
- `report()` now exposes `timings_by_tag` in addition to timings by function and module.

Remaining upstream open items for the current stabilization track:
- monitor the new normalized machine payload in real cross-library QA usage and extend it only if a concrete gap appears.

Additional upstream progress during this pass:
- opt-in slow-signal events (`slow_signal_ms`, `slow_signal_level`) now emit structured profiling events for QA/developer workflows.
- profile-aware truncation for large structured payloads is now implemented in human-readable handlers.
- `smonitor.integrations.context_extra(...)` now provides the canonical helper for common structured diagnostic fields.

### 8. Next-session checkpoint and implementation order

Current upstream status in `../smonitor`:
- structured per-call signal context is implemented,
- tag-aware profiling summaries are implemented,
- opt-in slow-signal profiling events are implemented,
- profile-aware truncation for large structured payloads is implemented in human-readable handlers.

Next implementation slices proposed upstream, in order:
1. monitor the new normalized machine payload in real cross-library QA usage and only extend it if a concrete gap appears.

MolSysMT-side follow-up after each upstream slice:
1. adopt the new `smonitor` helper APIs in local callsites that still handcraft repeated `extra` payloads;
2. extend cross-repo contract tests when new structured fields become canonical;
3. keep this file synchronized as the authoritative MolSysMT-side checkpoint for the upstream `smonitor` stabilization track.


Additional upstream progress in this pass:
- opt-in warning coalescing is now available, with triage summaries for suppressed duplicates.
- JSON output now includes a normalized machine-oriented payload section for stable QA ingestion.
