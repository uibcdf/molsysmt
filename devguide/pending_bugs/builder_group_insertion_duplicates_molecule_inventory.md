---
summary: MolSysBuilder group insertion duplicates an existing molecule inventory.
issue: uibcdf/molsysmt#494
status: open
opened: 2026-10-27
closed:
severity: medium
verification: reproduced
area: [native, builder, topology]
guard:
normative:
blocked_by: []
supersedes: []
---

# MolSysBuilder group insertion duplicates an existing molecule inventory.

**Reported:** 2026-10-27, isolated while receiving the bound TPSA reader under
uibcdf/molsysviewer#264; independently reproduced without Viewer.
**Status:** open; the scientific owner is responsible for correction and a native
pytest guard. The consumer adds no topology or selector workaround.

## What

Adding groups to a MolSysBuilder initialized from a valid group-free MolSys duplicates the molecule inventory. Two complete molecules become four metadata rows, while molecule atom memberships still describe only two molecules. The native TPSA reader consequently rejects the correspondence.

## Reproduction

Reproduced without MolSysViewer on MolSysMT `c905d8ac753e98ec11959fac5ccbe049311d2068` (unchanged native runtime from `97a8dc08c`), Python 3.14, using RDKit:

```python
from rdkit import Chem
import molsysmt as msm

source = msm.convert(Chem.MolFromSmiles('CCO.COC'), to_form='molsysmt.MolSys')
print(msm.get(source, n_molecules=True))  # 2
builder = msm.MolSysBuilder(source)
builder.add_group([0, 1, 2], group_name='LIG')
builder.add_group([3, 4, 5], group_name='LIG')
result = builder.build()
print(msm.get(result, n_molecules=True))  # 4, expected 2
print(result.topology.groups.molecule_index.tolist())  # [2.0, 3.0]
print(msm.get(result, element='molecule', atom_index=True))
# [[0, 1, 2], [3, 4, 5]]
msm.physchem.get_tpsa(result)
# StructuralInconsistencyError: Molecule labels and source atom membership
# must have matching lengths.
```

## How

`MolSysBuilder._fill_molecule_fallbacks` appends molecule rows for unassigned groups without reconciling the existing group-free molecule inventory copied by the constructor. The older molecule rows remain unowned. This is a native hierarchy/molecule-axis issue, not a TPSA or Viewer calculation defect.

## Why and acceptance

This affects molecular readers after adding normal group hierarchy to converted graphs. Preserve valid source molecule identity/membership when adding groups, or reject conflicting declarations explicitly. Add pytest guards for one/multiple disconnected source molecules, full/partial group insertion, rebuild/query agreement and downstream molecule-level access; retain ordinary group-free builds and explicit declared molecule boundaries. Do not fix this in downstream consumers by discarding rows or inventing molecule indices.

Related: uibcdf/molsysmt#491 (closed group-free inventory repair), uibcdf/molsysmt#493 (separate constructor diagnostic), uibcdf/molsysviewer#264 (consumer receiving).

Record: `devguide/pending_bugs/builder_group_insertion_duplicates_molecule_inventory.md`.


## What is measured and what is assumed

The pasted public-call reproductions execute on committed source c905d8ac7
(native code inherited from 97a8dc08c). Observations are reproduced; neither a
fix nor a general policy for all molecular hierarchies is established here.

## Scope and exclusions

Keep the native repair reusable and preserve source chemistry, molecule identity
and correspondence. This report does not change TPSA criteria or authorize a
consumer-specific reconstruction. The neighboring builder/selection issues are
separate themes, as are the previously closed #491/#493 repairs.

## Provenance

2026-10-27, Linux x86-64, Python 3.14, molsyssuite@uibcdf_3.14 development
interpreter, isolated source snapshot of c905d8ac7 with retained ABI3 backend.
No installed-package or cross-platform qualification is claimed.
