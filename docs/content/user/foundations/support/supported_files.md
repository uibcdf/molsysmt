(user-foundations-support-supported-files)=
# Supported Files

MolSysMT supports a comprehensive set of disk file formats spanning structural models, trajectory binary files, topological definitions, and forcefield parameter files.

---

## File Format Support Matrix

| Format Extension | Description | Native Handler / Parser | Streaming Support |
| :--- | :--- | :--- | :--- |
| **`.h5msm`** | Native HDF5 binary container | `file:h5msm` / `H5MSMFileHandler` | Full Chunked & Iterative Streaming |
| **`.pdb`** | Protein Data Bank file | `file:pdb` / `PDBFileHandler` | Iterative Streaming (`TopologyIterator`, `StructuresIterator`) |
| **`.cif` / `.mmcif`** | Macromolecular Crystallographic Info | `file:cif` / `CIFFileHandler` | Iterative Streaming |
| **`.bcif`** | Binary mmCIF file | `file:bcif` | In-Memory Parsing |
| **`.gro`** | GROMACS structure file | `file:gro` / `GROFileHandler` | Iterative Streaming |
| **`.dcd`** | CHARMM/NAMD binary trajectory | `file:dcd` / `mdtraj_DCDTrajectoryFile` | Bounded Chunked Streaming |
| **`.xtc`** | GROMACS compressed trajectory | `file:xtc` / `mdtraj_XTCTrajectoryFile` | Bounded Chunked Streaming |
| **`.mol2`** | Tripos MOL2 chemical format | `file:mol2` | In-Memory Parsing |
| **`.prmtop` / `.inpcrd`** | AMBER topology & coordinate files | `file:prmtop`, `file:inpcrd` | Full Topology & Coordinate Parsing |
| **`.psf` / `.crd`** | CHARMM topology & coordinate files | `file:psf`, `file:crd` | Full Topology & Coordinate Parsing |
| **`.sdf`** | Structure-Data File (small molecules) | `file:sdf` | In-Memory Parsing |
