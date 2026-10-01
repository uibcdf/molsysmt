---
summary: Initializing a missing periodic box through set silently does nothing
issue: uibcdf/molsysmt#268
status: resolved
opened: 2026-10-01
closed: 2026-10-01
severity: high
verification: reproduced
area: [basic, attribute, units, tests]
guard: tests/native/test_set_missing_box.py::test_full_box_assignment_initializes_missing_series_with_units
normative:
blocked_by: []
supersedes: []
---

# Initializing a missing periodic box through set silently does nothing

**Reported:** 2026-10-01, while executing the pi-pi tutorial tracked by
uibcdf/molsysmt#265.
**Status:** Resolved. Full-axis setters initialize the missing series; partial
initialization fails explicitly. Native/public unit and read-only guards pass.

## What

A native system with coordinates but no periodic boxes accepts a full box
assignment without storing it:

```python
import numpy as np
import molsysmt as msm
from molsysmt.native import Structures

molsys = Structures(coordinates=msm.pyunitwizard.quantity(np.zeros((2, 1, 3)), 'nm'))
msm.set(molsys, box=msm.pyunitwizard.quantity(np.repeat(np.eye(3)[None], 2, axis=0), 'nm'))
assert molsys.box is not None
```

Before the repair the assertion fails. The same native early-return affects
Structures.set_box, MolSys forwarding and msm.set. Existing-box updates work.

## How

Structures.set_box returned immediately whenever its internal _box was None,
including a valid full assignment. The public dispatcher already finds the
writable native route; include_none fallback is not the cause. The repair sends
full-axis assignments through the existing unit-aware property setter before
checking whether a series exists. Partial updates require an existing series;
empty partial requests remain no-ops. Existing partial updates retain read-only
array handling and explicit nm extraction.

## Why

The user can believe periodic geometry was initialized while calculations still
see no box. Detectors with an explicit mic_when_box_available policy can then
return nonperiodic observations. The issue is a silent setter failure, not an
error in MIC geometry or a change to the detector's documented missing-box policy.

## What is measured and what is assumed

The reproduction above fails on the preceding implementation. Five focused
parameterized cases now pass across native Structures, Structures-only MolSys,
public setters, Angstrom input, expected nm values, fixed frame counts,
read-only buffers and partial initialization rejection/update. The combined
native/pi-pi molecular checkpoint passes 103 tests. The executed pi-pi tutorial
now obtains the expected image [0,0,0]/[-1,0,0] through public box assignment.
This does not certify every optional observable's missing-value setter.

## What was refuted

Separate versus combined public assignments do not repair the failure: both
reach the native early return. The dispatcher can find the route, so changing
attribute discovery would not solve the native failure.

## Scope and exclusions

Only periodic box assignment is repaired. Full-axis clearing and existing
partial updates retain their native semantics. No missing-frame periodic values
are invented; nonempty partial initialization raises StructuralInconsistencyError.
Other optional observables and general coordinate reconstruction are outside scope.

## Resolution

Full box initialization uses the existing property setter, preserving input
units and read-only canonical storage. Tests/native/test_set_missing_box.py
asserts actual stored values, not successful dispatch alone. Foundations, the
public set tutorial and the executed periodic pi-pi example describe/verify the
full-versus-partial contract. The guard fails if full assignment becomes a no-op.

## Provenance

Local editable MolSysSuite Python 3.13 environment, Linux, 2026-10-01. Validation:

```bash
python -m pytest --receptor=llm tests/native/test_set_missing_box.py tests/native/test_structures_extended.py tests/interactions/pi_pi tests/scientific_truth/curated/test_pi_pi_interactions.py --disable-warnings
```
