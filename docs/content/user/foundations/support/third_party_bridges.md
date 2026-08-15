(user-foundations-support-third-party-bridges)=
# Third-Party Bridges

MolSysMT acts as a form-agnostic bridge across the Python structural biology ecosystem, enabling transparent conversion, query delegation, and topological synchronization between major computational chemistry packages.

---

## Supported Ecosystem Libraries

Overview of major ecosystem packages bridged by MolSysMT and their core conversion capabilities:

| Library | Primary Data Objects | Bridge Capabilities | Dependency Tier |
| :--- | :--- | :--- | :--- |
| **MDTraj** | `mdtraj.Trajectory`, `mdtraj.Topology` | Coordinate array extraction, trajectory slicing, selection query translation. | Soft Dependency |
| **OpenMM** | `openmm.Topology`, `openmm.System`, `openmm.Modeller` | Force field system creation, OpenMM state extraction, solvation modeling. | Soft Dependency |
| **MDAnalysis** | `MDAnalysis.Universe`, `MDAnalysis.AtomGroup` | Trajectory ensemble digestion, selection expression parsing. | Soft Dependency |
| **ParmEd** | `parmed.Structure`, `parmed.gromacs.GromacsTopology` | Force field parameter editing, format conversion, molecular topology graph. | Soft Dependency |
| **PyTraj** | `pytraj.Trajectory`, `pytraj.Topology` | CPPTRAJ analysis acceleration, trajectory coordinate extraction. | Soft Dependency |
| **BioPython** | `Bio.PDB.Structure`, `Bio.Seq`, `Bio.SeqRecord` | Structural PDB hierarchy parsing, biological sequence alignment. | Soft Dependency |
| **OpenFF** | `openff.toolkit.topology.Molecule`, `Topology` | Small molecule stereochemistry, SMIRNOFF forcefield assignment. | Soft Dependency |
| **RDKit** | `rdkit.Chem.Mol` | Small molecule 2D/3D conformer generation, SMILES parsing, graph topology. | Soft Dependency |
| **NetworkX** | `networkx.Graph` | Covalent graph network analysis, component connectivity queries. | Hard Dependency |

---

## Bridge Operation Modes

Interoperability bridge operations follow three execution patterns:

| Pattern | Description | Primary API Methods |
| :--- | :--- | :--- |
| **Zero-Copy View** | Direct array pointer sharing for heavy 3D coordinate and trajectory arrays without memory duplication. | `msm.get(..., coordinates=True)` |
| **Form Adapter Conversion** | Lossless conversion between native MolSysMT objects and third-party classes. | `msm.convert(source, to_form=...)` |
| **Delegated Querying** | Transparent delegation of structural queries to underlying library engines. | `msm.select(source, syntax=...)` |
