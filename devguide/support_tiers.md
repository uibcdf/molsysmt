# Support Tiers for Molecular System Forms

To ensure reliability and scientific rigor, MolSysMT classifies supported molecular system forms into three tiers. This classification determines the level of testing, stability guarantees, and the scope of **Contract Testing** for the 1.0.0 release.

---

## 🥇 Tier 1: First-Class Forms (Guaranteed)

Forms in Tier 1 are the core of MolSysMT. They are subject to rigorous **Contract Testing** to ensure that any operation (`get`, `set`, `select`, `extract`) returns mathematically and structurally identical results across all of them.

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
| `string:pdb_id` | Remote | MolSysMT / RCSB PDB |

### 🛡️ Tier 1 Guarantees:
- **Parity**: Identical selection indices for the same query.
- **Unit Stability**: Physical quantities are always returned in standard MolSysMT units (nm, ps, kJ/mol).
- **CI Enforcement**: Any regression in Tier 1 forms blocks a PR merge.

---

## 🥈 Tier 2: Community & Best-Effort Forms

Tier 2 forms are supported and maintained, but they may not cover all edge cases or have full parity guarantees in complex operations.

| Form Name | Category | Provider/Engine |
| :--- | :--- | :--- |
| `MDAnalysis.Universe` | Class | MDAnalysis |
| `parmed.Structure` | Class | ParmEd |
| `pytraj.Trajectory` | Class | Pytraj |
| `file:gro` | File | GROMACS |
| `file:mol2` | File | Tripos |
| `file:xtc` / `file:dcd` | File | Trajectory formats |

### ⚠️ Tier 2 Notes:
- Supported for basic conversions and common attributes.
- May emit warnings if certain MolSysMT features are not fully translatable.

---

## 🥉 Tier 3: Experimental or Niche Forms

Tier 3 includes forms that are under development, deprecated, or highly specialized.

| Form Name | Category | Provider/Engine |
| :--- | :--- | :--- |
| `networkx.Graph` | Class | NetworkX (Topology only) |
| `biopython.Seq` | Class | Biopython |
| `molsysviewer.MolSysView` | Viewer | MolSysViewer |
| Obscure file formats | File | Various |

---

## 🧪 Contract Testing Mandate

For the 1.0.0 release, **Contract Tests** must be implemented for all Tier 1 forms to verify the following invariants:
1. **Schema Identity**: `msm.get(molsys, ...)` must return the same data type and nesting.
2. **Physical Identity**: Coordinate and box values must match within a tolerance of $10^{-5}$ nm after unit standardization.
3. **Selection Identity**: `msm.select(molsys, selection="...")` must return identical index lists.
