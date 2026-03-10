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
