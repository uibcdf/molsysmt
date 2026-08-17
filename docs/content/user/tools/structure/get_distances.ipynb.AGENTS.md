# Micro-Governance: get_distances.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/get_distances.ipynb` (`msm.structure.get_distances`).

## Variable Naming Invariant
The canonical variable representing the input molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_distances)=`
   - H1 Title `# Get distances`
   - Italic gerund summary `*Getting the distance between specific elements of a molecular system or two different molecular systems.*`
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
   - `distances = msm.structure.get_distances(molsys, selection=0, selection_2=10)`
   - `distances.shape`
   - `distances[0]`
   - Header H2 `## Distances between centers of atom groups`
   - `dist_groups = msm.structure.get_distances(molsys, selection='group_index==0', selection_2='group_index==4', center_of_atoms=True)`
   - `dist_groups[0]`
   - Header H2 `## Pairwise distance matrix`
   - `ca_atoms = msm.select(molsys, selection='atom_name=="CA"')`
   - `ca_dist_matrix = msm.structure.get_distances(molsys, selection=ca_atoms, structure_indices=0)`
   - `ca_dist_matrix.shape`
   - `ca_dist_matrix[0]`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
