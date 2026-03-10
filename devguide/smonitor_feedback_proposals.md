# Temporary SMonitor Feedback Proposals

This note remains a living dump for new feedback gathered while debugging MolSysMT data generation, online downloads, lossy round-trips through PDB-backed forms such as `nglview.NGLWidget`, and future cross-library QA workflows.

It is no longer the active upstream implementation checkpoint for `smonitor`.
The active plan now lives in:
- `../smonitor/devguide/README.md`
- `../smonitor/devguide/implementation_plan.md`

Use this file to record:
- new pain points observed in real debugging/CI/support work;
- suggestions not yet reflected in the active upstream plan;
- MolSysMT-side adoption notes for newly introduced `smonitor` capabilities.

## Already implemented upstream in `../smonitor`

The following capabilities that originally motivated this note are now implemented upstream:

- better profile-aware handling of structured context in human-readable outputs;
- canonical structured context helper via `smonitor.integrations.context_extra(...)`;
- structured retry diagnostics through canonical retry metadata fields;
- optional coalescing of repeated transient warnings;
- final summary event for coalesced warning windows;
- richer normalized JSON payloads for QA/agent ingestion;
- canonical retry and causal metadata in normalized machine output;
- structured per-call signal context via `signal(..., extra_factory=...)`;
- tag-aware profiling summaries via `timings_by_tag`;
- opt-in slow-signal events for QA/developer workflows;
- bundle/report triage summaries for codes, categories, fingerprints, slow signals, and coalesced warnings.

## MolSysMT-side adoption notes

Current MolSysMT-side adoption progress:
- `context_extra(...)` is already used in the shared download helper, JIT warning emission, and the multi-container/ambiguous-structure warning callsites touched during this pass.
- The AlphaFold BCIF import path and selection fallback warning path also use `context_extra(...)`.
- Upstream `smonitor` now exposes explicit runtime identifiers (`run_id`, `session_id`, optional `correlation_id`) with default generation and override support; MolSysMT can consume those identifiers directly in QA/support workflows without local identifier plumbing.
- Remaining manual `extra` payloads should be reviewed incrementally as future diagnostics work touches those paths.

## Open area for new suggestions

Keep adding new suggestions here when real work reveals gaps in:
- diagnostic structure;
- noise reduction without information loss;
- reproducible support and triage;
- human/agent dual usability;
- cross-library payload conventions.

## Suggested format for future entries

For each new suggestion, prefer capturing:
- observed problem;
- why current `smonitor` behavior is insufficient;
- desired behavior;
- whether it belongs in `smonitor` core or in MolSysMT-side adoption;
- example payload/report/bundle shape if relevant.
