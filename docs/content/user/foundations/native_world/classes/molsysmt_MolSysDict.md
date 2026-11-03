(user-foundations-native-world-classes-molsysmt-molsysdict)=
# MolSysDict

`molsysmt.MolSysDict` wraps the declarative molecular-system schema **0.2**.
It preserves independently optional stable inventory, chemical states, structures,
explicit state associations and named interaction analyses. Readers also accept
legacy 0.1 payloads through their separate interpretation.

## Declarative Schema

| Key | Stored value | Meaning |
| :--- | :--- | :--- |
| `format` | string | `molsysmt`. |
| `kind` | string | `molsys`. |
| `version` | string | `0.2`. |
| `metadata` | empty dictionary | Reserved; unrepresented metadata is rejected on reconstruction. |
| `topology` | dictionary or `None` | Complete versioned TopologyDict 0.2 envelope. |
| `chemical_states` | typed transport or `None` | ChemicalStatesDict inventory, assignments, components, bonds and preparation history. |
| `structures` | typed transport or `None` | Structural series, quantities, sparse alternate sites, assemblies and supported metadata. |
| `structure_chemical_state_indices` | typed transport or `None` | Nullable int64 associations; `None` retains the native implicit/unknown convention. |
| `interactions` | dictionary | Named InteractionsDict transports, including coverage, occurrence indices, measurements and producer provenance. |

An absent chemical domain is `None`; a present zero-state collection encodes
`states=[]`. Empty named analyses are `{}`. Counts do not establish correspondence:
assembly declares that represented domains share their positional atom axis.
Stable topology owns no chemical fields. See
{ref}`TopologyDict <user-foundations-native-world-classes-molsysmt-topologydict>`.

## Typed Transport

The private, versioned transport contains JSON primitives and explicit array
records. Numeric/bool arrays retain dtype, shape and C-order bytes through base64;
Unicode arrays retain typed string values. Large integers, nonfinite numeric
values and nullable masks survive without pickle or object-array decoding.
Dimensionful fields use PyUnitWizard quantity records. Length/time/energy values
have explicit units, independent of the user's active output-unit policy.

Structures preserve coordinates, box, velocities, time, labels, B-factors,
occupancies, temperatures, potential/kinetic energies, alternate sites and
bioassemblies when present. Arrays retain the native structure/atom axis shapes.
Schema-declared array positions distinguish transport records from arbitrary
mappings. Unknown versions, invalid dtype/shape/byte lengths and unsupported
fields fail on reconstruction.

## Usage and Workflow

```python
import json
import molsysmt as msm

builder = msm.MolSysBuilder()
builder.add_atom(atom_id='10', atom_name='C', atom_type='C')
builder.add_atom(atom_id='20', atom_name='O', atom_type='O')
builder.add_group([0, 1], group_name='LIG')
builder.add_bond(0, 1, bond_order=1, bond_type='covalent')
builder.add_chain([0], chain_id='A')
molecule_index = builder.add_molecule([0], molecule_name='ligand', molecule_type='small molecule')
builder.add_entity([molecule_index], entity_name='ligand', entity_type='small molecule')
builder.set_coordinates(msm.pyunitwizard.quantity(
    [[[0.0, 0.0, 0.0], [1.2, 0.0, 0.0]]], 'angstrom'))
builder.set_time(msm.pyunitwizard.quantity([2.0], 'ps'))
molsys = builder.build()

payload = msm.convert(molsys, to_form='molsysmt.MolSysDict')
data = json.loads(json.dumps(payload.to_dict(), allow_nan=False))
assert data['version'] == '0.2'
assert 'bonds' not in data['topology']
rebuilt = msm.convert(msm.MolSysDict(data=data), to_form='molsysmt.MolSys')
assert rebuilt.get(n_atoms=True, n_structures=True, n_bonds=True) == [2, 1, 1]

molsys_A = msm.convert(payload, selection=[1], structure_indices=[0, 0],
                      to_form='molsysmt.MolSys')
assert molsys_A.get(n_atoms=True, n_structures=True) == [1, 2]
assert molsys_A.get(element='atom', atom_id=True) == ['20']
```

Selected reconstruction retains atoms in sorted source order; structures preserve
requested order and repetitions. All represented dependent domains follow the
same maps. The source payload remains unchanged.

## Fidelity Limits

Nonempty MolecularMechanics, unsupported native extension attributes/slots,
unknown topology fields and unrepresented root metadata are refused rather
than silently omitted. No arbitrary Python class identity is serialized. Inspect
conversion reports and use `strict=True` for reported projections; successful
JSON encoding alone does not certify the source's scientific completeness.

Legacy 0.1 reads retain their four structural fields and reference bond projection;
they cannot recover chemical data never written. Writers always emit 0.2.
For large numeric workloads use
{ref}`H5MSM 0.5 <user-foundations-native-world-files-file-h5msm>`: JSON/YAML
transport materializes the encoded arrays. Standalone ChemicalStatesDict and
InteractionsDict retain their existing typed NumPy contracts.

## Invariants and Performance

`copy()`, Python `copy.copy`/`copy.deepcopy` and `to_dict(copy=True)` detach mutable
wrapper payloads without validating the schema or decoding a molecular system.
`data` and `to_dict(copy=False)` expose mutable data. Such edits do not notify an
owning system. See {ref}`Native Copying <user-foundations-resident-copying>`.

## Querying Attributes

Use `msm.get(payload, ...)` and `msm.info(payload, ...)`; this dictionary wrapper
has no resident `get()` method. Stored atom-index/label queries have a bounded
direct route when their required fields are already normalized. Other queries
use supported native decoding. Explicit chemical state/structure-associated
queries resolve the decoded independent collection without changing the payload's
reference. This is not an on-disk or bounded chemical-column query guarantee.
