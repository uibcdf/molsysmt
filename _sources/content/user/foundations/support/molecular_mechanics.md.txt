(user-foundations-support-molecular-mechanics)=
# Molecular Mechanics Data

MolSysMT provides a unified representation of force fields, water models, non-bonded interaction parameters, and simulation engine metadata.

---

## Supported Mechanics Parameters & Models

| Category | Supported Models & Parameters | Ecosystem Bridge |
| :--- | :--- | :--- |
| **Force Fields** | AMBER14, CHARMM36, GROMOS, OPLS-AA, OpenFF | OpenMM, ParmEd, GROMACS |
| **Water Models** | TIP3P, TIP4P, TIP4P-Ew, TIP5P, SPC, SPC/E | OpenMM, AMBER, GROMACS |
| **Implicit Solvent** | OBC1, OBC2, GBn, GBn2, HCT | OpenMM, AMBER |
| **Non-Bonded Methods** | NoCutoff, CutoffNonPeriodic, CutoffPeriodic, PME, LJPME | OpenMM, GROMACS, CHARMM |
| **Integrators** | Langevin, Verlet, VariableLangevin, Brownian | OpenMM, GROMACS |
