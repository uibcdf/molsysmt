(user-foundations-molecular-system-definition)=
# The Molecular System

**MolSysMT** (*Molecular Systems Multi-Toolkit*) defines a **molecular system** as an abstract physical and chemical model representing a collection of atoms, groups, molecules, or macromolecular assemblies along with their structural, topological, mechanical, and chemical properties.

Crucially, in MolSysMT a molecular system is **independent of its underlying data representation or file format**. A system can be represented by a PDB file on disk, a BinaryCIF file, an OpenMM `Topology` object in memory, an MDTraj `Trajectory`, a ParmEd `Structure`, or a native `molsysmt.MolSys` dictionary. While these representation forms may carry different levels of detail or subsets of attributes—for instance, an OpenMM `Topology` contains structural connectivity but no atomic coordinates, whereas an MDTraj `Trajectory` contains coordinates but may lack certain force field metadata—MolSysMT treats all of them as valid representation forms of the same molecular system we work with.

---

## The Form-Agnostic Paradigm

Traditional molecular modeling workflows often tie analysis scripts to specific software libraries or file formats. MolSysMT eliminates format lock-in by placing **form agnosticism** at the core of its architecture:

- **Form-Agnostic Functionality**: Virtually all functions in MolSysMT are form-agnostic. Whether querying, selecting, comparing, or building systems, functions accept any supported input form transparently. Only internal helper functions within the form-specific `molsysmt.form` submodules are form-specific by design.
- **Transparent Interoperability**: Data is read or converted on-the-fly only when necessary, minimizing memory overhead and execution latency while ensuring seamless integration across software ecosystems.
- **Fidelity Verification**: When converting between different representation forms, MolSysMT validates schema compatibility and reports structural or topological omissions explicitly via preflight fidelity reports.

---

## Architectural Layers

A complete molecular system in MolSysMT is composed of four non-exclusive, complementary architectural layers:

### 1. Topology Layer
Defines the physical inventory of elements (`atoms`, `groups`, `components`, `molecules`, `chains`, `entities`, `bioassemblies`) and their chemical connectivity (covalent bonds, formal bond orders, aromaticity, and chemical state descriptors, among others).

### 2. Structure Layer
Defines spatial geometry, temporal evolution, and structural properties. Key examples of structural attributes include 3D atom coordinates with shape `(n_structures, n_atoms, 3)`, periodic box vectors with shape `(n_structures, 3, 3)`, simulation time points, and structure indices or IDs, among others.

### 3. Molecular Mechanics Layer
Defines force field parameters and mechanical attributes required for energy evaluation and molecular dynamics simulations, such as atomic partial charges, formal masses, force field atom types, non-bonded parameters, and harmonic term constants, among others.

### 4. Chemical State Layer
Defines state-dependent chemical variations, such as explicit protonation states, tautomeric forms, stereochemical configurations (`R`/`S`, `E`/`Z`), and chemical-state associations across structures, among others.

---

## Single vs. Multiple-Item Systems

A molecular system in MolSysMT can be instantiated from a single item or built by combining multiple items:

- **Single-Item System**: A system represented by a single container file or Python object (such as a PDB file, an `.h5msm` file, or a `molsysmt.MolSys` object). A single-item system does not need to contain every possible attribute; it may represent a partial model with missing attributes, which is completely valid—it is simply the molecular system as currently defined.
- **Multiple-Item System**: A system constructed by combining multiple complementary items—for example, pairing a topology file (`.prmtop` or `.psf`) with a coordinate or trajectory file (`.inpcrd` or `.dcd`). MolSysMT merges these complementary items into a single unified molecular system.
