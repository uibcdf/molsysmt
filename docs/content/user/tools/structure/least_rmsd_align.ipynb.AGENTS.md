# Micro-Governance: least_rmsd_align.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/least_rmsd_align.ipynb` (`msm.structure.least_rmsd_align`).

## Variable Naming Invariant
The canonical variables representing the reference and mobile systems MUST be `molsys_1` and `molsys_2`, and the aligned output `molsys_2_aligned`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Least_rmsd_align)=`
   - H1 Title `# Least RMSD align`
   - Italic gerund summary `*Aligning structures with different topologies via sequence alignment and least-RMSD fitting.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing T4 lysozyme mutant comparison (181L vs 1L17).
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5+**:
   - `molsys_1 = msm.convert('181l', selection='molecule_type=="protein"')`
   - `molsys_2 = msm.convert('1l17', selection='molecule_type=="protein"')`
   - Sequence length comparison.
   - Header H2 `## Sequence-guided structural superposition`
   - `molsys_2_aligned = msm.structure.least_rmsd_align(molsys_2, reference_molecular_system=molsys_1)`
   - Centers comparison printout.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
