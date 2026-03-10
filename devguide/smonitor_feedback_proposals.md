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

Still proposed, not yet implemented upstream:
- slow-call threshold events for QA/performance triage,
- richer profile-aware rendering or truncation for large structured payloads,
- small helper APIs for common context keys.
