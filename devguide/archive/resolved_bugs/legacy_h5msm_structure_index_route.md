---
summary: Legacy H5MSM declares structure indices without a delivery route.
issue: uibcdf/molsysmt#523
status: resolved
opened: 2026-11-03
closed: 2026-11-03
severity: medium
verification: reproduced
area: [form, attribute]
guard: tests/form/file_h5msm/test_structure_indices.py
normative:
blocked_by: []
supersedes: []
---

# Legacy H5MSM structure-index delivery

**Reported:** by DockingMT under uibcdf/dockingmt#55; reproduced on main
c0e8742dc71e312eee98c62c7f5d1133a97a7480 on 2026-11-03.
**Status:** resolved; both form-owned routes deliver metadata-only indices,
with source, resource, unit and documentation guards passing.

## What

The public query below raises `NotWithThisFormError`, even though `file:h5msm`
declares `structure_index`. The existing legacy deprecation warning is expected.

```python
import molsysmt as msm
path = msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']
msm.get(path, structure_indices=0, structure_index=True)
```

## How

Neither the file adapter nor `molsysmt.H5MSMFileHandler` implements
`get_structure_index_from_system`. Add the file route and delegate to the handler
route, reading only `structures@n_structures_written`. Reuse the shared index
validator with the available count. Return positional lists independently of
stored IDs, preserving explicit order and repetitions. Keep `None` and empty
selection semantics aligned with the resident Structures getter. The file route
owns and closes its read-only handle, including on validation errors; a
caller-owned handler remains open.

## Why

Consumers need the source structure axis without constructing a resident system.
Making each consumer convert an entire file just to query positions defeats the
declared attribute contract and adds avoidable memory use. This is a missing
adapter route, not a chemical or geometric calculation change.

## What is measured and what is assumed

The original bundled-file regression fails before the correction with
`NotWithThisFormError` (one failed case, pytest exit 1). Initial focused
selections pass 57 and then 69 cases. The first broad selection passes 1,388
and fails two new resource tests: their test-only import confused the converter
module with the lazily exported function after another test loaded it. An
explicit module import fixes this order dependency without a runtime change.
The failed run remains failed; the later receiving below is a separate run.

Final receiving uses two pytest workers:

```bash
python -m pytest --receptor=llm -n 2 tests/form/file_h5msm tests/form/molsysmt_H5MSMFileHandler tests/basic/test_structure_index_types.py
python -m pytest --receptor=llm -n 2 tests/documentation --doctest-modules molsysmt/basic/get.py molsysmt/form/file_h5msm/get_structural_attributes.py molsysmt/form/molsysmt_H5MSMFileHandler/get_structural_attributes.py
```

- **1,390 passed**, zero failures/omissions, 59.98 seconds. All 686 warnings
  are expected legacy deprecations (655 for 0.4 and 31 for 0.3).
- **566 documentation/doctest cases passed**, zero failures/omissions,
  52.85 seconds. The 532 warnings comprise 514 Sphinx/MyST deprecations,
  11 legacy deprecations, six headless plotting notices and one intentional
  structural-attribute-drop control.
- All 14 fast release gates pass; Ruff lint/format passes for 4,316 files and
  the public docstring checker passes for 246 functions.

Both modified notebooks retain every code cell, output, execution count and
code-cell metadata unchanged. The four unrelated pre-existing autosummary edits
are untouched. These are source contract and parity results, not an I/O benchmark,
installed-platform qualification or an extension of the frozen addon candidate.

## What was refuted

The defect remains on current main, so it is not limited to the reporter's old
source pin. A new structure resolver, native conversion, stored-ID interpretation
or migration is unnecessary: the written structure count already exists.

## Scope and exclusions

Legacy 0.3/0.4 file and handler index getters only. The 0.5 public modular reader
retains its separate resident-load behavior. Legacy unit checks and warnings
remain active; no source bytes, units, IDs or state associations are rewritten.
This does not change other getters' counts or introduce a file-backed 0.5 query API.

## Acceptance criteria

- The original public query returns `[0]`.
- All/scalar/nonconsecutive/repeated/empty/None requests have explicit results;
  invalid types and out-of-range positions raise `ArgumentError`.
- Both file and caller-owned handler paths work for 0.3 and 0.4 without dataset
  payload reads. IDs are not interpreted as positions; source bytes stay unchanged.
- Resource ownership, legacy units and modular-reader regressions remain covered.
- Public docstrings, User Guide and course explain the supported boundary.

## Provenance

Local Linux source checkout, Python 3.14.7, NumPy 2.4.6, Pandas 2.3.3, shared
development environment, starting at c0e8742dc71e312eee98c62c7f5d1133a97a7480.
The commands above use the repository on PYTHONPATH and the retained Viewer
ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352 source runtime, Agg plotting and one
OpenMP thread per process. No environment or backend was replaced. No package
or release was published, and no installed-pair qualification is claimed.
