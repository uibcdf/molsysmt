# Micro-Governance: get_secondary_structure.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/get_secondary_structure.ipynb` (`msm.structure.get_secondary_structure`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_secondary_structure)=`
   - H1 Title `# Get secondary structure`
   - Italic gerund summary `*Assigning secondary structure elements to amino acid residues across molecular structures.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing TcTIM `1tcd.h5msm`.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5+**:
   - `molsys = msm.convert(msm.systems['TcTIM']['1tcd.h5msm'])`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - `ss = msm.structure.get_secondary_structure(molsys, simplified=True)`
   - `ss.shape`
   - `ss[0, :20]`
   - Header H2 `## Full 8-state DSSP assignment`
   - `ss_full = msm.structure.get_secondary_structure(molsys, simplified=False)`
   - `ss_full[0, :20]`
   - Header H2 `## Restricting to a specific residue selection`
   - `msm.structure.get_secondary_structure(molsys, selection='10<=group_index<=20')`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
