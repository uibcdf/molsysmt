# Micro-Governance: solvate.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/solvate.ipynb` (`msm.build.solvate`).

## Variable Naming Invariant
The canonical variable representing the input molecular system MUST be `molsys`, and solvated variants MUST be `molsys_cub`, `molsys_ions`, `molsys_oct`, and `molsys_rhomb`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Solvate)=`
   - H1 Title `# Solvate`
   - Italic gerund summary `*Adding solvent molecules and ions to solvate a molecular system.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing PDB 1VII dataset.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `import numpy as np`
5. **Cells 5+**:
   - `molsys = msm.convert('pdb_id:1vii', to_form='molsysmt.MolSys')`
   - The narrative must state that `solvate()` requires exactly one structure and must
     point ensemble and trajectory users to `structure_indices`.
   - `molsys_cub = msm.build.solvate(molsys, box_shape='cubic', clearance='14.0 angstroms')`
   - Box inspection and MolSysViewer 3D view with static HTML view `tools_build_solvate_1.html`.
   - Header H2 `## Adding physiological ions`
   - `molsys_ions = msm.build.solvate(molsys, box_shape='cubic', clearance='14.0 angstroms', ionic_strength='150.0 millimolar')`
   - Header H2 `## Box shape`
   - Comparing water count and solvent savings across `'cubic'`, `'truncated octahedral'`, and `'rhombic dodecahedral'` geometries.
   - MolSysViewer 3D view with static HTML view `tools_build_solvate_2.html`.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
