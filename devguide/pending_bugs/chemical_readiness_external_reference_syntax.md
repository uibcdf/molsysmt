---
summary: Chemical readiness rejects external syntax for its default reference state.
issue: uibcdf/molsysmt#480
status: open
opened: 2026-10-26
closed:
severity: medium
verification: reproduced
area: [physchem, selection, chemical-states]
guard:
normative:
blocked_by: []
supersedes: []
---

# Chemical readiness rejects external syntax for its default reference state

**Reported:** 2026-10-26, native-only reproduction during addon receiving.
**Status:** Open; no consumer selector/state compensation is implemented.

## What
`physchem.get_chemical_readiness(..., syntax='MDTraj')` rejects an ordinary atom-name selection even with the default `chemical_state='reference'`. The equivalent numeric selection works, as does the hydrogen inventory with the external syntax. Reproduced without MolSysViewer.

## How
```python
import molsysmt as msm
molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'], structure_indices=[0, 8, 3])
indices = msm.select(molsys, selection='name CA', syntax='MDTraj')
print(msm.physchem.get_chemical_readiness(molsys, selection=indices, structure_indices=[2])['atom_indices'])
# The equivalent request raises ArgumentError(argument='syntax', value='MDTraj'):
msm.physchem.get_chemical_readiness(molsys, selection='name CA', syntax='MDTraj', structure_indices=[2])
```
The readiness assessor resolves the reference state to integer 0, then passes that integer to `basic.select`. The public selector correctly rejects external string syntax with a non-reference state request. Thus even the ordinary default-reference audit hits a restriction introduced by the helper's internal normalization.

## Why
The public readiness signature documents `syntax` and the tutorial says rich atom selections use syntax as usual. This blocks the expert addon receiving (uibcdf/molsysmt#421; uibcdf/molsysviewer#264). The consumer will preserve the native error, not translate scientific selectors or guess state semantics.

## Acceptance criteria
Add native pytest coverage comparing default-reference external atom-name syntax with the intended explicit atom population, on a real single-state source and an explicit single structure from a trajectory; include sorted unique output, empty matches and read-only state preservation. Define explicit/non-reference and structure-associated state restrictions clearly, retaining common-selector safety. Test native and supported complementary/H5MSM routes as appropriate; no claim of unsupported external chemical-state syntax is required.

## Provenance

Linux x86-64, Python 3.14; isolated source 9442e0df20a659b9d8fa6c9a8a6bc0d115a074fc; existing ABI3 backend SHA256 f32ed73f7ef3cf3225e12fbc56b9c4236a4452d758c94661f41860ad00d82c1c. No new backend build or installed-package qualification.

## What is measured and what is assumed

Executed on a frozen checkout, with asserted native snapshot import paths.
The call fails in the common selector after the assessor resolves state 0;
this is not an unrecognized MDTraj atom-name expression or a Viewer effect.

## What was refuted

The same external selector works directly with the default reference. Numeric
readiness selection and the native hydrogen inventory succeed on the same
selected structure. The source has only one chemical state at reproduction.

## Scope and exclusions

The report does not request removing the common selector's non-reference state
restriction, adding implicit preparation or interpreting unsupported state
semantics in the addon. Explicit unsupported combinations retain diagnostics.
The existing addon wrapper forwards native results/errors; native scientific
resolution and a positive intended-population guard belong to MolSysMT.
