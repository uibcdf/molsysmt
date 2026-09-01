---
summary: Published benchmark surfaces retain pre-#183 timings
issue: uibcdf/molsysmt#194
status: resolved
opened: 2026-09-01
closed: 2026-09-01
severity: medium
verification: reproduced
area: [docs, performance]
guard: tests/documentation/test_benchmark_baseline_sync.py
normative:
blocked_by: []
supersedes: []
---

# Bug: published benchmark surfaces retain pre-#183 timings

**Reported:** 2026-09-01, while auditing derived documentation after resolving the
unconditional garbage-collection cost in `uibcdf/molsysmt#183`.
**Status:** active. Reproduced by comparing the canonical baseline files with the data
and values served by the documentation.

## What

MolSysMT's published performance surfaces do not show the post-#183 implementation:

- the interactive dashboard reads `docs/_static/benchmarks_data/`, whose competitor
  copy still identifies MolSysMT 0.18.0 and predates the regenerated canonical file;
- `benchmarks/baselines/macro_kernels_session.json` still records full-GC-dominated
  public timings from MolSysMT 0.18.0;
- the user-facing benchmark notebook embeds a third, hard-coded timing matrix;
- the dashboard requests `competitor_least_rmsd_*` keys, while the producer emits
  `competitor_rmsd_*`, so that plotted series resolves to zero.

```console
$ cmp benchmarks/baselines/competitor_matrix_session.json \
      docs/_static/benchmarks_data/competitor_matrix_session.json
$ echo $?
1
```

## How

The benchmark runner writes canonical JSON under `benchmarks/baselines/`, but there is no
checked synchronization step for the copies consumed by
`docs/_static/benchmarks_dashboard.html`. The notebook separately writes timing strings
inside a code cell instead of reading the same canonical data. These three independent
surfaces drift whenever a baseline is regenerated.

The dashboard has a second contract mismatch: `renderCompetitors()` labels the third
operation `Least-RMSD` and reads four `competitor_least_rmsd_*` keys that do not exist in
the producer or canonical JSON. The benchmark producer consistently names that operation
`competitor_rmsd_*`.

## Why

Users reading the performance chapter or interactive dashboard see obsolete public API
costs after the implementation changed by factors of approximately 6 to 48. The site
claims that the dashboard is compiled from the latest baseline, so stale copies make a
current, user-facing claim false rather than merely historical.

## What is measured and what is assumed

Measured: the canonical competitor baseline at `ade8a0d51` records center, RMSD, and
distance public medians of 49.7 ms, 35.7 ms, and 6.73 ms. The documentation copy still
records 280.3 ms, 284.5 ms, and 325.0 ms. The macro baseline records 256.3 ms, 265.3 ms,
and 709.0 ms from MolSysMT 0.18.0. The notebook embeds 291.13 ms, 306.49 ms, and a
separately measured distance value.

Assumed: no published deployment rewrites these files outside the repository build. The
checked Sphinx source and static asset paths show no such synchronization step.

## What was refuted

The interactive dashboard does not read `benchmarks/baselines/` directly. Its endpoint
map explicitly targets `docs/_static/benchmarks_data/`, and the two competitor files are
not byte-identical. Rebuilding Sphinx alone therefore cannot repair the data.

The notebook values are not generated outputs from the current canonical JSON. They are
literal strings in an executable code cell, so copying the static dashboard data alone
does not repair the table.

## Scope and exclusions

Covers the competitor and macro-kernel baselines, their published static copies, the
benchmark notebook matrix, the dashboard key contract, and the active Rust optimization
guide's statement about the removed collection cost.

Excludes archived reports, whose dated measurements remain historical evidence. Excludes
redesigning the benchmark suite or dashboard, adding new benchmark domains, and the
broader regression-gate reliability theme.

## Acceptance criteria

1. The macro-kernel baseline is regenerated against the post-#183 implementation.
2. Published competitor and macro JSON files exactly match their canonical baselines.
3. The notebook presents the same benchmark session rather than independent literals.
4. The dashboard reads the producer's `competitor_rmsd_*` keys.
5. A guard fails when a published baseline copy diverges from its canonical source.
6. The relevant notebook execution and Sphinx build complete successfully.

## Dependencies and risks

The benchmark notebook is temporarily frozen against expansion, but correcting false
measurements preserves its required timing matrix and is not an expansion. Regenerating
the macro baseline is environment-sensitive, so the record must retain its environment,
commit, warm-up, repeat, and memory metadata.

## Provenance

Inspected and reproduced on 2026-09-01 at MolSysMT `ade8a0d51`, Linux
7.0.0-28-generic x86_64, Python 3.13.14. The post-#183 competitor matrix was generated in
the `molsyssuite@uibcdf_3.13` environment. Historical values above come directly from the
committed JSON and notebook cells named in this report.

## Resolution

Resolved in `6cea6580a`. The macro-kernel baseline was regenerated at commit
`a50caa292`; public medians changed from 256.3 to 13.30 ms for center, from 265.3
to 14.46 ms for RMSD, and from 709.0 to 147.12 ms for pairwise distances. The
published competitor and macro files now exactly match their canonical baselines.

The notebook now reads the published competitor JSON instead of maintaining timing
literals. Its table was executed successfully and presents the same session as the
dashboard. The dashboard reads the producer's `competitor_rmsd_*` keys, and its legend
states that the shared series uses MDTraj or SciPy according to the operation. The active
Rust guide now labels its full-GC profile as historical and records the resolutions in
`uibcdf/molsysmt#183` and `uibcdf/argdigest#3`.

The synchronization command and its `--check` mode are documented for developers. The
guard compares both published JSON objects with their canonical sources and verifies
that every competitor key referenced by the dashboard exists in the producer output.
All three guard tests pass with `--receptor=llm`, Ruff passes, the notebook executes, and
the full Sphinx HTML build completes. The build used MolSysViewer's local stable
`build/lib` copy because the concurrently edited source checkout contained an incomplete
`catalog.py`; no MolSysViewer file was changed. The build retained only pre-existing
not-in-toctree warnings.
