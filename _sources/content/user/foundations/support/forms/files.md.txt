(user-foundations-support-forms-files)=
# Files

MolSysMT supports a comprehensive set of disk file forms spanning native binary files, PDB/mmCIF structures, trajectory binaries, topological definitions, sequence files, and forcefield parameter files.

---

## Native

Native file formats are specifically engineered for high-performance storage, trajectory streaming, and lossy-free persistence. For complete format specifications and dataset layouts, see the [{doc}`Native World Files Section </content/user/foundations/native_world/files/index>`].

| Form Name | Extension | Description | Native Handler / Parser | Streaming Support |
| :--- | :--- | :--- | :--- | :--- |
| **`file:h5msm`** | `.h5msm` | Native HDF5 binary container | `H5MSMFileHandler` | Full Chunked & Iterative Streaming |

---

## External

MolSysMT seamlessly reads, parses, and writes major third-party disk file formats across computational chemistry tools:

| Form Name | Extension | Description | Native Handler / Parser | Streaming Support |
| :--- | :--- | :--- | :--- | :--- |
| **`file:pdb`** | `.pdb` | Protein Data Bank file | `PDBFileHandler` | Iterative Streaming (`TopologyIterator`, `StructuresIterator`) |
| **`file:cif`** | `.cif` / `.mmcif` | Macromolecular Crystallographic Info | `CIFFileHandler` | Iterative Streaming |
| **`file:cif_gz`** | `.cif.gz` | Gzipped mmCIF file | `CIFFileHandler` | Iterative Streaming |
| **`file:bcif`** | `.bcif` | Binary mmCIF file | Internal BCIF Parser | In-Memory Parsing |
| **`file:bcif_gz`** | `.bcif.gz` | Gzipped Binary mmCIF file | Internal BCIF Parser | In-Memory Parsing |
| **`file:gro`** | `.gro` | GROMACS structure file | `GROFileHandler` | Iterative Streaming |
| **`file:dcd`** | `.dcd` | CHARMM/NAMD binary trajectory | `mdtraj_DCDTrajectoryFile` | Bounded Chunked Streaming |
| **`file:xtc`** | `.xtc` | GROMACS compressed trajectory | `mdtraj_XTCTrajectoryFile` | Bounded Chunked Streaming |
| **`file:h5`** | `.h5` / `.trj.h5` | MDTraj HDF5 trajectory | `mdtraj_HDF5TrajectoryFile` | Chunked Streaming |
| **`file:trjpk`** | `.trjpk` | Compressed trajectory package | Internal Parser | Bounded Streaming |
| **`file:mol2`** | `.mol2` | Tripos MOL2 chemical format | Third-Party Adapter | In-Memory Parsing |
| **`file:prmtop`** | `.prmtop` | AMBER topology file | `openmm_AmberPrmtopFile` | Full Topology Parsing |
| **`file:inpcrd`** | `.inpcrd` | AMBER coordinate file | `openmm_AmberInpcrdFile` | Full Coordinate Parsing |
| **`file:mdcrd`** | `.mdcrd` | AMBER trajectory coordinate file | Third-Party Adapter | Trajectory Parsing |
| **`file:top`** | `.top` | GROMACS topology file | `openmm_GromacsTopFile` | Full Topology Parsing |
| **`file:psf`** | `.psf` | CHARMM topology file | `openmm_CharmmPsfFile` | Full Topology Parsing |
| **`file:crd`** | `.crd` | CHARMM coordinate file | `openmm_CharmmCrdFile` | Full Coordinate Parsing |
| **`file:smi`** | `.smi` | SMILES chemical sequence file | Third-Party Adapter | In-Memory Parsing |
| **`file:fasta`** | `.fasta` / `.fa` | FASTA sequence alignment file | Internal Sequence Parser | Sequence Parsing |
| **`file:pir`** | `.pir` | PIR sequence alignment file | Internal Sequence Parser | Sequence Parsing |
| **`file:xyz`** | `.xyz` | Cartesian XYZ coordinate file | Third-Party Adapter | Coordinate Parsing |
| **`file:xyznpy`** | `.xyz.npy` | NumPy array XYZ trajectory file | Internal Parser | Array Parsing |
| **`file:sdf`** | `.sdf` | Structure-Data File (small molecules) | Third-Party Adapter | In-Memory Parsing |
| **`file:molsys_yaml`** | `.molsys.yaml` | Declarative system YAML specification | Internal YAML Parser | Declarative Parsing |
| **`file:topology_yaml`** | `.topology.yaml` | Declarative topology YAML specification | Internal YAML Parser | Declarative Parsing |
| **`file:structures_yaml`** | `.structures.yaml` | Declarative structures YAML specification | Internal YAML Parser | Declarative Parsing |
