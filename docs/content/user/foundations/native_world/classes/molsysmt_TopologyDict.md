(user-foundations-native-world-classes-molsysmt-topologydict)=
# TopologyDict

`molsysmt.TopologyDict` wraps the declarative topology record schema **0.1**.
It contains atom and hierarchy records plus a projection of reference-state
bonds. It does not store the complete native chemical-state domain.

## Declarative Schema

`data` contains the following keys. Indices are zero-based positions in the
corresponding record lists; IDs are string labels, not positions.

| Key | Stored value | Record fields or meaning |
| :--- | :--- | :--- |
| `format` | string | Format identifier, `molsysmt`. |
| `kind` | string | Object kind, `topology`. |
| `version` | string | Schema version, `0.1`. |
| `metadata` | dictionary | User metadata in the wrapper; native conversion does not restore it as topology attributes. |
| `atoms` | list of records | `atom_id`, `atom_name`, `atom_type`, `isotope`. |
| `groups` | list of records | `group_id`, `group_name`, `group_type`, `atom_indices`. |
| `bonds` | list of records | `atom_index_1`, `atom_index_2`; optional `bond_order`, `bond_type`. |
| `chains` | list of records | `chain_id`, `chain_name`, `chain_type`, `group_indices`. |
| `molecules` | list of records | `molecule_id`, `molecule_name`, `molecule_type`, `group_indices`. |
| `entities` | list of records | `entity_id`, `entity_name`, `entity_type`, `molecule_indices`. |

`atom_type` means an element symbol. Atom records do not contain parent
`group_index` or `chain_index` fields. Membership is expressed by the lists in
group, chain, molecule and entity records. Components are derived on native
reconstruction; no `components` collection is serialized.

Bond order can be a numeric order or the legacy `aromatic` label. The latter
can represent aromaticity when no separate formal order is stored. It does not
encode every combination of formal order and chemical bond annotations.

## Usage and Workflow

```python
import json
import molsysmt as msm

builder = msm.MolSysBuilder()
builder.add_atom(atom_id='10', atom_name='C', atom_type='C')
builder.add_atom(atom_id='20', atom_name='O', atom_type='O')
builder.add_group([0, 1], group_id='L', group_name='LIG')
builder.add_bond(0, 1, bond_order=1, bond_type='covalent')
molsys = builder.build()

topology_dict, report = msm.convert(
    molsys.topology, to_form='molsysmt.TopologyDict', return_report=True)
data = json.loads(json.dumps(topology_dict.to_dict(), allow_nan=False))
assert data['groups'][0]['atom_indices'] == [0, 1]
assert data['bonds'][0]['atom_index_1'] == 0
assert data['bonds'][0]['atom_index_2'] == 1
rebuilt = msm.convert(msm.TopologyDict(data=data), to_form='molsysmt.Topology')
assert msm.get(rebuilt, element='atom', atom_id=True) == ['10', '20']
```

## Fidelity Limits

Inspect `report.issues` and `report.outcome` before using this representation as
an interchange boundary. Use `strict=True` in conversion to refuse reported
losses. JSON encoding preserves the emitted dictionary; it does not certify
that every attribute of the original native object survived projection.

Schema 0.1 does not retain a chemical-state inventory, atom formal charges,
stereochemistry, preparation history or all bond annotations. Conversion uses
a resolvable reference state; ambiguous or absent reference chemistry can be
rejected. Other lost assignments are described by the conversion report.
For versioned chemical-state storage, use `ChemicalStatesDict` or
{ref}`H5MSM <user-foundations-native-world-files-file-h5msm>`.

Reconstruction uses the native builder: missing memberships/defaults may be
filled and group/molecule/entity information inferred. Raw record counts do
not necessarily equal the finalized hierarchy counts.

## Invariants and Performance

- Generated record scalars are Python primitives; missing values are `None`.
  User-supplied metadata must itself be JSON compatible if JSON is required.
- `to_dict(copy=True)` and `copy()` create deep copies. `data` and
  `to_dict(copy=False)` expose mutable wrapper data.
- The wrapper is not a whole-system validator. Conversion and molecular queries
  apply their own supported contracts.

## Querying Attributes

`msm.get()` reads the atom count, atom indices and already stored string
ID/name/type fields directly. Missing fields retain defaults and element
inference. Hierarchy counts and complete `msm.info()` summaries can require
native conversion. For repeated queries across many attributes, convert once
to a resident native object. An inventory query does not validate unrelated
serialized domains.

## API Documentation

See {func}`molsysmt.basic.convert`, {func}`molsysmt.basic.get` and
{ref}`the conversion tutorial <Tutorial_Convert>` for public conversion and
query options. The resident owner is
{ref}`Topology <user-foundations-native-world-classes-molsysmt-topology>`.
