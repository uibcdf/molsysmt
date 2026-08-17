---
summary: solvate tutorial 3D views show broken/split protein across periodic boundary faces
issue: uibcdf/molsysmt#162
status: open
opened: 2026-08-17
closed:
verification: asserted
severity: medium
area: [build, docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# `solvate` tutorial 3D views show broken/split protein across periodic boundary faces

**Reported:** 2026-08-17 during User Guide audit of `docs/content/user/tools/build/solvate.ipynb`.
**Status:** Open defect under investigation.

## What

In `docs/content/user/tools/build/solvate.ipynb`, 3D static views generated for solvated systems (e.g. `1VII` solvated in cubic and truncated octahedral boxes) display protein chains split across periodic boundary box faces instead of being compactly centered.

While PBC coordinates are mathematically consistent and valid for simulation engines, rendering fractured protein segments across opposite faces of the box is unappealing for documentation readers and user guide tutorials.

## How

When `msm.build.solvate` or `msm.pbc.wrap_to_pbc` is invoked without prior molecular centering (`msm.pbc.wrap_to_mic` or `msm.structure.center`), atoms wrapping across PBC box faces fragment the visual representation of the protein.

## Why

Molecular visualization in tutorial notebooks must be clear, compact, and aesthetically pleasing. Solvated protein views should demonstrate whole, intact protein structures centered within the periodic water box.
