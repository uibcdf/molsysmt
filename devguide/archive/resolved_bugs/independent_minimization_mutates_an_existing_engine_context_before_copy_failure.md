---
summary: Independent minimization mutates an existing engine context before copy failure.
issue: uibcdf/molsysmt#588
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: high
verification: reproduced
area: [api, form, docs, tests]
guard: tests/molecular_mechanics/potential_energy_minimization/test_potential_energy_minimization.py
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

## Resolution — 2026-11-05

**Contract-tested / actual engine execution.** Independent minimization now
resolves source forms and invokes the existing public copy contract for live
OpenMM inputs before any optimizer call. A composite containing a live engine
object follows the same rule. A requested output form/file cannot bypass source
ownership. Unsupported copy errors therefore propagate before optimization,
source-state modification or output-file creation. There is no catch/rebuild,
platform substitution or partial-State reconstruction.

Context and Simulation copying remain unsupported, with meaningful existing
NotImplementedMethodError metadata identifying the requested form. State copying
also receives a truthful diagnostic, including for snapshots without positions.
Its form already exists; no new form or independent runtime-copy capability is
introduced. Native MolSys independent/in-place workflows and explicit existing
engine in-place execution retain their behavior. The latter keeps the actual
model/platform and returns None, without a newly promised rollback after an
intentional in-place engine failure.

The public copy tool remains the reusable owner of detachment. No minimizer-local
clone, checkpoint rollback or snapshot cache is added. Runtime engine details
remain inside the selected OpenMM branch, not in native stored mechanical data.
Signatures/defaults, physical optimizer/force models, units, dependency floors,
H5MSM and compiled kernels are unchanged. No new scientific criterion or Ackredit
event is introduced for the ownership correction.

### Primary-source review and future copying

The supplied OpenMM source at ba0aa236ac4d07241382869604c4d2ea58c4f3f5
was inspected. Context.h distinguishes requested State fields and incomplete
setState restoration from environment/model/platform-dependent checkpoints;
TestPickle exercises System, Integrator and State serialization separately.
These mechanisms do not establish a general independent runtime copy contract.
Copying positions alone would lose model/integrator/runtime information. A
Simulation also has topology and reporter/workflow ownership to define.

That separate reusable capability is now #592, including partial State fields,
System/Context synchronization, runtime fidelity, platform properties and
reporters. It follows the current safety queue unless a concrete consumer changes
its priority. #588 is resolved by the acceptance-permitted early refusal; full
Context/Simulation/State copying is not claimed.

### Regression controls and receiving

The red guard on source 80ec9c1928a4dd43865c81a02ffab2f9a22c5959
fails for both forms: source State/checkpoint bytes change after the copy error
(2 failed, exit 1, 4.48 s). The final module has 29 cases: the nine existing
native/course controls plus 20 engine/snapshot cases. Default and explicit
outputs, file output, both composite source orders and deliberate in-place
execution are exercised using actual Reference contexts. Native mode/unit
controls also execute CPU.

Rejection guards compare serialized State, System and Integrator, same-live-
context checkpoint bytes and platform; they verify that the optimizer is not
called. The fixture includes nondefault time, step count, velocities, current
box, a current global parameter, a fixed integrator seed/constraint tolerance
and Simulation reporters. Explicit in-place execution decreases this bounded
fixture's energy and changes positions while retaining its other state/model/
platform and None return. Partial/full State copy rejection preserves captured
fields. Snapshot/checkpoint creation is test evidence only, not product work or
a portable clone recipe. No GPU or cross-machine checkpoint qualification.

Final local receiving passes 1,847 affected tests (120.68 s), 318 published-
support-floor cases (16.25 s), 569 documentation/doctest controls (21.16 s)
and the seven-cell tutorial (11.6 s). Suites overlap. Runtime SMonitor stays
active; only its unrelated editable pytest entry point is excluded in the floor
run under #524. All original executable cells, outputs and metadata of nine
prose-only course/Cookbook/form notebooks are preserved. No full downloaded
preparation scenario, browser scene or installed release is qualified here.

Docstrings, Foundations, Toolbox, Cookbook, five relevant course lessons and the
three form pages describe early refusal consistently. Copy rows no longer
advertise unimplemented deep-copy support. Public basic.copy also distinguishes
recognition, conversion, snapshots and supported independent copying.
[The receipt](../../../devtools/data/engine_minimization_ownership_receiving_588_20261105.json)
retains commands, versions, hashes and primary-source identities.

### Queue and qualification boundary

Next native work: #583 and #584, then #589's course observable. The current PR
#543 owner receiving also retains #587 and the incoming real-Jupyter addon
reports #590 (completion outcome lifetime) and #591 (host definition-list CSS).
Those are separate addon boundaries, not reasons to patch native physics or
hide this source correction. #592 is a later capability proposal. Inspect this
unskipped source checkpoint's hosted controls; #334 retains missing runner/
installed/platform/release evidence. No tag, Release, promotion or new full
matrix is launched.
