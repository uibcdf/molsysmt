(user-foundations-molecular-system-definition)=
# The Molecular System

*Understanding the formal definition and form-agnostic architecture of a molecular system in MolSysMT.*

In MolSysMT, a **molecular system** is a physical or chemical model representing a set of atoms, molecules, or macromolecular assemblies along with their structural, topological, mechanical, and chemical properties.

Crucially, in MolSysMT a molecular system is **independent of its underlying data representation or file format**. Whether your system is stored in a PDB file, a BinaryCIF file, an OpenMM `Topology`, an MDTraj `Trajectory`, a ParmEd `Structure`, or a native `molsysmt.MolSys` object, MolSysMT treats it as the *same unified molecular entity*.

:::{versionadded} 1.0.0
:::

---

## Architectural Layers

A complete molecular system in MolSysMT is composed of four conceptual layers:

1. **Topology Layer**:  
   Defines the physical inventory of elements (`atoms`, `groups`, `components`, `molecules`, `chains`, `entities`, `bioassemblies`) and their connectivity (covalent bonds, formal bond orders, aromaticity, and chemical state descriptors).

2. **Structure Layer**:  
   Defines spatial geometry and temporal evolution: 3D atom coordinates with shape `(n_structures, n_atoms, 3)`, periodic box vectors with shape `(n_structures, 3, 3)`, simulation time points, and structure indices or IDs.

3. **Molecular Mechanics Layer**:  
   Defines force field attributes required for energy evaluation and simulations: atomic partial charges, formal masses, force field atom types, non-bonded parameters, and harmonic term constants.

4. **Chemical State Layer**:  
   Defines state-dependent chemical variations: explicit protonation states, tautomeric forms, stereochemical configurations (`R`/`S`, `E`/`Z`), and chemical-state associations across structures.

---

## Form-Agnostic Philosophy

Traditional molecular modeling workflows often tie analysis scripts to specific software libraries or file formats. MolSysMT eliminates format lock-in by providing a transparent, unified API across all forms:

- **Form Agnosticism**: Functions like `msm.get()`, `msm.select()`, `msm.compare()`, and `msm.convert()` operate identically regardless of whether the input is a file path, a third-party Python object, or a native dictionary.
- **Lazy Conversion**: Data is converted on-the-fly only when necessary, minimizing memory overhead and execution latency.
- **Fidelity Verification**: When converting between forms, MolSysMT validates schema compatibility and reports any structural or topological omissions explicitly.

---

:::{seealso}
{ref}`Introduction_Forms`:  
Learn how physical items differ from representation forms and explore the catalog of supported forms.

{ref}`user-foundations-02-molecular-system`:  
Return to the main Molecular System section overview.
:::
