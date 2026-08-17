# Micro-Governance: has_hydrogens.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/has_hydrogens.ipynb` (`msm.build.has_hydrogens`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Has_hydrogens)=`
   - H1 Title `# Has hydrogens`
   - Italic gerund summary `*Checking whether a molecular system or selection contains hydrogen atoms.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing T4 lysozyme `181l.h5msm`.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-17**:
   - `molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - `msm.get(molsys, selection='atom_type=="H"', n_atoms=True)`
   - `msm.build.has_hydrogens(molsys)`
   - `msm.build.has_hydrogens(molsys, selection='molecule_type=="protein"')`
   - `molsys = msm.build.add_missing_terminal_cappings(molsys)`
   - `molsys = msm.build.add_missing_heavy_atoms(molsys)`
   - `molsys = msm.build.add_missing_hydrogens(molsys)`
   - `msm.build.has_hydrogens(molsys)`
   - `msm.build.has_hydrogens(molsys, selection='molecule_type=="protein"')`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.
