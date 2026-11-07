---
summary: Provide a public axis-angle rotation constructor for molecular consumers.
issue: uibcdf/molsysmt#602
status: resolved
opened: 2026-11-06
closed: 2026-11-07
verification: measured
area: [structure, math, molsysviewer]
guard: tests/structure/test_get_rotation_matrix_from_axis_angle.py
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

## Owner implementation and receiving — 2026-11-07

### Implemented boundary

Expose `structure.get_rotation_matrix_from_axis_angle(axis, angle,
skip_digestion=False)` as an experimental reusable tool. One finite, nonzero,
unit-free real three-vector and an explicit degree/radian scalar produce a new
dimensionless float64 proper matrix. Positive 90 degrees about +z maps +x to +y;
row-coordinate application is `coordinates @ rotation.T`.

### How

Reuse the existing scale-safe vector normalizer and bundled nonmutating Rust
Rodrigues kernel on the Cartesian basis. This introduces no mathematical method,
backend or optional dependency, and does not change the private peptide builder's
own near-zero-axis policy. Original angular metadata is checked before unit
conversion: generic dimensionless quantities, percentages and bare numbers are
not guessed as angles. PyUnitWizard converts once to radians without changing
the application's policy. Axis/angle digesters are scoped to this public caller;
trusted internal delegation takes an already normalized axis and radians scalar.

The new expert-addon method preserves the native explicit-input signature and
can run on an open empty view. It does not bind/read/synchronize molecular data,
consume pending edits, change scene/history or take invented edit controls.
Returned matrices remain independent after view closure; new calls through a
closed view reject. A Geometry/Rotate graphical panel remains separate #421 work.

### Why

Clients should compose a provider-owned orientation constructor with the existing
rotation/center tools instead of copying a formula or requiring SciPy solely
to obtain a matrix. Scientific criteria remain in their owners. The docstring
identifies the reused mathematical kernel; no third-party software implementation
was copied and no new empirical scientific attribution is invented.

### Evidence and corrections

The first combined receiving has 255 passes and eleven failures among 266 cases.
Nine require the new angle diagnostic to identify its argument; that message is
corrected. One boolean fixture fails in quantity construction before reaching
MolSysMT; a supported zero-dimensional boolean array quantity now exercises the
actual rejection boundary. The final failure detects the existing XYZ transform
source-alias defect, reported separately as #633 rather than changing the source
preservation expectation.

After the selected-coordinate ownership correction, 324 combined cases pass
without errors, failures or skips. They include constructor contracts, signed
analytic matrices, unit-policy invariance, finite extreme axes, subnormal angles,
inverse/composition/periodicity, unchanged inputs, actual public row-coordinate
rotation, its doctest, expert input/lifetime/effect guards, existing native/edit
guards and the new #633 controls. Initial failed receipts remain available.
Minimum public-provider receiving and broader consumers/documentation execution
remain in progress; no installed or graphical Rotate acceptance is claimed.

The API registry marks the new boundary experimental. The scientific registry
explicitly includes its reviewed claim and independent analytic nodes; its
declaration status is not execution certification. User Guide, Cookbook,
Foundations and all four Module 46 paths receive examples and cross-links; new
notebook outputs must come from actual execution before lifecycle completion.

### Acceptance and limits

- Finish native, declared-minimum provider, expert-wrapper and affected consumer
  receiving without weakening source/geometry/unit/lifetime assertions.
- Execute the docstring, five affected notebooks and Cookbook; validate API,
  scientific registry, documentation/course and dependency contracts.
- Deliver reviewed source and durable receipts before closing this owner issue.
- #421 retains Geometry/Rotate GUI, actual fixed/per-structure centers and visible
  molecular coordinates, remaining task families, installed and human acceptance.
  This constructor reads no center/box/system and applies no wrapping or edit.
- Preserve existing phase weights and experimental classifications; no tag,
  Release, candidate or artifact promotion follows from this work.

### Completed local receiving — 2026-11-07

Declared public ArgDigest 0.14.0 / PyUnitWizard 0.28.1 receiving passes 76 new
native/analytic/expert/doctest cases. Broader geometry, complete addon and affected
executable documentation receiving passes 7,764 cases with zero omissions. The
registered scientific runner passes 107 cases across 68 nodes, explicitly on
modified development source with `release_eligible=false`.

All five changed notebooks now have actual execution: four pass in the initial
campaign, while the Antiviral example first exposes #634 and then passes after
its explicit inhibitor-chain correction. The original failure and separately
retained 6LU7 input controls remain available. HTML compilation exits zero with
six retained title-underline warnings: four previously observed warnings and two
in isolated copies of human-owned API stubs that are not altered by this work.

#633 and #634 are locally corrected/received; source delivery remains pending.
New #638 separately owns accepted XYZ rank/integer edit behavior, not this
matrix-construction boundary. #636 owns the independently reproduced untracked
Python/source-eligibility gap before exact-candidate certification. #635 requires
separate panel-guard receiving on the newer host and does not retroactively
qualify that host through this block's exact Viewer 25061d9e9 evidence.

The portable [combined receiving receipt](../../../devtools/data/axis_angle_and_transform_receiving_602_633_634_637_20261107.json) retains native exits, original failed attempts, source fingerprints and the separately incomplete candidate/host gates. All fourteen final fast source gates pass.

## Resolution — 2026-11-07

The correction is delivered on main in checkpoint
`684a5b0cb9991e0538a0bd55bc934a5b57719a97`. An independent, complete GitHub
API tree matches all 141 changed source/record paths against the local commit.
The guard named in this record protects the stated boundary; its receiving and
original failures are retained in the linked portable receipt. The earlier
local/pending statements describe prior stages, not the current disposition.

This closes this bounded correction only. #421 graphical/installed/human scope,
#524 public-host/installed closure and the separate #635/#636/#638 work remain
open. No final-candidate, stability promotion or release approval is implied.
