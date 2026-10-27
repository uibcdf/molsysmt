---
summary: Builder atom insertion leaves populated chemical states misaligned after mutation
issue: uibcdf/molsysmt#499
status: open
opened: 2026-10-27
closed:
severity: medium
verification: reproduced
area: [native, build, chemical-states]
guard:
normative:
blocked_by: []
supersedes: []
---

# Appending an atom to populated builder chemistry misaligns state rows

**Reported:** 2026-10-27, an independent exploratory control while resolving
uibcdf/molsysmt#494. Group insertion itself does not require an atom-axis change.
**Status:** Open; retained as a strict expected-failure guard, not silently removed
from the test scope or claimed fixed by #494.

## What

```python
from rdkit import Chem
import molsysmt as msm
molsys = msm.convert(Chem.MolFromSmiles('CCO'), to_form='molsysmt.MolSys')
builder = msm.MolSysBuilder(molsys)
builder.add_atom(atom_name='Ar', atom_type='Ar')
# StructuralInconsistencyError: Chemical-state atom attributes are not aligned
# with the stable atom inventory: 3 rows for 4 atoms.
```

The builder has already appended its atom row and changed the atom-domain count
when the error is raised. Populated chemical-state atom attributes retain their
old length, so the failure leaves inconsistent staging data.

## How

`MolSysBuilder.add_atom` updates the atom table and `_n_atoms` before calling
`_set_component_indices`. State resolution then invokes strict compatibility
validation against the larger atom axis, while the existing per-state attribute
rows have not been resized. `ChemicalStates._resize_atom_domain` validates aligned
records rather than implementing atom creation. Do not relax that validator.

Provide an owned native atom-domain growth operation, or explicitly reject an
unsupported populated-state append before mutation. If growth is supported,
align all states, retain old assignments/bonds, mark new chemistry unknown or
partial rather than guessing, and preserve the structural-array admission check.

## Why and acceptance

Builders can assemble new empty chemistry today, but extending a chemically
populated source fails and can corrupt staging state. Add success or atomic
refusal guards for one/multiple states, typed columns, source immutability,
existing bonds and coordinate-array restrictions. Retain the independent group
insertion repair from #494.

The reproducer is retained in
`tests/native/test_builder_inherited_molecules.py::test_new_atoms_and_explicit_new_molecule_remain_supported`
with strict xfail limited to StructuralInconsistencyError and this issue number.
An unexpected pass is a failing test; unrelated exception classes remain failures.
The desired post-append molecule assertions are preserved for a future repair.
This is an open defect, not a closed-issue guard or a release waiver.

## Provenance

Linux/Python 3.14 shared development environment, 2026-10-27; original builder
append path inherited from source 010c489aa. The #494 fix changes group ownership,
not atom-domain append. No installed/cross-platform qualification is claimed.
