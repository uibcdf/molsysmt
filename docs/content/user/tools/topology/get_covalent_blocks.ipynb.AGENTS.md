# Micro-Governance: get_covalent_blocks.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/topology/get_covalent_blocks.ipynb` (`msm.topology.get_covalent_blocks`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_covalent_blocks)=`
   - H1 Title `# Get covalent blocks`
   - Italic gerund summary `*Determining sets of atoms that remain covalently connected in a molecular system.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing Met-enkephalin `met_enkephalin.h5msm`.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-19**:
   - `molsys = msm.convert(msm.systems['Met-enkephalin']['met_enkephalin.h5msm'])`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - `blocks = msm.topology.get_covalent_blocks(molsys)`
   - `msm.get(molsys, element='atom', selection='atom_name==["C", "N"]', inner_bonded_atom_pairs=True)`
   - `blocks = msm.topology.get_covalent_blocks(molsys, remove_bonds=[[19, 21], [33, 35]])`
   - `blocks = msm.topology.get_covalent_blocks(molsys, remove_bonds=[[19, 21], [33, 35]], output_type='numpy.ndarray')`
   - Header H2 `## Filtering protein covalent blocks`
   - `molsys = msm.convert('1BRS')`
   - `molsys = msm.remove(molsys, selection='molecule_type==["water", "ion", "cosolute"]')`
   - `blocks = msm.topology.get_covalent_blocks(molsys, selection='molecule_type=="protein"')`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.
