# Micro-Governance: wrap_to_pbc.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/pbc/wrap_to_pbc.ipynb` (`msm.pbc.wrap_to_pbc`).

## Variable Naming Invariant
The canonical variable representing the molecular system is `molsys` and wrapped system `molsys_wrapped`, `molsys_pep_wrapped`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Wrap_to_pbc)=`
   - H1 Title `# Wrap to PBC`
   - Italic gerund summary `*Wrapping atomic coordinates into the primary periodic boundary condition unit cell.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing two LJ particles trajectory.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `import numpy as np`, `import matplotlib.pyplot as plt`
5. **Cells 5+**:
   - `molsys = msm.convert(msm.systems['two LJ particles']['traj_two_lj_particles.trjpk'], to_form='molsysmt.StructuresDict')`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - Plotting continuous trajectory before wrapping.
   - Wrapping with `molsys_wrapped = msm.pbc.wrap_to_pbc(molsys)`.
   - Plotting wrapped coordinates inside periodic cell.
   - Quantitative distance invariance test with `msm.structure.get_distances`.
   - Header H2 `## Preserving covalent bonds during macromolecular wrapping`
   - Wrapping solvated peptide with `keep_covalent_bonds=True`.
   - 3D MolSysViewer interactive visualization with `molsysviewer_htmlfile = '_static/views/tools_pbc_wrap_to_pbc_1.html'` and `msm.view(molsys_pep_wrapped)`.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
