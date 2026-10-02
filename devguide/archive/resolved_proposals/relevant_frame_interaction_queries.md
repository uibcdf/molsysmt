---
summary: Bound internal and cross frame queries to relevant relation candidates.
issue: uibcdf/molsysmt#288
status: resolved
opened: 2026-10-02
closed: 2026-10-02
verification: measured
area: [performance]
guard: tests/interactions/test_query_candidates.py::test_frame_queries_inspect_only_relevant_relations
normative:
blocked_by: []
supersedes: []
---

# Bound interaction membership tests to requested frames

## What

MolSysViewer measured frame-local `internal` and `cross` queries inspecting
relations across all 5,000 structures. Five relevant occurrences took hundreds
of milliseconds when a synthetic catalog contained 22,495 distinct relations.

## How

Select the requested structure occurrences before testing atom membership or
interaction type. Keep atom postings for trajectory-wide atom queries. Preserve
requested frame order, parallel occurrence handles, compound participants and
view intersection semantics.

## Why

Frame-local inspection must depend on relevant relations rather than unrelated
trajectory chemistry. A reused relation and a rapidly changing catalog are both
valid workloads.

## What is measured and what is assumed

`python devtools/scripts/benchmark_interactions_query_pages.py --output result.json`
reproduces the reported changing-relation shape, times five warmed repetitions,
and measures per-operation Python/NumPy allocation peaks separately. Before and
after artifacts and local results belong in the resolution.

## What was refuted

Occurrence projection is a separate allocation boundary, tracked in #264.
Optimizing projection alone cannot eliminate irrelevant membership tests.

## Scope and exclusions

In-memory queries only. No file format change or scientific detector changes.
Cold atom-posting construction remains a separate trajectory-wide operation.

## Acceptance criteria

An executable guard forbids evaluating unrelated relations for explicit frame
queries and compares all three modes with an independent participant-set
reference. Existing frame validity, replacement and persistence tests pass.

## Provenance

Benchmark artifacts record Python, NumPy, platform, warm-up policy, timings and
allocation peaks; the final dated resolution identifies the source revision.

## Resolution

Explicit-frame queries select occurrence candidates first and test only their
unique relations. They do not construct whole-trajectory atom postings. Atom
queries without an explicit frame selection retain the postings path. Existing
full projection and ordering semantics remain supported.

| Frame-zero mode | Before median, ms | After median, ms | Matches |
| --- | ---: | ---: | ---: |
| incident | 3.171 | 0.414 | 5 |
| internal | 816.200 | 0.441 | 5 |
| cross | 400.208 | 0.384 | 0 |

The changing catalog contains 22,495 relations/occurrences across 5,000
structures and 62 atoms. A second measured fixture reuses 32 relation
definitions across the same occurrence schedule; frame and nonconsecutive
queries remain sub-millisecond on this host. Trajectory-wide changing-relation
internal queries still evaluate their relevant whole-trajectory catalog.

The guard compares results with Python participant-set semantics for repeated
and changing relations, compound groups, parallel occurrences and scalar or
nonconsecutive frames. Instrumentation fails if an unrelated relation is
inspected or a global atom index is built. Chained views must preserve the same
selected occurrences. Frame invalidation, replacement and persistence remain
covered by the interaction suite.

These are synthetic query measurements, not detector throughput. The lazy
posting memory avoided by a frame-only query will be needed if the caller later
requests a trajectory-wide atom query.

### Provenance of the measurement

Linux x86_64, Intel Xeon E5-2630 v4 @ 2.20GHz, Python 3.13.14, NumPy 2.4.6.
One untimed operation warm-up, median of five repetitions. Allocation peaks use
`tracemalloc` and exclude already retained analysis/index storage. Source before:
main 18536a793; source after: the tested runtime hashes in the dated artifact.

## Verification checkpoint — 2026-10-02

The default local suite passed **11,744 tests**, with 11 known environment skips,
in 341.85 seconds. The focused interaction/chemistry/doctest suite passed 723
tests; Pandas 3.0.6 focused qualification passed 161 tests. Developer-tool tests
and result doctests passed 260 tests. Ruff, docstrings, API signatures and the
14 fast release gates passed. This is local source evidence, not an installed
artifact or cross-platform release certification.

The [dated evidence artifact](../../../devtools/data/interactions_reported_bugs_20261002.json)
records commands, source hashes, measurements and exclusions.
