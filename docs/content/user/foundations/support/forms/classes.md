(user-foundations-support-forms-classes)=
# Classes

MolSysMT provides a form-agnostic architecture capable of digesting, querying, and converting data across a broad matrix of in-memory object classes from native data structures to major third-party libraries in the Python structural biology ecosystem.

---

## Native

Native MolSysMT objects are engineered for high-performance indexing, zero-loss serialization, and fast spatial queries. For detailed technical specifications, internal schemas, and attributes of each native class, see the [{doc}`Native World Classes Section </content/user/foundations/native_world/classes/index>`].

| Class | Description |
| :--- | :--- |
| **`molsysmt.MolSys`** | Primary unified molecular system container composing topology, structures, and mechanics contracts. |
| **`molsysmt.MolSysBuilder`** | Editable native staging container for incremental system assembly and structural modifications. |
| **`molsysmt.MolSysDict`** | Declarative, serializable dictionary representation of a complete molecular system. |
| **`molsysmt.Topology`** | Native topological graph managing atom inventories, residue groups, and chemical state attributes. |
| **`molsysmt.TopologyDict`** | Declarative, serializable dictionary representation of molecular topology. |
| **`molsysmt.Structures`** | Native 3D coordinate, periodic cell box, and trajectory frame container. |
| **`molsysmt.StructuresDict`** | Declarative, serializable dictionary representation of structural and trajectory data. |
| **`molsysmt.MolecularMechanics`** | Native molecular mechanics object managing force field terms, partial charges, and masses. |
| **`molsysmt.MolecularMechanicsDict`** | Declarative, serializable dictionary representation of molecular mechanics parameters. |
| **`molsysmt.ViewerJSON`** | Lightweight, JSON-serializable graphics schema for 3D visualization. |

---

## Supported Third-Party Classes

MolSysMT seamlessly digests and converts object instances from major ecosystem packages:

| Class | Library | Description |
| :--- | :--- | :--- |
| **`mdtraj.Trajectory`** | MDTraj | Full 3D coordinate and box trajectory ensemble. |
| **`mdtraj.Topology`** | MDTraj | Topological atom and residue hierarchy. |
| **`mdtraj.DCDTrajectoryFile`** | MDTraj | DCD file object handle. |
| **`mdtraj.HDF5TrajectoryFile`** | MDTraj | HDF5 file object handle. |
| **`mdtraj.XTCTrajectoryFile`** | MDTraj | XTC compressed file object handle. |
| **`openmm.Topology`** | OpenMM | Molecular topology object representation. |
| **`openmm.System`** | OpenMM | Physical forcefield system and force terms object. |
| **`openmm.State`** | OpenMM | Thermodynamic state holding coordinates, velocities, and energies. |
| **`openmm.Modeller`** | OpenMM | Structural editing, residue addition, and solvation object. |
| **`openmm.app.PDBFile`** | OpenMM | OpenMM PDB file object representation. |
| **`MDAnalysis.Universe`** | MDAnalysis | Core trajectory and topology container object. |
| **`MDAnalysis.AtomGroup`** | MDAnalysis | Atom selection subset group. |
| **`parmed.Structure`** | ParmEd | Unified molecular topology, coordinate, and forcefield structure. |
| **`parmed.gromacs.GromacsTopologyFile`** | ParmEd | GROMACS topology file object representation. |
| **`parmed.amber.AmberParm`** | ParmEd | AMBER prmtop parameter structure. |
| **`pytraj.Trajectory`** | PyTraj | Trajectory container object representation. |
| **`pytraj.Topology`** | PyTraj | Topology container object representation. |
| **`Bio.PDB.Structure.Structure`** | BioPython | Structural PDB hierarchy object. |
| **`Bio.Seq.Seq`** | BioPython | Biological sequence object. |
| **`Bio.SeqRecord.SeqRecord`** | BioPython | Sequence record with metadata annotations. |
| **`networkx.Graph`** | NetworkX | Covalent graph network topology representation. |
| **`rdkit.Chem.Mol`** | RDKit | Small molecule topology and 3D conformers representation. |
