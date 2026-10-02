---
summary: Provide bounded public occurrence pages for Interactions queries.
issue: uibcdf/molsysmt#264
status: resolved
opened: 2026-10-02
closed: 2026-10-02
verification: measured
area: [api, performance]
guard: tests/interactions/test_occurrence_pages.py::test_one_row_page_does_not_materialize_selected_occurrences
normative:
blocked_by: []
supersedes: []
---

# Bounded public occurrence pages

## What

MolSysViewer's inspector needs 50 rows per page, but `query().to_dict()` copies
every selected occurrence before the client can slice it. With 50,001 parallel
observations, even inspecting one row materializes 50,001 rows.

## How

Add an experimental public `Interactions.to_page()` with offset, row limit and
a participant-atom budget checked before copying compound definitions. Preserve
full-analysis occurrence and relation indices. Include only referenced relation
definitions and aligned occurrence geometry, evidence and measurements. Count
and coverage remain available without a full projection. Preserve `to_dict()`.

## Why

Interactive inspection needs bounded additional allocations after constructing
the retained query. A single compound participant also needs a pre-copy guard;
a row limit alone cannot bound its memory cost.

## What is measured and what is assumed

The benchmark in `devtools/scripts/benchmark_interactions_query_pages.py`
separates retained analysis bytes, query-position bytes, full projection and
one-/50-row page allocation. Tests must cover edited analyses without silently
packing all active occurrence columns.

## What was refuted

Changing H5MSM or implementing file-backed lazy loading is unnecessary for this
in-memory inspector boundary. Full `to_dict()` must retain its existing meaning.

## Scope and exclusions

Bounded projection from a constructed query or analysis. Query construction and
optional indexes have their own cost; paging does not promise free selection.

## Acceptance criteria

Public pages preserve order and stable handles, units, evidence, roles and PBC
images, including empty/unevaluated frames. Tiny pages do not copy all selected
rows. Oversized compound participants fail before copying their atom vectors.
Updated API documentation, User Guide, Cookbook and course explain the boundary.

## Provenance

Date: 2026-10-02. The benchmark records runtime versions and allocation evidence;
final commands and results are recorded in the resolution.

## Resolution

Experimental `Interactions.to_page(offset=0, limit=50,
max_participant_atoms=10000)` returns typed `molsysmt.interactions.page@1` columns.
Global relation and occurrence handles remain stable; a compact relation
catalog carries roles, atom groups and offsets. Total count, continuation offset,
coverage, source maps, evidence, measures, units and PBC images remain explicit.
A zero limit returns typed empty arrays. Invalid bounds raise argument errors.

The constituent-atom budget counts reused relations per occurrence and fails
before copying definitions or image blocks. Packed query views slice positions;
invalidated and replaced analyses select active frame windows without packing
all surviving columns. Tests cover nonconsecutive order, parallel observations,
empty/unevaluated coverage, H5MSM 0.5 round trips and repeated edits.

For 50,001 parallel observations, retained numeric analysis storage is
1,800,132 bytes and the constructed query's positions use 400,008 bytes.
Additional warmed projection allocations are measured separately:

| Projection | Allocation peak, bytes | Median, ms |
| --- | ---: | ---: |
| Full `to_dict()` | 4,201,987 | 1.287 |
| One-row page | 7,152 | 0.205 |
| 50-row page | 11,613 | 0.215 |

The guard forbids calling the full public projection, checks one-row allocation
below 100,000 bytes and asserts stable handles, compound roles, producer version
and aligned geometry. Other tests forbid complete edited packing and participant
copies before the budget check. These checks protect the mechanism, rather than
a machine-specific timing threshold.

User Guide Foundations, Toolbox, Cookbook and Common Core Module 20 explain the
separate analysis, query/index and page costs. Fourteen executable result-guide
blocks and nine cookbook blocks passed; course executable cells and their saved
outputs were preserved. The result method's doctest is part of the focused and
developer-tool validation. A page is an inspection projection, not a standalone
codec or a file-backed lazy reader.

### Provenance of the measurement

Linux x86_64, Intel Xeon E5-2630 v4 @ 2.20GHz, Python 3.13.14, NumPy 2.4.6.
One warm-up, median of five repetitions; `tracemalloc` peaks exclude retained
analysis and query arrays. The dated artifact identifies final runtime hashes.

## Verification checkpoint — 2026-10-02

The default local suite passed **11,744 tests**, with 11 known environment skips,
in 341.85 seconds. The focused interaction/chemistry/doctest suite passed 723
tests; Pandas 3.0.6 focused qualification passed 161 tests. Developer-tool tests
and result doctests passed 260 tests. Ruff, docstrings, API signatures and the
14 fast release gates passed. This is local source evidence, not an installed
artifact or cross-platform release certification.

The [dated evidence artifact](../../../devtools/data/interactions_reported_bugs_20261002.json)
records commands, source hashes, measurements and exclusions.
