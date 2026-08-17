# Micro-Governance: add_bonds.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/topology/add_bonds.ipynb` (`molsysmt.Topology.add_bonds`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Add_bonds)=`
   - H1 Title `# Add bonds`
   - Italic gerund summary `*Adding covalent bonds between specified atom pairs in a molecular system.*`
   - Narrative intro paragraph explaining function role and cross-referencing `{ref}`Editable <Tutorial_Editable>``.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing alanine dipeptide.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-9**:
   - `molsys = msm.convert(msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'])`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - `molsys.topology.remove_bonds()`
   - `msm.get(molsys, n_bonds=True)`
   - `molsys.topology.add_bonds([[0, 1], [0, 2], [1, 4]])`
   - `msm.get(molsys, n_bonds=True)`
   - `bonded_atom_pairs = msm.get(molsys, bonded_atom_pairs=True)`
   - `bonded_atom_pairs`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
