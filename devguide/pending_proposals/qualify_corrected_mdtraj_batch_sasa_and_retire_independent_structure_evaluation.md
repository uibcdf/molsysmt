---
summary: Qualify corrected MDTraj batch SASA and retire independent-structure evaluation
issue: uibcdf/molsysmt#530
status: open
opened: 2026-11-02
closed:
verification: inspected
area: [deps, performance, tests]
guard:
normative:
blocked_by: []
supersedes: []
---

# Qualifying corrected MDTraj batch SASA

## What

After a corrected upstream provider is available, qualify multi-structure MDTraj
SASA and retire MolSysMT's independent-structure adapter when it is safe and
measurably useful. This is future performance receiving, separate from the
correctness protection and current source qualification in #529/#255.

The implemented adapter in source de7ffad2a evaluates each structure separately
to avoid retained worker-area buffers in
[MDTraj #2195](https://github.com/mdtraj/mdtraj/issues/2195). It preallocates the
atomic result and uses a no-copy structure slice; it preserves provider identity,
scientific method, all-atom occlusion, order/repetitions and units. It adds
provider-call overhead and removes provider parallelism across structures.
The native compiled engine remains available for larger ensembles.

## How

1. Identify an actual published upstream source fix and corresponding installable
   artifacts; an issue milestone, merged proposal or version number alone is not
   evidence of corrected execution. Record exact versions/builds and relevant code.
2. Compare independent calls and candidate batched execution on analytic isolated
   spheres, variable overlap and realistic structures. Use more structures than
   OpenMP threads and explicitly test one/two threads; default many-core execution
   can hide the original buffer defect.
3. Measure provider-call cost, first/steady throughput and peak memory across
   representative atom/structure counts. Preserve output order/repetitions,
   atomic/grouped selections, all-atom occlusion and PyUnitWizard area policies.
4. Choose an explicitly supported provider compatibility route. Do not assume a
   new MDTraj release supports MolSysMT's complete Python 3.11–3.14 range, and do
   not raise public floors merely to remove the workaround. Older supported
   installations must retain a correct independent-structure path if needed.
5. Restore batching only for qualified providers and update the API notes,
   Foundations, Toolbox, Cookbook, relevant course pages and dependency contracts.
   Retain the real-provider worker-reuse guard permanently.

## Why

Current correctness is preferable to biased, worker-dependent solvent exposure.
Once upstream batching is fixed, repeated Python/provider calls can become
avoidable overhead. A deliberate qualification can recover parallel throughput
without silently accepting wrong areas or dropping older supported environments.
No performance improvement magnitude is claimed before measurement.

## What is measured and what is assumed

The original worker-buffer defect is independently reproduced and the current
protection is tested under #529. Its before/after evidence remains there.
No corrected future artifact, version floor, speedup or cross-platform batching
qualification is established by this proposal. Upstream #2195 was observed open
with milestone 1.12.0 on 2026-11-02; that is historical tracking context, not a
promise that this version contains a verified fix.

## What was refuted

Raising numerical tolerances, increasing the sampling density or testing only
as many structures as available threads does not fix retained worker state.
Changing global OpenMP policy is not a substitute for a correct provider, and
silently substituting the native engine would obscure the requested provider.

## Scope and exclusions

Post-1.0 performance receiving of the existing Cartesian MDTraj engine. No new
SASA method, radius/profile change, PBC capability, GPU backend or installed
release is authorized here. This work does not block closing the protected
adapter's correctness defect or the ChemicalStates refactor after their own
required gates pass.

## Acceptance criteria

- A published provider fix and exact executed artifacts are identified.
- Real-provider multi-structure results agree with independent/analytic oracles
  under constrained threads, varied counts, selections and unit policies.
- Existing scientific tolerances and all-atom occlusion remain unchanged.
- Measured performance/memory justifies the selected dispatch route.
- The complete supported Python/platform contract remains explicit and correct,
  including any retained older-provider path.
- Documentation and dependency surfaces agree, and the worker-reuse regression
  continues to protect both qualified and retained paths.

## Provenance

Opened after the 2026-11-02 source investigation of #529. Current source:
de7ffad2aef18ff3bccd184133dc69e081cb506e. No future benchmark or artifact result
is asserted; #529 owns original red/green and final-source qualification evidence.
