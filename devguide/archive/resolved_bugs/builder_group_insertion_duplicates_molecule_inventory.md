---
summary: MolSysBuilder group insertion duplicates an existing molecule inventory.
issue: uibcdf/molsysmt#494
status: resolved
opened: 2026-10-27
closed: 2026-10-27
severity: medium
verification: measured
area: [native, builder, topology]
guard: tests/native/test_builder_inherited_molecules.py::test_full_and_partial_group_insertion_preserves_molecular_identity
normative:
blocked_by: []
supersedes: []
---

# MolSysBuilder group insertion duplicates an existing molecule inventory.

**Reported:** 2026-10-27, isolated while receiving the bound TPSA reader under
uibcdf/molsysviewer#264; independently reproduced without Viewer.
**Status:** Resolved and locally qualified. Source ownership is preserved in the
native builder; no consumer hierarchy workaround is used.

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

Record: `devguide/archive/resolved_bugs/builder_group_insertion_duplicates_molecule_inventory.md`.


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

## Native correction — 2026-10-27

MolSysBuilder captures the reference molecule membership of a group-free source
in a compact staging-only integer array. New groups inherit their one known
source owner; a group spanning distinct inherited molecules is rejected before
mutation. During compilation the ordinary fallback groups for remaining source
atoms inherit the same owner. Existing molecule IDs, names, types and entity
relationships remain intact, with no appended duplicate molecule rows. Builders
without inherited molecule membership retain their existing inference path.
The source, full/partial grouping, independent builder copies, repeated builds
and reference-versus-alternate-state partition are covered by native tests.

This does not implement atom-domain growth for populated chemical states. Its
independent failure was discovered during exploratory testing and is retained
as a strict, exception-specific expected failure under uibcdf/molsysmt#499,
not removed, hidden or claimed fixed here.

## Qualification closeout — 2026-10-27

The expanded local scope passes 2,404 tests with one explicitly retained strict
xfail for the separate open #499 defect (134.83 seconds). The final focused
source/builder controls pass 40 tests with that same one xfail. All 59 bound
TPSA receiving tests pass after requiring positive selector success; three
builder doctests and 496 notebook-schema controls pass. All 14 fast gates,
scoped Ruff, docstring and signature checks pass.

The new group-free hierarchy recipe executes in 12.3 seconds. Five existing
Tools/Form/course notebooks retain their code cells and saved outputs; their
legacy scenarios are not requalified by the prose-only additions. HTML exits
zero with 32 existing header/directive/orphan warnings under the #144 debt;
none comes from the new recipe. No warning-debt reduction, whole-suite,
installed-pair, cross-platform, benchmark or release qualification is claimed.
See the [dated receipt](../../../devtools/data/group_free_builder_mdtraj_20261027.json)
for commands, environment, source hashes and the explicit expected-failure scope.
