# Molecular mechanics

MolSysMT provides a unified Pythonic interface for molecular mechanics operations—including potential energy calculations, energy minimizations, atomic force evaluations, and parameter definitions.

:::{note} Molecular Mechanics Backend Philosophy
Unlike other areas of MolSysMT where native algorithms are implemented (such as structural analyses, SASA, contact maps, and visual inspection), molecular mechanics calculations intentionally rely on established, high-performance simulation engines (currently **OpenMM** by default). MolSysMT standardizes the interaction with these engines, translating topology formats, parameter files, and force field keywords seamlessly.
:::

|      |      |
| :--- | :--- |
| [Get degrees of freedom](get_degrees_of_freedom.ipynb) | Calculating mechanical degrees of freedom for parameterized systems |
| [Get engine forcefield](get_engine_forcefield.ipynb) | Translating force field specifications into engine parameter definitions |
| [Get forces](get_forces.ipynb) | Extracting atomic force vectors and magnitudes from force fields |
| [Get non-bonded potential energy](get_non_bonded_potential_energy.ipynb) | Calculating non-bonded interaction energies across selections or residue sets |
| [Get potential energy](get_potential_energy.ipynb) | Evaluating total potential energy and force field energy components |
| [Potential energy minimization](potential_energy_minimization.ipynb) | Relaxing molecular structures to local potential energy minima |

```{eval-rst}
.. toctree::
   :maxdepth: 2
   :hidden:

   get_degrees_of_freedom.ipynb
   get_engine_forcefield.ipynb
   get_forces.ipynb
   get_non_bonded_potential_energy.ipynb
   get_potential_energy.ipynb
   potential_energy_minimization.ipynb
```
