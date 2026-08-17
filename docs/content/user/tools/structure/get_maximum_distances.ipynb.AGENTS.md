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
   - Italic gerund summary `*Getting the maximum distance between specific groups of elements or systems.*`
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
   - `pairs, max_distances = msm.structure.get_maximum_distances(molsys, selection='group_index==0', selection_2='group_index==4')`
   - `max_distances[:5]`
   - `pairs[:5]`
   - Header H2 `## Maximum molecular dimension (span)`
   - `span_pairs, max_span = msm.structure.get_maximum_distances(molsys, selection='all', selection_2='all', structure_indices=0)`
   - `max_span[0]`
   - `span_pairs[0]`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
