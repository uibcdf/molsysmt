# Micro-Governance: get_sequence_alignment.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/topology/get_sequence_alignment.ipynb` (`msm.topology.get_sequence_alignment`).

## Variable Naming Invariant
The canonical variables representing the molecular systems MUST be `molsys_1` and `molsys_2`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_sequence_alignment)=`
   - H1 Title `# Get sequence alignment`
   - Italic gerund summary `*Computing the amino acid or nucleotide sequence alignment between molecular systems.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing T4 lysozyme variants `181L` and `1L17`.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-11**:
   - `molsys_1 = msm.convert('pdb_id:181l', to_form='molsysmt.MolSys')`
   - `molsys_2 = msm.convert('pdb_id:1l17', to_form='molsysmt.MolSys')`
   - `msm.get(molsys_1, element='atom', selection='molecule_type=="protein"', n_groups=True)`
   - `msm.get(molsys_2, element='atom', selection='molecule_type=="protein"', n_groups=True)`
   - `msm.topology.get_sequence_alignment(molsys_1, selection='molecule_type=="protein"', reference_molecular_system=molsys_2, reference_selection='molecule_type=="protein"', prettyprint=True)`
   - `seq, seq_ref = msm.topology.get_sequence_alignment(molsys_1, selection='molecule_type=="protein"', reference_molecular_system=molsys_2, reference_selection='molecule_type=="protein"')`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.
