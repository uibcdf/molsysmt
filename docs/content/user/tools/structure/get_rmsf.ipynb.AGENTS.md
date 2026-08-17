# Micro-Governance: get_rmsf.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/get_rmsf.ipynb` (`msm.structure.get_rmsf`).

## Variable Naming Invariant
The canonical variable representing the trajectory MUST be `molsys` and the fitted trajectory `molsys_fitted`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_rmsf)=`
   - H1 Title `# Get RMSF`
   - Italic gerund summary `*Calculating root-mean-square fluctuations per atom over a trajectory.*`
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
   - `rmsf_heavy = msm.structure.get_rmsf(molsys_fitted, selection='atom_type!="H"')`
   - Header H2 `## Plotting per-atom fluctuation profile`
   - Matplotlib line plot of atomic RMSF profile.
   - Header H2 `## Per-residue fluctuation analysis`
   - Bar chart of average RMSF per residue.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
