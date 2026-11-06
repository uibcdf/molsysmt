# Periodic tools GUI — bounded native receiving

**Role:** operational qualification boundary for the source addon under #421 /
PR #543 and uibcdf/molsysviewer#264. **Date:** 2026-11-06.

Wrap coordinates and Unwrap trajectory delegate all image/reconstruction science
to public MolSysMT operations through existing managed/independent adapters.
The complete general-cell family remains required work; this interim source
slice is not a 1.0 clearance or an expert-API restriction.

## Interim admission and ownership

| Operation | Temporary source GUI admission | Owning prerequisite |
| --- | --- | --- |
| Wrap primary, centered-primary or nearest images | Stored lower-triangular row-vector cells (exact zero upper triangle). Components or atomwise grouping are explicit; selected cells may vary. | #607 general orientation |
| Unwrap temporal coordinates | Same orientation admission and identical box vectors across the selected structure sequence; at least two structures. | #606 changing cells and #607 orientation |
| Construct/assign a cell | Not registered yet; remains required before completion. | #605 physical factory validation |

The native owner is MolSysMT. The consumer admission belongs to this addon in
MolSysMT, with Viewer integration tracked in uibcdf/molsysviewer#264. Reassess
by **2026-11-13**, or immediately when a published native correction is available.
Remove each guard only after receiving the exact owner fix and independent
lattice/unit/order/atomicity tests for the formerly rejected cases. Keep the
remaining full-scope tasks visible; none is silently deferred past 1.0.

The orientation check is an explicit compatibility guard for a known broken
route. It is not a definition of all valid physical boxes. It uses no tolerance,
cell rotation, lattice reduction or replacement image algorithm. The fixed-cell
check is conservative while the native varying-cell contract is repaired.
Native public getters own box selection and quantity conversion. Invalid stored
cells still undergo native scientific validation before publication. Expert
wrappers retain native signatures, behavior and currently reported limits.

## Additional native reference-point blocker

Native #608 shows that atomwise primary wrapping can snap a small nonzero origin
with an application-unit-dependent threshold. The same [1e-5,0,0]-nm origin can
return x=0 nm under nm/angstrom policies and x=3 nm under pm. This issue remains
unrepaired in the prepared source; no consumer tolerance, origin replacement or
unit-policy override is added. Passing lattice tests for their stated origins
do not qualify this failed boundary case. **Do not publish or clear the periodic
family for 1.0 until the native fix and exact cross-policy receiving exist.**
The source GUI remains experimental/partial, not a general scientific readiness
claim. Native correction is owned by MolSysMT and is part of the same
2026-11-13-or-earlier review/removal checkpoint.

## Effects and required evidence

Preview freezes resolved atom populations, structure order and exact request
parameters without copying coordinates. Confirmation revalidates within the
managed edit lock. Independent results copy the whole molecular system and
change only selected atoms/structures. Boxes are retained. Compact wrapping uses
provided bonds among selected atoms, never inferred connectivity; component
centers can be in the cell while atoms extend outside it. Temporal unwrapping
is per atom and does not reconstruct a split molecule in one structure.

Use independent fractional/lattice-enumeration controls for canonical orthogonal
and representative triclinic cells, explicit origins/centers, changing wrap
cells, nonconsecutive order, fixed-cell temporal sequences, units and component
reconstruction. Verify coverage, unchanged source/unselected data, stale/single-
use review, native rejection without partial writes and projection-only retry.
Real Mol*/Jupyter/popup receiving remains separate from human and installed
qualification. The source profile makes no universal periodic-accuracy claim.
