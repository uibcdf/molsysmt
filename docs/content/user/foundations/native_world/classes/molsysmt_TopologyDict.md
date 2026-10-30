(user-foundations-native-world-classes-molsysmt-topologydict)=
# TopologyDict

`molsysmt.TopologyDict` wraps the stable inventory schema **0.2**. It stores
atoms and represented hierarchy with no bonds, components or chemical states.
Legacy 0.1 dictionaries remain readable; projecting their chemical content to
pure Topology does not preserve that content. Use a complete MolSys conversion
when you need chemistry.

## Declarative Schema

Indices are zero-based positions; IDs are string labels.

| Key | Stored value | Fields or meaning |
| :--- | :--- | :--- |
| `format` | string | `molsysmt`. |
| `kind` | string | `topology`. |
| `version` | string | `0.2`. |
| `metadata` | empty dictionary | Reserved; unrepresented metadata is rejected. |
| `atoms` | record list | `atom_id`, `atom_name`, `atom_type`, `isotope`, `group_index`, `chain_index`. |
| `groups` | record list | `group_id`, `group_name`, `group_type`, `molecule_index`. |
| `molecules` | record list | `molecule_id`, `molecule_name`, `molecule_type`, `entity_index`. |
| `entities` | record list | `entity_id`, `entity_name`, `entity_type`. |
| `chains` | record list | `chain_id`, `chain_name`, `chain_type`. |
| `chain_groups` | optional list of index lists | Explicit ordered/shared groups for each chain, including empty chains. |
| `atom_molecules` | optional nullable index list | Stable molecule ownership of ungrouped atoms; grouped positions remain unknown here. |

Missing values are `None`. `atom_type` means element symbol. Native decoding
retains rows and nullable parent memberships directly; it does not infer chemical
states or synthesize hierarchy. Every declared index is checked against its
represented axis. Zero-atom group inventories and empty occurrences are retained.
Unknown version 0.2 fields and row fields are rejected, including chemical data
incorrectly inserted into this stable schema.

## Usage and Workflow

```python
import json
import molsysmt as msm

builder = msm.MolSysBuilder()
builder.add_atom(atom_id='10', atom_name='C', atom_type='C')
builder.add_atom(atom_id='20', atom_name='O', atom_type='O')
builder.add_group([0, 1], group_id='L', group_name='LIG')
builder.add_bond(0, 1, bond_order=1, bond_type='covalent')
builder.add_chain([0], chain_id='A')
molecule_index = builder.add_molecule([0], molecule_name='ligand', molecule_type='small molecule')
builder.add_entity([molecule_index], entity_name='ligand', entity_type='small molecule')
molsys = builder.build()
payload = msm.convert(molsys.topology, to_form='molsysmt.TopologyDict')
data = json.loads(json.dumps(payload.to_dict(), allow_nan=False))
assert data['version'] == '0.2'
assert [atom['group_index'] for atom in data['atoms']] == [0, 0]
assert 'bonds' not in data
rebuilt = msm.convert(msm.TopologyDict(data=data), to_form='molsysmt.Topology')
assert rebuilt.get(element='atom', atom_id=True) == ['10', '20']
assert not hasattr(rebuilt, 'bonds')
```

## Fidelity Limits

The source in this example is already pure Topology. To preserve a complete
molecular system, convert MolSys to
{ref}`MolSysDict <user-foundations-native-world-classes-molsysmt-molsysdict>` or
{ref}`H5MSM <user-foundations-native-world-files-file-h5msm>` instead.
Unsupported table columns/metadata and native extension attributes/slots are
refused by the 0.2 writer. Inspect conversion reports when projecting richer
input forms, and use `strict=True` to reject reported losses.

The 0.1 reader interprets membership lists in its legacy records. Complete
legacy MolSys decoding retains its written reference chemistry in ChemicalStates;
Topology output is stable inventory only. No reader can recover assignments that
were absent from the old file.

## Invariants and Performance

`copy()`, Python `copy.copy`/`copy.deepcopy` and `to_dict(copy=True)` detach mutable
wrapper payloads without decoding or certifying a schema. `data` and
`to_dict(copy=False)` expose mutable records. These are interchange lists, not a
compressed numeric store. See
{ref}`Native Copying <user-foundations-resident-copying>`.

## Querying Attributes

Use `msm.get(payload, ...)` and `msm.info(payload, ...)`. Stored atom counts,
indices and normalized label fields support direct reads without native
finalization. Other queries use supported native decoding; legacy 0.1 behavior
is interpreted separately. Chemical capabilities are absent for schema 0.2,
including when the dictionary originally came from an attached Topology.
