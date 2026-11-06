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

Model vocabularies do not imply that every engine supports every combination.
Engine-specific resource mappings are metadata: ordered XML or leaprc names,
returned as independent lists. Editing a returned list does not change later
parameterizations or another caller's resources. These names have no physical
units. Inspecting them requires neither an installed engine nor installed
parameter files; construction and scientific model configuration are separate
steps. A stored model request does not certify completed parameterization.

The solute force field, solvation model and execution engine are separate
choices. `OBC1` and `OBC2` identify the two Onufriev-Bashford-Case variants,
corresponding to Amber `igb=2` and `igb=5`. The current OpenMM adapter supports
them for its seven registered AMBER solute fields and uses the engine's
standard model definitions. A future engine translates the same physical
choices within its own adapter or refuses unsupported combinations. OpenMM
resources and force classes are not part of the native mechanics model.

---

## Non-Bonded and Continuum Solvent Settings

Cutoff parameters, electrostatics algorithms, and continuum dielectric properties:

| Attribute / Property | Scope / Options | Description | Canonical Unit |
| :--- | :--- | :--- | :--- |
| **`non_bonded_method`** | `NoCutoff`, `CutoffNonPeriodic`, `CutoffPeriodic`, `PME`, `LJPME` | Non-bonded interaction algorithm. | N/A |
| **`cutoff_distance`** | Real positive quantity | Direct-space non-bonded interaction cutoff. | `nanometer` (`nm`) |
| **`switch_distance`** | Real positive quantity | Distance at which non-bonded switching function begins. | `nanometer` (`nm`) |
| **`implicit_solvent`** | `None`, `OBC1`, `OBC2`, subject to engine support | Requested continuum solvent variant; `None` requests no implicit model. | N/A |
| **`salt_concentration`** | Real positive quantity | Ionic strength for Debye-Hückel / Generalized Born screening. | `molar` (`M`) |
| **`solute_dielectric`** | Real positive scalar | Relative dielectric permittivity inside the solute cavity (solute dielectric). | N/A |
| **`solvent_dielectric`** | Real positive scalar | Relative dielectric permittivity of bulk solvent (solvent dielectric). | N/A |

For the current OpenMM OBC adapters, the executed recipe uses mbondi2 radii,
the ACE surface term, solute/solvent dielectric constants 1/78.5 and zero salt
screening, as supplied by OpenMM's standard XML definitions. The converter does
not expose independent dielectric/screening/cutoff controls; storing such fields
in the experimental mechanics container does not establish support for applying
them. OBC construction admits no cutoff, a nonperiodic cutoff or a periodic
cutoff; it refuses PME, Ewald and LJPME. An absent OBC nonbonded setting uses
no cutoff even when a cell is available.

See the [OpenMM model definitions](https://docs.openmm.org/latest/userguide/application/02_running_sims.html#implicit-solvent)
and [Onufriev, Bashford and Case (2004)](https://doi.org/10.1002/prot.20033).
The scientific variant and the engine actually executing it have distinct
attribution roles. Metadata lookup alone records no scientific execution.
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

The execution platform is an engine-owned choice, separate from these physical
parameters. General mechanics validation checks its name format; the selected
adapter resolves supported names and registration. OpenMM admits exact names
such as `Reference`, `CPU`, `CUDA` and `OpenCL`, plus installed plugin names.
Discovery reports registration, which does not certify that a driver/device can
initialize a calculation. Unknown names, known unregistered platforms, missing
engines and subsequent initialization failures have separate diagnostics.

The `platform` argument selects newly constructed contexts. Existing engine
Context/Simulation inputs retain their actual platform; the argument does not
migrate them. A failed explicit request does not choose another platform. The
Reference implementation can be used for small numerical checks against other
platforms, with tolerances reflecting their precision and settings. See the
[engine's platform documentation](https://docs.openmm.org/latest/userguide/library/04_platform_specifics.html).
