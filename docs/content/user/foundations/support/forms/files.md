(user-foundations-support-forms-files)=
# Files

MolSysMT supports a comprehensive set of disk file forms spanning native binary files, PDB/mmCIF structures, trajectory binaries, topological definitions, and forcefield parameter files.

---

## File Forms Matrix

| Form Name | Extension | Description | Native Handler / Parser | Streaming Support |
| :--- | :--- | :--- | :--- | :--- |
| **`file:h5msm`** | `.h5msm` | Native HDF5 binary container | `H5MSMFileHandler` | Full Chunked & Iterative Streaming |
| **`file:pdb`** | `.pdb` | Protein Data Bank file | `PDBFileHandler` | Iterative Streaming (`TopologyIterator`, `StructuresIterator`) |
| **`file:cif`** | `.cif` / `.mmcif` | Macromolecular Crystallographic Info | `CIFFileHandler` | Iterative Streaming |
| **`file:bcif`** | `.bcif` | Binary mmCIF file | Internal BCIF Parser | In-Memory Parsing |
| **`file:gro`** | `.gro` | GROMACS structure file | `GROFileHandler` | Iterative Streaming |
| **`file:dcd`** | `.dcd` | CHARMM/NAMD binary trajectory | `mdtraj_DCDTrajectoryFile` | Bounded Chunked Streaming |
| **`file:xtc`** | `.xtc` | GROMACS compressed trajectory | `mdtraj_XTCTrajectoryFile` | Bounded Chunked Streaming |
| **`file:mol2`** | `.mol2` | Tripos MOL2 chemical format | Third-Party Adapter | In-Memory Parsing |
| **`file:prmtop`** | `.prmtop` | AMBER topology file | `openmm_AmberPrmtopFile` | Full Topology Parsing |
| **`file:inpcrd`** | `.inpcrd` | AMBER coordinate file | `openmm_AmberInpcrdFile` | Full Coordinate Parsing |
| **`file:psf`** | `.psf` | CHARMM topology file | `openmm_CharmmPsfFile` | Full Topology Parsing |
| **`file:crd`** | `.crd` | CHARMM coordinate file | `openmm_CharmmCrdFile` | Full Coordinate Parsing |
| **`file:sdf`** | `.sdf` | Structure-Data File (small molecules) | Third-Party Adapter | In-Memory Parsing |
