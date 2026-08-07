(user-foundations-governance-quantities-and-units)=
# Quantities & Units

Physical quantities and unit safety are fundamental constitutional guarantees in MolSysMT. Structural biology calculations demand strict dimensional consistency to prevent numerical corruption when mixing data across software packages.

---

## The Unit-Safety Principle

In MolSysMT, physical quantities are treated as first-class citizens. Functions returning spatial coordinates, velocities, forces, box dimensions, or simulation times return array quantities explicitly bound to physical units.

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

## Unit Management with PyUnitWizard

Unit handling, dimensional checking, and unit conversions are managed through **PyUnitWizard**, an open-source universal unit wrapper developed by UIBCDF.

- **Universal Ecosystem Support**: PyUnitWizard unifies unit objects from **Pint**, **OpenMM**, **Astropy**, and **unyt** into a single standardized interface.
- **Fast-Track Acceleration (`puw.fast_track`)**: For high-frequency internal calculations involving canonical units (`nm`, `ps`, `e`), MolSysMT registers fast-track unit handlers in `puw.fast_track` to strip and re-wrap units without dimensional AST parsing overhead.
- **Documentation**: Comprehensive PyUnitWizard documentation and API guides are hosted at [https://www.uibcdf.org/pyunitwizard](https://www.uibcdf.org/pyunitwizard).

---

## Customizing Default Output Units and Quantity Forms

Users can query or update output unit preferences and quantity representation forms globally or per session:

```python
import molsysmt as msm
import pyunitwizard as puw

# 1. Inspecting or setting default output units via PyUnitWizard
puw.configure.default_length_unit = 'angstrom'
puw.configure.default_time_unit = 'nanosecond'

# 2. Setting quantity output form (e.g. Pint vs OpenMM vs NumPy plain array)
puw.configure.default_parser = 'pint'

# 3. Temporary unit override using PyUnitWizard context managers
with puw.context(default_length_unit='angstrom'):
    coords = msm.structure.get_coordinates(system)  # Returns array in Angstroms
```
