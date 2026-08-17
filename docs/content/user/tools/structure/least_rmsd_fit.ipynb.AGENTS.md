# Micro-Governance: least_rmsd_fit.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/least_rmsd_fit.ipynb` (`msm.structure.least_rmsd_fit`).

## Variable Naming Invariant
The canonical variable representing the input trajectory MUST be `molsys` and the fitted output `molsys_fitted`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Least_rmsd_fit)=`
   - H1 Title `# Least RMSD fit`
   - Italic gerund summary `*Superposing a molecular system onto a reference structure using the Kabsch algorithm.*`
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
   - `molsys_fitted = msm.structure.least_rmsd_fit(molsys, selection='all', selection_fit='backbone', reference_structure_index=0)`
   - Header H2 `## Verifying alignment with get_rmsd`
   - Comparison of `get_rmsd(molsys_fitted)` with `get_least_rmsd(molsys)`.
   - Header H2 `## Plotting fitted trajectory RMSD`
   - Matplotlib time series comparison plot before vs after fitting.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
