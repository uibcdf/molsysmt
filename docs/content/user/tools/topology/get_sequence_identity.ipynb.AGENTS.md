# Micro-Governance: get_sequence_identity.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/topology/get_sequence_identity.ipynb` (`msm.topology.get_sequence_identity`).

## Variable Naming Invariant
The canonical variables representing the molecular systems MUST be `molsys_1` and `molsys_2`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_sequence_identity)=`
   - H1 Title `# Get sequence identity`
   - Italic gerund summary `*Computing the sequence identity percentage and matching residue index mappings between molecular systems.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing T4 lysozyme variants `181L` and `1L17`.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-9**:
   - `molsys_1 = msm.convert('pdb_id:181l', to_form='molsysmt.MolSys')`
   - `molsys_2 = msm.convert('pdb_id:1l17', to_form='molsysmt.MolSys')`
   - `identity, intersection, ref_intersection = msm.topology.get_sequence_identity(molsys_1, selection='molecule_type=="protein"', reference_molecular_system=molsys_2, reference_selection='molecule_type=="protein"')`
   - `identity`
   - `print(intersection)`
   - `print(ref_intersection)`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.
