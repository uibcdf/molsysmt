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
Defines the stable atom inventory and hierarchy (`atoms`, `groups`, `molecules`, `chains`, `entities`, and `bioassemblies`). `Topology.bonds` remains a convenient way to inspect the reference chemical state's covalent bonds; it reads the `ChemicalStates` domain.

### 2. Structure Layer
Defines spatial geometry, temporal evolution, and structural properties—including 3D atom coordinates with shape `(n_structures, n_atoms, 3)`, periodic box vectors with shape `(n_structures, 3, 3)`, simulation time points, and structure indices or IDs.

### 3. Molecular Mechanics Layer
Defines force field parameters and mechanical attributes required for energy evaluation and simulations (e.g., atomic partial charges, formal masses, force field atom types, non-bonded parameters, and harmonic term constants).

### 4. Chemical State Layer
Defines state-dependent chemical variations, including covalent bonds, bond orders, component membership, protonation states, tautomeric forms, and stereochemical assignments (`R`/`S`, `E`/`Z`). A native `MolSys` exposes the collection as `molsys.chemical_states`; `Topology` does not expose a `chemical_states` property. Each state uses the topology's atom-index domain; a standalone `ChemicalStates` collection can specify that domain by atom count alone. Associations between structures and states belong to `MolSys`.

An experimental partial `MolSys` may contain any combination of topology,
chemical states, and structures, or only named interaction analyses. Each
analysis declares atom and structure index domains even when both topology and
structures are absent. `MolSys.extract` can use explicit atom and structure
index lists for such a system; when a domain is undeclared, extraction on that
axis raises an error. `msm.get` reports data from the domains
present, while `msm.has_attribute` reports attributes of an absent domain as
unavailable. A topology without chemical states does not claim zero bonds:
its chemistry is unavailable. Public `msm.convert` writes H5MSM 0.5 when
`to_form="file:h5msm"`; legacy file-form operations remain available for
H5MSM 0.3 and 0.4. The explicit `msm.h5msm.write` and
`msm.h5msm.read` functions use the modular 0.5 schema and preserve supported
partial native systems. The {doc}`H5MSM 0.5 guide
<../../tools/form/file/h5msm_05>` describes the versioned API and its current
limits.

---

## Independent Analysis Results

Available chemistry and validated chemistry are different properties of a
model. An experimental read-only assessment with
`msm.physchem.get_chemical_readiness()` reports stored field coverage and limited
consistency checks for one selected state and structure. Missing fields and
ambiguous state associations remain unknown; the assessment does not repair
the system. Its {ref}`chemical readiness guide <Tutorial_Chemical_Readiness>`
explains why stored formal charges, bond orders or H counts alone do not
certify protonation, valence or readiness for a downstream calculation.

For grouped residues, `msm.build.get_residue_chemical_coverage()` adds a bounded
comparison against exact supported templates. Unsupported groups appear explicitly
as unassessed, and modified residues retain their own chemical identity. Its
{ref}`residue coverage guide <Tutorial_Residue_Chemical_Coverage>` explains why
heavy-atom completeness and candidate H inventories do not establish environmental
protonation, terminal context or repair quality.

An explicit preparation operation can fill
missing chemical assignments on an independent system through a declared
template-to-source atom map. It preserves the source pose and identity, rejects
conflicting assignments and keeps a detached preparation report. It does not
generate missing hydrogens or certify the selected template. See the
{ref}`chemical-template guide <Tutorial_Chemical_Templates>` for this experimental
boundary. Chemical changes invalidate named interaction observations on the
prepared copy; the original input remains unchanged.

Some analyses produce data associated with a molecular system without changing
its topology or structures. The experimental `molsysmt.Interactions` class is
one such result: it records chemically classified observations and the source
atom and structure indices they refer to. A native `MolSys` can hold several
named analyses in `molsys.interactions`; its extraction methods remap their
indices. Each analysis declares which atom relationships and structures were
searched, so an evaluated structure with no matches has a defined scope.
An observed disulfide candidate does not establish a covalent bond.
Derived directional sites are another kind of analysis. Chemical recognition
identifies candidate atoms; a local geometric model proposes directions, with
explicit multiplicity and unsupported or undefined outcomes. A recognized
acceptor is not itself a measured lone-pair direction. Observed donor-to-hydrogen
directions require indexed hydrogen coordinates. These detached hypotheses
neither change chemical states nor become named interaction analyses automatically.
See the {ref}`site-direction guide <Tutorial_Get_hbond_site_directions>` for the
experimental bounded models and their source-index correspondence.
See {doc}`Querying interaction results
<../../tools/interactions/result>` for its current query behavior.

---

## Single vs. Multiple-Item Systems

A molecular system in MolSysMT can be instantiated from a single item or built by combining multiple items:

- **Single-Item System**: A system represented by a single container file or Python object (such as a PDB file, an `.h5msm` file, or a `molsysmt.MolSys` object). A single-item system does not need to contain every possible attribute; it may represent a partial model with missing attributes, which is completely valid—it is simply the molecular system as currently defined.
- **Multiple-Item System**: A system constructed by combining multiple complementary items—for example, pairing a topology file (`.prmtop` or `.psf`) with a coordinate or trajectory file (`.inpcrd` or `.dcd`). MolSysMT merges these complementary items into a single unified molecular system.
