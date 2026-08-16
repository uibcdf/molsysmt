# Micro-Governance: get.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/basic/get.ipynb` (`msm.basic.get`).

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get)=`
   - H1 Title `# Get`
   - Italic summary `*Retrieving attribute values from a molecular system.*`
   - Narrative intro explaining attribute retrieval across forms.
   - Collapsible `{hint}` dropdown linked to `{ref}`Introduction_Molecular_Systems`.
   - References to `{ref}`Introduction_Attributes` and `{ref}`Introduction_Forms`.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing `1TCD`.
4. **Cell 4 (Code)**:
   - `import molsysmt as msm`
5. **Cells 5+**: Practical usage examples for topological and structural attributes across atoms, groups, components, molecules, chains, entities, bonds, and system.
6. **Collapsible Demo Systems Note**: Right after the code cell using `msm.systems`.
7. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance.
