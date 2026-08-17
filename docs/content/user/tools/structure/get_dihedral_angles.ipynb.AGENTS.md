# Micro-Governance: get_dihedral_angles.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/get_dihedral_angles.ipynb` (`msm.structure.get_dihedral_angles`).

## Variable Naming Invariant
The canonical variable representing the input molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_dihedral_angles)=`
   - H1 Title `# Get dihedral angles`
   - Italic gerund summary `*Getting the dihedral angles of a molecular system.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing pentalanine trajectory dataset.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `import numpy as np`
5. **Cells 5+**:
   - `molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - `dihedrals = msm.structure.get_dihedral_angles(molsys, dihedral_quartets=[[4, 6, 8, 14], [6, 8, 14, 16]])`
   - `dihedrals.shape`
   - `dihedrals[0]`
   - Header H2 `## Named backbone dihedral angles`
   - `phi, psi = msm.structure.get_dihedral_angles(molsys, phi=True, psi=True)`
   - `print('phi shape:', phi.shape)`
   - `print('psi shape:', psi.shape)`
   - `phi[0]`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
