---
summary: Builder atom insertion leaves populated chemical states misaligned after mutation
issue: uibcdf/molsysmt#499
status: resolved
opened: 2026-10-27
closed: 2026-10-27
severity: medium
verification: measured
area: [native, build, chemical-states]
guard: tests/native/test_builder_atom_extension.py::test_atom_extension_aligns_every_state_and_preserves_existing_evidence
normative:
blocked_by: []
supersedes: []
---

# Appending an atom to populated builder chemistry misaligns state rows

**Reported:** 2026-10-27, an independent exploratory control while resolving
uibcdf/molsysmt#494. Group insertion itself does not require an atom-axis change.
**Status:** Resolved and locally qualified. The original expected-failure
assertions now pass as an ordinary regression guard.

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

The reproducer was initially retained in
`tests/native/test_builder_inherited_molecules.py::test_new_atoms_and_explicit_new_molecule_remain_supported`
with strict xfail limited to StructuralInconsistencyError and this issue number.
The marker is now removed without changing its desired post-append assertions;
the test passes as an ordinary regression guard.

## Provenance

Linux/Python 3.14 shared development environment, 2026-10-27; original builder
append path inherited from source 010c489aa. The #494 fix changes group ownership,
not atom-domain append. No installed/cross-platform qualification is claimed.

## Coordinated correction — 2026-10-27

ChemicalStates owns a private extension primitive that prepares aligned nullable
attribute/component rows for every state before publication. It validates the
original row axes, known columns, dtypes, values and completeness declarations.
New atom fields and component membership remain missing; complete declarations
become partial, and unavailable evidence is not upgraded. Existing bonds, component
tables, state identity/reference and original producer history are retained.
The strict _resize_atom_domain post-edit validator is unchanged.

MolSysBuilder normalizes and stages its new atom table first, then delegates
coordinated state growth and publishes the prepared atom inventory. Invalid state
rows or values, atom-name resolution failure and controlled later-state allocation
failure leave the existing inventory and state tables unchanged. Coordinates,
velocities and B factors continue to prohibit an atom-axis change.

Compilation also keeps a group-free source's molecule metadata aligned when
new disconnected components appear. Rebuilt reference component positions are
aligned with inherited molecule indices, including permuted sources; new rows
are appended without overwriting old IDs/names/types. Shared metadata filling
reuses the existing native inference tools. Connectivity splits/merges that cannot
retain group-free molecule boundaries fail explicitly and can be represented
with declared groups. No generic table/chemistry validation is relaxed.

This is inventory editing, not a chemical preparation or a new public chemical
store. Existing scientific methods may reject the resulting partial chemistry.
Allocation concerns the stable atom table and materialized atom-state fields;
coordinates, bonds and component tables are not copied by state growth itself.
No runtime/memory benchmark, concurrent-edit transaction, external dependency or
new scientific attribution boundary is introduced.

## Qualification and documentation

The named guard checks all-state growth, typed missing fields, preservation of
existing assignments and evidence, and source independence. Additional controls
cover refusal before writes, including a controlled later-state allocation failure,
reference ambiguity, group-free compilation and public H5MSM persistence. The
original append/group/build guard from #499 is unchanged apart from removing its
strict expected-failure marker.

The expanded native/builder/Topology/descriptor regression passed 2,391 tests;
the final focused run, including the additional H5MSM round trip, passed 80.
Four builder doctests and 496 notebook-schema controls passed; the 14 fast gates,
scoped Ruff, public docstring and signature checks passed. Existing warnings are
retained, not suppressed. The Cookbook recipe was executed and HTML rebuilt;
the final incremental HTML build reports 17 existing orphan-document warnings.
Foundations, the editable builder tutorial and the native-forms course now explain
unknown chemistry, all-state alignment and the structural-array restriction.

[Qualification receipt](../../../devtools/data/builder_atom_extension_20261027.json)
records exact commands and source hashes. This is shared-environment local source
qualification, not a whole-suite, clean-installed, cross-platform, performance or
release qualification. No artifact, tag, dependency floor or format version changes.
