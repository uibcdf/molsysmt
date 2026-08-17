# Micro-Governance: get_least_rmsd.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/get_least_rmsd.ipynb` (`msm.structure.get_least_rmsd`).

## Variable Naming Invariant
The canonical variable representing the input molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_least_rmsd)=`
   - H1 Title `# Get least RMSD`
   - Italic gerund summary `*Getting the least RMSD of a molecular system from a reference structure after optimal superimposition.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing pentalanine trajectory dataset.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `import numpy as np`, `import matplotlib.pyplot as plt`
5. **Cells 5+**:
   - `molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - `rmsd = msm.structure.get_rmsd(molsys, selection='backbone', reference_structure_index=0)`
   - `lrmsd = msm.structure.get_least_rmsd(molsys, selection='backbone', reference_structure_index=0)`
   - `time = msm.get(molsys, element='system', time=True)`
   - Matplotlib comparison plot of RMSD vs Least RMSD over time.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
