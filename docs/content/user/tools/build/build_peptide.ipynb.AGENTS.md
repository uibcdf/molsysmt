# Micro-Governance: build_peptide.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/build_peptide.ipynb` (`msm.build.build_peptide`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Build_peptide)=`
   - H1 Title `# Build peptide`
   - Italic gerund summary `*Building peptides from amino acid sequence.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing dipeptide construction (`AceAlaNme`).
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-18**:
   - `molsys = msm.build.build_peptide('AceAlaNme')`
   - MolSysViewer static tag cell (`molsysviewer_htmlfile = '_static/views/tools_build_build_peptide_1.html'`) + `msm.view(molsys)`
   - `molsys = msm.build.build_peptide('GRKFRRKFKK')`
   - `molsys = msm.build.add_missing_terminal_cappings(molsys, N_terminal='ACE', C_terminal='NME')`
   - `molsys = msm.structure.center(molsys)`
   - `molsys = msm.build.solvate(molsys, box_shape='truncated octahedral', clearance='14.0 angstroms')`
   - `molsys = msm.pbc.wrap_to_mic(molsys)`
   - MolSysViewer static tag cell (`molsysviewer_htmlfile = '_static/views/tools_build_build_peptide_2.html'`) + `msm.view(molsys)`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance.
