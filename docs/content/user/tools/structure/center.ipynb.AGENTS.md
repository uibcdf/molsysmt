# Micro-Governance: center.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/center.ipynb` (`msm.structure.center`).

## Variable Naming Invariant
The canonical variable representing the input molecular system MUST be `molsys` and the centered system MUST be `molsys_centered`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Center)=`
   - H1 Title `# Center`
   - Italic gerund summary `*Centering a molecular system around coordinate origin or reference points.*`
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
   - `center_before = msm.structure.get_center(molsys)`
   - Matplotlib plot of center coordinates (x, y, z) over time.
   - `molsys_centered = msm.structure.center(molsys)`
   - `center_after = msm.structure.get_center(molsys_centered)`
   - Matplotlib comparison plot of distance to origin before vs after centering.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
