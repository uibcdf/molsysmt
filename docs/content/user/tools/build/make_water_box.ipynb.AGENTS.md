# Micro-Governance: make_water_box.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/make_water_box.ipynb` (`msm.build.make_water_box`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Make_water_box)=`
   - H1 Title `# Make water box`
   - Italic gerund summary `*Generating a box of water molecules with specified dimensions.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing numpy box.
4. **Cell 4 (Code)**: `import molsysmt as msm; import numpy as np`
5. **Cells 5-11**:
   - `box = np.array([[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]]) * msm.pyunitwizard.unit('nm')`
   - `molsys = msm.build.make_water_box(box)`
   - `msm.info(molsys)`
   - `coordinates = msm.get(molsys, selection='atom_type=="O"', coordinates=True)`
   - `print(f'Min X: {coordinates[0,:,0].min()} and Max X: {coordinates[0,:,0].max()}')`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.
