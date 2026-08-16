# Micro-Governance: iterator.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/basic/iterator.ipynb` (`msm.basic.Iterator`).

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Iterator)=`
   - H1 Title `# Iterator`
   - Italic summary `*Iterating over topological and structural attributes of a molecular system.*`
   - Narrative intro paragraph explaining attribute iteration with `start`, `stop`, `step`, `chunk`.
   - Collapsible `{hint}` dropdown linked to `{ref}`Introduction_Attributes`.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing `chicken villin HP35` and `pentalanine`.
4. **Cells 4+**: Practical examples demonstrating topological and structural iteration over atoms, groups, structures, trajectories, and chunked execution.
5. **Collapsible Demo Systems Note**: Right after the first code cell using `msm.systems`.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance.
