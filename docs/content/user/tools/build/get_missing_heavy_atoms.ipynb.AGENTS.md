# Micro-Governance: get_missing_heavy_atoms.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/get_missing_heavy_atoms.ipynb` (`msm.build.get_missing_heavy_atoms`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_missing_heavy_atoms)=`
   - H1 Title `# Get missing heavy atoms`
   - Italic gerund summary `*Identifying missing non-hydrogen heavy atoms in a molecular system.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing PDB structure `1BRS`.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-13**:
   - `molsys = msm.convert('1BRS', selection='molecule_type=="protein"')`
   - `msm.info(molsys, element='molecule')`
   - `missing_heavy_atoms = msm.build.get_missing_heavy_atoms(molsys)`
   - `missing_heavy_atoms`
   - `residue_indices = list(missing_heavy_atoms.keys())`
   - `molecule_indices = msm.get(molsys, element='molecule', selection='group_index in @residue_indices', molecule_index=True)`
   - `msm.info(molsys, element='molecule', selection='molecule_index in @molecule_indices')`
   - `msm.build.has_hydrogens(molsys)`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.
