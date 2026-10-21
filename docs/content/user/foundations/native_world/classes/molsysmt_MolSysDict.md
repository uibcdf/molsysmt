(user-foundations-native-world-classes-molsysmt-molsysdict)=
# MolSysDict

`molsysmt.MolSysDict` wraps the declarative molecular-system schema **0.1**.
It combines a topology projection and four structural fields. Its content is
narrower than the domains available in a native `MolSys`.

## Declarative Schema

| Key | Stored value | Meaning |
| :--- | :--- | :--- |
| `format` | string | Format identifier, `molsysmt`. |
| `kind` | string | Object kind, `molsys`. |
| `version` | string | Schema version, `0.1`. |
| `metadata` | dictionary | User metadata in the wrapper; native conversion does not restore it as molecular attributes. |
| `topology` | dictionary | Collections `atoms`, `groups`, `bonds`, `chains`, `molecules`, `entities`. |
| `structures` | dictionary | Fields `structure_id`, `time`, `box`, `coordinates`. |

The nested topology uses the record fields described in
{ref}`TopologyDict <user-foundations-native-world-classes-molsysmt-topologydict>`,
without that wrapper's envelope keys. There is no nested `TopologyDict` object.
The structural payload is specific to schema 0.1; it is not a general
`StructuresDict` or a nested native `Structures` object.

## Structural Payload

| Key | Stored value | Shape and units |
| :--- | :--- | :--- |
| `structure_id` | list or `None` | Structure labels, one per structure. The native builder reads these as integers. |
| `time` | list or `None` | `(n_structures,)`, values in ps. |
| `box` | nested list or `None` | `(n_structures, 3, 3)`, box vectors in rows, values in nm. |
| `coordinates` | nested list or `None` | `(n_structures, n_atoms, 3)`, values in nm. |

Lengths/time are serialized as numbers in fixed nm/ps units, even when the
source quantities use other units. Reconstruction attaches those units again.
Neither velocities, B-factors, occupancies, alternate sites nor thermodynamic
series are fields of this nested payload.

## Usage and Workflow

```python
import json
import molsysmt as msm

builder = msm.MolSysBuilder()
builder.add_atom(atom_id='10', atom_name='C', atom_type='C')
builder.add_atom(atom_id='20', atom_name='O', atom_type='O')
builder.add_group([0, 1], group_name='LIG')
builder.add_bond(0, 1, bond_order=1, bond_type='covalent')
builder.set_coordinates(msm.pyunitwizard.quantity(
    [[[0.0, 0.0, 0.0], [1.2, 0.0, 0.0]]], 'angstrom'))
builder.set_time(msm.pyunitwizard.quantity([2.0], 'ps'))
molsys = builder.build()

molsys_dict, report = msm.convert(
    molsys, to_form='molsysmt.MolSysDict', return_report=True)
data = json.loads(json.dumps(molsys_dict.to_dict(), allow_nan=False))
assert set(data['structures']) == {'structure_id', 'time', 'box', 'coordinates'}
assert abs(data['structures']['coordinates'][0][1][0] - 0.12) < 1e-12
rebuilt = msm.convert(msm.MolSysDict(data=data), to_form='molsysmt.MolSys')
assert msm.get(rebuilt, n_atoms=True, n_structures=True) == [2, 1]
```

## Fidelity Limits

Inspect `report.issues`/`report.outcome`; use `strict=True` to refuse reported
losses. JSON transport of this dictionary does not imply a lossless round trip
of the original native system.

The native MolSys writer requires topology, chemical states and structures.
It refuses attached interaction analyses and preparation history. Other
unsupported chemical assignments, observables and mechanics can be omitted
and reported. Schema 0.1 does not store MolecularMechanics, a complete
ChemicalStates inventory or named Interactions analyses. Reference-state
resolution/refusal rules apply to the topology projection.

Use {ref}`H5MSM 0.5 <user-foundations-native-world-files-file-h5msm>` for supported
modular system, chemical-state, structure and named-interaction persistence.
MolecularMechanics persistence is not part of H5MSM 0.5. Standalone
`ChemicalStatesDict` and `InteractionsDict` retain their typed NumPy payloads;
they are not JSON record dictionaries.

## Invariants and Performance

- Generated topology fields are Python primitives; the four structural arrays
  become lists in fixed units. Nonfinite values or custom metadata need an
  explicit transport policy; `allow_nan=False` rejects nonfinite JSON numbers.
- `to_dict(copy=True)` and `copy()` isolate wrapper data by deep copying.
  `data` and `to_dict(copy=False)` expose mutable data.
- Reconstruction can supply missing hierarchy/defaults through the native builder.
  Raw list lengths need not equal inferred hierarchy counts.

## Querying Attributes

`msm.get()` reads the atom count, atom indices and already stored string
ID/name/type fields directly. Missing fields retain their default/inference
route. Hierarchy counts and complete `msm.info()` summaries can still require
native conversion. For repeated queries across many attributes, convert once
to a resident native object. An inventory query does not validate unrelated
serialized domains.

## API Documentation

See {func}`molsysmt.basic.convert`, {func}`molsysmt.basic.get` and
{ref}`the conversion tutorial <Tutorial_Convert>`. The resident owner is
{ref}`MolSys <user-foundations-native-world-classes-molsysmt-molsys>`.
