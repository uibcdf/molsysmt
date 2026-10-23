(Tutorial_Project_Atom_Names)=
# Projecting atom names for export

*Applying explicit format constraints while preserving original atom identity.*

{func}`molsysmt.form.project_atom_names` returns a native MolSys whose selected
atom names fit the requested export profile. The experimental first profile
supports `file:pdbqt` and `string:pdbqt_text`, both with four-character names.
`to_form` selects the constraints; the tool returns a MolSys and writes no file.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

{func}`molsysmt.form.project_atom_names`
:::

## Applying a deterministic policy

The source may be any supported form convertible to a native MolSys with atom
names. For foreign inputs, report source indices and labels describe the
converted native atom axis; the input conversion retains its own contract.
This small native example needs no chemistry engine or coordinates.

```python
import molsysmt as msm
from molsysmt.native import MolSys

molsys = MolSys(n_atoms=3, n_groups=1)
molsys.topology.atoms['group_index'] = [0, 0, 0]
msm.set(molsys, atom_name=['C-long', 'H1291', 'H0'])
msm.set(molsys, atom_id=['17', '45', '3'])
projected = msm.form.project_atom_names(
    molsys, to_form='file:pdbqt', return_report=True)
prepared = projected['molecular_system']
report = projected['report']
assert prepared.topology.atoms.atom_name.tolist() == ['C0', 'H1', 'H0']
assert molsys.topology.atoms.atom_name.tolist() == ['C-long', 'H1291', 'H0']
assert prepared.topology.atoms.atom_id.tolist() == ['17', '45', '3']
```

The `preserve_or_base36` policy reserves **all** existing nonempty printable
ASCII names of at most four characters before changing selected invalid names.
It preserves existing valid duplicates: names are labels, not atom identity.
For each invalid selected name, its first ASCII letter is uppercased and followed
by a base-36 counter (`0`–`9`, `A`–`Z`, then `10`, …). If no ASCII letter exists,
the prefix is `X`. This is a lexical prefix, never an inferred chemical element.
The first available name is chosen in ascending source atom-index order.

New names cannot collide with a reserved name or an earlier generated name in
the same group. Different groups may reuse names. If any group membership is
unknown, the tool uses one conservative system-wide namespace for all atoms and
reports `collision_scope='system'`. It never invents group membership. Known
out-of-range group indices are errors. Each prefix permits 36³ candidate names;
exhaustion raises before any result is returned. There is no silent truncation.

## Selecting atoms without extracting them

`selection` controls which names may change. It does not remove or reorder atoms
or structures. Repeated atom indices are deduplicated and sorted. Use plain
integer indices; lengths and explicit dimensionless quantity wrappers are
rejected before projection.

```python
partial = msm.form.project_atom_names(molsys, to_form='string:pdbqt_text',
    selection=[1, 1], return_report=True)
assert partial['report']['selected_atom_indices'].tolist() == [1]
assert partial['report']['renamed_atom_indices'].tolist() == [1]
assert partial['molecular_system'].topology.atoms.atom_name.tolist() == [
    'C-long', 'H1', 'H0']
```

The unselected `C-long` remains invalid for PDBQT. The writer will still reject it.
This operation also does not fix serial IDs, group/chain fields, typing, charges
or torsion trees. Those retain their existing explicit export contracts.

## Keeping a reversible label record

The detached `molsysmt.atom_map@1` report contains the complete original/output
name and ID arrays, identity forward/inverse atom maps, selected/renamed indices,
policy parameters and the producing MolSysMT version. Indices retain their
original positions; IDs remain string labels. Original labels can be recovered
by source index even when they were duplicated. Name matching is unnecessary.

```python
import json

lineage = msm.form.compose_atom_maps([report])
assert lineage['source_to_output_atom_indices'].tolist() == [0, 1, 2]
assert lineage['source_atom_names'].tolist() == ['C-long', 'H1291', 'H0']
encoded = json.dumps(report, default=lambda value: value.tolist())
restored = msm.form.compose_atom_maps([json.loads(encoded)])
assert restored['stages'][0]['renamed_atom_indices'].tolist() == [0, 1]
```

Place this report at the actual renaming step in a longer preparation → H
projection → writer → pose sequence. The writer map records the actual written
order; the rename map alone does not. See {ref}`Tutorial_Compose_Atom_Maps`.
The report is a typed sidecar, not a new H5MSM domain or molecular form.

## Preserving molecular data and provenance

The source is unchanged. The result has independent mutable native domains;
coordinates and boxes share protected blocks until a managed edit replaces them.
This avoids a trajectory-sized geometry copy for label-only work. Coordinates,
units, chemistry, charges, types and analysis data are not recalculated.

Stored scientific reports are retained without new credit or recertification.
For example, Gasteiger charge and chemical-environment typing bindings do not
depend on atom names. A template-sensitive force-field charge binding can become
invalid after renaming; its original report is preserved and the existing writer
validation rejects it. Project names **before** such an assignment, or explicitly
recalculate/replace that assignment. No automatic rebinding occurs.

:::{seealso}
:class: dropdown

- {ref}`Tutorial_Compose_Atom_Maps`
- {ref}`cookbook-native-pdbqt`
- {func}`molsysmt.basic.set`
:::
