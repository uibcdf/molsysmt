# Micro-Governance: add_bonds.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/add_bonds.ipynb` (`msm.build.add_bonds`).

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Add_bonds)=`
   - H1 Title `# Add bonds`
   - Italic gerund summary `*Adding covalent bonds between specified atom pairs in a molecular system.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing alanine dipeptide system.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cell 5 (Code)**: `molsys = msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']` & `msm.convert(molsys)`
6. **Collapsible Demo Systems Note**: Right after code cell loading `msm.systems`.
7. **Cells 7-16**:
   - `msm.build.remove_bonds(molsys)`
   - `msm.get(molsys, n_bonds=True)`
   - `msm.build.add_bonds(molsys, bonded_atom_pairs=[[0, 1], [0, 2], [1, 4]])`
   - `msm.get(molsys, n_bonds=True)` and `msm.get(molsys, bonded_atom_pairs=True)`
8. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance.
