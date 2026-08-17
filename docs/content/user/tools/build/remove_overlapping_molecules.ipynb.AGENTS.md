# Micro-Governance: remove_overlapping_molecules.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/remove_overlapping_molecules.ipynb` (`msm.build.remove_overlapping_molecules`).

## Variable Naming Invariant
The canonical variable representing the input molecular system MUST be `molsys`, and cleaned system MUST be `molsys_clean`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Remove_overlapping_molecules)=`
   - H1 Title `# Remove overlapping molecules`
   - Italic gerund summary `*Removing solvent or ligand molecules that spatially overlap with other components in a molecular system.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing merged water box and peptide.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `import numpy as np`
5. **Cells 5+**:
   - Merging water box and peptide.
   - Removing overlapping waters with `remove_overlapping_molecules`.
   - Header H2 `## Quantitative clash verification`
   - `get_contacts` verification proving `np.any(clashes) == False`.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
