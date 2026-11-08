---
summary: Jupyter result-window guards read titles before presentation acknowledgement.
issue: uibcdf/molsysmt#609
status: resolved
opened: 2026-11-06
closed: 2026-11-08
severity: medium
verification: reproduced
area: [tests, molsysviewer, jupyter]
guard: tests/molsysviewer_molsysmt/jupyter_receiving_guard.py
normative:
blocked_by: []
supersedes: []
---

# Result-window title receiving before acknowledgement

## Resolution — owner receiving, 2026-11-08

Fixed in `dd34c371cbe78ba2ddd884266c0915d0783fb831` and received on clean source
`68323539ee6b6473d453f6fbe61f5dc5ae826630` with independently verified
Viewer export `e4dd58cf0edcb2c3afb2c982ccd50d3899d504ab`. All five original Copy/Translate/Center/Fit/Periodic drivers receive presentation acknowledgement before checking exact custom titles, including detached-Studio results.

All fourteen explicit Jupyter guards pass: 109 browser checks, zero skips,
failures or errors, in 1,451.53 s. All 8,560 owner and 2,463 Viewer-export
inputs remain unchanged. The
[portable receipt](../../../devtools/data/jupyter_owner_receiving_590_591_609_614_20261108.json)
retains original failures, both deliberate interruptions, the two-CPU Results
deadline and four-CPU receiving. Peak charged memory is 2,365,796,352 bytes;
host available memory remains above 14,193,504,256 bytes, with no memory/task-cap
or OOM event. No numerical, source, title, browser-error, lifetime or functional
deadline assertion is relaxed.

This closes this source-owner defect, not installed, human Qt, other-platform,
final-candidate or publication qualification. #615 remains open: later startup
passes do not establish its causal repair. Earlier pending-owner/contribution
statements below describe their historical checkpoints.

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
