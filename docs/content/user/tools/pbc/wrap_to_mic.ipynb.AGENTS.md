# Micro-Governance: wrap_to_mic.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/pbc/wrap_to_mic.ipynb` (`msm.pbc.wrap_to_mic`).

## Variable Naming Invariant
The canonical variable representing the molecular system is `molsys` and wrapped system `molsys_mic`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Wrap_to_mic)=`
   - H1 Title `# Wrap to MIC`
   - Italic gerund summary `*Wrapping atomic coordinates into the Minimum Image Convention (MIC) box.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing Met-enkephalin solvated dataset.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5+**:
   - `molsys = msm.convert(msm.systems['Met-enkephalin']['met_enkephalin.h5msm'])`
   - `molsys_solvated = msm.build.solvate(...)`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - `molsys_mic = msm.pbc.wrap_to_mic(molsys_solvated, center_of_selection='molecule_type=="peptide"', keep_covalent_bonds=True)`.
   - 3D MolSysViewer interactive visualization with `molsysviewer_htmlfile = '_static/views/tools_pbc_wrap_to_mic_1.html'` and `msm.view(molsys_mic)`.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
