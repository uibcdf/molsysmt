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
| **`file:cif.gz`** | `.cif.gz` | Gzipped mmCIF file | `CIFFileHandler` | Iterative Streaming |
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
| **`file:sdf`** | `.sdf` | Single-record V2000/V3000, experimental subset | Native CTAB Parser, no RDKit required | One Record |
| **`file:molsys_yaml`** | `.molsys.yaml` | Declarative system YAML specification | Internal YAML Parser | Declarative Parsing |
| **`file:topology_yaml`** | `.topology.yaml` | Declarative topology YAML specification | Internal YAML Parser | Declarative Parsing |
| **`file:structures_yaml`** | `.structures.yaml` | Declarative structures YAML specification | Internal YAML Parser | Declarative Parsing |

Reading a local compressed CIF preserves the source and neighboring files.
Each read uses independent temporary storage, allowing concurrent reads from an
input directory without write permission. Temporary artifacts are removed after
success or failure. Parsing remains eager; see {ref}`Tutorial_Form_file_cif_gz`.

For local PDB conversion to `molsysmt.MolSys` or `molsysmt.Topology`, use
`get_missing_bonds=False` to retain only connectivity declared in PDB records.
The file and `PDBFileHandler` routes honor the same explicit choice without
invoking OpenMM. Their existing `True` default attempts optional OpenMM inference;
the legacy reader can retain only declared edges if that engine is unavailable
or fails. Reading coordinates does not establish complete connectivity, bond
orders or a protonation state. See {ref}`Tutorial_Form_file_pdb` and
{ref}`cookbook-pdb-connectivity-policy`.

The native SDF adapter retains all explicitly drawn hydrogens, ordinary and
explicit aromatic bonds, formal charges, supported radical counts, isotopes
and coordinates. V3000 also retains coordination relationships and endpoint
direction through native dative roles. Ordinary conversion rejects active stereo flags,
queries and multiple records. No chemical perception occurs on the default
native route. Explicit `stereo_engine='rdkit'` enables the optional CIP provider
for supported tetrahedral and double-bond stereo, without removing source
hydrogens. Enhanced and unsupported stereo remain errors. SD property blocks
need explicit authorization to discard when converting into native objects.
Unselected SDF identity copies preserve bytes after checking only the
single-record envelope, including source chemistry outside the native profile.
Their exact conversion reports certify preservation rather than chemical
validity. Native projection and subset output still require supported parsing.
See {ref}`cookbook-native-sdf` for selections, units and conversion reports.

## Prepared docking records

`file:pdbqt` reads the experimental native AutoDock4 subset: one rigid receptor
or one ligand tree, with explicit charges and types. The explicit string form
is `string:pdbqt_text`, using the prefix `pdbqt_text:`. Input coordinates and B
factors are angstrom and angstrom squared; the native boundary uses PyUnitWizard.
PDBQT does not contain complete connectivity. A ligand's torsion tree must be
retained separately and explicitly omitted when projecting to MolSys. No
chemical preparation is performed. See {ref}`cookbook-native-pdbqt` for writer
requirements, hydrogen policy, selection, strict reports and unsupported dialects.

For `file:inpcrd`, `msm.get(molsys, element="atom", atom_index=True)`
returns positions on the source coordinate-file axis. A selection such as
`[2, 0, 2]` retains that order and repetition without renumbering. An index-only
query uses header metadata without loading coordinates. These positions do not
provide atom IDs, names, groups, bonds or chemical assignments; those require
a compatible topology. See {ref}`Tutorial_Form_file_inpcrd`.
