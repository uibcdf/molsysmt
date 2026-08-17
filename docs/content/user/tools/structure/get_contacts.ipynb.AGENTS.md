# Micro-Governance: get_contacts.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/get_contacts.ipynb` (`msm.structure.get_contacts`).

## Variable Naming Invariant
The canonical variable representing the input molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_contacts)=`
   - H1 Title `# Get contacts`
   - Italic gerund summary `*Computing contact maps and inter-atomic contact matrices.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing TcTIM dataset.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `import numpy as np`
5. **Cells 5+**:
   - `molsys = msm.convert(msm.systems['TcTIM']['1tcd.h5msm'])`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - `ca_atoms = msm.select(molsys, selection='atom_name=="CA"')`
   - `contact_map = msm.structure.get_contacts(molsys, selection=ca_atoms, threshold='1.2 nm')`
   - `contact_map.shape`
   - `print(f'Total contacts: {np.sum(contact_map)}')`
   - Header H2 `## Inter-chain contact map`
   - `ca_chain_0 = msm.select(molsys, selection='atom_name=="CA" and chain_index==0')`
   - `ca_chain_1 = msm.select(molsys, selection='atom_name=="CA" and chain_index==1')`
   - `interchain_contacts = msm.structure.get_contacts(molsys, selection=ca_chain_0, selection_2=ca_chain_1, threshold='1.0 nm')`
   - `interchain_contacts.shape`
   - `print(f'Inter-chain contacts: {np.sum(interchain_contacts)}')`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
