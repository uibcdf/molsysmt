---
summary: move_away rejects multiple structures after partial publication.
issue: uibcdf/molsysmt#457
status: open
opened: 2026-10-25
closed:
severity: high
verification: measured
area: [structure]
guard:
normative:
blocked_by: []
supersedes: []
---

# move_away rejects multiple structures after partial publication

**Reported:** 2026-10-25 during authorized addon receiving under
uibcdf/molsysmt#421 / uibcdf/molsysviewer#264.
**Status:** reproduced natively; correction belongs to the scientific owner.

## What

What — Explicit-direction `structure.move_away(..., in_place=True)` can modify coordinates before raising `NotImplementedMethodError` for multiple structures.

How — Reproduced without Viewer on source fc2936bf9, Python 3.14/Linux:
```python
import molsysmt as msm
import numpy as np
p = msm.pyunitwizard
molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'], structure_indices=[0, 8, 3])
before = p.get_value(msm.get(molsys, coordinates=True), to_unit='nm').copy()
try:
    msm.structure.move_away(molsys, selection=[0, 2, 4], center_of_selection=[0, 2],
        reference_center_of_selection=[1, 3], structure_indices=[2, 0],
        direction=[1, 0, 0], in_place=True)
except Exception as error:
    print(type(error).__name__)  # NotImplementedMethodError
assert np.array_equal(before, p.get_value(msm.get(molsys, coordinates=True), to_unit='nm'))  # fails
```

## How

The explicit in-place route in molsysmt/structure/move_away.py calls native
center before checking the supported single-structure direction/coordinate
shapes. With moving atoms [0, 2, 4], source [0, 2], reference [1, 3], selected
structures [2, 0] and direction [1, 0, 0], it raises NotImplementedMethodError
after changing coordinates on structures 0 and 2. If initial source/reference
centers happen to coincide, that example can look like a no-op; distinct
populations make the partial write visible.



## Why

Public coordinate editing can publish invalid or incomplete scientific results.
The addon cannot infer rollback or add an alternate scientific algorithm. Only
single-structure nondegenerate displacement receives positive qualification.

## What is measured and what is assumed

The pure-MolSysMT reproduction script and JSON are retained in temporary source
receiving evidence. The issue reproduction uses the same bundled pentalanine
file, structure subset and arguments. No Viewer call is required for the defect.
The report does not certify every direction/weight/reference combination.

## What was refuted

This is not a frontend or synchronization failure. It reproduces before any
viewer or addon participates. Existing successful single-structure tests do not
exercise these failing populations or axes.

## Scope and exclusions

The native move_away boundary owns the repair. No runtime observer, automatic
scientific replay, fallback method, or new molecular Undo is requested.

## Acceptance criteria

Check unsupported cases before publication or implement the broader native
contract explicitly. Add pytest for auto/explicit direction, copy/in-place,
scalar/list/nonconsecutive/repeated structures, reference shape combinations and
coordinate/box/interaction preservation on rejection. Native valid single
structure behavior must remain covered. This receiving does not demand new
multi-structure support; pre-write rejection is sufficient.

## Provenance

Native source fc2936bf9efd198f02f1d195107e5a5e6f62d13b; Linux x86-64;
Conda molsyssuite@uibcdf_3.14, Python 3.14. Bundled
pentalanine/traj_pentalanine.h5msm, structure subset [0, 8, 3]. The fresh native
reproductions ran on 2026-10-25 and retain their original JSON in the receiving
receipt. No package installation or cross-platform qualification is asserted.
