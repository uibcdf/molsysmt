# Micro-Governance: rotate.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/rotate.ipynb` (`msm.structure.rotate`).

## Variable Naming Invariant
The canonical variable representing the input system is `molsys` and the rotated system `molsys_rotated`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Rotate)=`
   - H1 Title `# Rotate`
   - Italic gerund summary `*Rotating atomic coordinates by rotation matrices or transformations.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing Met-enkephalin dataset.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `import numpy as np`
5. **Cells 5+**:
   - `molsys = msm.convert(msm.systems['Met-enkephalin']['met_enkephalin.h5msm'])`
   - `molsys = msm.structure.center(molsys, selection='all')`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - Initial 3D view with `molsysviewer_htmlfile = '_static/views/tools_structure_rotate_1.html'` and `msm.view(molsys)`.
   - `molsys_rotated = msm.structure.rotate(molsys, rotation=rotation_matrix)`.
   - Rotated 3D view with `molsysviewer_htmlfile = '_static/views/tools_structure_rotate_2.html'` and `msm.view(molsys_rotated)`.
   - Header H2 `## Rotating around a specific center`
   - Demonstration of `rotation_center`.
   - Header H2 `## Rotating using SciPy Rotation objects`
   - Demonstration of `scipy.spatial.transform.Rotation`.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
