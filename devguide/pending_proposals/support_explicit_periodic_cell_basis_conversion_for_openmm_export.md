---
summary: Support explicit periodic-cell basis conversion for OpenMM export
issue: uibcdf/molsysmt#774
status: open
opened: 2026-11-17
closed:
verification: reproduced
area: [convert]
guard:
normative:
blocked_by: []
supersedes: []
---

# Exporting valid periodic cells in an OpenMM-compatible basis

## Observation

The [OpenMM capability study](openmm_openmmtools_capability_review_20261117.md)
confirmed a representation gap. MolSysMT constructs a valid row-vector cell with
lengths `[2, 2, 3] nm` and angles `[90, 90, 30] degrees`. The emitted rows in nm
are `(2, 0, 0)`, `(1.732051, 1, 0)`, and `(0, 0, 3)`, with volume
`6 nm³`. Public `MolSys → openmm.Topology` conversion for one selected atom
and structure raises OpenMM's reduced-form `ValueError`. Current export forwards
the box through `set_box_to_system`.

The independently constructed integer change of basis `b' = b - a` gives the
same lattice and produces the accepted second row `(-0.267949, 1, 0)`. The
pinned OpenMM `reducePeriodicBoxVectors` returns those same vectors. With the
reduced box selected on a detached system, conversion accepts the one atom.
The original coordinates and box are preserved. Executed on MolSysMT
`a57f4c51b4feafc54cad2677c862cae85c4e2534`, Python 3.14.7 and OpenMM 8.6.1.
This confirms a useful extension at the adapter boundary. The native factory
correctly represents the requested cell.

## Proposal

Review an explicit atom-independent lattice-basis operation owned by `pbc`
and an OpenMM-specific admission/export policy owned by the existing adapters.
The reusable operation should give the unit-bearing row-vector box and the
integer transformation between bases. Distinguish the integer basis change
from an orientation change. A rotated input requires a rigid rotation of
coordinates and all affected vector quantities, with an explicit mapping and
a coherent policy for fractional positions, stored images and derived analyses.
Start with a real consumer and the smallest admitted domain.

## Acceptance before implementation can be declared complete

- State which cell bases, handedness, degeneracies, units and per-structure
  shapes are accepted. Address exact tie cases and near-degenerate inputs.
- Preserve lattice translations and volume under the integer transform. Check
  rotation separately with analytical Cartesian and periodic distance controls.
- Keep the correct atom correspondence and original ownership for output forms.
  Handle fractional data and retained image/provenance fields explicitly.
- Exercise equivalent nm and pm inputs, empty and multiple structure axes where
  applicable, and one-structure OpenMM exports. Document that OpenMM's diagonal
  dimensions and original crystallographic vector lengths need not coincide.
- Keep explicit failure for unsupported cases. Do not silently change the
  general native box factory or normalize only the box when a rotation must
  also move coordinates and velocities.

This is a post-1.0 proposal. Existing compiled cell construction and geometry
are the starting point. Use small deterministic fixtures before considering
any new compiled code or performance work.
