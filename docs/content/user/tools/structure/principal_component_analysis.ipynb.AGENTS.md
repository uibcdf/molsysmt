# Micro-Governance: principal_component_analysis.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/principal_component_analysis.ipynb` (`msm.structure.principal_component_analysis`).

## Variable Naming Invariant
The canonical variable representing the trajectory MUST be `molsys` and the fitted trajectory `molsys_fitted`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Principal_component_analysis)=`
   - H1 Title `# Principal Component Analysis`
   - Italic gerund summary `*Computing covariance eigenvectors and eigenvalues to identify principal conformational motions.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing pentalanine trajectory dataset.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `import matplotlib.pyplot as plt`, `import pyunitwizard as puw`, `import numpy as np`
5. **Cells 5+**:
   - `molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'])`
   - `molsys_fitted = msm.structure.least_rmsd_fit(molsys, selection='all', selection_fit='backbone', reference_structure_index=0)`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - `eigenvectors, eigenvalues = msm.structure.principal_component_analysis(molsys_fitted, selection='atom_type!="H"')`
   - Header H2 `## Cumulative explained variance and eigenvalue spectrum`
   - Matplotlib dual bar/line scree plot.
   - Header H2 `## Projecting trajectory onto principal components`
   - 2D scatter plot projection onto PC1 and PC2 colored by time.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
