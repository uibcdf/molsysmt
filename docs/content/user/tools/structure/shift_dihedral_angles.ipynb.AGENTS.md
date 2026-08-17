# Micro-Governance: shift_dihedral_angles.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/shift_dihedral_angles.ipynb` (`msm.structure.shift_dihedral_angles`).

## Variable Naming Invariant
The canonical variable representing the input system is `molsys` and shifted systems `molsys_shifted`, `molsys_multi_shift`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Shift_dihedral_angles)=`
   - H1 Title `# Shift dihedral angles`
   - Italic gerund summary `*Shifting dihedral angles by incremental angular amounts.*`
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
   - Initial 3D view with `molsysviewer_htmlfile = '_static/views/tools_structure_shift_dihedral_angles_1.html'` and `msm.view(molsys)`.
   - `molsys_shifted = msm.structure.shift_dihedral_angles(molsys, dihedral_quartets=phi_quartets[1], shifts='90.0 degrees')`.
   - Quantitative angle verification with `get_dihedral_angles`.
   - Shifted 3D view with `molsysviewer_htmlfile = '_static/views/tools_structure_shift_dihedral_angles_2.html'` and `msm.view(molsys_shifted)`.
   - Header H2 `## Shifting multiple dihedral angles simultaneously`
   - Simultaneous shifting of all $\phi$ angles.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
