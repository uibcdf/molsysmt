# Micro-Governance: get_center.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/get_center.ipynb` (`msm.structure.get_center`).

## Variable Naming Invariant
The canonical variable representing the input molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_center)=`
   - H1 Title `# Get center`
   - Italic gerund summary `*Getting the geometric center or center of mass of a molecular system.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing pentalanine trajectory dataset.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `import numpy as np`
5. **Cells 5+**:
   - `molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - `center = msm.structure.get_center(molsys)`
   - `center.shape`
   - `center[0]`
   - Header H2 `## Getting the center of mass`
   - `center_of_mass = msm.structure.get_center(molsys, selection='group_index==0', weights='masses')`
   - `center_of_mass[0]`
   - Header H2 `## Custom weighted center`
   - `ca_atoms = msm.select(molsys, selection='atom_name=="CA"')`
   - `ca_center = msm.structure.get_center(molsys, selection=ca_atoms, weights=weights_ca)`
   - `ca_center[0]`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
