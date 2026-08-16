# Micro-Governance: view.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/basic/view.ipynb` (`msm.basic.view`).

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_View)=`
   - H1 Title `# View`
   - Italic summary `*Visualizing a molecular system.*`
   - Narrative intro paragraph explaining visualization engines with MolSysViewer as default.
   - Collapsible `{hint}` dropdown linked to `{ref}`Introduction_Viewers`.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing `181L` with MolSysViewer as default.
4. **Cell 4 (Code)**:
   - `import molsysmt as msm`
5. **Cells 5-14**: MolSysViewer default view calls with pre-generated static 3D HTML view assets (`tools_basic_view_1.html`, `tools_basic_view_2.html`, `tools_basic_view_3.html`).
6. **Section 2 (`## Working with NGLView`)**: Demonstrating optional NGLView integration (`viewer='NGLView'`) and passing `nglview.NGLWidget` form objects into MolSysMT tools.
7. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance.
