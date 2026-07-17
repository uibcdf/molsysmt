# Resolved: PCA Dimensional and Semantic Contract

**Resolved:** 2026-07-17

## Original defect

`molsysmt.structure.principal_component_analysis()` discarded coordinate units,
returned bare covariance eigenvalues, and described its first output loosely
enough that course notebooks treated eigenvectors as per-frame projections. The
backend also exposed NumPy's ascending eigenvalue order while the educational
material treated index zero as PC1.

## Accepted contract

- The first output contains dimensionless covariance eigenvectors, one per row.
- The second output contains eigenvalues with squared-coordinate units,
  normally `nm**2`.
- Both outputs are ordered from largest to smallest eigenvalue.
- The first row is PC1 and captures the largest mean squared dispersion.
- The function does not project trajectory frames onto the eigenvectors.

## Resolution evidence

The public wrapper restores squared-coordinate units and reverses the backend
eigendecomposition consistently for CPU and GPU paths. An analytic Scientific
Truth test uses eight sign combinations with population covariance
`diag(1, 4, 9)` and requires eigenvalues `(9, 4, 1) nm**2` with the corresponding
eigenvectors. The ordinary regression test and doctest enforce the same order
and unit contract.

The User Guide and all four course paths now call the outputs `eigenvectors`
and `eigenvalues` and no longer describe the first output as a projection. A
separate pending proposal records trajectory projection as possible future
functionality.
