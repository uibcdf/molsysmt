---
summary: Independent minimization mutates an existing engine context before copy failure.
issue: uibcdf/molsysmt#588
status: open
opened: 2026-11-05
closed:
severity: high
verification: reproduced
area: [api, docs, tests]
guard:
normative:
blocked_by: []
supersedes: []
---

# Existing engine-context minimization ownership

## What

The default independent minimization request on an existing openmm.Context
minimizes the supplied context, then fails because the public Context copy
route is unimplemented. Failure does not preserve input coordinates. Both Context and Simulation reproduce this ownership failure in bounded execution.

## How

Main 1b359d441b899d26a06a6d927b809f770a09c462, Linux/Python
3.14.7/OpenMM 8.6.1; bundled alanine dipeptide, structure index 0, Reference.

```python
import molsysmt as msm
import numpy as np
puw = msm.pyunitwizard
molsys = msm.convert(msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'], structure_indices=0)
context = msm.convert(molsys, to_form='openmm.Context', platform='Reference')
before = puw.get_value(context.getState(getPositions=True).getPositions(asNumpy=True), to_unit='nm').copy()
try:
    msm.molecular_mechanics.potential_energy_minimization(context)
except Exception as error:
    print(type(error).__name__)
after = puw.get_value(context.getState(getPositions=True).getPositions(asNumpy=True), to_unit='nm')
print(np.max(np.abs(after-before)))
```

Observed: NotImplementedMethodError, then a maximum absolute coordinate change
of 0.07551541742736932 nm. The force-field/engine minimization ran before the
copy failure. The native MolSys independent/in-place path is checked separately
under #562 and is not the failing input form.

## Why and acceptance

An unsupported output/copy operation must be rejected before changing input.
Decide whether independent engine contexts should be cloned fully, or unsupported
routes preflighted, using existing form-copy/conversion ownership. Preserve actual
engine model, platform, positions, current cell, integrator/state semantics and
native diagnostics; do not silently switch to another form or physical recipe.
Test both Context and Simulation, default/explicit output paths, intentional
in-place editing and failure atomicity, using bounded actual engine execution.

## Scope and workaround

For the independent workflow, use a prepared native MolSys input. Existing
engine-context in-place execution must be deliberately requested and documented;
its successful contract does not excuse mutation on independent-mode failure.
No fix or new Context-copy support is claimed by the #562 course/doc correction.
The minimization docstring and tutorial disclose this boundary while this report
remains open. Related: #562, #421 and PR #543.

## Additional receiving — 2026-11-05

Actual Reference execution now also reproduces the independent-mode failure on
Simulation, with the same 0.07551541742736932 nm maximum absolute coordinate
component change. Explicit in_place=True succeeds and returns None on both
engine forms, deliberately changing coordinates. These are demonstrations of
current behavior, not a correction or permission to mutate an independent input.
The #562 receipt retains the four observations; no xfail or gate exemption is
introduced for this unresolved native defect.
