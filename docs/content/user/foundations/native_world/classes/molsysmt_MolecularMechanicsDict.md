(user-foundations-native-world-classes-molsysmt-molecularmechanicsdict)=
# MolecularMechanicsDict

`molsysmt.MolecularMechanicsDict` is a registered form represented by a plain
Python dictionary of mechanical parameters. It is not a wrapper class. Values
can include NumPy arrays and quantities, so the dictionary is not necessarily
JSON serializable.

## Declarative Schema

Keys are drawn from the parameter registry; values can be absent or `None`.
Per-atom parameter arrays share one atom-index axis.

| Keys | Stored values | Meaning |
| :--- | :--- | :--- |
| `forcefield`, `water_model` | Names or lists of names | Prepared force-field and water-model settings. |
| `partial_charge`, `atom_ff_type` | Per-atom arrays | Partial charges in elementary charge and force-field typing labels. `atom_ff_type` is not the element-symbol attribute `atom_type`. |
| `formal_charge` | Legacy per-atom array | Compatibility field; `MolSys.chemical_states` remains the chemical-assignment authority. |
| `non_bonded_method`, `cutoff_distance`, `switch_distance` | Method and length quantities | Non-bonded settings; native lengths use nm. |
| `dispersion_correction`, `ewald_error_tolerance` | Boolean and dimensionless tolerance | Non-bonded controls. |
| `hydrogen_mass` | Mass quantity | Hydrogen-mass setting, in Da in native units. General atom masses are not stored under a `mass` key. |
| `constraints`, `flexible_constraints`, `rigid_water` | Constraint settings | Prepared bond/water controls. |
| `implicit_solvent`, `solute_dielectric`, `solvent_dielectric` | Solvent name and dimensionless values | Implicit-solvent settings. |
| `salt_concentration`, `kappa` | Concentration and inverse-length quantities | Salt and screening settings. |

There are no generic `charge` or `mass` keys. This parameter projection does not
carry the complete named assignment reports of `MolecularMechanics` and is not
a replacement for H5MSM domain persistence.

## Independent Copies

Python `parameters.copy()` and `copy.copy(parameters)` retain references to
nested values, as for any plain dictionary. Use `msm.copy(parameters)` or
`copy.deepcopy(parameters)` for independent nested lists, arrays and quantities:

```python
import copy
import numpy as np
import molsysmt as msm

parameters = {
    'forcefield': ['amber14-all.xml'],
    'partial_charge': np.array([0.1, -0.1]),
    'cutoff_distance': msm.pyunitwizard.quantity(1.0, 'nm'),
}
independent = msm.copy(parameters)
independent['forcefield'].append('amber14/tip3p.xml')
independent['partial_charge'][0] = 0.9
assert parameters['forcefield'] == ['amber14-all.xml']
assert parameters['partial_charge'][0] == 0.1
assert copy.copy(parameters)['forcefield'] is parameters['forcefield']
assert msm.pyunitwizard.get_value(independent['cutoff_distance'], to_unit='nm') == 1.0
```

The conversion `msm.convert(mechanics, to_form='molsysmt.MolecularMechanicsDict')`
projects stored parameters. Copying the resulting dictionary does not calculate
charges or parameterize a force field. See
{ref}`Native Copying <user-foundations-resident-copying>`.

## API Documentation

Use {func}`molsysmt.basic.convert` for conversion and the
{doc}`form tools reference </api/form/api_form>` for form discovery and capabilities.
