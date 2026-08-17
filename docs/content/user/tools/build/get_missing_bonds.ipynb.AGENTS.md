# Micro-Governance: get_missing_bonds.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/get_missing_bonds.ipynb` (`msm.build.get_missing_bonds`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_missing_bonds)=`
   - H1 Title `# Get missing bonds`
   - Italic gerund summary `*Identifying missing covalent bonds in a molecular system.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing peptide building (`AceAlaNme`).
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-10**:
   - `molsys = msm.build.build_peptide('AceAlaNme')`
   - `msm.get(molsys, element='bond', selection=[0, 1, 2], bonded_atoms=True)`
   - `molsys.topology.remove_bonds([0])`
   - `msm.build.get_missing_bonds(molsys)`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.
