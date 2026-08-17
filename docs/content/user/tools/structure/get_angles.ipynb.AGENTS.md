# Micro-Governance: get_angles.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/get_angles.ipynb` (`msm.structure.get_angles`).

## Variable Naming Invariant
The canonical variable representing the input molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_angles)=`
   - H1 Title `# Get angles`
   - Italic gerund summary `*Getting angles between specific triplets of atoms in a molecular system.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing pentalanine trajectory dataset.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `import numpy as np`, `import matplotlib.pyplot as plt`
5. **Cells 5+**:
   - `molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - `msm.info(molsys, element='atom', selection=[0, 1, 2])`
   - `angles = msm.structure.get_angles(molsys, [0, 1, 2])`
   - `angles_deg = msm.pyunitwizard.convert(angles, to_unit='degrees')`
   - Shape and mean printouts.
   - Matplotlib time evolution plot.
   - Header H2 `## Computing multiple angle triplets`
   - `multi_angles = msm.structure.get_angles(molsys, triplets=[[0, 1, 2], [1, 2, 3]])`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
