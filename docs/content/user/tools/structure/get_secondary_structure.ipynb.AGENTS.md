# Micro-Governance: get_secondary_structure.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/get_secondary_structure.ipynb` (`msm.structure.get_secondary_structure`).

## Variable Naming Invariant
The canonical variable representing the input molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_secondary_structure)=`
   - H1 Title `# Get secondary structure`
   - Italic gerund summary `*Assigning secondary structure per residue using DSSP rules.*`
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
   - Simplified 3-state assignment (`simplified=True`).
   - Header H2 `## Full 8-state DSSP assignment`
   - Detailed 8-state assignment (`simplified=False`).
   - Header H2 `## Visualizing secondary structure composition`
   - Bar chart of secondary structure elements distribution.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
