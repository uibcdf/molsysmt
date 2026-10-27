---
summary: is_solvated fails for multiple structures with waters and periodic boxes.
issue: uibcdf/molsysmt#504
status: open
opened: 2026-10-27
closed:
severity: medium
verification: reproduced
area: [build, molsysviewer]
guard:
normative:
blocked_by: []
supersedes: []
---

# Multi-structure native solvation predicate

**Reported:** 2026-10-27 during expert-addon receiving under uibcdf/molsysmt#421.
**Status:** open; native scientific-contract decision and repair required.

## What

`molsysmt.build.is_solvated()` raises `ValueError` for a resident MolSys with multiple structures, indexed waters and a periodic box. The equivalent one-structure input returns True. Native 4e544cb12dd6bb7738da651827f3b69fa5847a9c, Python 3.14; independently reproduced without Viewer calls while receiving the expert addon under uibcdf/molsysmt#421 / uibcdf/molsysviewer#264.

## How

The synthetic coordinates intentionally do not model equilibrated water: this tests only the function's documented water-count/box-volume predicate. Each unit box is 1 nm³ and contains 16 declared waters.

```python
import numpy as np
import molsysmt as msm
puw = msm.pyunitwizard
for n_structures in [1, 2]:
    builder = msm.MolSysBuilder()
    for _ in range(16):
        oxygen = builder.add_atom(atom_name="O", atom_type="O")
        first = builder.add_atom(atom_name="H1", atom_type="H")
        second = builder.add_atom(atom_name="H2", atom_type="H")
        builder.add_group([oxygen, first, second], group_name="HOH")
        builder.add_bond(oxygen, first)
        builder.add_bond(oxygen, second)
    builder.set_coordinates(puw.quantity(np.zeros((n_structures, 48, 3)), "nm"))
    builder.set_box(puw.quantity(np.repeat(np.eye(3)[None], n_structures, axis=0), "nm"))
    molsys = builder.build()
    try:
        print(n_structures, msm.build.is_solvated(molsys))
    except Exception as error:
        print(n_structures, type(error).__name__, str(error))
```

Observed:

```text
1 True
2 ValueError The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
```

The implementation compares `density_number > 15` in a Python `if`; the multi-structure box-volume array cannot be interpreted as one truth value. It has no public structure-selection argument. No scientific workaround has been added to the addon.

## Why

Users need an explicit and reliable contract for trajectories/ensembles. Please decide and document per-structure output versus an explicit aggregation/selection contract; silently choosing first/any/all would change the scientific meaning. Preserve the single-structure density threshold, units, water/box prerequisites and native argument validation. Test multiple structures with densities above/below/equal to the threshold, mixed densities, no waters/box and equivalent length units, with supported shape and error behavior explicit.

## What is measured and what is assumed

The standalone native reproduction on 4e544cb12, Python 3.14, returns True for
one structure and the quoted ValueError for two. Inputs use identical 1 nm cubed
boxes with 16 indexed O-H-H groups. This is a predicate/shape test, not a
simulation, a water-density model benchmark or a physical solvation claim.

## What was refuted

No Viewer callback, scene state or wrapper computation is required to reproduce
it. Water absence does not expose the branch because native logic short-circuits.
The source cause is the scalar Python condition applied to multiple box volumes;
there is no evidence that selecting a first structure or silently reducing the
array would match the intended scientific contract.

## Scope and exclusions

Native build.is_solvated and its expert bound reader only. No solvation,
coordinate generation, periodic reconstruction or automatic scientific repair is
implemented in this receiving. The addon delegates native outcomes unchanged.

## Acceptance criteria

Define the public multi-structure result/selection/aggregation contract, retain
single-structure behavior and test it with native pytest. Include above/equal/
below/mixed thresholds, no waters/box, length-unit equivalence and supported
shape/error cases. Supply a failing-before/passing-after native guard before
closing; receive the result separately in the addon without a consumer formula.

## Dependencies and risks

The decision belongs to MolSysMT. An implicit first/any/all reduction would change
meaning. The current addon documents the limitation; no publication or universal
multi-structure qualification is claimed.
