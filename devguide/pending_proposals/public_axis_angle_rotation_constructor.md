---
summary: Provide a public axis-angle rotation constructor for molecular consumers.
issue: uibcdf/molsysmt#602
status: open
opened: 2026-11-06
closed:
verification: inspected
area: [structure, math, molsysviewer]
guard:
normative:
blocked_by: []
supersedes: []
---

# Public axis-angle rotation construction

## What

Viewer's approved Geometry design needs a unit-bearing angle and explicit axis
for Rotate. Request a supported standalone mathematical constructor from the
scientific owner. The owner chooses public placement/name and validation; this
report does not promote the private builder helper or add a GUI formula.

## How

On native ed09f6453, structure.rotate accepts proper matrices or an apply object.
lib.math exposes quaternion-to-matrix and Rodrigues primitives. The builder's
private _rotation_matrix_from_axis_angle has builder-specific near-zero identity
handling and no supported public unit/validation contract for this consumer.
The complete 597-record issue/PR inventory contained no equivalent proposal.

Existing primitive/matrix rotation receiving passes 50 cases (63 deselected,
17.18 s), with 51 legacy-H5MSM warnings and one expected invalid-determinant
warning. The selection is tests/lib/test_math_and_series_kernels.py plus
 tests/molsysviewer_molsysmt/test_structure_transform_tools.py, filtered by
rotation. Those tests qualify existing kernels/matrix rotation, not the proposed
axis/angle constructor, its invalid-input rules or a Rotate GUI.

## Why and proposed acceptance

A reusable conversion belongs to MolSysMT's mathematical owner and can reuse
its kernels. Require an unchanged finite nonzero real three-vector, an explicit
finite scalar angle with documented degree/radian semantics, and an independent
dimensionless proper 3x3 matrix. Document active right-handed rotation compatible
with row-vector coordinates @ R.T. Positive 90 degrees about +z maps +x to +y.
Reject zero/nonfinite/invalid input explicitly; do not infer units or identity.
Preserve application quantity policy and existing scientific APIs.

Guard signed axis quarter-turns, inverse/composition/periodicity, extreme axis
scaling, determinant/orthonormality, input ownership, units and invalid inputs.
The consumer separately owns centers per structure, selections/structure order,
fixed-box effects, native coverage, lifecycle and actual rendered receiving.
Native periodic wrapping and rotating the lattice are outside this utility.

This is a missing supported convenience, not a reproduced defect in the native
kernels or builder. The integration remains uibcdf/molsysmt#421 / PR #543 and
uibcdf/molsysviewer#264. Geometry centering and the other required task families
can proceed independently while this public contract receives owner review.
