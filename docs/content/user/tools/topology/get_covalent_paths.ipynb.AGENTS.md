# Micro-Governance: get_covalent_paths.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/topology/get_covalent_paths.ipynb` (`msm.topology.get_covalent_paths`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_covalent_paths)=`
   - H1 Title `# Get covalent paths`
   - Italic gerund summary `*Finding paths of covalently bonded atoms matching specified element patterns.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing TcTIM `1tcd.h5msm`.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-16**:
   - `molsys = msm.convert(msm.systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - `msm.info(molsys)`
   - `covalent_paths = msm.topology.get_covalent_paths(molsys, path=['atom_name=="C"', 'atom_name=="N"', 'atom_name=="CA"'])`
   - `covalent_paths.shape`
   - `msm.get(molsys, element='atom', selection=covalent_paths[0], name=True)`
   - Header H2 `## Using multi-name atom selections`
   - `covalent_paths = msm.topology.get_covalent_paths(molsys, path=['atom_name==["C", "N"]', 'atom_name=="CA"', 'atom_name=="C"'])`
   - `msm.get(molsys, element='atom', selection=covalent_paths[0], name=True)`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.
