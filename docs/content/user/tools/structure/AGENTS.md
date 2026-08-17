# Sub-Portal Governance: `tools/structure/` (`AGENTS.md`)

This guide governs all content under `docs/content/user/tools/structure/`.

---

## 🧭 Subdirectory Purpose & Scope
Houses tutorial units for structural coordinate operations, spatial measurements, RMSD, PCA, fitting, alignment, center of mass/geometry, radius of gyration, dihedral angles, and contact matrices.

## 📐 Scientific & Architectural Invariants for Structure Tutorials
1. **Data Dimensions & Units**:
   - Coordinate arrays follow shape `(n_structures, n_atoms, 3)` with units explicitly in nanometers (`nm`).
   - Structural distances ($d$) are in `nm` or `angstroms`.
   - Angles ($	heta, \phi, \psi, \omega, \chi$) are reported in degrees (`degrees`) or radians (`rad`).
2. **Mandatory Visual & Graphical Richness**:
   - Every function calculating continuous structural metrics over trajectories (such as distances $d(t)$, angles $	heta(t)$, dihedral series, RMSD, radius of gyration, or PCA projections) **MUST** include clear `matplotlib.pyplot` time-series or scatter plots.
   - Matrix-valued functions (contacts, pairwise distance maps) **MUST** include 2D heatmap plots using `plt.imshow`.
   - Geometric transformations (alignments, coordinate reflections, centering) **MUST** include interactive 3D MolSysViewer scenes or before/after displacement comparisons.
3. **Multi-Scenario Pedagogical Coverage**:
   - Tutorials must cover both single-atom/triplet/quartet queries and realistic macromolecular scenarios (residue selections, intra/inter-chain contacts, whole-system spans, or external native reference comparisons).

## 📄 Pages List & Paired Micro-`AGENTS.md` Files
- `index.md` ➔ `index.AGENTS.md`: Index portal with 2-column function catalog table and hidden `toctree`.
- `align_principal_axes.ipynb` ➔ `align_principal_axes.ipynb.AGENTS.md`
- `center.ipynb` ➔ `center.ipynb.AGENTS.md`
- `flip.ipynb` ➔ `flip.ipynb.AGENTS.md`
- `get_angles.ipynb` ➔ `get_angles.ipynb.AGENTS.md`
- `get_center.ipynb` ➔ `get_center.ipynb.AGENTS.md`
- `get_contacts.ipynb` ➔ `get_contacts.ipynb.AGENTS.md`
- `get_dihedral_angles.ipynb` ➔ `get_dihedral_angles.ipynb.AGENTS.md`
- `get_distances.ipynb` ➔ `get_distances.ipynb.AGENTS.md`
- `get_least_rmsd.ipynb` ➔ `get_least_rmsd.ipynb.AGENTS.md`
- `get_maximum_distances.ipynb` ➔ `get_maximum_distances.ipynb.AGENTS.md`
- `get_minimum_distances.ipynb` ➔ `get_minimum_distances.ipynb.AGENTS.md`
- `get_neighbors.ipynb` ➔ `get_neighbors.ipynb.AGENTS.md`
- `get_principal_axes.ipynb` ➔ `get_principal_axes.ipynb.AGENTS.md`
- `get_radius_of_gyration.ipynb` ➔ `get_radius_of_gyration.ipynb.AGENTS.md`
- `get_rmsd.ipynb` ➔ `get_rmsd.ipynb.AGENTS.md`
- `get_rmsf.ipynb` ➔ `get_rmsf.ipynb.AGENTS.md`
- `get_secondary_structure.ipynb` ➔ `get_secondary_structure.ipynb.AGENTS.md`
- `least_rmsd_align.ipynb` ➔ `least_rmsd_align.ipynb.AGENTS.md`
- `least_rmsd_fit.ipynb` ➔ `least_rmsd_fit.ipynb.AGENTS.md`
- `move_away.ipynb` ➔ `move_away.ipynb.AGENTS.md`
- `principal_component_analysis.ipynb` ➔ `principal_component_analysis.ipynb.AGENTS.md`
- `rotate.ipynb` ➔ `rotate.ipynb.AGENTS.md`
- `set_dihedral_angles.ipynb` ➔ `set_dihedral_angles.ipynb.AGENTS.md`
- `shift_dihedral_angles.ipynb` ➔ `shift_dihedral_angles.ipynb.AGENTS.md`
- `translate.ipynb` ➔ `translate.ipynb.AGENTS.md`
