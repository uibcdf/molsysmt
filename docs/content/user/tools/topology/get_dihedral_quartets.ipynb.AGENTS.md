# Micro-Governance: get_dihedral_quartets.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/topology/get_dihedral_quartets.ipynb` (`msm.topology.get_dihedral_quartets`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_dihedral_quartets)=`
   - H1 Title `# Get dihedral quartets`
   - Italic gerund summary `*Getting the quartets of atoms defining specific dihedral angles in a molecular system.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing TcTIM `1tcd.h5msm`.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-26**:
   - `molsys = msm.convert(msm.systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - `phi_chains = msm.topology.get_dihedral_quartets(molsys, phi=True)`
   - `psi_chains = msm.topology.get_dihedral_quartets(molsys, selection='10<=group_index<=15', psi=True)`
   - `chi5_chains = msm.topology.get_dihedral_quartets(molsys, chi5=True)`
   - `phi, psi = msm.topology.get_dihedral_quartets(molsys, phi=True, psi=True)`
   - Header H2 `## Summary of dihedral angle definitions`
   - Header H2 `## Extracting atom blocks attached to dihedral quartets`
   - `phi_chains, phi_blocks = msm.topology.get_dihedral_quartets(molsys, with_blocks=True, phi=True)`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.
