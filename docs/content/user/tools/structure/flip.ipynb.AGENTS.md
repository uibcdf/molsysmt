# Micro-Governance: flip.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/flip.ipynb` (`msm.structure.flip`).

## Variable Naming Invariant
The canonical variable representing the input system is `molsys` and the flipped output `molsys_flipped`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Flip)=`
   - H1 Title `# Flip`
   - Italic gerund summary `*Flipping a molecular system over a specified plane or normal vector.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing POPC lipid dataset.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `import numpy as np`
5. **Cells 5+**:
   - `crd = msm.systems['POPC']['popc.crd']`, `psf = msm.systems['POPC']['popc.psf']`, `molsys = msm.convert([crd, psf], to_form='molsysmt.MolSys')`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - Centering around phosphorus atom (`atom_name=="P"`).
   - Nitrogen atom coordinate inspection before flip.
   - Header H2 `## Flipping coordinates over a plane`
   - `molsys_flipped = msm.structure.flip(molsys, vector=[0, 0, 1], point='[0,0,0] nm')`
   - Nitrogen atom coordinate inspection after flip ($z \to -z$).
   - Header H2 `## Visualizing the flipped conformation in 3D`
   - `molsys_both = msm.basic.concatenate_structures([molsys, molsys_flipped])`
   - Hidden cell `molsysviewer_htmlfile = '_static/views/tools_structure_flip_1.html'`
   - `msm.view(molsys_both)` 3D interactive MolSysViewer view.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
