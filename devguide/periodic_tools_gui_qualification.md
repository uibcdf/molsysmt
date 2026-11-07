# Periodic tools GUI — bounded native receiving

**Role:** operational qualification boundary for the source addon under #421 /
PR #543 and uibcdf/molsysviewer#264. **Date:** 2026-11-06.

Wrap coordinates and Unwrap trajectory delegate all image/reconstruction science
to public MolSysMT operations through existing managed/independent adapters.
The complete general-cell family remains required work; this interim source
slice is not a 1.0 clearance or an expert-API restriction.

## Interim admission and ownership

| Operation | Temporary source GUI admission | Remaining consumer receiving |
| --- | --- | --- |
| Wrap primary, centered-primary or nearest images | Stored lower-triangular row-vector cells (exact zero upper triangle). Components or atomwise grouping are explicit; selected cells may vary. | Receive the owner [#607 correction](archive/resolved_bugs/periodic_wrapping_rotated_basis.md). |
| Unwrap temporal coordinates | Same orientation admission and identical box vectors across the selected structure sequence; at least two structures. | Receive the owner [#606 transition-cell correction](archive/resolved_bugs/unwrap_changing_cell_classification.md) and #607. |
| Construct/assign a cell | Not registered yet; remains required before completion. | Receive the owner [#605 factory validation](archive/resolved_bugs/box_factory_physical_domain.md) in the graphical task. |

The native owner is MolSysMT. The consumer admission belongs to this addon in
MolSysMT, with Viewer integration tracked in uibcdf/molsysviewer#264. Reassess
by **2026-11-13**, or immediately when a published native correction is available.
Remove each guard only after receiving the exact owner fix and independent
lattice/unit/order/atomicity tests for the formerly rejected cases. Keep the
remaining full-scope tasks visible; none is silently deferred past 1.0.

The owner has delivered the native corrections. The orientation and fixed-cell
checks remain unchanged in this isolated reconciliation until their exact
consumer receiving. They are not definitions of all valid physical boxes. They
use no tolerance, cell rotation, lattice reduction or replacement image algorithm.
Native public getters own box selection and quantity conversion. Invalid stored
cells still undergo native scientific validation before publication. Expert
wrappers retain native signatures, behavior and currently reported limits.

## Reference-point owner correction and consumer receiving

The original #608 counterexample showed atomwise primary wrapping snapping a
small nonzero origin with an application-unit-dependent threshold. The owner
has delivered the [native correction](archive/resolved_bugs/periodic_origin_unit_policy.md).
This reconciliation preserves the original receiving evidence and adds no
consumer tolerance, origin replacement or unit-policy override. Combined
cross-policy consumer receiving remains due. **Do not clear the periodic family
for 1.0 from the native fix alone.**
The source GUI remains experimental/partial, not a general scientific readiness
claim. Review the retained admission immediately against the delivered owner
source, preserving the original 2026-11-13-or-earlier review/removal checkpoint.

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
