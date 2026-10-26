---
summary: Physchem property readers have inconsistent element scope contracts.
issue: uibcdf/molsysmt#471
status: open
opened: 2026-10-26
closed:
severity: medium
verification: reproduced
area: [physchem, api, selection]
guard:
normative:
blocked_by: []
supersedes: []
---

# Physchem property readers have inconsistent element scope contracts

**Reported:** 2026-10-26 during addon receiving under uibcdf/molsysmt#421,
consumer uibcdf/molsysviewer#264. Filing explicitly authorized by the maintainer.
**Status:** open; native owner must define and validate supported levels.

## What

Four property readers ignore their declared element parameter and always resolve
the selection on a fixed axis. Hydrophobicity rejects non-group levels as an
internal algorithm failure. Parameter documentation lists broader structural
levels despite the actual atom/group return contracts.

```python
import molsysmt as msm
molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'])
for element in ['atom', 'group', 'system']:
    print(msm.physchem.get_atomic_radius(molsys, element=element, selection=[1]))
# all three: [0.17] nm, selecting atom 1
```

Electronegativity similarly returns [2.55] for all three scopes. Polarity returns
[8.1] and transmembrane tendency [0.38], always selecting group 1. Hydrophobicity
returns [0.62] at group scope and raises InternalAlgorithmError at atom/system.

## How

Radius/electronegativity explicitly call basic.get(element='atom');
polarity/transmembrane explicitly call basic.get(element='group'), ignoring the
public argument. Hydrophobicity explicitly rejects element != 'group' with an
internal algorithm exception. The bound addon preserves these native calls and
has no alternative aggregation formula or argument rewriting.

## Why

Integer selections can address different populations at atom/group scope. A
successful call can therefore be interpreted as a different requested population,
without an explicit rejection. This is a contract issue even if the per-atom or
per-group default is scientifically correct. It is separate from syntax
propagation in uibcdf/molsysmt#470.

## What is measured and what is assumed

Fifteen native calls were executed: five tools times atom/group/system with
selection=[1]. The values/rejections above were observed. Other hierarchy
levels follow inspected fixed-axis code but were not individually executed.
No scientifically meaningful universal aggregation is assumed.

## What was refuted

No Viewer synchronization or result conversion is involved. The native functions
reproduce this directly. Supporting every hierarchy by an arbitrary sum or mean
is not a justified repair.

## Scope and exclusions

Define each function's supported levels. Prefer an explicit public argument error
for unsupported levels before interpreting selection. If broader aggregation is
deliberately supported, document its scientific meaning, selection axis and output
shape. Do not change the default property tables or hide unknown chemistry.

## Acceptance criteria

Native pytest guards cover all five functions and supported/unsupported levels,
string and integer selections with distinct atom/group populations, empty,
repeated/reordered inputs, definitions, units/container/shape and source
nonmutation. Documentation must agree. Invalid public choices must not look like
internal algorithm failures or silently use a different scope. Receive that
native contract through the addon afterwards.

## Provenance

Linux, Python 3.14.7, molsyssuite@uibcdf_3.14, frozen native e395e5264.
Native-only calls use the bundled pentalanine MolSys without importing Viewer.
