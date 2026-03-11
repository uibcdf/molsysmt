# MolSysBuilder

`MolSysBuilder` is the native editable form for constructing or editing a
molecular system before materializing it as `molsysmt.MolSys`.

The canonical internal design notes live in `devguide/molsys_builder.md`. This
developer page highlights the practical reason the builder matters for daily
development and testing.

## Why it matters for converter tests

Before `MolSysBuilder`, many converter tests had an awkward problem: the target
format under test also had to provide the expected truth used in assertions.
For example, when testing a PDB converter, the test often had to trust either:

- a PDB parser to tell us that atom 34 is named `CA`; or
- a separate conversion path to reconstruct that truth first.

That weakens the test because the expected answer is no longer declared by the
test itself.

`MolSysBuilder` changes this workflow:

1. declare the exact molecular truth first in native editable form;
2. build the corresponding `molsysmt.MolSys`;
3. export that `MolSys` to the target external form;
4. run the converter under test;
5. compare the converted result with the original declared truth.

This means converter tests can now assert facts such as:

- atom indices and names;
- group membership;
- bond connectivity;
- chain, molecule, and entity declarations;
- coordinates, box, time, and structure identifiers.

The expected truth exists *before* the file format is involved.

## Editing policy

`MolSysBuilder` and `molsysmt.build.editable(...)` are now the public path for
explicit topology editing. The older public helpers

- `molsysmt.build.add_bonds`
- `molsysmt.build.remove_bonds`
- `molsysmt.build.define_new_chain`

have been removed from the public API during the pre-`1.0` phase. Internal
code paths that still need equivalent behavior use native topology methods or
private helpers instead.

`MolSysBuilder` now covers the explicit editing primitives that motivated those
helpers:
- `MolSysBuilder.add_bond(...)`
- `MolSysBuilder.remove_bonds(...)`
- `MolSysBuilder.assign_groups_to_new_chain(...)`

## Preferred testing pattern

For small and deterministic fixtures, prefer this sequence:

```python
import molsysmt as msm

builder = msm.MolSysBuilder()
atom_0 = builder.add_atom(atom_name="N")
atom_1 = builder.add_atom(atom_name="CA")
group_0 = builder.add_group([atom_0, atom_1], group_name="ALA")

molsys = builder.build()
pdb_text = msm.convert(molsys, to_form="string:pdb_text")
roundtrip = msm.convert(pdb_text, to_form="molsysmt.MolSys")
```

The assertions should be written against the declared truth, not discovered
later from the file under test.

This deterministic-fixture pattern already covers:
- PDB text / file / `molsysmt.PDBFileHandler`;
- H5MSM file / `molsysmt.H5MSMFileHandler`;
- `openmm.Topology`;
- `MolSysDict` / `file:molsys_yaml`;
- `StructuresDict` / `file:structures_yaml`.

## Current supported builder surface

The first implemented slice intentionally keeps the surface narrow:

- `MolSysBuilder()` from scratch;
- `MolSys -> MolSysBuilder`;
- `MolSysBuilder -> MolSys`;
- declared-state queries through `get()`, `info()`, `select()`, and `set()`.

Broader conversion support should be added later by routing through `MolSys`.
