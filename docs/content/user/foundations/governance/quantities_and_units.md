(user-foundations-governance-quantities-and-units)=
# Quantities & Units

Physical quantities and unit safety are fundamental constitutional guarantees in MolSysMT. Structural biology calculations demand strict dimensional consistency to prevent numerical corruption when mixing data across software packages.

---

## The Unit-Safety Principle

In MolSysMT, physical quantities are treated as first-class citizens. Functions returning spatial coordinates, velocities, forces, box dimensions, or simulation times return array quantities explicitly bound to physical units.

By default, physical quantities returned by MolSysMT are represented in the **Pint** quantity form (`default_form='pint'` using the `pint` parser). However, users can configure this default globally or contextually.

---

## Canonical Internal Base Units

While MolSysMT accepts input quantities expressed in any valid physical unit (e.g. Angstroms, Picometers, Calorie/mol), internal computations normalize quantities into canonical base units:

- **Length**: `nanometers` (`nm`)
- **Time**: `picoseconds` (`ps`)
- **Temperature**: `kelvin` (`K`)
- **Charge**: `elementary charge` (`e`)
- **Mass**: `daltons` (`Da`)
- **Energy**: `kilojoules / mole` (`kJ/mol`)

---

## Input quantities

Quantity arguments accept the representations supported by their public
contract and PyUnitWizard configuration: strings such as `'10 angstrom'`,
Pint quantities, and quantities from enabled optional backends such as OpenMM,
Astropy or unyt. An optional backend must be installed before you request it.
The function still validates dimensions, shape and its physical domain.

Do not assume a bare array has a unit. Some operations explicitly accept one
in canonical units; others require a quantity. For example,
{func}`molsysmt.pbc.get_box_from_lengths_and_angles` documents bare NumPy lengths
in nm. These three representations therefore define the same orthogonal box:

```python
import molsysmt as msm
import numpy as np

puw = msm.pyunitwizard
length_inputs = [
    '[20, 30, 40] angstrom',
    puw.quantity([2000., 3000., 4000.], 'pm', form='pint'),
    np.array([2., 3., 4.]),  # documented nm input for this operation
]
boxes = [
    msm.pbc.get_box_from_lengths_and_angles(value)
    for value in length_inputs
]
for box in boxes:
    np.testing.assert_allclose(
        puw.get_value(box, to_unit='nm'), [np.diag([2., 3., 4.])],
    )
```

---

## Unit Management with PyUnitWizard

Unit handling, dimensional checking, and unit conversions are managed through **PyUnitWizard**, an open-source universal unit wrapper developed by UIBCDF ([https://www.uibcdf.org/pyunitwizard](https://www.uibcdf.org/pyunitwizard)).

### Angular Output Policy

{func}`molsysmt.structure.get_dihedral_angles` returns an angle quantity in the
active PyUnitWizard standard-angle unit. MolSysMT initially declares radians;
an application or user policy, including `puw.context`, takes precedence.
A degrees policy therefore returns degrees without changing the physical angle.
For a numerical calculation requiring radians, use
`puw.get_value(angles, to_unit='radians')`. To retain a quantity for display in
degrees, use `puw.convert(angles, to_unit='degrees')`. See
{ref}`Tutorial_Get_dihedral_angles` for examples with molecular structures.

{func}`molsysmt.pbc.get_lengths_and_angles_from_box` standardizes both returned
quantities: edge lengths follow the standard-length unit, and angles follow
the standard-angle unit. Input box units do not fix the output length unit.
For numeric comparisons in specified units, use
`puw.get_value(lengths, to_unit='nm')` and
`puw.get_value(angles, to_unit='radians')`. The
{ref}`box-geometry tutorial <Tutorial_Get_lengths_and_angles_from_box>` defines
the row-vector convention and alpha/beta/gamma ordering.

### The `puw.context()` Manager

PyUnitWizard's **`puw.context()`** temporarily selects an output form, parser and
standard units, then restores the preceding application policy. Changing a form
does not itself choose angstroms: the length standard must also be declared.
This example requires optional OpenMM and keeps Pint as the string parser:

```python
from openmm import unit as openmm_unit

lengths_openmm = openmm_unit.Quantity([20., 30., 40.], openmm_unit.angstrom)
with puw.context(
    default_form='openmm.unit', default_parser='pint',
    standard_units=['angstrom', 'ps', 'radians', 'elementary_charge'],
):
    box_openmm = msm.pbc.get_box_from_lengths_and_angles(lengths_openmm)
    assert puw.get_form(box_openmm) == 'openmm.unit'
    np.testing.assert_allclose(
        puw.get_value(box_openmm, to_unit='angstrom'), [np.diag([20., 30., 40.])],
    )

after_context = msm.pbc.get_box_from_lengths_and_angles('[2, 3, 4] nm')
assert puw.get_form(after_context) == puw.get_form(boxes[0])
assert puw.get_unit(after_context) == puw.get_unit(boxes[0])
```

- **Fast-Track Acceleration (`puw.fast_track`)**: For high-frequency internal calculations involving canonical units (`nm`, `ps`, `e`), MolSysMT registers fast-track unit handlers in `puw.fast_track` to strip and re-wrap units without dimensional AST parsing overhead.

### Comparing physical values

{func}`molsysmt.basic.compare` converts quantity-valued normalized attributes,
such as box lengths, angles and volume, to compatible common units before
numerical comparison. Equal raw magnitudes do not establish physical equality.
Incompatible dimensions compare unequal, and a missing unit is not inferred
from the other operand. See {ref}`Tutorial_Compare` for explicit attribute queries.


## Covariance units and numerical weights

{func}`molsysmt.structure.principal_component_analysis` returns dimensionless
row eigenvectors and eigenvalues in squared-length units. Atom weights are
dimensionless numerical factors; they scale the covariance and are not
normalized by their sum. A length presentation policy of angstrom therefore
returns angstrom² eigenvalues with the same physical variance as nm² output.
See {ref}`Cookbook_Weighting_PCA` for a numerical covariance and projection check.

## Endpoint consistency

Distances and geometric neighborhoods carry two coordinate index spaces. Physical
units must be aligned before comparing endpoints, and index lists retain their
own source and requested structure order. Changing a presentation unit does not
change which observation or atom an index addresses. A periodic comparison uses
the primary source's box; a center uses the supplied participant positions.
See {ref}`user-tools-distance-family` for the operational contract.
