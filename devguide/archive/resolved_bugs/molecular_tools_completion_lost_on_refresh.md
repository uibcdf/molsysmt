---
summary: Molecular tools loses the completed-removal outcome during automatic panel refresh
issue: uibcdf/molsysmt#590
status: resolved
opened: 2026-11-05
closed: 2026-11-08
severity: medium
verification: reproduced
area: [molsysviewer]
guard: tests/molsysviewer_molsysmt/test_system_panel.py::test_completed_removal_survives_context_refresh_without_replaying_science
normative:
blocked_by: []
supersedes: []
---

# Completed removal loses its outcome

## Resolution — owner receiving, 2026-11-08

Fixed in `4c681998c9236f701521a892705548ca0ea80597` and received on clean source
`68323539ee6b6473d453f6fbe61f5dc5ae826630` with independently verified
Viewer export `e4dd58cf0edcb2c3afb2c982ccd50d3899d504ab`. The real notebook retains the completed removal across refresh, confirms 3,817 final atoms and exactly two managed edits, and preserves outcome expiry and token/revision guards.

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

Actual Jupyter widget comms briefly publish the successful removal message and
then clear it during the automatic synchronized-context refresh. Bundled 1TCD
correctly changes from 3,983 to 3,818 atoms and Mol* draws the result; the error
is in reporting the operation, not in the scientific edit.

## How

On contribution e3d5d21a5, a DOM observer records review, updating, completed
removal, then empty selection-stage status. The refresh response follows the
completion response in real comms. Its default empty message replaces that
completion. The old standalone transport did not expose this ordering.

## Why

A destructive operation needs a truthful, durable outcome. Refresh must never
re-execute science or recover a consumed confirmation token.

## Correction and receiving

The proposed fix retains only the target weak reference, expected managed
revision and bounded draft for a completed removal. A matching context refresh
reprojects completion. A new task action, changed draft, revision/replacement
or panel lifetime expires the notice. Atom arrays and review tokens are not
retained in the outcome or persisted in frontend state.

The real-demo guard originally fails with select instead of done; five new
outcome-lifetime cases and the existing panel tests pass in the scoped run.
Actual Jupyter receiving also retains the completion after refreshing. The
reproducible runner is `tests/molsysviewer_molsysmt/system_panel_jupyter.py`;
the final receipt is recorded separately after all receiving gates finish.
Owner review/integration of PR #543 remains pending. Native science, expert
defaults, visible human Qt review and installed artifacts are unchanged.

Final local receiving passes 4,485 default addon cases and the explicit actual-
Jupyter pytest guard (one case, six browser checks). Native source/backend and
recorded support providers remain unchanged. The final source-hash receipt is
`devtools/data/molsysviewer_tools_jupyter_receiving_20261105.json`.
