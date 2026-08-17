# Micro-Governance: translate.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/translate.ipynb` (`msm.structure.translate`).

## Variable Naming Invariant
The canonical variable representing the input system is `molsys` and translated systems `molsys_translated`, `molsys_sub`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Translate)=`
   - H1 Title `# Translate`
   - Italic gerund summary `*Translating atomic coordinates along spatial displacement vectors.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing Met-enkephalin dataset.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `import pyunitwizard as puw`, `import numpy as np`
5. **Cells 5+**:
   - `molsys = msm.convert(msm.systems['Met-enkephalin']['met_enkephalin.h5msm'])`
   - `molsys = msm.structure.center(molsys, selection='all')`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - Initial geometric centroid inspection.
   - Global translation by vector `[1.0, 2.0, -0.5] nm`.
   - Quantitative verification of displaced center.
   - Header H2 `## Translating a specific atom selection`
   - Translation of a specific residue subset with `selection='group_index==0'`.
   - Header H2 `## Frame-by-frame translation along trajectories`
   - Per-frame displacement array broadcasting over pentalanine trajectory.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
