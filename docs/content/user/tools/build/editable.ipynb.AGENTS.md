# Micro-Governance: editable.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/editable.ipynb` (`msm.build.editable`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`, the builder MUST be `builder`, and the materialized system MUST be `new_molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Editable)=`
   - H1 Title `# Editable`
   - Italic gerund summary `*Creating an editable molecular system builder to modify or construct topologies.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing Met-enkephalin `met_enkephalin.h5msm`.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-18**:
   - `molsys = msm.convert(msm.systems['Met-enkephalin']['met_enkephalin.h5msm'])`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - `builder = msm.build.editable(molsys)`
   - `type(builder)`
   - Header H2 `## Modifying topology and bonds`
   - `builder.add_bond(0, 10, bond_order=1)`
   - `builder.assign_groups_to_new_chain(group_indices=[0, 1], chain_name='B')`
   - Header H2 `## Materializing the final molecular system`
   - `new_molsys = builder.build()`
   - `msm.info(new_molsys, element='chain')`
   - Header H2 `## Creating a builder from scratch`
   - `empty_builder = msm.build.editable()`
   - `type(empty_builder)`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.
