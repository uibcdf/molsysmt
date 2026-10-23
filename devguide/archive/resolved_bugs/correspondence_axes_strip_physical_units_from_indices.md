---
summary: Correspondence axes strip physical units from positional indices
issue: uibcdf/molsysmt#433
status: resolved
opened: 2026-10-23
closed: 2026-10-23
severity: medium
verification: reproduced
area: [argdigest, units]
guard: tests/test_correspondence_axis_units.py
normative:
blocked_by: []
supersedes: []
---

# Correspondence axes strip units before validating positions

**Reported:** 2026-10-23 while qualifying explicit name projection under #223.
**Status:** Resolved; all shared public axes reject unit wrappers before work.

## What

`topology.get_atom_correspondences` accepts a length quantity containing integer
values as a positional atom selection. A prepared methanol graph with
`selection=quantity(array([0, 1], dtype=int), 'nm')` emits UnitStrippedWarning and
returns correspondences of shape (1, 2, 2), rather than rejecting the input.
The new naming boundary reproduced the same acceptance.

## How

The shared `_correspondence_axes.flat_axis` casts with `np.asarray` before
checking type/shape. Quantity-backed integer arrays lose their unit and satisfy
the flat integer-index test. It serves correspondence and symmetry-RMSD atom
and structure axes, mapped pose structure indices, and the new name selection.

The repair must reject quantity objects before casting. Both dimensionful and
explicit dimensionless quantities are rejected: these APIs require plain index
values, not a quantity-valued population. This changes no physical-unit
conversion or scientific criterion. No Ackredit calculation boundary is added.

## Why

A molecular length and an atom position are different inputs even when both
contain zero or integer-valued numbers. Silently converting units to indices
admits an unintended calculation rather than protecting the user's intent.

## Acceptance criteria

- Every public caller of this helper rejects quantity-backed atom/structure
  indices before scientific work or label projection.
- No unit-stripping warning is emitted on rejection.
- Plain integer axes and shaped empty arrays retain their supported contracts.
- Valid correspondence, symmetry-RMSD and mapped-pose regressions continue passing.

## Verification

Guard: tests/test_correspondence_axis_units.py. The corrected regression has nineteen failures and two passes before repair:
eighteen public cases reach patched scientific/label kernels, and a list holding
a dimensionless scalar quantity is accepted. Two controls already pass: rejected dimensionful list membership and
plain/empty integer-axis support.
After repair all 21 cases pass. Warnings are recorded and must remain empty;
no warning-as-error conversion can satisfy the expected ArgumentError.

The final combined selection passes 765 tests, no failures/skips, in 42.60 seconds
with twelve workers and Pytest Receptor. Valid correspondence, symmetry-RMSD,
pose, preparation and native-copy paths are included. All 35 warnings are known
legacy/dependency/structural-drop notices, with no unit-stripping warning.
The correspondence and symmetry-RMSD tutorials execute in 16.8/13.2 seconds;
public docstrings explain plain positional indices. No public signature changes.
The [receipt](../../../devtools/data/atom_name_projection_20261023.json) records
commands and source hashes.
Coverage is bounded to the shared flat-axis helper;
it is not a claim to audit every index argument in the library.
