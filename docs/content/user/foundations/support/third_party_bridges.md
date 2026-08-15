(user-foundations-support-third-party-bridges)=
# Third-Party Bridges

MolSysMT acts as a form-agnostic bridge across the Python structural biology ecosystem, enabling transparent conversion, query delegation, and topological synchronization between major computational chemistry packages.

---

## Ecosystem Interoperability Architecture

Soft dependencies in MolSysMT are managed centrally through lazy imports enforced by `@dep_digest` (`molsysmt._depdigest`). Optional third-party packages are never imported at top-level module load time. Instead, adapters dynamically detect package availability when a specific object form or file format is passed into API functions.

---

## Supported Ecosystem Packages

Comprehensive matrix of third-party packages bridged by MolSysMT, their target objects, and integration capabilities:

| Library | Primary Data Objects | Bridge Capabilities | Dependency Tier |
| :--- | :--- | :--- | :--- |
| **MDTraj** | `mdtraj.Trajectory`, `mdtraj.Topology` | Coordinate array extraction, trajectory slicing, selection query translation, file format parsers (`dcd`, `xtc`, `h5`). | Soft Dependency |
| **OpenMM** | `openmm.Topology`, `openmm.System`, `openmm.Modeller` | Force field system creation, OpenMM state extraction, solvation modeling, simulation context bridge. | Soft Dependency |
| **MDAnalysis** | `MDAnalysis.Universe`, `MDAnalysis.AtomGroup` | Trajectory ensemble digestion, selection expression parsing, Universe extraction. | Soft Dependency |
| **ParmEd** | `parmed.Structure`, `parmed.gromacs.GromacsTopology` | Force field parameter editing, format conversion (`mol2`, `top`), molecular topology graph. | Soft Dependency |
| **PyTraj** | `pytraj.Trajectory`, `pytraj.Topology` | CPPTRAJ analysis acceleration, trajectory coordinate extraction. | Soft Dependency |
| **BioPython** | `Bio.PDB.Structure`, `Bio.Seq`, `Bio.SeqRecord` | Structural PDB hierarchy parsing, biological sequence alignment, FASTA/PIR parsing. | Soft Dependency |
| **OpenFF** | `openff.toolkit.topology.Molecule`, `Topology` | Small molecule stereochemistry, SMIRNOFF forcefield assignment. | Soft Dependency |
| **RDKit** | `rdkit.Chem.Mol` | Small molecule 2D/3D conformer generation, SMILES parsing (`string:smiles`, `file:smi`), graph topology. | Soft Dependency |
| **PDBFixer** | `pdbfixer.PDBFixer` | Protein structure fixing, missing heavy atom and residue rebuilding, terminal capping. | Soft Dependency |
| **CuPy** | `cupy.ndarray` | GPU-accelerated 3D coordinate array extraction and spatial transformations. | Soft Dependency |
| **NetworkX** | `networkx.Graph` | Covalent graph network analysis, component connectivity queries. | Hard Dependency |

---

## Bridge Operation Modes

Interoperability bridge operations follow three execution patterns:

| Pattern | Description | Primary API Methods |
| :--- | :--- | :--- |
| **Zero-Copy View** | Direct array pointer sharing for heavy 3D coordinate and trajectory arrays without memory duplication. | `msm.get(..., coordinates=True)` |
| **Form Adapter Conversion** | Lossless conversion between native MolSysMT objects and third-party classes. | `msm.convert(source, to_form=...)` |
| **Delegated Querying** | Transparent delegation of structural queries and selection syntax translation to underlying engines. | `msm.select(source, syntax=...)` |

---

## Third-Party Helper Extensions

Beyond data conversion and selection translation, MolSysMT provides dedicated helper extensions in `molsysmt.third_party` designed to simplify and streamline workflows when working directly with external tools. Detailed, function-by-function tutorials for these extensions are provided in the **User Guide > Tools > Third-Party** section.

| Extension Module | Target Software | Primary Helper Capabilities |
| :--- | :--- | :--- |
| **`msm.third_party.nglview`** | NGLView | Helper functions to manipulate NGLView representations (`show_as_cartoon`, `show_as_surface`), overlay 3D shapes (`add_arrows`, `add_cylinders`, `add_hbonds`), customize color schemes, and export HTML views. |
| **`msm.third_party.openmm`** | OpenMM | Helper functions to construct custom OpenMM forces (`add_harmonic_bond_force`, `pin_atoms`, region restraints) and specialized trajectory reporters (`H5MSMReporter`, `StructuresDictReporter`, `TQDMReporter`). |
| **`msm.third_party.tleap`** | AMBER LEaP | Helper wrappers to streamline system parameterization and LEaP script generation. |
