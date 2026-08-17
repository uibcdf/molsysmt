# Micro-Governance: get_angles.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/get_angles.ipynb` (`msm.structure.get_angles`).

## Variable Naming Invariant
The canonical variable representing the molecular system is `molsys` or `traj`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_angles)=`
   - H1 Title `# Get angles`
   - Italic gerund summary `*Calculating bond and valence angles defined by atom triplets.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing Met-enkephalin dataset.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `import pyunitwizard as puw`, `import matplotlib.pyplot as plt`
5. **Cells 5+**:
   - `molsys = msm.convert(msm.systems['Met-enkephalin']['met_enkephalin.h5msm'])`
   - Single triplet angle computation.
   - Header H2 `## Angle evolution across structural ensembles`
   - Plotting angle time series across pentalanine ensemble with Matplotlib.
   - Header H2 `## Computing multiple angle triplets concurrently`
   - Passing multiple triplets concurrently.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
