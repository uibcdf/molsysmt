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
| **`file:cif`** | `.cif` / `.mmcif` | Macromolecular Crystallographic Info | `mmcif.io.IoAdapter` | In-Memory Parsing |
| **`file:cif.gz`** | `.cif.gz` | Gzipped mmCIF file | `mmcif.io.IoAdapter` | In-Memory Parsing |
| **`file:bcif`** | `.bcif` | Binary mmCIF file | Internal BCIF Parser | In-Memory Parsing |
| **`file:bcif_gz`** | `.bcif.gz` | Gzipped Binary mmCIF file | Internal BCIF Parser | In-Memory Parsing |
| **`file:gro`** | `.gro` | GROMACS structure file | `GROFileHandler` | Iterative Streaming |
| **`file:dcd`** | `.dcd` | CHARMM/NAMD binary trajectory | `mdtraj_DCDTrajectoryFile` | Bounded Chunked Streaming |
| **`file:xtc`** | `.xtc` | GROMACS compressed trajectory | `mdtraj_XTCTrajectoryFile` | Bounded Chunked Streaming |
| **`file:h5`** | `.h5` / `.trj.h5` | MDTraj HDF5 trajectory | `mdtraj_HDF5TrajectoryFile` | Chunked Streaming |
| **`file:trjpk`** | `.trjpk` | Pickled coordinate arrays and structure metadata | Existing TRJPK reader | In-Memory Parsing |
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

FASTA and PIR record axes use zero-based chain and entity indices. Source record
IDs are string labels, independent of their positions. Index queries preserve
selection order and repetitions; an empty file or selection has an empty axis.
The existing optional Biopython reader supplies sequence record counts without
constructing atom-level chemistry. See {ref}`Tutorial_Form_file_fasta` and
{ref}`Tutorial_Form_file_pir`.

CHARMM CRD supplies positional atom/group metadata through its native topology
conversion, with string atom, group and chain IDs. Atom-index-only queries read
just the header count. A selected native MolSys uses the established sorted atom
order for topology and coordinates together; a coordinate-only Structures subset
retains requested atom order. Empty structure selections remain empty. CRD
coordinates carry units, while absent connectivity, box and time are not inferred.
See {ref}`Tutorial_Form_file_crd`.

Intermediate PDBs used by the `openmm.Simulation` to PDBFixer converter and the
optional PyTraj missing-bond audit are owned by those operations. Managed scratch
is retired after eager reading, on both success and failure; returned in-memory
objects or bond pairs remain usable. Cleanup errors are visible. A separately
requested file output remains a caller-owned result, even in a temporary location.
See {ref}`Tutorial_Form_openmm_Simulation` and {ref}`Tutorial_Get_missing_bonds`.

Simulation PDB export uses its current context pose and box, rather than an older
box stored in the source topology. It converts the single structure box into
OpenMM units before writing; PDB lengths remain in angstroms under other session
unit policies. The source topology is unchanged.

RCSB downloads and PDB-ID/AlphaFold file conversions prepare their data in a
private staging directory beside the destination. They replace the destination
only after download and any requested extraction succeed. An HTTP, streaming or
extraction failure preserves an existing destination; partial staging is retired.
The parent directory must therefore be writable. Cleanup errors remain visible;
an error retiring the staging directory after publication does not roll back the
completed file. These operations do not promise crash durability or rollback after
publication.

The PDB-text and UniProt FASTA adapters can generate output paths when called
without one. They retire those files if writing or closing fails, and transfer
successful results to you. Explicit paths in these two writers remain yours;
a failed direct write can leave partial content for inspection. The high-level
{func}`molsysmt.basic.convert` continues to require an explicit output filename
for file targets. See {ref}`Tutorial_Form_file_pdb` and
{ref}`Tutorial_Form_file_fasta`.
