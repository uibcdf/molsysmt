# Micro-Governance: get_principal_axes.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/get_principal_axes.ipynb` (`msm.structure.get_principal_axes`).

## Variable Naming Invariant
The canonical variable representing the input coordinates is `coords`, the protein system is `molsys`, and the trajectory is `traj`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_principal_axes)=`
   - H1 Title `# Get principal axes`
   - Italic gerund summary `*Calculating principal axes of inertia and principal moments of a molecular system.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing rectangular coordinate box.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `import numpy as np`, `import matplotlib.pyplot as plt`, `import pyunitwizard as puw`
5. **Cells 5+**:
   - Defining rectangular coordinates box.
   - `axes, moments = msm.structure.get_principal_axes(coords)`
   - Eigenvectors and moments printouts.
   - Header H2 `## Mass-weighted principal moments of inertia on a protein`
   - `axes_prot, moments_prot = msm.structure.get_principal_axes(molsys, selection='atom_type!="H"', weights='masses')`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - Header H2 `## Principal moments evolution over a trajectory`
   - Matplotlib time series plot of $I_1(t), I_2(t), I_3(t)$.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
