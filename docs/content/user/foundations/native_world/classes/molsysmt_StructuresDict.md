(user-foundations-native-world-classes-molsysmt-structuresdict)=
# StructuresDict

`molsysmt.StructuresDict` is the form name for a **plain Python dictionary**
of structure arrays and quantities. There is no public `msm.StructuresDict`
constructor. This in-memory form is different from `MolSysDict 0.1`'s nested
structural record and from a serialized structures YAML file.

## Declarative Schema

Converting native Structures emits available fields only; absent fields may
be omitted. The dictionary carries no `format`, `kind` or `version` envelope.

| Key | Stored value | Physical units | Shape or meaning |
| :--- | :--- | :--- | :--- |
| `coordinates` | quantity | length, e.g. nm | `(n_structures, n_atoms, 3)`. |
| `velocities` | quantity | length/time, e.g. nm/ps | `(n_structures, n_atoms, 3)`. |
| `box` | quantity | length, e.g. nm | `(n_structures, 3, 3)`, box vectors in rows. |
| `time` | quantity | time, e.g. ps | `(n_structures,)`. |
| `structure_id` | array | none | `(n_structures,)`, structure labels rather than positional indices. |
| `b_factor` | quantity | length squared, e.g. nm² | `(n_structures, n_atoms)`. |
| `occupancy` | array | dimensionless | `(n_structures, n_atoms)`. |
| `alternate_location` | sequence of dictionaries | per entry | One sparse atom-index-to-site mapping per structure; entries can carry arrays and quantities. |
| `temperature` | quantity | temperature, e.g. K | `(n_structures,)`. |
| `potential_energy` | quantity | energy/mole, e.g. kJ/mol | `(n_structures,)`. |
| `kinetic_energy` | quantity | energy/mole, e.g. kJ/mol | `(n_structures,)`. |

Quantities retain explicit unit information. Use PyUnitWizard to inspect or
convert values; do not assume a bare nested list is a quantity. The ordinary
`msm.get()` result follows the configured unit policy.

## Usage and Workflow

```python
import numpy as np
import molsysmt as msm
from molsysmt.native import Structures

molsys = Structures(coordinates=msm.pyunitwizard.quantity(
    np.arange(12, dtype=float).reshape(2, 2, 3), 'angstrom'))
structures_dict = msm.convert(molsys, to_form='molsysmt.StructuresDict')
assert type(structures_dict) is dict
assert msm.get_form(structures_dict) == 'molsysmt.StructuresDict'
assert msm.pyunitwizard.is_quantity(structures_dict['coordinates'])
rebuilt = msm.convert(structures_dict, to_form='molsysmt.Structures')
np.testing.assert_allclose(
    msm.pyunitwizard.get_value(rebuilt.coordinates, to_unit='angstrom'),
    np.arange(12, dtype=float).reshape(2, 2, 3))
```

## Persistence Limits

This dictionary is not directly JSON serializable: arrays, quantities and
sparse alternate-site entries require their own encoding. The in-memory form
does not use base64 strings. Use public `msm.convert()` with
`to_form='file:structures_yaml'` for the versioned quantity/sparse-site codec,
or {ref}`H5MSM <user-foundations-native-world-files-file-h5msm>` for binary
structural persistence. Inspect conversion reports and use `strict=True` when
reported losses must be refused; fields outside the supported dictionary
contract, such as bioassembly information, are not automatically retained.

Atom extraction remaps alternate-site keys to the new local atom axis.
Structure selections preserve order and repetitions. Source labels remain
labels; they must not be substituted for selection indices.

## Invariants and Performance

Use `msm.get()`/`msm.info()` for molecular queries. `structures_dict.get(key)`
is ordinary Python dictionary lookup and performs no molecular selection or
unit normalization. Direct dictionary access is not a whole-system validator.
The dictionary does not provide the resident `Structures.get()` method or
turn a complete trajectory into a small JSON object.

## API Documentation

See {func}`molsysmt.basic.convert`, {func}`molsysmt.basic.get` and
{ref}`the conversion tutorial <Tutorial_Convert>`. The resident owner is
{ref}`Structures <user-foundations-native-world-classes-molsysmt-structures>`.
