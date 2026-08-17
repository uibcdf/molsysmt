# Micro-Governance: solve_atoms_with_alternate_locations.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/solve_atoms_with_alternate_locations.ipynb` (`msm.build.solve_atoms_with_alternate_locations`).

## Variable Naming Invariant
The canonical variable representing the input molecular system MUST be `molsys`, and occupancy variant MUST be `molsys_occ`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Solve_atoms_with_alternate_locations)=`
   - H1 Title `# Solve atoms with alternate locations`
   - Italic gerund summary `*Resolving alternate crystallographic atom locations in a molecular system.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing PDB 1BNF dataset.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `from importlib.resources import files`
5. **Cells 5+**:
   - Loading 1BNF.
   - Inspecting atom 480 alternate location.
   - Solving to location 'B'.
   - Header H2 `## Resolving by maximum occupancy`
   - Solving with `location_id='occupancy'`.
   - Non-collapsible `{warning}` on alternate location metadata preservation.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
