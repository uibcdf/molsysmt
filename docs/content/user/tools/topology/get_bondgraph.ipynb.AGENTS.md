# Micro-Governance: get_bondgraph.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/topology/get_bondgraph.ipynb` (`msm.topology.get_bondgraph`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_bondgraph)=`
   - H1 Title `# Get bondgraph`
   - Italic gerund summary `*Extracting the covalent bond graph of a molecular system.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing TcTIM `1tcd.h5msm`.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-15**:
   - `molsys = msm.convert(msm.systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - `graph = msm.topology.get_bondgraph(molsys, selection='molecule_index==0', to_form="networkx.Graph")`
   - `n_nodes = graph.number_of_nodes(); n_edges = graph.number_of_edges()`
   - `n_atoms, n_bonds = msm.get(molsys, element='atom', selection='molecule_index==0', n_atoms=True, n_inner_bonds=True)`
   - `from networkx import connected_components`
   - `components = connected_components(graph)`
   - `msm.get(molsys, element='atom', selection='molecule_index==0', n_components=True)`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.
