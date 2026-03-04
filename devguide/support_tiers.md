# Support Tiers for Molecular System Forms

To ensure reliability and scientific rigor, MolSysMT classifies supported molecular system forms into three tiers. This classification determines the level of testing, stability guarantees, and the scope of **Contract Testing**.

---

## 🥇 Tier 1: First-Class Forms (Guaranteed Parity)

Tier 1 forms are the indestructible core of MolSysMT. They are subject to rigorous **Contract Testing** ensuring that any operation returns identical results across the entire stack.

| Form Name | Category | Provider/Engine |
| :--- | :--- | :--- |
| `molsysmt.MolSys` | Native | MolSysMT |
| `molsysmt.Topology` | Native | MolSysMT |
| `molsysmt.Structures` | Native | MolSysMT |
| `openmm.Topology` | Class | OpenMM |
| `mdtraj.Trajectory` | Class | MDTraj |
| `mdtraj.Topology` | Class | MDTraj |
| `file:pdb` | File | MolSysMT / MDTraj |
| `file:h5msm` | File | MolSysMT (Native) |

---

## 🥈 Tier 2: Hardened Ecosystem Forms

Tier 2 forms are stable, hardened, and highly recommended for general use. They have passed the 1.0.0 interoperability audit.

| Form Name | Category | Provider/Engine |
| :--- | :--- | :--- |
| `MDAnalysis.Universe` | Class | MDAnalysis |
| `MDAnalysis.AtomGroup` | Class | MDAnalysis |
| `rdkit.Mol` | Class | RDKit |
| `biopython.PDBStructure`| Class | BioPython |
| `parmed.Structure` | Class | ParmEd |
| `molsysviewer.MolSysView` | Viewer | MolSysViewer |
| `nglview.NGLWidget` | Viewer | NGLView |
| `string:pdb_id` | Remote | MolSysMT / RCSB PDB |

---

## 🥉 Tier 3: Experimental or Niche Forms

Tier 3 includes forms that are under development, deprecated, or highly specialized.

| Form Name | Category | Provider/Engine |
| :--- | :--- | :--- |
| `networkx.Graph` | Class | NetworkX (Topology only) |
| `pytraj.Trajectory` | Class | Pytraj |
| `biopython.Seq` | Class | Biopython (Sequences only) |
| `XYZ` | Format | Standard XYZ |
| Obscure file formats | File | Various |

---

## 🧪 Contract Testing Status (1.0.0)

For the 1.0.0 release, **Contract Tests** verify the following invariants across Tier 1 and Tier 2:
1. **Schema Identity**: `msm.get(molsys, ...)` returns the same data type and nesting. [VERIFIED for Tier 1]
2. **Physical Identity**: Coordinate and box values match within $10^{-5}$ nm. [VERIFIED for Tier 1]
3. **Selection Identity**: `msm.select(molsys, selection="...")` returns identical index lists. [VERIFIED for Tier 1 & Hardened MDA]
4. **Visual Introspection**: High-level API calls (`get`, `compare`) work directly on Viewer objects. [VERIFIED for MolSysViewer]
