# Micro-Governance: set.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/basic/set.ipynb` (`msm.basic.set`).

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Set)=`
   - H1 Title `# Set`
   - Italic summary `*Setting attribute values to a molecular system.*`
   - Narrative intro paragraph explaining attribute modification.
   - Collapsible `{hint}` dropdown linked to `{ref}`Introduction_Attributes`.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing `181L`.
4. **Cell 4 (Code)**:
   - `import molsysmt as msm`
5. **Cells 5+**: Practical examples demonstrating topological group name updates and structural coordinate modifications.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance.
