---
summary: Post-1.0 streaming interactions and H5MSM append
issue: uibcdf/molsysmt#336
status: open
opened: 2026-10-05
closed:
verification: inspected
area: [form, performance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Post-1.0 streaming interactions and H5MSM append

## What

Design bounded detector-to-file accumulation and resumable H5MSM append for systems with topology and named analyses after 1.0.

## How

Reuse bounded numeric-window occurrence writing and chunked detector execution. Define transactional visibility for complete structure batches, relation catalog updates, evaluation coverage, execution records and chemical-state/axis associations. Specify interruption recovery and read compatibility before choosing schema changes. Support variable and zero interaction counts without padding or whole-trajectory materialization.

## Why

The implemented H5MSM 0.5 round trip and bounded export of resident analyses do not directly stream detector results. Public `h5msm.append_structures` currently excludes topology/interaction layers. Earlier design work considered append/recovery, but it must have a separate post-1.0 owner.

## What is inspected and what is assumed

Source inspection of `molsysmt/h5msm.py` and [#252's provider checklist](../archive/resolved_proposals/implement_experimental_sparse_interactions_results_and_queries.md#provider-closure-checklist) establishes those exclusions. Existing writer/compaction measurements are in [the benchmark guide](../benchmarking/h5msm.md). This proposal supplies no new implementation, benchmark, crash-safety proof or arbitrary lazy query API.

## What was refuted

Writing a resident result in windows is not direct detector streaming. Extending coordinate arrays alone cannot atomically update named analysis coverage, axes and provenance. A HDF5 library call succeeding does not establish crash-consistent visibility.

## Scope and exclusions

Post-1.0 under the [scope freeze](../release_1_0_scope.md). Preserve current H5MSM 0.5 behavior until a reviewed compatibility decision. There is no automatic 0.6 bump; MolecularMechanics persistence is #256. Individual in-memory editing is #335. Initial Viewer integration loads the chosen analysis in memory.

## Acceptance criteria

- Define supported layer combinations, axis/state updates, append identity and visible commit units.
- Verify interruption before/during/after data and metadata writes against an independently specified committed-state oracle.
- Exercise variable/zero observations, compound participants, parallel images, multiple named analyses and original producers through public reads/conversions.
- Measure sustained write/read cost, memory and disk overhead with projected versus full-source workloads and retained implementation/environment identities.
- Publish a reviewed compatibility contract and meaningful guards before claiming resumability or bounded end-to-end memory.

## Dependencies and risks

Current native associations and codecs under #252/#254 are prerequisites. Future client file access is guided by measured workloads; no new uibcdf/molsysviewer#114 initial-integration gate is added.
