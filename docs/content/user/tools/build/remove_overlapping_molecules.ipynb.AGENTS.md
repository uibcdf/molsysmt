# Micro-Governance: remove_overlapping_molecules.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/remove_overlapping_molecules.ipynb` (`msm.build.remove_overlapping_molecules`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys` (`new_molsys`).

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Remove_overlapping_molecules)=`
   - H1 Title `# Remove overlapping molecules`
   - Italic gerund summary `*Removing solvent or ligand molecules that overlap with solute atoms.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing merged water box and peptide.
4. **Cell 4 (Code)**: `import molsysmt as msm; import numpy as np`
5. **Cells 5-9**:
   - `box = np.array([[[3.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, 0.0, 3.0]]]) * msm.pyunitwizard.unit('nm')`
   - `water_box = msm.build.make_water_box(box)`
   - `peptide = msm.build.build_peptide('ACEALAALANME')`
   - `molsys = msm.merge([water_box, peptide])`
   - `msm.info(molsys)`
   - `new_molsys = msm.build.remove_overlapping_molecules(molsys, selection='molecule_type=="water"', selection_2='molecule_type=="protein"')`
   - `msm.get(new_molsys, n_waters=True)`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.
