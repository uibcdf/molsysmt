# Micro-Governance: merge.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/basic/merge.ipynb` (`msm.basic.merge`).

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Merge)=`
   - H1 Title `# Merge`
   - Italic summary `*Merging elements from multiple molecular systems.*`
   - Narrative intro paragraph explaining system merging.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing the three peptides (`AceProNme`, `AceValNme`, `AceLysNme`).
4. **Cell 4 (Code)**:
   - `import molsysmt as msm`
5. **Cells 5+**: Practical examples demonstrating peptide construction, spatial translation, merging into system $D$, summary table inspection, and 3D visualization.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order of first appearance.
