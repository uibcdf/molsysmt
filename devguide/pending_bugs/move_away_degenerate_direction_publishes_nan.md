---
summary: move_away publishes NaNs for degenerate directions.
issue: uibcdf/molsysmt#456
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

# move_away publishes NaNs for degenerate directions

**Reported:** 2026-10-25 during authorized addon receiving under
uibcdf/molsysmt#421 / uibcdf/molsysviewer#264.
**Status:** reproduced natively; correction belongs to the scientific owner.

## What

What — `structure.move_away()` publishes NaN coordinates when source/reference centers coincide (including its defaults), or when `direction=[0, 0, 0]`. No exception is raised.

How — On source fc2936bf9, Python 3.14/Linux, load bundled pentalanine and run either call on a fresh copy:
```python
import molsysmt as msm
import numpy as np
molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'], structure_indices=[0, 8, 3])
msm.structure.move_away(molsys, in_place=True)  # alternatively direction=[0, 0, 0]
assert np.isfinite(msm.pyunitwizard.get_value(msm.get(molsys, coordinates=True))).all()  # fails
```

## How

The native default uses the same population for source and reference, so its
automatic direction is zero. In molsysmt/structure/move_away.py the direction is
divided by its norm without validating it. Explicit zero vectors are normalized
similarly by molsysmt/_private/argdigest/argument/direction.py. Both routes
publish NaNs without a scientific exception.

On a fresh bundled pentalanine MolSys, structure.move_away(molsys, in_place=True)
or the same call with direction=[0, 0, 0] returns None, emits a RuntimeWarning
and leaves nonfinite coordinates on structure 0. The independent route and
other degenerate variants need owning scientific tests; this report does not
claim they were all measured.



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

Reject undefined/nonfinite directions before writes, or document and implement
an explicit accepted zero-displacement policy. Retain coordinates, box and
interaction coverage on rejection. Include native pytest across automatic and
explicit modes, independent/in-place results, references, weights and structure
scopes, alongside valid finite displacement checks.

## Provenance

Native source fc2936bf9efd198f02f1d195107e5a5e6f62d13b; Linux x86-64;
Conda molsyssuite@uibcdf_3.14, Python 3.14. Bundled
pentalanine/traj_pentalanine.h5msm, structure subset [0, 8, 3]. The fresh native
reproductions ran on 2026-10-25 and retain their original JSON in the receiving
receipt. No package installation or cross-platform qualification is asserted.
