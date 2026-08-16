# Micro-Governance: where_is_attribute.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/basic/where_is_attribute.ipynb` (`msm.basic.where_is_attribute`).

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Where_is_attribute)=`
   - H1 Title `# Where is attribute`
   - Italic summary `*Identifying the item holding a specific attribute in a molecular system.*`
   - Narrative intro paragraph explaining attribute location in composite systems.
   - Collapsible `{hint}` dropdown linked to `{ref}`Introduction_Attributes`.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing `pentalanine` composite files (`.prmtop` and `.inpcrd`).
4. **Cell 4 (Code)**:
   - `import molsysmt as msm`
5. **Cell 5 (Code)**:
   - `structure = msm.systems['pentalanine']['pentalanine.inpcrd']`
   - `topology = msm.systems['pentalanine']['pentalanine.prmtop']`
6. **Collapsible Demo Systems Note**: Right after the code cell loading `msm.systems`.
7. **Cells 7+**: Executable queries demonstrating `msm.where_is_attribute([topology, structure], attribute='box')` and `msm.where_is_attribute([topology, structure], attribute='group_name')`.
8. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance.
