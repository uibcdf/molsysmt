# Micro-Governance: move_away.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/structure/move_away.ipynb` (`msm.structure.move_away`).

## Variable Naming Invariant
The canonical variables representing the reference and mobile systems MUST be `molsys_A` and `molsys_B`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Move_away)=`
   - H1 Title `# Move away`
   - Italic gerund summary `*Translating a molecular selection away from a reference center by a fixed distance.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing alanine dipeptide dataset.
4. **Cell 4 (Code)**: `import molsysmt as msm`, `import numpy as np`, `import pyunitwizard as puw`
5. **Cells 5+**:
   - `molsys_A = msm.convert(msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'])`
   - `molsys_B = msm.convert(msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'])`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - `molsys_B_moved = msm.structure.move_away(molsys_B, reference_molecular_system=molsys_A, distance='2.0 nm', direction=[1.0, 0.0, 0.0])`
   - Header H2 `## Directional displacement along arbitrary 3D vectors`
   - Translation along diagonal direction vector.
   - Header H2 `## Quantitative verification of spatial separation`
   - Euclidean distance confirmation printout.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools in strict chronological order with explicit titles `{ref}`Title <AnchorLabel>``.
