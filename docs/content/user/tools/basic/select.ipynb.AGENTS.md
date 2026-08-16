# Micro-Governance: select.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/basic/select.ipynb` (`msm.basic.select`).

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Select)=`
   - H1 Title `# Select`
   - Italic summary `*Selecting elements of a molecular system using selection syntax.*`
   - Narrative intro paragraph explaining query syntax and selection engine.
   - Collapsible `{hint}` dropdown linked to `{ref}`user-foundations-support-selection-syntaxes`.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cells 3-9 (Markdown - Selection Syntax Reference Tables)**:
   - Tables listing keywords, operators, distances, and shortcuts.
4. **Cell 10 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing `1TCD`.
5. **Cell 11 (Code)**:
   - `import molsysmt as msm`
6. **Cells 12+**: Executable selection examples across atom/group/molecule/chain levels, external variables (`@var`), spatial distances (`within ... of`), bonding relationships (`bonded to`), hierarchical queries (`in elements of`), and syntax translations (`MDTraj`, `NGLView`).
7. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance.
