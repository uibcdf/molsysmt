# Proposal: Resolution of Global PyUnitWizard Standards Conflict in MolSysSuite

## Abstract

We propose establishing a safe initialization protocol and a local context policy for `pyunitwizard` configurations across the entire `molsyssuite`. Currently, `pyunitwizard` relies on a single shared global state within Python memory to store standard units, default forms, and default parsers. When multiple sibling packages of the suite (e.g., `molsysmt` and `pharmacophoremt`) are imported in the same Python session, their import-time configurations overwrite each other. This results in global state pollution and unexpected unit standardization conflicts (such as potential energy returning in `kcal/mol` instead of `kJ/mol`).

---

## The Problem

`pyunitwizard` manages quantities and units using a global configuration registry. Libraries in the `molsyssuite` define their default standards at import time through an internal `_pyunitwizard.py` module. For example:

*   **`molsysmt`** registers:
    ```python
    puw.configure.set_standard_units(['nm', 'ps', 'K', 'mole', 'dalton', 'e',
                                     'kJ/mol', 'kJ/(mol*nm)', 'kJ/(mol*nm**2)', 'radians'])
    ```
*   **`pharmacophoremt`** registers:
    ```python
    puw.configure.set_standard_units(['nm', 'ps', 'K', 'mole', 'amu', 'e',
                                     'kcal/mol', 'kJ/mol', 'degrees'])
    ```

Because both libraries are imported into the same Python environment, whichever module gets imported last completely overwrites the global standard units of `pyunitwizard`. 

Since `pharmacophoremt` lists `kcal/mol` before `kJ/mol`, any subsequent call to `puw.standardize` on an energy-per-mole quantity (like potential energy or molecular mechanics forces) will automatically downcast the quantity to `kilocalorie / mole` instead of `kilojoule / mole`.

### Impact

1.  **Test Suite Pollution**: During parallel test execution (e.g., using `pytest-xdist`), worker processes that run tests importing downstream packages like `pharmacophoremt` end up with a polluted global `pyunitwizard` state. This causes unrelated molecular mechanics tests in `molsysmt` (which assert outputs in `kilojoule/mole`) to fail unexpectedly.
2.  **Downstream API Mismatches**: A script that imports both `molsysmt` and `pharmacophoremt` will have inconsistent API behaviors depending strictly on the import order of the packages.
3.  **Fragile Architecture**: Downstream and sibling packages break the assumptions of upstream core packages without any warning or direct code interaction.

---

## Proposed Solutions

To prevent global state pollution and resolve standard unit conflicts, we propose the following guidelines for all packages in the `molsyssuite`:

### 1. Safe Initialization Check
Instead of calling `set_standard_units` unconditionally at import time, `_pyunitwizard.py` initialization scripts must check if standard units are already set:

```python
import pyunitwizard as puw

# Only set global defaults if they have not been configured yet
if not puw.configure.get_standard_units():
    puw.configure.set_standard_units([
        'nm', 'ps', 'K', 'mole', 'dalton', 'e',
        'kJ/mol', 'kJ/(mol*nm)', 'kJ/(mol*nm**2)', 'radians'
    ])
```

### 2. Context-Based Local Standardization
Functions that depend on a specific standard unit system for their calculations should use `pyunitwizard` context managers to isolate their configuration dynamically rather than assuming a global state:

```python
with puw.configure.context(standard_units=['nm', 'ps', 'kJ/mol']):
    # Perform local operations safely here
    standardized_output = puw.standardize(raw_quantity)
```

### 3. Suite-Wide Standard Policy
Define a single shared standard units list at the suite level (e.g., in a base package or meta-package) so that all downstream packages inherit a unified coordinate, time, and energy unit standard (`kJ/mol`, `nm`, `ps`).

### 4. Global Test Suite Isolation
Ensure that test suites employ a global, autouse cleanup fixture in their `conftest.py` to restore the default configuration of the library after every single test function. This isolates tests from import-time pollution:

```python
# conftest.py
@pytest.fixture(autouse=True)
def restore_pyunitwizard_config():
    yield
    import pyunitwizard as puw
    puw.configure.set_default_form('pint')
    puw.configure.set_default_parser('pint')
    puw.configure.set_standard_units(['nm', 'ps', 'K', 'mole', 'dalton', 'e',
                                     'kJ/mol', 'kJ/(mol*nm)', 'kJ/(mol*nm**2)', 'radians'])
```

---

## Benefits

*   **Robustness**: Guarantees consistent unit outputs regardless of which packages are imported or the order of imports.
*   **Isolability**: Prevents test suites from randomly failing due to parallel worker test scheduling.
*   **Predictability**: Downstream developers can build plugins and extensions without risking breaking core package unit assumptions.
