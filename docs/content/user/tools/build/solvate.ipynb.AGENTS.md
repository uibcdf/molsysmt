# Micro-Governance: solvate.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/solvate.ipynb` (`msm.build.solvate`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys` (`molsys_cub`, `molsys_oct`).

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
   - Opening sentence introducing PDB structure `1VII`.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-25**:
   - `molsys = msm.convert('pdb_id:1vii', to_form='molsysmt.MolSys')`
   - `msm.info(molsys)`
   - `msm.build.is_solvated(molsys)`
   - `molsys_cub = msm.build.solvate(molsys, box_shape='cubic', clearance='14.0 angstroms')`
   - `msm.build.is_solvated(molsys_cub)`
   - `msm.info(molsys_cub)`
   - `box, box_angles, box_shape = msm.get(molsys_cub, element='system', box=True, box_angles=True, box_shape=True)`
   - `molsys_cub = msm.pbc.wrap_to_pbc(molsys_cub, center_of_selection='molecule_type=="peptide"')`
   - MolSysViewer static view 1 tag + `msm.view(molsys_cub)`
   - Header H2 `## Periodic box geometries`
   - `molsys_oct = msm.build.solvate(molsys, box_shape='truncated octahedral', clearance='14.0 angstroms')`
   - `msm.info(molsys_oct)`
   - `molsys_oct = msm.pbc.wrap_to_pbc(molsys_oct, center_of_selection='molecule_type=="peptide"')`
   - MolSysViewer static view 2 tag + `msm.view(molsys_oct)`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.
