---
summary: Centered periodic wrapping ignores the original in-place target.
issue: uibcdf/molsysmt#467
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: high
verification: reproduced
area: [pbc, structure]
guard: tests/pbc/test_centered_wrapping_ownership.py
normative:
blocked_by: []
supersedes: []
---

# Centered periodic wrapping ignores the original in-place target

**Reported:** 2026-10-26, authorized after a native-only audit during addon
receiving under uibcdf/molsysviewer#264 / uibcdf/molsysmt#421.

## What

Both `pbc.wrap_to_pbc` and `pbc.wrap_to_mic` return None but leave the original
coordinates intact with `center_of_selection` and `in_place=True`:

```python
import numpy as np
import molsysmt as msm
puw = msm.pyunitwizard
molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
                     to_form='molsysmt.MolSys', structure_indices=[0, 8, 3])
coordinates = puw.get_value(msm.get(molsys, coordinates=True), to_unit='nm')
msm.set(molsys, coordinates=puw.quantity(coordinates + [8, 7, 6], 'nm'),
        box=puw.quantity(np.tile(np.eye(3)*3, (3, 1, 1)), 'nm'))
before = puw.get_value(msm.get(molsys, coordinates=True), to_unit='nm').copy()
options = dict(selection=[0, 1, 2, 3], structure_indices=[2, 0],
               center_of_selection=[0, 1], compact=False)
independent = msm.pbc.wrap_to_pbc(molsys, **options)
msm.pbc.wrap_to_pbc(molsys, in_place=True, **options)
after = puw.get_value(msm.get(molsys, coordinates=True), to_unit='nm')
assert not np.array_equal(after, before)  # fails: no original coordinate changes
```

Repeat with `wrap_to_mic`. With no centering, both in-place calls agree with
the independent route and do change the original coordinates.

## How

Both functions rebind `molecular_system` to `center(..., in_place=False)`, then
publish the wrapping result into that detached copy. The original object is
no longer the write target. Returning None hides the detached scientific result.

## Why

An expert caller expects an in-place edit to affect its supplied system. The
addon cannot announce completed science and synchronize the current primary
when that scientific target was silently ignored. Its managed receiving
rejects this known combination before writes, without implementing an alternate
centering or wrapping algorithm. Independent centered output remains useful.

## What is measured and what is assumed

Pure native audit `/tmp/msv-pbc-edits-native-audit.json` records all four
method/centering controls and source hashes. Both centered calls have a maximum
9.686439514160156 nm discrepancy against their independent counterpart; both
original systems are byte-for-byte unchanged. No scientific coordinate
corruption is claimed. The audit source is the currently reviewed provider
63a70b2e7; Viewer is not imported or called in that audit.

## What was refuted

The uncentered controls execute in place correctly. The centered independent
outputs change and preserve their inputs. This isolates target ownership from
rendering, validation, missing boxes or a general failure to wrap coordinates.

## Scope and exclusions

Repair the native original-target contract. Viewer receiving stays separate;
no implicit preparation, manual array copyback or substitute PBC kernel is added.

## Acceptance criteria

Cover both wrappers, centered/uncentered, independent/in-place, atom-wise and
component modes, units and ordered structure scopes with native pytest tests.
Assert actual target/source coordinates, native returns, preserved boxes,
retained topology identity and exact edited-structure analysis invalidation.
An assertion only on a returned independent system cannot guard this defect.

## Provenance

Linux/Python 3.14 in `molsyssuite@uibcdf_3.14`; bundled 62-atom pentalanine,
three structures selected as [0, 8, 3], cubic 3 nm boxes and explicit shifts.
Raw audit and exact source hashes are retained with addon receiving evidence.

## Resolution — 2026-10-26

Both wrappers keep the original argument as their final in-place publication
target and use a separate centered working system for computation. Independent
centered output reuses that working system, avoiding the former second complete
system copy. No periodic geometry kernel, centering criterion or public
signature changes. Native coordinate setters retain exact edited-structure
analysis invalidation; evaluated-empty structures are covered explicitly.

The guard compares actual original/output coordinates with independent
orthogonal-cell arithmetic for primary boxes, shifted origins, box centers and
MIC, with atom-wise and two covalent-component populations. It covers MolSys,
Structures and StructuresDict, nm/pm standards, nonconsecutive/repeated structure
lists, selected/unselected atoms, original topology identity and boxes, previous
analysis snapshots, rejected centering/box validation and the one-copy bound.
The original pre-fix guard run had 48 native numerical failures from the wrong
in-place target; its separate 64 dictionary failures are resolved under
uibcdf/molsysmt#472. Four invalid-box test expectations were corrected before
that final baseline because assigning the invalid box itself legitimately
invalidated analyses before the wrapping call. The recorded baseline is
112 failures and 152 passes, not a successful qualification.

Public docstrings, PBC tutorials, Foundations, Cookbook, course Module 19 and
[native structural rules](../../native_structures_contract.md) describe ownership.
The addon intentionally rejects this combination until its separate reception
adopts the native repair; provider success alone does not qualify Viewer.

## Qualification receipt — 2026-10-26

The integrated PBC/centering/translation/dictionary/argument/documentation
selection passes **1,121 tests** in 45.92 seconds with `--receptor=llm -n 12`,
without skips (13 intentional legacy-H5MSM warnings). Four source modules pass
all 27 doctest examples. All five modified executable notebooks run successfully.
The Cookbook change is explanatory prose; its pre-existing solvation workflow
was not newly executed. Ruff and format checks, 251-function docstring validation
and all fourteen fast repository gates pass. Incremental Sphinx HTML completes
without errors and with 29 existing heading/toctree warnings; no warning-free
full build or installed release qualification is claimed.

Commands, environment, tested source hashes, fixture bindings and limitations
are retained in the [PBC repair receipt](../../../devtools/data/pbc_repairs_20261026.json).
