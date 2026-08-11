# OpenMM

MolSysMT can build an `openmm.app.Simulation` directly from a molecular system that
contains both topology and coordinates. The conversion builds an OpenMM `System`, creates
a Langevin integrator, and initializes the resulting `Context` with the first requested
structure.

```python
import molsysmt as msm

molecular_system = msm.convert(
    msm.systems["alanine dipeptide"]["alanine_dipeptide.h5msm"],
    to_form="molsysmt.MolSys",
)
simulation = msm.convert(
    molecular_system,
    to_form="openmm.Simulation",
    structure_indices=0,
    temperature="300 K",
)
```

The default platform is `CPU`, which makes the conversion portable on machines without
an accelerator. Request an installed accelerator explicitly, for example with
`platform="CUDA"`.

The initial structure is never invented. A source without coordinates is rejected, and
when `structure_indices` contains multiple entries, their order is preserved and the
first requested structure initializes the context. An `openmm.System` alone cannot be
converted into a `Simulation`, because it does not contain the required topology or
coordinates. An `openmm.Topology` can be used when coordinates are supplied explicitly.

Force fields and water models use MolSysMT's canonical names, such as
`forcefield="AMBER14"` and `water_model="TIP3P-FB"`.

```{eval-rst}
.. toctree::
   :maxdepth: 2

   forces/index.md
   reporters/index.md
   
```
