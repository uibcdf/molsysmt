# Micro-Governance: set_dihedral_angles.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/set_dihedral_angles.ipynb` (`msm.structure.set_dihedral_angles`).

## Variable Naming Invariant
The canonical variable representing the input system is `molsys` and modified systems `molsys_mod`, `molsys_multi`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Set_dihedral_angles)=`
   - H1 Title `# Set dihedral angles`
   - Italic gerund summary `*Setting dihedral angles to target values by rotating covalent blocks.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing Met-enkephalin dataset.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `import pyunitwizard as puw`
5. **Cells 5+**:
   - `molsys = msm.convert(msm.systems['Met-enkephalin']['met_enkephalin.h5msm'])`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - Querying $\phi$ quartets and initial angle measurement.
   - Initial 3D view with `molsysviewer_htmlfile = '_static/views/tools_structure_set_dihedral_angles_1.html'` and `msm.view(molsys)`.
   - `molsys_mod = msm.structure.set_dihedral_angles(molsys, dihedral_quartets=phi_quartets[1], angles='60.0 degrees')`.
   - Quantitative angle verification with `get_dihedral_angles`.
   - Modified 3D view with `molsysviewer_htmlfile = '_static/views/tools_structure_set_dihedral_angles_2.html'` and `msm.view(molsys_mod)`.
   - Header H2 `## Setting multiple dihedral angles simultaneously`
   - Simultaneous modification of all $\phi$ angles.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
