---
summary: Full-system writers silently discard report-only mechanical provenance
issue: uibcdf/molsysmt#660
status: resolved
opened: 2026-11-08
closed: 2026-11-08
severity: medium
verification: reproduced
area: [form, data]
guard: tests/form/file_h5msm/test_mechanics_presence.py
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

## Resolution and clean receiving — 2026-11-08

Fixed in `272745fc8df870b9a75b4e6d89b4e09a1dea0f7a`. The complete affected
selection passes **1,111 cases with no omissions**, including H5MSM 0.3/0.4/0.5,
partial/full native routes, typed dictionaries, real prepared-system checkpoints
and public H5MSM doctests. Fourteen fast gates and HTML pass. Three rendered
pages are inspected; course code, execution counts and outputs are unchanged.
The six preexisting HTML warnings remain. The test warnings are 680 legacy-file
deprecations and two unchanged unknown-atom-name diagnostics.

The [receiving record](../../devtools/data/mechanics_presence_receiving_660_20261108.json)
retains the incomplete original negative run, directed run and clean-source
profiles with unchanged input manifests and explicit pandas/Pint versions.
Tests peak at 542,543,872 bytes; all final process trees retain more than 14 GB
decimal host availability without resource interruption. Public source delivery
is recorded separately; no new format, client acceptance or release follows.

The guard independently submits report-only evidence through every H5MSM branch
and both complete-system transports. It also checks strict conversion, actual
absence, unprojected storage, unknown extensions and preservation of an existing
file. It fails when the original parameter-only emptiness decision returns.

## Correction — 2026-11-08: partial-domain fixture

The earlier statement that the original guards independently reached every H5MSM
branch was too broad. `_system("no_structures")` used `MolSys(n_atoms=2)`, which
creates an empty Structures object; it repeated a represented-structures route
instead of exercising actual absence. The original counts, commands and passing
results remain historical observations, but do not prove that fifth branch.
The shared runtime correction still covers all five branch preflights by inspection.

The #256 composition work now explicitly removes Structures in that fixture and
asserts domain presence before each report-only call. Its integrated selection
passes 1,229 cases without omissions, including the corrected absence case and
all existing 29 presence controls. Final clean-source receiving is recorded in
the #256 composition receipt. This is a coverage-claim correction, not evidence
that the original runtime repair failed or that a valid client file was lost.

Replacement clean-source evidence is now available on `b184e9d18`: the same
1,229-case selection passes without omissions, with fourteen fast gates and
fresh HTML. The corrected 29 presence guards explicitly assert all five native
compositions. See the
[composition receipt](../../devtools/data/mechanics_composition_receiving_256_20261108.json).
