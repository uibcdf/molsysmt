---
summary: Jupyter result-window guards read titles before presentation acknowledgement.
issue: uibcdf/molsysmt#609
status: partial
opened: 2026-11-06
closed:
severity: medium
verification: reproduced
area: [tests, molsysviewer, jupyter]
guard: tests/molsysviewer_molsysmt/jupyter_receiving_guard.py::test_actual_jupyter_periodic_geometry
normative:
blocked_by: []
supersedes: []
---

# Result-window title receiving before acknowledgement

## What

The Jupyter drivers used the child loading marker as a proxy for completed
presentation, then immediately asserted the custom title. Popup reservation uses
“Molecular result”; the real title is set after the asynchronous popup operation.
The marker can disappear before that operation completes.

## How

`/tmp/msv-periodic-jupyter-current-20261106.log` retains a 33.41-second failure:
all preceding molecular checks passed, then the title was “Molecular result”
instead of “Periodic result”. Viewer runtime 49dba88a's
presentation-surface.ts awaits molsysviewerOpenPopup, sets item.title, then
sends shown. The actual provider present_view promise resolves on that
acknowledgement and its result card reports “Result opened in its own window.”
Existing Translate/Center/Fit and copy receiving used the same early assertion.

## Why and correction

Wait for the actual acknowledged result-card completion before asserting the
exact custom title. All molecular, lifetime, destination, title and timeout
checks are retained; no sleep or placeholder-title acceptance is added. The
five affected drivers now use that boundary, including the detached-Studio
result path. This is a receiving-harness correction under PR #543, not a Viewer
runtime or scientific algorithm change. All seven actual Jupyter/Mol*/popup
scenarios pass after the correction (322.92 s, no skips), including the exact
titles and original scientific/lifetime assertions. The periodic scenario checks
eight steps and actual coordinates in both parent and independent result.
The dated receipt is
[periodic receiving](../../devtools/data/molsysviewer_tools_periodic_receiving_20261106.json).
Owner review/integration remains pending; the issue is not closed from this PR.
