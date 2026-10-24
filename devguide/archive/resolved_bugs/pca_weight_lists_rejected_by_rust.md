---
summary: PCA rejects documented weight lists at the Rust boundary.
issue: uibcdf/molsysmt#448
status: resolved
opened: 2026-10-24
closed: 2026-10-24
severity: medium
verification: reproduced
area: [structure, weights, rust]
guard: tests/structure/principal_component_analysis/test_weighted_contract.py
normative: docs/content/user/cookbook/weighting_pca.md
blocked_by: []
supersedes: []
---

# PCA rejects documented weight lists at the Rust boundary

**Reported:** 2026-10-24 while receiving the structural-analysis addon under
uibcdf/molsysmt#421 / uibcdf/molsysviewer#264. Filing explicitly authorized.
**Initial status:** open. The scientific owner supplies normalization and validation;
the addon forwards native arguments and receives supported ndarray routes.

## What

The public PCA docstring accepts NumPy arrays, lists and tuples for weights.
An equivalent numeric list fails at the Rust boundary while a float64 array
succeeds:

```python
import numpy as np
import molsysmt as msm
molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
                     structure_indices=[0, 8, 3])
options = dict(selection=[0, 2], structure_indices=[2, 0, 2], use_gpu=False)
msm.structure.principal_component_analysis(
    molsys, weights=np.array([1., 2.]), **options,
)
msm.structure.principal_component_analysis(molsys, weights=[1., 2.], **options)
# TypeError: 'list' object is not an instance of 'ndarray'
# while processing 'weights'
```

## How

principal_component_analysis.py passes the supplied weights through
_private/rust_backend.py to the PyReadonlyArray1 Rust argument without converting
the documented Python sequence. The generic weights digester admits the list.
The same selected coordinates and a float64 ndarray reach the kernel normally.

## Why

Documented equivalent Python containers should represent the same weighted
covariance. This prevents ordinary expert use of both native PCA and the thin
addon. Correct it in the scientific owner, not through an addon-only conversion.

## What is measured and what is assumed

The list failure is reproduced without Viewer. The ndarray result has leading
eigenvalue approximately 0.874743573 nm**2. Independent NumPy covariance checks
protect the addon ndarray route. Other dtypes, tuples, bad lengths, nonfinite or
negative values require native test coverage; no further crash is asserted.

## What was refuted

The source, structures, atom selection, numeric values and CPU route are the
same in both calls. No optional GPU engine, Viewer synchronization, missing
coordinates or alternate units cause this failure. H5MSM 0.4 warnings remain
visible and do not explain the type failure.

## Scope and exclusions

No scientific change, weight conversion, implicit engine substitution or public
compatibility floor is introduced by the addon. Optional GPU qualification and
general molecular edits remain separate.

## Acceptance criteria

Normalize supported sequences/dtypes and validate dimensions, finite and
nonnegative weights before native execution. Define the all-zero-weight policy.
Guard list/tuple/ndarray equivalence, independent covariance/eigenvalue values,
nonconsecutive/repeated structures, squared-length units under nm/angstrom/pm,
and unchanged inputs in pytest. Invalid cases must reject before a foreign-function
failure or nonfinite covariance. Preserve eigenvector row/order and degeneracy
semantics. Do not change the scientific covariance definition to repair typing.

## Provenance

Linux, Python 3.14.7 in molsyssuite@uibcdf_3.14, base
3502232d802ee2927f6b6f5d19f0ae045777ecb5 with recorded working-tree changes.
Bundled pentalanine; CPU use_gpu=False. Source evidence, not an installed package.


## Implementation and verification — 2026-10-24

The public scientific boundary reuses `_private.weighted_geometry.prepare_weights`
to produce contiguous float64 arrays with finite, nonnegative values, matching
atom count and a positive sum. Individual zeros remain valid. PCA-specific checks
reject named models, complex weights and dimensional quantities; dimensionless
quantities are converted before normalization (100 percent means 1). Empty axes
and nonfinite coordinates reject before the Rust eigensolver. No Rust formula,
feature layout, eigenvector convention or weight-sum normalization changes.

The independent guard initially failed 60 cases and passed 36. After the repair,
100 contract cases plus the existing real pentalanine regression and two analytic
scientific-truth tests pass: **103 tests in 7.00 seconds**, pytest-receptor,
12 workers. The matrix includes lists, tuples, integer/float32/float64 arrays,
strided/read-only storage, zero individual weights, native MolSys/Structures and
H5MSM, repeated/nonconsecutive structures and atoms, one-structure degeneracy,
input preservation, all nine storage/presentation combinations of nm/angstrom/pm,
invalid input guards and absolute covariance scaling. NumPy supplies independent
covariances/eigenvalues; checks use orthonormality, reconstruction, covariance
residuals and projection variances rather than a specific degenerate basis.

The User Guide recipe also exposed an old manual-projection layout mismatch in
the toolbox notebook: interleaved Cartesian features were used with block-ordered
PCA vectors. Its projection now uses the same documented x/y/z blocks; both
plots remain. Course fixture defects discovered by actual execution have their
own identity under uibcdf/molsysmt#449. Source qualification does not qualify a
GPU kernel, installed package, release or out-of-core PCA.


## Closing qualification — 2026-10-24

The toolbox PCA notebook and all four path module-35 notebooks pass fresh Jupyter
execution. The weighted Cookbook Python blocks and the public docstring doctest
pass. The complete HTML documentation builds successfully; pre-existing MyST
heading/admonition warnings remain part of uibcdf/molsysmt#144. Ruff lint/format,
scientific-evidence validation and all fourteen fast release checks pass. Hosted
exact-source gates and the publication commit are recorded at issue closure.
No release, package publication or installed-pair qualification is implied.

Reproduce the native/scientific selection with:

```bash
python -m pytest tests/structure/principal_component_analysis tests/scientific_truth/structure/test_principal_component_analysis.py --receptor=llm -n 12
```
