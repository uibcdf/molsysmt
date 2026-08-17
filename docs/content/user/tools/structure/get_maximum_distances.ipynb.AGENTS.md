# Micro-Governance: get_maximum_distances.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/get_maximum_distances.ipynb` (`msm.structure.get_maximum_distances`).

## Variable Naming Invariant
The canonical variable representing the input molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_maximum_distances)=`
   - H1 Title `# Get maximum distances`
   - Italic gerund summary `*Calculating maximum spatial distances between atom selections or molecular groups.*`
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
   - System diameter calculation with `get_maximum_distances(molsys)`.
   - Header H2 `## Plotting maximum span time series`
   - Matplotlib time series plot of molecular diameter.
   - Header H2 `## Computing maximum distances between atom sets`
   - Maximum distance between two distinct selections.
   - Header H2 `## Computing maximum distances between group centers`
   - Maximum distance between group centroids (`center_of_atoms=True, center_of_atoms_2=True`).
   - Header H2 `## Measuring maximum displacements across structures`
   - Maximum atom displacement with `pairs=True`.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
