# Micro-Governance: define_new_chain.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/define_new_chain.ipynb` (`msm.build.define_new_chain`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Define_new_chain)=`
   - H1 Title `# Define new chain`
   - Italic gerund summary `*Defining a new chain by grouping a selection of atoms.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing PDB structure `1TCD`.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-10**:
   - `molsys = msm.convert('1TCD')`
   - `msm.info(molsys, element='chain')`
   - `msm.build.define_new_chain(molsys, selection='molecule_type=="water"', chain_name='C')`
   - `msm.info(molsys, element='chain')`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.
