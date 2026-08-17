# Micro-Governance: get_rmsd.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/get_rmsd.ipynb` (`msm.structure.get_rmsd`).

## Variable Naming Invariant
The canonical variable representing the input molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_rmsd)=`
   - H1 Title `# Get RMSD`
   - Italic gerund summary `*Calculating the root-mean-square deviation without prior spatial superposition.*`
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
   - `rmsd_raw = msm.structure.get_rmsd(molsys, selection='backbone', reference_structure_index=0)`
   - Header H2 `## Plotting RMSD time series`
   - Matplotlib time series plot of raw RMSD.
   - Header H2 `## Comparing unaligned RMSD against optimal least-RMSD`
   - Dual plot comparing raw RMSD vs `get_least_rmsd`.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
