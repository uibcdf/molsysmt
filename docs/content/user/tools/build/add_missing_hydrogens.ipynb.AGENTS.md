# Micro-Governance: add_missing_hydrogens.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/add_missing_hydrogens.ipynb` (`msm.build.add_missing_hydrogens`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Add_missing_hydrogens)=`
   - H1 Title `# Add missing hydrogens`
   - Italic gerund summary `*Adding missing hydrogen atoms to a molecular system.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing T4 lysozyme (`181L`) protein selection.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-12**:
   - `molsys = msm.convert('181L', selection='molecule_type=="protein"')`
   - `msm.info(molsys)`
   - `msm.build.has_hydrogens(molsys)`
   - `molsys = msm.build.add_missing_hydrogens(molsys, pH=7.4)`
   - `msm.get(molsys, element='atom', selection='atom_type=="H"', n_atoms=True)`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance.
