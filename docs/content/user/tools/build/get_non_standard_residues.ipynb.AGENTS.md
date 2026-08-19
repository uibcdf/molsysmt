# Micro-Governance: get_non_standard_residues.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/get_non_standard_residues.ipynb` (`msm.build.get_non_standard_residues`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Get_non_standard_residues)=`
   - H1 Title `# Get non standard residues`
   - Italic gerund summary `*Identifying non-standard residues in a molecular system.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing PDB entry `1ATP`, cAMP-dependent protein kinase.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-7**:
   - `from molsysmt import systems` and `molsys = msm.convert(systems['1ATP']['1atp.pdb'])`
   - `msm.build.get_non_standard_residues(molsys)`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.

## Frozen dataset contract

The demonstration system MUST be `1ATP` and MUST be loaded from the bundled demo
systems, not fetched from the PDB.

It was `1YRI` until 2026-08-19, when `uibcdf/molsysmt#164` recorded that `1YRI`
contains no non-standard residues at all, so the call returned `{}` and the page
demonstrated nothing.

Any replacement must satisfy both conditions, and the second is what `1YRI` failed:

- **It ships with MolSysMT.** The page must not depend on a network fetch.
- **It actually contains non-standard residues**, so the returned mapping is
  non-empty and the reader sees the shape of a real answer.

`1ATP` carries `TPO` at residue id 197 and `SEP` at 338, reported as `THR` and `SER`
respectively. If that expected output changes, the narrative in the markdown cell
naming those residues must change with it.
