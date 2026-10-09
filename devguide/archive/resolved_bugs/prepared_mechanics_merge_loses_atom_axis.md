---
summary: Prepared mechanics merge fails on numeric charges and retains the first atom axis
issue: uibcdf/molsysmt#352
status: resolved
opened: 2026-10-09
closed: 2026-10-09
severity: high
verification: reproduced
area: [basic, form, native]
guard: tests/basic/merge/test_merge_prepared_mechanics.py::test_merge_preserves_prepared_mechanics_atom_axis
normative:
blocked_by: []
supersedes: []
---

# Prepared mechanics merge fails on numeric charges and retains the first atom axis

**Reported:** 2026-10-09 by DockingMT during uibcdf/dockingmt#17/#33.
**Status:** Resolved; focused public regressions, doctest and original fixture verified.

## What

Public `msm.merge` cannot combine two prepared native systems. On the reported
PDBQT input it raises `NotImplementedFormError` for numerical charges; removing
charges exposes a second `ValueError` assigning 1,483 types to 1,481 rows.

```python
import molsysmt as msm
molsys = msm.convert('5x72_receptor.pdbqt', to_form='molsysmt.MolSys')
part = msm.extract(molsys, selection=[0, 1])
msm.set(part, element='atom', atom_id=[1482, 1483])
combined = msm.merge([molsys, part], keep_ids=True)
```

The file comes from DockingMT commit
`ee095f4548441dfd043e4f322095810c54c4e002`, path
`tests/data/vina_torsions/5x72_receptor.pdbqt`, SHA-256
`25d4e9b5f3932bc2953152dffc2d9dadf13726ae029e5e88712a0dc9525361e6`.

## How

`molsysmt/form/molsysmt_MolecularMechanics/merge.py` incorrectly sends native
numerical columns to a physical-quantity concatenator. Those values already have
the native elementary-charge convention. Its copied first `atoms_ff` table also
constrains assignments to the original row count.

Concatenate the canonical numerical/type columns with NumPy onto a fresh atom
table, retaining input and selected order. Keep the existing column-intersection
policy: a missing column in a contributing input clears that column, now with a
catalog warning if values are lost. Empty selections contribute nothing. Copy
scalar settings from the first input as before. Do not recalibrate charges/types.

Combining inputs or selecting atoms invalidates named charge/type assignment
reports, with an explicit `StructuralAttributeDropWarning`. Such reports describe
their original atom graph rather than a new joint calculation. A single full
input keeps detached reports. Source values and provenance remain unchanged.

## Why

DockingMT needs to compose previously prepared systems without retyping,
recharging or dropping their atom-aligned data. The same fault affects standalone
`MolecularMechanics` forms and selected native `MolSys` merges.

## What is measured and what is assumed

Both reported failures are reproduced on unchanged source `ad9353d91` in the
shared Python 3.14 development environment with the exact downloaded fixture.
The regression selection fails before the fix: six failures covering numeric
charges, type-only rows, selected charge order/units, empty contribution, named
provenance invalidation and detached singleton ownership.

Command: `python -m pytest tests/basic/merge/test_merge_prepared_mechanics.py
--receptor=llm -n12 --junitxml=/tmp/molsysmt-352-before.xml`.

After correction, the exact original fixture combines into 1,483 rows with
unchanged charges and types, preserving both source axes. The focused selection
`python -m pytest tests/basic/merge tests/basic/add/test_add_audit_decisions.py
--receptor=llm -n12 --junitxml=/tmp/molsysmt-352-final.xml` passes 46 tests.
These are source checks, not installed-artifact or docking-search qualification.
The strengthened input-unit control supplies charges in coulombs, and keeps a
coulomb/angstrom session during public merging. Eight regression cases plus the
public merge doctest pass with `--doctest-modules --receptor=llm -n12`.
These selections overlap and their counts must not be added. The User Guide
Foundations, merge tutorial, PDBQT Cookbook and course Module 17 are updated;
notebook code cells and saved outputs are unchanged. Ruff and course validation
pass.
All fourteen fast release gates also pass. This bounded check does not restart
the paused release's heavy source/native/installed qualification campaigns.

## What was refuted

The issue is not missing force-field preparation or a charge-unit policy change:
the parser already produces the required numerical charges and type labels.
Removing charges does not fix the retained table length. A downstream setter
workaround is unnecessary once the public general merge is corrected.
An intermediate regression incorrectly treated native `get(partial_charge=True)`
as a physical quantity. Its established contract returns the numerical column
in elementary charge; the corrected control checks that convention under a
nondefault session policy, without changing the getter contract.

## Scope and exclusions

Repair public native mechanics/`MolSys` merging, including explicit atom
selections and provenance invalidation. Chemical-state alignment, first-input
scalar-setting compatibility, new force fields and H5MSM mechanics persistence
remain separate contracts. The chain-ID defect is uibcdf/molsysmt#353.
No original qualified release candidate or artifact is modified.

## Acceptance criteria

- Preserve combined atom rows, charge values in elementary charge and type labels.
- Preserve explicit selected order and empty contributions without input mutation.
- Work under nondefault unit policy through public get/set/merge operations.
- Define report invalidation and retain detached singleton provenance.
- Qualify the original 1,481 + 2 atom fixture and relevant public regressions.
- Update public documentation and close with an addressable regression guard.

## Provenance

2026-10-09, Linux, shared Python 3.14.7 environment, Pandas 2.3.3,
ArgDigest `0.15.0+1.g5c6711e`, existing native extension. Source tests do not
qualify a rebuilt package or a replacement release pair.
