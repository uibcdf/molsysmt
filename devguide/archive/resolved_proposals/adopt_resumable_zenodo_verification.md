---
summary: Adopt resumable read-only Zenodo verification.
issue: uibcdf/molsysmt#273
status: resolved
opened: 2026-10-01
closed: 2026-10-01
verification: measured
area: [ci]
guard:
normative: devguide/release_and_citation.md
blocked_by: []
supersedes: []
---

# Adopt resumable read-only Zenodo verification

**Reported:** 2026-10-01, common recovery work under uibcdf/molsyssuite#49.
**Status:** Resolved; published exact-tag and covered-release hosted checks pass.

## What

Adopt the common provider rather than another component-local retry algorithm.
Replace the 900-second release wait with one bounded probe, scheduled complete
discovery and manual exact-tag verification. Preserve explicit archival states.

## How

The caller pins `b78fa9d30d46ce5607999cdecae85cf6c03f5fcd`, stable concept DOI `10.5281/zenodo.1298752`, and a fixed
2026-09-25 coverage cutoff. It handles published releases, public prereleases,
six-hour schedules and manual dispatch. The common job checks out its own pinned
source, not the component's commit, and queries only public facts. The local
normative citation contract routes sign-off through explicit verified evidence.

## Why

The paired public archives appeared about 87 minutes after publication, beyond
the old 15-minute window. A pending archive or inconclusive service query must
not become a permanent absence claim or prompt duplicate publication.

## What is measured and what is assumed

The central provider passed thirteen semantic tests and the complete 177-test
central suite; direct public checks matched both paired releases. Local adoption
is configuration inspection until the published hosted run completes. A 72-hour
deadline is a maintainer intervention threshold, not a Zenodo service guarantee.

## What was refuted

Long runner sleeps waste resources. Rolling lookbacks can drop overdue work.
Green jobs with pending evidence cannot complete archival sign-off. Replaying
accepted hooks or deposits is unnecessary for read-only recovery.

## Scope and exclusions

Release verification, contributor operation and reporting governance. No release
publication, package promotion, scientific execution or product code changes.

## Acceptance criteria

Published caller uses the immutable provider; local reporting/index guards pass;
hosted exact-tag and covered-release scan pass with native verified states and
the exact source file identity. Archive this report with hosted evidence and the
local normative contract, preserving scientific review deferrals.

## Dependencies and risks

The caller relies on GitHub scheduling and anonymous Zenodo queries; failures
remain visible. Maintainers own overdue follow-up and manual dispatch. Central
request/discovery bounds must not silently omit a covered release.

## Provenance

2026-10-01, Python 3.13.15, isolated checkout from refreshed main. Original member
worktrees are preserved. Publication/hosted measurements are recorded at closure.

## Resolution — 2026-10-01

[exact hosted run 36841371420](https://github.com/uibcdf/molsysmt/actions/runs/36841371420) passed at `f09ed3b4c73a8ecdd0cf2341a62ec450dbadcc7d`. Native checkout logs prove provider `b78fa9d30d46ce5607999cdecae85cf6c03f5fcd`; the actual probe step passed. The sanitized artifact reports `verified` for 0.22.4, record 22959294, version DOI 10.5281/zenodo.22959294, with the registered exact source ZIP size and checksum.

[scan hosted run 36841371556](https://github.com/uibcdf/molsysmt/actions/runs/36841371556) passed at `f09ed3b4c73a8ecdd0cf2341a62ec450dbadcc7d`. Native checkout logs prove provider `b78fa9d30d46ce5607999cdecae85cf6c03f5fcd`; the actual probe step passed. The sanitized artifact reports `verified` for 0.22.4, record 22959294, version DOI 10.5281/zenodo.22959294, with the registered exact source ZIP size and checksum.

The fixed-cutoff scan and exact-tag routes both execute the common provider;
they do not install or test the scientific runtime. The shared tests protect the
72-hour/pending boundary, original clock, unavailable distinction, late recovery,
complete discovery and exact-file validation. Restoring a 15-minute outer window
causes the central pending-state regression to fail in a controlled mutation.

Local citation/sign-off instructions require the per-release verified state;
operationally green pending results are insufficient. The implementation changes
only archival automation, governance guidance and report records. Original working
state is preserved and scientific execution review remains deferred. Closure is
guarded by the local normative release/citation contract and the pinned common
provider's semantic regression module recorded under uibcdf/molsyssuite#49.

## Provider hardening and revalidation — 2026-10-01

Final provider `2cc2d9bfe80f14a981d40bc109ecdf2af39b693b` also handles concept records without a
usable version identity. A new failing reproducer showed that such a result
could be classified as overdue absent; it is now temporarily_unavailable when
no exact match can be established. All fourteen provider regressions pass.
The current caller and normative operation guide pin this hardened commit.
Initial adoption observations above remain unchanged historical evidence.

[exact final hosted run 36843304931](https://github.com/uibcdf/molsysmt/actions/runs/36843304931) passed at `3dfdd51ee8f841eec3940cd161b988c98aae1e16`. Native checkout logs prove the final provider commit and actual verified-state output; the sanitized artifact matches the registered source ZIP name, size and checksum.

[scan final hosted run 36843305017](https://github.com/uibcdf/molsysmt/actions/runs/36843305017) passed at `3dfdd51ee8f841eec3940cd161b988c98aae1e16`. Native checkout logs prove the final provider commit and actual verified-state output; the sanitized artifact matches the registered source ZIP name, size and checksum.
