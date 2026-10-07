(user-foundations-support-molecular-mechanics)=
# Molecular Mechanics Data

MolSysMT standardizes molecular mechanics forcefields, implicit solvent models, non-bonded interaction parameters, and constraint options across simulation engines.

---

## Forcefields and Water Models

Recognized forcefield architectures, explicit water models, and atom-level parameter attributes:

| Attribute / Property | Scope / Options | Description | Canonical Unit |
| :--- | :--- | :--- | :--- |
| **`forcefield`** | AMBER14, CHARMM36, OpenFF, GROMOS, OPLS-AA | Force field parameter definition string or object. | N/A |
| **`water_model`** | TIP3P, TIP4P, TIP4P-Ew, TIP5P, SPC, SPC/E, OPC | Explicit solvent model specification. | N/A |
| **`atom_ff_type`** | Atom | Forcefield-assigned atom type name. | N/A |
| **`partial_charge`** | Atom | Fractional atomic point charge. | `elementary_charge` (`e`) |

---

## Non-Bonded and Continuum Solvent Settings

Cutoff parameters, electrostatics algorithms, and continuum dielectric properties:

| Attribute / Property | Scope / Options | Description | Canonical Unit |
| :--- | :--- | :--- | :--- |
| **`non_bonded_method`** | `NoCutoff`, `CutoffNonPeriodic`, `CutoffPeriodic`, `PME`, `LJPME` | Non-bonded interaction algorithm. | N/A |
| **`cutoff_distance`** | Real positive quantity | Direct-space non-bonded interaction cutoff. | `nanometer` (`nm`) |
| **`switch_distance`** | Real positive quantity | Distance at which non-bonded switching function begins. | `nanometer` (`nm`) |
| **`implicit_solvent`** | `OBC1`, `OBC2`, `GBn`, `GBn2`, `HCT`, `GB` | Implicit continuum solvent model. | N/A |
| **`salt_concentration`** | Real positive quantity | Ionic strength for Debye-Hückel / Generalized Born screening. | `molar` (`M`) |
| **`solute_dielectric`** | Real positive scalar | Relative dielectric permittivity inside the solute cavity (solute dielectric). | N/A |
| **`solvent_dielectric`** | Real positive scalar | Relative dielectric permittivity of bulk solvent (solvent dielectric). | N/A |
| **`dispersion_correction`** | Boolean | Analytical long-range dispersion correction for energy and pressure. | N/A |
| **`ewald_error_tolerance`** | Real positive scalar | Target relative error tolerance for PME / Ewald direct-space sum. | N/A |

---

## Constraints and Integration Parameters

Geometric constraints, rigid water settings, and mass repartitioning:

| Attribute / Property | Scope / Options | Description | Canonical Unit |
| :--- | :--- | :--- | :--- |
| **`constraints`** | `None`, `HBonds`, `AllBonds`, `HAngles` | Geometric distance constraint policy. | N/A |
| **`flexible_constraints`** | Boolean | Policy allowing constrained bonds to vibrate harmonically. | N/A |
| **`rigid_water`** | Boolean | Enforces rigid geometry on tri-atomic water molecules. | N/A |
| **`hydrogen_mass`** | Real positive quantity | Mass repartitioning value assigned to hydrogen atoms for integration stability. | `dalton` (`Da`) |
