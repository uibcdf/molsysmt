# Micro-Governance: is_solvated.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/build/is_solvated.ipynb` (`msm.build.is_solvated`).

## Variable Naming Invariant
The canonical variable representing the molecular system MUST be `molsys`.

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Is_solvated)=`
   - H1 Title `# Is solvated`
   - Italic gerund summary `*Checking a water-density solvation criterion per structure.*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing Met-enkephalin `met_enkephalin.h5msm`.
4. **Cell 4 (Code)**: `import molsysmt as msm`
5. **Cells 5-15**:
   - `molsys = msm.convert(msm.systems['Met-enkephalin']['met_enkephalin.h5msm'], to_form='molsysmt.MolSys')`
   - Collapsible `{note}` dropdown for Demo Systems Catalog.
   - `molsys = msm.build.add_missing_terminal_cappings(molsys)`
   - `molsys = msm.build.add_missing_hydrogens(molsys)`
   - `msm.build.is_solvated(molsys)`
   - `molsys = msm.build.solvate(molsys, box_shape='cubic', clearance='14.0 angstroms', water_model='TIP3P')`
   - `msm.build.is_solvated(molsys)`
   - `msm.get(molsys, n_waters=True)`
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance, with explicit titles `{ref}`Title <AnchorLabel>``.

## Per-structure predicate contract

Preserve the original preparation example and its source. Retain explicit ensemble
selection, repeated source indices, one-structure bool versus array/empty outputs,
caller-chosen all/any reduction and the synthetic-box warning in the ensemble
example. Explain the strict 15 waters/nm³ criterion, machine-roundoff boundary
tolerance, prerequisite/error distinction and metadata-only computation. Do not
present this predicate as solvent completeness, equilibration or preparation.
