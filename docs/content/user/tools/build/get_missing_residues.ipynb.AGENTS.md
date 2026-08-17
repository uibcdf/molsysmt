# Micro-Governance: get_missing_residues.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/get_missing_residues.ipynb` (`msm.build.get_missing_residues`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_missing_residues)=`
   - H1 Title `# Get missing residues`
   - Italic gerund summary `*Identifying missing amino acid or nucleotide residues in a molecular system.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing PDB structure `1BRS`.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-8**:
   - `molsys = msm.convert('1BRS', to_form='mmcif_PdbxContainers_DataContainer')`
   - `missing_residues = msm.build.get_missing_residues(molsys)`
   - `missing_residues`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.
