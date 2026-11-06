---
summary: Molecular tools review summary inherits incompatible Jupyter definition-list floats
issue: uibcdf/molsysmt#591
status: partial
opened: 2026-11-05
closed:
severity: medium
verification: reproduced
area: [molsysviewer]
guard: tests/molsysviewer_molsysmt/jupyter_receiving_guard.py::test_actual_jupyter_review_and_independent_popups
normative:
blocked_by: []
supersedes: []
---

# Jupyter distorts the review summary

## What

The removal summary's Structures label overlaps its value in an actual
JupyterLab 4.6.4 output, despite the addon stylesheet being mounted correctly.
This is distinct from the host's closed stylesheet-lifetime defect #298 in
uibcdf/molsysviewer.

## How

Computed styles on contribution e3d5d21a5 show float:left on all six dt/dd
elements. The Structures label receives width 39.6562px; its value starts
39.6562px to the right. Jupyter's definition-list selectors override the
less-specific addon defaults. The ordinary standalone page lacks those styles.

## Why

Selected/retained counts and structure scope must stay legible before a
destructive confirmation in the supported notebook host.

## Correction and receiving

The proposed addon-scoped rule explicitly resets float, clear and width for
the review summary's label/value blocks. The host and other panels keep their
styles. The actual Jupyter runner checks computed floats, vertical separation
and aligned left edges, as well as the real native 165/3,818 selection result.
Its command is documented in the maintained GUI design; screenshots alone
are not a passing guard. PR #543 owner review and final receiving remain
pending. The addressable pytest guard invokes the real runner in an explicit
local GUI lane, separately from the default scientific collection. Missing GUI
prerequisites fail; this is not a skipped or simulated notebook result.

Final local receiving passes 4,485 default addon cases and the explicit actual-
Jupyter pytest guard (one case, six browser checks). Native source/backend and
recorded support providers remain unchanged. The final source-hash receipt is
`devtools/data/molsysviewer_tools_jupyter_receiving_20261105.json`.
