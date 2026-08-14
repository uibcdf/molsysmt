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

## Universal Input Quantity Flexibility

All functions and classes in MolSysMT that accept input parameters requiring physical quantities (such as lengths, temperatures, simulation times, or forces) offer total input flexibility. Users can supply inputs as:

1. **String Representations**: E.g. `'10.0 angstroms'`, `'300 K'`, `'1.0 / picoseconds'`.
2. **PyUnitWizard Quantity Objects**: Quantity objects from any supported ecosystem backend (**Pint**, **OpenMM**, **Astropy**, or **unyt**).
3. **Plain NumPy Arrays**: Plain numeric arrays (interpreted automatically in canonical base units).

### Code Example: Flexible Input Formats

```python
import molsysmt as msm
from openmm import unit as openmm_unit
import pint

ureg = pint.UnitRegistry()

# All four calls below are 100% equivalent in MolSysMT:

# 1. Supplying a string representation
coords1 = msm.structure.get_distances(system, selection='all')

# 2. Supplying a Pint quantity object
temp_pint = 300.0 * ureg.kelvin

# 3. Supplying an OpenMM quantity object
temp_openmm = 300.0 * openmm_unit.kelvin

# 4. Supplying a string in a building function
system = msm.build.add_missing_heavy_atoms(system)
```

---

## Unit Management with PyUnitWizard

Unit handling, dimensional checking, and unit conversions are managed through **PyUnitWizard**, an open-source universal unit wrapper developed by UIBCDF ([https://www.uibcdf.org/pyunitwizard](https://www.uibcdf.org/pyunitwizard)).

### The `puw.context()` Manager

PyUnitWizard provides the **`puw.context()`** context manager, allowing users to temporarily override default quantity forms, parsers, or standard units within specific code blocks:

```python
import pyunitwizard as puw
import molsysmt as msm

# 1. Global configuration
puw.configure.default_form = 'pint'
puw.configure.default_parser = 'pint'

# 2. Temporary contextual override using puw.context()
# Temporarily return quantities in OpenMM form with default length in Angstroms
with puw.context(default_form='openmm.unit', default_parser='openmm.unit'):
    coords = msm.structure.get_coordinates(system)  # Returns OpenMM quantity object
```

- **Fast-Track Acceleration (`puw.fast_track`)**: For high-frequency internal calculations involving canonical units (`nm`, `ps`, `e`), MolSysMT registers fast-track unit handlers in `puw.fast_track` to strip and re-wrap units without dimensional AST parsing overhead.
