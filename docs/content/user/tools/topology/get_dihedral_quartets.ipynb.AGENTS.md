# Micro-Governance: get_dihedral_quartets.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/topology/get_dihedral_quartets.ipynb` (`msm.topology.get_dihedral_quartets`).

## Variable Naming Invariant
The canonical variable representing the input molecular system MUST be `molsys` and the peptide system MUST be `molsys_peptide`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_dihedral_quartets)=`
   - H1 Title `# Get dihedral quartets`
   - Italic gerund summary `*Getting the quartets of atoms defining dihedral angles in a molecular system.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing TcTIM dataset.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5+**:
   - `molsys = msm.convert(msm.systems['TcTIM']['1tcd.h5msm'])`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - Extracting $\phi$ quartets, subset selection, $\chi_5$ sidechain quartets, multiple types dictionary.
   - Header H2 `## Summary of dihedral angle definitions`
   - Markdown summary table of standard definitions.
   - Header H2 `## Extracting atom blocks attached to dihedral quartets`
   - `molsys_peptide = msm.convert(msm.systems['Met-enkephalin']['met_enkephalin.h5msm'])`
   - `phi_chains, phi_blocks = msm.topology.get_dihedral_quartets(molsys_peptide, with_blocks=True, phi=True)`
   - Block atom counts printout.
   - Hidden pre-execution tag cell for `molsysviewer_htmlfile = '_static/views/tools_topology_get_dihedral_quartets_1.html'`.
   - `msm.view(molsys_peptide)`.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
