(user-foundations-molecular-system-definition)=
# The Molecular System

**MolSysMT** (*Molecular Systems Multi-Toolkit*) defines a **molecular system** as an abstract physical and chemical model representing a collection of atoms, groups, molecules, or macromolecular assemblies along with their structural, topological, mechanical, and chemical properties.

Crucially, in MolSysMT a molecular system is **independent of its underlying data representation or file format**. Whether your system is stored in a PDB file on disk, a BinaryCIF file, an OpenMM `Topology` object in memory, an MDTraj `Trajectory`, a ParmEd `Structure`, or a native `molsysmt.MolSys` dictionary, MolSysMT treats it as the *same unified molecular entity*.

---

## The Form-Agnostic Paradigm

Traditional molecular modeling workflows often tie analysis scripts to specific software libraries or file formats. MolSysMT eliminates format lock-in by placing **form agnosticism** at the core of its architecture:

- **Unified Vocabulary**: Core operations such as `get`, `set`, `select`, `compare`, `convert`, and `view` operate identically regardless of whether the input is a file path, a web database ID, a third-party Python object, or a native data structure.
- **Transparent Interoperability**: Data is read or converted on-the-fly only when necessary, minimizing memory overhead and execution latency while ensuring seamless integration across software ecosystems.
- **Fidelity Verification**: When converting between different representation forms, MolSysMT validates schema compatibility and reports structural or topological omissions explicitly via preflight fidelity reports.

---

## Architectural Layers

A complete molecular system in MolSysMT is composed of four non-exclusive, complementary architectural layers:

### 1. Topology Layer
Defines the physical inventory of elements (`atoms`, `groups`, `components`, `molecules`, `chains`, `entities`, `bioassemblies`) and their chemical connectivity (covalent bonds, formal bond orders, aromaticity, and chemical state descriptors).

### 2. Structure Layer
Defines spatial geometry and temporal evolution: 3D atom coordinates with shape `(n_structures, n_atoms, 3)`, periodic box vectors with shape `(n_structures, 3, 3)`, simulation time points, and structure indices or IDs.

### 3. Molecular Mechanics Layer
Defines force field attributes required for energy evaluation and molecular dynamics simulations: atomic partial charges, formal masses, force field atom types, non-bonded parameters, and harmonic term constants.

### 4. Chemical State Layer
Defines state-dependent chemical variations: explicit protonation states, tautomeric forms, stereochemical configurations (`R`/`S`, `E`/`Z`), and chemical-state associations across structures.

---

## Single vs. Composite Systems

A molecular system in MolSysMT can be instantiated from a single item or composed from multiple complementary items:

- **Single-Item System**: A self-contained file or object (such as an `.h5msm` file, a `.mmcif` file, or a `molsysmt.MolSys` object) that holds topology, structures, and metadata in one container.
- **Composite System**: A system constructed by combining complementary items—for example, pairing a topology file (`.prmtop` or `.psf`) with a coordinate or trajectory file (`.inpcrd` or `.dcd`). MolSysMT merges these complementary sources into a single unified molecular system.
