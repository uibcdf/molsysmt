---
summary: Full-system writers silently discard report-only mechanical provenance
issue: uibcdf/molsysmt#660
status: active
opened: 2026-11-08
closed:
severity: medium
verification: reproduced
area: [form, data]
guard:
normative:
blocked_by: []
supersedes: []
---

# Report-only mechanics can disappear during complete-system serialization

## What

A native MolecularMechanics may carry partial_charge_assignment or
atom_type_assignment while its projected parameter values are all None.
H5MSM 0.5 and MolSysDict 0.2 accept this object and reconstruct both report
fields as None. They should refuse unsupported mechanical state rather than
silently omit it. This is separate from #256's future format design, which the maintainer now
permits before 1.0.

## How

The bounded probe uses runtime source
`fab8cbccf570a60205a3863aad19dd4b7cfb8d3a`; only receiver/tests/docs are modified.
A one-atom native system receives one report field with an explicitly synthetic
stale mapping. This is a negative fixture, not a valid chemical assignment.
All four field/transport combinations accept and lose that mapping on read.

```python
import molsysmt as msm
from molsysmt.native import MolSys

molsys = MolSys(n_atoms=1)
molsys.molecular_mechanics.partial_charge_assignment = {
    'schema': 'manual-negative-probe', 'status': 'stale',
    'note': 'not a scientific assignment',
}
payload = msm.convert(molsys, to_form='molsysmt.MolSysDict')
restored = msm.convert(payload, to_form='molsysmt.MolSys')
assert restored.molecular_mechanics.partial_charge_assignment is None
```

`MolecularMechanics.to_dict()` is intentionally a parameter projection. The
complete-system encoders use its values as an emptiness test, so recognized
non-parameter reports are invisible. The omission affects both full/partial
H5MSM branches and the native typed dictionary boundary; their exact affected
routes need explicit guards in the correction.

## Why

A successful complete-system write must not claim that unsupported stored
mechanical evidence survived. No corruption of a valid prepared client system
or previously delivered artifact is established by this manual negative probe.
The current persistence restrictions and the future 0.6 model remain intact.
The related consumer requirement is uibcdf/dockingmt#79/#88, discussed under
uibcdf/molsysmt#256; no consumer acceptance is granted here.

## Acceptance

- Include recognized mechanical report metadata in the unsupported-domain
  presence decision, with one owned helper reused by relevant transports.
- Reject before publishing H5MSM output and before returning a lossy MolSysDict.
- Cover both reports, ordinary/strict requests and complete/partial-domain paths.
- Preserve genuinely empty mechanics, supported domains and atomic replacement.
- Do not expand H5MSM 0.5, reinterpret parameter-only dictionaries as complete
  models, or reconstruct missing scientific evidence from diagnostics.

## Evidence and exclusions

`native-checkpoint-256-presence-probe-fixed` retains the exact command, JSON
outcomes, full before/after source hashes and resource receipt under
`.pytest_cache/external-reference-421/`. All four writes accept and all restored
values are None. The first attempt used a nonexistent root constructor alias
and failed before any writer; it remains separately retained. The successful
probe used a monitored one-CPU/2-GiB process tree with no resource interruption.
No complete-suite, installed, release or valid-client-loss claim follows.

## Local correction — 2026-11-08

**Contract-tested locally:** one native presence helper now inspects the complete
stored domain by reference, without the parameter projection, per-atom scans or
copies. `None` and the default native object remain absent; non-None stored
values, empty tables/reports and unsupported extensions/implementations do not.
All five native H5MSM branch preflights and MolSysDict 0.2 use that helper.
`MolecularMechanics.to_dict()` remains parameter-only.

The new guard fails on the original code (two cases reached before maxfail,
not a completed suite). The first corrected directed selection passes 84 cases,
including all 29 new guards, public 0.5 behavior and native dictionary routes.
The monitored process tree peaks at 303,808,512 bytes with host availability over
15 GB decimal, no swap use in its cgroup and no resource stop. Final clean-source
receiving, documentation verification and public delivery remain pending here.
