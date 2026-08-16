# Micro-Governance: add_missing_bonds.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/add_missing_bonds.ipynb` (`msm.build.add_missing_bonds`).

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Add_missing_bonds)=`
   - H1 Title `# Add missing bonds`
   - Italic gerund summary `*Inferring and adding missing covalent bonds based on interatomic distances and chemical element types.*`
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
   - `bonded_atom_pairs = msm.get(molsys, bonded_atom_pairs=True)`
   - `molsys.topology.remove_bonds()`
   - `msm.get(molsys, n_bonds=True)`
   - `msm.build.add_missing_bonds(molsys)`
   - `msm.get(molsys, n_bonds=True)`
   - `new_bonded_atom_pairs = msm.get(molsys, bonded_atom_pairs=True)`
   - `new_bonded_atom_pairs == bonded_atom_pairs`
8. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance.
