# Micro-Governance: get_bondgraph.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/topology/get_bondgraph.ipynb` (`msm.topology.get_bondgraph`).

## Variable Naming Invariant
The canonical variable representing the input molecular system MUST be `molsys`.

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
   - Opening sentence introducing Met-enkephalin dataset.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `import networkx as nx`, `import matplotlib.pyplot as plt`
5. **Cells 5+**:
   - `molsys = msm.convert(msm.systems['Met-enkephalin']['met_enkephalin.h5msm'])`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - `graph = msm.topology.get_bondgraph(molsys, to_form='networkx.Graph')`
   - Node and edge count printouts.
   - Header H2 `## Visualizing the 2D bond graph`
   - NetworkX 2D graph drawing with atom labels.
   - Header H2 `## Connected components analysis`
   - Connected components count check.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
