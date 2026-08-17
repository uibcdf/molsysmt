# Micro-Governance: get_radius_of_gyration.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/get_radius_of_gyration.ipynb` (`msm.structure.get_radius_of_gyration`).

## Variable Naming Invariant
The canonical variable representing the input molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_radius_of_gyration)=`
   - H1 Title `# Get radius of gyration`
   - Italic gerund summary `*Computing the radius of gyration of a molecular system.*`
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
   - Geometric radius of gyration with `get_radius_of_gyration`.
   - Header H2 `## Mass-weighted radius of gyration`
   - Mass-weighted calculation with `weights='masses'`.
   - Header H2 `## Plotting radius of gyration trajectory`
   - Matplotlib dual-panel plot (time series + distribution histogram).
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
