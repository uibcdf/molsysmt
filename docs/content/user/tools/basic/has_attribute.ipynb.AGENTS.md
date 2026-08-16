# Micro-Governance: has_attribute.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/basic/has_attribute.ipynb` (`msm.basic.has_attribute`).

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Has_attribute)=`
   - H1 Title `# Has attribute`
   - Italic summary `*Checking whether a molecular system has a specific attribute.*`
   - Narrative intro paragraph explaining attribute availability checking.
   - Collapsible `{hint}` dropdown linked to `{ref}`Introduction_Attributes`.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing `pentalanine.inpcrd`.
4. **Cell 4 (Code)**:
   - `import molsysmt as msm`
5. **Cells 5+**: Practical examples checking attribute presence on system instances and form declarations.
6. **Collapsible Demo Systems Note**: Right after the code cell using `msm.systems`.
7. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance.
