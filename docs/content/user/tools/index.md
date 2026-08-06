(User_Tools)=
(user-tools-index)=
# Tools

Welcome to the MolSysMT **Toolbox**. These functional modules provide targeted, high-performance tools to build, inspect, manipulate, analyze, and convert molecular systems.

Each module groups specialized operations by domain — working uniformly across all 89 supported forms. Browse the 11 categories below to explore dedicated tutorials for each tool function.

---

## **Sections**

::::{grid} 1 2 2 4
:gutter: 3

:::{grid-item-card} **Basic**
:link: basic/index
:link-type: doc

Form-agnostic core operations to load, inspect, convert, copy, select, compare, add, and display molecular systems.
:::

:::{grid-item-card} **Build**
:link: build/index
:link-type: doc

Native system preparation, missing heavy atom recovery, terminal capping, protonation, solvation, and mutation tools.
:::

:::{grid-item-card} **Topology**
:link: topology/index
:link-type: doc

Covalent bond graphs, connectivity matrices, element inventory, sequence extraction, and secondary structure assignment.
:::

:::{grid-item-card} **Structure**
:link: structure/index
:link-type: doc

Coordinate geometry, spatial measurements, SASA, RMSD, fitting, alignment, radius of gyration, and dihedral angle calculations.
:::

:::{grid-item-card} **PBC**
:link: pbc/index
:link-type: doc

Periodic boundary conditions, unit cell box vectors, minimum image conventions, and boundary unwrapping.
:::

:::{grid-item-card} **Physchem**
:link: physchem/index
:link-type: doc

Physical-chemical descriptors, charge distribution, molecular weights, and thermodynamic degrees of freedom.
:::

:::{grid-item-card} **Hbonds**
:link: hbonds/index
:link-type: doc

Hydrogen-bonding network detection, donor-acceptor identification, and polar interaction monitoring across structures.
:::

:::{grid-item-card} **Molecular Mechanics**
:link: molecular_mechanics/index
:link-type: doc

Forcefield engine assignments, atom typing, partial charges, and mechanics evaluation parameter sets.
:::

:::{grid-item-card} **Element**
:link: element/index
:link-type: doc

Hierarchical sub-entity operations across biological structural tiers (atoms, groups, components, molecules, entities, chains).
:::

:::{grid-item-card} **Form**
:link: form/index
:link-type: doc

Form discovery, capability inspection, attribute availability reporting, and format-specific conversions.
:::

:::{grid-item-card} **Third Party**
:link: third_party/index
:link-type: doc

Zero-friction bridges and handshakes for interoperability with external packages (OpenMM, MDAnalysis, MDTraj, PyTraj, etc.).
:::

::::

```{eval-rst}
.. toctree::
   :maxdepth: 2
   :hidden:

   basic/index.md
   build/index.md
   topology/index.md
   structure/index.md
   pbc/index.md
   physchem/index.md
   hbonds/index.md
   molecular_mechanics/index.md
   element/index.md
   form/index.md
   third_party/index.md
```

---

```{key-takeaway}
The MolSysMT toolbox is form-agnostic. Every function operates uniformly across all 89 supported data structures and file formats.
```
