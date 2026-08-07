(user-foundations-governance-quantities-and-units)=
# Quantities & Units

Physical quantities and unit safety are fundamental constitutional guarantees in MolSysMT. Structural biology calculations demand strict dimensional consistency to prevent numerical corruption when mixing data across software packages.

---

## The Unit-Safety Principle

In MolSysMT, physical quantities are treated as first-class citizens. Functions returning spatial coordinates, velocities, forces, box dimensions, or simulation times return array quantities explicitly bound to physical units.

---

## Canonical Internal Units

While MolSysMT accepts input quantities expressed in any valid physical unit (e.g. Angstroms, Picometers, Calorie/mol), internal computations normalize quantities into canonical base units:

- **Length**: `nanometers` (`nm`)
- **Time**: `picoseconds` (`ps`)
- **Temperature**: `kelvin` (`K`)
- **Charge**: `elementary charge` (`e`)
- **Mass**: `daltons` (`Da`)
- **Energy**: `kilojoules / mole` (`kJ/mol`)

---

## Unit Enforcement via PyUnitWizard

Unit handling, dimensional checking, and unit conversions are managed through the **`pyunitwizard`** library:

- **Universal Interoperability**: Seamlessly converts quantities between Pint, OpenMM, Astropy, and native NumPy representations.
- **Fast-Track Acceleration (`puw.fast_track`)**: For high-frequency internal calculations involving canonical units (`nm`, `ps`, `e`), MolSysMT registers fast-track unit handlers in `puw.fast_track` to strip and re-wrap units without dimensional AST parsing overhead.
