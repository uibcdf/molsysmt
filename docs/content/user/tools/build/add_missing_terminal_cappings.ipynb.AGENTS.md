# Micro-Governance: add_missing_terminal_cappings.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/add_missing_terminal_cappings.ipynb` (`msm.build.add_missing_terminal_cappings`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys` (`molsys_charged`, `molsys_uncharged`).

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Add_missing_terminal_cappings)=`
   - H1 Title `# Add missing terminal cappings`
   - Italic gerund summary `*Adding terminal cappings to peptides and proteins.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing tripeptide (`AlaValPro`).
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-15**:
   - `molsys = msm.build.build_peptide('AlaValPro', to_form='molsysmt.MolSys')`
   - `msm.info(molsys, element='group')`
   - `molsys_charged = msm.build.add_missing_terminal_cappings(molsys, N_terminal=None, C_terminal=None)`
   - `msm.info(molsys_charged, element='group')`
   - `msm.physchem.get_charge(molsys_charged, element='group')`
   - `molsys_uncharged = msm.build.add_missing_terminal_cappings(molsys, N_terminal='ACE', C_terminal='NME')`
   - `msm.info(molsys_uncharged, element='group')`
   - `msm.physchem.get_charge(molsys_uncharged, element='group')`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance.
