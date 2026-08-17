# Micro-Governance: get_minimum_distances.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/get_minimum_distances.ipynb` (`msm.structure.get_minimum_distances`).

## Variable Naming Invariant
The canonical variable representing the trajectory system MUST be `molsys` and the dimeric system MUST be `tctim`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_minimum_distances)=`
   - H1 Title `# Get minimum distances`
   - Italic gerund summary `*Calculating minimum spatial distances between atom selections or molecular groups.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing pentalanine trajectory dataset.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `import matplotlib.pyplot as plt`, `import pyunitwizard as puw`
5. **Cells 5+**:
   - `molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'])`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - `pairs, min_distances = msm.structure.get_minimum_distances(molsys, selection='group_index==0', selection_2='group_index==4')`
   - Header H2 `## Plotting minimum distance time series`
   - Matplotlib time series plot of $d_{\min}(t)$.
   - Header H2 `## Computing minimum distance between whole chains`
   - TcTIM inter-chain minimum contact calculation.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
