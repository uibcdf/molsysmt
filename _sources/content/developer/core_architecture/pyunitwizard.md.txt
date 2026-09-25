# Physical Units Architecture

MolSysMT relies on **PyUnitWizard** to manage physical quantities, unit conversion, and dimension safety across all molecular calculations.

---

## 1. Canonical Library Units

To ensure numerical consistency across all algorithms, MolSysMT standardizes internally on canonical SI/molecular units:

| Physical Dimension | Canonical Unit | Representation |
| :--- | :--- | :--- |
| **Length** | Nanometer | `nm` |
| **Time** | Picosecond | `ps` |
| **Mass** | Dalton / amu | `Da` |
| **Temperature** | Kelvin | `K` |
| **Angle** | Radians | `rad` |
| **Electric Charge** | Elementary charge | `e` |
| **Energy** | Kilojoules per mole | `kJ/mol` |
| **Force** | Kilojoules per mole per nanometer | `kJ/(mol*nm)` |

---

## 2. Fast-Track Unit Bypass

Unit conversion can introduce significant overhead if applied naively inside performance-critical numerical loops. MolSysMT registers canonical units in the PyUnitWizard Fast-Track cache (`puw.fast_track` in `molsysmt._pyunitwizard`).

When input quantities already match canonical units:
- PyUnitWizard performs an instant bypass without parsing unit strings or invoking heavy quantity wrappers.
- NumPy arrays are passed directly to numerical kernels.

---

## 3. Developer Best Practices

- **Never hardcode conversion factors**: Always use PyUnitWizard functions (`puw.get_value`, `puw.convert`, `puw.standardize`) when handling user-provided quantities with units.
- **Return quantities with standard units**: Public functions that return physical dimensions (e.g. coordinates, distances, energies, forces, areas) must return quantities explicitly wrapped with standard units unless documented otherwise.
- **Strip units before native kernels**: When delegating to Numba or Rust kernels, extract raw NumPy values with `puw.get_value(quantity, to_unit=canonical_unit)`.
