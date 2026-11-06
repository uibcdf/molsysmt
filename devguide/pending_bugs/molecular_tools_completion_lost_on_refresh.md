---
summary: Molecular tools loses the completed-removal outcome during automatic panel refresh
issue: uibcdf/molsysmt#590
status: partial
opened: 2026-11-05
closed:
severity: medium
verification: reproduced
area: [molsysviewer]
guard: tests/molsysviewer_molsysmt/test_system_panel.py::test_completed_removal_survives_context_refresh_without_replaying_science
normative:
blocked_by: []
supersedes: []
---

# Completed removal loses its outcome

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
