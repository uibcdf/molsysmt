---
summary: RDKit all-atom selections advertise a missing native count getter
issue: uibcdf/molsysmt#266
status: resolved
opened: 2026-09-30
closed: 2026-09-30
severity: medium
verification: reproduced
area: [form, selection, attribute]
guard: tests/form/rdkit_Mol/test_subset_and_structures.py::test_all_atom_selection_uses_a_declared_attribute_pipe_without_a_direct_count_getter
normative:
blocked_by: []
supersedes: []
---

# RDKit all-atom selections advertise a missing native count getter

**Reported:** 2026-09-30, while checking form-agnostic ring participants.
**Status:** Resolved. The count lookup delegates through the public attribute
pipeline when a form lacks a direct getter. The combined selection/RDKit/ring/ionic
checkpoint passed 289 tests; the bounded guarded selections pass for all three fixtures.

## What

`msm.has_attribute(rdkit_mol, "n_atoms")` returns True and
`msm.get(rdkit_mol, n_atoms=True)` succeeds, but `msm.select(rdkit_mol)` raises
AttributeError for a missing get_n_atoms_from_system adapter.

```python
import molsysmt as msm
from rdkit import Chem
molsys = Chem.MolFromSmiles("c1ccccc1")
assert msm.get(molsys, n_atoms=True) == 6
msm.select(molsys)  # AttributeError before this correction
```

## How

The all-elements branch of basic.select directly invokes a getter on the source
form after where_is_attribute locates its declared count. RDKit supplies that
attribute through its valid native-topology pipe, not a direct getter. Retain
the fast direct path when it exists; otherwise use basic.get's established
attribute delivery route. The internal boolean attribute request is controlled
and canonical, so trusted delegation skips redundant digestion.

## Why

Form-agnostic selection must work for sources delivering an attribute through
a registered pipe. Requiring every piped form to duplicate a count getter would
conflict with the adapter contract. This correction does not fabricate missing
attributes or broaden the meaning of a form declaration.

## What is measured and what is assumed

**Reproduced:** RDKit benzene all-atom selection failed with AttributeError while
its count query returned 6. Focused regressions cover empty molecules, ordinary
small molecules, aromatic molecules and the empty group axis.

**Not claimed:** This bounded correction does not validate every RDKit getter
or repair unrelated attribute deliveries.

## What was refuted

The source's n_atoms declaration is not false: public get already delivers it
through conversion. Deleting the declaration or adding a detector-local raw
RDKit special case would hide the actual missing public delegation.

## Scope and exclusions

Correct the shared all-elements count branch. Preserve direct getter dispatch
for established forms, selection syntax, output indices and state resolution.

## Acceptance criteria

The guarded RDKit selections agree with native atom counts, including zero,
and existing basic-selection and RDKit form tests remain passing.

## Resolution

The regression guards the public failure mechanism: a declared piped atom count
with no direct count getter must still support all-atom selection, including an
empty molecule. Group selections additionally preserve an empty axis. Existing
direct getters retain their prior route. This restores the established
form-agnostic contract without adding RDKit-only logic to basic.select.

```bash
python -m pytest --receptor=llm tests/basic/select tests/form/rdkit_Mol --disable-warnings
```
