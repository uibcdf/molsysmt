# Micro-Governance: remove.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/basic/remove.ipynb` (`msm.basic.remove`).

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Remove)=`
   - H1 Title `# Remove`
   - Italic summary `*Removing atoms or structures from a molecular system.*`
   - Narrative intro paragraph explaining atom and structure removal.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing `181L`.
4. **Cell 4 (Code)**:
   - `import molsysmt as msm`
5. **Cells 5+**: Practical examples demonstrating atom removal via `selection` and structure removal via `structure_indices`.
6. **Collapsible Demo Systems Note**: Right after the code cell using `msm.systems`.
7. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance.
