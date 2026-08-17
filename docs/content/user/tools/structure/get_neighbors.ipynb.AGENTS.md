# Micro-Governance: get_neighbors.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/get_neighbors.ipynb` (`msm.structure.get_neighbors`).

## Variable Naming Invariant
The canonical variable representing the input molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_neighbors)=`
   - H1 Title `# Get neighbors`
   - Italic gerund summary `*Finding neighboring atoms or residue groups within a distance threshold or by nearest count.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing TcTIM dataset.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `import matplotlib.pyplot as plt`, `import numpy as np`
5. **Cells 5+**:
   - `molsys = msm.convert(msm.systems['TcTIM']['1tcd.h5msm'])`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - Header H2 `## Querying fixed nearest neighbors`
   - Nearest neighbor query with `n_neighbors=3`.
   - Header H2 `## Cutoff-based neighbor search`
   - Spherical cutoff search with `threshold='0.6 nm'`.
   - Header H2 `## Visualizing neighbor count distribution`
   - Matplotlib histogram plot of local packing density.
   - Header H2 `## Inter-set neighbor search`
   - Inter-set contacts between reference and target selections.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
