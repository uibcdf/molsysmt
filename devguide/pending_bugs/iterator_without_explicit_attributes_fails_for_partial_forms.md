# Iterator Without Explicit Attributes Fails for Partial Forms

## Status

Open. Discovered during the F2 notebook-execution audit on 2026-07-28.

## Public Contract

`molsysmt.Iterator` documents that, when no attributes are requested, each
iteration yields a molecular system whose structural data are updated for the
current chunk.

## Reproducers

The following two constructions fail before yielding an item:

```python
import molsysmt as msm
from molsysmt import systems

villin = [
    systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.h5msm'],
    systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.dcd'],
]
msm.Iterator(villin, chunk=10)

popc = systems['POPC membrane']['popc_membrane.dcd']
msm.Iterator(popc, chunk=20)
```

## Observed Causes

The composite case calls `convert(..., structure_indices=None)` while creating
the reusable output object. The H5MSM reader treats `None` as an iterable of
indices and raises `TypeError`.

The coordinate-only DCD case requests the implicit series `structure_id`,
`time`, `coordinates`, and `box`. At least one unavailable attribute resolves
to no source item, leaving `tmp_iterator` unassigned before it is appended and
raising `UnboundLocalError`.

## Impact

Explicit structural iteration, such as
`Iterator(system, chunk=10, coordinates=True)`, works and is sufficient for the
current scalability course examples. The documented molecular-system-yielding
mode is nevertheless broken for important partial and composite forms.

## Proposed Resolution

1. Normalize `structure_indices=None` consistently to the complete structure
   axis before conversion and form dispatch.
2. Define how implicit output handles unavailable optional structural series:
   omit them or preserve them as absent, rather than constructing an
   uninitialized iterator.
3. Add public regressions for a coordinate-only DCD and a
   topology-plus-trajectory composite.
4. Verify that yielded chunks preserve atom selection, structure order, units,
   and the single-state classical-dynamics association.

This bug is not an F2 blocker because the affected course examples request
coordinates explicitly. It should be prioritized after the 1.0 release gate
unless another Tier-1 workflow depends on the implicit-output mode.
