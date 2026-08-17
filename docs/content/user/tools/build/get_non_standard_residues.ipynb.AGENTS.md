# Micro-Governance: get_non_standard_residues.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/get_non_standard_residues.ipynb` (`msm.build.get_non_standard_residues`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_non_standard_residues)=`
   - H1 Title `# Get non standard residues`
   - Italic gerund summary `*Identifying non-standard residues in a molecular system.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing PDB structure `1YRI`.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-7**:
   - `molsys = msm.convert('1YRI')`
   - `msm.build.get_non_standard_residues(molsys)`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.
