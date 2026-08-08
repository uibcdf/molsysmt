(user-foundations-support-forms-classes)=
# Classes

MolSysMT provides a form-agnostic architecture capable of digesting, querying, and converting data across a broad matrix of in-memory object classes from native data structures to major third-party libraries in the Python structural biology ecosystem.

---

## Native Data Structures

Native MolSysMT objects are engineered for high-performance indexing, zero-loss serialization, and fast spatial queries:

- **`molsysmt.MolSys`**: Primary unified molecular system container.
- **`molsysmt.MolSysBuilder`**: Editable staging container for incremental system assembly.
- **`molsysmt.MolSysDict`**: Declarative serializable system dictionary.
- **`molsysmt.Topology`**: Native topological graph and hierarchy representation.
- **`molsysmt.TopologyDict`**: Declarative serializable topology dictionary.
- **`molsysmt.Structures`**: Native 3D coordinate and box trajectory container.
- **`molsysmt.StructuresDict`**: Declarative serializable structure dictionary.
- **`molsysmt.MolecularMechanics`**: Native forcefield and interaction parameters container.
- **`molsysmt.MolecularMechanicsDict`**: Declarative serializable molecular mechanics dictionary.
- **`molsysmt.ViewerJSON`**: 3D rendering schema dictionary.

---

## Third-Party Library In-Memory Objects

MolSysMT seamlessly digests and converts objects from major ecosystem packages:

| Library | Supported Object Classes | Support Level |
| :--- | :--- | :--- |
| **MDTraj** | `mdtraj.Trajectory`, `mdtraj.Topology`, `mdtraj.DCDTrajectoryFile`, `mdtraj.HDF5TrajectoryFile`, `mdtraj.XTCTrajectoryFile` | Full Topology, Coordinates & Trajectories |
| **OpenMM** | `openmm.Topology`, `openmm.System`, `openmm.State`, `openmm.Modeller`, `openmm.app.PDBFile` | Topology, Coordinates & Mechanics |
| **MDAnalysis** | `MDAnalysis.Universe`, `MDAnalysis.AtomGroup` | Full Topology, Coordinates & Trajectories |
| **ParmEd** | `parmed.Structure`, `parmed.gromacs.GromacsTopologyFile`, `parmed.amber.AmberParm` | Topology, Coordinates & Forcefields |
| **PyTraj** | `pytraj.Trajectory`, `pytraj.Topology` | Full Topology & Trajectories |
| **BioPython** | `Bio.PDB.Structure.Structure`, `Bio.Seq.Seq`, `Bio.SeqRecord.SeqRecord` | Topology & Sequence Analysis |
| **NetworkX** | `networkx.Graph` | Chemical & Covalent Bond Graphs |
| **RDKit** | `rdkit.Chem.Mol` | Small Molecule Topology & Conformers |
