# Micro-Governance: align_principal_axes.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/align_principal_axes.ipynb` (`msm.structure.align_principal_axes`).

## Variable Naming Invariant
The canonical variable representing the input molecular system MUST be `molsys` and the aligned system MUST be `molsys_aligned`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Align_principal_axes)=`
   - H1 Title `# Align principal axes`
   - Italic gerund summary `*Aligning the principal inertia or geometric axes of a molecular system over reference coordinate axes.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing POPC dataset.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `import numpy as np`
5. **Cells 5+**:
   - `molsys = msm.convert([crd, psf], to_form='molsysmt.MolSys')`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - `axes, momenta = msm.structure.get_principal_axes(molsys)`
   - Loop printing initial axes and moments.
   - `molsys_aligned = msm.structure.align_principal_axes(molsys, axes=[[1,0,0], [0,1,0], [0,0,1]])`
   - `axes_aligned, momenta_aligned = msm.structure.get_principal_axes(molsys_aligned)`
   - Loop printing aligned axes.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
