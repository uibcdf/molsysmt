# Micro-Governance: solve_atoms_with_alternate_locations.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/solve_atoms_with_alternate_locations.ipynb` (`msm.build.solve_atoms_with_alternate_location`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Solve_atoms_with_alternate_locations)=`
   - H1 Title `# Solve atoms with alternate locations`
   - Italic gerund summary `*Resolving alternate atomic coordinate locations in experimental structures.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing bundled PDB file `1bnf.pdb`.
4. **Cell 4 (Code)**: `import molsysmt as msm; from importlib.resources import files`
5. **Cells 5-13**:
   - `pdb_filename = str(files('molsysmt.data.pdb').joinpath('1bnf.pdb'))`
   - `molsys = msm.convert(pdb_filename, to_form='molsysmt.MolSys', get_missing_bonds=False)`
   - `msm.get(molsys, element='atom', selection='atom_index==480', alternate_location=True)`
   - `msm.build.solve_atoms_with_alternate_location(molsys, location_id='B')`
   - `msm.get(molsys, element='atom', selection=480, atom_id=True, coordinates=True)`
   - `msm.build.solve_atoms_with_alternate_location(molsys, selection=[480, 481], location_id=['A', 'B'])`
   - `msm.get(molsys, element='atom', selection=[480, 481], atom_id=True, coordinates=True)`
   - Non-collapsible warning box for alternate location metadata preservation.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.
