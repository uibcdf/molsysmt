# Micro-Governance: is_a_molecular_system.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/basic/is_a_molecular_system.ipynb` (`msm.basic.is_a_molecular_system`).

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Is_a_molecular_system)=`
   - H1 Title `# Is a molecular system`
   - Italic summary `*Verifying whether an object defines a single valid molecular system.*`
   - Narrative intro paragraph explaining single vs combined items validity.
   - Collapsible `{hint}` dropdown linked to `{ref}`Introduction_Forms`.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing `pentalanine`.
4. **Cell 4 (Code)**:
   - `import molsysmt as msm`
5. **Cells 5+**: Practical examples demonstrating valid and invalid item combinations (matching vs mismatched atom counts).
6. **Collapsible Demo Systems Note**: Right after the code cell using `msm.systems`.
7. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance.
