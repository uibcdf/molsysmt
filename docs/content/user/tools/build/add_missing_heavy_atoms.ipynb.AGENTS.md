# Micro-Governance: add_missing_heavy_atoms.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/add_missing_heavy_atoms.ipynb` (`msm.build.add_missing_heavy_atoms`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Add_missing_heavy_atoms)=`
   - H1 Title `# Add missing heavy atoms`
   - Italic gerund summary `*Adding missing non-hydrogen heavy atoms to a molecular system.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing peptide construction (`AceHisThrNme`).
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-16**:
   - `molsys = msm.build.build_peptide('AceHisThrNme')`
   - `msm.info(molsys)`
   - `molsys = msm.remove(molsys, selection='atom_type=="H"')`
   - `msm.build.has_hydrogens(molsys)`
   - `molsys = msm.remove(molsys, selection='atom_name in ["NE2", "CD2", "OG1"]')`
   - `msm.build.get_missing_heavy_atoms(molsys)`
   - `molsys = msm.build.add_missing_heavy_atoms(molsys)`
   - `msm.info(molsys, element='atom')`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance.
