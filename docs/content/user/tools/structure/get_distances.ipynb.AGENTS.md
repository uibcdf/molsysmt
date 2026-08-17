# Micro-Governance: get_distances.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/get_distances.ipynb` (`msm.structure.get_distances`).

## Variable Naming Invariant
The canonical variable representing the input molecular system MUST be `molsys` and distinct systems MUST be `molsys_A` and `molsys_B`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_distances)=`
   - H1 Title `# Get distances`
   - Italic gerund summary `*Getting the distance between specific elements of a molecular system or two different molecular systems.*`
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
   - Distance between specific atoms across trajectory + Matplotlib time series plot.
   - Distance between geometric centers of residue groups (`center_of_atoms=True, center_of_atoms_2=True`) + Matplotlib end-to-end distance plot.
   - Pairwise distances (`pairs=True`).
   - C-alpha distance matrix + Matplotlib 2D heatmap plot (`plt.imshow`).
   - Distances between two different molecular systems (`molsys_A` and `molsys_B`).
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
