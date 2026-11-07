---
summary: Principal-axis rejection reports a local position as a source structure index
issue: uibcdf/molsysmt#640
status: open
opened: 2026-11-07
closed:
severity: low
verification: reproduced
area: [diagnostics, structure]
guard:
normative:
blocked_by: []
supersedes: []
---

# Principal-axis rejection reports a local position as a source structure index

## What

`structure.align_principal_axes` labels a local position in the selected structure array as a molecular structure number. With requested structures `[2, 0]` and degenerate moments only in source structure 0, the error says that structure 1 is degenerate. Structure 1 was not evaluated.

## How

Owner Geometry/principal-axis receiving uses bundled pentalanine, three structures, moving atoms 0–7 and `structure_indices=[2, 0]`. Set only source structure 0's selected atoms collinear. Native validation rejects before writes, but its reason says `structure 1 has degenerate principal moments`. The loop enumerates the returned moments rather than reporting the source axis or explicitly naming a local selection position.

## Why

A user may inspect or repair the wrong structure. Numerical rejection, molecular coordinates, revision and coverage remain correct; this is an index-space diagnostic defect. The GUI must preserve the native reason rather than translate it. Report the actual source structure index, or explicitly label the selected-array position and its mapping. Cover nonconsecutive/reordered, repeated and all-structure native scopes. Preserve all-structure rejection before coordinate publication.

Related consumer: uibcdf/molsysviewer#315, provider work uibcdf/molsysmt#421.

## Evidence and acceptance

Observed on the native source retained in owner `aadefc11d`, during the new principal-axis GUI guard. The directed run's degenerate case and final combined 5,569-case run preserve coordinates/revisions; they expose the misleading native reason. Source location: `molsysmt/structure/align_principal_axes.py`, the loop over `moments`. No detector, eigensolver or GUI workaround is requested. A new regression should independently put the defective geometry in source structure 0, request `[2,0]`, and check that the reason identifies the correct index space.
