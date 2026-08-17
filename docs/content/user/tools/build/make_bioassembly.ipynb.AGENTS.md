# Micro-Governance: make_bioassembly.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/make_bioassembly.ipynb` (`msm.build.make_bioassembly`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys` (`assembled_molsys`).

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Make_bioassembly)=`
   - H1 Title `# Make bioassembly`
   - Italic gerund summary `*Constructing biological assemblies using symmetry transformations from PDB records.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing PDB structure `1OUT`.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-19**:
   - `molsys = msm.convert('1OUT')`
   - MolSysViewer static view 1 tag + `msm.view(molsys)`
   - `molsys = msm.build.make_bioassembly(molsys, bioassembly='1')`
   - MolSysViewer static view 2 tag + `msm.view(molsys)`
   - `molsys = msm.convert('2BUK')`
   - MolSysViewer static view 3 tag + `msm.view(molsys)`
   - `assembled_molsys = msm.build.make_bioassembly(molsys, bioassembly='1')`
   - `msm.info(assembled_molsys)`
   - MolSysViewer static view 4 tag + `msm.view(assembled_molsys)`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.
