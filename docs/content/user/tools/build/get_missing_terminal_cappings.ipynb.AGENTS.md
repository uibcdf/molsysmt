# Micro-Governance: get_missing_terminal_cappings.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/get_missing_terminal_cappings.ipynb` (`msm.build.get_missing_terminal_cappings`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_missing_terminal_cappings)=`
   - H1 Title `# Get missing terminal cappings`
   - Italic gerund summary `*Identifying missing terminal cappings in peptides and proteins.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing PDB structure `1BRS`.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-9**:
   - `molsys = msm.convert(msm.systems["Barnase-Barstar"]["1brs.bcif.gz"], selection='molecule_type=="protein"')`
   - `missing_caps = msm.build.get_missing_terminal_cappings(molsys)`
   - `missing_caps`
   - `msm.select(molsys, selection='atom_name=="OXT"')`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.

## Scientific coverage correction under #686

Use the frozen bundled 1BRS source instead of a network lookup. Preserve the public
missing-OXT query and add the explicit peptide-termini coverage report after its
dictionary display. The two interrupted chains stay unassessed, with a visible
warning even though the legacy opening cell suppresses runtime warnings. Never
restore group-ID sorting or claim that an empty partial dictionary proves complete
chemistry. Re-execute the affected tutorial when its scientific output changes.
