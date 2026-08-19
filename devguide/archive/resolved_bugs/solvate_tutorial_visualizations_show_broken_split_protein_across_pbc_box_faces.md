---
summary: solvate tutorial 3D views show broken/split protein across periodic boundary faces
issue: uibcdf/molsysmt#162
status: resolved
opened: 2026-08-17
closed: 2026-08-19
verification: reproduced
severity: medium
area: [build, docs]
guard:
normative: devguide/INTERFACES.md
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

## Resolution — 2026-08-19

Not a rendering problem and not a missing centering step. **Two parts of MolSysMT
disagreed about where the box is.**

`solvate` returned the whole system centred on the origin while `wrap_to_pbc` wraps
into `[0, L)`. The tutorial chained them, and that is what split the solute.

Measured on 1VII solvated in a 4.93 nm cubic box:

| | longest solute bond | bonds over 0.3 nm | atoms outside |
| --- | --- | --- | --- |
| after `solvate` | 0.181 nm | 0 | 86.5 % |
| after `wrap_to_pbc` as the page called it | 6.863 nm | 93 | 0 % |

The peptide left `solvate` intact. Wrapping it atom-wise while it straddled the
origin is what stretched 93 bonds to 6.86 nm in a 4.93 nm cell.

### What was refuted

*PBC coordinates are mathematically consistent and the problem is only visual.* The
report says so and it is wrong: 93 bonds of the solute were stretched in the data,
not in the drawing.

*The page fails to centre the system before viewing.* It centred it. The centroid
landed within 0.045 nm of the box centre — because a molecule smeared across the
whole cell has its centroid in the middle.

*`solvate` leaves the solute at a box vertex while the waters fill the cell.* Both
were centred on the origin: 87 % of water atoms were outside the box too. It is the
whole system, not the solute.

### What changed

`INTERFACES.md` now states the convention, since its absence is what let the two
sides diverge. The choice is measured rather than assumed: OpenMM's
`enforcePeriodicBox` returns `[0, 4.93]` on this system and MDTraj's
`image_molecules` moves it into `[0, 5.00]`, both with the same ±0.07 nm overhang
that keeping molecules whole produces. There is no computational argument either
way — the MIC kernels work on displacement vectors, invariant under the origin.

`solvate` applies the placement its native engine already performed, at all three
returns. Atoms outside the cell afterwards: OpenMM 86.5 % to 0.9 %, PDBFixer 86.3 %
to 1.7 %, native 0.7 % to 0.9 %.

The page no longer wraps. It shows what `solvate` returns and explains why molecules
overhang the faces, and points at `wrap_to_pbc(..., compact=False)` for a reader who
wants every atom inside the cell.

### Related

The wrapping argument was renamed in the same session: `keep_covalent_bonds` became
`compact`, defaulting to `'component'`, so the call the page used no longer splits
molecules by default either.
