# Micro-Governance: mutate.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/mutate.ipynb` (`msm.build.mutate`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys` (`new_molsys`).

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Mutate)=`
   - H1 Title `# Mutate`
   - Italic gerund summary `*Mutating amino acid or nucleotide residues in a molecular system.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing pentapeptide `TyrGlyGlyPheMet`.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-13**:
   - `molsys = msm.build.build_peptide('TyrGlyGlyPheMet')`
   - `msm.info(molsys, element='group')`
   - `new_molsys = msm.build.mutate(molsys, mutations=["GLY-2-ALA"])`
   - `msm.info(new_molsys, element='group')`
   - `new_molsys = msm.build.mutate(molsys, mutations={1: 'ALA', 2: 'VAL'})`
   - `new_molsys = msm.build.mutate(molsys, mutations={'GLY': 'ALA'})`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.
