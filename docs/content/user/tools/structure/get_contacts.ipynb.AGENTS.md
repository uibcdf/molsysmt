# Micro-Governance: get_contacts.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/get_contacts.ipynb` (`msm.structure.get_contacts`).

## Variable Naming Invariant
The canonical variable representing the molecular system is `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_contacts)=`
   - H1 Title `# Get contacts`
   - Italic gerund summary `*Computing contact maps and inter-atomic contact matrices.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing TcTIM (1TCD) dataset.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `import numpy as np`, `import matplotlib.pyplot as plt`
5. **Cells 5+**:
   - `molsys = msm.convert(msm.systems['TcTIM']['1tcd.h5msm'])`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - Selection of C-alpha atoms and intra-set contact calculation.
   - 2D contact matrix heatmap with `ax.imshow`.
   - Header H2 `## Computing contacts between two different atom selections`
   - Cross-set contacts with `selection` and `selection_2`.
   - Inter-chain interface heatmap with `ax.imshow`.
   - Header H2 `## Computing contacts between atom-group centroids`
   - Group centroid contacts with `center_of_atoms=True`.
   - Header H2 `## Querying contact pairs list`
   - Pairwise output with `output_type='pairs'` and `output_indices='atom'`.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
