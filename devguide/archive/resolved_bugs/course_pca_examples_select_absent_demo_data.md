---
summary: Course PCA examples select absent demo data.
issue: uibcdf/molsysmt#449
status: resolved
opened: 2026-10-24
closed: 2026-10-24
severity: low
verification: reproduced
area: [docs, structure]
guard: devtools/tests/test_course_pca_examples.py
normative: docs/content/course/Path_Biophysics/35_Principal_Components.ipynb
blocked_by: []
supersedes: []
---

# Course PCA examples select absent demo data

**Reported:** 2026-10-24 while verifying PCA documentation for uibcdf/molsysmt#448.
**Initial status:** active; limited repair of module-35 demonstration inputs.

## What

Forced execution of Path Alzheimer and Enzyme module 35 selects zero atoms with
`molecule_type=="protein"` on the bundled HP35 system: its 605 peptide atoms
are classified as `peptide`. Their principal-axes calls reject the empty set.
Path Biophysics names an absent `popc_membrane.h5msm` key and alpha carbons
in a lipid membrane. The registered topology is `popc_membrane.psf`; its CA
selection is empty and it contains 294 phosphorus sites.

## How

Run `python docs/execute_notebooks.py -q -f` on the affected module-35 notebooks.
After correcting selection, Alzheimer also attempts a file-to-same-file copy
when its final alignment acts directly on the composite disk-backed input.
Native conversion before molecular operations prevents that sample misuse.

## Why

These are executable scientific lessons. A false demo key, empty population or
file-copy failure prevents readers from reaching the intended PCA interpretation.
The scientific API should retain its explicit input validation.

## Repair and guard

Alzheimer/Enzyme include protein and peptide molecule classifications and load
the composite ensemble as a native MolSys. Biophysics uses the registered PSF/DCD
pair and eight real phosphorus sites across three selected observations, bounding
dense covariance work. The narrative distinguishes this coordinate-dispersion
example from a properly prepared biological gating analysis. All original lesson
topics remain; no placeholder coordinates replace a failing molecular input.

`devtools/tests/test_course_pca_examples.py` executes the actual code cells of all
four paths against bundled data. It fails if an invalid source or empty scientific
selection returns, including later operations in each lesson. The first receiving
run passes three paths and fails Alzheimer on its final disk-backed transformation;
the final repair passes **4 tests in 62.90 seconds**, pytest-receptor, 12 workers.
The 67 warnings are retained legacy-H5MSM and off-axis structure-attribute warnings
from the bundled composite samples. This guard does not certify a full scientific
membrane/gating protocol or remove broader course editorial debt.


## Closing qualification — 2026-10-24

The toolbox PCA notebook and all four path module-35 notebooks pass fresh Jupyter
execution. The weighted Cookbook Python blocks and the public docstring doctest
pass. The complete HTML documentation builds successfully; pre-existing MyST
heading/admonition warnings remain part of uibcdf/molsysmt#144. Ruff lint/format,
scientific-evidence validation and all fourteen fast release checks pass. Hosted
exact-source gates and the publication commit are recorded at issue closure.
No release, package publication or installed-pair qualification is implied.

Reproduce the executable course guard with:

```bash
python -m pytest devtools/tests/test_course_pca_examples.py --receptor=llm -n 12
```
