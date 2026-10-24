---
summary: PCA rejects documented weight lists at the Rust boundary.
issue: uibcdf/molsysmt#448
status: open
opened: 2026-10-24
closed:
severity: medium
verification: reproduced
area: [structure, weights, rust]
guard:
normative:
blocked_by: []
supersedes: []
---

# PCA rejects documented weight lists at the Rust boundary

**Reported:** 2026-10-24 while receiving the structural-analysis addon under
uibcdf/molsysmt#421 / uibcdf/molsysviewer#264. Filing explicitly authorized.
**Status:** open. The scientific owner supplies normalization and validation;
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
