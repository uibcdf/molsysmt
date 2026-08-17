# Micro-Governance: get_disulfide_bonds.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/get_disulfide_bonds.ipynb` (`msm.build.get_disulfide_bonds`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_disulfide_bonds)=`
   - H1 Title `# Get disulfide bonds`
   - Italic gerund summary `*Identifying disulfide bridges between sulfur atoms in protein structures.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing PDB structure `5XJH`.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-14**:
   - `molsys = msm.convert('5XJH')`
   - `msm.build.get_disulfide_bonds(molsys)`
   - `msm.element.bond.max_expected_bond_length['protein']['S']['S']`
   - `msm.get(molsys, element='atom', selection='atom_type=="S"', n_atoms=True)`
   - `msm.structure.get_neighbors(molsys, selection='atom_type=="S"', n_neighbors=1, output_type='pairs', mutual_only=True, output_indices='atom')`
   - `msm.build.get_disulfide_bonds(molsys, max_bond_length='2.15 angstroms')`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.
